# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech (Jaya Jaya Institut)

## Business Understanding
**Jaya Jaya Institut** merupakan institusi pendidikan tinggi terkemuka yang telah berdiri sejak tahun 2000. Sepanjang perjalanannya, institut ini telah berhasil mencetak banyak lulusan dengan reputasi yang sangat baik di berbagai bidang industri. Namun demikian, institusi menghadapi tantangan operasional dan akademis yang signifikan, yaitu **tingginya angka mahasiswa yang tidak menyelesaikan pendidikan atau *dropout*** (mencapai 32.1% dari total populasi mahasiswa).

Tingginya angka dropout ini berimplikasi langsung pada:
1. **Penurunan Akreditasi & Reputasi Kampus**: Rasio kelulusan tepat waktu (*completion rate*) merupakan salah satu indikator vital dalam penilaian akreditasi institusi pendidikan tinggi.
2. **Inisiatif Keuangan yang Tidak Efisien**: Pengurangan jumlah mahasiswa aktif di semester lanjut menurunkan pendapatan SPP dan meningkatkan biaya akuisisi mahasiswa baru.
3. **Ketidakmampuan Deteksi Dini**: Tim Bimbingan Konseling (BK) dan Dosen Pembimbing Akademik (DPA) terlambat mengetahui mahasiswa yang berisiko, sehingga upaya pertolongan sering kali dilakukan ketika mahasiswa sudah memutuskan untuk berhenti kuliah.

### Permasalahan Bisnis
Permasalahan utama yang dihadapi oleh Jaya Jaya Institut adalah:
1. Mengapa tingkat dropout di Jaya Jaya Institut tergolong tinggi (~32.1%) dan program studi apa saja yang memiliki rasio dropout tertinggi?
2. Faktor-faktor apa saja (finansial, demografi, latar belakang masuk, atau performa akademik semester awal) yang paling signifikan memicu keputusan mahasiswa untuk dropout?
3. Bagaimana merancang dan menerapkan sistem pendeteksian dini (*Early Warning System*) berbasis machine learning yang akurat guna mendeteksi mahasiswa yang rentan dropout sejak semester awal?
4. Apa strategi intervensi institusional dan rekomendasi aksi nyata (*action items*) yang harus diambil manajemen untuk menekan laju dropout dan meningkatkan angka kelulusan mahasiswa?

### Cakupan Proyek
Untuk menjawab permasalahan bisnis tersebut, cakupan proyek data science ini meliputi:
1. **Eksplorasi Data (Exploratory Data Analysis / EDA)**: Menganalisis 4.424 baris data mahasiswa dengan 36 fitur prediktor untuk mengidentifikasi korelasi antara performa akademik, beban finansial, usia, program studi, dan status kelulusan.
2. **Pemodelan Machine Learning**: Mengembangkan dan membandingkan beberapa algoritma klasifikasi (Logistic Regression, Random Forest, Gradient Boosting, HistGradientBoosting) dengan penanganan ketidakseimbangan kelas (*class weight balancing*) untuk memprediksi status kelulusan (`Graduate` vs `Dropout`) serta mengkalkulasi probabilitas risiko dropout secara akurat bagi pemantauan mahasiswa aktif.
3. **Pengembangan Business Dashboard Interaktif**: Membangun dashboard pemantauan performa dan retensi mahasiswa yang dilengkapi visualisasi KPI, grafik perbandingan akademik, dan faktor finansial.
4. **Pengembangan Prototipe Web Machine Learning (Streamlit)**: Membangun aplikasi web interaktif yang siap pakai (*ready-to-use prototype*) dengan fitur simulasi prediksi individual dan prediksi massal (*batch processing CSV*).
5. **Penyusunan Rekomendasi Action Items**: Merumuskan strategi intervensi berbasis data yang siap diimplementasikan oleh pihak manajemen kampus.

---

### Persiapan

