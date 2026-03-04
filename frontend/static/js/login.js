document.addEventListener('DOMContentLoaded', () => {
    // Redirect if already logged in
    const token = localStorage.getItem('access_token');
    if (token) {
        window.location.href = '/dashboard';
        return;
    }

    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('remember_me').checked;
        
        errorMessage.classList.add('d-none');
        
        try {
            const response = await fetch('/api/v1/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    username, 
                    password,
                    remember_me: rememberMe
                }),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Successful login
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('token_type', data.token_type);
                localStorage.setItem('user_role', data.role);
                localStorage.setItem('user_full_name', data.full_name);
                localStorage.setItem('user_department', data.department);
                
                // Automatically redirect to dashboard
                window.location.href = '/dashboard';
            } else {
                // Error from server
                errorMessage.textContent = data.detail || 'Login failed. Please try again.';
                errorMessage.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = 'Network error. Please ensure the server is running.';
            errorMessage.classList.remove('d-none');
        }
    });
});
