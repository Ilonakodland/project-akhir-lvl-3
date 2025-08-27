import discord


# ===== KONFIGURASI BOT =====
TOKEN = "your_discord_bot_token_here"  # Ganti dengan token bot Discord Anda

# ===== FAQ DATABASE =====
faq_database = {
    'pembayaran': {
        'keywords': ['pembayaran', 'bayar', 'payment', 'transfer'],
        'answer': '💳 **Metode Pembayaran Kami:**\n• Transfer Bank (BCA, Mandiri, BRI, BNI)\n• E-wallet (OVO, Dana, GoPay, ShopeePay)\n• Kartu Kredit/Debit\n• QRIS\n\n*Pembayaran akan diverifikasi dalam 1x24 jam*'
    },
    'pengiriman': {
        'keywords': ['pengiriman', 'kirim', 'shipping', 'delivery'],
        'answer': '🚚 **Info Pengiriman:**\n• Waktu: 1-3 hari kerja setelah pembayaran\n• Ekspedisi: JNE, J&T, SiCepat, AnterAja\n• Lacak paket melalui website ekspedisi\n• Barang dikemas dengan bubble wrap'
    },
    'ongkir': {
        'keywords': ['ongkir', 'ongkos kirim', 'biaya kirim'],
        'answer': '📦 **Ongkos Kirim:**\n• Dihitung otomatis saat checkout\n• Berdasarkan berat dan jarak\n• **GRATIS ONGKIR** untuk pembelian > Rp 100.000\n• Estimasi biaya bisa dicek di website'
    },
    'garansi': {
        'keywords': ['garansi', 'warranty', 'jaminan'],
        'answer': '🛡️ **Garansi Produk:**\n• 1 tahun garansi resmi\n• Berlaku untuk kerusakan pabrik\n• Tidak berlaku: kerusakan karena pemakaian salah\n• Klaim garansi melalui customer service'
    },
    'return': {
        'keywords': ['return', 'tukar', 'kembalikan', 'retur'],
        'answer': '↩️ **Kebijakan Return:**\n• 7 hari setelah terima barang\n• Kondisi: barang utuh, belum dipakai\n• Alasan: rusak/cacat, salah kirim, tidak sesuai\n• Biaya return ditanggung toko jika kesalahan dari kami'
    },
    'kontak': {
        'keywords': ['kontak', 'contact', 'hubungi', 'cs'],
        'answer': '📞 **Hubungi Customer Service:**\n• WhatsApp: 0812-3456-7890\n• Email: cs@semuabisakamubeli.com\n• Instagram: @semuabisakamubeli\n• Jam kerja: 09:00-17:00 WIB (Senin-Sabtu)'
    },
    'promo': {
        'keywords': ['promo', 'diskon', 'sale', 'discount'],
        'answer': '🎉 **Promo Terkini:**\n• Diskon 20% untuk member baru\n• Flash sale setiap Jumat 12.00 WIB\n• Cashback 10% untuk pembelian > Rp 500.000\n• Follow IG @semuabisakamubeli untuk info promo terbaru'
    },
    'produk': {
        'keywords': ['produk', 'barang', 'item', 'katalog'],
        'answer': '🛍️ **Katalog Produk:**\n• Elektronik (HP, Laptop, Aksesoris)\n• Fashion (Pakaian, Sepatu, Tas)\n• Rumah Tangga (Perabot, Dekorasi)\n• Kecantikan (Skincare, Makeup)\n\n*Lihat katalog lengkap di website kami*'
    }
}

# ===== DATABASE PERTANYAAN SEDERHANA =====
questions_storage = []

# ===== SETUP BOT =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ===== FUNGSI HELPER =====
def find_faq_answer(message_content):
    """Mencari jawaban FAQ berdasarkan kata kunci"""
    content_lower = message_content.lower()
    
    for category, data in faq_database.items():
        for keyword in data['keywords']:
            if keyword in content_lower:
                return data['answer']
    return None

def save_question(user, question):
    """Menyimpan pertanyaan yang tidak terjawab"""
    question_data = {
        'id': len(questions_storage) + 1,
        'user': str(user),
        'question': question,
        'status': 'pending'
    }
    questions_storage.append(question_data)
    return question_data['id']

