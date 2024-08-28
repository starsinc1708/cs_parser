import os
import pandas as pd
from datetime import datetime

class FileManager:
    def __init__(self, base_filename="cs2run_data"):
        self.filename = f"{base_filename}_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        self.df = self.load_existing_data()

    def load_existing_data(self):
        """Load existing data from the Excel file or create a new DataFrame if the file does not exist."""
        if os.path.exists(self.filename):
            return pd.read_excel(self.filename)
        else:
            return pd.DataFrame(columns=["round_id", "winner_number", "color", "multiplier", "multiplier_winner_number", "random_number", "timestamp"])

    def save_to_excel(self):
        """Save the current DataFrame to the Excel file."""
        if self.df is not None:
            self.df.to_excel(self.filename, index=False)

    def append_data(self, new_data):
        """Append new round data to the DataFrame and save it."""
        self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
        self.save_to_excel()

    def count_colors(self, num=0):
        """Count the occurrences of each color in the most recent `num` rounds."""
        if num == 0:
            recent_games = self.df
        else:
            recent_games = self.df.tail(num)
        return {
            "синий": recent_games[recent_games["color"] == "синий"].shape[0],
            "зеленый": recent_games[recent_games["color"] == "зеленый"].shape[0],
            "оранжевый": recent_games[recent_games["color"] == "оранжевый"].shape[0]
        }
