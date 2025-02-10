from cx_Freeze import setup, Executable

import pathspec
import sys
import os
import subprocess
import shutil
import time

start_time = time.time()

sys.setrecursionlimit(10000)

version_cache_file = "version-cache.txt"

# Check for version argument
if "-v" in sys.argv or "--version" in sys.argv:
    version_index = sys.argv.index("-v") if "-v" in sys.argv else sys.argv.index("--version")
    if version_index + 1 < len(sys.argv):
        version = sys.argv[version_index + 1]
    else:
        raise ValueError("Version argument provided but no version specified.")
else:
    if os.path.exists(version_cache_file):
        with open(version_cache_file, "r", encoding="utf-8") as f:
            version = f.read().strip()
    else:
        version = input("Enter the version: ")
        with open(version_cache_file, "w", encoding="utf-8") as f:
            f.write(version)


def get_ignored_files():
    ignored_files = [
        ".git",
        ".gitignore",
        ".github",
        "build.bat",
        "requirements.txt",
        "tests/*",
        "*.py",
    ]

    with open(".gitignore", "r") as gitignore_file:
        for line in gitignore_file:
            line = line.strip()
            if line and not line.startswith("#"):
                if line.startswith("\\"):
                    line = line[1:]
                ignored_files.append(line)

    print("IGNORED:", ignored_files)
    return ignored_files

ignored_files = get_ignored_files()


def is_excluded(file_path):
    rel_path = os.path.relpath(file_path)
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignored_files)

    if spec.match_file(rel_path):
        # Check for negation patterns
        negation_spec = pathspec.PathSpec.from_lines("gitwildmatch", [line[1:] for line in ignored_files if line.startswith("!")])
        if negation_spec.match_file(rel_path):
            # print(f"NOT EXCLUDED (negation): {file_path}")
            return False
        # print(f"EXCLUDED: {file_path}")
        return True

    # print(f"NOT EXCLUDED: {file_path}")
    return False

def get_include_files():
    include_files = []
    for root, dirs, files in os.walk("."):
        # Check if the directory itself is excluded first
        if is_excluded(root):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if not is_excluded(file_path.replace('\\', '/')):
                include_files.append((file_path, file_path))
    return include_files


def sign_executable(file_path):
    signtool_path = r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe"
    timestamp_url = "http://timestamp.digicert.com"
    command = [
        signtool_path,
        "sign",
        "/a",
        "/fd", "SHA256",
        "/tr", timestamp_url,
        "/td", "SHA256",
        file_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to sign {file_path}: {result.stderr}")
    else:
        print(f"Successfully signed {file_path}")

def zip_build(build_dir):
    # Create a temporary directory outside the build directory to hold the build directory with the desired structure
    temp_dir = os.path.join("temp", "PortableBuild")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    # Move the build directory into the temporary directory
    shutil.move(build_dir, temp_dir)

    # Rename the directory inside PortableBuild to "RARPC"
    final_dir = os.path.join("temp", "PortableBuild")
    inner_dir = os.path.join(final_dir, os.listdir(final_dir)[0])
    new_inner_dir = os.path.join(final_dir, "RARPC")
    # Ensure the path doesn't exist before creating it
    if os.path.exists(new_inner_dir):
        shutil.rmtree(new_inner_dir)
    os.rename(inner_dir, new_inner_dir)

    # Create a zip file of the temporary directory
    zip_file = shutil.make_archive('RARPC-win-amd64-portable', 'zip', final_dir)

    # Move the zip file to the /dist directory
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    shutil.move(zip_file, os.path.join(dist_dir, os.path.basename(zip_file)))

    # Remove the PortableBuild directory
    shutil.rmtree(final_dir)

    print(f"Portable build zipped as '{os.path.join(dist_dir, os.path.basename(zip_file))}'")


if __name__ == "__main__":
    build_exe_options = {
        "excludes": ["cx_Freeze", "pathspec"],
        "packages": [],
        "zip_exclude_packages": [
        ],
        "zip_include_packages": "*",
        "include_msvcr": False,
        "include_files": get_include_files(),
    }

    bdist_msi_options = {
        "upgrade_code": "{7fbc1e14-31b1-41c4-a352-f1040e7b7050}",
        "add_to_path": True,
        "initial_target_dir": r"[ProgramFilesFolder]\RetroAchievementsRPC",
        "install_icon": "ra-icon.ico",
        "summary_data": {
            "author": "Jade Lenoch",
            "comments": "A simple way to use to display RetroAchievements activity as Discord rich presence",
            "keywords": "Discord RPC, RetroAchievements, RetroArch, Discord, RPC, Retro, Achievements, RetroAchievements.org",
        }
    }

    base = "Win32GUI" if sys.platform == "win32" else "gui"
    # base = 'console' if sys.platform=='win32' else None
    executables = [
        Executable(
            script="main.py",
            base=base,
            icon="ra-icon.ico",
            target_name="RARPC",
            shortcut_name="RARPC",
            shortcut_dir="ProgramMenuFolder",
            copyright="RARPC",
            trademarks="RARPC",
            manifest=None,
            uac_admin=False,
        ),
    ]

    setup(
        name="RARPC",
        description="RARPC",
        author="Jade Lenoch",
        author_email="contact.lenoch@gmail.com",
        url="https://github.com/Lenochxd/RetroAchievements-DiscordRPC",
        license="MIT",
        version=version,
        options={
            "build_exe": build_exe_options,
            "bdist_msi": bdist_msi_options,
        },
        executables=executables,
    )


    build_dir = f"build/exe.win-amd64-{sys.version_info.major}.{sys.version_info.minor}"
    
    # Sign the main executable
    sign_executable(os.path.join(build_dir, "RARPC.exe"))
    
    
    # Zip the build directory
    zip_build(build_dir)
    
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    
    print(f"Build done! {minutes}m {seconds}s")
