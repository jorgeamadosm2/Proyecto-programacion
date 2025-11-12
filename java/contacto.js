// Funcionalidad para el formulario de contacto
document.addEventListener('DOMContentLoaded', function() {
    const formularioContacto = document.querySelector('form');
    
    formularioContacto.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevenir el envío normal del formulario
        
        // Obtener los valores del formulario
        const nombre = document.getElementById('nombre').value;
        const email = document.getElementById('email').value;
        const mensaje = document.getElementById('mensaje').value;
        
        // Validar que todos los campos estén completos
        if (nombre.trim() === '' || email.trim() === '' || mensaje.trim() === '') {
            mostrarPopup('Por favor, completa todos los campos del formulario.', 'error');
            return;
        }
        
        // Validar formato de email básico
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            mostrarPopup('Por favor, ingresa un correo electrónico válido.', 'error');
            return;
        }
        
        // Enviar correo electrónico usando EmailJS
        enviarCorreo(nombre, email, mensaje);
        
        // Limpiar el formulario
        formularioContacto.reset();
    });
});

function mostrarPopup(mensaje, tipo) {
    // Crear el elemento del popup
    const popup = document.createElement('div');
    popup.className = `popup-overlay ${tipo}`;
    
    popup.innerHTML = `
        <div class="popup-content">
            <div class="popup-header">
                <h4>${tipo === 'success' ? '¡Mensaje enviado!' : 'Error'}</h4>
                <button class="popup-close" onclick="cerrarPopup()">&times;</button>
            </div>
            <div class="popup-body">
                <p>${mensaje}</p>
            </div>
            <div class="popup-footer">
                <button class="btn-popup-cerrar" onclick="cerrarPopup()">Cerrar</button>
            </div>
        </div>
    `;
    
    // Agregar el popup al body
    document.body.appendChild(popup);
    
    // Mostrar el popup con animación
    setTimeout(() => {
        popup.classList.add('show');
    }, 10);
    
    // Auto cerrar después de 5 segundos si es de éxito
    if (tipo === 'success') {
        setTimeout(() => {
            cerrarPopup();
        }, 5000);
    }
}

function cerrarPopup() {
    const popup = document.querySelector('.popup-overlay');
    if (popup) {
        popup.classList.remove('show');
        setTimeout(() => {
            popup.remove();
        }, 300);
    }
}

// Cerrar popup al hacer clic fuera del contenido
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('popup-overlay')) {
        cerrarPopup();
    }
});

// Cerrar popup con la tecla Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        cerrarPopup();
    }
});

// Función para enviar correo electrónico
async function enviarCorreo(nombre, email, mensaje) {
    const API_URL = 'http://localhost:8000';
    
    // Mostrar mensaje de envío
    mostrarPopup('Enviando mensaje...', 'info');
    
    try {
        const response = await fetch(`${API_URL}/api/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: nombre,
                email: email,
                message: mensaje
            })
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Mensaje guardado exitosamente');
            
            // Cerrar popup de "enviando" y mostrar éxito
            cerrarPopup();
            setTimeout(() => {
                mostrarPopup(data.message, 'success');
            }, 300);
            
        } else {
            console.error('Error al guardar mensaje:', data.detail);
            cerrarPopup();
            setTimeout(() => {
                mostrarPopup('Hubo un error al enviar el mensaje. Por favor, inténtalo de nuevo.', 'error');
            }, 300);
        }
    } catch (error) {
        console.error('Error al conectar con el servidor:', error);
        cerrarPopup();
        setTimeout(() => {
            mostrarPopup('Error al conectar con el servidor. Por favor, inténtalo de nuevo.', 'error');
        }, 300);
    }
}