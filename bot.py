

import discord
from discord.ext import commands
import asyncio
import json
from config import TOKEN, PREFIX, BOT_NAME, BOT_DESCRIPTION
from commands import Commands
from events import on_ready, on_message, on_reaction_add, on_command_error
from tasks import change_status, auto_promo

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, description=BOT_DESCRIPTION)

# Setup tasks
bot.tasks = {
    'change_status': change_status,
    'auto_promo': auto_promo
}

# Register events
@bot.event
async def on_ready():
    await on_ready(bot)

@bot.event
async def on_message(message):
    await on_message(message, bot)
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    await on_reaction_add(reaction, user, bot)

@bot.event
async def on_command_error(ctx, error):
    await on_command_error(ctx, error)

# Register commands
bot.add_cog(Commands(bot))

# Jalankan bot
if __name__ == '__main__':
    print(f"🚀 Memulai {BOT_NAME} - Customer Service Discord yang Kreatif!")
    print("📝 Pastikan sudah mengganti TOKEN dengan token bot Discord Anda!")
    print("🔗 Invite bot ke server dengan permission 'Send Messages', 'Read Message History', dan 'Use Slash Commands'")
    
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ ERROR: Token Discord tidak valid!")
        print("📋 Cara mendapatkan token:")
        print("1. Buka https://discord.com/developers/applications")
        print("2. Buat aplikasi baru atau pilih yang sudah ada")
        print("3. Pergi ke tab 'Bot' dan copy token")
        print("4. Ganti 'your_discord_bot_token_here' dengan token tersebut")