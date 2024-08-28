import asyncio
from datetime import datetime

from socket_manager import SocketManager
from file_manager import FileManager
from socket_data_processor import SocketDataProcessor


def main():
    data_manager = FileManager()
    data_processor = SocketDataProcessor(data_manager)
    socket_manager = SocketManager(data_processor)

    asyncio.run(socket_manager.connect())


if __name__ == "__main__":
    main()
