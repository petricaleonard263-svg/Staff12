import discord
from discord import app_commands
from discord.ext import commands
import requests

BIN_ID = "6ae95ee3ac6210605a679435"
API_KEY = "$2a$10$pXpnrii6P4eFEwd5JS9UP.BCpv8ocjkYM0MgkLju6zUHdwyayfKm"
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {"X-Master-Key": API_KEY}

class IpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ip", description="Afișează detaliile de rețea (IPv4 / LAN și IP Public) pentru PC-uri.")
    async def ip(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            res = requests.get(URL, headers=HEADERS, timeout=4)
            if res.status_code != 200:
                await interaction.followup.send("❌ Nu s-au putut prelua datele din cloud.", ephemeral=True)
                return

            resp_json = res.json()
            pc_data = resp_json.get("record", resp_json)
            if not isinstance(pc_data, dict):
                pc_data = {}

            embed = discord.Embed(title="🌐 Informații Rețea PC-uri", color=discord.Color.orange())

            if not pc_data:
                embed.description = "Niciun PC înregistrat momentan."
            else:
                for nume, info in pc_data.items():
                    if isinstance(info, dict):
                        ip_privat = info.get("ip_privat", "N/A")
                        ip_public = info.get("ip_public", "N/A")
                        
                        valoare = (
                            f"**IPv4 (LAN / Privat):** `{ip_privat}`\n"
                            f"**IP Public:** `{ip_public}`"
                        )
                        embed.add_field(name=f"🖥️ PC: {nume}", value=valoare, inline=False)

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"Eroare: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(IpCog(bot))
