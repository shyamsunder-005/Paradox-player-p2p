import asyncio
from app.drive_uploader import upload_to_drive
from webtorrent import WebTorrentClient  # hypothetical module

async def stream_and_upload(magnet, filename):
    client = WebTorrentClient()
    stream = await client.download_to_stream(magnet)
    await upload_to_drive(filename, stream)
