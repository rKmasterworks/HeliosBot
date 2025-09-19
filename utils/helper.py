import json
import os

def category_helios(interaction):
    """
    Returns True if the command is used in a channel under the 'Helios Labs' category.
    Otherwise returns False.
    """
    category = getattr(interaction.channel, 'category', None)
    return category and category.name == "Helios Labs"

def require_helios_category(func):
    """
    Decorator for Discord commands to restrict usage to 'Helios Labs' category.
    Sends an ephemeral message and returns if used elsewhere.
    Usage: @require_helios_category above async command methods.
    """
    import functools
    @functools.wraps(func)
    async def wrapper(self, interaction, *args, **kwargs):
        if not category_helios(interaction):
            await interaction.response.send_message(
                "This command can only be used in the 'Helios Labs' category.", ephemeral=True)
            return
        return await func(self, interaction, *args, **kwargs)
    return wrapper

def load_words():
    try:
        with open('data/words.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Check if data is a dict with `words` key or a list
        if isinstance(data, dict) and 'words' in data:
            words = data['words']
        elif isinstance(data, list):
                words = data
        else:
            # Unexpected structure
            print("Error: words.json has unexpected structure.")
            return []
        # Filter out empty strings
        return [w.strip() for w in words if isinstance(w, str) and w.strip()]
    except FileNotFoundError:
        print("Error: data/words.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error: data/words.json contains invalid JSON.")
        return []
    except Exception as e:
        print(f"Unexpected error loading words: {e}")
        return []