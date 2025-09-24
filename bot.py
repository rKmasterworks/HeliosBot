import discord
from discord.ext import commands
from discord import app_commands, Embed
import os
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class HeliosBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents, application_id=None)

    async def setup_hook(self):
        # Dynamically load all cogs in the cogs folder
        for filename in os.listdir("cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        # Sync slash commands
        await self.tree.sync()

bot = HeliosBot()

@bot.tree.command(name="help", description="Show available commands")
async def help_command(interaction: discord.Interaction):
    embed = Embed(title="Helios Bot Help", color=discord.Color.blurple())
    embed.add_field(name="/teacherpassword", value="Generate a teacher password and receive it as a hidden message.", inline=False)
    embed.add_field(name="/studentpassword", value="Generate a student password and receive it as a hidden message.", inline=False)
    embed.add_field(name="/ping <host>", value="Ping a host and get the result (sent via DM).", inline=False)
    embed.add_field(name="/ipinfo <ip>", value="Get info about an IP address (hidden message).", inline=False)
    embed.add_field(name="/uptime", value="Shows how long Helios has been online (hidden message).", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)
