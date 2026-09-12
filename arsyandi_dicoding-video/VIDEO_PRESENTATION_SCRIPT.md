# Naskah Presentasi Video Singkat (Maksimal 5 Menit)
## Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan (Jaya Jaya Institut)

> **Catatan untuk Mahasiswa**: Naskah ini disusun terstruktur untuk video presentasi berdurasi **3 - 5 menit** guna memenuhi kriteria penilaian bintang 5 (*Rating 5/5*) pada submission Dicoding. Anda dapat merekam layar (screen recording) menggunakan OBS Studio, Loom, atau PowerPoint sambil membaca naskah ini.

---

### ⏱️ Timeline & Alur Video (Total Durasi: ~4 Menit 30 Detik)

| Waktu | Bagian | Fokus Pembahasan | Visual Screen Record |
| :--- | :--- | :--- | :--- |
| **00:00 - 00:45** | **1. Pembuka & Latar Belakang Bisnis** | Profil Jaya Jaya Institut, masalah dropout (32.1%), urgensi early detection | Slide Judul / `README.md` / Beranda Aplikasi |
| **00:45 - 02:00** | **2. Walkthrough Business Dashboard** | KPI Cards, faktor pemicu (SPP, SKS Semester 1 & 2, Prodi berisiko) | Tab "📊 Executive Dashboard" pada `app.py` |
| **02:00 - 03:15** | **3. Solusi Machine Learning & Demo Sistem** | Model Random Forest, form prediksi individu, gauge risiko, batch CSV | Tab "🎯 Prediksi Risiko" & "📁 Batch Prediction" |
| **03:15 - 04:15** | **4. Kesimpulan & Rekomendasi Action Items** | 3 kesimpulan utama & 5 rekomendasi strategis implementasi | Tab "💡 Panduan Aksi & Insights" / Slide Action Items |
| **04:15 - 04:30** | **5. Penutup** | Penutup & terima kasih | Tampilan akhir aplikasi web |

---

### 🎙️ Naskah Lengkap (Script Kata Demi Kata)

#### 1. Pembuka & Latar Belakang Bisnis (00:00 - 00:45)
> *"Halo semuanya! Selamat datang di presentasi Proyek Akhir Penerapan Data Science untuk studi kasus Jaya Jaya Institut.*  
> 
> *Jaya Jaya Institut adalah perguruan tinggi yang telah berdiri sejak tahun 2000 dengan reputasi yang sangat baik. Namun, pihak institusi menghadapi tantangan besar: angka dropout mahasiswa mencapai **32.1%**, yang berarti hampir satu dari tiga mahasiswa tidak menyelesaikan studinya.*  
> 
> *Tingginya angka dropout ini mengancam akreditasi kampus, menimbulkan kerugian finansial, dan menurunkan efisiensi akademik. Untuk menyelesaikan masalah ini, saya mengembangkan dua solusi utama: pertama, **Business Dashboard** untuk monitoring performa mahasiswa, dan kedua, **Sistem Prediksi Machine Learning** sebagai Early Warning System deteksi dini risiko dropout."*

---

#### 2. Menjelaskan Business Dashboard yang Dibuat (00:45 - 02:00)
*(Arahkan layar ke tab "📊 Executive Dashboard" pada Streamlit `app.py`)*

> *"Mari kita lihat Business Dashboard yang telah saya kembangkan.*  
> 
> *Di bagian atas dashboard, terdapat Executive KPI Cards yang merangkum kondisi 4.424 mahasiswa: tingkat kelulusan 49.9%, tingkat dropout 32.1%, dan 11.4% mahasiswa tercatat memiliki tunggakan hutang.*  
> 
> *Dashboard ini dilengkapi filter interaktif per Program Studi, Status Pembayaran SPP, dan Status Beasiswa.*  
> 
> *Dari visualisasi analitik, kita menemukan tiga pola penting:*  
> 1. *Pertama, **Beban Finansial Sangat Berpengaruh**: Mahasiswa yang menunggak pembayaran SPP memiliki rasio dropout lebih dari **62%**, berbanding hanya 23% pada mahasiswa dengan pembayaran lancar.*  
> 2. *Kedua, **Performa Akademik Semester 1 dan 2 adalah Indikator Dini**: Mahasiswa yang lulus kurang dari 4 mata kuliah di tahun pertama memiliki kemungkinan dropout 4 kali lipat lebih tinggi.*  
> 3. *Ketiga, program studi teknologi terapan dan manajemen kelas malam memiliki tingkat dropout tertinggi, yang menandakan perlunya perhatian khusus pada mahasiswa yang kuliah sambil bekerja."*

