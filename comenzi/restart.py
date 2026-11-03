import discord
from discord import app_commands
from discord.ext import commands
import os

class RestartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="restart", description="Repornește calculatorul local.")
    async def restart(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔄 Se repornește PC-ul în 30 secunde...", ephemeral=True)
        os.system("shutdown /r /t 30")

async def setup(bot):
    await bot.add_cog(RestartCog(bot))
