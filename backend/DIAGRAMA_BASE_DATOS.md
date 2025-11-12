# DIAGRAMA ENTIDAD-RELACIÓN - BASE DE DATOS CUERAR

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     DIAGRAMA DE BASE DE DATOS - CUERAR                       │
│                    Sistema de Gestión de Tienda de Cueros                   │
└──────────────────────────────────────────────────────────────────────────────┘


╔════════════════════════╗
║       USERS            ║
║ ─────────────────────  ║
║ • id (PK)              ║
║ • username (UNIQUE)    ║
║ • email (UNIQUE)       ║
║ • password_hash        ║
║ • phone                ║
║ • created_at           ║
╚════════════════════════╝
         │
         │ 1
         │
         │ (Un usuario puede tener múltiples pedidos)
         │
         │ N
         ▼
╔════════════════════════╗
║       ORDERS           ║
║ ─────────────────────  ║
║ • id (PK)              ║
║ • user_id (FK) ◄───────╢─── Relación 1:N con USERS
║ • total                ║
║ • status               ║
║ • created_at           ║
╚════════════════════════╝
         │
         │ 1
         │
         │ (Un pedido puede contener múltiples items)
         │
         │ N
         ▼
╔════════════════════════╗
║     ORDER_ITEMS        ║
║ ─────────────────────  ║
║ • id (PK)              ║
║ • order_id (FK) ◄──────╢─── Relación 1:N con ORDERS
║ • product_name         ║
║ • product_price        ║
║ • quantity             ║
╚════════════════════════╝


┌──────────────────────────────────────────────────────────────────┐
│              RELACIÓN MUCHOS A MUCHOS (N:M)                      │
└──────────────────────────────────────────────────────────────────┘

╔════════════════════════╗             ╔════════════════════════╗
║      PRODUCTS          ║             ║     CATEGORIES         ║
║ ─────────────────────  ║             ║ ─────────────────────  ║
║ • id (PK)              ║             ║ • id (PK)              ║
║ • name                 ║             ║ • name (UNIQUE)        ║
║ • description          ║             ║ • description          ║
║ • price                ║             ╚════════════════════════╝
║ • image_url            ║                        ▲
║ • stock                ║                        │
╚════════════════════════╝                        │
         │                                        │
         │                                        │
         │ N                                    N │
         │                                        │
         │            ╔════════════════════════╗  │
         └────────────║  PRODUCT_CATEGORIES    ║──┘
                      ║ ─────────────────────  ║
                      ║ • product_id (FK,PK)   ║
                      ║ • category_id (FK,PK)  ║
                      ╚════════════════════════╝
                      Tabla intermedia para
                      relación muchos a muchos


╔════════════════════════╗
║  CONTACT_MESSAGES      ║  ← Tabla independiente sin relaciones
║ ─────────────────────  ║
║ • id (PK)              ║
║ • name                 ║
║ • email                ║
║ • message              ║
║ • created_at           ║
╚════════════════════════╝


┌──────────────────────────────────────────────────────────────────────────────┐
│                           RESUMEN DE RELACIONES                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1️⃣  RELACIÓN UNO A MUCHOS (1:N)                                            │
│     ┌─────────┐    1       N   ┌─────────┐                                 │
│     │  USERS  │────────────────▶│ ORDERS  │                                 │
│     └─────────┘                 └─────────┘                                 │
│     Un usuario puede tener múltiples pedidos                                │
│     Un pedido pertenece a un solo usuario                                   │
│                                                                              │
│  2️⃣  RELACIÓN UNO A MUCHOS (1:N)                                            │
│     ┌─────────┐    1       N   ┌──────────────┐                            │
│     │ ORDERS  │────────────────▶│ ORDER_ITEMS  │                            │
│     └─────────┘                 └──────────────┘                            │
│     Un pedido puede contener múltiples items                                │
│     Un item pertenece a un solo pedido                                      │
│                                                                              │
│  3️⃣  RELACIÓN MUCHOS A MUCHOS (N:M)                                         │
│     ┌──────────┐         ┌──────────────────┐        ┌────────────┐        │
│     │ PRODUCTS │─── N ───│ PRODUCT_CATEGS   │─── M ──│ CATEGORIES │        │
│     └──────────┘         └──────────────────┘        └────────────┘        │
│     Un producto puede pertenecer a múltiples categorías                     │
│     Una categoría puede contener múltiples productos                        │
│     Implementado mediante tabla intermedia                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│                        INTEGRIDAD REFERENCIAL                                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FOREIGN KEYS (Claves Foráneas):                                            │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  ✓ orders.user_id         → users.id                                        │
│    ON DELETE SET NULL (Si se elimina usuario, pedidos quedan huérfanos)     │
│                                                                              │
│  ✓ order_items.order_id   → orders.id                                       │
│    ON DELETE CASCADE (Si se elimina pedido, se eliminan sus items)          │
│                                                                              │
│  ✓ product_categories.product_id   → products.id                            │
│    ON DELETE CASCADE (Si se elimina producto, se eliminan sus relaciones)   │
│                                                                              │
│  ✓ product_categories.category_id  → categories.id                          │
│    ON DELETE CASCADE (Si se elimina categoría, se eliminan sus relaciones)  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│                            ÍNDICES CREADOS                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Para optimizar consultas frecuentes:                                       │
│                                                                              │
│  ✓ idx_users_email                    → users(email)                        │
│  ✓ idx_orders_user_id                 → orders(user_id)                     │
│  ✓ idx_orders_status                  → orders(status)                      │
│  ✓ idx_order_items_order_id           → order_items(order_id)               │
│  ✓ idx_product_categories_product     → product_categories(product_id)      │
│  ✓ idx_product_categories_category    → product_categories(category_id)     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│                         EJEMPLOS DE CONSULTAS                                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Obtener pedidos de un usuario con sus items:                            │
│     ────────────────────────────────────────────                            │
│     SELECT u.username, o.total, oi.product_name                             │
│     FROM users u                                                             │
│     JOIN orders o ON u.id = o.user_id                                       │
│     JOIN order_items oi ON o.id = oi.order_id                               │
│     WHERE u.id = 1;                                                          │
│                                                                              │
│  2. Obtener productos de una categoría:                                     │
│     ─────────────────────────────────                                       │
│     SELECT p.name, p.price                                                  │
│     FROM products p                                                          │
│     JOIN product_categories pc ON p.id = pc.product_id                      │
│     WHERE pc.category_id = 2;                                               │
│                                                                              │
│  3. Estadísticas de ventas por usuario:                                     │
│     ─────────────────────────────────────                                   │
│     SELECT u.username, COUNT(o.id) as orders, SUM(o.total) as total        │
│     FROM users u                                                             │
│     JOIN orders o ON u.id = o.user_id                                       │
│     GROUP BY u.id;                                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│                          DATOS PRECARGADOS                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ✅ users ........................... 10 registros                           │
│  ✅ products ........................ 15 registros                           │
│  ✅ categories ...................... 10 registros                           │
│  ✅ product_categories .............. 26 registros (relaciones)             │
│  ✅ orders .......................... 12 registros                           │
│  ✅ order_items ..................... 16 registros                           │
│  ✅ contact_messages ................ 10 registros                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━     │
│  TOTAL .............................. 99 registros                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


Leyenda:
─────────
PK  = Primary Key (Clave Primaria)
FK  = Foreign Key (Clave Foránea)
1   = Uno (en relación 1:N)
N   = Muchos (en relación 1:N)
M   = Muchos (en relación N:M)
◄── = Referencia de clave foránea
```
