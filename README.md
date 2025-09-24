# Helios Discord Bot

Helios is a modular Discord bot built with discord.py and slash commands.

## Features
- `/teacherpassword`: Generates a random teacher password (14 characters, Norwegian words + digits) and sends it as a hidden (ephemeral) message.
- `/studentpassword`: Generates a random student password (8 characters, Norwegian words + digits) and sends it as a hidden (ephemeral) message.
- `/ping <host>`: Pings a given host and returns the result.
- `/ipinfo <ip>`: Fetches information about an IP address (country, city, ISP, organization).
- `/help`: Shows available commands in an embed.
- `/uptime`: Shows how long Helios has been online (hidden message).

## Setup
1. Clone the repository and install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the root directory:
   ```env
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```
 3. Create a `data/words.json` file containing a list of Norwegian words:
    ```json
    {
      "words": ["hund", "katt", "sol", ...]
    }
    ```
    The bot will not function without this file.
4. Run the bot:
   ```sh
   python bot.py
   ```

## Structure
- `bot.py`: Main bot file, loads cogs and commands.
- `config.py`: Loads bot token from `.env`.
- `cogs/`: Contains modular command files (`passwords.py`, `network.py`, `uptime.py`).
- `requirements.txt`: Required Python packages.
- `data/words.json`: List of Norwegian words for password generation.

## Requirements
- discord.py
- requests
- python-dotenv

## Notes
- Make sure your bot token is kept secret and never shared publicly.
- The bot uses slash commands; invite it with the `applications.commands` scope.
- You must provide a `data/words.json` file for the password commands to work.