# ===== EVENT HANDLERS =====
@bot.event
async def on_ready():
    print(f'🤖 Bot {bot.user} siap melayani toko Semua Bisa Kamu Beli!')
    print(f'📊 Bot aktif di {len(bot.guilds)} server')

@bot.event
async def on_message(message):
    # Skip pesan dari bot sendiri
    if message.author == bot.user:
        return
    
    # Skip jika pesan adalah command
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return
    
    # Cari jawaban FAQ
    faq_answer = find_faq_answer(message.content)
    
    if faq_answer:
        # Kirim jawaban FAQ dengan embed
        embed = discord.Embed(
            title="🏪 Semua Bisa Kamu Beli",
            description=faq_answer,
            color=0x00ff00
        )
        embed.set_footer(text="Customer Service Bot • Ketik !help untuk bantuan")
        await message.channel.send(embed=embed)
    else:
        # Simpan pertanyaan yang tidak terjawab
        question_id = save_question(message.author, message.content)
        
        embed = discord.Embed(
            title="📝 Pertanyaan Diterima",
            description="Terima kasih! Pertanyaan Anda telah kami terima dan akan dijawab oleh tim customer service.",
            color=0xffaa00
        )
        embed.add_field(
            name="📋 ID Pertanyaan", 
            value=f"#{question_id}", 
            inline=True
        )
        embed.add_field(
            name="💬 Pertanyaan Anda", 
            value=message.content[:200] + "..." if len(message.content) > 200 else message.content, 
            inline=False
        )
        embed.set_footer(text="Tim CS akan membalas dalam 1x24 jam")
        await message.channel.send(embed=embed)
    
    # Proses command jika ada
    await bot.process_commands(message)

# ===== COMMANDS =====
@bot.command(name='help')
async def help_command(ctx):
    """Menampilkan bantuan penggunaan bot"""
    embed = discord.Embed(
        title="🤖 Customer Service Bot",
        description="**Semua Bisa Kamu Beli** - Toko Online Terpercaya",
        color=0x0099ff
    )
    
    embed.add_field(
        name="💬 Kata Kunci FAQ",
        value="`pembayaran`, `pengiriman`, `ongkir`, `garansi`, `return`, `kontak`, `promo`, `produk`",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Commands untuk Semua User",
        value="`!help` - Bantuan ini\n`!faq` - Tampilkan semua FAQ\n`!contact` - Info kontak\n`!promo` - Info promo terkini",
        inline=False
    )
    
    embed.add_field(
        name="🔧 Commands untuk Admin",
        value="`!pending` - Lihat pertanyaan pending\n`!close [ID]` - Tutup pertanyaan\n`!stats` - Statistik bot",
        inline=False
    )
    
    embed.set_footer(text="Ketik pertanyaan langsung atau gunakan kata kunci FAQ!")
    await ctx.send(embed=embed)

@bot.command(name='faq')
async def show_faq(ctx):
    """Menampilkan semua FAQ"""
    embed = discord.Embed(
        title="❓ Frequently Asked Questions",
        description="Informasi lengkap tentang toko kami:",
        color=0x9932cc
    )
    
    faq_list = []
    for category, data in faq_database.items():
        # Ambil jawaban singkat untuk preview
        short_answer = data['answer'].split('\n')[0][:100]
        faq_list.append(f"**{category.title()}:** {short_answer}...")
    
    embed.add_field(
        name="📋 Daftar FAQ",
        value="\n".join(faq_list[:8]),  # Maksimal 8 FAQ
        inline=False
    )
    
    embed.set_footer(text="Ketik kata kunci untuk mendapat jawaban lengkap!")
    await ctx.send(embed=embed)

@bot.command(name='contact')
async def contact_info(ctx):
    """Menampilkan info kontak"""
    answer = faq_database['kontak']['answer']
    embed = discord.Embed(
        title="📞 Kontak Customer Service",
        description=answer,
        color=0x00ccff
    )
    await ctx.send(embed=embed)

