// Search JavaScript

let configData = null;

async function loadConfig() {
    if (!configData) {
        configData = await apiCall('/api/config/');
    }
    return configData;
}

async function initSearchPage() {
    const config = await loadConfig();
    
    // Şehir dropdown'ını doldur
    const sehirSelect = document.getElementById('search-sehir');
    config.sehirler.forEach(sehir => {
        const option = document.createElement('option');
        option.value = sehir;
        option.textContent = sehir;
        sehirSelect.appendChild(option);
    });
    
    // Ülke dropdown'ını doldur
    const ulkeSelect = document.getElementById('search-ulke');
    config.ulkeler.forEach(ulke => {
        const option = document.createElement('option');
        option.value = ulke;
        option.textContent = ulke;
        ulkeSelect.appendChild(option);
    });
}

async function handleSearch() {
    const sehir = document.getElementById('search-sehir').value;
    const ulke = document.getElementById('search-ulke').value;
    const kategori = document.getElementById('search-kategori').value;
    const limit = parseInt(document.getElementById('search-limit').value);
    const tumSehirler = document.getElementById('search-tum-sehirler').checked;
    const telefonFiltre = document.getElementById('search-telefon-filtre').checked;
    const errorDiv = document.getElementById('search-error');
    const loadingBar = document.getElementById('loading-bar');
    const resultsDiv = document.getElementById('search-results');
    
    if (!kategori) {
        errorDiv.textContent = 'Lütfen kategori girin';
        return;
    }
    
    if (!tumSehirler && !sehir) {
        errorDiv.textContent = 'Lütfen şehir seçin veya "Tüm Şehirler" işaretleyin';
        return;
    }
    
    errorDiv.textContent = '';
    loadingBar.classList.add('active');
    resultsDiv.innerHTML = '';
    
    try {
        const response = await apiCall('/api/search/', {
            method: 'POST',
            body: JSON.stringify({
                sehir: tumSehirler ? null : sehir,
                ulke,
                kategori,
                limit,
                tum_sehirler: tumSehirler,
                telefon_filtre: telefonFiltre
            })
        });
        
        if (!response) return;
        
        // Kullanıcı bakiyesini güncelle
        const user = getUser();
        if (user) {
            user.balance = response.remaining_balance;
            setUser(user);
            updateNavUser();
        }
        
        // Sonuçları göster
        if (response.companies.length === 0) {
            resultsDiv.innerHTML = '<p>Sonuç bulunamadı</p>';
        } else {
            resultsDiv.innerHTML = `
                <h2>${response.total_found} sonuç bulundu (${response.credits_used} kredi harcandı)</h2>
                ${response.companies.map(company => `
                    <div class="result-item">
                        <h3>${company.firma_adi}</h3>
                        <p><strong>Adres:</strong> ${company.adres || 'Yok'}</p>
                        <p><strong>Şehir:</strong> ${company.sehir || 'Yok'}</p>
                        <p><strong>İlçe:</strong> ${company.ilce || 'Yok'}</p>
                        <p><strong>Telefon:</strong> ${company.telefon || 'Yok'}</p>
                        <p><strong>Web:</strong> ${company.web ? `<a href="${company.web}" target="_blank">${company.web}</a>` : 'Yok'}</p>
                        ${company.rating ? `<p><strong>Rating:</strong> ${company.rating} (${company.user_ratings_total || 0} değerlendirme)</p>` : ''}
                    </div>
                `).join('')}
            `;
        }
    } catch (error) {
        errorDiv.textContent = error.message;
    } finally {
        loadingBar.classList.remove('active');
    }
}

function updateNavUser() {
    const navUser = document.getElementById('nav-user');
    if (navUser) {
        const user = getUser();
        if (user) {
            navUser.textContent = `${user.username} (${user.balance} kredi)`;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const user = getUser();
    if (!user) {
        window.location.href = '/';
        return;
    }
    
    initSearchPage();
});

