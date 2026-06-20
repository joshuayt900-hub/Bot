from discord import app_commands

def register(bot):

    @bot.tree.command(name="ping")
    async def ping(interaction):
        await interaction.response.send_message("🏓 Pong")

    @bot.tree.command(name="info")
    async def info(interaction):
        await interaction.response.send_message(f"🤖 {bot.user}")

    @bot.tree.command(name="kick")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(interaction, member, reason="Kein Grund"):
        await member.kick(reason=reason)
        await interaction.response.send_message("👢 gekickt")

    @bot.tree.command(name="ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(interaction, member, reason="Kein Grund"):
        await member.ban(reason=reason)
        await interaction.response.send_message("🔨 gebannt")