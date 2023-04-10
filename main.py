# powered by Viktor Danilin 4th variant

import requests
import json
import random
import vosk
import pyaudio
# модель распознавания речи
model = vosk.Model("vosk-model-small-ru-0.22")
# апи курса валют к рублю
response = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/rub.json")
data = json.loads(response.content)


# функция считывания речи с микрофона
def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            command = json.loads(rec.Result())
            if command['text']:
                yield command['text']


# Функция для вывода текущего курса доллара
def usd_rate():
    print("Курс доллара: ", data["rub"]["usd"])


# Функция для вывода текущего курса евро
def eur_rate():
    print("Курс евро: ", data["rub"]["eur"])


# Функция для сохранения списка курсов валют в файл
def save_data():
    with open("rates.txt", "w") as f:
        json.dump(data["rub"], f)
    print("Данные сохранены в файл rates.txt")


# Функция для вывода количества доступных валют
def count_currencies():
    print("Количество доступных валют: ", len(data["rub"].keys()))


# Функция для вывода текущего курса случайной валюты
def random_rate():
    currency = list(data["rub"].keys())
    currency = str(random.choice(currency))
    print(currency)
    print("Курс", currency, ":", data["rub"][currency])


# инициализация микрофона и распознавалки
rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=16000
)
stream.start_stream()

for text in listen():
    # Обработка команды
    if "курс доллара" in text:
        usd_rate()
    elif "курс евро" in text:
        eur_rate()
    elif "сохранить" in text:
        save_data()
    elif "количество" in text:
        count_currencies()
    elif "случайный" in text:
        random_rate()
    elif "выход" in text:
        break
    else:
        print("Не удалось распознать команду")