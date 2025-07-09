import requests
import webbrowser
import re
import pycountry
import json
import os
from geopy.geocoders import Nominatim

# Словарь перевода стран с русского на английский
russian_to_english_countries = {
    "россия": "Russia",
    "япония": "Japan",
    "франция": "France",
    "германия": "Germany",
    "италия": "Italy",
    "сша": "United States",
    "узбекистан": "Uzbekistan",
    "китай": "China",
    "индия": "India",
    "украина": "Ukraine",
    "беларусь": "Belarus",
    "казахстан": "Kazakhstan",
    "великобритания": "United Kingdom",
    "турция": "Turkey"
}

FILENAME = "last_cats.json"

def get_cat():
    # Проверка наличия файла с историей
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            last_cats = json.load(f)
        print("\n📂 Предыдущие котики:")
        for url in last_cats:
            print("🐾", url)
        again = input("🔁 Открыть этих котиков снова? (да/нет): ").strip().lower()
        if again == "да":
            for url in last_cats:
                print("🔗 Открываю:", url)
                webbrowser.open(url)
            return
        print("⏭ Получаем новых котиков...")

    # Запрос нового количества котиков
    try:
        c = int(input("\n🐱 Сколько новых котиков показать? "))
        url = f"https://api.thecatapi.com/v1/images/search?limit={c}"
        response = requests.get(url)
        data = response.json()

        urls = []
        for i in range(c):
            cat_url = data[i]['url']
            print("🔗 Открываю:", cat_url)
            webbrowser.open(cat_url)
            urls.append(cat_url)

        # Сохраняем список последних котиков
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(urls, f)

    except Exception as e:
        print(f"⚠️ Ошибка: {e}")

def translate_location(city_input, country_input):
    """
    Определяет английское название города и страны по введённому на любом языке
    """
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(f"{city_input}, {country_input}", language="en")
    
    if location:
        parts = location.address.split(', ')
        eng_city = parts[0]
        eng_country = parts[-1]
        return eng_city, eng_country
    else:
        return None, None

# 🧠 Определение языка интерфейса
def detect_language_from_city(city):
    return 'ru' if re.search(r'[а-яА-ЯёЁ]', city) else 'en'

# 🌐 Нормализация названий через geopy
def translate_location(city_input, country_input):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(f"{city_input}, {country_input}", language="en")
    if location:
        parts = location.address.split(', ')
        eng_city = parts[0]
        eng_country = parts[-1]
        return eng_city, eng_country
    else:
        return None, None

# 📦 Основная функция
def get_weather():
    filename = "last_weather.json"

    # 🔁 Проверка на сохранённые данные
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            last = json.load(file)
        print("\n📂 Последний выбор:")
        print(f"Страна: {last['country_input']}")
        print(f"Город: {last['city_input']}")
        use_last = input("🔁 Использовать эти данные снова? (да/нет): ").strip().lower()
        if use_last == "да":
            eng_city, eng_country = last['eng_city'], last['eng_country']
            lang = detect_language_from_city(last['city_input'])
            return fetch_and_show_weather(eng_city, eng_country, lang, last['city_input'], last['country_input'])

        print("\n🔄 Введите новые данные:")

    # 🌏 Ввод города и страны
    while True:
        country_input = input("🌍 Введите страну (на русском или английском): ").strip()
        city_input = input("🏙 Введите город (на русском или английском): ").strip()

        # Перевод в английский для API
        eng_city, eng_country = translate_location(city_input, country_input)
        if not eng_city:
            print("❗️ Не удалось найти такой город. Попробуйте ещё раз.")
            continue

        lang = detect_language_from_city(city_input)

        # Сохраняем запрос
        with open(filename, "w", encoding="utf-8") as file:
            json.dump({
                "city_input": city_input,
                "country_input": country_input,
                "eng_city": eng_city,
                "eng_country": eng_country
            }, file)

        break

    fetch_and_show_weather(eng_city, eng_country, lang, city_input, country_input)

# 🌦 Вывод погоды
def fetch_and_show_weather(eng_city, eng_country, lang, orig_city, orig_country):
    try:
        location = f"{eng_city},{eng_country}"
        url = f"https://wttr.in/{location}?format=j1&lang={lang}"
        response = requests.get(url)
        data = response.json()

        temp_c = data['current_condition'][0]['temp_C']
        description = data['current_condition'][0]['lang_ru' if lang == 'ru' else 'weatherDesc'][0]['value']

        print(f"\n🌤 Погода в городе {orig_city.title()}, {orig_country.title()}:")
        print(f"🌡 Температура: {temp_c}°C")
        print(f"☁️ Описание: {description}")

    except Exception as e:
        print(f"⚠️ Не удалось получить данные о погоде: {e}")

def get_exchange_rate():
    filename = "last_currency_input.json"

    # Проверяем, есть ли сохранённый выбор
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            last_data = json.load(file)
        
        base = last_data["base"]
        symbols = last_data["symbols"]
        
        print("\n📂 Последний выбор:")
        print(f"Базовая валюта: {base}")
        print(f"Сравниваемые валюты: {', '.join(symbols)}")

        use_last = input("🔁 Использовать их снова? (да/нет): ").strip().lower()
        if use_last != "да":
            base, symbols = ask_user_and_save(filename)
    else:
        base, symbols = ask_user_and_save(filename)

    # Запрашиваем курс
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    try:
        response = requests.get(url)
        data = response.json()

        print(f"\n📊 Курс {base} к другим валютам:")
        for sym in symbols:
            sym = sym.strip().upper()
            rate = data['rates'].get(sym)
            if rate:
                print(f"🔸 {base} ➝ {sym}: {rate}")
            else:
                print(f"⚠️ Валюта '{sym}' не найдена")

    except Exception as e:
        print("⚠️ Ошибка получения курса:", e)

def ask_user_and_save(filename):
    base = input("💱 Введите базовую валюту (например, USD, EUR, RUB): ").strip().upper()
    symbols_input = input("💹 Введите валюты через запятую (например: RUB, EUR, JPY): ")
    symbols = [s.strip().upper() for s in symbols_input.split(",")]

    # Сохраняем в файл
    with open(filename, "w", encoding="utf-8") as file:
        json.dump({"base": base, "symbols": symbols}, file)

    return base, symbols


