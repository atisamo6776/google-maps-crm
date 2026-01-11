// Admin JavaScript

async function searchUsers() {
    const searchQuery = document.getElementById('user-search').value;
    
    try {
        const params = searchQuery ? `?search=${encodeURIComponent(searchQuery)}` : '';
        const users = await apiCall(`/api/admin/users${params}`);
        
        displayUsers(users);
    } catch (error) {
        console.error('Kullanıcı arama hatası:', error);
    }
}

function displayUsers(users) {
    const usersList = document.getElementById('users-list');
    
    if (users.length === 0) {
        usersList.innerHTML = '<p>Kullanıcı bulunamadı</p>';
        return;
    }
    
    usersList.innerHTML = users.map(user => `
        <div class="user-card">
            <div class="user-info">
                <h3>${user.username}</h3>
                <p>${user.email}</p>
                <p>Bakiye: <strong>${user.balance} kredi</strong></p>
                ${user.is_admin ? '<span style="color: var(--primary-color);">Admin</span>' : ''}
            </div>
            <div class="user-actions">
                <div class="credit-form">
                    <input type="number" id="credit-${user.id}" placeholder="Kredi miktarı" min="1">
                    <input type="text" id="desc-${user.id}" placeholder="Açıklama">
                    <button class="btn" onclick="addCredit(${user.id})">Kredi Ekle</button>
                </div>
                <button class="btn btn-secondary" onclick="viewTransactions(${user.id})">İşlemler</button>
            </div>
        </div>
    `).join('');
}

async function addCredit(userId) {
    const amount = parseInt(document.getElementById(`credit-${userId}`).value);
    const description = document.getElementById(`desc-${userId}`).value;
    
    if (!amount || amount <= 0) {
        alert('Geçerli bir kredi miktarı girin');
        return;
    }
    
    if (!description) {
        alert('Açıklama girin');
        return;
    }
    
    try {
        const result = await apiCall(`/api/admin/users/${userId}/credit`, {
            method: 'POST',
            body: JSON.stringify({ amount, description })
        });
        
        alert(`Kredi eklendi! Yeni bakiye: ${result.new_balance}`);
        searchUsers(); // Listeyi yenile
    } catch (error) {
        alert('Kredi ekleme hatası: ' + error.message);
    }
}

async function viewTransactions(userId) {
    try {
        const transactions = await apiCall(`/api/admin/users/${userId}/transactions`);
        
        const transactionsHtml = transactions.map(t => `
            <div style="padding: 0.5rem; background: var(--bg-hover); margin-bottom: 0.5rem; border-radius: 4px;">
                <strong>${t.description}</strong>
                <span style="color: ${t.amount > 0 ? 'var(--success-color)' : 'var(--danger-color)'};">
                    ${t.amount > 0 ? '+' : ''}${t.amount} kredi
                </span>
                <small>${new Date(t.created_at).toLocaleString('tr-TR')}</small>
            </div>
        `).join('');
        
        alert(`İşlem Geçmişi:\n\n${transactionsHtml || 'İşlem bulunamadı'}`);
    } catch (error) {
        console.error('İşlem geçmişi yükleme hatası:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const user = getUser();
    if (!user) {
        window.location.href = '/';
        return;
    }
    
    if (!user.is_admin) {
        alert('Bu sayfaya erişim yetkiniz yok');
        window.location.href = '/dashboard';
        return;
    }
    
    // Enter tuşu ile arama
    document.getElementById('user-search').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchUsers();
        }
    });
    
    searchUsers(); // İlk yüklemede tüm kullanıcıları göster
});

