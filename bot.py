import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import setup_db, simpan_pertanyaan, ambil_pertanyaan_pending, close_pertanyaan
from FAQ import faq

# Load token dari .env
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Setup database saat mulai
setup_db()

@bot.event
async def on_ready():
    print(f'Bot aktif sebagai {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    answered = False

    for key in faq.keys():
        if key in content:
            await message.channel.send(faq[key])
            answered = True
            break

    if not answered:
        simpan_pertanyaan(str(message.author), message.content)
        await message.channel.send(
            "Terima kasih atas pertanyaanmu! Kami akan teruskan ke tim spesialis dan segera menghubungimu."
        )

    await bot.process_commands(message)

@bot.command(name='helpbot')
async def help_bot(ctx):
    text = (
        "Halo! Saya Bot Bantuan Semarak untuk toko Semua Bisa Kamu Beli.\n"
        "Saya bisa menjawab pertanyaan umum secara otomatis.\n"
        "Pertanyaan rumit akan diteruskan ke tim spesialis.\n"
        "Gunakan bot ini untuk memudahkan layanan pelanggan."
    )
    await ctx.send(text)

@bot.command(name='list_escalations')
@commands.has_permissions(administrator=True)
async def list_escalations(ctx):
    rows = ambil_pertanyaan_pending()
    if not rows:
        await ctx.send("Tidak ada pertanyaan yang perlu eskalasi saat ini.")
    else:
        response = "Pertanyaan yang perlu eskalasi:\n"
        for row in rows:
            response += f"ID {row[0]} - Dari: {row[1]}\nPertanyaan: {row[2]}\n\n"
        await ctx.send(response[:2000])

@bot.command(name='close_escalation')
@commands.has_permissions(administrator=True)
async def close_escalation(ctx, id: int):
    close_pertanyaan(id)
    await ctx.send(f"Pertanyaan dengan ID {id} telah ditandai selesai.")

if __name__ == '__main__':
    bot.run(TOKEN)