---

#### 3. Menjelaskan Solusi Machine Learning & Demo Prototipe (02:00 - 03:15)
*(Arahkan layar ke tab "🎯 Prediksi Risiko Mahasiswa" dan "📁 Batch Prediction")*

> *"Selanjutnya, mari beralih ke solusi machine learning.*  
> 
> *Berdasarkan benchmark beberapa algoritma—termasuk Logistic Regression, Gradient Boosting, dan Random Forest—model terbaik yang dipilih adalah **Random Forest Classifier dengan pembobotan kelas seimbang (Balanced Class Weight)** pada klasifikasi biner (Graduate vs Dropout). Model ini berhasil mencapai **akurasi 92.98% (~93.0%)** dan **Macro F1-score 0.9264 (~0.93)**, dengan presisi mendeteksi kelas Dropout mencapai **91%** dan recall mencapai **92%**.*  
> 
> *Di menu Prediksi Risiko Individual, dosen wali atau staf bimbingan konseling dapat menginput data profil mahasiswa, mulai dari usia, status SPP, hutang, hingga SKS yang lulus di semester 1 dan 2.*  
> 
> *Ketika tombol Analisis Risiko diklik, sistem tidak hanya memprediksi status kelulusan, tetapi juga menampilkan **Gauge Bar Probabilitas Risiko (Tinggi, Sedang, atau Rendah)** beserta **Rekomendasi Rencana Aksi Intervensi Otomatis**.*  
> 
> *Selain prediksi individual, sistem ini juga menyediakan menu **Batch Prediction**, di mana staf kampus cukup mengunggah file CSV kumpulan data mahasiswa satu angkatan, dan sistem akan langsung menandai mahasiswa berisiko tinggi secara massal untuk diunduh hasilnya."*

---

#### 4. Kesimpulan & Rekomendasi Action Items (03:15 - 04:15)
*(Arahkan layar ke tab "💡 Panduan Aksi & Insights")*

> *"Dari proyek ini, terdapat tiga kesimpulan kunci:*  
> *1. Masalah dropout di Jaya Jaya Institut dipicu oleh kombinasi kegagalan akademik di semester awal dan kesulitan finansial pembayaran SPP.*  
> *2. Penerima beasiswa terbukti memiliki retensi sangat tinggi (kelulusan 76.3%).*  
> *3. Model machine learning yang dibangun terbukti efektif mengidentifikasi mahasiswa rentan sejak dini.*  
> 
> *Berdasarkan kesimpulan tersebut, saya merekomendasikan **5 Action Items Strategis** bagi institusi:*  
> 1. *Mengintegrasikan sistem machine learning ini ke SIAKAD kampus sebagai **Early Warning System otomatis** tiap akhir semester.*  
> 2. *Menyediakan **skema cicilan SPP bulanan fleksibel** dan bantuan dana darurat bagi mahasiswa berkendala biaya.*  
> 3. *Membuka **Klinik Akademik dan program Peer Tutoring wajib** bagi mahasiswa yang gagal ≥ 2 mata kuliah di semester 1.*  
> 4. *Memberikan **fleksibilitas materi perkuliahan daring asinkronus** bagi mahasiswa kelas malam dan pekerja.*  
> 5. *Melakukan **monitoring dan pendampingan proaktif** bagi mahasiswa penerima beasiswa sebelum performa mereka turun.*"

---

#### 5. Penutup (04:15 - 04:30)
> *"Dengan mengimplementasikan solusi data science dan sistem deteksi dini ini, Jaya Jaya Institut dapat menekan angka dropout secara signifikan dan membantu lebih banyak mahasiswa mencapai kelulusan tepat waktu.*  
> 
> *Terima kasih atas perhatian Anda, dan salam hangat!"*
