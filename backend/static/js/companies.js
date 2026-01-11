// Companies JavaScript

let companies = [];
let selectedCompanyId = null;
let sortColumn = null;
let sortDirection = 'asc';

async function loadConfig() {
    const config = await apiCall('/api/config/');
    return config;
}

async function loadCompanies() {
    const sehir = document.getElementById('filter-sehir').value;
    const ilce = document.getElementById('filter-ilce').value;
    const asama = document.getElementById('filter-asama').value;
    const telefon = document.getElementById('filter-telefon').value;
    
    try {
        const params = new URLSearchParams();
        if (sehir && sehir !== 'Hepsi') params.append('sehir_filtre', sehir);
        if (ilce && ilce !== 'Hepsi') params.append('ilce_filtre', ilce);
        if (asama && asama !== 'Hepsi') params.append('asama_filtre', asama);
        if (telefon && telefon !== 'hepsi') params.append('telefon_filtre', telefon);
        
        companies = await apiCall(`/api/companies/?${params.toString()}`);
        
        updateCompaniesTable();
        updateFilters();
    } catch (error) {
        console.error('Firmalar yükleme hatası:', error);
    }
}

function updateCompaniesTable() {
    const tbody = document.getElementById('companies-tbody');
    
    if (companies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">Firma bulunamadı</td></tr>';
        return;
    }
    
    // Sıralama
    if (sortColumn) {
        companies.sort((a, b) => {
            const aVal = a[sortColumn] || '';
            const bVal = b[sortColumn] || '';
            const comparison = aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
            return sortDirection === 'asc' ? comparison : -comparison;
        });
    }
    
    tbody.innerHTML = companies.map(company => `
        <tr class="company-row ${selectedCompanyId === company.id ? 'selected' : ''}" 
            onclick="selectCompany(${company.id})">
            <td>${company.firma_adi || ''}</td>
            <td>${company.sehir || ''}</td>
            <td>${company.ilce || ''}</td>
            <td>${company.kategori || ''}</td>
            <td>${company.telefon || ''}</td>
            <td>${company.rating || ''}</td>
        </tr>
    `).join('');
}

async function selectCompany(companyId) {
    selectedCompanyId = companyId;
    updateCompaniesTable();
    
    try {
        const company = await apiCall(`/api/companies/${companyId}`);
        const activities = await apiCall(`/api/companies/${companyId}/activities`);
        
        const config = await loadConfig();
        
        const detailPanel = document.getElementById('detail-panel');
        detailPanel.innerHTML = `
            <h3>${company.firma_adi}</h3>
            <div class="detail-info">
                <p><strong>Adres:</strong> ${company.adres || 'Yok'}</p>
                <p><strong>Şehir:</strong> ${company.sehir || 'Yok'}</p>
                <p><strong>İlçe:</strong> ${company.ilce || 'Yok'}</p>
                <p><strong>Telefon:</strong> ${company.telefon || 'Yok'}</p>
                <p><strong>Web:</strong> ${company.web ? `<a href="${company.web}" target="_blank">${company.web}</a>` : 'Yok'}</p>
                <p><strong>Kategori:</strong> ${company.kategori || 'Yok'}</p>
                ${company.rating ? `<p><strong>Rating:</strong> ${company.rating} (${company.user_ratings_total || 0} değerlendirme)</p>` : ''}
            </div>
            
            <div class="form-group" style="margin-top: 1rem;">
                <label>Aşama</label>
                <select id="company-asama" onchange="updateCompanyStage(${companyId})">
                    ${config.asama_secenekleri.map(a => 
                        `<option value="${a}" ${company.asama === a ? 'selected' : ''}>${a}</option>`
                    ).join('')}
                </select>
            </div>
            
            <div style="margin-top: 1rem;">
                <h4>Aktiviteler</h4>
                <div id="activities-list">
                    ${activities.map(a => `
                        <div style="padding: 0.5rem; background: var(--bg-hover); margin-bottom: 0.5rem; border-radius: 4px;">
                            <strong>${a.aktivite_tipi}</strong>
                            ${a.sonuc ? `<p>${a.sonuc}</p>` : ''}
                            <small>${new Date(a.created_at).toLocaleString('tr-TR')}</small>
                            <button class="btn btn-danger btn-small" onclick="deleteActivity(${companyId}, ${a.id})">Sil</button>
                        </div>
                    `).join('')}
                </div>
                
                <div class="form-group" style="margin-top: 1rem;">
                    <label>Yeni Aktivite</label>
                    <select id="new-activity-type">
                        ${config.aktivite_tipleri.map(t => `<option value="${t}">${t}</option>`).join('')}
                    </select>
                    <textarea id="new-activity-result" placeholder="Sonuç/Not" style="margin-top: 0.5rem;"></textarea>
                    <button class="btn" onclick="addActivity(${companyId})" style="margin-top: 0.5rem;">Ekle</button>
                </div>
            </div>
            
            <button class="btn btn-danger" onclick="deleteCompany(${companyId})" style="margin-top: 1rem;">Firmayı Sil</button>
        `;
    } catch (error) {
        console.error('Firma detay yükleme hatası:', error);
    }
}

