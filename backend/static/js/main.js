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
    
    // Debug: Token kontrolü
    if (!token) {
        console.warn('Token bulunamadı! localStorage:', localStorage.getItem('token'));
    } else {
        console.log('Token bulundu, uzunluk:', token.length);
    }
    
    // Headers oluştur
    const headers = {
        ...options.headers
    };
    
    // Content-Type sadece body varsa ekle
    if (options.body && !headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
    }
    
    // Token varsa Authorization header ekle
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
        console.log('Authorization header eklendi');
    } else {
        console.warn('Token yok, Authorization header eklenmedi!');
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            // Unauthorized - logout
            console.error('401 Unauthorized - Token geçersiz veya eksik');
            console.error('Response status:', response.status);
            console.error('Response headers:', response.headers);
            // YÖNLENDİRMEYİ KALDIR - SADECE LOG
            // handleLogout();
            return null;
        }
        
        // Response'u parse et
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            data = await response.text();
        }
        
        if (!response.ok) {
            throw new Error(data.detail || data || 'Bir hata oluştu');
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
    if (stylesheet) {
        if (theme === 'dark') {
            stylesheet.href = '/static/css/dark.css';
        } else {
            stylesheet.href = '/static/css/light.css';
        }
    }
    
    // Kullanıcı bilgisini güncelle
    const user = getUser();
    if (user) {
        user.theme = theme;
        setUser(user);
        
        // API'ye kaydet (token kontrolü ile)
        const token = getToken();
        if (token) {
            fetch(`${API_BASE}/api/theme/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ theme })
            }).catch(console.error);
        }
    }
}

// Sayfa yüklendiğinde temayı ayarla
document.addEventListener('DOMContentLoaded', () => {
    // Debug: Token kontrolü
    const token = getToken();
    const user = getUser();
    console.log('Sayfa yüklendi - Token:', token ? 'Var (' + token.length + ' karakter)' : 'YOK');
    console.log('Sayfa yüklendi - User:', user ? user.username : 'YOK');
    
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
    
    // Kullanıcı bilgisini navbar'a yaz
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
