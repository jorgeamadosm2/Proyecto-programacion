document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('.register-form');
    const API_URL = 'http://localhost:8000';

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        const phone = document.getElementById('phone').value.trim();
        const email = document.getElementById('email').value.trim();

        try {
            const response = await fetch(`${API_URL}/api/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password,
                    phone: phone
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Guardar sesión
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('username', data.user.username);
                sessionStorage.setItem('email', data.user.email);
                sessionStorage.setItem('userId', data.user.id);

                // Mensaje de éxito
                alert(data.message);
                
                // Redirigir al index
                window.location.href = '../index.html';
            } else {
                alert(data.detail || 'Error al registrar usuario');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error al conectar con el servidor. Asegúrate de que el backend esté funcionando.');
        }
    });
});