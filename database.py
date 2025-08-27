# database.py

# Database pertanyaan
questions_storage = []

# Database pesanan
orders_db = []

# Database loyalty points
loyalty_db = {}

def save_question(user, question):
    """Menyimpan pertanyaan yang tidak terjawab"""
    from datetime import datetime
    
    question_data = {
        'id': len(questions_storage) + 1,
        'user': str(user),
        'question': question,
        'status': 'pending',
        'timestamp': datetime.now()
    }
    questions_storage.append(question_data)
    return question_data['id']

def get_pending_questions():
    """Mendapatkan semua pertanyaan yang pending"""
    return [q for q in questions_storage if q['status'] == 'pending']

def close_question(question_id):
    """Menutup pertanyaan berdasarkan ID"""
    for q in questions_storage:
        if q['id'] == question_id and q['status'] == 'pending':
            q['status'] = 'closed'
            return True
    return False

def create_order(user, product_id, quantity):
    """Membuat pesanan baru"""
    from datetime import datetime
    from products import get_product_by_id
    
    product = get_product_by_id(product_id)
    if not product:
        return None
    
    if product['stock'] < quantity:
        return None
    
    # Kurangi stok
    product['stock'] -= quantity
    
    # Buat pesanan
    order_id = len(orders_db) + 1
    order = {
        'id': order_id,
        'user': str(user),
        'product_id': product_id,
        'product_name': product['name'],
        'quantity': quantity,
        'price': product['price'],
        'total': product['price'] * quantity,
        'status': 'pending',
        'timestamp': datetime.now()
    }
    orders_db.append(order)
    return order

def get_user_points(user_id):
    """Mendapatkan poin loyalty user"""
    return loyalty_db.get(str(user_id), 0)

def add_user_points(user_id, points):
    """Menambahkan poin loyalty user"""
    user_id_str = str(user_id)
    if user_id_str in loyalty_db:
        loyalty_db[user_id_str] += points
    else:
        loyalty_db[user_id_str] = points
    return loyalty_db[user_id_str]

def use_user_points(user_id, points):
    """Menggunakan poin loyalty user"""
    user_id_str = str(user_id)
    if user_id_str in loyalty_db and loyalty_db[user_id_str] >= points:
        loyalty_db[user_id_str] -= points
        return True
    return False

def get_bot_stats():
    """Mendapatkan statistik bot"""
    pending_count = len([q for q in questions_storage if q['status'] == 'pending'])
    total_questions = len(questions_storage)
    total_orders = len(orders_db)
    pending_orders = len([o for o in orders_db if o['status'] == 'pending'])
    total_users = len(loyalty_db)
    total_points = sum(loyalty_db.values())
    
    return {
        'pending_questions': pending_count,
        'total_questions': total_questions,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_users': total_users,
        'total_points': total_points
    }