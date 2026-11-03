import discord
from discord import app_commands
from discord.ext import commands
import requests
import time

BIN_ID = "https://api.jsonbin.io/v3/b/6ae95ee3ac6210605a679435"
API_KEY = "$2a$10$AuX5EfW.TJthVBUsPC7DY.Z9ZceMkoJYP18sRM9HrNbiwc.xx92Kq"
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {"X-Master-Key": API_KEY}

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Verifică statusul calculatoarelor online.")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            res = requests.get(URL, headers=HEADERS, timeout=5)
            if res.status_code != 200:
                await interaction.followup.send("❌ Nu s-au putut prelua datele din cloud.", ephemeral=True)
                return

            pc_data = res.json().get("record", {})
            embed = discord.Embed(title="🖥️ Stare PC-uri Conectate", color=discord.Color.green())
            acum = time.time()

            if not pc_data:
                embed.description = "Niciun PC înregistrat."
            else:
                for nume, info in pc_data.items():
                    ts = info.get("timestamp", 0) if isinstance(info, dict) else 0
                    # Dacă calculatorul a trimis semnal în ultimele 45 de secunde, apare Online
                    stare = "🟢 Online" if (acum - ts <= 45) else "🔴 Offline"
                    embed.add_field(name=nume, value=stare, inline=True)

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"Eroare: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(StatusCog(bot))
