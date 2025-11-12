from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import sqlite3
from datetime import datetime
import hashlib
import secrets

app = FastAPI(title="Cuerar API", version="1.0.0")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect('cuerar.db')
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            stock INTEGER DEFAULT 0
        )
    ''')
    
    # Tabla de pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabla de items de pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_name TEXT NOT NULL,
            product_price REAL NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        )
    ''')
    
    # Tabla de mensajes de contacto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de categorías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    # Tabla de relación productos-categorías (muchos a muchos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_categories (
            product_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    # Insertar categorías si no existen
    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        categories = [
            ('Alfombras', 'Alfombras de cuero natural para decoración'),
            ('Carteras', 'Accesorios de cuero genuino'),
            ('Cueros', 'Cueros naturales de diversos animales'),
            ('Billeteras', 'Billeteras de cuero premium'),
            ('Cinturones', 'Cinturones artesanales de cuero'),
            ('Mochilas', 'Mochilas de cuero resistentes'),
            ('Zapatos', 'Calzado de cuero hecho a mano'),
            ('Chaquetas', 'Chaquetas de cuero de alta calidad'),
            ('Decoración', 'Artículos decorativos de cuero'),
            ('Accesorios', 'Diversos accesorios de cuero')
        ]
        cursor.executemany('INSERT INTO categories (name, description) VALUES (?, ?)', categories)
    
    # Insertar productos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        products = [
            ('Alfombra de vaca blanca con puntos', 'Cuero genuino de vaca con patrón natural', 45000.00, '../img/alfombra-de-vaca-blanca-con-puntos.jpg', 10),
            ('Alfombra de vaca overa', 'Cuero genuino de vaca overa', 45000.00, '../img/alfombra-de-vaca-overa.jpg', 8),
            ('Cuero de cabra premium', 'Cuero genuino de cabra, suave y resistente', 40000.00, '../img/cuero-de-cabra.jpg', 15),
            ('Cartera de cuero grande', 'Cartera espaciosa de cuero genuino', 40000.00, '../img/cartera-cuero-g.jpg', 20),
            ('Cartera de cuero clásica', 'Cartera elegante de cuero genuino', 40000.00, '../img/cartera-cuero.jpg', 12),
            ('Billetera de cuero marrón', 'Billetera compacta con múltiples compartimentos', 15000.00, '../img/cartera-cuero.jpg', 25),
            ('Cinturón de cuero negro', 'Cinturón resistente con hebilla metálica', 18000.00, '../img/cartera-cuero.jpg', 30),
            ('Mochila de cuero vintage', 'Mochila espaciosa estilo vintage', 65000.00, '../img/cartera-cuero.jpg', 5),
            ('Zapatos de cuero casual', 'Zapatos cómodos para uso diario', 55000.00, '../img/cartera-cuero.jpg', 15),
            ('Chaqueta de cuero negra', 'Chaqueta clásica de cuero negro', 120000.00, '../img/cartera-cuero.jpg', 8),
            ('Alfombra de oveja blanca', 'Suave alfombra de cuero de oveja', 50000.00, '../img/alfombra-de-vaca-blanca-con-puntos.jpg', 6),
            ('Cartera crossbody', 'Cartera pequeña con correa ajustable', 35000.00, '../img/cartera-cuero-g.jpg', 18),
            ('Cuero de cabra negro', 'Cuero premium de cabra color negro', 42000.00, '../img/cuero-de-cabra.jpg', 12),
            ('Porta documentos de cuero', 'Elegante porta documentos profesional', 48000.00, '../img/cartera-cuero.jpg', 10),
            ('Cojines decorativos de cuero', 'Set de 2 cojines de cuero para sofá', 28000.00, '../img/cuero-de-cabra.jpg', 20)
        ]
        cursor.executemany('INSERT INTO products (name, description, price, image_url, stock) VALUES (?, ?, ?, ?, ?)', products)
        
        # Asignar categorías a productos (relación muchos a muchos)
        product_category_relations = [
            (1, 1), (1, 9),  # Alfombra vaca blanca -> Alfombras, Decoración
            (2, 1), (2, 9),  # Alfombra overa -> Alfombras, Decoración
            (3, 3),          # Cuero cabra -> Cueros
            (4, 2), (4, 10), # Cartera grande -> Carteras, Accesorios
            (5, 2), (5, 10), # Cartera clásica -> Carteras, Accesorios
            (6, 4), (6, 10), # Billetera -> Billeteras, Accesorios
            (7, 5), (7, 10), # Cinturón -> Cinturones, Accesorios
            (8, 6), (8, 10), # Mochila -> Mochilas, Accesorios
            (9, 7),          # Zapatos -> Zapatos
            (10, 8),         # Chaqueta -> Chaquetas
            (11, 1), (11, 9),# Alfombra oveja -> Alfombras, Decoración
            (12, 2), (12, 10),# Cartera crossbody -> Carteras, Accesorios
            (13, 3),         # Cuero cabra negro -> Cueros
            (14, 2), (14, 10),# Porta documentos -> Carteras, Accesorios
            (15, 9), (15, 10) # Cojines -> Decoración, Accesorios
        ]
        cursor.executemany('INSERT INTO product_categories (product_id, category_id) VALUES (?, ?)', product_category_relations)
    
    # Insertar usuarios de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Contraseña: "password123" hasheada
        default_hash = hashlib.sha256("password123".encode()).hexdigest()
        users = [
            ('juan_perez', 'juan.perez@email.com', default_hash, '1122334455'),
            ('maria_garcia', 'maria.garcia@email.com', default_hash, '1133445566'),
            ('carlos_rodriguez', 'carlos.rodriguez@email.com', default_hash, '1144556677'),
            ('ana_martinez', 'ana.martinez@email.com', default_hash, '1155667788'),
            ('luis_fernandez', 'luis.fernandez@email.com', default_hash, '1166778899'),
            ('sofia_lopez', 'sofia.lopez@email.com', default_hash, '1177889900'),
            ('diego_gomez', 'diego.gomez@email.com', default_hash, '1188990011'),
            ('laura_diaz', 'laura.diaz@email.com', default_hash, '1199001122'),
            ('pablo_ruiz', 'pablo.ruiz@email.com', default_hash, '1100112233'),
            ('valentina_torres', 'valentina.torres@email.com', default_hash, '1111223344')
        ]
        cursor.executemany('INSERT INTO users (username, email, password_hash, phone) VALUES (?, ?, ?, ?)', users)
    
    # Insertar pedidos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM orders')
    if cursor.fetchone()[0] == 0:
        orders = [
            (1, 45000.00, 'completed'),
            (2, 80000.00, 'completed'),
            (3, 40000.00, 'pending'),
            (4, 120000.00, 'completed'),
            (1, 15000.00, 'completed'),
            (5, 90000.00, 'completed'),
            (6, 35000.00, 'pending'),
            (7, 48000.00, 'completed'),
            (8, 73000.00, 'completed'),
            (9, 28000.00, 'completed'),
            (10, 105000.00, 'pending'),
            (2, 55000.00, 'completed')
        ]
        cursor.executemany('INSERT INTO orders (user_id, total, status) VALUES (?, ?, ?)', orders)
        
        # Insertar items de pedidos
        order_items = [
            (1, 'Alfombra de vaca blanca con puntos', 45000.00, 1),
            (2, 'Cartera de cuero grande', 40000.00, 1),
            (2, 'Cartera de cuero clásica', 40000.00, 1),
            (3, 'Cuero de cabra premium', 40000.00, 1),
            (4, 'Chaqueta de cuero negra', 120000.00, 1),
            (5, 'Billetera de cuero marrón', 15000.00, 1),
            (6, 'Alfombra de vaca overa', 45000.00, 1),
            (6, 'Alfombra de oveja blanca', 50000.00, 1),
            (7, 'Cartera crossbody', 35000.00, 1),
            (8, 'Porta documentos de cuero', 48000.00, 1),
            (9, 'Cinturón de cuero negro', 18000.00, 1),
            (9, 'Zapatos de cuero casual', 55000.00, 1),
            (10, 'Cojines decorativos de cuero', 28000.00, 1),
            (11, 'Mochila de cuero vintage', 65000.00, 1),
            (11, 'Cartera de cuero grande', 40000.00, 1),
            (12, 'Zapatos de cuero casual', 55000.00, 1)
        ]
        cursor.executemany('INSERT INTO order_items (order_id, product_name, product_price, quantity) VALUES (?, ?, ?, ?)', order_items)
    
    # Insertar mensajes de contacto de ejemplo
    cursor.execute('SELECT COUNT(*) FROM contact_messages')
    if cursor.fetchone()[0] == 0:
        messages = [
            ('Juan Pérez', 'juan@email.com', '¿Tienen envíos a todo el país?'),
            ('María García', 'maria@email.com', 'Me gustaría saber más sobre los cueros de cabra'),
            ('Carlos López', 'carlos@email.com', '¿Hacen trabajos personalizados?'),
            ('Ana Rodríguez', 'ana@email.com', 'Consulta sobre garantía de productos'),
            ('Luis Martínez', 'luis@email.com', '¿Cuánto demora el envío a Córdoba?'),
            ('Sofía Fernández', 'sofia@email.com', 'Quiero saber si tienen stock de alfombras'),
            ('Diego Torres', 'diego@email.com', '¿Aceptan tarjetas de crédito?'),
            ('Laura Gómez', 'laura@email.com', 'Me interesa la chaqueta de cuero negra'),
            ('Pablo Díaz', 'pablo@email.com', '¿Tienen local físico para ver productos?'),
            ('Valentina Ruiz', 'valentina@email.com', 'Consulta sobre cuidado del cuero')
        ]
        cursor.executemany('INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)', messages)
    
    conn.commit()
    conn.close()

