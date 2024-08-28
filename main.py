import asyncio
from datetime import datetime

from socket_manager import SocketManager
from file_manager import FileManager
from socket_data_processor import SocketDataProcessor


def main():
    url = "wss://ws.cs2run.app/connection/websocket"
    headers = {
        "Pragma": "no-cache",
        "Origin": "https://cs2a.run",
        "Accept-Language": "ru,en;q=0.9",
        "Sec-WebSocket-Key": "tKE+1q+KUhtyCnCRNR0KMA==",
        "User-Agent": "Mozilla/5.0",
        "Upgrade": "websocket",
        "Cache-Control": "no-cache",
        "Connection": "Upgrade",
        "Sec-WebSocket-Version": "13",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"
    }

    data_manager = FileManager()
    data_processor = SocketDataProcessor(data_manager)
    socket_manager = SocketManager(url, headers, data_processor)

    asyncio.run(socket_manager.connect())


if __name__ == "__main__":
    main()
