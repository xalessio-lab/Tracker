import os
import requests
import yfinance as yf
import telebot

# --- CONFIGURAZIONE ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
WEATHER_KEY = os.environ.get('OPENWEATHER_API_KEY')
CITTA = "Cagliari,IT"

bot = telebot.TeleBot(TOKEN)

def get_direzione_vento(gradi):
    """Mappa i gradi nella direzione cardinale corretta"""
    if 337.5 <= gradi or gradi < 22.5:
        return "Nord (Tramontana)"
    if 22.5 <= gradi < 67.5:
        return "Nord-Est (Grecale)"
    if 67.5 <= gradi < 112.5:
        return "Est (Levante)"
    if 112.5 <= gradi < 157.5:
        return "Sud-Est (Scirocco)"
    if 157.5 <= gradi < 202.5:
        return "Sud (Ostro)"
    if 202.5 <= gradi < 247.5:
        return "Sud-Ovest (Libeccio)"
    if 247.5 <= gradi < 292.5:
        return "Ovest (Ponente)"
    if 292.5 <= gradi < 337.5:
        return "Nord-Ovest (Maestrale)"
    return "N/D"

def ottieni_report():
    # 1. Recupero Dati Meteo
    w_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITTA}&appid={WEATHER_KEY}&units=metric&lang=it"
    w_res = requests.get(w_url).json()
    
    temp = w_res['main']['temp']
    desc = w_res['weather'][0]['description'].capitalize()
    vento_kmh = w_res['wind']['speed'] * 3.6
    direzione = get_direzione_vento(w_res['wind'].get('deg', 0))

    # 2. Recupero Quotazioni (Azioni e Commodities)
    tickers = {
        "NVIDIA": "NVDA",
        "APPLE": "AAPL",
        "ORO (LBMA)": "GC=F",
        "BRENT CRUDE": "BZ=F"
    }
    
    prezzi_msg = ""
    for nome, t in tickers.items():
        dati = yf.Ticker(t).history(period="1d")
        if not dati.empty:
            prezzo = dati['Close'].iloc[-1]
            prezzi_msg += f"🔹 {nome}: {prezzo:.2f}\n"

    # 3. Composizione Finale del Messaggio
    msg = f"📊 **REPORT ORARIO AGGIORNATO**\n\n"
    msg += f"🌡️ {CITTA}: {temp:.1f}°C, {desc}\n"
    msg += f"🌬️ Vento: {vento_kmh:.1f} km/h - {direzione}\n\n"
    msg += f"💰 **Mercati & Commodities:**\n{prezzi_msg}"
    
    return msg

if __name__ == "__main__":
    try:
        report = ottieni_report()
        bot.send_message(CHAT_ID, report, parse_mode="Markdown")
        print("Report inviato con successo!")
    except Exception as e:
        print(f"Errore durante l'invio: {e}")
