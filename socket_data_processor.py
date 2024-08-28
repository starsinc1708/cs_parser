from colorama import Fore, Style


def determine_color(winner_number):
    """Определение цвета на основе выигрышного номера."""
    if winner_number == 1:
        return "синий"
    elif winner_number == 2:
        return "зеленый"
    else:
        return "оранжевый"


def print_colored_round(round_info):
    """Печать деталей раунда с форматированием цвета."""
    color = round_info['color']
    color_map = {
        "синий": Fore.BLUE,
        "зеленый": Fore.GREEN,
        "оранжевый": Fore.YELLOW
    }
    color_code = color_map.get(color, Fore.WHITE)
    multiplier_info = str(round_info.get('multiplier'))
    if round_info['multiplier_winner_number'] == round_info['winner_number']:
        multiplier_info += " ✅"
    else:
        multiplier_info += " ❌"
    print(
        f"\nРаунд ID: {round_info['round_id']}, "
        f"Выигрышный номер: {round_info['winner_number']}, "
        f"Цвет: {color_code}{color}{Style.RESET_ALL}, "
        f"Множитель: {multiplier_info}, "
    )


class SocketDataProcessor:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def process_message(self, data, timestamp):
        """Обрабатывает входящие сообщения и выполняет соответствующие действия в зависимости от канала."""
        if (
            "result" in data and
            data["result"].get("channel") == "csgorun:roulette" and
            data["result"]["data"]["data"].get("type") == "update"
        ):
            self.process_roulette(data, timestamp)

    def process_roulette(self, data, timestamp):
        """Обрабатывает данные канала csgorun:roulette."""
        round_info = data['result']['data']['data']['round']
        winner_number = round_info['winnerNumber']
        multiplier = round_info.get('multiplier')
        if multiplier is None:
            multiplier = 0
        multiplier_winner_number = round_info.get('multiplierNumber')
        random_number = round_info.get('randomNumber')

        if winner_number is not None:
            color = determine_color(winner_number)
            new_data = {
                "round_id": round_info['id'],
                "winner_number": winner_number,
                "color": color,
                "multiplier": multiplier,
                "multiplier_winner_number": multiplier_winner_number,
                "random_number": random_number,
                "timestamp": timestamp
            }
            if new_data["round_id"] not in self.data_manager.df["round_id"].values:
                self.data_manager.append_data(new_data)
                print_colored_round(new_data)
                self.print_color_counts()

    def process_medkit(self, data, timestamp):
        """Обработка данных для канала csgorun:medkit."""
        # Логика обработки данных для medkit
        pass  # Заглушка для обработки medkit

    def print_color_counts(self):
        """Печать количества выигрышей по цветам за последние 100 раундов и за всё время."""
        counts = self.data_manager.count_colors(100)
        msg = "Количество выигрышей за последние 100 игр:"
        for color, count in counts.items():
            msg += f"| {color}: {count} "
        print(msg)

        counts = self.data_manager.count_colors(0)
        msg = "Количество выигрышей за все время:"
        for color, count in counts.items():
            msg += f"| {color}: {count} "
        print(msg)
