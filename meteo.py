import os
import requests
import telebot

# Recupero variabili dai Secrets
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
WEATHER_KEY = os.environ.get('OPENWEATHER_API_KEY')
CITTA = "Cagliari,IT"

bot = telebot.TeleBot(TOKEN)

def get_direzione_vento(gradi):
    """Converte i gradi in direzioni e nomi dei venti"""
    if 337.5 <= gradi or gradi < 22.5: return "Nord (Tramontana)"
    if 22.5 <= gradi < 67.5: return "Nord-Est (Grecale)"
    if 67.5 <= gradi < 112.5: return "Est (Levante)"
    if 112.5 <= gradi < 157.5: return "Sud-Est (Scirocco)"
    if 157.5 <= gradi < 202.5: return "Sud (Ostro)"
    if 202.5 <= gradi < 247.5: return "Sud-Ovest (Libeccio)"
    if 247.5 <= gradi < 292.5: return "Ovest (Ponente)"
    if 292.5 <= gradi < 337.5: return "Nord-Ovest (Maestrale)"
    return "N/D"

def prendi_meteo():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITTA}&appid={WEATHER_KEY}&units=metric&lang=it"
    risposta = requests.get(url).json()

    # Estrazione dati
    temp = risposta['main']['temp']
    desc = risposta['weather'][0]['description']
    vento_ms = risposta['wind']['speed']
    vento_kmh = vento_ms * 3.6
    gradi = risposta['wind'].get('deg', 0)
    direzione = get_direzione_vento(gradi)

    # Composizione messaggio
    messaggio = f"☀️ **Meteo a Cagliari:**\n"
    messaggio += f"🌡️ Temperatura: {temp:.1f}°C\n"
    messaggio += f"☁️ Condizioni: {desc.capitalize()}\n"
    messaggio += f"🌬️ Vento: {vento_kmh:.1f} km/h\n"
    messaggio += f"🧭 Direzione: {direzione}\n"

    # Logica dei consigli
    if vento_kmh > 30:
        messaggio += "\n🚩 **Consiglio:** C'è vento forte! Occhio se vai al Poetto o se hai panni stesi! 🧺"
    elif "pioggia" in desc:
        messaggio += "\n☔ **Consiglio:** Oggi serve l'ombrello."
    elif temp > 28:
        messaggio += "\n🏖️ **Consiglio:** Fa caldo, giornata da spiaggia!"

    return messaggio

# Esecuzione e invio
testo_meteo = prendi_meteo()
bot.send_message(CHAT_ID, testo_meteo, parse_mode="Markdown")
