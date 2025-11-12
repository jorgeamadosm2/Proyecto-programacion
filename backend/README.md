# Backend de Cuerar - FastAPI

Este es el backend de la aplicación Cuerar, implementado con FastAPI y SQLite.

## Características

- API RESTful con FastAPI
- Base de datos SQLite
- CORS configurado para comunicación con frontend
- Endpoints para:
  - Registro y autenticación de usuarios
  - Gestión de productos
  - Procesamiento de pedidos
  - Mensajes de contacto

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Navegar a la carpeta del backend:
```bash
cd backend
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
python main.py
```

O con uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

## Documentación de la API

FastAPI genera automáticamente documentación interactiva:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints disponibles

### General
- `GET /` - Mensaje de bienvenida

### Productos
- `GET /api/products` - Obtener todos los productos con sus categorías
- `GET /api/categories` - Obtener todas las categorías
- `GET /api/categories/{category_id}/products` - Productos por categoría

### Usuarios
- `POST /api/register` - Registrar nuevo usuario
- `POST /api/login` - Iniciar sesión
- `GET /api/users` - Obtener todos los usuarios
- `GET /api/users/{user_id}/orders` - Estadísticas de pedidos de un usuario

### Pedidos
- `POST /api/orders` - Crear nuevo pedido
- `GET /api/orders/{user_id}` - Obtener pedidos de un usuario con detalles

### Contacto
- `POST /api/contact` - Enviar mensaje de contacto
- `GET /api/contact-messages` - Obtener todos los mensajes

### Estadísticas (Reportes)
- `GET /api/statistics/sales` - Estadísticas generales de ventas
  - Total de ventas
  - Top 5 clientes
  - Productos más vendidos
  - Pedidos por estado
- `GET /api/statistics/products` - Estadísticas de productos
  - Productos por categoría
  - Stock total
  - Productos con bajo stock

## Base de datos

La base de datos SQLite (`cuerar.db`) se crea automáticamente al iniciar el servidor por primera vez con **datos de ejemplo precargados**.

### Estructura de tablas:

#### 1. **users** - Usuarios registrados (10+ registros)
- `id` (PRIMARY KEY)
- `username` (UNIQUE)
- `email` (UNIQUE)
- `password_hash`
- `phone`
- `created_at`

#### 2. **products** - Catálogo de productos (15+ registros)
- `id` (PRIMARY KEY)
- `name`
- `description`
- `price`
- `image_url`
- `stock`

#### 3. **categories** - Categorías de productos (10 registros)
- `id` (PRIMARY KEY)
- `name` (UNIQUE)
- `description`

#### 4. **product_categories** - Relación muchos a muchos entre productos y categorías
- `product_id` (FOREIGN KEY → products)
- `category_id` (FOREIGN KEY → categories)
- PRIMARY KEY compuesta (product_id, category_id)

#### 5. **orders** - Pedidos realizados (12+ registros)
- `id` (PRIMARY KEY)
- `user_id` (FOREIGN KEY → users) - Relación uno a muchos
- `total`
- `status`
- `created_at`

#### 6. **order_items** - Detalles de items en pedidos (16+ registros)
- `id` (PRIMARY KEY)
- `order_id` (FOREIGN KEY → orders) - Relación uno a muchos
- `product_name`
- `product_price`
- `quantity`

#### 7. **contact_messages** - Mensajes de contacto (10+ registros)
- `id` (PRIMARY KEY)
- `name`
- `email`
- `message`
- `created_at`

### Relaciones entre tablas:

1. **Uno a muchos**: `users` → `orders` (Un usuario puede tener múltiples pedidos)
2. **Uno a muchos**: `orders` → `order_items` (Un pedido puede tener múltiples items)
3. **Muchos a muchos**: `products` ↔ `categories` (mediante tabla intermedia `product_categories`)

### Datos precargados:
- ✅ 10 usuarios de prueba (contraseña: "password123")
- ✅ 15 productos diversos
- ✅ 10 categorías
- ✅ 12 pedidos de ejemplo
- ✅ 16 items de pedidos
- ✅ 10 mensajes de contacto

## Configuración de CORS

El backend está configurado para aceptar peticiones desde cualquier origen (`allow_origins=["*"]`). 

**Para producción**, es recomendable especificar los dominios permitidos:
```python
allow_origins=["http://localhost", "https://tudominio.com"]
```

## Estructura del proyecto

```
backend/
├── main.py              # Aplicación principal de FastAPI
├── requirements.txt     # Dependencias del proyecto
├── cuerar.db           # Base de datos SQLite (se crea automáticamente)
└── README.md           # Este archivo
```

## Archivos de documentación

- **README.md** - Este archivo (guía de instalación y uso)
- **RESUMEN_PROYECTO.md** - Documentación completa del proyecto
- **DIAGRAMA_BASE_DATOS.md** - Diagrama entidad-relación visual
- **database_schema.sql** - Esquema SQL con comentarios detallados
- **verify_database.py** - Script para verificar la base de datos
- **mostrar_relaciones.py** - Ejemplos prácticos de relaciones

## Notas importantes

1. Asegúrate de que el backend esté ejecutándose antes de usar el frontend
2. El frontend está configurado para conectarse a `http://localhost:8000`
3. Las contraseñas se almacenan hasheadas usando SHA-256
4. Los productos de ejemplo se insertan automáticamente en la primera ejecución
5. **Base de datos con 99 registros** distribuidos en 7 tablas relacionadas
6. Usuarios de prueba: contraseña `password123` para todos

## Troubleshooting

### Error: "No module named 'fastapi'"
Asegúrate de haber instalado las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
El puerto 8000 ya está siendo usado. Puedes:
1. Cerrar el proceso que usa el puerto
2. Usar un puerto diferente:
```bash
uvicorn main:app --reload --port 8001
```

### CORS errors en el frontend
Verifica que:
1. El backend esté ejecutándose
2. La URL del API_URL en los archivos JavaScript sea correcta
3. CORS esté configurado correctamente en main.py
