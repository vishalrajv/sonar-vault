document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const statusMessage = document.getElementById('status-message');
    const submitBtn = document.getElementById('submit-btn');

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Clear previous messages
            statusMessage.classList.add('d-none');
            statusMessage.classList.remove('alert-danger', 'alert-success');
            
            // Get form data
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());
            
            // Disable button
            submitBtn.disabled = true;
            submitBtn.textContent = 'Registering...';

            try {
                const response = await fetch('/api/v1/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                const result = await response.json();

                if (response.ok) {
                    statusMessage.textContent = 'Registration submitted successfully! Please await admin approval before logging in.';
                    statusMessage.classList.remove('d-none');
                    statusMessage.classList.add('alert-success');
                    registerForm.reset();
                } else {
                    statusMessage.textContent = result.detail || 'Registration failed. Please try again.';
                    statusMessage.classList.remove('d-none');
                    statusMessage.classList.add('alert-danger');
                }
            } catch (error) {
                console.error('Error during registration:', error);
                statusMessage.textContent = 'A network error occurred. Please check your connection.';
                statusMessage.classList.remove('d-none');
                statusMessage.classList.add('alert-danger');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Register Account';
            }
        });
    }
});
