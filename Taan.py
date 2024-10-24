import discord
import subprocess
import os
import psutil
import logging
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading

# Create a basic logger for the GUI
logger = logging.getLogger('discord_bot_logger')
logger.setLevel(logging.INFO)

# Initial preset games and their Steam App IDs
PRESET_GAMES = {
    "CS GO": 730,
    "Dota 2": 570,
    "Apex Legends": 1172470,
    "Among Us": 945360
}

# GUI Setup
class DiscordBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Game Discord Bot")

        # Set grid weights for resizing
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(5, weight=1)

        # Discord Token Input
        tk.Label(root, text="Discord Bot Token:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.token_entry = tk.Entry(root, width=50)
        self.token_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        # Steam Executable Path Input
        tk.Label(root, text="Steam Executable Path:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.steam_path_entry = tk.Entry(root, width=50)
        self.steam_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        # Add game button
        self.add_game_button = tk.Button(root, text="Add Game", command=self.add_game_input)
        self.add_game_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create a frame for the scrollable area
        self.game_frame = tk.Frame(root)
        self.game_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Scrollable area for games
        self.game_canvas = tk.Canvas(self.game_frame)
        self.scrollbar = tk.Scrollbar(self.game_frame, orient="vertical", command=self.game_canvas.yview)
        self.scrollable_frame = tk.Frame(self.game_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.game_canvas.configure(
                scrollregion=self.game_canvas.bbox("all")
            )
        )

        self.game_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.game_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.game_canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.game_frame.grid_rowconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(0, weight=1)

        # Button to add new games to the preset dropdown dynamically
        self.extend_button = tk.Button(root, text="Add New Preset Game", command=self.add_preset_game)
        self.extend_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Log display area (scrollable)
        self.log_area = scrolledtext.ScrolledText(root, width=70, height=10, state='disabled')
        self.log_area.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        # Data for the dynamically added games
        self.game_data = []

    # Method to add new game input fields
    def add_game_input(self):
        row = len(self.game_data)

        # Voice Channel ID input
        tk.Label(self.scrollable_frame, text=f"Voice Channel ID (Game {row+1}):").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        channel_entry = tk.Entry(self.scrollable_frame, width=20)
        channel_entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        # Dropdown for preset games (updated dynamically)
        preset_games_combobox = ttk.Combobox(self.scrollable_frame, values=list(PRESET_GAMES.keys()), state="readonly")
        preset_games_combobox.grid(row=row, column=2, padx=10, pady=5, sticky="w", ipadx=10)
        preset_games_combobox.set("Select Game")

        # Custom Steam App ID input
        tk.Label(self.scrollable_frame, text="Custom Steam App ID (Optional):").grid(row=row, column=3, padx=10, pady=5, sticky="w")
        app_id_entry = tk.Entry(self.scrollable_frame, width=10)
        app_id_entry.grid(row=row, column=4, padx=10, pady=5, sticky="w")

        # Minimum Players input
        tk.Label(self.scrollable_frame, text="Min Players:").grid(row=row, column=5, padx=10, pady=5, sticky="w")
        min_players_entry = tk.Entry(self.scrollable_frame, width=5)
        min_players_entry.grid(row=row, column=6, padx=10, pady=5, sticky="w")

        self.game_data.append((channel_entry, preset_games_combobox, app_id_entry, min_players_entry))

    # Method to extend the preset games dropdown with a new game
    def add_preset_game(self):
        # Create a pop-up window to take game name and Steam App ID
        new_game_window = tk.Toplevel(self.root)
        new_game_window.title("Add New Preset Game")

        # Input for new game name
        tk.Label(new_game_window, text="Game Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        game_name_entry = tk.Entry(new_game_window, width=30)
        game_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Input for new game's Steam App ID
        tk.Label(new_game_window, text="Steam App ID:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        app_id_entry = tk.Entry(new_game_window, width=30)
        app_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        def add_new_game():
            game_name = game_name_entry.get()
            steam_app_id = app_id_entry.get()
            if game_name and steam_app_id.isdigit():
                PRESET_GAMES[game_name] = int(steam_app_id)
                self.log_message(f"Added new game '{game_name}' with Steam App ID {steam_app_id}.")
                new_game_window.destroy()
            else:
                self.log_message("Invalid input. Please enter a valid game name and Steam App ID.")

        # Button to confirm adding the new game
        add_button = tk.Button(new_game_window, text="Add Game", command=add_new_game)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Method to display logs in the GUI
    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.yview(tk.END)
        self.log_area.config(state='disabled')

    # Start the bot in a separate thread
    def start_bot(self):
        token = self.token_entry.get()
        steam_path = self.steam_path_entry.get()

        games = []
        for channel_entry, preset_combobox, app_id_entry, min_players_entry in self.game_data:
            preset_game = preset_combobox.get()
            custom_app_id = app_id_entry.get()

            # Use preset game ID if selected, otherwise use the custom Steam App ID
            if preset_game in PRESET_GAMES:
                steam_app_id = PRESET_GAMES[preset_game]
            elif custom_app_id:
                steam_app_id = custom_app_id
            else:
                self.log_message("Error: No valid Steam App ID provided.")
                return

            games.append({
                'channel_id': channel_entry.get(),
                'app_id': steam_app_id,
                'min_players': int(min_players_entry.get())
            })

        if token and steam_path and games:
            # Run the bot in a separate thread to keep the GUI responsive
            threading.Thread(target=run_discord_bot, args=(token, steam_path, games, self.log_message), daemon=True).start()

# Discord bot implementation
def run_discord_bot(token, steam_path, games, log_function):
    intents = discord.Intents.default()
    intents.members = True
    intents.guilds = True
    intents.voice_states = True

    client = discord.Client(intents=intents)

    # Function to launch a game from Steam
    def launch_game(steam_app_id):
        log_function(f"Attempting to launch game with Steam App ID {steam_app_id}...")

        # Check if Steam is already running
        steam_running = any('steam.exe' in p.name() for p in psutil.process_iter())

        if not steam_running:
            log_function("Steam is not running. Starting Steam and launching the game...")
            try:
                subprocess.Popen([steam_path, f'steam://rungameid/{steam_app_id}'])
                log_function(f"Game {steam_app_id} launched via Steam.")
            except Exception as e:
                log_function(f"Failed to launch Steam or game: {e}")
        else:
            log_function(f"Steam is already running, launching the game {steam_app_id}...")
            try:
                subprocess.Popen([steam_path, f'steam://rungameid/{steam_app_id}'])
                log_function(f"Game {steam_app_id} launched.")
            except Exception as e:
                log_function(f"Error launching game {steam_app_id}: {e}")

    @client.event
    async def on_ready():
        log_function(f'Logged in as {client.user}')

    @client.event
    async def on_voice_state_update(member, before, after):
        for game in games:
            channel_id = game['channel_id']
            steam_app_id = game['app_id']
            min_players = game['min_players']

            # Check if user joined the correct voice channel for the game
            if after.channel and str(after.channel.id) == channel_id:
                # Get the channel by its ID
                channel = client.get_channel(int(channel_id))

                # Check how many members are in the channel
                if len(channel.members) >= min_players:
                    log_function(f'{len(channel.members)} members joined the channel for game {steam_app_id}!')
                    launch_game(steam_app_id)

    client.run(token)

# Set up the GUI application
root = tk.Tk()
app = DiscordBotGUI(root)

# Run the GUI loop
root.mainloop()
