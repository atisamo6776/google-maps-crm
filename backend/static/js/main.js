// Main JavaScript - API helper functions

const API_BASE = window.location.origin;

// Token yönetimi
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function removeUser() {
    localStorage.removeItem('user');
}

// API çağrıları
async function apiCall(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            // Unauthorized - logout
            handleLogout();
            return null;
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Bir hata oluştu');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Logout
function handleLogout() {
    removeToken();
    removeUser();
    window.location.href = '/';
}

// Tema yönetimi
function getTheme() {
    const user = getUser();
    return user?.theme || 'dark';
}

function setTheme(theme) {
    const stylesheet = document.getElementById('theme-stylesheet');
    if (theme === 'dark') {
        stylesheet.href = '/static/css/dark.css';
    } else {
        stylesheet.href = '/static/css/light.css';
    }
    
    // Kullanıcı bilgisini güncelle
    const user = getUser();
    if (user) {
        user.theme = theme;
        setUser(user);
        
        // API'ye kaydet
        apiCall('/api/theme/', {
            method: 'PATCH',
            body: JSON.stringify({ theme })
        }).catch(console.error);
    }
}

// Sayfa yüklendiğinde temayı ayarla
document.addEventListener('DOMContentLoaded', () => {
    const theme = getTheme();
    setTheme(theme);
    
    // Theme toggle butonu
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = getTheme();
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
            themeToggle.textContent = newTheme === 'dark' ? '🌙' : '☀️';
        });
    }
});

// Kullanıcı bilgisini navbar'a yaz
document.addEventListener('DOMContentLoaded', () => {
    const navUser = document.getElementById('nav-user');
    if (navUser) {
        const user = getUser();
        if (user) {
            navUser.textContent = `${user.username} (${user.balance} kredi)`;
            
            // Admin link göster
            if (user.is_admin) {
                const adminLink = document.getElementById('admin-link');
                if (adminLink) {
                    adminLink.style.display = 'inline';
                }
            }
        }
    }
});

