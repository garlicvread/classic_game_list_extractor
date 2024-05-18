"""
Game Titles Extractor
=====================

Author: Kim, Che Pill
Contact: ceo@aidall.tech
Date: 05-18-2024
Description: This application allows users to select a game console and directory to extract game titles from .zip files.
"""

import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk, messagebox
from datetime import datetime
import webbrowser

class GameTitlesExtractor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Titles Extractor")
        self.console_entries = {}
        self.selected_console = None
        self.output_files = {}

        # List of popular home and handheld game consoles
        self.popular_consoles = [
            "Atari 2600",
            "Nintendo Entertainment System (NES)",
            "Super Nintendo Entertainment System (SNES)",
            "Nintendo 64",
            "Sega Genesis",
            "Sega Saturn",
            "Sega Dreamcast",
            "Sony PlayStation",
            "Sony PlayStation 2",
            "Nintendo GameCube",
            "Nintendo Wii",
            "Xbox",
            "Xbox 360",
            "Nintendo Game Boy (GBC)",
            # "Nintendo Game Boy Color",
            "Nintendo Game Boy Advance",
            "Nintendo DS",
            "Nintendo 3DS",
            "PlayStation Portable (PSP)",
            "PlayStation Vita",
            "Atari Lynx",
            "Neo Geo Pocket",
            "TurboGrafx-16 Portable"
        ]

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Console Name:").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)

        self.console_var = tk.StringVar()
        self.console_dropdown = ttk.Combobox(self, textvariable=self.console_var, state='readonly', width=35)
        self.console_dropdown['values'] = self.popular_consoles
        self.console_dropdown.grid(column=1, row=0, padx=10, pady=5)
        self.console_dropdown.bind("<Configure>", self.adjust_combobox_width)

        self.select_console_button = ttk.Button(self, text="Select Console", command=self.select_console)
        self.select_console_button.grid(column=2, row=0, padx=10, pady=5, sticky=tk.W)

        self.console_frame = ttk.Frame(self)
        self.console_frame.grid(column=0, row=1, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.directory_label = ttk.Label(self.console_frame, text="Directory:")
        self.directory_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        self.directory_entry = ttk.Entry(self.console_frame, width=50)
        self.directory_entry.grid(column=1, row=0, padx=5, pady=5)
        self.directory_button = ttk.Button(self.console_frame, text="Browse", command=self.browse_directory)
        self.directory_button.grid(column=2, row=0, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(self, length=400, mode='determinate')
        self.progress_bar.grid(column=0, row=2, columnspan=3, padx=10, pady=10)

        self.start_button = ttk.Button(self, text="Start Process", command=self.start_process)
        self.start_button.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

        self.open_folder_button = ttk.Button(self, text="Go to Outcome Folder", command=self.open_folder, state='disabled')
        self.open_folder_button.grid(column=0, row=4, padx=10, pady=10)

        self.open_file_button = ttk.Button(self, text="Open Outcome File", command=self.open_file, state='disabled')
        self.open_file_button.grid(column=1, row=4, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(self, width=70, height=15, wrap=tk.WORD)
        self.log_text.grid(column=0, row=5, columnspan=3, padx=10, pady=10)

    def adjust_combobox_width(self, event):
        self.console_dropdown.configure(width=len(max(self.popular_consoles, key=len)))

    def select_console(self):
        console_name = self.console_var.get()
        if console_name:
            self.selected_console = console_name
            self.console_entries[console_name] = self.console_entries.get(console_name, "")
            self.select_console_button.config(text="Change Console")
            self.log_message(f"Selected console: {console_name}")
        else:
            messagebox.showinfo("Info", "You need to select a console first!")
            self.log_message("Info: No console selected.")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
            if self.selected_console:
                self.console_entries[self.selected_console] = directory
                self.log_message(f"Selected directory for {self.selected_console}: {directory}")
            else:
                messagebox.showinfo("Info", "You need to select a console first!")
                self.log_message("Info: Attempt to select a directory without a selected console.")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_game_titles(self, directory):
        game_titles = []
        try:
            for file_name in os.listdir(directory):
                if file_name.endswith('.zip'):
                    game_titles.append(file_name)
        except FileNotFoundError:
            self.log_message(f"Error: The directory '{directory}' does not exist.")
        except PermissionError:
            self.log_message(f"Error: Permission denied to access the directory '{directory}'.")
        except Exception as e:
            self.log_message(f"An unexpected error occurred while accessing the directory '{directory}': {e}")
        return game_titles

    def write_game_titles(self, directory, console_name, game_titles):
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            file_name = f"{console_name}_{date_str}.txt"
            file_path = os.path.join(directory, file_name)
            self.log_message(f"Attempting to write file to: {file_path}")
            if game_titles:  # Only write the file if there are game titles
                with open(file_path, 'w') as file:
                    file.write(f"Console: {console_name}\n")
                    file.write(f"Warning: We do not know if the list below is actual {console_name} game titles or not. Please double-check by yourself.\n\n")
                    for title in game_titles:
                        file.write(title + '\n')
                self.log_message(f"Game titles have been written to {file_path}")
                self.output_files[console_name] = file_path
                self.open_folder_button.config(state='normal')
                self.open_file_button.config(state='normal')
            else:
                self.log_message(f"No game titles found in the directory: {directory}")
        except FileNotFoundError:
            self.log_message(f"Error: The file path '{file_path}' does not exist.")
        except PermissionError:
            self.log_message(f"Error: Permission denied to write to the file '{file_path}'.")
        except Exception as e:
            self.log_message(f"An unexpected error occurred while writing to the file '{file_path}': {e}")

    def start_process(self):
        self.log_message(f"Debug: Start process initiated. Selected console: {self.selected_console}")
        self.log_message(f"Debug: Console entries: {self.console_entries}")
        if not self.selected_console or not self.console_entries.get(self.selected_console):
            messagebox.showinfo("Info", "You need to select a console and a directory first!")
            self.log_message("Info: Attempt to start process without selecting both console and directory.")
            return

        self.progress_bar['value'] = 0
        total_consoles = len(self.console_entries)
        for idx, (console_name, directory) in enumerate(self.console_entries.items()):
            self.log_message(f"Processing {console_name} with directory '{directory}'...")
            if not os.path.exists(directory):
                self.log_message(f"Error: The directory '{directory}' does not exist.")
                continue
            game_titles = self.get_game_titles(directory)
            self.write_game_titles(directory, console_name, game_titles)
            self.progress_bar['value'] += (100 / total_consoles)

        self.log_message("Process completed.")
        self.progress_bar['value'] = 100

    def open_folder(self):
        if self.selected_console and self.selected_console in self.output_files:
            directory = os.path.dirname(self.output_files[self.selected_console])
            webbrowser.open(directory)

    def open_file(self):
        if self.selected_console and self.selected_console in self.output_files:
            file_path = self.output_files[self.selected_console]
            webbrowser.open(file_path)

if __name__ == "__main__":
    app = GameTitlesExtractor()
    app.mainloop()
