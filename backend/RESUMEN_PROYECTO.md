# 📊 DOCUMENTACIÓN COMPLETA - BACKEND CUERAR

## ✅ REQUISITOS CUMPLIDOS

### Base de Datos
- ✅ **7 tablas** implementadas (supera el mínimo de 3)
- ✅ **Relaciones entre tablas** claramente definidas:
  - **1:N** (Uno a muchos): `users` → `orders`
  - **1:N** (Uno a muchos): `orders` → `order_items`
  - **N:M** (Muchos a muchos): `products` ↔ `categories`
- ✅ **73+ registros totales** cargados automáticamente (supera el mínimo de 10 por tabla)

## 📋 ESTRUCTURA DE LA BASE DE DATOS

### Tablas Principales

#### 1. **users** (10 registros) ✅
Almacena información de usuarios registrados.
```sql
id, username, email, password_hash, phone, created_at
```
- Contraseña de prueba para todos: `password123`
- Relación: 1:N con `orders` (un usuario puede tener múltiples pedidos)

#### 2. **products** (15 registros) ✅
Catálogo de productos disponibles en la tienda.
```sql
id, name, description, price, image_url, stock
```
- Incluye: alfombras, carteras, billeteras, cinturones, mochilas, zapatos, chaquetas, etc.
- Relación: N:M con `categories` a través de `product_categories`

#### 3. **categories** (10 registros) ✅
Categorías para clasificar productos.
```sql
id, name, description
```
- Categorías: Alfombras, Carteras, Cueros, Billeteras, Cinturones, Mochilas, Zapatos, Chaquetas, Decoración, Accesorios
- Relación: N:M con `products` a través de `product_categories`

#### 4. **product_categories** (26 registros) ✅
Tabla intermedia para la relación muchos a muchos.
```sql
product_id, category_id
```
- Implementa relación N:M entre productos y categorías
- Un producto puede tener múltiples categorías
- Una categoría puede tener múltiples productos

#### 5. **orders** (12 registros) ✅
Pedidos realizados por usuarios.
```sql
id, user_id, total, status, created_at
```
- Estados: `completed`, `pending`
- Relación: N:1 con `users` (muchos pedidos → un usuario)
- Relación: 1:N con `order_items` (un pedido → múltiples items)

#### 6. **order_items** (16 registros) ✅
Detalles de cada item dentro de un pedido.
```sql
id, order_id, product_name, product_price, quantity
```
- Relación: N:1 con `orders` (muchos items → un pedido)

#### 7. **contact_messages** (10 registros) ✅
Mensajes de contacto de clientes.
```sql
id, name, email, message, created_at
```
- Tabla independiente sin relaciones

## 🔗 RELACIONES IMPLEMENTADAS

### Tipo 1: Uno a Muchos (1:N)

#### users → orders
```
Un usuario puede realizar múltiples pedidos
Un pedido pertenece a un solo usuario
```

**Ejemplo práctico:**
- Usuario `juan_perez` tiene 2 pedidos (ID: 1 y 5)
- Usuario `maria_garcia` tiene 2 pedidos (ID: 2 y 12)

#### orders → order_items
```
Un pedido puede contener múltiples items
Un item pertenece a un solo pedido
```

**Ejemplo práctico:**
- Pedido #2 contiene 2 items: Cartera grande ($40,000) + Cartera clásica ($40,000)
- Pedido #6 contiene 2 items: Alfombra overa ($45,000) + Alfombra oveja ($50,000)

### Tipo 2: Muchos a Muchos (N:M)

#### products ↔ categories
```
Un producto puede pertenecer a múltiples categorías
Una categoría puede contener múltiples productos
Implementado mediante tabla intermedia: product_categories
```

**Ejemplo práctico:**
- Producto "Alfombra de vaca blanca" pertenece a: **Alfombras** + **Decoración**
- Producto "Cartera de cuero grande" pertenece a: **Carteras** + **Accesorios**
- Categoría "Accesorios" contiene: 8 productos diferentes

## 📊 ESTADÍSTICAS DE DATOS

### Registros por Tabla
```
✓ users................................ 10 registros
✓ products............................. 15 registros
✓ categories........................... 10 registros
✓ product_categories................... 26 registros
✓ orders............................... 12 registros
✓ order_items.......................... 16 registros
✓ contact_messages..................... 10 registros
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL.................................. 99 registros
```

### Estadísticas de Ventas
```
Total vendido............. $734,000.00
Promedio por pedido....... $61,166.67
Pedido más grande......... $120,000.00
Pedidos completados....... 9
Pedidos pendientes........ 3
```

## 🌐 ENDPOINTS DE LA API

