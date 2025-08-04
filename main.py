""" Приложение для отображения курсов криптовалют """
from tkinter import *
from tkinter import ttk, messagebox
import datetime
import requests

def get_current_rates() -> None:
    """ Функция получает из открытого API значения курсов популярных криптовалюты в популярные валюты и
    сохраняет данные в глобальной переменной current_exchange_rates, обновляя их раз в 10 секунд"""
    global current_exchange_rates
    cryptocurrencies = ','.join(popular_cryptocurrencies.values())
    currencies = ','.join(popular_currencies.values())
    url = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={cryptocurrencies}&tsyms={currencies}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        current_exchange_rates = response.json()
    except Exception as e:
        messagebox.showerror('Ошибка', f'Произошла ошибка при обновлении крусов криптовалют: {e}\nСейчас используются старые данные, мы попробуем обновить их чуть позже!')
        window.after(ms=30000, func=get_current_rates)
    else:
        window.after(ms=10000, func=get_current_rates)

def get_cryptocurrency_rate() -> None:
    current_cryptocurrency = cryptocurrencies_combobox.get()
    current_currency = currencies_combobox.get()
    if current_cryptocurrency == set_value_cryptocurrencies or current_currency == set_value_currencies:
        messagebox.showerror('Ошибка', 'Пожалуйста, выберите криптовалюту и валюту для получения актуального курса!')
        return

    if not current_exchange_rates:
        messagebox.showerror('Ошибка', 'Сейчас нет актуальных данных по курсам криптовалют\n Пожалуйста, попробуйте сделать запрос чуть позже, мы автоматически обновим данные!')

    abbreviated_name_cryptocurrency = popular_cryptocurrencies.get(current_cryptocurrency)
    abbreviated_name_currency = popular_currencies.get(current_currency)
    text = f'''1 {abbreviated_name_cryptocurrency} ({current_cryptocurrency}) = {current_exchange_rates[abbreviated_name_cryptocurrency][abbreviated_name_currency]:,} {current_currency}
Последнее получение данных: {datetime.datetime.now().strftime('%H:%M %d.%m.%Y')}'''
    lbl_current_cryptocurrency_rate.config(text=text, justify='center')


current_exchange_rates = {}

popular_cryptocurrencies = {
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Tether': 'USDT',
    'Binance Coin': 'BNB',
    'Cardano': 'ADA',
    'Solana': 'SOL',
    'Ripple': 'XRP',
    'Polkado': 'DOT',
    'Litecoin': 'LTC',
    'Chainlink': 'LINK',
    'Dogecoin': 'DOGE',
    'TRON': 'TRX'
}

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

window = Tk()
window.title('Курсы криптовалют')
window.geometry('500x200')

Label(text='Выберите криптовалюту для отображения ее стоимости').pack(pady=10)

frm_combobox = ttk.Frame(master=window)
frm_combobox.pack()

cryptocurrencies_combobox = ttk.Combobox(master=frm_combobox, values=list(popular_cryptocurrencies.keys()))
cryptocurrencies_combobox.pack(side='left', padx=5)
set_value_cryptocurrencies = '-- криптовалюта --'
cryptocurrencies_combobox.set(set_value_cryptocurrencies)

currencies_combobox = ttk.Combobox(master=frm_combobox, values=list(popular_currencies.keys()))
currencies_combobox.pack(side='left', padx=5)
set_value_currencies = '-- валюта --'
currencies_combobox.set(set_value_currencies)

ttk.Button(master=window, text='Посмотреть курс криптовалюты', command=get_cryptocurrency_rate).pack(pady=10)

lbl_current_cryptocurrency_rate = ttk.Label(text='')
lbl_current_cryptocurrency_rate.pack(pady=10)

get_current_rates()

window.mainloop()
