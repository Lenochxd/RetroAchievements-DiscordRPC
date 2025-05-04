# RetroAchievements-DiscordRPC

RetroAchievements-DiscordRPC is a simple app that allows RetroAchievements rich presence to be tracked on Discord's rich presence.

<div align="center">

  <img src="https://i.imgur.com/1J6yQp5.png" alt="example" width="55%" height="55%">
  
  [![GitHub License](https://img.shields.io/github/license/Lenochxd/RetroAchievements-DiscordRPC)](https://github.com/Lenochxd/RetroAchievements-DiscordRPC/blob/master/LICENSE)
  [![GitHub release (latest by date)](https://img.shields.io/github/v/release/Lenochxd/RetroAchievements-DiscordRPC.svg?style=flat)](https://github.com/Lenochxd/RetroAchievements-DiscordRPC/releases)
  [![Stars](https://img.shields.io/github/stars/Lenochxd/RetroAchievements-DiscordRPC?style=flat)](https://github.com/Lenochxd/RetroAchievements-DiscordRPC)
  [![GitHub issues](https://img.shields.io/github/issues/Lenochxd/RetroAchievements-DiscordRPC.svg?style=flat)](https://github.com/Lenochxd/RetroAchievements-DiscordRPC/issues)
  [![Discord](https://img.shields.io/discord/391919052563546112?style=flat&logo=Discord&logoColor=fff&label=Discord&color=5e6ae8&link=https%3A%2F%2Fdiscord.gg%2FtUPsYHAGfm)](https://discord.gg/tUPsYHAGfm)
</div>

## Installation

You can install RetroAchievements-DiscordRPC in two ways:

1. **Using the MSI Installer**:
   - Download the installer file named `RARPC-<version>-win64.msi` (e.g., `RARPC-1.0.0-win64.msi`) from the [Releases Page](https://github.com/Lenochxd/RetroAchievements-DiscordRPC/releases).
   - Run the installer and follow the on-screen instructions.

2. **Using the Portable Version**:
   - Download the portable version named `RARPC-win-amd64-portable.zip` from the [Releases Page](https://github.com/Lenochxd/RetroAchievements-DiscordRPC/releases).
   - Extract the contents of the ZIP file to a folder of your choice.
   - Run the `RARPC.exe` file to start the application.

## First-Time Setup

On the first run, a popup window will appear asking you to set up your RetroAchievements account. You will need to provide:

- **Username**: Your RetroAchievements username.
- **API Key**: Your RetroAchievements API key.

A button will be available in the popup to redirect you to the [RetroAchievements Settings Page](https://retroachievements.org/settings), where you can easily copy your API key.

<div align="center">
   <img src="https://i.imgur.com/LZVWlMH.png" alt="First-Time Setup Window" width="270px">
</div>

## Settings

The settings for RetroAchievements-DiscordRPC are stored in the `config.yml` file. Below is a list of available settings and their descriptions:

### Configurable via Tray Icon

- **Activity Title**: Choose between `RetroAchievements` and `RetroArch` for the activity title.
- **Change Sleeping Time**: Adjust the time interval (in seconds) for fetching updates. Options include 10s, 15s, 20s, etc.
- **Force Presence**: Enable or disable forcing the presence even if offline.
- **Start on Startup**: Enable or disable starting the application on system startup.
- **Edit RA Infos**: Update your RetroAchievements username and API key.
- **Check for Updates**: Check for and install updates if available.

### Experimental (Manual Configuration Only)

These settings are experimental and must be added manually to the `config.yml` file:

- **`presence_timeout`**: Time in seconds to keep the presence active if the status doesn't update.
  - Default: `900` seconds (15 minutes)
- **`github_repo`**: The GitHub repository URL for checking updates.
  - Default: `Lenochxd/RetroAchievements-DiscordRPC`
- **`discord_client_id`**: The Discord client ID for the application name to be displayed. 
  - Default: `1337553980779266078` (retroachievements)

## Development

To set up a development environment:

1. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

2. **Run the Script**:
   ```bash
   python main.py
   ```

3. **Build Portable Executable and MSI Installer**:
   - Ensure you have Python 3.11 installed.
   - Run the `build.bat` script.
   - This will generate both the portable version and the MSI installer in the `dist` directory.
