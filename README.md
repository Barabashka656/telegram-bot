<h1 align="center">
  Gabe Newell's agent
</h1>

<h3 align="center">
  <!--- <img height="300px" src="bot/data/images/bot_logo.jpg"> --->
</h3>

<p align="center">
  <a title="Python version" href="https://www.python.org/downloads/release/python-3100">
    <img alt="'Build' workflow Status" src="https://img.shields.io/github/pipenv/locked/python-version/barabashka656/super-bot?color=%231E90FF&style=for-the-badge">
  </a>
  <a title="aiogram version" href="https://github.com/aiogram/aiogram#aiogram">
   <img alt= ""src="https://img.shields.io/github/pipenv/locked/dependency-version/barabashka656/super-bot/aiogram?color=%23008000&style=for-the-badge">
  </a>
  <a title="telegram bot" href="https://t.me/MaksimNeBot">
   <img alt= ""src="https://img.shields.io/badge/telegram-%40MaksimNeBot-blue?style=for-the-badge">
  </a>
  <a title="license" href="https://github.com/Barabashka656/super-bot/blob/main/LICENSE">
  <img alt="" src="https://img.shields.io/github/license/Barabashka656/super-bot?color=%239ACD32&style=for-the-badge">
  </a>
</p>

# Description

### This is a Telegram Bot built using [Aiogram](https://github.com/aiogram/aiogram#aiogram) library in Python. 
### The bot can perform the following tasks:

- translate text (soon)
- Notify about new free games on Epic Games Store
- Generate QR codes
- Scan QR codes
- Generate short URLs
- Scan short URLs
- Download videos from YouTube
- chatting with chatGPT using bot wrapper


# Installing
1. Clone the repository
```shell
git clone https://github.com/Barabashka656/super-bot.git
```
2. change working directory to a new one
```shell
cd super-bot
```

3. Install pipenv
if you're using Windows
```shell
pip install --user pipenv
```
Otherwise refer to the [documentation](https://github.com/pypa/pipenv#installation)
for instructions

4. Create virtual environment 
```shell
pipenv shell
```
5. Install dependencies from pipfile
```shell
pipenv sync
```
1. Rename the **[.env.dist](.env.dist)** file to **.env** and update it with your API keys

# Usage
1. Run the bot:
```shell
python run.py
```
2. Start chatting with your bot on Telegram.

# Env
*(REQUIRED)*

- TELEGRAM_API_TOKEN - Bot token from [BotFather](https://telegram.me/BotFather)
- [OPEN_AI_API_KEY](https://platform.openai.com/account/api-keys) -
secret API key for using chatGPT
- ACCU_WEATHER_API_KEY - [API key](https://developer.accuweather.com/) for accessing accuweather.com api
- TOMORROW_IO_API_KEY - [API key](https://www.tomorrow.io/) for accessing tomorrow.io api
- VISUAL_API_KEY - [API key](https://www.visualcrossing.com/weather-api) for accessing visualcrossing.com api

# Contributions
All contributions are welcome. Feel free to create a pull request or an issue.

# License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).
