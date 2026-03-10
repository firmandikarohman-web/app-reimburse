const API_URL = "http://127.0.0.1:8000/api";

// Login Logic
document.getElementById("login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nrp = document.getElementById("nrp").value;
    const password = document.getElementById("password").value;

    // Check if UI is in Admin Mode
    const isAdminMode = document.getElementById('auth-title')?.innerText.includes("Admin");

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nrp, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Role Validation for Admin Mode
            if (isAdminMode && data.role !== 'keuangan') {
                alert("Akses Ditolak: Akun ini bukan akun Admin/Keuangan.");
                return;
            }

            localStorage.setItem("token", data.access_token);
            localStorage.setItem("nrp", data.nrp);
            localStorage.setItem("role", data.role);
            window.location.href = "dashboard.html";
        } else {
            alert(data.detail || "Login gagal");
        }
    } catch (error) {
        console.error("Error logging in:", error);
        alert("Gagal terhubung ke server. Pastikan backend sudah berjalan.");
    }
});

// Register Logic
document.getElementById("register-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nrp = document.getElementById("reg-nrp").value;
    const nama_lengkap = document.getElementById("reg-nama").value;
    const pangkat_satker = document.getElementById("reg-pangkat").value;
    const password = document.getElementById("reg-password").value;

    // Determine role based on UI mode
    const isAdminMode = document.getElementById('reg-title')?.innerText.includes("Admin");
    const role = isAdminMode ? "keuangan" : "anggota";

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nrp,
                nama_lengkap,
                pangkat_satker,
                password,
                role: role
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Pendaftaran berhasil! Silakan login.");
            toggleAuth(); // Switch back to login view
        } else {
            alert(data.detail || "Pendaftaran gagal");
        }
    } catch (error) {
        console.error("Error registering:", error);
        alert("Gagal terhubung ke server.");
    }
});

// Logout logic removed, moved to api.js
