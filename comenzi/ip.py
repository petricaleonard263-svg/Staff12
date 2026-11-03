import discord
from discord import app_commands
from discord.ext import commands
import os
import json
import time

class IPCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ip", description="Afișează detaliile IP ale unui PC.")
    @app_commands.describe(nume="Numele PC-ului")
    async def ip(self, interaction: discord.Interaction, nume: str):
        pc_file = "pc_online.json"
        if not os.path.exists(pc_file):
            await interaction.response.send_message("Nu există PC-uri înregistrate.", ephemeral=True)
            return

        try:
            with open(pc_file, "r", encoding="utf-8") as f:
                pc_data = json.load(f)
        except Exception as e:
            await interaction.response.send_message(f"Eroare: {e}", ephemeral=True)
            return

        if nume not in pc_data:
            await interaction.response.send_message(f"❌ PC-ul **{nume}** nu a fost găsit.", ephemeral=True)
            return

        info = pc_data[nume]
        if isinstance(info, dict):
            ip_privat = info.get("ip_privat", "N/A")
            ip_public = info.get("ip_public", "N/A")
            ultimul = info.get("timestamp", 0)
        else:
            ip_privat = ip_public = "N/A"
            ultimul = info

        stare = "🟢 Online" if (time.time() - ultimul <= 60) else "🔴 Offline"

        embed = discord.Embed(title="🔍 Informații PC", color=discord.Color.blue())
        embed.add_field(name="Nume PC", value=f"`{nume}`", inline=False)
        embed.add_field(name="IP Privat", value=f"`{ip_privat}`", inline=True)
        embed.add_field(name="IP Public", value=f"`{ip_public}`", inline=True)
        embed.add_field(name="Status", value=stare, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(IPCog(bot))
