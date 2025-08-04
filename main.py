""" Приложение для отображения курсов криптовалют """
from tkinter import *
from tkinter import ttk, messagebox
import datetime
import requests

def get_current_rates() -> None:
    """Функция получает из открытого API значения курсов популярных криптовалюты в популярные валюты и
    сохраняет данные в глобальной переменной current_exchange_rates"""
    global current_exchange_rates

    for site, url in urls.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            current_exchange_rates[site] = response.json()
        except requests.exceptions.ConnectionError as e:
            messagebox.showerror('Ошибка', f'Произошла ошибка при запросе данных.\n\nПожалуйста, проверьте интернет соединение на устройстве!')
            return
        except requests.exceptions.RequestException as e:
            messagebox.showerror('Ошибка', f'Произошла ошибка при обновлении крусов криптовалют с API сайта "{site}": \n\n{e}\n\n')

def get_cryptocurrency_rate() -> None:
    """Функция после нажатия на кнопку 'Отправить' показывает выбранный курс криптовалюты в выбранной валюте из разных источников,
    обновляя их актуальность раз в 30 секунд при запросе"""
    global last_update_time_rates

    current_cryptocurrency = cryptocurrencies_combobox.get()
    current_currency = currencies_combobox.get()
    if current_cryptocurrency == set_value_cryptocurrencies or current_currency == set_value_currencies:
        messagebox.showerror('Ошибка', 'Пожалуйста, выберите криптовалюту и валюту для получения актуального курса!')
        return

    if datetime.datetime.now() - last_update_time_rates > datetime.timedelta(seconds=30):
        get_current_rates()
        last_update_time_rates = datetime.datetime.now()

    if not current_exchange_rates:
        messagebox.showerror('Ошибка', 'Сейчас нет актуальных данных по курсам криптовалют\n\nПожалуйста, попробуйте сделать запрос чуть позже!')
        return

    text = ''

    abbreviated_name_cryptocurrency = popular_cryptocurrencies.get(current_cryptocurrency)
    abbreviated_name_currency = popular_currencies.get(current_currency)
    for site in current_exchange_rates.keys():
        try:
            if site == 'Cryptocompare':
                current_exchange_rate = current_exchange_rates['Cryptocompare'][abbreviated_name_cryptocurrency][abbreviated_name_currency]
            elif site == 'Coingecko':
                current_exchange_rate = current_exchange_rates['Coingecko'][current_cryptocurrency.lower().replace(' ', '')][abbreviated_name_currency.lower()]
            text += f'Источник "{site}": 1 {abbreviated_name_cryptocurrency} ({current_cryptocurrency}) = {current_exchange_rate:,.2f} {current_currency}\n\n'
        except KeyError:
            continue
    text += f'Последнее обновление данных: {last_update_time_rates.strftime('%H:%M %d.%m.%Y')}'
    lbl_current_cryptocurrency_rate.config(text=text, justify='center')

# Словарь актуальных курсов криптовалют
current_exchange_rates = {}

# Словарь полного названия криптовалюты и его сокращенного названия
popular_cryptocurrencies = {
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Tether': 'USDT',
    'Binance Coin': 'BNB',
    'Cardano': 'ADA',
    'Solana': 'SOL',
    'Ripple': 'XRP',
    'Polkadot': 'DOT',
    'Litecoin': 'LTC',
    'Chainlink': 'LINK',
    'Dogecoin': 'DOGE',
    'TRON': 'TRX'
}

# Словарь популярных валюты и их сокращенное название
popular_currencies = {
    'Российский рубль': 'RUB',
    'Доллар США': 'USD',
    'Евро': 'EUR',
    'Фунт стерлингов': 'GBP',
    'Швейцарский франк': 'CHF',
    'Юань': 'CNY',
    'Японская иена': 'JPY',
    'Австралийский доллар': 'AUD',
    'Канадский доллар': 'CAD',
    'Сингапурский доллар': 'SGD'
}

# Заготовленные API для запроса курса криптовалют с разных сайтов
currencies = ','.join(popular_currencies.values())
url_cryptocompare = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={','.join(popular_cryptocurrencies.values())}&tsyms={currencies}'
url_coingecko = f'https://api.coingecko.com/api/v3/simple/price?ids={','.join(map(lambda w: w.replace(' ', ''), popular_cryptocurrencies.keys()))}&vs_currencies={currencies}'
urls = {'Cryptocompare': url_cryptocompare, 'Coingecko': url_coingecko}

# Создание основного окна приложения
window = Tk()
window.title('Курсы криптовалют')
window.geometry('500x250')

Label(text='Выберите криптовалюту для отображения ее стоимости\n').pack(pady=10)

frm_combobox = ttk.Frame(master=window)
frm_combobox.pack()

# Список для выбора популярной криптовалюты
cryptocurrencies_combobox = ttk.Combobox(master=frm_combobox, values=list(popular_cryptocurrencies.keys()))
cryptocurrencies_combobox.pack(side='left', padx=5)
set_value_cryptocurrencies = '-- криптовалюта --'
cryptocurrencies_combobox.set(set_value_cryptocurrencies)

# Список для выбора популярной валюты
currencies_combobox = ttk.Combobox(master=frm_combobox, values=list(popular_currencies.keys()))
currencies_combobox.pack(side='left', padx=5)
set_value_currencies = '-- валюта --'
currencies_combobox.set(set_value_currencies)

ttk.Button(master=window, text='Посмотреть курс криптовалюты', command=get_cryptocurrency_rate).pack(pady=10)

lbl_current_cryptocurrency_rate = ttk.Label(text='')
lbl_current_cryptocurrency_rate.pack(pady=10)

# Загружаем данные по актуальным курсам и сохраняем последнюю дату и время его обновления
get_current_rates()
last_update_time_rates = datetime.datetime.now()

window.mainloop()
