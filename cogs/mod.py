import discord
from discord.ext import commands
import datetime

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_spam_control = {}
        self.user_warns = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        user_id = message.author.id
        now = datetime.datetime.now()

        if user_id not in self.user_spam_control:
            self.user_spam_control[user_id] = []

        self.user_spam_control[user_id].append(now)
        self.user_spam_control[user_id] = [t for t in self.user_spam_control[user_id] if (now - t).total_seconds() < 5]

        if(len(self.user_spam_control[user_id])) > 5:
            self.user_warns[user_id] = self.user_warns.get(user_id, 0) + 1
            contagem = self.user_warns[user_id]

            if contagem == 3:
                await message.channel.send("⚠️ **Este é seu último aviso** ⚠️", delete_after=5) 
            elif contagem > 3:
                try:
                    timepunition = datetime.timedelta(minutes=10)
                    await message.author.timeout(timepunition, reason="Spam ")
                    await message.channel.send(f"🚫 {message.author.mention} foi silenciado por 10 minutos (Spam).")
                    self.user_warns[user_id] = 0 
                except discord.Forbidden:
                    print("Sem permissão para dar timeout.")
            else:
                await message.channel.send(f"⚠️ {message.author.mention}, pare de fazer spam! ({contagem}/3)", delete_after=5)
                try:
                    await message.delete()
                except:
                    pass

            self.user_spam_control[user_id] = []

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, i: int):
        if i <= 0:
            await ctx.send("A quantidade deve ser maior que 0!", delete_after=5)
            return

        deleted = await ctx.channel.purge(limit=i + 1) 
        await ctx.send(f"✅ Limpeza concluída! **{len(deleted) - 1}** mensagens foram removidas.", delete_after=10)

    @clear.error 
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument): 
            await ctx.send("❌ Uso incorreto! Exemplo: `!clear 10`", delete_after=5)
        elif isinstance(error, commands.MissingPermissions): 
            await ctx.send(f"⚠️ {ctx.author.mention} Você não tem permissão para gerenciar mensagens!", delete_after=5)
        elif isinstance(error, commands.BadArgument): 
            await ctx.send("❌ Por favor, digite um número válido.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Mod(bot))