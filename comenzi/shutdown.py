import discord
from discord import app_commands
from discord.ext import commands
import os

class ShutdownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shutdown", description="Închide calculatorul local.")
    async def shutdown(self, interaction: discord.Interaction):
        await interaction.response.send_message("⚠️ Se închide PC-ul în 30 secunde...", ephemeral=True)
        os.system("shutdown /s /t 30")

async def setup(bot):
    await bot.add_cog(ShutdownCog(bot))
