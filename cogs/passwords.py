
import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os
from utils.helper import require_helios_category

# Path to the words.json file containing Norwegian words
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'words.json')

def load_words():
    """
    Load Norwegian words from the JSON file.
    Supports both a plain array or an object with a 'words' key.
    Returns a list of non-empty strings.
    """
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict) and 'words' in data:
            words = data['words']
        else:
            words = data
        return [str(w).strip() for w in words if isinstance(w, str) and w.strip()]
    except Exception:
        # If file is missing or invalid, return empty list
        return []

def generate_password():
    """
    Generate a password of exactly 14 characters using Norwegian words and digits.
    Algorithm:
      1. Pick 2–3 random words from the list (never cut words).
      2. Add at least 1 random digit at the end (pad with more digits if needed).
      3. If too long, remove last word and try again.
      4. Capitalize the first letter.
    Returns the password as a string, or None if word list is missing.
    """
    words = load_words()
    if not words:
        return None
    max_len = 14
    for _ in range(10):
        num_words = random.choice([2, 3])
        selected = random.sample(words, k=min(num_words, len(words)))
        word_part = ''.join(selected)
        digit_count = max(1, max_len - len(word_part))
        password = word_part + ''.join(random.choices('0123456789', k=digit_count))
        # If too long, try with one less word
        if len(password) > max_len and len(selected) > 1:
            selected = selected[:-1]
            word_part = ''.join(selected)
            digit_count = max(1, max_len - len(word_part))
            password = word_part + ''.join(random.choices('0123456789', k=digit_count))
        if len(password) == max_len and any(c.isdigit() for c in password[-digit_count:]):
            return password.capitalize()
    # Fallback: one word + digits
    word = random.choice(words)
    digit_count = max(1, max_len - len(word))
    password = word + ''.join(random.choices('0123456789', k=digit_count))
    return password.capitalize()[:max_len]
class Passwords(commands.Cog):
    """
    Cog for password generation using Norwegian words and digits.
    Provides the /password command, restricted to 'Helios Labs' category.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="password", description="Generate a Norwegian word-based password and receive it as a hidden message.")
    @require_helios_category
    async def password(self, interaction: discord.Interaction):
        """
        Slash command to generate a password and send it as an ephemeral (hidden) message in the server.
        Only works in channels under the 'Helios Labs' category.
        """
        password = generate_password()
        if not password:
            await interaction.response.send_message("Could not load word list. Please contact the bot admin.", ephemeral=True)
            return
        # Send password in a code block for easy copying
        await interaction.response.send_message(
            f"Your generated password:\n```{password}```\n*(This message will disappear after a short time)*",
            ephemeral=True
        )

async def setup(bot):
    """
    Setup function to add this cog to the bot.
    """
    await bot.add_cog(Passwords(bot))
