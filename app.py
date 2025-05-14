import streamlit as st
import requests
import pandas as pd
from collections import Counter
from dotenv import load_dotenv
import os  
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

st.set_page_config(page_title="Senam & Kesehatan Ibu Hamil", page_icon="🤰")

st.title("🤰 Aplikasi Informasi Senam & Kesehatan Ibu Hamil")

tab1, tab2 = st.tabs(["📰 Berita Kesehatan Ibu Hamil", "📊 Statistik Kata dari Judul Berita"])

# ---------- TAB 1: Berita ----------
with tab1:
    st.header("📰 Cari Informasi Seputar Kehamilan")
    st.write("Temukan berita dan artikel terpercaya tentang kehamilan, senam ibu hamil, dan kesehatan wanita.")

    query = st.text_input("Masukkan topik (contoh: prenatal yoga, senam hamil, trimester ketiga)")

    if query:
        API_URL
        params = {
            "q": query,
            "language": "id",  
            "pageSize": 10,
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("articles"):
            st.success(f"Ditemukan {len(data['articles'])} artikel:")
            for article in data["articles"]:
                with st.expander(article.get("title", "Judul tidak tersedia")):
                    st.write(f"📅 {article.get('publishedAt', '')[:10]}")
                    st.write(article.get("description", "Deskripsi tidak tersedia."))
                    if article.get("urlToImage"):
                        st.image(article["urlToImage"], width=300)
                    if article.get("url"):
                        st.markdown(f"[Baca Selengkapnya]({article['url']})")
        else:
            st.warning("Tidak ada berita ditemukan atau terjadi kesalahan.")

# ---------- TAB 2: Analisis Judul ----------
with tab2:
    st.header("📊 Analisis Kata Populer dari Judul Artikel")

    query2 = st.text_input("Masukkan topik utama (contoh: pregnancy exercise, prenatal care)", key="query2")

    if query2:
        API_URL
        params = {
            "q": query2,
            "language": "en",
            "pageSize": 50,
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("articles"):
            word_counter = Counter()
            for article in data["articles"]:
                title = article.get("title", "")
                words = title.lower().split()
                for word in words:
                    if len(word) > 3 and word.isalpha():
                        word_counter[word] += 1

            top_words = word_counter.most_common(10)
            df = pd.DataFrame(top_words, columns=["Kata", "Jumlah Muncul"])

            st.bar_chart(df.set_index("Kata"))
            st.dataframe(df)
        else:
            st.warning("Gagal memuat data berita.")
