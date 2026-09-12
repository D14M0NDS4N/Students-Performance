import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Config
st.set_page_config(
    page_title="Jaya Jaya Institut - Student Retention System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 18px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }
    .risk-badge-high {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .risk-badge-medium {
        background-color: #FEF3C7;
        color: #B45309;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .risk-badge-low {
        background-color: #D1FAE5;
        color: #047857;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Load Model and Metadata
@st.cache_resource
def load_model_artifacts():
    model_path = "model/student_dropout_model.joblib"
    meta_path = "model/model_metadata.json"
    if not os.path.exists(model_path) or not os.path.exists(meta_path):
        return None, None
    model = joblib.load(model_path)
    with open(meta_path, "r") as f:
        meta = json.load(f)
    return model, meta

@st.cache_data
def load_student_data():
    if os.path.exists("data/students_clean.csv"):
        return pd.read_csv("data/students_clean.csv")
    elif os.path.exists("data/data.csv"):
        return pd.read_csv("data/data.csv", sep=";")
    return None

model, metadata = load_model_artifacts()
df_students = load_student_data()

COURSE_MAP = {
    33: "Biofuel Production Technologies",
    171: "Animation and Multimedia Design",
    8014: "Social Service (Evening)",
    9003: "Agronomy",
    9070: "Communication Design",
    9085: "Veterinary Nursing",
    9119: "Informatics Engineering",
    9130: "Equinculture",
    9147: "Management",
    9238: "Social Service",
    9254: "Tourism",
    9500: "Nursing",
    9556: "Oral Hygiene",
    9670: "Advertising & Marketing Management",
    9773: "Journalism and Communication",
    9853: "Basic Education",
    9991: "Management (Evening)"
}

INV_COURSE_MAP = {v: k for k, v in COURSE_MAP.items()}

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/education.png", width=70)
    st.markdown("## **Jaya Jaya Institut**")
    st.caption("Sistem Deteksi Dini & Monitoring Dropout Mahasiswa")
    st.markdown("---")
    
    menu = st.radio(
        "Pilih Menu Navigasi:",
        [
            "📊 Executive Dashboard",
            "🎯 Prediksi Risiko Mahasiswa",
            "📁 Batch Prediction (CSV)",
            "💡 Panduan Aksi & Insights"
        ],
        index=0
    )
    
    st.markdown("---")
    if metadata:
        st.markdown(f"**Model:** `{metadata.get('model_name', 'Random Forest')}`")
        st.markdown(f"**Akurasi Model:** `{metadata.get('metrics', {}).get('accuracy', 0.75):.1%}`")
        st.markdown(f"**Macro F1-Score:** `{metadata.get('metrics', {}).get('macro_f1', 0.71):.1%}`")
    st.caption("© 2026 Jaya Jaya Institut Data Science Team")

# -------------------------------------------------------------
# MENU 1: EXECUTIVE DASHBOARD
# -------------------------------------------------------------
if menu == "📊 Executive Dashboard":
    st.markdown('<div class="main-header">Executive Dashboard: Performa & Retensi Mahasiswa</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analisis komprehensif faktor akademik, finansial, dan demografis yang mempengaruhi kelulusan di Jaya Jaya Institut.</div>', unsafe_allow_html=True)
    
    if df_students is None:
        st.error("Data mahasiswa tidak ditemukan di folder data/. Pastikan data/data.csv tersedia.")
    else:
        # Filters
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            selected_course = st.selectbox(
                "Filter Program Studi:",
                ["Semua Program Studi"] + sorted(list(COURSE_MAP.values()))
            )
        with col_f2:
            selected_tuition = st.selectbox(
                "Filter Status SPP:",
                ["Semua Status", "SPP Lunas / Up to date", "SPP Menunggak"]
            )
        with col_f3:
            selected_scholarship = st.selectbox(
                "Filter Beasiswa:",
                ["Semua Status", "Penerima Beasiswa", "Bukan Penerima Beasiswa"]
            )
        
        filtered_df = df_students.copy()
        if "Course_Name" not in filtered_df.columns:
            filtered_df["Course_Name"] = filtered_df["Course"].map(COURSE_MAP).fillna("Other")
            
        if selected_course != "Semua Program Studi":
            filtered_df = filtered_df[filtered_df["Course_Name"] == selected_course]
        if selected_tuition == "SPP Lunas / Up to date":
            filtered_df = filtered_df[filtered_df["Tuition_fees_up_to_date"] == 1]
        elif selected_tuition == "SPP Menunggak":
            filtered_df = filtered_df[filtered_df["Tuition_fees_up_to_date"] == 0]
        if selected_scholarship == "Penerima Beasiswa":
            filtered_df = filtered_df[filtered_df["Scholarship_holder"] == 1]
        elif selected_scholarship == "Bukan Penerima Beasiswa":
            filtered_df = filtered_df[filtered_df["Scholarship_holder"] == 0]
            
        # Top KPI Cards
        total_mhs = len(filtered_df)
        dropout_cnt = (filtered_df["Status"] == "Dropout").sum()
        grad_cnt = (filtered_df["Status"] == "Graduate").sum()
        enrolled_cnt = (filtered_df["Status"] == "Enrolled").sum()
        
        dropout_pct = (dropout_cnt / total_mhs * 100) if total_mhs > 0 else 0
        grad_pct = (grad_cnt / total_mhs * 100) if total_mhs > 0 else 0
        enrolled_pct = (enrolled_cnt / total_mhs * 100) if total_mhs > 0 else 0
        
        debtor_cnt = (filtered_df["Debtor"] == 1).sum()
        debtor_pct = (debtor_cnt / total_mhs * 100) if total_mhs > 0 else 0
        
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            st.metric("Total Mahasiswa", f"{total_mhs:,}")
        with kpi2:
            st.metric("Tingkat Dropout", f"{dropout_pct:.1f}%", delta=f"{dropout_cnt} Mhs", delta_color="inverse")
        with kpi3:
            st.metric("Tingkat Kelulusan", f"{grad_pct:.1f}%", delta=f"{grad_cnt} Mhs")
        with kpi4:
            st.metric("Masih Terdaftar", f"{enrolled_pct:.1f}%", delta=f"{enrolled_cnt} Mhs")
        with kpi5:
            st.metric("Memiliki Tunggakan", f"{debtor_pct:.1f}%", delta=f"{debtor_cnt} Debtor", delta_color="inverse")
            
        st.markdown("---")
        
        # Charts Row 1
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("Distribusi Status Mahasiswa")
            if total_mhs > 0:
                fig1, ax1 = plt.subplots(figsize=(6, 4))
                status_series = filtered_df["Status"].value_counts()
                colors = {"Graduate": "#10B981", "Dropout": "#EF4444", "Enrolled": "#F59E0B"}
                ax1.pie(
                    status_series,
                    labels=[f"{k}: {v} ({v/total_mhs:.1%})" for k, v in status_series.items()],
                    autopct="%1.1f%%",
                    colors=[colors.get(c, "#3B82F6") for c in status_series.index],
                    startangle=140,
                    wedgeprops=dict(width=0.45, edgecolor='w')
                )
                st.pyplot(fig1)
            else:
                st.info("Tidak ada data yang cocok dengan kombinasi filter.")
                
        with col_c2:
            st.subheader("Dropout Rate Berdasarkan Program Studi")
            if total_mhs > 0:
                c_df = df_students.copy()
                if "Course_Name" not in c_df.columns:
                    c_df["Course_Name"] = c_df["Course"].map(COURSE_MAP).fillna("Other")
                course_stats = c_df.groupby("Course_Name")["Status"].apply(
                    lambda s: (s == "Dropout").mean() * 100
                ).sort_values(ascending=True).tail(8)
                
                fig2, ax2 = plt.subplots(figsize=(7, 4.3))
                bars = ax2.barh(course_stats.index, course_stats.values, color="#EF4444", alpha=0.85)
                ax2.set_xlabel("Persentase Dropout (%)")
                ax2.set_xlim(0, max(course_stats.values) + 10)
                for bar in bars:
                    w = bar.get_width()
                    ax2.text(w + 1, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va="center", fontweight="bold", fontsize=9)
                st.pyplot(fig2)
            else:
                st.info("Tidak ada data.")

        # Charts Row 2
        col_c3, col_c4 = st.columns(2)
        with col_c3:
            st.subheader("Performa Akademik: Mata Kuliah Lulus Semester 2")
            if total_mhs > 0:
                fig3, ax3 = plt.subplots(figsize=(7, 4))
                sns.boxplot(
                    data=filtered_df,
                    x="Status",
                    y="Curricular_units_2nd_sem_approved",
                    hue="Status",
                    legend=False,
                    palette={"Graduate": "#10B981", "Dropout": "#EF4444", "Enrolled": "#F59E0B"},
                    order=["Graduate", "Enrolled", "Dropout"],
                    ax=ax3
                )
                ax3.set_ylabel("Mata Kuliah Disetujui (SKS)")
                ax3.set_xlabel("Status Mahasiswa")
                st.pyplot(fig3)
                
        with col_c4:
            st.subheader("Pengaruh Keterlambatan SPP terhadap Dropout")
            if total_mhs > 0:
                tuition_stat = filtered_df.groupby("Tuition_fees_up_to_date")["Status"].apply(
                    lambda s: (s == "Dropout").mean() * 100
                )
                fig4, ax4 = plt.subplots(figsize=(6, 3.8))
                labels = ["SPP Menunggak", "SPP Lunas"]
                vals = [tuition_stat.get(0, 0), tuition_stat.get(1, 0)]
                bars4 = ax4.bar(labels, vals, color=["#DC2626", "#059669"], width=0.5)
                ax4.set_ylabel("Persentase Dropout (%)")
                ax4.set_ylim(0, 100)
                for b in bars4:
                    h = b.get_height()
                    ax4.text(b.get_x() + b.get_width()/2, h + 2, f"{h:.1f}%", ha="center", fontweight="bold")
                st.pyplot(fig4)

        # Strategic Insight Callout
        st.info("""
        📌 **Key Analytical Insights bagi Jaya Jaya Institut:**
        1. **Faktor Finansial Sangat Menentukan**: Mahasiswa yang menunggak pembayaran SPP memiliki risiko dropout hingga **>60%**, dibandingkan hanya ~20% pada mahasiswa dengan SPP lancar.
        2. **Performa Akademik Semester 1 & 2 adalah Early Indicator**: Mahasiswa yang lulus kurang dari 4 mata kuliah pada semester 1 & 2 memiliki kecenderungan dropout 4 kali lipat lebih tinggi.
        3. **Program Studi Berisiko Tinggi**: Biofuel Production, Equinculture, dan Manajemen Kelas Malam memerlukan pendampingan belajar khusus.
        """)

# -------------------------------------------------------------
# MENU 2: PREDIKSI RISIKO MAHASISWA (INDIVIDUAL)
# -------------------------------------------------------------
elif menu == "🎯 Prediksi Risiko Mahasiswa":
    st.markdown('<div class="main-header">Sistem Prediksi Dini Risiko Dropout Mahasiswa</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Masukkan profil mahasiswa untuk mendeteksi probabilitas dropout dan memperoleh rekomendasi intervensi.</div>', unsafe_allow_html=True)
    
    if model is None:
        st.error("Model machine learning belum dilatih atau file model/student_dropout_model.joblib tidak ditemukan.")
    else:
        with st.form("prediction_form"):
            tab1, tab2, tab3 = st.tabs(["👤 Data Demografis", "💳 Latar Belakang Finansial & Masuk", "📚 Performa Akademik (Sem 1 & 2)"])
            
            with tab1:
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    age = st.slider("Usia saat Mendaftar (Tahun):", 17, 70, 20)
                    gender = st.selectbox("Jenis Kelamin:", ["Perempuan", "Laki-laki"])
                    marital = st.selectbox("Status Pernikahan:", ["Single (Lajang)", "Menikah", "Bercerai", "Lainnya"])
                with col_d2:
                    displaced = st.selectbox("Perantau / Displaced (Tinggal Jauh dari Keluarga):", ["Ya", "Tidak"])
                    intl = st.selectbox("Mahasiswa Internasional:", ["Tidak", "Ya"])
                    special_needs = st.selectbox("Kebutuhan Edukasi Khusus:", ["Tidak", "Ya"])
                    
            with tab2:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    course_name = st.selectbox("Program Studi (Course):", list(COURSE_MAP.values()), index=8) # Default Management
                    attendance = st.selectbox("Jadwal Kuliah:", ["Kelas Pagi/Siang (Daytime)", "Kelas Malam (Evening)"])
                    admission_grade = st.slider("Nilai Masuk / Seleksi (Skala 0 - 200):", 50.0, 200.0, 125.0, step=0.5)
                    prev_grade = st.slider("Nilai Kualifikasi Sebelumnya (Skala 0 - 200):", 50.0, 200.0, 125.0, step=0.5)
                with col_f2:
                    tuition_paid = st.selectbox("Status Pembayaran SPP (Tuition Fees):", ["Lunas (Up to date)", "Menunggak / Terlambat"])
                    has_debt = st.selectbox("Memiliki Tunggakan Hutang (Debtor):", ["Tidak", "Ya"])
                    scholarship = st.selectbox("Penerima Beasiswa (Scholarship Holder):", ["Tidak", "Ya"])
                    app_order = st.slider("Urutan Pilihan Jurusan:", 0, 9, 1)

            with tab3:
                st.markdown("##### Performa Akademik Semester 1")
                col_s1_1, col_s1_2, col_s1_3 = st.columns(3)
                with col_s1_1:
                    sem1_enrolled = st.number_input("SKS Diambil (Sem 1):", min_value=0, max_value=25, value=6)
                with col_s1_2:
                    sem1_approved = st.number_input("SKS Lulus (Sem 1):", min_value=0, max_value=25, value=5)
                with col_s1_3:
                    sem1_grade = st.slider("Nilai Rata-rata Sem 1 (0 - 20):", 0.0, 20.0, 12.5, step=0.1)
                
                sem1_evals = st.number_input("Jumlah Evaluasi/Ujian Sem 1:", min_value=0, max_value=30, value=sem1_enrolled + 2)
                sem1_credited = st.number_input("SKS Ditransfer/Kredit Sem 1:", min_value=0, max_value=20, value=0)
                sem1_without_evals = st.number_input("SKS Tanpa Evaluasi Sem 1:", min_value=0, max_value=10, value=0)
                
                st.markdown("##### Performa Akademik Semester 2")
                col_s2_1, col_s2_2, col_s2_3 = st.columns(3)
                with col_s2_1:
                    sem2_enrolled = st.number_input("SKS Diambil (Sem 2):", min_value=0, max_value=25, value=6)
                with col_s2_2:
                    sem2_approved = st.number_input("SKS Lulus (Sem 2):", min_value=0, max_value=25, value=5)
                with col_s2_3:
                    sem2_grade = st.slider("Nilai Rata-rata Sem 2 (0 - 20):", 0.0, 20.0, 12.5, step=0.1)
                
                sem2_evals = st.number_input("Jumlah Evaluasi/Ujian Sem 2:", min_value=0, max_value=30, value=sem2_enrolled + 2)
                sem2_credited = st.number_input("SKS Ditransfer/Kredit Sem 2:", min_value=0, max_value=20, value=0)
                sem2_without_evals = st.number_input("SKS Tanpa Evaluasi Sem 2:", min_value=0, max_value=10, value=0)
                
            submitted = st.form_submit_button("🔮 Analisis Risiko Mahasiswa", use_container_width=True)

        if submitted:
            # Map input to model feature vector
            course_id = INV_COURSE_MAP.get(course_name, 9147)
            marital_id = 1 if "Single" in marital else (2 if "Menikah" in marital else 4)
            gender_id = 1 if gender == "Laki-laki" else 0
            displaced_id = 1 if displaced == "Ya" else 0
            intl_id = 1 if intl == "Ya" else 0
            special_id = 1 if special_needs == "Ya" else 0
            attendance_id = 1 if "Pagi" in attendance else 0
            tuition_id = 1 if "Lunas" in tuition_paid else 0
            debt_id = 1 if has_debt == "Ya" else 0
            scholar_id = 1 if scholarship == "Ya" else 0
            
            # Construct row with all 36 features matching training dataset
            features = {
                'Marital_status': marital_id,
                'Application_mode': 1,
                'Application_order': app_order,
                'Course': course_id,
                'Daytime_evening_attendance': attendance_id,
                'Previous_qualification': 1,
                'Previous_qualification_grade': prev_grade,
                'Nacionality': 1,
                'Mothers_qualification': 19,
                'Fathers_qualification': 19,
                'Mothers_occupation': 5,
                'Fathers_occupation': 5,
                'Admission_grade': admission_grade,
                'Displaced': displaced_id,
                'Educational_special_needs': special_id,
                'Debtor': debt_id,
                'Tuition_fees_up_to_date': tuition_id,
                'Gender': gender_id,
                'Scholarship_holder': scholar_id,
                'Age_at_enrollment': age,
                'International': intl_id,
                'Curricular_units_1st_sem_credited': sem1_credited,
                'Curricular_units_1st_sem_enrolled': sem1_enrolled,
                'Curricular_units_1st_sem_evaluations': sem1_evals,
                'Curricular_units_1st_sem_approved': sem1_approved,
                'Curricular_units_1st_sem_grade': sem1_grade,
                'Curricular_units_1st_sem_without_evaluations': sem1_without_evals,
                'Curricular_units_2nd_sem_credited': sem2_credited,
                'Curricular_units_2nd_sem_enrolled': sem2_enrolled,
                'Curricular_units_2nd_sem_evaluations': sem2_evals,
                'Curricular_units_2nd_sem_approved': sem2_approved,
                'Curricular_units_2nd_sem_grade': sem2_grade,
                'Curricular_units_2nd_sem_without_evaluations': sem2_without_evals,
                'Unemployment_rate': 11.5,
                'Inflation_rate': 1.4,
                'GDP': 0.5
            }
            
            input_df = pd.DataFrame([features])
            pred_idx = model.predict(input_df)[0]
            probs = model.predict_proba(input_df)[0]
            
            classes_list = ["Dropout", "Graduate"]
            pred_label = classes_list[pred_idx]
            dropout_prob = probs[0]  # Index 0 is Dropout in binary classification
            graduate_prob = probs[1] # Index 1 is Graduate
            enrolled_prob = 0.0
            
            st.markdown("### 📋 Hasil Analisis Risiko Mahasiswa")
            
            res_col1, res_col2 = st.columns([1, 1.2])
            with res_col1:
                st.markdown(f"#### Prediksi Status Akhir: **{pred_label.upper()}**")
                
                # Risk Category Definition
                if dropout_prob >= 0.50 or pred_label == "Dropout":
                    risk_status = "TINGGI (High Risk)"
                    badge_class = "risk-badge-high"
                    st.markdown(f'Kategori Risiko: <span class="{badge_class}">⚠️ {risk_status}</span>', unsafe_allow_html=True)
                    st.error(f"Mahasiswa ini memiliki probabilitas dropout sebesar **{dropout_prob:.1%}**. Memerlukan tindakan intervensi segera!")
                elif dropout_prob >= 0.30:
                    risk_status = "SEDANG (Moderate Risk)"
                    badge_class = "risk-badge-medium"
                    st.markdown(f'Kategori Risiko: <span class="{badge_class}">⚡ {risk_status}</span>', unsafe_allow_html=True)
                    st.warning(f"Mahasiswa ini memiliki probabilitas dropout sebesar **{dropout_prob:.1%}**. Perlu pemantauan akademik berkala.")
                else:
                    risk_status = "RENDAH (Low Risk / On Track)"
                    badge_class = "risk-badge-low"
                    st.markdown(f'Kategori Risiko: <span class="{badge_class}">✅ {risk_status}</span>', unsafe_allow_html=True)
                    st.success(f"Mahasiswa ini aman dengan probabilitas kelulusan **{graduate_prob:.1%}** (Risiko dropout rendah: {dropout_prob:.1%}).")
                
                st.write("")
                st.markdown("**Distribusi Probabilitas Model:**")
                st.progress(float(dropout_prob), text=f"Probabilitas Dropout: {dropout_prob:.1%}")
                st.progress(float(enrolled_prob), text=f"Probabilitas Bertahan (Enrolled): {enrolled_prob:.1%}")
                st.progress(float(graduate_prob), text=f"Probabilitas Lulus (Graduate): {graduate_prob:.1%}")
                
            with res_col2:
                st.markdown("#### 🎯 Rekomendasi Intervensi Akademik (Action Plan):")
                recs = []
                if tuition_id == 0 or debt_id == 1:
                    recs.append("💳 **Restrukturisasi Keuangan**: Hubungi bagian keuangan untuk program cicilan SPP fleksibel dan evaluasi permohonan beasiswa darurat.")
                if sem1_approved < sem1_enrolled or sem2_approved < sem2_enrolled:
                    recs.append("📖 **Program Remedial & Tutoring**: Daftarkan mahasiswa ke bimbingan belajar sebaya (*peer tutoring*) pada mata kuliah yang belum tuntas.")
                if age >= 25 or attendance_id == 0:
                    recs.append("⏰ **Dukungan Mahasiswa Bekerja/Dewasa**: Berikan konseling manajemen waktu dan fleksibilitas akses materi asinkronus.")
                if sem2_grade < 11.0:
                    recs.append("👩‍🏫 **Mentoring Dosen Pembimbing Akademik**: Jadwalkan sesi konseling akademik 1-on-1 minimal 2 minggu sekali.")
                
                if not recs:
                    recs.append("🌟 **Pertahankan Prestasi**: Mahasiswa memiliki rekam jejak yang baik. Berikan apresiasi dan dorongan untuk bergabung dalam program magang atau riset.")
                    
                for rec in recs:
                    st.markdown(f"- {rec}")

# -------------------------------------------------------------
# MENU 3: BATCH PREDICTION (CSV)
# -------------------------------------------------------------
elif menu == "📁 Batch Prediction (CSV)":
    st.markdown('<div class="main-header">Prediksi Massal Risiko Dropout (Batch Processing)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Unggah file CSV kumpulan data mahasiswa untuk mengidentifikasi seluruh mahasiswa yang berisiko sekaligus.</div>', unsafe_allow_html=True)
    
    # Download sample template
    if df_students is not None:
        sample_df = df_students.drop(columns=["Status", "Course_Name", "Gender_Label", "Scholarship_Label", "Tuition_Fees_Label", "Debtor_Label", "Daytime_Evening_Label"], errors="ignore").head(20)
        csv_sample = sample_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Contoh Template CSV (20 Baris)",
            data=csv_sample,
            file_name="sample_students_data.csv",
            mime="text/csv"
        )
    
    uploaded_file = st.file_uploader("Pilih file CSV data mahasiswa:", type=["csv"])
    if uploaded_file is not None:
        try:
            batch_data = pd.read_csv(uploaded_file, sep=";" if ";" in uploaded_file.readline().decode('utf-8') else ",")
            uploaded_file.seek(0)
            batch_data = pd.read_csv(uploaded_file, sep=";" if ";" in uploaded_file.readline().decode('utf-8') else ",")
            
            st.success(f"File berhasil dimuat! Terdeteksi **{len(batch_data)}** baris data mahasiswa.")
            
            # Predict
            feature_cols = metadata.get("feature_names", list(batch_data.columns))
            # Filter to required features
            X_batch = batch_data[[col for col in feature_cols if col in batch_data.columns]]
            
            if len(X_batch.columns) == len(feature_cols):
                preds = model.predict(X_batch)
                probs = model.predict_proba(X_batch)
                
                classes_list = metadata.get("classes", ["Dropout", "Enrolled", "Graduate"])
                batch_result = batch_data.copy()
                batch_result["Predicted_Status"] = [classes_list[p] for p in preds]
                batch_result["Dropout_Probability"] = np.round(probs[:, 0] * 100, 1)
                batch_result["Graduate_Probability"] = np.round(probs[:, 2] * 100, 1)
                
                # Risk level categorization
                def assign_risk(row):
                    if row["Dropout_Probability"] >= 50 or row["Predicted_Status"] == "Dropout":
                        return "High Risk"
                    elif row["Dropout_Probability"] >= 30:
                        return "Medium Risk"
                    return "Low Risk"
                    
                batch_result["Risk_Level"] = batch_result.apply(assign_risk, axis=1)
                
                # Summary metrics
                high_cnt = (batch_result["Risk_Level"] == "High Risk").sum()
                med_cnt = (batch_result["Risk_Level"] == "Medium Risk").sum()
                low_cnt = (batch_result["Risk_Level"] == "Low Risk").sum()
                
                b1, b2, b3 = st.columns(3)
                with b1:
                    st.metric("Mahasiswa Berisiko Tinggi (High Risk)", f"{high_cnt} ({high_cnt/len(batch_result):.1%})")
                with b2:
                    st.metric("Mahasiswa Berisiko Sedang (Medium Risk)", f"{med_cnt} ({med_cnt/len(batch_result):.1%})")
                with b3:
                    st.metric("Mahasiswa Jalur Aman (Low Risk)", f"{low_cnt} ({low_cnt/len(batch_result):.1%})")
                    
                st.markdown("#### Tabel Hasil Identifikasi Risiko Mahasiswa")
                display_cols = ["Course", "Age_at_enrollment", "Tuition_fees_up_to_date", "Debtor", "Predicted_Status", "Dropout_Probability", "Risk_Level"]
                avail_disp = [c for c in display_cols if c in batch_result.columns]
                
                st.dataframe(batch_result[avail_disp].head(50), use_container_width=True)
                
                # Download analyzed result
                csv_out = batch_result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Unduh Hasil Prediksi Lengkap (CSV)",
                    data=csv_out,
                    file_name="hasil_prediksi_dropout_batch.csv",
                    mime="text/csv"
                )
            else:
                st.error("Kolom pada file CSV tidak lengkap. Harap gunakan template yang sesuai dengan data latih.")
        except Exception as e:
            st.error(f"Gagal memproses file CSV: {str(e)}")

# -------------------------------------------------------------
# MENU 4: PANDUAN AKSI & INSIGHTS
# -------------------------------------------------------------
elif menu == "💡 Panduan Aksi & Insights":
    st.markdown('<div class="main-header">Rekomendasi Action Items & Penjelasan Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Langkah strategis institusi pendidikan untuk meminimalisir tingkat dropout mahasiswa secara berkelanjutan.</div>', unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns([1.1, 0.9])
    
    with col_i1:
        st.markdown("### 🏆 5 Rekomendasi Action Items Strategis:")
        
        st.markdown("""
        #### 1. Implementasi Sistem Peringatan Dini Terintegrasi (Early Warning System)
        - Menghubungkan model prediktif machine learning ini dengan Sistem Informasi Akademik (SIAKAD) kampus.
        - Notifikasi otomatis dikirimkan ke Dosen Pembimbing Akademik (DPA) segera setelah rekap nilai semester 1 & 2 keluar untuk mahasiswa dengan probabilitas dropout ≥ 50%.
        
        #### 2. Restrukturisasi Bantuan Finansial & Fleksibilitas SPP
        - Data membuktikan bahwa **keterlambatan SPP berkorelasi sangat tinggi dengan dropout**.
        - Buat skema *installment plan* (cicilan bulanan) tanpa denda, program kerja paruh waktu di kampus (*student work-study*), dan dana darurat beasiswa transisi.
        
        #### 3. Intervensi Remedial & Bimbingan Belajar Sebaya (Peer Tutoring)
        - Mengingat jumlah SKS lulus semester 1 & 2 merupakan prediktor nomor 1, sediakan kelas klinik belajar (*academic clinic*) wajib bagi mahasiswa yang tidak lulus ≥ 2 mata kuliah di semester pertama.
        
        #### 4. Pendampingan Khusus Mahasiswa Usia Dewasa & Kelas Malam
        - Mahasiswa usia di atas 24 tahun dan kelas malam memiliki tingkat dropout lebih tinggi karena beban kerja/keluarga.
        - Sediakan konseling fleksibel, rekaman perkuliahan daring asinkronus, dan bimbingan karir yang selaras dengan industri.
        
        #### 5. Pengawasan Retensi Penerima Beasiswa
        - Mahasiswa penerima beasiswa memiliki dropout rate jauh lebih rendah, namun yang mengalami penurunan IPK berisiko kehilangan beasiswa lalu dropout seketika.
        - Bentuk program *mentorship* khusus penerima beasiswa yang mengalami penurunan performa sebelum beasiswa dicabut.
        """)
        
    with col_i2:
        st.markdown("### 📊 Faktor Paling Berpengaruh (Feature Importance):")
        if metadata and "top_features" in metadata:
            feat_df = pd.DataFrame(metadata["top_features"][:10], columns=["Fitur", "Importance"])
            feat_df["Importance (%)"] = feat_df["Importance"] * 100
            
            fig_f, ax_f = plt.subplots(figsize=(7, 5.5))
            sns.barplot(data=feat_df, y="Fitur", x="Importance (%)", palette="Blues_r", ax=ax_f)
            ax_f.set_title("Top 10 Feature Importance (Random Forest)", fontweight="bold")
            for p in ax_f.patches:
                w = p.get_width()
                ax_f.text(w + 0.3, p.get_y() + p.get_height()/2, f"{w:.1f}%", va="center", fontsize=8)
            st.pyplot(fig_f)
        
        st.markdown("### 📑 Prosedur Operasional Standar (SOP) Penanganan:")
        st.markdown("""
        | Tahap | Penanggung Jawab | Tindakan |
        | :--- | :--- | :--- |
        | **Deteksi Dini** | Tim Data & Sistem | Running model prediksi tiap akhir semester |
        | **Verifikasi** | Dosen Wali (DPA) | Review histori nilai & catatan kehadiran |
        | **Pendekatan** | Bagian Konseling | Wawancara empatik kendala akademik / finansial |
        | **Solusi** | Prodi & Keuangan | Dispensasi SPP, jadwal ulang SKS, remedial |
        """)
