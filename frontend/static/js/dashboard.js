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
    // Kullanıcı kontrolü
    const user = getUser();
    if (!user) {
        window.location.href = '/';
        return;
    }
    
    loadDashboard();
    
    // Her 30 saniyede bir güncelle
    setInterval(loadDashboard, 30000);
});
