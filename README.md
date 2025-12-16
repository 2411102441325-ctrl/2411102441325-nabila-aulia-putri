## Analisis Code Smell pada UKTManager (Sebelum Refactor)

### 1. Pelanggaran SRP (Single Responsibility Principle)
Class `UKTManager`:
- Melakukan pengecekan penghasilan orang tua mahasiswa
- Melakukan pengecekan status beasiswa mahasiswa
- Menentukan kategori UKT (tinggi atau rendah)
- Menampilkan hasil perhitungan UKT ke terminal

Artinya satu class memiliki lebih dari satu alasan untuk berubah, sehingga melanggar SRP.

### 2. Pelanggaran OCP (Open/Closed Principle)
Aturan perhitungan UKT ditulis secara hardcoded di dalam method `calculate_ukt()` menggunakan if/else.
Jika ingin menambah rule baru (batas minimal penghasilan orang tua, validasi jumlah tanggungan keluarga, dll),
maka kita **harus mengubah** isi method `calculate_ukt()`. Hal ini melanggar OCP karena class
tidak tertutup terhadap modifikasi.

### 3. Pelanggaran DIP (Dependency Inversion Principle)
`UKTManager` bergantung langsung pada detail implementasi (logika if/else) di dalamnya.
Tidak ada abstraksi (interface/kontrak) untuk rule validasi. Modul high-level dan low-level
bercampur di satu tempat, sehingga melanggar DIP.
