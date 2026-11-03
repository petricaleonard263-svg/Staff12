import discord
from discord import app_commands
from discord.ext import commands
import os
import json
import time

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Afișează toate PC-urile online.")
    async def status(self, interaction: discord.Interaction):
        pc_file = "pc_online.json"
        if not os.path.exists(pc_file):
            await interaction.response.send_message("Nu există date înregistrate.", ephemeral=True)
            return

        try:
            with open(pc_file, "r", encoding="utf-8") as f:
                pc_data = json.load(f)
        except Exception:
            await interaction.response.send_message("Eroare la citirea fișierului de status.", ephemeral=True)
            return

        embed = discord.Embed(title="🖥️ Stare Calculatoare", color=discord.Color.green())
        acum = time.time()
        
        if not pc_data:
            embed.description = "Niciun PC înregistrat."
        else:
            for nume, info in pc_data.items():
                if isinstance(info, dict):
                    ts = info.get("timestamp", 0)
                else:
                    ts = info
                
                stare = "🟢 Online" if (acum - ts <= 60) else "🔴 Offline"
                embed.add_field(name=nume, value=stare, inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(StatusCog(bot))
