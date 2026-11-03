import discord
from discord import app_commands
from discord.ext import commands
import requests
import time

BIN_ID = "6ae95ee3ac6210605a679435"
API_KEY = "$2a$10$pXpnrii6P4eFEwd5JS9UP.BCpv8ocjkYM0MgkLju6zUHdwyayfKm"
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {"X-Master-Key": API_KEY}

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Afișează doar calculatoarele online în rețea.")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            res = requests.get(URL, headers=HEADERS, timeout=4)
            if res.status_code != 200:
                await interaction.followup.send("Nu s-au putut prelua datele din cloud.", ephemeral=True)
                return

            resp_json = res.json()
            pc_data = resp_json.get("record", resp_json)
            if not isinstance(pc_data, dict):
                pc_data = {}

            embed = discord.Embed(title="🟢 PC-uri Active Online", color=discord.Color.green())
            acum = time.time()
            online_count = 0

            for nume, info in pc_data.items():
                if isinstance(info, dict):
                    ts = info.get("timestamp", 0)
                    if acum - ts <= 15:
                        online_count += 1
                        embed.add_field(name=f"🖥️ {nume}", value="🟢 Online", inline=False)

            if online_count == 0:
                embed.description = "Niciun calculator online momentan."
                embed.color = discord.Color.red()

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"Eroare: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(StatusCog(bot))
