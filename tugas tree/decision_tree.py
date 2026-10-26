
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier, plot_tree, _tree
from sklearn.metrics import accuracy_score


# ==========================================
# 1. MEMUAT DATA
# ==========================================

data = load_breast_cancer()

X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

print("=" * 50)
print("1. DATASET YANG DIGUNAKAN")
print("=" * 50)

print("Jumlah seluruh data:", X.shape[0])
print("Jumlah fitur:", X.shape[1])
print("Kelas data:", data.target_names)


# ==========================================
# 2. MEMBAGI DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\n" + "=" * 50)
print("2. PEMBAGIAN DATA")
print("=" * 50)

print("Data untuk training:", len(X_train))
print("Data untuk testing :", len(X_test))


# ==========================================
# 3. FUNGSI UNTUK MENGHITUNG HASIL MODEL
# ==========================================

def hitung_hasil(nama_model, model):
    prediksi_train = model.predict(X_train)
    prediksi_test = model.predict(X_test)

    return {
        "Nama Model": nama_model,
        "Jumlah Node": model.tree_.node_count,
        "Akurasi Training (%)": round(
            accuracy_score(y_train, prediksi_train) * 100, 2
        ),
        "Akurasi Testing (%)": round(
            accuracy_score(y_test, prediksi_test) * 100, 2
        )
    }


hasil_model = []


# ==========================================
# 4. MODEL TANPA PRUNING
# ==========================================

model_awal = DecisionTreeClassifier(random_state=42)
model_awal.fit(X_train, y_train)

hasil_model.append(
    hitung_hasil("Tanpa pruning", model_awal)
)


# ==========================================
# 5. PRUNING DENGAN max_depth
# ==========================================

model_depth = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

model_depth.fit(X_train, y_train)

hasil_model.append(
    hitung_hasil("max_depth = 4", model_depth)
)


# ==========================================
# 6. PRUNING DENGAN min_samples_leaf
# ==========================================

model_leaf = DecisionTreeClassifier(
    min_samples_leaf=5,
    random_state=42
)

model_leaf.fit(X_train, y_train)

hasil_model.append(
    hitung_hasil("min_samples_leaf = 5", model_leaf)
)


# ==========================================
# 7. PRUNING DENGAN ccp_alpha
# ==========================================

pohon_awal = DecisionTreeClassifier(random_state=42)

jalur_pruning = pohon_awal.cost_complexity_pruning_path(
    X_train, y_train
)

daftar_alpha = np.unique(jalur_pruning.ccp_alphas)

# Tidak menggunakan alpha yang membuat pohon hanya
# memiliki satu node akar jika pilihan lainnya tersedia.
if len(daftar_alpha) > 1:
    daftar_alpha = daftar_alpha[:-1]

validasi = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

pencarian_alpha = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid={"ccp_alpha": daftar_alpha},
    scoring="accuracy",
    cv=validasi,
    n_jobs=-1
)

pencarian_alpha.fit(X_train, y_train)

alpha_terpilih = pencarian_alpha.best_params_["ccp_alpha"]

model_ccp = DecisionTreeClassifier(
    ccp_alpha=alpha_terpilih,
    random_state=42
)

model_ccp.fit(X_train, y_train)

hasil_model.append(
    hitung_hasil(
        f"ccp_alpha = {alpha_terpilih:.5g}",
        model_ccp
    )
)


# ==========================================
# 8. MEMBANDINGKAN HASIL SEMUA MODEL
# ==========================================

tabel_hasil = pd.DataFrame(hasil_model)

print("\n" + "=" * 70)
print("3. HASIL PERBANDINGAN MODEL")
print("=" * 70)

print(tabel_hasil.to_string(index=False))

print("\nNilai ccp_alpha yang terpilih:",
      alpha_terpilih)

print(
    "Akurasi rata-rata validasi silang:",
    round(pencarian_alpha.best_score_ * 100, 2),
    "%"
)


# ==========================================
# 9. MENAMPILKAN POHON SETELAH PRUNING
# ==========================================

print("\n" + "=" * 50)
print("4. POHON KEPUTUSAN SETELAH PRUNING")
print("=" * 50)

plt.figure(figsize=(18, 9))

plot_tree(
    model_ccp,
    feature_names=data.feature_names,
    class_names=data.target_names,
    filled=True,
    rounded=True,
    impurity=False,
    fontsize=8
)

plt.title("Pohon Keputusan Setelah Pruning")
plt.tight_layout()

plt.savefig("pohon_keputusan_pruning.png", dpi=200)
plt.show()


# ==========================================
# 10. MENAMPILKAN TIGA ATURAN IF-THEN
# ==========================================

print("\n" + "=" * 50)
print("5. ATURAN KEPUTUSAN IF-THEN")
print("=" * 50)

pohon = model_ccp.tree_
nama_fitur = data.feature_names
daftar_aturan = []


def cari_aturan(node, kondisi):
    if pohon.feature[node] != _tree.TREE_UNDEFINED:
        fitur = nama_fitur[pohon.feature[node]]
        batas = pohon.threshold[node]

        # Cabang kiri
        cari_aturan(
            pohon.children_left[node],
            kondisi + [f"{fitur} <= {batas:.3f}"]
        )

        # Cabang kanan
        cari_aturan(
            pohon.children_right[node],
            kondisi + [f"{fitur} > {batas:.3f}"]
        )

    else:
        indeks_kelas = int(np.argmax(pohon.value[node][0]))
        nama_kelas = data.target_names[indeks_kelas]

        daftar_aturan.append((kondisi, nama_kelas))


cari_aturan(0, [])

for nomor, (kondisi, kelas) in enumerate(
    daftar_aturan[:3], start=1
):
    syarat = " DAN ".join(kondisi)

    print(f"\nAturan {nomor}:")
    print(f"JIKA {syarat}")
    print(f"MAKA hasil prediksi adalah {kelas}")


# ==========================================
# 11. KESIMPULAN
# ==========================================

print("\n" + "=" * 50)
print("6. KESIMPULAN")
print("=" * 50)

model_terbaik = tabel_hasil.loc[
    tabel_hasil["Akurasi Testing (%)"].idxmax()
]

print(
    "Model dengan akurasi testing tertinggi adalah",
    model_terbaik["Nama Model"]
)

print(
    "Akurasi testing model tersebut adalah",
    model_terbaik["Akurasi Testing (%)"],
    "%"
)

print("""
Dari percobaan ini, Decision Tree digunakan untuk
mengelompokkan data menjadi kelas malignant dan benign.

Model tanpa pruning dibandingkan dengan model yang
menggunakan max_depth, min_samples_leaf, dan ccp_alpha.
Perbandingannya dapat dilihat dari jumlah node serta
akurasi pada data training dan testing.

Pruning digunakan untuk membatasi ukuran pohon agar
tidak terlalu rumit. Namun, pohon yang lebih sederhana
belum tentu menghasilkan akurasi yang lebih tinggi.

Oleh karena itu, hasil setiap model perlu dibandingkan
untuk mengetahui metode mana yang memberikan hasil
paling baik pada data testing.
""")
