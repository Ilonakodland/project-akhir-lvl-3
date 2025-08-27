# quiz.py

quiz_questions = [
    {
        'question': 'Apa kepanjangan dari "E-commerce"?',
        'options': ['Electronic Commerce', 'Easy Commerce', 'Economic Commerce', 'Effective Commerce'],
        'answer': 0
    },
    {
        'question': 'Metode pembayaran mana yang paling aman untuk transaksi online?',
        'options': ['Transfer Bank', 'Kartu Kredit', 'E-wallet', 'Semua sama amannya'],
        'answer': 3
    },
    {
        'question': 'Apa keuntungan berbelanja di "Semua Bisa Kamu Beli"?',
        'options': ['Harga murah', 'Gratis ongkir', 'Produk berkualitas', 'Semua benar'],
        'answer': 3
    },
    {
        'question': 'Berapa lama waktu pengiriman biasanya?',
        'options': ['1-3 hari kerja', '3-5 hari kerja', '5-7 hari kerja', '1-2 minggu'],
        'answer': 0
    },
    {
        'question': 'Apa yang harus dilakukan jika produk rusak?',
        'options': ['Buang saja', 'Klaim garansi', 'Beli baru', 'Komplain di media sosial'],
        'answer': 1
    }
]

def get_random_question():
    """Mendapatkan pertanyaan kuis secara acak"""
    import random
    return random.choice(quiz_questions)