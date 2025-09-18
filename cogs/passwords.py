
import discord
from discord.ext import commands

# Discord imports for bot and command functionality
import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

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
    for _ in range(10):  # Try up to 10 times to find a good combination
        num_words = random.choice([2, 3])
        # Pick unique words if possible
        if len(words) >= num_words:
            selected_words = random.sample(words, k=num_words)
        else:
            selected_words = [random.choice(words) for _ in range(num_words)]
        word_part = ''.join(selected_words)
        # Always add at least one digit at the end
        digit_count = max(1, max_len - len(word_part))
        digit_part = ''.join(random.choices('0123456789', k=digit_count))
        password = word_part + digit_part
        # If too long, remove last word and try again
        if len(password) > max_len and num_words > 1:
            selected_words = selected_words[:-1]
            word_part = ''.join(selected_words)
            digit_count = max(1, max_len - len(word_part))
            digit_part = ''.join(random.choices('0123456789', k=digit_count))
            password = word_part + digit_part
        # Return if password is correct length and has at least one digit
        if len(password) == max_len and any(c.isdigit() for c in password[-digit_count:]):
            password = password.capitalize()
            return password
    # Fallback: use one word + digits
    word = random.choice(words)
    digit_count = max(1, max_len - len(word))
    digit_part = ''.join(random.choices('0123456789', k=digit_count))
    password = word + digit_part
    password = password.capitalize()
    return password[:max_len]
class Passwords(commands.Cog):
    """
    Cog for password generation using Norwegian words and digits.
    Provides the /password command, restricted to 'Helios Labs' category.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="password", description="Generate a Norwegian word-based password and receive it as a hidden message.")
    async def password(self, interaction: discord.Interaction):
        """
        Slash command to generate a password and send it as an ephemeral (hidden) message in the server.
        Only works in channels under the 'Helios Labs' category.
        """
        # Restrict command usage to 'Helios Labs' category
        category = getattr(interaction.channel, 'category', None)
        if not category or category.name != "Helios Labs":
            await interaction.response.send_message(
                "This command can only be used in the 'Helios Labs' category.", ephemeral=True)
            return
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
