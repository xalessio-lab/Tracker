import yfinance as yf
import telebot
import os
from datetime import datetime

# Carica i segreti dalle variabili d'ambiente di GitHub
TOKEN = os.getenv("8223933518:AAGQUdtMu3f-Ydn17l73_d8T7Cz9HGpvaXM")
CHAT_ID = os.getenv("38862263")

bot = telebot.TeleBot(TOKEN)

def send_update():
    try:
        # Recupero dati NVIDIA e Bitcoin
        nvda = yf.Ticker("NVDA")
        btc = yf.Ticker("BTC-USD")
        
        price_nvda = nvda.history(period="1d")['Close'].iloc[-1]
        price_btc = btc.history(period="1d")['Close'].iloc[-1]
        
        messaggio = (
            f"📊 *Update Mercati - {datetime.now().strftime('%d/%m/%Y')}*\n\n"
            f"🍏 *NVIDIA (NVDA):* ${price_nvda:.2f}\n"
            f"₿ *Bitcoin (BTC):* ${price_btc:.2f}"
        )
        
        bot.send_message(CHAT_ID, messaggio, parse_mode="Markdown")
        print("Messaggio inviato correttamente!")
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    send_update()
