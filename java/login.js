document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');
    const API_URL = 'http://localhost:8000';

    if (!loginForm) return;

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Quitar mensaje de error anterior
        const oldError = loginForm.querySelector('.error-message');
        if (oldError) oldError.remove();

        // Obtener valores del formulario
        const emailInput = loginForm.querySelector('input[type="text"]') || loginForm.querySelector('input[name="email"]');
        const passwordInput = loginForm.querySelector('input[type="password"]');

        const email = emailInput ? emailInput.value.trim() : '';
        const password = passwordInput ? passwordInput.value.trim() : '';

        if (!email || !password) {
            showError('Por favor ingresa email y contraseña.');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Guardar sesión
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('username', data.user.username);
                sessionStorage.setItem('email', data.user.email);
                sessionStorage.setItem('userId', data.user.id);
                sessionStorage.setItem('user', JSON.stringify(data.user));

                alert(data.message);
                window.location.href = '../index.html';
            } else {
                showError(data.detail || 'Usuario o contraseña incorrectos');
            }

        } catch (error) {
            console.error('Error:', error);
            showError('Error al conectar con el servidor. Asegúrate de que el backend esté funcionando.');
        }
    });

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = 'red';
        errorDiv.style.marginTop = '10px';
        errorDiv.style.textAlign = 'center';
        errorDiv.style.fontSize = '14px';
        errorDiv.setAttribute('role', 'alert');
        errorDiv.textContent = message;
        loginForm.appendChild(errorDiv);
    }
});
