const API_URL = "http://127.0.0.1:8000/api";

// Require login check for non-login pages
if (!localStorage.getItem("token") && !window.location.href.includes("index.html")) {
    window.location.href = "index.html";
}

function logout() {
    localStorage.clear();
    // Gunakan confirm agar tidak mengagetkan, atau langsung alert
    if (confirm("Apakah Anda yakin ingin keluar?")) {
        localStorage.clear();
        window.location.href = "index.html";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const userInfo = document.getElementById("user-info");
    if (userInfo) {
        userInfo.innerText = `NRP: ${localStorage.getItem("nrp")} (${localStorage.getItem("role")})`;
    }
    // Call fetchHistory and fetchFieldExpenses on DOMContentLoaded
    fetchHistory();
    fetchFieldExpenses();
});

async function fetchHistory() {
    const token = localStorage.getItem("token");
    const nrp = localStorage.getItem("nrp");
    if (!token) return;

    // Menampilkan NRP di badge
    const userInfo = document.getElementById("user-info");
    if (userInfo) userInfo.innerHTML = `<i class="ph-fill ph-user"></i> NRP: ${nrp}`;

    // Handle Visibilitas Anggaran Sistem (Hanya Admin)
    const role = localStorage.getItem("role");
    const adminBudgetCard = document.getElementById("admin-budget-card");
    if (adminBudgetCard) {
        if (role !== 'keuangan') {
            adminBudgetCard.style.display = 'none';
            // Hilangkan border left pada dompet lapangan jika budget sistem hilang
            const fieldWallet = document.getElementById("field-wallet-view").parentNode;
            fieldWallet.style.borderLeft = "none";
            fieldWallet.style.paddingLeft = "0";
        }
    }

    try {
        const response = await fetch(`${API_URL}/reimburse/history/1`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await response.json();
        const listContainer = document.getElementById("reimburse-list");
        if (!listContainer) return;

        if (data.length === 0) {
            listContainer.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-secondary);">Belum ada riwayat pengajuan.</div>`;
            return;
        }

        let totalApproved = 0;
        listContainer.innerHTML = "";
        data.forEach(trx => {
            if (trx.status === "Disetujui") totalApproved += trx.nominal_diajukan;
            const div = document.createElement("div");
            div.className = "transaction-item";

            let statusClass = "status-pending";
            if (trx.status === "Disetujui") statusClass = "status-approved";
            if (trx.status === "Ditolak") statusClass = "status-rejected";

            div.innerHTML = `
                <div class="item-info">
                    <h4>Pengajuan #${trx.id} ${trx.foto_kuitansi_url ? '' : '(Manual)'}</h4>
                    <div class="meta">
                        <i class="ph ph-calendar"></i> ${new Date(trx.tanggal_pengajuan).toLocaleDateString()}
                    </div>
                    <div class="status-label ${statusClass}">${trx.status}</div>
                    ${trx.catatan_ai ? `<div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 5px;">${trx.catatan_ai}</div>` : ''}
                </div>
                <div class="amount-display">
                    Rp ${trx.nominal_diajukan.toLocaleString('id-ID')}
                </div>
            `;
            listContainer.appendChild(div);
        });

        // Update budget view
        const totalBudget = document.getElementById("total-budget-view");
        if (totalBudget) {
            const plaforn = 10000000; // Contoh plafon tetap
            totalBudget.innerText = `Rp ${(plaforn - totalApproved).toLocaleString('id-ID')}`;
            // Simpan saldo lapangan (total yang disetujui - pengeluaran lapangan)
            localStorage.setItem("approved_total", totalApproved);
            updateFieldWallet(totalApproved);
        }

    } catch (error) {
        console.error("Error fetching history:", error);
    }
}

// Fitur Dana Lapangan (Personal Funds)
async function fetchFieldExpenses() {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
        const response = await fetch(`${API_URL}/reimburse/field-expenses/1`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await response.json();
        const list = document.getElementById("field-expense-list");
        if (!list) return;

        if (data.length === 0) {
            list.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-secondary);">Belum ada catatan pengeluaran mandiri.</div>`;
            updateFieldWallet(parseInt(localStorage.getItem("approved_total") || 0), 0);
            return;
        }

        let totalExp = 0;
        list.innerHTML = "";
        data.forEach(exp => {
            totalExp += exp.nominal;
            const div = document.createElement("div");
            div.className = "transaction-item";
            div.innerHTML = `
                <div class="item-info">
                    <h4>${exp.keterangan}</h4>
                    <div class="meta">${new Date(exp.tanggal).toLocaleDateString()}</div>
                </div>
                <div class="amount-display" style="color: var(--danger-color)">
                    - Rp ${exp.nominal.toLocaleString('id-ID')}
                </div>
            `;
            list.appendChild(div);
        });
        updateFieldWallet(parseInt(localStorage.getItem("approved_total") || 0), totalExp);
    } catch (e) { console.error(e); }
}

function updateFieldWallet(totalCair, totalPakai = 0) {
    const fieldWallet = document.getElementById("field-wallet-view");
    if (fieldWallet) {
        fieldWallet.innerText = `Rp ${(totalCair - totalPakai).toLocaleString('id-ID')}`;
    }
}

// Submit Field Expense
document.getElementById("expense-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token"); // Ensure token is available for this request
    const nominal = document.getElementById("exp-nominal").value;
    const keterangan = document.getElementById("exp-ket").value;

    const formData = new FormData();
    formData.append("user_id", 1);
    formData.append("nominal", nominal);
    formData.append("keterangan", keterangan);

    try {
        await fetch(`${API_URL}/reimburse/field-expense`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }, // Add Authorization header
            body: formData
        });
        location.reload();
    } catch (e) { alert("Gagal menyimpan"); }
});

// Submit Reimburse (Fixed for Optional File)
document.getElementById("reimburse-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token"); // Ensure token is available for this request
    const btn = e.target.querySelector('button');
    btn.disabled = true;
    btn.innerText = "Mengirim...";

    const formData = new FormData();
    formData.append("budget_id", document.getElementById("budget-id").value);
    formData.append("nominal_diajukan", document.getElementById("nominal").value);
    formData.append("user_id", 1); // Mock 1 for now

    const fileInput = document.getElementById("foto");
    if (fileInput && fileInput.files[0]) {
        formData.append("file", fileInput.files[0]);
        btn.innerText = "Memproses AI OCR..."; // Show AI processing if file is present
    }

    try {
        const response = await fetch(`${API_URL}/reimburse/upload`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });

        if (response.ok) {
            alert("Pengajuan berhasil disimpan dan dibaca oleh AI!");
            window.location.href = "dashboard.html";
        } else {
            alert("Gagal submit pengajuan: " + JSON.stringify(err));
            btn.innerText = "Kirim Laporan";
            btn.disabled = false;
        }
    } catch (error) {
        console.error("Error submit:", error);
        alert("Gagal terhubung ke backend");
    }
});
