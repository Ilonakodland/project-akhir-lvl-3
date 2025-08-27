# events.py

import discord
from discord.ext import commands
from FAQ import find_faq_answer
from database import save_question, add_user_points
from utils import create_embed, truncate_text

async def on_ready(bot):
    """Event saat bot siap"""
    print(f'🤖 {bot.user} siap melayani toko Semua Bisa Kamu Beli!')
    print(f'📊 Bot aktif di {len(bot.guilds)} server')
    
    # Mulai task
    bot.tasks['change_status'].start()
    bot.tasks['auto_promo'].start()

async def on_message(message, bot):
    """Event saat ada pesan baru"""
    # Skip pesan dari bot sendiri
    if message.author == bot.user:
        return
    
    # Skip jika pesan adalah command
    if message.content.startswith(bot.command_prefix):
        return
    
    # Cari jawaban FAQ
    category, faq_answer, emoji = find_faq_answer(message.content)
    
    if faq_answer:
        # Kirim jawaban FAQ dengan embed yang menarik
        embed = create_embed(
            title=f"{emoji} Informasi {category.title()}",
            description=faq_answer,
            color=discord.Color.blue(),
            footer=f"Dijawab oleh {bot.user.name} • Ketik !help untuk bantuan"
        )
        
        # Tambahkan reaksi emoji
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("❤️")
        
        # Beri poin loyalty untuk user
        from config import POINTS_PER_QUESTION
        add_user_points(message.author.id, POINTS_PER_QUESTION)
    else:
        # Simpan pertanyaan yang tidak terjawab
        question_id = save_question(message.author, message.content)
        
        embed = create_embed(
            title="📝 Pertanyaan Diterima",
            description="Terima kasih! Pertanyaan Anda telah kami terima dan akan dijawab oleh tim customer service.",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="📋 ID Pertanyaan", 
            value=f"#{question_id}", 
            inline=True
        )
        embed.add_field(
            name="💬 Pertanyaan Anda", 
            value=truncate_text(message.content, 200), 
            inline=False
        )
        embed.set_footer(text="Tim CS akan membalas dalam 1x24 jam")
        
        # Tambahkan reaksi emoji
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("🙏")
        
        # Beri poin loyalty untuk user
        from config import POINTS_PER_QUESTION
        add_user_points(message.author.id, POINTS_PER_QUESTION * 2)

async def on_reaction_add(reaction, user, bot):
    """Event saat user menambahkan reaksi"""
    # Skip jika reaksi dari bot sendiri
    if user == bot.user:
        return
    
    # Jika user mereaksi pesan FAQ dengan ❤️
    if reaction.emoji == "❤️":
        # Beri poin loyalty tambahan
        add_user_points(user.id, 1)
        await reaction.message.channel.send(f"Terima kasih {user.mention}! Anda mendapatkan 1 poin loyalty! ❤️")

async def on_command_error(ctx, error):
    """Event saat terjadi error pada command"""
    if isinstance(error, commands.MissingPermissions):
        embed = create_embed(
            title="❌ Akses Ditolak",
            description="Anda tidak memiliki izin untuk menggunakan perintah ini.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = create_embed(
            title="❌ Parameter Kurang",
            description="Perintah ini membutuhkan parameter tambahan. Ketik `!help` untuk bantuan.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        # Abaikan error command not found
        pass