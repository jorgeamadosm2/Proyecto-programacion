import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Conectar a la base de datos
conn = sqlite3.connect('cuerar.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*60)
print("👥 USUARIOS DISPONIBLES PARA LOGIN")
print("="*60 + "\n")

# Obtener todos los usuarios
cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
usuarios = cursor.fetchall()

print(f"Total de usuarios registrados: {len(usuarios)}\n")
print("-" * 60)

for user in usuarios:
    print(f"ID: {user['id']}")
    print(f"Usuario: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Registrado: {user['created_at']}")
    print("-" * 60)

print("\n💡 USUARIOS DE PRUEBA CON PASSWORD: 'password123'\n")
print("📧 carlos.ruiz@email.com")
print("📧 ana.martinez@email.com")
print("📧 luis.garcia@email.com")
print("📧 maria.lopez@email.com")
print("📧 jorge_amadosm@example.com")

# Verificar hash de la contraseña de prueba
password_test = "password123"
hash_test = hash_password(password_test)
print(f"\n🔐 Hash de 'password123': {hash_test[:20]}...")

# Contar cuántos usuarios tienen esta contraseña
cursor.execute("SELECT COUNT(*) as count FROM users WHERE password_hash = ?", (hash_test,))
count = cursor.fetchone()['count']
print(f"✅ {count} usuarios usan esta contraseña para pruebas\n")

conn.close()

print("\n" + "="*60)
print("INSTRUCCIONES PARA PROBAR EL LOGIN:")
print("="*60)
print("\n1. Asegúrate de que el backend esté corriendo:")
print("   cd backend")
print("   python main.py")
print("\n2. Abre login.html en el navegador")
print("\n3. Usa cualquiera de estos usuarios:")
print("   Email: carlos.ruiz@email.com")
print("   Password: password123")
print("\n4. ¡Deberías poder iniciar sesión correctamente!")
print("\n" + "="*60 + "\n")
