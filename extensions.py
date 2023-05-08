import json
import requests
from config import keys


class ChangeException(Exception):  # создание частного исключения
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ChangeException(f"перевод одной и той же валюты невозможен ({base} - {base})")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ChangeException(f"не удалось обработать указанную валюту - {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ChangeException(f"не удалось обработать указанную валюту - {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ChangeException(f"не удалось обработать указанное количество - {amount}")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base * amount
