# Ritual Checker

This script monitors the latest transactions of a given Ethereum wallet on the BaseScan blockchain and sends notifications to a Telegram group.

## Features
- Fetches the latest transaction from BaseScan API
- Sends formatted messages to a Telegram group
- Supports both successful and failed transaction tracking

## Installation

### Clone the repository
```sh
git clone https://github.com/bwoogmy/ritual_checker.git
cd ritual_checker
```

### Install dependencies
```sh
pip install -r requirements.txt
```

### Configure environment variables
```sh
cp .env.example .env
nano .env
```

### Run the script manually
```sh
python3 checker.py
```

### Set up a cron job for automation
```sh
0 0 * * * /usr/bin/python3 /path/to/ritual_checker/checker.py
```

## API Reference

### BaseScan API

This script fetches transactions from the [BaseScan API](https://api.basescan.org/).  
Requires an API key.

### Telegram Bot API

- `YOUR_TELEGRAM_BOT_TOKEN` - Bot token from BotFather.
- `YOUR_CHAT_ID` - Chat ID where messages will be sent.
