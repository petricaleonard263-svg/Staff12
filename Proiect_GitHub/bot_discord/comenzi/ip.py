import discord
from discord import app_commands
from discord.ext import commands
import os
import json
import time

class IPCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ip", description="Afișează IP-ul public, privat și numele complet al unui PC.")
    @app_commands.describe(nume="Numele exact al calculatorului")
    async def ip(self, interaction: discord.Interaction, nume: str):
        pc_file = "pc_online.json"
        
        if not os.path.exists(pc_file):
            await interaction.response.send_message("Nu există niciun PC înregistrat momentan.", ephemeral=True)
            return

        try:
            with open(pc_file, "r", encoding="utf-8") as f:
                pc_data = json.load(f)
        except Exception as e:
            await interaction.response.send_message(f"Eroare la citirea datelor: {e}", ephemeral=True)
            return

        if nume not in pc_data:
            await interaction.response.send_message(f"❌ Nu am găsit niciun PC cu numele **{nume}** sau acesta este offline.", ephemeral=True)
            return

        info = pc_data[nume]
        
        if isinstance(info, dict):
            ip_privat = info.get("ip_privat", "Indisponibil")
            ip_public = info.get("ip_public", "Indisponibil")
            ultimul_semnal = info.get("timestamp", 0)
        else:
            ip_privat = "Indisponibil"
            ip_public = "Indisponibil"
            ultimul_semnal = info

        status_online = "🟢 Online" if (time.time() - ultimul_semnal <= 60) else "🔴 Offline"

        embed = discord.Embed(title=f"🔍 Informații despre PC", color=discord.Color.blue())
        embed.add_field(name="Nume Complet PC", value=f"`{nume}`", inline=False)
        embed.add_field(name="IP Privat (Rețea Locală)", value=f"`{ip_privat}`", inline=True)
        embed.add_field(name="IP Public (Internet)", value=f"`{ip_public}`", inline=True)
        embed.add_field(name="Status", value=status_online, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(IPCog(bot))
