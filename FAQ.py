def format_faq_qa():
    qa_list = [
        {
            "question": "Bagaimana cara pembayaran? (Ani)",
            "answer": "Kamu bisa membayar melalui transfer bank, kartu kredit, e-wallet seperti OVO, Dana, GoPay, atau metode pembayaran lainnya yang tersedia di website kami."
        },
        {
            "question": "Apa saja metode pembayaran yang diterima? (Budi)",
            "answer": "Metode pembayaran yang kami terima meliputi transfer bank, kartu kredit, serta e-wallet seperti OVO, Dana, dan GoPay."
        },
        {
            "question": "Kapan pesanan dikirim? (Citra)",
            "answer": "Pesanan biasanya akan dikirim dalam waktu 1-3 hari kerja setelah pembayaran dikonfirmasi."
        },
        {
            "question": "Berapa biaya pengiriman saya? (Dedi)",
            "answer": "Biaya pengiriman tergantung jarak dan berat paket, dan akan otomatis dihitung saat checkout."
        },
        {
            "question": "Apakah produk ada garansi? (Ela)",
            "answer": "Semua produk kami memiliki garansi resmi selama 1 tahun sesuai ketentuan, kecuali yang sudah jelas dikecualikan."
        },
        # Tambahkan pertanyaan dan jawaban lainnya serupa di sini...
    ]

    formatted_text = "**Frequently Asked Questions (FAQ):**\n\n"
    for qa in qa_list:
        formatted_text += f"**Q:** {qa['question']}\n"
        formatted_text += f"**A:** {qa['answer']}\n\n"
    return formatted_text

# Contoh pemanggilan fungsi ini di bot:
# await channel.send(format_faq_qa())

