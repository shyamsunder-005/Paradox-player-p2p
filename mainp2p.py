import streamlit as st
from app.search import search_torrents
from app.torrent_streamer import stream_and_upload

st.title("🎯 Torrent to Google Drive Uploader")

query = st.text_input("Enter file name to search")
if st.button("Search"):
    results = search_torrents(query)
    for idx, item in enumerate(results):
        st.write(f"{idx + 1}. {item['name']}")
        st.button(f"Download {idx + 1}", key=str(idx), on_click=stream_and_upload, args=(item['magnet'], item['name']))
