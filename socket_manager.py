import asyncio
import websockets
import json
from datetime import datetime
from socket_data_processor import SocketDataProcessor

class SocketManager:
    def __init__(self, url, headers, data_processor):
        self.url = url
        self.headers = headers
        self.data_processor = data_processor

    async def connect(self):
        """Установление WebSocket соединения и обработка входящих сообщений."""
        while True:
            try:
                async with websockets.connect(self.url, extra_headers=self.headers) as websocket:
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