async function updateCompanyStage(companyId) {
    const asama = document.getElementById('company-asama').value;
    
    try {
        await apiCall(`/api/companies/${companyId}`, {
            method: 'PATCH',
            body: JSON.stringify({ asama })
        });
        
        // Listeyi güncelle
        const company = companies.find(c => c.id === companyId);
        if (company) {
            company.asama = asama;
        }
    } catch (error) {
        console.error('Aşama güncelleme hatası:', error);
    }
}

async function addActivity(companyId) {
    const aktivite_tipi = document.getElementById('new-activity-type').value;
    const sonuc = document.getElementById('new-activity-result').value;
    
    try {
        await apiCall(`/api/companies/${companyId}/activities`, {
            method: 'POST',
            body: JSON.stringify({ aktivite_tipi, sonuc })
        });
        
        selectCompany(companyId); // Detay panelini yenile
    } catch (error) {
        console.error('Aktivite ekleme hatası:', error);
    }
}

async function deleteActivity(companyId, activityId) {
    if (!confirm('Aktiviteyi silmek istediğinize emin misiniz?')) return;
    
    try {
        await apiCall(`/api/companies/${companyId}/activities/${activityId}`, {
            method: 'DELETE'
        });
        
        selectCompany(companyId); // Detay panelini yenile
    } catch (error) {
        console.error('Aktivite silme hatası:', error);
    }
}

async function deleteCompany(companyId) {
    if (!confirm('Firmayı silmek istediğinize emin misiniz?')) return;
    
    try {
        await apiCall(`/api/companies/${companyId}`, {
            method: 'DELETE'
        });
        
        selectedCompanyId = null;
        loadCompanies();
    } catch (error) {
        console.error('Firma silme hatası:', error);
    }
}

async function updateFilters() {
    // Şehirleri getir
    const cities = await apiCall('/api/companies/filters/cities');
    const sehirSelect = document.getElementById('filter-sehir');
    sehirSelect.innerHTML = '<option value="Hepsi">Hepsi</option>';
    cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        sehirSelect.appendChild(option);
    });
    
    // İlçeleri getir
    const sehir = sehirSelect.value;
    const districts = await apiCall(`/api/companies/filters/districts?sehir=${sehir || ''}`);
    const ilceSelect = document.getElementById('filter-ilce');
    ilceSelect.innerHTML = '<option value="Hepsi">Hepsi</option>';
    districts.forEach(district => {
        const option = document.createElement('option');
        option.value = district;
        option.textContent = district;
        ilceSelect.appendChild(option);
    });
    
    // Aşama seçeneklerini getir
    const config = await loadConfig();
    const asamaSelect = document.getElementById('filter-asama');
    asamaSelect.innerHTML = '<option value="Hepsi">Hepsi</option>';
    config.asama_secenekleri.forEach(asama => {
        const option = document.createElement('option');
        option.value = asama;
        option.textContent = asama;
        asamaSelect.appendChild(option);
    });
    
    // Şehir değiştiğinde ilçeleri güncelle
    sehirSelect.addEventListener('change', () => {
        updateFilters();
    });
}

async function exportExcel() {
    const sehir = document.getElementById('filter-sehir').value;
    const ilce = document.getElementById('filter-ilce').value;
    const asama = document.getElementById('filter-asama').value;
    const telefon = document.getElementById('filter-telefon').value;
    
    const params = new URLSearchParams();
    if (sehir && sehir !== 'Hepsi') params.append('sehir_filtre', sehir);
    if (ilce && ilce !== 'Hepsi') params.append('ilce_filtre', ilce);
    if (asama && asama !== 'Hepsi') params.append('asama_filtre', asama);
    if (telefon && telefon !== 'hepsi') params.append('telefon_filtre', telefon);
    
    const token = getToken();
    const url = `${API_BASE}/api/excel/export?${params.toString()}`;
    
    const response = await fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (response.ok) {
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `firmalar_${new Date().getTime()}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(downloadUrl);
    } else {
        alert('Excel export hatası');
    }
}

function sortTable(column) {
    if (sortColumn === column) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn = column;
        sortDirection = 'asc';
    }
    updateCompaniesTable();
}

document.addEventListener('DOMContentLoaded', () => {
    const user = getUser();
    if (!user) {
        window.location.href = '/';
        return;
    }
    
    loadCompanies();
    updateFilters();
});

