import discord
from discord.ext import commands
import json
import random
import asyncio
import os

class Edu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quiz")
    async def quiz(self, ctx):
        try:
            pasta_cogs = os.path.dirname(os.path.abspath(__file__))
            pasta_raiz = os.path.dirname(pasta_cogs)
            caminho_arquivo = os.path.join(pasta_raiz, 'questions.json')
            
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                jsonperguntas = json.load(f)
        except FileNotFoundError:
            print("Não foi Possível abrir o arquivo json")
            await ctx.send("Erro", delete_after=5)
            return

        item = random.choice(jsonperguntas) 
        pergunta = item["pergunta"] 
        opcoes = item["opcoes"] 
        res_correta = str(item["correta"]) 

        op = ""
        for i, opcao in enumerate(opcoes, start=1):
            op += f"**{i}.** {opcao}\n"

        embed = discord.Embed( 
            title="🧠 QUIZ DO PYTHON", 
            description=f"**{pergunta}**\n\n{op}", 
            color=discord.Color.gold() 
        ) 
        embed.set_footer(text="Você tem 15 segundos para responder o número correto!")
        
        await ctx.send(embed=embed)

        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author and msg.content in ["1", "2", "3", "4"] 

        try:
            res_user = await self.bot.wait_for('message', timeout=15.0, check=check)

            if res_user.content == res_correta:
                await ctx.send(f"✅ Parabéns {ctx.author.mention}! Você acertou.")
            else:
                texto_certo = opcoes[int(res_correta) - 1] 
                await ctx.send(f"❌ Errado, {ctx.author.mention}. A resposta correta era a **{res_correta}** ({texto_certo}).")

        except asyncio.TimeoutError:
            await ctx.send(f"Tempo esgotado, {ctx.author.mention}! Tente Novamente.")

async def setup(bot):
    await bot.add_cog(Edu(bot))