# commands.py

import discord
from discord.ext import commands
from FAQ import faq_database
from products import get_product_by_id, get_products_by_category, get_all_categories
from quiz import get_random_question
from database import (
    get_pending_questions, close_question, create_order, 
    get_user_points, add_user_points, use_user_points, get_bot_stats
)
from utils import (
    create_embed, format_price, format_datetime, truncate_text, 
    get_user_status, calculate_discount
)
from config import (
    COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR, COLOR_INFO,
    VIP_THRESHOLD, QUIZ_TIMEOUT_SECONDS, POINTS_PER_CORRECT_QUIZ
)

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx):
        """Menampilkan bantuan penggunaan bot"""
        embed = create_embed(
            title="🤖 SemarakBot - Customer Service",
            description="**Semua Bisa Kamu Beli** - Toko Online Terpercaya",
            color=COLOR_PRIMARY
        )
        
        embed.add_field(
            name="💬 Kata Kunci FAQ",
            value="`pembayaran`, `pengiriman`, `ongkir`, `garansi`, `return`, `kontak`, `promo`, `produk`",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Commands untuk Semua User",
            value="`!help` - Bantuan ini\n`!faq` - Tampilkan semua FAQ\n`!contact` - Info kontak\n`!promo` - Info promo terkini\n`!produk` - Lihat katalog produk\n`!points` - Cek poin loyalty\n`!quiz` - Ikuti kuis untuk dapat poin\n`!beli <id> <jumlah>` - Beli produk",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Commands untuk Admin",
            value="`!pending` - Lihat pertanyaan pending\n`!close <id>` - Tutup pertanyaan\n`!stats` - Statistik bot\n`!broadcast <pesan>` - Kirim pesan ke semua server\n`!addfaq <kategori> <jawaban>` - Tambah FAQ",
            inline=False
        )
        
        embed.set_footer(text="Ketik pertanyaan langsung atau gunakan kata kunci FAQ!")
        await ctx.send(embed=embed)

    @commands.command(name='faq')
    async def show_faq(self, ctx):
        """Menampilkan semua FAQ"""
        embed = create_embed(
            title="❓ Frequently Asked Questions",
            description="Informasi lengkap tentang toko kami:",
            color=COLOR_INFO
        )
        
        for category, data in faq_database.items():
            # Ambil jawaban singkat untuk preview
            short_answer = data['answer'].split('\n')[0][:100]
            embed.add_field(
                name=f"{data['emoji']} {category.title()}",
                value=short_answer + "...",
                inline=False
            )
        
        embed.set_footer(text="Ketik kata kunci untuk mendapat jawaban lengkap!")
        await ctx.send(embed=embed)

    @commands.command(name='contact')
    async def contact_info(self, ctx):
        """Menampilkan info kontak"""
        answer = faq_database['kontak']['answer']
        embed = create_embed(
            title="📞 Kontak Customer Service",
            description=answer,
            color=COLOR_SUCCESS
        )
        await ctx.send(embed=embed)

    @commands.command(name='promo')
    async def promo_info(self, ctx):
        """Menampilkan info promo"""
        answer = faq_database['promo']['answer']
        embed = create_embed(
            title="🎉 Promo Terkini",
            description=answer,
            color=COLOR_WARNING
        )
        await ctx.send(embed=embed)

    @commands.command(name='produk')
    async def show_products(self, ctx, category=None):
        """Menampilkan katalog produk"""
        if category:
            filtered_products = get_products_by_category(category)
            title = f"🛍️ Kategori {category.title()}"
        else:
            filtered_products = get_products_by_category('elektronik') + get_products_by_category('fashion') + get_products_by_category('kecantikan')
            title = "🛍️ Katalog Produk"
        
        if not filtered_products:
            categories = get_all_categories()
            await ctx.send(f"❌ Kategori '{category}' tidak ditemukan. Kategori yang tersedia: {', '.join(categories)}")
            return
        
        embed = create_embed(
            title=title,
            description=f"Total {len(filtered_products)} produk tersedia",
            color=COLOR_PRIMARY
        )
        
        for product in filtered_products:
            embed.add_field(
                name=f"ID: {product['id']} - {product['name']}",
                value=f"{format_price(product['price'])} | Stok: {product['stock']}\n{truncate_text(product['description'], 100)}",
                inline=False
            )
        
        embed.set_footer(text="Gunakan !beli <id> <jumlah> untuk membeli produk")
        await ctx.send(embed=embed)

    @commands.command(name='beli')
    async def buy_product(self, ctx, product_id: int, quantity: int = 1):
        """Membeli produk"""
        if quantity <= 0:
            await ctx.send("❌ Jumlah pembelian harus lebih dari 0!")
            return
        
        # Cari produk
        product = get_product_by_id(product_id)
        if not product:
            await ctx.send(f"❌ Produk dengan ID {product_id} tidak ditemukan! Gunakan !produk untuk melihat katalog.")
            return
        
        if product['stock'] < quantity:
            await ctx.send(f"❌ Stok tidak mencukupi! Stok tersedia: {product['stock']}")
            return
        
        # Buat pesanan
        order = create_order(ctx.author, product_id, quantity)
        if not order:
            await ctx.send("❌ Gagal membuat pesanan!")
            return
        
        # Hitung total dengan diskon jika ada
        total = order['total']
        discount = 0
        
        # Cek apakah user punya poin loyalty
        user_points = get_user_points(ctx.author.id)
        if user_points >= VIP_THRESHOLD:
            discount = calculate_discount(total, user_points)
            total -= discount
            use_user_points(ctx.author.id, VIP_THRESHOLD)
        
        # Tambahkan poin loyalty
        points_earned = int(total / 10000) * 5  # 5 poin untuk setiap 10.000
        add_user_points(ctx.author.id, points_earned)
        
        # Buat embed konfirmasi
        embed = create_embed(
            title="🛒 Pesanan Berhasil Dibuat!",
            description=f"Terima kasih {ctx.author.mention} telah berbelanja di Semua Bisa Kamu Beli!",
            color=COLOR_SUCCESS
        )
        
        embed.add_field(name="📋 ID Pesanan", value=f"#{order['id']}", inline=True)
        embed.add_field(name="📦 Produk", value=order['product_name'], inline=True)
        embed.add_field(name="🔢 Jumlah", value=str(order['quantity']), inline=True)
        embed.add_field(name="💰 Harga Satuan", value=format_price(order['price']), inline=True)
        embed.add_field(name="🧮 Subtotal", value=format_price(order['total']), inline=True)
        
        if discount > 0:
            embed.add_field(name="🎉 Diskon (VIP)", value=f"-{format_price(int(discount))}", inline=True)
            embed.add_field(name="💵 Total Bayar", value=format_price(int(total)), inline=True)
        else:
            embed.add_field(name="💵 Total Bayar", value=format_price(int(total)), inline=True)
        
        embed.add_field(name="⭐ Poin Didapat", value=f"+{points_earned} poin", inline=True)
        embed.add_field(name="💎 Total Poin Anda", value=f"{get_user_points(ctx.author.id)} poin", inline=True)
        
        embed.set_footer(text="Silakan lakukan pembayaran dalam 1x24 jam. Ketik !contact untuk info pembayaran.")
        await ctx.send(embed=embed)

    @commands.command(name='points')
    async def check_points(self, ctx):
        """Cek poin loyalty user"""
        points = get_user_points(ctx.author.id)
        
        embed = create_embed(
            title="💎 Poin Loyalty Anda",
            description=f"Halo {ctx.author.mention}! Berikut adalah informasi poin loyalty Anda:",
            color=COLOR_WARNING
        )
        
        embed.add_field(name="🏆 Total Poin", value=f"{points} poin", inline=True)
        
        if points >= VIP_THRESHOLD:
            embed.add_field(name="🎉 Status", value="VIP Member", inline=True)
            embed.add_field(name="💰 Benefit", value="Diskon 10% untuk pembelian berikutnya!", inline=False)
        else:
            embed.add_field(name="🎉 Status", value="Regular Member", inline=True)
            embed.add_field(name="📈 Target", value=f"Kumpulkan {VIP_THRESHOLD - points} poin lagi untuk menjadi VIP!", inline=False)
        
        embed.add_field(name="🎁 Cara Dapat Poin", value="• Ajukan pertanyaan: +1 poin\n• Beli produk: +5 poin per 10.000\n• Ikuti kuis: +10 poin", inline=False)
        
        embed.set_footer(text="Gunakan poin untuk mendapatkan diskon pada pembelian berikutnya!")
        await ctx.send(embed=embed)

    @commands.command(name='quiz')
    async def start_quiz(self, ctx):
        """Mulai kuis untuk dapat poin"""
        # Pilih pertanyaan random
        question_data = get_random_question()
        
        embed = create_embed(
            title="🧠 Kuis Poin Loyalty",
            description=f"Jawab pertanyaan berikut dengan benar dan dapatkan {POINTS_PER_CORRECT_QUIZ} poin!",
            color=COLOR_INFO
        )
        
        embed.add_field(name="❓ Pertanyaan", value=question_data['question'], inline=False)
        
        # Tambahkan opsi jawaban
        options_text = ""
        for i, option in enumerate(question_data['options']):
            options_text += f"**{i+1}.** {option}\n"
        
        embed.add_field(name="📝 Pilihan Jawaban", value=options_text, inline=False)
        embed.set_footer(text="Ketik nomor jawaban (1-4) untuk menjawab!")
        
        await ctx.send(embed=embed)
        
        # Fungsi untuk memeriksa jawaban
        def check(m):
            return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= 4
        
        try:
            # Tunggu jawaban user
            msg = await self.bot.wait_for('message', check=check, timeout=QUIZ_TIMEOUT_SECONDS)
            
            # Periksa jawaban
            answer_index = int(msg.content) - 1
            if answer_index == question_data['answer']:
                # Jawaban benar
                add_user_points(ctx.author.id, POINTS_PER_CORRECT_QUIZ)
                await ctx.send(f"🎉 Selamat {ctx.author.mention}! Jawaban Anda benar! Anda mendapatkan {POINTS_PER_CORRECT_QUIZ} poin!")
            else:
                # Jawaban salah
                correct_answer = question_data['options'][question_data['answer']]
                await ctx.send(f"❌ Maaf {ctx.author.mention}, jawaban Anda salah. Jawaban yang benar adalah: **{correct_answer}**")
        except:
            await ctx.send(f"⏱️ Waktu habis! Pertanyaan tidak dijawab.")

    @commands.command(name='pending')
    @commands.has_permissions(manage_messages=True)
    async def show_pending(self, ctx):
        """Admin: Menampilkan pertanyaan pending"""
        pending_questions = get_pending_questions()
        
        if not pending_questions:
            embed = create_embed(
                title="✅ Tidak Ada Pertanyaan Pending",
                description="Semua pertanyaan sudah dijawab!",
                color=COLOR_SUCCESS
            )
            await ctx.send(embed=embed)
            return
        
        embed = create_embed(
            title="📋 Pertanyaan Pending",
            description=f"Total: {len(pending_questions)} pertanyaan belum dijawab",
            color=COLOR_WARNING
        )
        
        # Tampilkan 5 pertanyaan terakhir
        for q in pending_questions[-5:]:
            embed.add_field(
                name=f"ID #{q['id']} - {q['user']}",
                value=f"{truncate_text(q['question'], 150)}\n⏱️ {format_datetime(q['timestamp'])}",
                inline=False
            )
        
        if len(pending_questions) > 5:
            embed.set_footer(text=f"Menampilkan 5 pertanyaan terakhir dari {len(pending_questions)} total")
        
        await ctx.send(embed=embed)

    @commands.command(name='close')
    @commands.has_permissions(manage_messages=True)
    async def close_question(self, ctx, question_id: int):
        """Admin: Tutup pertanyaan berdasarkan ID"""
        if close_question(question_id):
            embed = create_embed(
                title="✅ Pertanyaan Ditutup",
                description=f"Pertanyaan ID #{question_id} telah ditandai selesai.",
                color=COLOR_SUCCESS
            )
        else:
            embed = create_embed(
                title="❌ ID Tidak Ditemukan",
                description=f"Pertanyaan dengan ID #{question_id} tidak ditemukan atau sudah ditutup.",
                color=COLOR_ERROR
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='stats')
    async def show_stats(self, ctx):
        """Menampilkan statistik bot"""
        stats = get_bot_stats()
        
        embed = create_embed(
            title="📊 Statistik SemarakBot",
            color=COLOR_PRIMARY
        )
        
        embed.add_field(name="🏪 Server", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 Total User", value=sum(guild.member_count for guild in self.bot.guilds), inline=True)
        embed.add_field(name="📋 Total Pertanyaan", value=stats['total_questions'], inline=True)
        embed.add_field(name="❓ Pertanyaan Pending", value=stats['pending_questions'], inline=True)
        embed.add_field(name="🛒 Total Pesanan", value=stats['total_orders'], inline=True)
        embed.add_field(name="⏳ Pesanan Pending", value=stats['pending_orders'], inline=True)
        embed.add_field(name="👤 Member Loyalty", value=stats['total_users'], inline=True)
        embed.add_field(name="💎 Total Poin", value=stats['total_points'], inline=True)
        embed.add_field(name="📖 Kategori FAQ", value=len(faq_database), inline=True)
        
        embed.set_footer(text=f"Statistik per {format_datetime(discord.utils.utcnow())}")
        await ctx.send(embed=embed)

    @commands.command(name='broadcast')
    @commands.has_permissions(administrator=True)
    async def broadcast_message(self, ctx, *, message: str):
        """Admin: Kirim pesan ke semua server"""
        embed = create_embed(
            title="📢 Pengumuman dari Semua Bisa Kamu Beli",
            description=message,
            color=COLOR_WARNING
        )
        embed.set_footer(text=f"Dikirim oleh {ctx.author.display_name}")
        
        # Kirim ke channel "general" atau "pengumuman" di setiap server
        success_count = 0
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name in ["general", "pengumuman", "announcement"]:
                    try:
                        await channel.send(embed=embed)
                        success_count += 1
                        break
                    except:
                        pass
        
        await ctx.send(f"✅ Pesan berhasil dikirim ke {success_count} server!")

    @commands.command(name='addfaq')
    @commands.has_permissions(administrator=True)
    async def add_faq(self, ctx, category: str, *, answer: str):
        """Admin: Tambah FAQ baru"""
        # Konversi ke lowercase
        category = category.lower()
        
        # Cek apakah kategori sudah ada
        if category in faq_database:
            # Update FAQ yang ada
            faq_database[category]['answer'] = answer
            await ctx.send(f"✅ FAQ untuk kategori '{category}' telah diperbarui!")
        else:
            # Tambah FAQ baru
            faq_database[category] = {
                'keywords': [category],
                'answer': answer,
                'emoji': '❓'
            }
            await ctx.send(f"✅ FAQ baru untuk kategori '{category}' telah ditambahkan!")
