"""Приложение для отображения популярных курсов криптовалют в популярные валюты с использованием API сайта CoinGecko"""
from tkinter import *
from tkinter import ttk, messagebox
import datetime
import requests

def get_current_rates_from_api() -> None:
    """Функция для получения курсов криптовалют с готовым запросом API с сайта CoinGecko и сохранением данных в
    глобальную переменную"""
    global current_exchange_rates

    # Формируем готовую API ссылку для запроса с нужными криптовалютами и валютами
    url_api = f'https://api.coingecko.com/api/v3/simple/price?ids={cryptocurrencies}&vs_currencies={currencies}'

    # Запрашиваем данные, проверяем статус ответа и сохраняем сериализованные данные в словарь актуальных курсов
    try:
        response = requests.get(url_api)
        response.raise_for_status()
        current_exchange_rates = response.json()
    # Обрабатываем исключение, если отсутствует подключение к интернету
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Ошибка', f'Произошла ошибка при запросе данных\n\n'
                                       f'Пожалуйста, проверьте интернет соединение на устройстве и повторите попытку!')
        return
    # Обрабатываем исключение, если произошла любая другая ошибка при запросе данных
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Ошибка', f'Произошла ошибка при обновлении крусов криптовалют с API сайта: \n\n{e}\n\n')

def show_cryptocurrency_rate() -> None:
    """Функция для отображения результата курса выбранной криптовалюты в выбранной валюте после нажатия на кнопку
    'Отправить', обновляя их актуальность 1 раз в 20 секунд при новом запросе"""
    global last_update_time_rates

    # Получаем значения выбранной пользователем нужной криптовалюты и валюты
    current_cryptocurrency = cryptocurrencies_combobox.get()
    current_currency = currencies_combobox.get()

    # Проверяем, что пользователь выбрал из списка криптовалюту и валюту
    if current_cryptocurrency == set_value_cryptocurrencies or current_currency == set_value_currencies:
        messagebox.showerror('Ошибка', 'Пожалуйста, выберите криптовалюту и валюту для получения актуального курса!')
        return

    # Если с момента последнего запроса прошло более 20 секунд, то обновляет время запроса и получаем новые данные по курсам
    if datetime.datetime.now() - last_update_time_rates > datetime.timedelta(seconds=20):
        get_current_rates_from_api()
        last_update_time_rates = datetime.datetime.now()

    # Проверяем, что данные были получены и сохранены в программе
    if not current_exchange_rates:
        messagebox.showerror('Ошибка', 'Сейчас нет актуальных данных по курсам криптовалют\n\n'
                                       'Пожалуйста, попробуйте сделать запрос чуть позже!')
        return

    # Формируем ключи для обращения данных в словаре
    abbreviated_name_cryptocurrency = popular_cryptocurrencies.get(current_cryptocurrency)
    abbreviated_name_currency = popular_currencies.get(current_currency)

    # Обращаемся к нужным данным по ключам криптовалюты и валюты
    current_exchange_rate = current_exchange_rates[current_cryptocurrency.lower().replace(' ', '')][abbreviated_name_currency.lower()]

    # Формируем результат запроса в текст для показа в окне приложения
    text_rate = f'1 {abbreviated_name_cryptocurrency} ({current_cryptocurrency}) = {current_exchange_rate:,.2f} {abbreviated_name_currency} ({current_currency})'
    text_last_update = f'Последнее обновление данных: {last_update_time_rates.strftime("%H:%M %d.%m.%Y")}'

    # Показываем выбранный курс криптовалюты и валюты пользователем
    lbl_current_cryptocurrency_rate.config(text=f'{text_rate} \n\n{text_last_update}', justify='center')

def about() -> None:
    """Функция для отображения информационного меню о приложении, о разработчике и краткой инструкцией руководство пользователя
     в меню приложения"""
    text_about_program = '''Программа для получения актуальных курсов популярных криптовалют\n
Данные сохраняются и обновляются при новом запросе каждые 20 секунд\n
Выберите в главном меню из выпадающих списков нужную криптовалюту и валюту, после нажмите на кнопку "Посмотреть курс криптовалюты" для получения и отображения данных\n 
Данные по курсам криптовалют предоставлены сервисом "CoinGecko"\n
Разработчик приложения - Крылов Дмитрий Сергеевич\n
Ссылка на GitHub - github.com/kou5t\n
Email для связи - kou5t@yandex.ru'''
    messagebox.showinfo(title='О программе', message=text_about_program)

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

# Словарь актуальных курсов криптовалют с разных сайтов
current_exchange_rates = {}

# Формируем для запроса нужные криптовалюты и валюты для передачи их по API
currencies = ','.join(popular_currencies.values())
cryptocurrencies = ','.join(map(lambda w: w.replace(' ', ''), popular_cryptocurrencies.keys()))

# Создание основного окна приложения
window = Tk()
window.title('Курсы криптовалют')
window.geometry('500x250')

# Создаем меню в приложение окна
menu = Menu(master=window)

# Создаем вкладку "меню" с описанием программы и выходом
main_menu = Menu(master=menu, tearoff=0)
main_menu.add_command(label="О программе", command=about)
main_menu.add_command(label="Выйти", command=quit)
menu.add_cascade(label="Меню", menu=main_menu)

# Добавляем меню в окно приложения
window.config(menu=menu)

# Размещаем метку для информирования пользователя, что нужно сделать в этом окне
Label(text='Выберите криптовалюту и валюту для показа актуального курса\n').pack(pady=10)

# Создаем фрейм для корректного расположения выпадающих списков
frm_combobox = ttk.Frame(master=window)
frm_combobox.pack()

# Список для выбора популярной криптовалюты
cryptocurrencies_combobox = ttk.Combobox(master=frm_combobox, values=list(popular_cryptocurrencies.keys()), state='readonly')
cryptocurrencies_combobox.pack(side='left', padx=5)

# Устанавливаем выбор по умолчанию, чтобы пользователю было понятно, что нужно в этом списке выбрать криптовалюту
set_value_cryptocurrencies = '-- криптовалюта --'
cryptocurrencies_combobox.set(set_value_cryptocurrencies)

# Разделительная черта между выпадающими списками, что во что конвертируем (криптовалюту в валюту)
Label(master=frm_combobox, text='->').pack(side='left', padx=5)

# Список для выбора популярной валюты
currencies_combobox = ttk.Combobox(master=frm_combobox, values=list(popular_currencies.keys()), state='readonly')
currencies_combobox.pack(side='left', padx=5)

# Устанавливаем выбор по умолчанию, чтобы пользователю было понятно, что нужно в этом списке выбрать валюту
set_value_currencies = '-- валюта --'
currencies_combobox.set(set_value_currencies)

# Размещаем кнопку для возможности пользователю запросить курс криптовалюты
ttk.Button(master=window, text='Посмотреть курс криптовалюты', command=show_cryptocurrency_rate).pack(pady=20)

# Метка для показа курса криптовалюты после запроса
lbl_current_cryptocurrency_rate = ttk.Label(text='')
lbl_current_cryptocurrency_rate.pack(pady=10)

# Сохраняем последнюю дату и время обновления курса криптовалют и загружаем данные по актуальным курсам
last_update_time_rates = datetime.datetime.now()
get_current_rates_from_api()

# Запускаем цикл событий
window.mainloop()
