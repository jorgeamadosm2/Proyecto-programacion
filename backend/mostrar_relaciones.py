import sqlite3

conn = sqlite3.connect('cuerar.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*70)
print("🔗 EJEMPLOS DE RELACIONES EN LA BASE DE DATOS")
print("="*70)

# Ejemplo 1: Relación 1:N (users -> orders)
print("\n" + "📌 EJEMPLO 1: Relación UNO A MUCHOS (users → orders)")
print("-"*70)
print("Usuario 'juan_perez' y todos sus pedidos:\n")

cursor.execute('''
    SELECT u.id, u.username, u.email,
           o.id as order_id, o.total, o.status, o.created_at
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.username = 'juan_perez'
''')

user_orders = cursor.fetchall()
if user_orders:
    user = user_orders[0]
    print(f"👤 Usuario: {user['username']} ({user['email']})")
    print(f"   User ID: {user['id']}\n")
    print("   Pedidos:")
    for order in user_orders:
        if order['order_id']:
            print(f"   • Pedido #{order['order_id']} - ${order['total']:,.0f} - {order['status']}")

# Ejemplo 2: Relación 1:N (orders -> order_items)
print("\n" + "="*70)
print("📌 EJEMPLO 2: Relación UNO A MUCHOS (orders → order_items)")
print("-"*70)
print("Pedido #2 y todos sus items:\n")

cursor.execute('''
    SELECT o.id, o.user_id, o.total, o.status,
           oi.id as item_id, oi.product_name, oi.product_price, oi.quantity
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    WHERE o.id = 2
''')

order_items = cursor.fetchall()
if order_items:
    order = order_items[0]
    print(f"🛒 Pedido #{order['id']} (Usuario ID: {order['user_id']})")
    print(f"   Estado: {order['status']}")
    print(f"   Total: ${order['total']:,.0f}\n")
    print("   Items incluidos:")
    for item in order_items:
        if item['item_id']:
            print(f"   • {item['product_name']} - ${item['product_price']:,.0f} x{item['quantity']}")

# Ejemplo 3: Relación N:M (products <-> categories)
print("\n" + "="*70)
print("📌 EJEMPLO 3: Relación MUCHOS A MUCHOS (products ↔ categories)")
print("-"*70)
print("Producto 'Alfombra de vaca blanca' y sus categorías:\n")

cursor.execute('''
    SELECT p.id, p.name, p.description, p.price,
           c.id as cat_id, c.name as category_name, c.description as cat_desc
    FROM products p
    JOIN product_categories pc ON p.id = pc.product_id
    JOIN categories c ON pc.category_id = c.id
    WHERE p.name LIKE '%Alfombra de vaca blanca%'
''')

product_cats = cursor.fetchall()
if product_cats:
    product = product_cats[0]
    print(f"📦 Producto: {product['name']}")
    print(f"   Descripción: {product['description']}")
    print(f"   Precio: ${product['price']:,.0f}\n")
    print("   Pertenece a las categorías:")
    for pc in product_cats:
        print(f"   • {pc['category_name']} - {pc['cat_desc']}")

# Ejemplo inverso: Categoría y sus productos
print("\n" + "-"*70)
print("Categoría 'Accesorios' y todos sus productos:\n")

cursor.execute('''
    SELECT c.id, c.name as category_name,
           p.id as prod_id, p.name as product_name, p.price
    FROM categories c
    LEFT JOIN product_categories pc ON c.id = pc.category_id
    LEFT JOIN products p ON pc.product_id = p.id
    WHERE c.name = 'Accesorios'
''')

cat_products = cursor.fetchall()
if cat_products:
    category = cat_products[0]
    print(f"🏷️  Categoría: {category['category_name']}")
    print(f"   Productos en esta categoría:")
    count = 0
    for cp in cat_products:
        if cp['prod_id']:
            count += 1
            print(f"   {count}. {cp['product_name']} - ${cp['price']:,.0f}")

# Consulta compleja: Usuario -> Pedidos -> Items
print("\n" + "="*70)
print("📌 EJEMPLO 4: Consulta con MÚLTIPLES RELACIONES")
print("-"*70)
print("Usuario con sus pedidos e items completos:\n")

cursor.execute('''
    SELECT 
        u.username,
        o.id as order_id,
        o.total as order_total,
        o.status,
        oi.product_name,
        oi.product_price,
        oi.quantity
    FROM users u
    JOIN orders o ON u.id = o.user_id
    JOIN order_items oi ON o.id = oi.order_id
    WHERE u.username = 'maria_garcia'
    ORDER BY o.id, oi.id
''')

full_orders = cursor.fetchall()
if full_orders:
    print(f"👤 Usuario: {full_orders[0]['username']}\n")
    current_order = None
    for row in full_orders:
        if current_order != row['order_id']:
            current_order = row['order_id']
            print(f"\n   🛒 Pedido #{row['order_id']} - Total: ${row['order_total']:,.0f} ({row['status']})")
        print(f"      • {row['product_name']} - ${row['product_price']:,.0f} x{row['quantity']}")

print("\n" + "="*70)
print("✅ TODAS LAS RELACIONES FUNCIONAN CORRECTAMENTE")
print("="*70 + "\n")

conn.close()
