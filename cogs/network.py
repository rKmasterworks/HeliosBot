import discord
from discord.ext import commands
from discord import app_commands
import subprocess
import requests
from utils.helper import require_helios_category

class Network(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Ping a host and get the result.")
    @require_helios_category
    async def ping(self, interaction: discord.Interaction, host: str):
        try:
            # Defer response to avoid timeout
            await interaction.response.defer(ephemeral=True)
            # Windows ping: -n 4
            result = subprocess.run(["ping", "-n", "4", host], capture_output=True, text=True, timeout=10)
            output = result.stdout or result.stderr
            if len(output) > 1900:
                output = output[:1900] + "..."
            await interaction.followup.send(f"```{output}```", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="ipinfo", description="Get info about an IP address.")
    @require_helios_category
    async def ipinfo(self, interaction: discord.Interaction, ip: str):
        # Try to respond quickly with ephemeral message
        url = f"http://ip-api.com/json/{ip}"
        try:
            resp = requests.get(url, timeout=8)
            data = resp.json()
            if data.get("status") != "success":
                await interaction.response.send_message("Could not fetch info for this IP.", ephemeral=True)
                return
            embed = discord.Embed(title=f"IP Info: {ip}", color=discord.Color.green())
            embed.add_field(name="Country", value=data.get("country", "N/A"), inline=True)
            embed.add_field(name="City", value=data.get("city", "N/A"), inline=True)
            embed.add_field(name="ISP", value=data.get("isp", "N/A"), inline=True)
            embed.add_field(name="Organization", value=data.get("org", "N/A"), inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Network(bot))
