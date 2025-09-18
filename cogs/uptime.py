import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Store the bot start time (UTC, timezone-aware)
        self.start_time = datetime.datetime.now(datetime.timezone.utc)

    @app_commands.command(name="uptime", description="Shows how long Helios has been active.")
    async def uptime(self, interaction: discord.Interaction):
        # Restrict to 'Helios Labs' category
        category = getattr(interaction.channel, 'category', None)
        if not category or category.name != "Helios Labs":
            await interaction.response.send_message(
                "This command can only be used in the 'Helios Labs' category.", ephemeral=True)
            return
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - self.start_time

        days, seconds = delta.days, delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

        await interaction.response.send_message(
            f"🟢 Helios has been online for **{uptime_str}**", ephemeral=True
        )
        

async def setup(bot):
    await bot.add_cog(Uptime(bot))
