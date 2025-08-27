# faq.py

faq_database = {
    'pembayaran': {
        'keywords': ['pembayaran', 'bayar', 'payment', 'transfer', 'cara bayar'],
        'answer': '💳 **Metode Pembayaran Kami:**\n• Transfer Bank (BCA, Mandiri, BRI, BNI)\n• E-wallet (OVO, Dana, GoPay, ShopeePay)\n• Kartu Kredit/Debit\n• QRIS\n\n*Pembayaran akan diverifikasi dalam 1x24 jam*',
        'emoji': '💳'
    },
    'pengiriman': {
        'keywords': ['pengiriman', 'kirim', 'shipping', 'delivery', 'dikirim'],
        'answer': '🚚 **Info Pengiriman:**\n• Waktu: 1-3 hari kerja setelah pembayaran\n• Ekspedisi: JNE, J&T, SiCepat, AnterAja\n• Lacak paket melalui website ekspedisi\n• Barang dikemas dengan bubble wrap',
        'emoji': '🚚'
    },
    'ongkir': {
        'keywords': ['ongkir', 'ongkos kirim', 'biaya kirim', 'gratis ongkir'],
        'answer': '📦 **Ongkos Kirim:**\n• Dihitung otomatis saat checkout\n• Berdasarkan berat dan jarak\n• **GRATIS ONGKIR** untuk pembelian > Rp 100.000\n• Estimasi biaya bisa dicek di website',
        'emoji': '📦'
    },
    'garansi': {
        'keywords': ['garansi', 'warranty', 'jaminan', 'klaim garansi'],
        'answer': '🛡️ **Garansi Produk:**\n• 1 tahun garansi resmi\n• Berlaku untuk kerusakan pabrik\n• Tidak berlaku: kerusakan karena pemakaian salah\n• Klaim garansi melalui customer service',
        'emoji': '🛡️'
    },
    'return': {
        'keywords': ['return', 'tukar', 'kembalikan', 'retur', 'pengembalian'],
        'answer': '↩️ **Kebijakan Return:**\n• 7 hari setelah terima barang\n• Kondisi: barang utuh, belum dipakai\n• Alasan: rusak/cacat, salah kirim, tidak sesuai\n• Biaya return ditanggung toko jika kesalahan dari kami',
        'emoji': '↩️'
    },
    'kontak': {
        'keywords': ['kontak', 'contact', 'hubungi', 'cs', 'customer service'],
        'answer': '📞 **Hubungi Customer Service:**\n• WhatsApp: 0812-3456-7890\n• Email: cs@semuabisakamubeli.com\n• Instagram: @semuabisakamubeli\n• Jam kerja: 09:00-17:00 WIB (Senin-Sabtu)',
        'emoji': '📞'
    },
    'promo': {
        'keywords': ['promo', 'diskon', 'sale', 'discount', 'voucher'],
        'answer': '🎉 **Promo Terkini:**\n• Diskon 20% untuk member baru\n• Flash sale setiap Jumat 12.00 WIB\n• Cashback 10% untuk pembelian > Rp 500.000\n• Follow IG @semuabisakamubeli untuk info promo terbaru',
        'emoji': '🎉'
    },
    'produk': {
        'keywords': ['produk', 'barang', 'item', 'katalog', 'jual apa'],
        'answer': '🛍️ **Katalog Produk:**\n• Elektronik (HP, Laptop, Aksesoris)\n• Fashion (Pakaian, Sepatu, Tas)\n• Rumah Tangga (Perabot, Dekorasi)\n• Kecantikan (Skincare, Makeup)\n\n*Lihat katalog lengkap di website kami*',
        'emoji': '🛍️'
    }
}

def find_faq_answer(message_content):
    """Mencari jawaban FAQ berdasarkan kata kunci"""
    content_lower = message_content.lower()
    
    for category, data in faq_database.items():
        for keyword in data['keywords']:
            if keyword in content_lower:
                return category, data['answer'], data['emoji']
    return None, None, None