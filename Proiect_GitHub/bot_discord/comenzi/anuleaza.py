import discord
from discord import app_commands
from discord.ext import commands
import os

class AnuleazaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="anuleaza", description="Anulează o comandă de shutdown sau restart programată.")
    async def anuleaza(self, interaction: discord.Interaction):
        os.system("shutdown /a")
        await interaction.response.send_message("✅ Comanda de shutdown/restart a fost anulată.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AnuleazaCog(bot))
