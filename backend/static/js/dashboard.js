// Dashboard JavaScript

async function loadDashboard() {
    try {
        const stats = await apiCall('/api/dashboard/stats');
        
        if (!stats) {
            console.error('Dashboard stats alınamadı');
            return;
        }
        
        // İstatistikleri göster
        const balanceEl = document.getElementById('balance');
        const totalQueriesEl = document.getElementById('total-queries');
        const totalCompaniesEl = document.getElementById('total-companies');
        const queriesTodayEl = document.getElementById('queries-today');
        
        if (balanceEl) balanceEl.textContent = stats.balance;
        if (totalQueriesEl) totalQueriesEl.textContent = stats.total_queries;
        if (totalCompaniesEl) totalCompaniesEl.textContent = stats.total_companies;
        if (queriesTodayEl) queriesTodayEl.textContent = stats.queries_today;
        
        // Son işlemler
        const transactionsDiv = document.getElementById('recent-transactions');
        if (transactionsDiv) {
            if (stats.recent_transactions.length === 0) {
                transactionsDiv.innerHTML = '<p class="text-secondary">Henüz işlem yok</p>';
            } else {
                transactionsDiv.innerHTML = stats.recent_transactions.map(t => `
                    <div class="transaction-item">
                        <div class="transaction-desc">${t.description}</div>
                        <div class="transaction-amount ${t.amount > 0 ? 'positive' : 'negative'}">
                            ${t.amount > 0 ? '+' : ''}${t.amount} kredi
                        </div>
                        <div class="transaction-date">${new Date(t.created_at).toLocaleString('tr-TR')}</div>
                    </div>
                `).join('');
            }
        }
        
        // Son sorgular
        const queriesDiv = document.getElementById('recent-queries');
        if (queriesDiv) {
            if (stats.recent_queries.length === 0) {
                queriesDiv.innerHTML = '<p class="text-secondary">Henüz sorgu yok</p>';
            } else {
                queriesDiv.innerHTML = stats.recent_queries.map(q => `
                    <div class="query-item">
                        <div class="query-info">
                            <strong>${q.kategori}</strong> - ${q.sehir || 'Tüm Şehirler'}
                        </div>
                        <div class="query-result">${q.result_count} sonuç</div>
                        <div class="query-date">${new Date(q.created_at).toLocaleString('tr-TR')}</div>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        console.error('Dashboard yükleme hatası:', error);
    }
}

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', () => {
    // Kullanıcı ve token kontrolü - birkaç kez dene
    let user = getUser();
    let token = getToken();
    
    console.log('=== DASHBOARD YÜKLENDİ ===');
    console.log('İlk kontrol - User:', user ? user.username : 'YOK');
    console.log('İlk kontrol - Token:', token ? 'Var (' + token.length + ' karakter)' : 'YOK');
    console.log('localStorage token:', localStorage.getItem('token'));
    console.log('localStorage user:', localStorage.getItem('user'));
    
    // Eğer ilk kontrolde yoksa, biraz bekle ve tekrar kontrol et
    if (!user || !token) {
        console.warn('İlk kontrolde bulunamadı, 500ms bekleniyor...');
        setTimeout(() => {
            user = getUser();
            token = getToken();
            console.log('İkinci kontrol - User:', user ? user.username : 'YOK');
            console.log('İkinci kontrol - Token:', token ? 'Var (' + token.length + ' karakter)' : 'YOK');
            
            if (!user || !token) {
                console.error('❌ Kullanıcı veya token bulunamadı!');
                console.error('User objesi:', user);
                console.error('Token:', token);
                console.error('localStorage içeriği:', {
                    token: localStorage.getItem('token'),
                    user: localStorage.getItem('user')
                });
                
                // 3 saniye bekle ki console'u okuyabilsin
                alert('Giriş yapmanız gerekiyor. 3 saniye sonra ana sayfaya yönlendirileceksiniz.');
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
                return;
            }
            
            // Bulundu, devam et
            initializeDashboard(user, token);
        }, 500);
    } else {
        // Bulundu, devam et
        initializeDashboard(user, token);
    }
});

function initializeDashboard(user, token) {
    console.log('✅ Dashboard başlatılıyor...');
    console.log('Kullanıcı:', user.username);
    console.log('Token uzunluğu:', token.length);
    
    // Navbar'ı güncelle
    const navUser = document.getElementById('nav-user');
    if (navUser) {
        navUser.textContent = `${user.username} (${user.balance} kredi)`;
    }
    
    loadDashboard();
    
    // Her 30 saniyede bir güncelle
    setInterval(loadDashboard, 30000);
}
