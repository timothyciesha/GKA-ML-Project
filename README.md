# Analisis Segmentasi Pelanggan Berdasarkan Pola Pembelian

## Deskripsi Proyek
Proyek ini bertujuan untuk melakukan segmentasi pelanggan berdasarkan pola pembelian mereka untuk tiga merek utama: `AM`, `SIKA`, dan `Mortar Indonesia`. Dengan menggunakan algoritma K-Means clustering, pelanggan dikelompokkan menjadi 4 cluster berdasarkan fitur seperti total pembelian, kuantitas, dan frekuensi pembelian per merek. Analisis ini memberikan wawasan tentang karakteristik setiap kelompok pelanggan dan rekomendasi strategi pemasaran, khususnya untuk pengembangan merek `Mortar Indonesia`.

Proyek ini dilakukan menggunakan Python dengan library seperti `pandas`, `scikit-learn`, `matplotlib`, dan `seaborn` untuk analisis data dan visualisasi.

## Tujuan
1. Mengelompokkan pelanggan berdasarkan pola pembelian mereka.
2. Memahami karakteristik setiap cluster untuk strategi pemasaran yang lebih tepat.
3. Memberikan rekomendasi khusus untuk meningkatkan pembelian merek `Mortar Indonesia`.

## Dataset
Dataset yang digunakan adalah data penjualan yang mencakup informasi berikut:
- `slsNoSL`: Nomor transaksi.
- `slsDate`: Tanggal transaksi.
- `cstName`: Nama pelanggan.
- `itmName`: Nama item.
- `slsQty`: Kuantitas pembelian.
- `slsPrice`: Harga per unit.
- `slsDisc`: Diskon penjualan.
- `slsSubTotal`: Subtotal sebelum pajak.
- `slsPPN`: Pajak.
- `slsTotal`: Total pembelian.
- `Brand`: Merek produk (AM, SIKA, Mortar Indonesia, dll.).

Data awal memiliki 28.668 baris sebelum pembersihan.

## Langkah-langkah Analisis
1. **Pembersihan Data**:
   - Menghapus baris kosong atau anomali (misalnya baris dengan `cstName = '0'`).
   - Mengisi nilai kosong dengan 0 untuk kolom numerik.
2. **Ekstraksi Fitur**:
   - Mengelompokkan data berdasarkan pelanggan (`cstName`) dan merek (`Brand`).
   - Menghitung total pembelian (`slsTotal`), kuantitas (`slsQty`), dan frekuensi (`slsNoSL`) per merek.
   - Membuat pivot table untuk fitur per merek (misalnya `slsTotal_AM`, `slsTotal_SIKA`).
3. **Normalisasi Data**:
   - Menggunakan `StandardScaler` untuk menormalkan fitur agar memiliki skala yang sama.
4. **Clustering**:
   - Menerapkan K-Means dengan jumlah cluster optimal (4 cluster, ditentukan menggunakan metode Elbow).
   - Menambahkan label cluster ke data pelanggan.
5. **Analisis dan Visualisasi**:
   - Membuat boxplot untuk distribusi total pembelian per merek di setiap cluster.
   - Membuat bar plot untuk rata-rata total pembelian, kuantitas, dan frekuensi per merek.
   - Membuat scatter plot untuk hubungan total pembelian dan frekuensi pembelian.
6. **Rekomendasi**:
   - Memberikan strategi pemasaran berdasarkan karakteristik setiap cluster.

## Hasil
### Karakteristik Cluster
- **Cluster 0 (Pelanggan Kecil, 498 Pelanggan)**:
  - Pembelian kecil untuk semua merek: AM (~10⁶), SIKA (~10⁷), Mortar Indonesia (~10⁴).
  - Frekuensi dan kuantitas rendah.
- **Cluster 1 (Pelanggan Besar, 5 Pelanggan)**:
  - Pembelian sangat besar: AM (~10⁸), SIKA (~10⁹), Mortar Indonesia (~10⁵).
  - Frekuensi dan kuantitas tinggi, tetapi minim untuk Mortar Indonesia.
- **Cluster 2 (Pelanggan Menengah, Fokus Mortar Indonesia, 20 Pelanggan)**:
  - Pembelian menengah: AM (~10⁷), SIKA (~10⁸), Mortar Indonesia (~10⁷).
  - Aktif membeli Mortar Indonesia.
- **Cluster 3 (Pelanggan Menengah-Besar, Dominan SIKA, 105 Pelanggan)**:
  - Pembelian besar untuk SIKA (~10⁸), AM (~10⁷), Mortar Indonesia (~10⁵).
  - Frekuensi tinggi untuk SIKA, tetapi minim untuk Mortar Indonesia.

### Rekomendasi
- **Cluster 0**: Edukasi produk (seminar, demo) dan promosi sederhana (diskon kecil, paket uji coba) untuk Mortar Indonesia.
- **Cluster 1**: Cross-selling Mortar Indonesia melalui bundling dengan AM/SIKA, uji coba gratis, dan insentif pembelian pertama.
- **Cluster 2**: Program loyalitas (diskon volume) dan varian produk untuk meningkatkan pembelian Mortar Indonesia.
- **Cluster 3**: Cross-selling Mortar Indonesia dengan bundling dan insentif pembelian pertama.

## Struktur Kode
- **`Customer Segment.ipynb`**: File utama berisi kode lengkap untuk analisis, clustering, visualisasi, dan pembuatan daftar pelanggan.
- **`customer_list_per_cluster.xlsx`**: File output berisi daftar pelanggan per cluster, termasuk total pembelian, kuantitas, dan frekuensi per merek.
