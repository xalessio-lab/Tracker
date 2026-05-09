import os
import yfinance as ticker
import telebot

# Legge i segreti impostati su GitHub
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def invia_quotazioni():
    # Bitcoin e Nvidia
    assets = {'BTC-USD': 'Bitcoin', 'NVDA': 'NVIDIA'}
    messaggio = "📊 **Quotazioni di oggi:**\n\n"
    
    for simbolo, nome in assets.items():
        dati = ticker.Ticker(simbolo)
        prezzo = dati.history(period='1d')['Close'].iloc[-1]
        messaggio += f"🔹 {nome}: ${prezzo:.2f}\n"
    
    bot.send_message(CHAT_ID, messaggio, parse_mode='Markdown')

if __name__ == "__main__":
    invia_quotazioni()
