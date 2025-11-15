const API_URL = 'http://localhost:8000';
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Cargar carrito al inicio
document.addEventListener('DOMContentLoaded', function() {
  actualizarCarrito();
});

function agregarAlCarrito(boton) {
  const nombre = boton.dataset.nombre;
  const precio = parseFloat(boton.dataset.precio);

  carrito.push({ nombre, precio });
  localStorage.setItem('carrito', JSON.stringify(carrito));
  actualizarCarrito();
  
  // Actualizar contador en navbar
  if (window.actualizarContadorCarrito) {
    window.actualizarContadorCarrito();
  }
}

function actualizarCarrito() {
  const lista = document.getElementById("carrito-lista");
  const total = document.getElementById("carrito-total");
  const totalFinal = document.getElementById("carrito-total-final");
  const carritoVacio = document.getElementById("carrito-vacio");

  lista.innerHTML = "";
  let suma = 0;

  if (carrito.length === 0) {
    if (carritoVacio) carritoVacio.style.display = "block";
  } else {
    if (carritoVacio) carritoVacio.style.display = "none";
    
    carrito.forEach((item, index) => {
      const li = document.createElement("li");
      li.className = "list-group-item d-flex justify-content-between align-items-center";
      li.innerHTML = `
        <div>
          <h6 class="mb-1">${item.nombre}</h6>
          <small class="text-muted">Precio: $${item.precio.toLocaleString()}</small>
        </div>
        <button class="btn btn-sm btn-danger" onclick="eliminarDelCarrito(${index})">
          <i class="fas fa-trash"></i>
        </button>
      `;
      lista.appendChild(li);
      suma += item.precio;
    });
  }

  const sumaFormateada = suma.toLocaleString();
  total.textContent = sumaFormateada;
  if (totalFinal) totalFinal.textContent = sumaFormateada;
}

// Función para filtrar productos por categoría
function filtrarCategoria(categoria) {
  const productos = document.querySelectorAll('[data-categoria]');
  const botones = document.querySelectorAll('.btn-group .btn');
  
  // Actualizar botones activos
  botones.forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  
  // Filtrar productos
  productos.forEach(producto => {
    if (categoria === 'todos' || producto.dataset.categoria === categoria) {
      producto.style.display = 'block';
      producto.style.animation = 'fadeIn 0.5s ease-in-out';
    } else {
      producto.style.display = 'none';
    }
  });
}

function eliminarDelCarrito(index) {
  carrito.splice(index, 1);
  localStorage.setItem('carrito', JSON.stringify(carrito));
  actualizarCarrito();
  
  // Actualizar contador en navbar
  if (window.actualizarContadorCarrito) {
    window.actualizarContadorCarrito();
  }
}

// Nuevas funciones para mostrar modal con resumen y completar la compra
function finalizarCompra() {
  if (!carrito.length) {
    alert("El carrito está vacío.");
    return;
  }

  const resumenEl = document.getElementById("resumen-carrito");
  let suma = 0;
  const ul = document.createElement("ul");
  ul.className = "list-group mb-2";

  carrito.forEach(item => {
    const li = document.createElement("li");
    li.className = "list-group-item d-flex justify-content-between align-items-center";
    li.textContent = item.nombre;
    const span = document.createElement("span");
    span.textContent = `$${item.precio}`;
    li.appendChild(span);
    ul.appendChild(li);
    suma += item.precio;
  });

  const totalP = document.createElement("p");
  totalP.className = "fw-bold mt-2";
  totalP.textContent = `Total: $${suma.toFixed(2)}`;

  // Limpiar e insertar resumen
  resumenEl.innerHTML = "";
  resumenEl.appendChild(ul);
  resumenEl.appendChild(totalP);

  // Mostrar modal (Bootstrap 5)
  const modalEl = document.getElementById("confirmModal");
  const modal = new bootstrap.Modal(modalEl);
  modal.show();
}

async function completarCompra() {
  // Obtener datos del usuario si está logueado
  const userId = sessionStorage.getItem('userId');
  const total = carrito.reduce((sum, item) => sum + item.precio, 0);

  try {
    const response = await fetch(`${API_URL}/api/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        items: carrito,
        total: total,
        user_id: userId ? parseInt(userId) : null
      })
    });

    const data = await response.json();

    if (response.ok) {
      // Vaciar carrito y actualizar UI
      carrito = [];
      localStorage.removeItem('carrito');
      actualizarCarrito();

      // Actualizar contador en navbar
      if (window.actualizarContadorCarrito) {
        window.actualizarContadorCarrito();
      }

      const modalEl = document.getElementById("confirmModal");
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) modalInstance.hide();

      alert(data.message);
    } else {
      alert('Error al procesar la compra: ' + (data.detail || 'Error desconocido'));
    }
  } catch (error) {
    console.error('Error al conectar con el servidor:', error);
    alert('Error al conectar con el servidor. La compra no se pudo procesar.');
  }
}

// Función para finalizar compra desde modal (redirige a tienda si no estás ahí)
function finalizarCompraDesdeModal() {
  // Si no estamos en tienda.html, redirigir
  if (!window.location.pathname.includes('tienda.html')) {
    // Guardar que queremos finalizar
    sessionStorage.setItem('finalizarCompra', 'true');
    const isInPagesFolder = window.location.pathname.includes('/pages/');
    const tiendaPath = isInPagesFolder ? './tienda.html' : './pages/tienda.html';
    window.location.href = tiendaPath;
  } else {
    // Ya estamos en tienda, cerrar modal del carrito y abrir confirmación
    const carritoModal = bootstrap.Modal.getInstance(document.getElementById('carritoModal'));
    if (carritoModal) carritoModal.hide();
    finalizarCompra();
  }
}

// Al cargar tienda, verificar si se debe finalizar compra
if (window.location.pathname.includes('tienda.html')) {
  window.addEventListener('DOMContentLoaded', function() {
    if (sessionStorage.getItem('finalizarCompra') === 'true') {
      sessionStorage.removeItem('finalizarCompra');
      setTimeout(() => {
        finalizarCompra();
      }, 500);
    }
  });
}
