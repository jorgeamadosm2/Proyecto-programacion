// Actualizar navbar con sesión de usuario y carrito
document.addEventListener('DOMContentLoaded', function() {
    console.log('navbar.js cargado');
    actualizarNavbar();
    actualizarContadorCarrito();
});

function actualizarNavbar() {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
    const username = sessionStorage.getItem('username') || 'Usuario';
    
    console.log('Actualizando navbar. Logged in:', isLoggedIn, 'Username:', username);
    
    // Buscar el contenedor del navbar
    const navbarNav = document.querySelector('.navbar-nav');
    if (!navbarNav) {
        console.error('No se encontró .navbar-nav');
        return;
    }

    // Limpiar elementos dinámicos anteriores
    const dinamicos = navbarNav.querySelectorAll('#user-menu, #cart-menu, a[href*="login.html"], a[href*="registro.html"]');
    dinamicos.forEach(el => {
        if (el.tagName === 'A') {
            el.closest('li')?.remove();
        } else {
            el.remove();
        }
    });

    const isInPagesFolder = window.location.pathname.includes('/pages/');
    const tiendaPath = isInPagesFolder ? './tienda.html' : './pages/tienda.html';

    if (isLoggedIn) {
        console.log('Agregando elementos de usuario logueado');
        
        // Agregar carrito
        const cartLi = document.createElement('li');
        cartLi.className = 'nav-item';
        cartLi.id = 'cart-menu';
        cartLi.innerHTML = `
            <a class="nav-link px-3 position-relative" href="#" data-bs-toggle="modal" data-bs-target="#carritoModal" onclick="return false;">
                <i class="fas fa-shopping-cart me-1"></i>Carrito
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" id="cart-badge" style="display: none;">
                    0
                </span>
            </a>
        `;
        navbarNav.appendChild(cartLi);

        // Agregar menú de usuario con dropdown
        const userLi = document.createElement('li');
        userLi.className = 'nav-item dropdown';
        userLi.id = 'user-menu';
        userLi.innerHTML = `
            <a class="nav-link dropdown-toggle px-3" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fas fa-user-circle me-1"></i>${username}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#" onclick="cerrarSesion(); return false;">
                    <i class="fas fa-sign-out-alt me-2"></i>Cerrar Sesión
                </a></li>
            </ul>
        `;
        navbarNav.appendChild(userLi);
        
        console.log('Elementos de usuario agregados');
    } else {
        console.log('Agregando elementos de login/registro');
        
        const loginPath = isInPagesFolder ? './login.html' : './pages/login.html';
        const registerPath = isInPagesFolder ? './registro.html' : './pages/registro.html';
        
        // Agregar Login
        const loginLi = document.createElement('li');
        loginLi.className = 'nav-item';
        loginLi.innerHTML = `
            <a class="nav-link px-3" href="${loginPath}">
                <i class="fas fa-sign-in-alt me-1"></i>Login
            </a>
        `;
        navbarNav.appendChild(loginLi);
        
        // Agregar Registro
        const registerLi = document.createElement('li');
        registerLi.className = 'nav-item';
        registerLi.innerHTML = `
            <a class="nav-link px-3" href="${registerPath}">
                <i class="fas fa-user-plus me-1"></i>Registro
            </a>
        `;
        navbarNav.appendChild(registerLi);
        
        console.log('Elementos de login/registro agregados');
    }
}

function actualizarContadorCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const badge = document.getElementById('cart-badge');
    
    if (badge) {
        const cantidad = carrito.length;
        badge.textContent = cantidad;
        badge.style.display = cantidad > 0 ? 'inline-block' : 'none';
    }
    
    // Si no hay badge, actualizar el navbar completo
    setTimeout(() => {
        const newBadge = document.getElementById('cart-badge');
        if (newBadge) {
            const cantidad = carrito.length;
            newBadge.textContent = cantidad;
            newBadge.style.display = cantidad > 0 ? 'inline-block' : 'none';
        }
    }, 100);
}

function cerrarSesion() {
    // Limpiar sesión
    sessionStorage.clear();
    
    // Limpiar carrito
    localStorage.removeItem('carrito');
    
    // Redirigir a index
    const isInPagesFolder = window.location.pathname.includes('/pages/');
    const indexPath = isInPagesFolder ? '../index.html' : './index.html';
    
    alert('Sesión cerrada exitosamente');
    window.location.href = indexPath;
}

// Actualizar contador cuando cambie el carrito
window.addEventListener('storage', function(e) {
    if (e.key === 'carrito') {
        actualizarContadorCarrito();
    }
});

// Exponer función para actualizar desde otros scripts
window.actualizarContadorCarrito = actualizarContadorCarrito;
