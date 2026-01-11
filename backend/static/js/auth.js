// Authentication JavaScript

// Tab switching
document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const forms = document.querySelectorAll('.auth-form');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            
            // Remove active class from all
            tabButtons.forEach(b => b.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));
            
            // Add active class to selected
            btn.classList.add('active');
            document.getElementById(`${tab}-form`).classList.add('active');
        });
    });
});

async function handleLogin() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');
    
    if (!username || !password) {
        errorDiv.textContent = 'Lütfen tüm alanları doldurun';
        return;
    }
    
    errorDiv.textContent = '';
    
    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Giriş başarısız');
        }
        
        // Token ve kullanıcı bilgisini kaydet
        console.log('Login - Token kaydediliyor:', data.access_token ? 'Token var (' + data.access_token.length + ' karakter)' : 'Token yok');
        console.log('Login - User data:', data.user);
        
        if (!data.access_token) {
            console.error('HATA: Token response\'da yok!');
            errorDiv.textContent = 'Token alınamadı, lütfen tekrar deneyin';
            return;
        }
        
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Kontrol et
        const savedToken = localStorage.getItem('token');
        const savedUser = localStorage.getItem('user');
        console.log('Login - Token kaydedildi, localStorage kontrol:', savedToken ? 'OK (' + savedToken.length + ' karakter)' : 'HATA');
        console.log('Login - User kaydedildi, localStorage kontrol:', savedUser ? 'OK' : 'HATA');
        
        if (!savedToken || !savedUser) {
            console.error('HATA: Token veya user localStorage\'a kaydedilemedi!');
            errorDiv.textContent = 'Veri kaydedilemedi, lütfen tekrar deneyin';
            return;
        }
        
        // Kısa bir bekleme sonra dashboard'a yönlendir (localStorage'ın yazılması için)
        setTimeout(() => {
            console.log('Dashboard\'a yönlendiriliyor...');
            window.location.href = '/dashboard';
        }, 100);
    } catch (error) {
        errorDiv.textContent = error.message;
    }
}

async function handleRegister() {
    const email = document.getElementById('register-email').value;
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const errorDiv = document.getElementById('register-error');
    
    if (!email || !username || !password) {
        errorDiv.textContent = 'Lütfen tüm alanları doldurun';
        return;
    }
    
    if (password.length < 6) {
        errorDiv.textContent = 'Şifre en az 6 karakter olmalı';
        return;
    }
    
    errorDiv.textContent = '';
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                username,
                password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Kayıt başarısız');
        }
        
        // Token ve kullanıcı bilgisini kaydet
        console.log('Register - Token kaydediliyor:', data.access_token ? 'Token var (' + data.access_token.length + ' karakter)' : 'Token yok');
        console.log('Register - User data:', data.user);
        
        if (!data.access_token) {
            console.error('HATA: Token response\'da yok!');
            errorDiv.textContent = 'Token alınamadı, lütfen tekrar deneyin';
            return;
        }
        
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Kontrol et
        const savedToken = localStorage.getItem('token');
        const savedUser = localStorage.getItem('user');
        console.log('Register - Token kaydedildi, localStorage kontrol:', savedToken ? 'OK (' + savedToken.length + ' karakter)' : 'HATA');
        console.log('Register - User kaydedildi, localStorage kontrol:', savedUser ? 'OK' : 'HATA');
        
        if (!savedToken || !savedUser) {
            console.error('HATA: Token veya user localStorage\'a kaydedilemedi!');
            errorDiv.textContent = 'Veri kaydedilemedi, lütfen tekrar deneyin';
            return;
        }
        
        // Kısa bir bekleme sonra dashboard'a yönlendir (localStorage'ın yazılması için)
        setTimeout(() => {
            console.log('Dashboard\'a yönlendiriliyor...');
            window.location.href = '/dashboard';
        }, 100);
    } catch (error) {
        errorDiv.textContent = error.message;
    }
}

// Enter key ile submit
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    [loginForm, registerForm].forEach(form => {
        if (form) {
            form.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    if (form.id === 'login-form') {
                        handleLogin();
                    } else {
                        handleRegister();
                    }
                }
            });
        }
    });
});
