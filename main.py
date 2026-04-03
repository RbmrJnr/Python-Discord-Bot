import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

class RibBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'): #abrir pasta cogs
            if filename.endswith('.py'): #verifica se é .py
                await self.load_extension(f'cogs.{filename[:-3]}') #carrega
        
        # Isso sincroniza os comandos slash
        await self.tree.sync()
        print("tudo ok")

bot = RibBot()

@bot.event
async def on_ready():
    print(f'Tudo certo {bot.user}')

bot.run(TOKEN_BOT)