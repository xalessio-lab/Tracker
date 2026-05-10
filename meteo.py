import os
import requests
import telebot

# Recupero variabili dai Secrets
TOKEN = os.environ.get('8223933518:AAGQUdtMu3f-Ydn17l73_d8T7Cz9HGpvaXM')
CHAT_ID = os.environ.get('38862263')
WEATHER_KEY = os.environ.get('928253ef7fc98e6be269725c9f61b762')
CITTA = "Cagliari,IT"

bot = telebot.TeleBot(TOKEN)

def prendi_meteo():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITTA}&appid={WEATHER_KEY}&units=metric&lang=it"
    risposta = requests.get(url).json()
    
    # Estrazione dati
    temp = risposta['main']['temp']
    desc = risposta['weather'][0]['description']
    vento_kmh = risposta['wind']['speed'] * 3.6 # Converte m/s in km/h
    
    messaggio = f"☀️ **Meteo a Cagliari:**\n"
    messaggio += f"🌡️ Temperatura: {temp:.1f}°C\n"
    messaggio += f"☁️ Condizioni: {desc.capitalize()}\n"
    messaggio += f"💨 Vento: {vento_kmh:.1f} km/h\n\n"
    
    # Consiglio dell'Agent
    if vento_kmh > 30:
        messaggio += "🚩 **Consiglio:** C'è vento forte! Occhio se vai al Poetto o se hai panni stesi! 🌬️"
    elif "pioggia" in desc:
        messaggio += "☔ **Consiglio:** Oggi serve l'ombrello."
    elif temp > 28:
        messaggio += "🏖️ **Consiglio:** Fa caldo, giornata da spiaggia?"
    else:
        messaggio += "✨ **Consiglio:** Buona giornata in città!"

    bot.send_message(CHAT_ID, messaggio, parse_mode='Markdown')

if __name__ == "__main__":
    prendi_meteo()