### Productos y Categorías
```
GET  /api/products                          - Lista productos con categorías
GET  /api/categories                        - Lista todas las categorías
GET  /api/categories/{id}/products          - Productos por categoría
```

### Usuarios y Autenticación
```
POST /api/register                          - Registrar usuario
POST /api/login                             - Iniciar sesión
GET  /api/users                             - Lista usuarios
GET  /api/users/{id}/orders                 - Pedidos de un usuario
```

### Pedidos
```
POST /api/orders                            - Crear nuevo pedido
GET  /api/orders/{user_id}                  - Pedidos con detalles
```

### Contacto
```
POST /api/contact                           - Enviar mensaje
GET  /api/contact-messages                  - Lista mensajes
```

### Estadísticas (Reportes)
```
GET  /api/statistics/sales                  - Estadísticas de ventas
GET  /api/statistics/products               - Estadísticas de productos
```

## 🎯 CONSULTAS SQL COMPLEJAS IMPLEMENTADAS

### 1. Top Clientes por Ventas
```sql
SELECT u.username, u.email, 
       COUNT(o.id) as order_count,
       SUM(o.total) as total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY total_spent DESC
LIMIT 5
```

### 2. Productos Más Vendidos
```sql
SELECT product_name,
       COUNT(*) as times_sold,
       SUM(product_price * quantity) as revenue
FROM order_items
GROUP BY product_name
ORDER BY times_sold DESC
```

### 3. Productos por Categoría
```sql
SELECT p.*, c.name as category_name
FROM products p
JOIN product_categories pc ON p.id = pc.product_id
JOIN categories c ON pc.category_id = c.id
WHERE c.id = ?
```

### 4. Pedidos Completos con Items
```sql
SELECT o.*, oi.*
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
WHERE o.user_id = ?
ORDER BY o.created_at DESC
```

## 🔧 TECNOLOGÍAS UTILIZADAS

- **Backend:** FastAPI 0.104.1
- **Base de Datos:** SQLite 3
- **Validación:** Pydantic 2.5.0
- **Servidor:** Uvicorn (ASGI)
- **CORS:** Habilitado para comunicación frontend-backend

## 📁 ARCHIVOS DEL PROYECTO

```
backend/
├── main.py                    # API FastAPI (467 líneas)
├── cuerar.db                  # Base de datos SQLite (99 registros)
├── requirements.txt           # Dependencias Python
├── README.md                  # Documentación completa
├── database_schema.sql        # Esquema de la BD con comentarios
├── verify_database.py         # Script de verificación
└── RESUMEN_PROYECTO.md        # Este archivo
```

## ✅ VALIDACIÓN DE REQUISITOS

### Requisito 1: Al menos 3 tablas ✅
**Resultado:** 7 tablas implementadas
- users, products, categories, product_categories, orders, order_items, contact_messages

### Requisito 2: Relaciones entre tablas ✅
**Resultado:** 3 tipos de relaciones
- ✓ 1:N entre users y orders
- ✓ 1:N entre orders y order_items
- ✓ N:M entre products y categories (con tabla intermedia)

### Requisito 3: Mínimo 10 registros por tabla ✅
**Resultado:** Todas las tablas principales tienen 10+ registros
- users: 10 registros
- products: 15 registros
- categories: 10 registros
- orders: 12 registros
- order_items: 16 registros
- contact_messages: 10 registros

## 🚀 INSTRUCCIONES DE USO

### 1. Instalar dependencias
```bash
cd backend
pip install -r requirements.txt
```

### 2. Iniciar servidor
```bash
python main.py
```

### 3. Verificar base de datos
```bash
python verify_database.py
```

### 4. Acceder a documentación
```
http://localhost:8000/docs        # Swagger UI
http://localhost:8000/redoc       # ReDoc
```

## 💡 CARACTERÍSTICAS DESTACADAS

1. **Base de datos normalizada** con integridad referencial
2. **Datos de ejemplo realistas** cargados automáticamente
3. **Relaciones complejas** correctamente implementadas
4. **API RESTful completa** con documentación automática
5. **Consultas optimizadas** con JOINs y agregaciones
6. **Índices de base de datos** para mejor rendimiento
7. **Validación de datos** con Pydantic
8. **CORS configurado** para integración frontend
9. **Estadísticas y reportes** mediante endpoints especializados
10. **Scripts de verificación** para validar integridad

## 📞 SOPORTE

Para más información, consultar:
- `README.md` - Guía de instalación y uso
- `database_schema.sql` - Esquema detallado de la BD
- `http://localhost:8000/docs` - Documentación interactiva de la API

---
**Proyecto:** Cuerar - Sistema de gestión de tienda de productos de cuero
**Tecnología:** FastAPI + SQLite
**Estado:** ✅ Completado y verificado
