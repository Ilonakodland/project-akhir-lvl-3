# utils.py

import discord
from config import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR, COLOR_INFO, SERVER_ICON

def create_embed(title, description=None, color=COLOR_PRIMARY, footer=None):
    """Membuat embed Discord dengan format konsisten"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    embed.set_thumbnail(url=SERVER_ICON)
    if footer:
        embed.set_footer(text=footer)
    return embed

def format_price(price):
    """Format harga ke format Rupiah"""
    return f"Rp {price:,}"

def format_datetime(dt):
    """Format datetime ke string yang readable"""
    return dt.strftime('%d/%m/%Y %H:%M')

def truncate_text(text, max_length=100):
    """Memotong teks jika terlalu panjang"""
    return text[:max_length] + "..." if len(text) > max_length else text

def get_user_status(points):
    """Mendapatkan status user berdasarkan poin"""
    from config import VIP_THRESHOLD
    return "VIP Member" if points >= VIP_THRESHOLD else "Regular Member"

def calculate_discount(total, points):
    """Menghitung diskon berdasarkan poin"""
    from config import VIP_THRESHOLD, VIP_DISCOUNT
    if points >= VIP_THRESHOLD:
        return total * VIP_DISCOUNT
    return 0