# Inicializar DB al arrancar
init_db()

# Funciones de utilidad
def get_db():
    conn = sqlite3.connect('cuerar.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Modelos Pydantic
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str

class CartItem(BaseModel):
    nombre: str
    precio: float

class Order(BaseModel):
    items: List[CartItem]
    total: float
    user_id: Optional[int] = None

# Rutas de la API

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Cuerar"}

@app.get("/api/products")
def get_products():
    """Obtener todos los productos con sus categorías"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE stock > 0')
    products = []
    
    for row in cursor.fetchall():
        product = dict(row)
        # Obtener categorías del producto
        cursor.execute('''
            SELECT c.id, c.name, c.description 
            FROM categories c
            JOIN product_categories pc ON c.id = pc.category_id
            WHERE pc.product_id = ?
        ''', (product['id'],))
        product['categories'] = [dict(cat) for cat in cursor.fetchall()]
        products.append(product)
    
    conn.close()
    return {"products": products}

@app.get("/api/categories")
def get_categories():
    """Obtener todas las categorías"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"categories": categories}

@app.get("/api/categories/{category_id}/products")
def get_products_by_category(category_id: int):
    """Obtener productos de una categoría específica"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.* FROM products p
        JOIN product_categories pc ON p.id = pc.product_id
        WHERE pc.category_id = ? AND p.stock > 0
    ''', (category_id,))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"products": products}

@app.post("/api/register")
def register_user(user: UserRegister):
    """Registrar un nuevo usuario"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Verificar si el email o username ya existen
        cursor.execute('SELECT id FROM users WHERE email = ? OR username = ?', (user.email, user.username))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El email o nombre de usuario ya están registrados")
        
        # Hash de la contraseña
        password_hash = hash_password(user.password)
        
        # Insertar usuario
        cursor.execute(
            'INSERT INTO users (username, email, password_hash, phone) VALUES (?, ?, ?, ?)',
            (user.username, user.email, password_hash, user.phone)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        conn.close()
        return {
            "success": True,
            "message": f"¡Ya estás registrado {user.username}, bienvenido a Cuerar!",
            "user": {
                "id": user_id,
                "username": user.username,
                "email": user.email
            }
        }
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Error al registrar usuario")

@app.post("/api/login")
def login_user(credentials: UserLogin):
    """Iniciar sesión"""
    conn = get_db()
    cursor = conn.cursor()
    
    password_hash = hash_password(credentials.password)
    
    cursor.execute(
        'SELECT id, username, email FROM users WHERE email = ? AND password_hash = ?',
        (credentials.email, password_hash)
    )
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    return {
        "success": True,
        "message": f"¡Bienvenido, {user['username']}!",
        "user": {
            "id": user['id'],
            "username": user['username'],
            "email": user['email']
        }
    }

@app.post("/api/contact")
def contact_form(message: ContactMessage):
    """Guardar mensaje de contacto"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)',
        (message.name, message.email, message.message)
    )
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": "¡Gracias por contactarnos! Alguien de nuestro equipo se contactará contigo a la brevedad."
    }

@app.post("/api/orders")
def create_order(order: Order):
    """Crear un nuevo pedido"""
    if not order.items:
        raise HTTPException(status_code=400, detail="El carrito está vacío")
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Crear pedido
        cursor.execute(
            'INSERT INTO orders (user_id, total, status) VALUES (?, ?, ?)',
            (order.user_id, order.total, 'completed')
        )
        order_id = cursor.lastrowid
        
        # Insertar items del pedido
        for item in order.items:
            cursor.execute(
                'INSERT INTO order_items (order_id, product_name, product_price, quantity) VALUES (?, ?, ?, ?)',
                (order_id, item.nombre, item.precio, 1)
            )
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Compra realizada con éxito. ¡Gracias!",
            "order_id": order_id
        }
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error al procesar el pedido: {str(e)}")

@app.get("/api/orders/{user_id}")
def get_user_orders(user_id: int):
    """Obtener pedidos de un usuario con detalles"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    orders = []
    
    for order_row in cursor.fetchall():
        order = dict(order_row)
        # Obtener items del pedido
        cursor.execute('SELECT * FROM order_items WHERE order_id = ?', (order['id'],))
        order['items'] = [dict(item) for item in cursor.fetchall()]
        orders.append(order)
    
    conn.close()
    return {"orders": orders}

@app.get("/api/users")
def get_users():
    """Obtener todos los usuarios (sin contraseñas)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, phone, created_at FROM users')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"users": users}

@app.get("/api/users/{user_id}/orders")
def get_user_orders_stats(user_id: int):
    """Obtener estadísticas de pedidos de un usuario"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Información del usuario
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_dict = dict(user)
    
    # Estadísticas de pedidos
    cursor.execute('''
        SELECT 
            COUNT(*) as total_orders,
            SUM(total) as total_spent,
            AVG(total) as avg_order_value,
            MAX(total) as max_order
        FROM orders 
        WHERE user_id = ?
    ''', (user_id,))
    stats = dict(cursor.fetchone())
    
    # Pedidos recientes
    cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', (user_id,))
    recent_orders = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "user": user_dict,
        "statistics": stats,
        "recent_orders": recent_orders
    }

@app.get("/api/statistics/sales")
def get_sales_statistics():
    """Obtener estadísticas generales de ventas"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ventas totales
    cursor.execute('''
        SELECT 
            COUNT(*) as total_orders,
            SUM(total) as total_revenue,
            AVG(total) as avg_order_value
        FROM orders
    ''')
    sales_stats = dict(cursor.fetchone())
    
    # Top 5 usuarios por compras
    cursor.execute('''
        SELECT 
            u.id, u.username, u.email,
            COUNT(o.id) as order_count,
            SUM(o.total) as total_spent
        FROM users u
        JOIN orders o ON u.id = o.user_id
        GROUP BY u.id
        ORDER BY total_spent DESC
        LIMIT 5
    ''')
    top_customers = [dict(row) for row in cursor.fetchall()]
    
    # Productos más vendidos
    cursor.execute('''
        SELECT 
            product_name,
            COUNT(*) as times_sold,
            SUM(product_price * quantity) as revenue
        FROM order_items
        GROUP BY product_name
        ORDER BY times_sold DESC
        LIMIT 10
    ''')
    top_products = [dict(row) for row in cursor.fetchall()]
    
    # Pedidos por estado
    cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM orders
        GROUP BY status
    ''')
    orders_by_status = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "sales_overview": sales_stats,
        "top_customers": top_customers,
        "top_products": top_products,
        "orders_by_status": orders_by_status
    }

@app.get("/api/statistics/products")
def get_product_statistics():
    """Obtener estadísticas de productos y categorías"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Total de productos por categoría
    cursor.execute('''
        SELECT 
            c.id, c.name, c.description,
            COUNT(pc.product_id) as product_count
        FROM categories c
        LEFT JOIN product_categories pc ON c.id = pc.category_id
        GROUP BY c.id
        ORDER BY product_count DESC
    ''')
    categories_stats = [dict(row) for row in cursor.fetchall()]
    
    # Stock total
    cursor.execute('SELECT SUM(stock) as total_stock, COUNT(*) as total_products FROM products')
    stock_info = dict(cursor.fetchone())
    
    # Productos con bajo stock
    cursor.execute('SELECT * FROM products WHERE stock < 10 ORDER BY stock ASC')
    low_stock = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "categories": categories_stats,
        "stock_info": stock_info,
        "low_stock_products": low_stock
    }

@app.get("/api/contact-messages")
def get_contact_messages():
    """Obtener todos los mensajes de contacto"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC')
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"messages": messages}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
