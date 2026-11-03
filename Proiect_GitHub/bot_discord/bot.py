import discord
from discord.ext import commands
import json
import os

if not os.path.exists("config.json"):
    print("[-] Fișierul config.json nu există!")
    exit()

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config.get("token")

class ControlBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        if os.path.exists("comenzi"):
            for filename in os.listdir("comenzi"):
                if filename.endswith(".py"):
                    await self.load_extension(f"comenzi.{filename[:-3]}")
                    print(f"[+] S-a încărcat comanda: {filename}")

        synced = await self.tree.sync()
        print(f"[+] S-au sincronizat {len(synced)} comenzi Slash.")

bot = ControlBot()

@bot.event
async def on_ready():
    print(f"[+] Botul este conectat ca: {bot.user}")

if __name__ == "__main__":
    bot.run(TOKEN)