**Sumber Data**:
Dataset diperoleh dari rekam jejak akademik mahasiswa Jaya Jaya Institut (berdasarkan *Predict Students' Dropout and Academic Success dataset*, UCI Machine Learning Repository / Dicoding Dataset). Dataset mencakup 4.424 data mahasiswa dengan 37 atribut yang terdiri dari informasi demografis, sosio-ekonomi, data penerimaan, dan pencapaian akademik semester 1 dan semester 2.
- **Tautan Dataset**: [students_performance.csv](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv)

**Setup Environment**:

1. **Informasi Versi Python**:
   - **Versi Python yang Digunakan**: `Python 3.11.9` (Direkomendasikan menggunakan `Python 3.11.x` atau minimal `Python >= 3.10, < 3.12`).
   - *Penting*: Pencantuman dan penggunaan versi Python yang sesuai sangat krusial untuk memastikan kesesuaian environment saat reviewer maupun pengguna lain menjalankan proyek, memastikan kompatibilitas pustaka (*dependency compatibility*), serta membantu menghindari perbedaan perilaku program (*interpreter behavior discrepancies*) akibat perbedaan versi interpreter.
   - Verifikasi versi Python di terminal:
     ```bash
     python --version
     Python 3.11.9
     ```

2. **Membuat dan Mengaktifkan Virtual Environment (Direkomendasikan)**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Instalasi Dependencies**:
```bash
pip install -r requirements.txt
```

Dependensi utama yang digunakan:
- `streamlit>=1.24.0`: Framework prototipe web dan dashboard interaktif.
- `pandas>=2.0.0` & `numpy>=1.25.0`: Manipulasi dan pengolahan data tabular.
- `matplotlib>=3.7.0` & `seaborn>=0.12.0`: Visualisasi data statis dan grafis analisis.
- `scikit-learn>=1.3.0`: Pemodelan machine learning, preprocessing, dan metrik evaluasi.
- `joblib>=1.3.0`: Serialisasi dan pemuatan model machine learning terlatih.

---

## Business Dashboard

Dashboard analitik bisnis telah dibangun untuk membantu manajemen Jaya Jaya Institut memahami data, mengidentifikasi faktor risiko, dan memonitor perkembangan performa mahasiswa secara real-time.

Dashboard ini diintegrasikan langsung ke dalam prototipe aplikasi **Streamlit (`app.py`)** pada menu **"📊 Executive Dashboard"**, serta disiapkan dataset olahan bersih pada `data/students_clean.csv` yang siap dihubungkan ke platform BI seperti Google Looker Studio atau Tableau.

### Komponen Utama Dashboard:
1. **Executive KPI Cards**: Menampilkan metrik vital institusi:
   - Total Mahasiswa: **4.424**
   - Tingkat Dropout: **32.1%** (1.421 mahasiswa)
   - Tingkat Kelulusan: **49.9%** (2.209 mahasiswa)
   - Mahasiswa Aktif (*Enrolled*): **18.0%** (794 mahasiswa)
   - Mahasiswa Memiliki Tunggakan Hutang (*Debtor*): **11.4%**
2. **Filter Interaktif Multi-Dimensi**:
   - Filter Program Studi (17 Program Studi)
   - Filter Status Pembayaran SPP (Lunas vs Menunggak)
   - Filter Penerima Beasiswa (Ya vs Tidak)
3. **Visualisasi Analitik Kunci**:
   - **Distribusi Status Mahasiswa (Donut Chart)**: Proporsi kelulusan, aktif, dan dropout.
   - **Top Program Studi dengan Dropout Tertinggi**: Mengidentifikasi program studi paling rentan (seperti *Biofuel Production Technologies*, *Informatics Engineering*, dan kelas malam).
   - **Analisis SKS Lulus Semester 2 vs Dropout (Boxplot)**: Memperlihatkan perbedaan mencolok di mana mahasiswa dropout memiliki median SKS lulus mendekati 0.
   - **Dampak Keterlambatan SPP terhadap Dropout (Bar Chart)**: Menunjukkan mahasiswa yang menunggak SPP memiliki risiko dropout drastis mencapai **>62%**.

### Tautan Akses & Screenshot Dashboard:
- **Tautan Live Streamlit Dashboard**: [Jaya Jaya Institut - Student Retention System](https://students-performance25.streamlit.app/) *(Dapat diakses setelah proses deploy GitHub ke Streamlit Community Cloud)*
- **Tautan Looker Studio Template**: [Google Looker Studio - Student Performance Dashboard](https://datastudio.google.com/s/kO6PvPzsf60) *(Gunakan file `data/students_clean.csv` sebagai data source)*
- **Screenshot Dashboard Visual**:
  - File ringkasan visual master: `arsyandi_dicoding-dashboard.png`
  - Folder dokumentasi visual lengkap: `arsyandi_dicoding-dashboard/`
    - `01_executive_kpi_overview.png`: Distribusi Status Mahasiswa & Ranking Dropout per Prodi.
    - `02_academic_performance_analysis.png`: SKS Lulus dan Distribusi Nilai Semester 2.
    - `03_financial_demographic_factors.png`: Pengaruh Keterlambatan SPP dan Tunggakan Hutang.
    - `04_model_evaluation_confusion_matrix.png`: Hasil Evaluasi Confusion Matrix Model.

---

## Menjalankan Sistem Machine Learning

Sistem machine learning dikemas dalam prototipe aplikasi berbasis web menggunakan **Streamlit**, yang menyediakan fitur deteksi risiko mahasiswa secara individual maupun secara massal (*batch*).

### 1. Menjalankan Prototipe Secara Lokal

Pastikan Anda berada di direktori utama proyek (`Students_Performance`), kemudian jalankan perintah berikut:

```bash
streamlit run app.py
```

Setelah perintah dijalankan, aplikasi web akan otomatis terbuka pada browser Anda di alamat:
```
Local URL: http://localhost:8501
```

### 2. Cara Menggunakan Prototipe:
- **Fitur 1 - Executive Dashboard**: Pilih menu navigasi pertama untuk memantau metrik agregat dan memfilter data mahasiswa berdasarkan prodi atau status finansial.
- **Fitur 2 - Prediksi Risiko Individual**:
  1. Masukkan data demografis mahasiswa (Usia, Gender, Status Marital, Perantau).
  2. Masukkan data finansial & jalur masuk (Status SPP, Hutang, Beasiswa, Prodi).
  3. Masukkan data akademik semester 1 dan semester 2 (SKS terdaftar, SKS lulus, nilai rata-rata).
  4. Klik tombol **"🔮 Analisis Risiko Mahasiswa"**.
  5. Sistem akan menampilkan status prediksi (`Graduate`, `Enrolled`, atau `Dropout`), indikator kategori risiko (**High Risk**, **Moderate Risk**, **Low Risk**), progress bar probabilitas, serta **Rekomendasi Rencana Aksi Intervensi** yang disesuaikan secara otomatis dengan profil mahasiswa tersebut.
- **Fitur 3 - Prediksi Massal (Batch Prediction CSV)**:
  1. Unduh template CSV sampel melalui tombol yang disediakan di aplikasi.
  2. Unggah file CSV mahasiswa yang ingin dianalisis.
  3. Sistem secara instan memprediksi seluruh mahasiswa, mengelompokkan jumlah mahasiswa berisiko tinggi/sedang/rendah, menampilkan tabel data beranotasi risiko, dan menyediakan tombol unduh hasil prediksi lengkap (`hasil_prediksi_dropout_batch.csv`).
- **Fitur 4 - Panduan Aksi & Insights**: Menampilkan 10 fitur paling berpengaruh (*Feature Importance*) dan Standard Operating Procedure (SOP) penanganan bimbingan konseling.

### 3. Panduan Deployment ke Streamlit Community Cloud:
1. Pastikan seluruh berkas proyek (`app.py`, `requirements.txt`, folder `model/`, folder `data/`) telah di-push ke repository GitHub publik milik Anda:
   ```bash
   git init
   git add .
   git commit -m "Final Submission Data Science Jaya Jaya Institut"
   git branch -M main
   git remote add origin https://github.com/<username>/<nama-repo>.git
   git push -u origin main
   ```
2. Kunjungi [Streamlit Community Cloud](https://share.streamlit.io/) dan login dengan akun GitHub Anda.
3. Klik tombol **"New app"**.
4. Pilih repository, branch `main`, dan set *Main file path* ke `app.py`.
5. Klik **"Deploy!"** dan aplikasi akan aktif secara online dengan tautan publik yang dapat dibagikan kepada reviewer.

---

## Conclusion

Berdasarkan seluruh rangkaian proses data science mulai dari Business Understanding, Exploratory Data Analysis, Modeling, hingga Evaluasi, dapat disimpulkan beberapa temuan esensial:

1. **Laju Dropout Tinggi**: Sebesar **32.1%** mahasiswa Jaya Jaya Institut mengalami dropout, dengan program studi vokasi teknologi (*Biofuel Production*, *Equinculture*, *Informatics Engineering*) dan kelas malam memiliki proporsi dropout paling mengkhawatirkan (>40%).
2. **Faktor Pemicu Utama Dropout**:
   - **Performa Akademik Semester Awal (Indikator Dominan ~23% Importance)**: Mahasiswa yang lulus kurang dari 4 mata kuliah pada semester 1 & 2 memiliki kecenderungan dropout 4x lebih tinggi. Nilai rata-rata semester 2 yang rendah menjadi sinyal kuat mahasiswa kehilangan motivasi belajar.
   - **Beban Finansial (Indikator Kritis)**: Mahasiswa yang menunggak SPP (`Tuition_fees_up_to_date = 0`) memiliki tingkat dropout sebesar **62.3%**, berbanding hanya **23.9%** pada mahasiswa yang SPP-nya lancar. Status hutang/tunggakan (`Debtor = 1`) juga menyumbang tingkat dropout **61.7%**.
   - **Usia Saat Mendaftar & Kelas Malam**: Mahasiswa usia dewasa (>24 tahun) dan mahasiswa kelas malam menghadapi tantangan pembagian waktu antara pekerjaan dan perkuliahan yang memperbesar risiko putus kuliah.
   - **Dampak Positif Beasiswa**: Mahasiswa penerima beasiswa terbukti memiliki retensi sangat tinggi (**76.3% lulus dan hanya 13.6% dropout**).
3. **Kinerja Solusi Machine Learning**: Dengan memfokuskan pendeteksian secara spesifik pada mahasiswa yang telah berstatus *Graduate* dan *Dropout* (klasifikasi biner / *binary classification*), performa model mengalami peningkatan yang sangat signifikan:
   - **Algoritma Terbaik**: Random Forest Classifier (dengan penanganan *class weight balancing*)
   - **Akurasi Model**: **92.98%** (~93.0%)
   - **Macro F1-Score**: **0.9264** (~0.93)
   - **Weighted F1-Score**: **0.9299** (~0.93)
   - **Performa Deteksi Kelas Dropout**: Precision **91%**, Recall **92%**, F1-Score **91%**
   - **Performa Deteksi Kelas Graduate**: Precision **95%**, Recall **94%**, F1-Score **94%**
   Tingkat sensitivitas (*recall* 92%) dan presisi (91%) yang sangat tinggi pada kelas Dropout memastikan hampir seluruh mahasiswa yang berisiko dropout dapat terdeteksi secara akurat tanpa banyak *false alarms*, menjadikannya sangat andal sebagai tulang punggung *Early Warning System* kampus. Mahasiswa berstatus *Enrolled* diposisikan sebagai target populasi aktif yang dimonitor skor risikonya secara berkala pada akhir setiap semester.

---

### Rekomendasi Action Items

Berdasarkan temuan analitik di atas, berikut adalah 5 rekomendasi action items strategis yang dapat segera diimplementasikan oleh Jaya Jaya Institut:

1. **Implementasi Sistem Peringatan Dini Terintegrasi (Early Warning System)**:
   - Mengintegrasikan prototipe model machine learning ke dalam Sistem Informasi Akademik (SIAKAD) kampus.
   - Menjalankan *batch prediction* otomatis di akhir setiap semester untuk menghasilkan daftar mahasiswa berisiko tinggi (*High Risk Flagging*).
   - Mengirimkan notifikasi peringatan dini otomatis kepada Dosen Pembimbing Akademik (DPA) dan bagian Bimbingan Konseling (BK) agar intervensi dapat dilakukan sebelum masa registrasi semester berikutnya berakhir.

2. **Restrukturisasi Kebijakan Finansial & Skema Cicilan SPP Fleksibel**:
   - Menyediakan skema pembayaran SPP bertahap (*installment plan*) bulanan tanpa penalti denda keterlambatan bagi mahasiswa yang mengalami kesulitan ekonomi.
   - Menyediakan program bantuan finansial darurat (*emergency micro-grant*) atau kerja paruh waktu di lingkungan kampus (*student work-study program*) bagi mahasiswa yang terancam cuti/dropout akibat kendala biaya.

3. **Program Remedial & Bimbingan Belajar Sebaya (Peer Tutoring)**:
   - Membuka "Klinik Akademik" dan program remedial wajib bagi mahasiswa yang lulus kurang dari 4 mata kuliah atau memiliki IP semester 1 di bawah 2.0.
   - Memberdayakan mahasiswa berprestasi semester atas sebagai *peer tutors* untuk mendampingi mahasiswa baru dalam mata kuliah dengan tingkat kesulitan tinggi (*killer courses*).

4. **Pendampingan Khusus Mahasiswa Usia Dewasa & Kelas Malam**:
   - Memberikan fleksibilitas akademik bagi mahasiswa kelas malam dan mahasiswa pekerja melalui rekaman materi perkuliahan daring asinkronus dan penyesuaian batas waktu tugas.
   - Membatasi pengambilan beban SKS berlebih di semester awal bagi mahasiswa pekerja agar beban belajar tetap proporsional dan dapat diselesaikan dengan baik.

5. **Pengawasan Retensi dan Mentoring Penerima Beasiswa**:
   - Memantau mahasiswa penerima beasiswa yang mengalami penurunan performa di semester 1 secara proaktif, dan memberikan program mentoring khusus sebelum nilai mereka anjlok di bawah batas minimum pencabutan beasiswa.
