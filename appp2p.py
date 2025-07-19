import streamlit as st
from Py1337x import Py1337x
import libtorrent as lt
import time
import os
import shutil
import zipfile
import io

DOWNLOAD_PATH = "./downloads"

# ----- Torrent Search -----
def search_torrents(query):
    client = Py1337x()
    results = client.search(query, sort_by='time/desc')
    return [{
        'title': r['title'],
        'size': r['Total size'],
        'category': r['Category'],
        'uploaded': r['Date uploaded'],
        'seeders': r['Seeders'],
        'magnet': r['MagnetLink']
    } for r in results]

# ----- Torrent Download -----
def download_torrent(magnet_link):
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    ses = lt.session()
    params = {
        'save_path': DOWNLOAD_PATH,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
    }
    handle = lt.add_magnet_uri(ses, magnet_link, params)

    with st.spinner("Fetching metadata..."):
        while not handle.has_metadata():
            time.sleep(1)

    st.success("Metadata fetched. Downloading started...")

    progress_bar = st.progress(0)
    while handle.status().state != lt.torrent_status.seeding:
        s = handle.status()
        percent = int(s.progress * 100)
        progress_bar.progress(percent)
        st.write(f"{percent}% - Down: {s.download_rate / 1000:.1f} kB/s | Peers: {s.num_peers}")
        time.sleep(2)

    st.success("Download complete!")

# ----- Folder Delete -----
def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        st.success(f"🗑Deleted folder: {folder_path}")
    else:
        st.warning("Folder not found.")

# ----- List Files -----
def list_downloaded_files():
    filepaths = []
    for root, _, files in os.walk(DOWNLOAD_PATH):
        for file in files:
            filepaths.append(os.path.join(root, file))
    return filepaths

# ----- Zip Files -----
def zip_downloaded_files(filepaths):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in filepaths:
            arcname = os.path.relpath(file_path, DOWNLOAD_PATH)
            zipf.write(file_path, arcname=arcname)
    zip_buffer.seek(0)
    return zip_buffer

# =========================
# ===== Streamlit UI =====
# =========================
st.set_page_config(page_title="Torrent Downloader", page_icon="📥")
st.title("📥 P2P Torrent Downloader")
st.caption("Search torrents from 1337x and download using libtorrent. Built with Streamlit.")

# Search section
st.header("🔍 Search Torrents")
query = st.text_input("Enter search keyword:")
if st.button("Search") and query:
    with st.spinner("Searching..."):
        results = search_torrents(query)

    if results:
        for r in results:
            st.markdown(f"### {r['title']}")
            st.text(f" {r['category']} |  {r['size']} |  {r['uploaded']} |  {r['seeders']}")
            if st.button(f"Download", key=r['magnet']):
                download_torrent(r['magnet'])
            st.divider()
    else:
        st.info("No results found.")

# File viewer and ZIP download
st.header(" Downloaded Files")
downloaded_files = list_downloaded_files()

if downloaded_files:
    for f in downloaded_files:
        st.text(f)

    zip_data = zip_downloaded_files(downloaded_files)
    st.download_button(
        label=" Download All as ZIP",
        data=zip_data,
        file_name="torrent_downloads.zip",
        mime="application/zip"
    )
else:
    st.info("No files downloaded yet.")

# Folder deletion
st.header(" Delete Folder")
folder_to_delete = st.text_input("Enter folder path to delete (e.g., ./downloads/somefolder):")
if st.button("Delete Folder"):
    delete_folder(folder_to_delete)
