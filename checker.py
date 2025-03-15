import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
NODE_NAME = os.getenv("NODE_NAME")

# Start and end block from environment variables (default values if not set)
START_BLOCK = int(os.getenv("START_BLOCK", 21000000))
END_BLOCK = int(os.getenv("END_BLOCK", 99999999))

# API URLs
BASESCAN_URL = "https://api.basescan.org/api"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def get_transactions(wallet_address):
    """Fetch the latest transactions for the given wallet."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": START_BLOCK,
        "endblock": END_BLOCK,
        "sort": "desc",
        "apikey": BASESCAN_API_KEY,
    }
    
    try:
        response = requests.get(BASESCAN_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        if data.get("status") == "1" and data.get("result"):
            return data["result"]  # List of transactions
        else:
            print(f"Error in BaseScan API Response: {data}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def format_transaction_message(transactions):
    """Format the transaction details into a readable message with emojis."""
    if not transactions:
        return f"🔷 *{NODE_NAME}* (`{WALLET_ADDRESS}`)\n❌ No transactions found."

    latest_tx = transactions[0]  # Last transaction
    timestamp = int(latest_tx["timeStamp"])
    tx_date = datetime.utcfromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M (UTC+0200)")
    status = "✅ *Success*" if latest_tx["isError"] == "0" else "❌ *Failed* (🟡 ok for node working)"

    message = f"🔷 *{NODE_NAME}* (`{WALLET_ADDRESS}`) - *Latest Transaction*\n"
    message += f"📅 *Date:* {tx_date}\n"
    message += f"📝 *Status:* {status}\n"

    # Find the last successful transaction
    if latest_tx["isError"] == "1":
        last_success_tx = next((tx for tx in transactions if tx["isError"] == "0"), None)
        if last_success_tx:
            timestamp_success = int(last_success_tx["timeStamp"])
            tx_date_success = datetime.utcfromtimestamp(timestamp_success).strftime("%d-%m-%Y %H:%M (UTC+0200)")

            message += f"\n🔹 *Last Successful Transaction*\n"
            message += f"📅 *Date:* {tx_date_success}\n"
            message += f"✅ *Status:* Success\n"

    return message

def send_telegram_message(message):
    """Send a message to the Telegram group."""
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(TELEGRAM_URL, data=payload, timeout=10)
        response.raise_for_status()  # Check HTTP response
        result = response.json()
        
        if result.get("ok"):
            print(f"Message sent successfully: {result}")
        else:
            print(f"Failed to send message: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Telegram API request failed: {e}")

def main():
    transactions = get_transactions(WALLET_ADDRESS)
    message = format_transaction_message(transactions)
    send_telegram_message(message)

if __name__ == "__main__":
    main()
