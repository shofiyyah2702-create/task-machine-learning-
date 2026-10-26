
# Jawaban Latihan Find-S dan Candidate-Elimination

## 1. Data EnjoySport

Pada latihan ini, label contoh ke-3 diubah dari No menjadi Yes sesuai instruksi tugas.

| No. | Sky | AirTemp | Humidity | Wind | Water | Forecast | EnjoySport |
|---|---|---|---|---|---|---|---|
| 1 | Sunny | Warm | Normal | Strong | Warm | Same | Yes |
| 2 | Sunny | Warm | High | Strong | Warm | Same | Yes |
| 3 | Rainy | Cold | High | Strong | Warm | Change | Yes |
| 4 | Sunny | Warm | High | Strong | Cool | Change | Yes |

Urutan atribut hipotesis:
`<Sky, AirTemp, Humidity, Wind, Water, Forecast>`

## 2. Find-S

Find-S dimulai dengan hipotesis paling khusus:

h0 = <Ø, Ø, Ø, Ø, Ø, Ø>

### Langkah perhitungan

**Contoh 1 (Yes)**

Semua atribut diisi berdasarkan contoh pertama.

h1 = <Sunny, Warm, Normal, Strong, Warm, Same>

**Contoh 2 (Yes)**

Humidity berubah dari Normal menjadi High. Karena nilainya berbeda, atribut tersebut diganti dengan tanda ?.

h2 = <Sunny, Warm, ?, Strong, Warm, Same>

**Contoh 3 (Yes)**

Sky berubah dari Sunny menjadi Rainy.
AirTemp berubah dari Warm menjadi Cold.
Forecast berubah dari Same menjadi Change.

Ketiga atribut tersebut diganti dengan ?.

h3 = <?, ?, ?, Strong, Warm, ?>

**Contoh 4 (Yes)**

Water berubah dari Warm menjadi Cool, sehingga Water diganti dengan ?.

h4 = <?, ?, ?, Strong, ?, ?>

### Hasil akhir Find-S

Hipotesis akhir:

h = <?, ?, ?, Strong, ?, ?>

Artinya, hipotesis hanya membatasi atribut Wind harus bernilai Strong, sedangkan atribut lainnya boleh memiliki nilai apa saja.

## 3. Candidate-Elimination

Candidate-Elimination mempertahankan dua batas hipotesis:

- S adalah batas hipotesis paling khusus.
- G adalah batas hipotesis paling umum.

Kondisi awal:

S0 = {<Ø, Ø, Ø, Ø, Ø, Ø>}
G0 = {<?, ?, ?, ?, ?, ?>}

### Langkah perhitungan

**Awal**

S = {<Ø, Ø, Ø, Ø, Ø, Ø>}
G = {<?, ?, ?, ?, ?, ?>}

**Contoh 1 (Yes)**

S = {<Sunny, Warm, Normal, Strong, Warm, Same>}
G = {<?, ?, ?, ?, ?, ?>}

S digeneralisasi agar menerima contoh positif pertama.

**Contoh 2 (Yes)**

S = {<Sunny, Warm, ?, Strong, Warm, Same>}
G = {<?, ?, ?, ?, ?, ?>}

Humidity menjadi ? karena nilainya berbeda.

**Contoh 3 (Yes)**

S = {<?, ?, ?, Strong, Warm, ?>}
G = {<?, ?, ?, ?, ?, ?>}

Sky, AirTemp, dan Forecast menjadi ? karena nilainya berbeda dari contoh sebelumnya.

**Contoh 4 (Yes)**

S = {<?, ?, ?, Strong, ?, ?>}
G = {<?, ?, ?, ?, ?, ?>}

Water menjadi ? karena nilainya berbeda.

### Hasil akhir Candidate-Elimination

S = {<?, ?, ?, Strong, ?, ?>}

G = {<?, ?, ?, ?, ?, ?>}

## 4. Version Space

Version space adalah kumpulan hipotesis yang konsisten dengan semua contoh latihan.

Karena keempat contoh berlabel Yes, version space akhir berisi dua hipotesis:

1. <?, ?, ?, Strong, ?, ?>
2. <?, ?, ?, ?, ?, ?>

Hipotesis pertama membatasi Wind = Strong, sedangkan hipotesis kedua tidak membatasi atribut apa pun.

Hal ini terjadi karena Wind selalu bernilai Strong pada semua contoh positif, sedangkan atribut lainnya memiliki nilai yang berbeda.

Perubahan label contoh ke-3 dari No menjadi Yes membuat contoh tersebut harus diterima sebagai positif. Tidak adanya contoh negatif menyebabkan batas G tetap paling umum.

## 5. Kesimpulan

Find-S menghasilkan hipotesis paling khusus yang konsisten dengan contoh positif. Candidate-Elimination mempertahankan batas khusus S dan batas umum G untuk menggambarkan hipotesis yang masih mungkin.

Dengan label contoh ke-3 yang telah diubah menjadi Yes, hasil akhir Find-S adalah <?, ?, ?, Strong, ?, ?> dan version space berisi dua hipotesis yang konsisten dengan data.
