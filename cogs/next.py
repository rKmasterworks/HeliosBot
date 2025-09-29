import discord
from discord.ext import commands
import json
import os
import datetime

NAMES = ["Iben", "Paulius", "Leo"]
STATE_FILE = "data/next.json"

def get_next_state():
	if not os.path.exists(STATE_FILE):
		return {"index": 0, "date": None}
	with open(STATE_FILE, "r") as f:
		return json.load(f)

def set_next_state(index, date):
	with open(STATE_FILE, "w") as f:
		json.dump({"index": index, "date": date}, f)

class NextCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(name="next", description="Who is next for Badehus duty?")
	async def next(self, ctx):
		today = datetime.datetime.now()
		weekday = today.weekday()  # 0=Monday, 6=Sunday
		if weekday >= 5:
			await ctx.respond("No one is at the department on weekends (Saturday/Sunday).", ephemeral=True)
			return
		state = get_next_state()
		last_date = state.get("date")
		idx = state.get("index", 0)
		today_str = today.strftime("%Y-%m-%d")
		# Only advance if it's a new weekday
		if last_date != today_str:
			idx = (idx + 1) % len(NAMES) if last_date else idx  # Don't advance on first run
			set_next_state(idx, today_str)
		name = NAMES[idx % len(NAMES)]
		await ctx.respond(f"Next is: {name}", ephemeral=True)

def setup(bot):
	bot.add_cog(NextCog(bot))