@bot.command(name='promo')
async def promo_info(ctx):
    """Menampilkan info promo"""
    answer = faq_database['promo']['answer']
    embed = discord.Embed(
        title="🎉 Promo Terkini",
        description=answer,
        color=0xff6600
    )
    await ctx.send(embed=embed)

@bot.command(name='pending')
@commands.has_permissions(manage_messages=True)
async def show_pending(ctx):
    """Admin: Menampilkan pertanyaan pending"""
    pending_questions = [q for q in questions_storage if q['status'] == 'pending']
    
    if not pending_questions:
        embed = discord.Embed(
            title="✅ Tidak Ada Pertanyaan Pending",
            description="Semua pertanyaan sudah dijawab!",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="📋 Pertanyaan Pending",
        description=f"Total: {len(pending_questions)} pertanyaan belum dijawab",
        color=0xff6600
    )
    
    # Tampilkan 5 pertanyaan terakhir
    for q in pending_questions[-5:]:
        embed.add_field(
            name=f"ID #{q['id']} - {q['user']}",
            value=q['question'][:150] + "..." if len(q['question']) > 150 else q['question'],
            inline=False
        )
    
    if len(pending_questions) > 5:
        embed.set_footer(text=f"Menampilkan 5 pertanyaan terakhir dari {len(pending_questions)} total")
    
    await ctx.send(embed=embed)

@bot.command(name='close')
@commands.has_permissions(manage_messages=True)
async def close_question(ctx, question_id: int):
    """Admin: Tutup pertanyaan berdasarkan ID"""
    found = False
    for q in questions_storage:
        if q['id'] == question_id and q['status'] == 'pending':
            q['status'] = 'closed'
            found = True
            break
    
    if found:
        embed = discord.Embed(
            title="✅ Pertanyaan Ditutup",
            description=f"Pertanyaan ID #{question_id} telah ditandai selesai.",
            color=0x00ff00
        )
    else:
        embed = discord.Embed(
            title="❌ ID Tidak Ditemukan",
            description=f"Pertanyaan dengan ID #{question_id} tidak ditemukan atau sudah ditutup.",
            color=0xff0000
        )
    
    await ctx.send(embed=embed)

@bot.command(name='stats')
async def show_stats(ctx):
    """Menampilkan statistik bot"""
    pending_count = len([q for q in questions_storage if q['status'] == 'pending'])
    total_questions = len(questions_storage)
    
    embed = discord.Embed(
        title="📊 Statistik Bot Customer Service",
        color=0x00ccff
    )
    
    embed.add_field(name="🏪 Server", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 Total User", value=sum(guild.member_count for guild in bot.guilds), inline=True)
    embed.add_field(name="❓ Pertanyaan Pending", value=pending_count, inline=True)
    embed.add_field(name="📋 Total Pertanyaan", value=total_questions, inline=True)
    embed.add_field(name="📖 Kategori FAQ", value=len(faq_database), inline=True)
    embed.add_field(name="✅ Pertanyaan Selesai", value=total_questions - pending_count, inline=True)
    
    await ctx.send(embed=embed)

# ===== ERROR HANDLER =====
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Akses Ditolak",
            description="Anda tidak memiliki izin untuk menggunakan perintah ini.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Parameter Kurang",
            description="Perintah ini membutuhkan parameter tambahan. Ketik `!help` untuk bantuan.",
            color=0xff0000
        )
        await ctx.send(embed=embed)

# ===== JALANKAN BOT =====
if __name__ == '__main__':
    print("🚀 Memulai Discord Bot Customer Service...")
    print("📝 Pastikan sudah mengganti TOKEN dengan token bot Discord Anda!")
    print("🔗 Invite bot ke server dengan permission 'Send Messages' dan 'Use Slash Commands'")
    
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ ERROR: Token Discord tidak valid!")
        print("📋 Cara mendapatkan token:")
        print("1. Buka https://discord.com/developers/applications")
        print("2. Buat aplikasi baru atau pilih yang sudah ada")
        print("3. Pergi ke tab 'Bot' dan copy token")
        print("4. Ganti 'your_discord_bot_token_here' dengan token tersebut")