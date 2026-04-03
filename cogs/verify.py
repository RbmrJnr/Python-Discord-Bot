import discord
from discord.ext import commands
from discord import app_commands # necessário para comandos slash
import aiohttp
import os

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bloxlink_token = os.getenv("BLOXLINK_TOKEN")
        self.cargo_visitante_id = int(os.getenv("CARGOVISITANTE_ID"))
        self.cargo_aluno_id = int(os.getenv("CARGOALUNO_ID"))
        self.canal_aviso_id = int(os.getenv("ID_CANAL_AVISO"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role2 = member.guild.get_role(self.cargo_visitante_id) #pegando cargo
        aviso = self.bot.get_channel(self.canal_aviso_id) 
        await aviso.send(f"{member.mention}, Digite '/verify' para verificar")
        
        if role2:
            try:
                await member.add_roles(role2)
            except discord.Forbidden:
                print('Sem permissão')

    # Olha o decorador novo aqui!
    @app_commands.command(name="verify")
    async def verify(self, interaction: discord.Interaction): # Trocamos ctx por interaction
        role = interaction.guild.get_role(self.cargo_aluno_id)
        role2 = interaction.guild.get_role(self.cargo_visitante_id)
        
        # interaction.user substitui o ctx.author
        if self.cargo_aluno_id in [r.id for r in interaction.user.roles]:
            await interaction.response.send_message(f"{interaction.user.mention}, você já possui o cargo de {role.name}", ephemeral=True)
            return # interaction.response para comandos slash, ao inves de ctx.comando
        
        user_id = interaction.user.id
        guild_id = interaction.guild.id
        url = f"https://api.blox.link/v4/public/guilds/{guild_id}/discord-to-roblox/{user_id}"
        headers = {"Authorization": self.bloxlink_token}

        await interaction.response.defer(ephemeral=True) #aqui manda o bot responder logo, pois a api demora um pouco

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as res_bloxlink:
                if res_bloxlink.status == 404:
                    await interaction.followup.send("❌ Você não possui conta verificada. Acesse https://blox.link/ para vincular! 🚫")
                    return
                elif res_bloxlink.status != 200:
                    await interaction.followup.send("❌ Não foi possível consultar o Bloxlink no momento. 🚫")
                    return
        
        try:
            if role:
                await interaction.user.add_roles(role)
                if role2 in interaction.user.roles:
                    await interaction.user.remove_roles(role2)
                await interaction.followup.send(f"✅ Verificação Concluída! Seja Bem vindo {interaction.user.display_name}")
        except discord.errors.Forbidden:
            await interaction.followup.send("Sem Permissão para gerenciar cargos.")

async def setup(bot):
    await bot.add_cog(Verify(bot))