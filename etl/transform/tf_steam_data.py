import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Fungsi untuk memuat dan menampilkan data dari file JSON
def load_json_data(file_path):
    return pd.read_json(file_path)


def main():
    # Memuat file JSON pertama (steam_data.json)
    steam_data = load_json_data('steam_data.json')
    
    # Memuat file JSON kedua (cleaned_data.json)
    cleaned_data = load_json_data('cleaned_data.json')
    
    # Menampilkan data pertama dan kedua untuk memastikan telah dimuat dengan benar
    print("Steam Data:")
    print(steam_data.head())
    
    print("\nCleaned Data:")
    print(cleaned_data.head())
    
    # Menggabungkan data berdasarkan kolom 'appid'
    merged_data = pd.merge(steam_data, cleaned_data, on="appid", how="inner")  # Merge berdasarkan 'appid'
    
    # Menampilkan data gabungan
    print("\nMerged Data:")
    print(merged_data.head())
    
    # Menangani nilai kosong dan tipe data yang tidak sesuai
    merged_data["discount"] = merged_data["discount"].fillna(0)  # Ganti NaN dengan 0 pada 'discount'
    merged_data["discount"] = merged_data["discount"].replace([np.inf, -np.inf], 0)  # Ganti inf dengan 0
    merged_data["discount"] = merged_data["discount"].astype(int)  # Konversi 'discount' ke integer
    
    # Melakukan transformasi kolom lainnya
    merged_data["price"] = merged_data["price"].astype(float) / 100  # Konversi harga menjadi format yang sesuai
    merged_data["initialprice"] = merged_data["initialprice"].astype(float) / 100  # Konversi harga awal
    merged_data["release_date"] = pd.to_datetime(merged_data["release_date"])  # Konversi tanggal rilis
    
    # Mengonversi kolom bertipe numerik yang memiliki nilai kosong menjadi NaN
    merged_data['positive'] = pd.to_numeric(merged_data['positive'], errors='coerce')
    merged_data['negative'] = pd.to_numeric(merged_data['negative'], errors='coerce')
    merged_data['discount'] = pd.to_numeric(merged_data['discount'], errors='coerce')
    merged_data['score_rank'] = pd.to_numeric(merged_data['score_rank'], errors='coerce')
    
    # Mengganti NaN dengan None agar bisa disimpan sebagai NULL di PostgreSQL
    merged_data = merged_data.where(pd.notnull(merged_data), None)
    
    # Menampilkan hasil transformasi
    print("\nTransformed Merged Data:")
    print(merged_data.head())
    
    # Memisahkan genre dan languages menjadi format relasional
    def process_column_data(merged_data, column_name, new_column_name):
        records = []
        for _, row in merged_data.iterrows():
            appid = row["appid"]
            values = row[column_name].split(", ") if row[column_name] else ["Unknown"]
            for value in values:
                records.append({ "appid": appid, new_column_name: value })
        return pd.DataFrame(records)
    
    # Memproses genre dan languages
    genres_df = process_column_data(merged_data, "genre", "genre")
    languages_df = process_column_data(merged_data, "languages", "language")
    
    # Menghapus kolom yang tidak diperlukan setelah pemrosesan
    merged_data = merged_data.drop(columns=["tags", "genre", "languages"])
    
    # Menampilkan hasil DataFrame
    print("\nGenres DataFrame:")
    print(genres_df.head())
    
    print("\nLanguages DataFrame:")
    print(languages_df.head())
    
    # Membuat koneksi ke PostgreSQL
    engine = create_engine("postgresql://postgres:mtsuzakachan954@localhost:5432/SteamRekdat")
    
    # Memasukkan data ke tabel 'games' di PostgreSQL
    merged_data.to_sql('games', engine, if_exists='append', index=False)
    
    # Memasukkan data ke tabel 'genres' di PostgreSQL
    genres_df.to_sql('genres', engine, if_exists='append', index=False)
    
    # Memasukkan data ke tabel 'languages' di PostgreSQL
    languages_df.to_sql('languages', engine, if_exists='append', index=False)
    
    print("Data berhasil dimuat ke PostgreSQL!")
