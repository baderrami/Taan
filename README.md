
# 🎮 Taan طعّان: Automate Game Launch Based on Discord Voice Channel Activity

## 📜 Introduction

**Taan طعّان** is a Python application designed to automate the launch of games based on user activity in Discord voice channels. The bot monitors specific voice channels in your gaming server, and when a certain number of users join a channel, it automatically launches the corresponding game via Steam.

This solution is ideal for gamers who want to streamline their gaming experience. Instead of manually launching games, the bot takes care of everything when the required number of players is ready!

## 🎯 Goal

The goal of this project is to:
- Monitor voice channels in a Discord server.
- Automatically launch games from Steam when a predefined number of users join the corresponding voice channels.
- Support multiple games with unique configurations (custom games or preset games like CS: GO, Dota 2, Apex Legends, and more).
- Provide a simple and intuitive GUI for managing these settings.

## 🛠️ Prerequisites

To successfully run this project, ensure you have the following prerequisites:

### 1. Discord Application Setup
You need to create a Discord bot via the Discord Developer Portal to interact with your server:

- **Create a Discord bot**:
  - Go to [Discord Developer Portal](https://discord.com/developers/applications).
  - Create a new application and then navigate to the **Bot** section.
  - Click **Add Bot** and generate a bot token (you will use this in the application).
  - Enable **Privileged Intents** (for `Server Members Intent` and `Presence Intent`).

### 2. Steam Account and Games
You need to have a Steam account with installed games that the bot will be able to launch. The application uses **Steam App IDs** to launch specific games.

### 3. System Requirements
This bot is designed to run on:
- **Windows** (since it uses the `subprocess.Popen()` method to interact with Steam and requires Windows paths).
- **Python 3.6 or higher**.
  
## 🧰 Installation

Follow these steps to set up the project on your local machine:

### Step 1: Clone the Repository
```bash
git clone https://github.com/baderrami/Taan.git
cd Taan
```

### Step 2: Install Required Python Packages
Make sure Python 3.6 or higher is installed on your system. Then, install the necessary packages via `pip`:
```bash
pip install discord.py psutil
```

### Step 3: Configure the Discord Bot
You will need to enter your **Discord bot token** and **Steam executable path** into the GUI.

1. Run the application.
   ```bash
   python Taan.py
   ```
2. Enter the **Discord Bot Token** and **Steam Executable Path**. Example Steam path:
   ```bash
   C:\Program Files (x86)\Steam\steam.exe
   ```

3. Add multiple games, configure the voice channel IDs, and start the bot.

### Step 4: Run the Application
Once everything is set up, click "Start Bot" in the GUI. The bot will start monitoring the voice channels and launch games accordingly.

## 📝 Code Documentation

### Project Structure:
```
.
├── README.md
├── Taan.py
└── LICENSE
```

### Key Components:

#### 1. **GUI Creation** (using `tkinter`):
The GUI allows users to configure:
- **Discord bot token** and **Steam executable path**.
- Add/remove multiple games with their respective voice channel IDs, minimum players, and Steam App IDs.

#### 2. **Discord Bot Functionality** (using `discord.py`):
The bot monitors Discord voice channels for user activity and triggers the launch of games when certain conditions are met (e.g., the number of users in the channel reaches the required minimum).

- **Event handler `on_voice_state_update()`**:
  - This method triggers every time a user joins or leaves a voice channel. It checks the user count in the channel and launches the appropriate game when the conditions are met.

#### 3. **Game Launching** (via `subprocess`):
Games are launched using Steam's URI protocol. The `subprocess.Popen()` method is used to call Steam with the specific game’s App ID, like so:
```python
subprocess.Popen([steam_path, f'steam://rungameid/{steam_app_id}'])
```

#### 4. **Dynamic Game List Extension**:
The application allows the addition of custom games, dynamically updating the preset dropdown with new game names and their respective Steam App IDs.

### Code Walkthrough

- **`DiscordBotGUI` class**: Handles all GUI operations (input forms, logs, dynamic dropdowns).
  - **`add_game_input()`**: Adds a new game entry with options for voice channel ID, preset game selection, and custom Steam App IDs.
  - **`add_preset_game()`**: Allows the user to add custom preset games to the dropdown dynamically.
  
- **`run_discord_bot()`**: Initializes the Discord bot, sets up intents, and starts listening for voice state changes (when users join/leave voice channels).

- **`launch_game()`**: Launches the specified game from Steam based on its App ID.

## 💻 Usage Example

1. **Configure the Bot**:
   - Enter your **Discord Bot Token**.
   - Provide the **Steam Executable Path**.
   - Add games with their corresponding voice channels and set the required minimum players.
   
2. **Monitor Voice Channels**:
   - The bot will listen for users joining the configured channels.
   - When the number of users reaches the minimum, the game associated with the channel will launch automatically.

## 🏷️ Adding More Games

If you want to extend the list of preset games, you can dynamically add games via the GUI:

- Click on **"Add New Preset Game"** in the GUI.
- Enter the **Game Name** and its corresponding **Steam App ID**.
- This game will now appear in the dropdown for easy selection in the future.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🖥️ Contributions

Contributions, issues, and feature requests are welcome! Feel free to submit a pull request or open an issue.

Best regards

Rami
