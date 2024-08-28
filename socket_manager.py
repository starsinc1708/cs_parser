import asyncio
import websockets
import json
from datetime import datetime
from socket_data_processor import SocketDataProcessor

class SocketManager:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    async def connect(self):
        """Установление WebSocket соединения и обработка входящих сообщений."""
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
        while True:
            try:
                async with websockets.connect(url, extra_headers=headers) as websocket:
                    print("Соединение установлено")
                    await self.authenticate(websocket)
                    await self.subscribe_channels(websocket)
                    await self.listen(websocket)
            except Exception as e:
                print(f"Ошибка при подключении: {e}")
                print("Переподключение через 5 секунд...")
                await asyncio.sleep(5)

    async def authenticate(self, websocket):
        """Отправка сообщения аутентификации на сервер."""
        token_message = json.dumps({
            "params": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNzMyNjUzIiwiaWF0IjoxNzI0NDgxNzg2fQ.Wn3eaZxP5FGyx6yitJq_Rpb42uVuxZcIBfUhMPhBVUY",
                "name": "js"
            },
            "id": 1
        })
        await websocket.send(token_message)
        print(f"Отправлено сообщение: {token_message}")

    async def subscribe_channels(self, websocket):
        """Подписка на необходимые каналы."""
        channels = [
            "csgorun:roulette",
            "csgorun:medkit",
            # Добавьте дополнительные каналы по необходимости
        ]

        for i, channel in enumerate(channels, start=2):
            channel_message = json.dumps({
                "method": 1,
                "params": {"channel": channel},
                "id": i
            })
            await websocket.send(channel_message)
            print(f"Отправлено сообщение: {channel_message}")

    async def listen(self, websocket):
        """Прослушивание входящих сообщений и их обработка."""
        buffer = ""

        while True:
            try:
                buffer += await websocket.recv()
                timestamp = datetime.now()

                while buffer:
                    try:
                        data, index = json.JSONDecoder().raw_decode(buffer)
                        buffer = buffer[index:].lstrip()
                        self.data_processor.process_message(data, timestamp)
                    except json.JSONDecodeError:
                        break
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Соединение закрыто: {e}")
                break
            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                continue