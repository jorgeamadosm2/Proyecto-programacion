-- ============================================
-- ESQUEMA DE BASE DE DATOS - CUERAR
-- Sistema de gestión de tienda de productos de cuero
-- ============================================

-- Tabla: users
-- Descripción: Almacena información de usuarios registrados
-- Relaciones: 1:N con orders (un usuario puede tener múltiples pedidos)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: categories
-- Descripción: Categorías de productos
-- Relaciones: N:M con products (mediante product_categories)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- Tabla: products
-- Descripción: Catálogo de productos disponibles
-- Relaciones: N:M con categories (mediante product_categories)
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image_url TEXT,
    stock INTEGER DEFAULT 0
);

-- Tabla: product_categories
-- Descripción: Tabla intermedia para relación muchos a muchos entre productos y categorías
-- Relaciones: N:M entre products y categories
CREATE TABLE IF NOT EXISTS product_categories (
    product_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);

-- Tabla: orders
-- Descripción: Pedidos realizados por usuarios
-- Relaciones: 
--   - N:1 con users (muchos pedidos pueden pertenecer a un usuario)
--   - 1:N con order_items (un pedido puede tener múltiples items)
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

-- Tabla: order_items
-- Descripción: Items individuales dentro de cada pedido
-- Relaciones: N:1 con orders (muchos items pertenecen a un pedido)
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
);

-- Tabla: contact_messages
-- Descripción: Mensajes enviados por clientes a través del formulario de contacto
-- Relaciones: Ninguna (tabla independiente)
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ÍNDICES PARA MEJORAR RENDIMIENTO
-- ============================================

-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_product_categories_product ON product_categories(product_id);
CREATE INDEX IF NOT EXISTS idx_product_categories_category ON product_categories(category_id);

-- ============================================
-- RESUMEN DE RELACIONES
-- ============================================

-- 1. RELACIÓN UNO A MUCHOS (1:N)
--    users (1) ←→ (N) orders
--    Un usuario puede tener múltiples pedidos
--    Un pedido pertenece a un solo usuario

-- 2. RELACIÓN UNO A MUCHOS (1:N)
--    orders (1) ←→ (N) order_items
--    Un pedido puede contener múltiples items
--    Un item pertenece a un solo pedido

-- 3. RELACIÓN MUCHOS A MUCHOS (N:M)
--    products (N) ←→ (M) categories
--    Un producto puede pertenecer a múltiples categorías
--    Una categoría puede contener múltiples productos
--    Implementado mediante tabla intermedia: product_categories

-- ============================================
-- CONSULTAS DE EJEMPLO
-- ============================================

-- 1. Obtener todos los pedidos de un usuario con sus items
-- SELECT o.*, oi.* 
-- FROM orders o
-- JOIN order_items oi ON o.id = oi.order_id
-- WHERE o.user_id = 1;

-- 2. Obtener productos de una categoría específica
-- SELECT p.* 
-- FROM products p
-- JOIN product_categories pc ON p.id = pc.product_id
-- WHERE pc.category_id = 2;

-- 3. Top 5 clientes por total gastado
-- SELECT u.username, u.email, SUM(o.total) as total_spent
-- FROM users u
-- JOIN orders o ON u.id = o.user_id
-- GROUP BY u.id
-- ORDER BY total_spent DESC
-- LIMIT 5;

-- 4. Productos más vendidos
-- SELECT product_name, COUNT(*) as times_sold, SUM(product_price * quantity) as revenue
-- FROM order_items
-- GROUP BY product_name
-- ORDER BY times_sold DESC;

-- 5. Categorías con más productos
-- SELECT c.name, COUNT(pc.product_id) as product_count
-- FROM categories c
-- LEFT JOIN product_categories pc ON c.id = pc.category_id
-- GROUP BY c.id
-- ORDER BY product_count DESC;
