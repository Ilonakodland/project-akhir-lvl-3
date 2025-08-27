# tasks.py

import discord
import random
from discord.ext import tasks
from utils import create_embed

# Status bot yang akan dirotasi
bot_statuses = [
    discord.Game("🛒 Melayani pelanggan setia"),
    discord.Activity(type=discord.ActivityType.watching, name="📦 Pesanan masuk"),
    discord.Activity(type=discord.ActivityType.listening, name="💬 Pertanyaan pelanggan"),
    discord.Streaming(name="🛍️ Belanja hemat di Semua Bisa Kamu Beli", url="https://www.twitch.tv/discord")
]

@tasks.loop(minutes=30)
async def change_status(bot):
    """Mengganti status bot setiap 30 menit"""
    await bot.change_presence(activity=random.choice(bot_statuses))

@tasks.loop(hours=24)
async def auto_promo(bot):
    """Mengirim promo otomatis setiap hari"""
    # Cari channel dengan nama "promo" atau "general"
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name in ["promo", "general", "diskon"]:
                embed = create_embed(
                    title="🎉 PROMO HARI INI! 🎉",
                    description="Jangan lewatkan promo spesial hari ini hanya di Semua Bisa Kamu Beli!",
                    color=discord.Color.purple()
                )
                embed.add_field(
                    name="🔥 FLASH SALE",
                    value="Diskon hingga 50% untuk produk elektronik pilihan!",
                    inline=False
                )
                embed.add_field(
                    name="💰 CASHBACK",
                    value="Cashback 15% untuk pembayaran menggunakan e-wallet!",
                    inline=False
                )
                embed.add_field(
                    name="🎁 BONUS POINT",
                    value="Dapatkan 2x poin loyalty untuk setiap pembelian hari ini!",
                    inline=False
                )
                embed.set_footer(text="Promo berlaku hanya hari ini! Segera kunjungi toko kami.")
                
                await channel.send(embed=embed)
                break