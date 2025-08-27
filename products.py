# products.py

products = [
    {
        'id': 1,
        'name': 'Smartphone X Pro',
        'category': 'elektronik',
        'price': 4999000,
        'description': 'Smartphone dengan kamera 48MP dan baterai 5000mAh',
        'image': 'https://example.com/phone.jpg',
        'stock': 25
    },
    {
        'id': 2,
        'name': 'Laptop Ultra Slim',
        'category': 'elektronik',
        'price': 8999000,
        'description': 'Laptop tipis dengan RAM 8GB dan SSD 256GB',
        'image': 'https://example.com/laptop.jpg',
        'stock': 15
    },
    {
        'id': 3,
        'name': 'Sepatu Sneakers Premium',
        'category': 'fashion',
        'price': 799000,
        'description': 'Sneakers nyaman untuk aktivitas sehari-hari',
        'image': 'https://example.com/shoes.jpg',
        'stock': 40
    },
    {
        'id': 4,
        'name': 'Tas Backpack Travel',
        'category': 'fashion',
        'price': 399000,
        'description': 'Tas backpack dengan banyak kompartemen',
        'image': 'https://example.com/backpack.jpg',
        'stock': 30
    },
    {
        'id': 5,
        'name': 'Skincare Set Premium',
        'category': 'kecantikan',
        'price': 599000,
        'description': 'Set perawatan wajah lengkap untuk semua jenis kulit',
        'image': 'https://example.com/skincare.jpg',
        'stock': 20
    }
]

def get_product_by_id(product_id):
    """Mendapatkan produk berdasarkan ID"""
    return next((p for p in products if p['id'] == product_id), None)

def get_products_by_category(category):
    """Mendapatkan produk berdasarkan kategori"""
    return [p for p in products if p['category'] == category.lower()]

def get_all_categories():
    """Mendapatkan semua kategori produk"""
    return list(set(p['category'] for p in products))