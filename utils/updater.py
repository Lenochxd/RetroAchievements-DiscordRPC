from . import get_config, log
from .restart import restart_program
import requests
import os
import tempfile
import subprocess
import webbrowser

version_file = "version.txt"

def get_actual_version() -> str:
    """
    Get the actual version of the application from the version file.
    """
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            return f.read().strip().removeprefix("v")
    return "1.0.0"  # Default version if file doesn't exist

def check_for_updates() -> bool | str:
    """
    Check for updates by comparing the current version with the latest version from GitHub.
    """
    config = get_config()
    
    # Get the actual version of the application from the version file.
    current_version = get_actual_version()
    
    # Get the latest version from the GitHub repository
    github_repo = config.get("github_repo", "Lenochxd/RetroAchievements-DiscordRPC")
    try:
        response = requests.get(f"https://api.github.com/repos/{github_repo}/releases/latest")
        response.raise_for_status()
        latest_version = response.json()["tag_name"].removeprefix("v")
    except requests.RequestException as e:
        log.error(f"Error checking for updates: {e}")
        return
    
    if current_version != latest_version:
        log.info(f"New version available: {latest_version}")
        # Create a cache file to store the latest version
        cache_latest_version_path = os.path.join(tempfile.gettempdir(), "RARPC_latest_version.txt")
        with open(cache_latest_version_path, "w", encoding="utf-8") as f:
            f.write(latest_version)
        return latest_version
    else:
        log.info("You are using the latest version.")
        return False

def install_update() -> None:
    """
    Download and install the latest version of the application.
    """
    config = get_config()
    
    # Get the latest version from the GitHub repository
    github_repo = config.get("github_repo", "Lenochxd/RetroAchievements-DiscordRPC")
    try:
        response = requests.get(f"https://api.github.com/repos/{github_repo}/releases/latest")
        response.raise_for_status()
        assets = response.json()["assets"]
        download_url = next((asset["browser_download_url"] for asset in assets if asset["name"].endswith(".msi")), None)

        if not download_url:
            log.error("No suitable MSI file found in the release assets. Opening the releases page...")
            releases_page_url = f"https://github.com/{github_repo}/releases"
            try:
                webbrowser.open(releases_page_url)
            except Exception as e:
                log.error(f"Failed to open the releases page: {e}")
            return
    except requests.RequestException as e:
        log.error(f"Error downloading update: {e}")
        return
    
    
    # Download the update
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Create a temporary file to save the update
        temp_file_path = os.path.join(tempfile.gettempdir(), "RARPC_update.msi")
        with open(temp_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Install the update using msiexec
        subprocess.run(["msiexec", "/i", temp_file_path, "/quiet", "/norestart"], check=True)
        
        log.success("Update installed successfully!")
    except requests.RequestException as e:
        log.error(f"Error downloading update: {e}")
    except subprocess.CalledProcessError as e:
        log.error(f"Error installing update: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    
    # Restart the program after installation
    restart_program()
