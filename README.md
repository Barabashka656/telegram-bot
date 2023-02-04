<h1 align="center">
  Gabe Newell's agent
</h1>

<h2 align="center">
  <img height="300px" src="images/bot_logo.jpg">
</h2>

<p align="center">
  <a title="Python version" href="https://www.python.org/downloads/release/python-3100">
    <img alt="'Build' workflow Status" src="https://img.shields.io/github/pipenv/locked/python-version/barabashka656/super-bot?color=%231E90FF">
  </a>
  <a title="Aiogram version" href="https://github.com/aiogram/aiogram#aiogram">
   <img alt= ""src="https://img.shields.io/github/pipenv/locked/dependency-version/barabashka656/super-bot/aiogram?color=%2300FF00">
  </a>
</p>

## This is a Telegram Bot built using [Aiogram](https://github.com/aiogram/aiogram#aiogram) library in Python. The bot can perform the following tasks:


- translate text (soon)
- Notify about new free games on Epic Games Store
- Generate QR codes
- Scan QR codes
- Generate short URLs
- Scan short URLs
- Download videos from YouTube


# Installing
1. Clone the repository:
```shell
git clone https://github.com/Barabashka656/super-bot.git
```

```shell
cd super-bot
```

2. Install pipenv 
if you're using Windows
```shell
pip install --user pipenv
```
Otherwise refer to the [documentation](https://github.com/pypa/pipenv#installation)
for instructions

3. Create virtual environment 
```shell
pipenv shell
```
4. Install dependencies from pipfile:
  ```shell
  pipenv sync
  ```
5. Rename the **[.env.dist](https://github.com/Barabashka656/super-bot/blob/main/.env.dist)** file to **.env** and update it with your API keys

# Usage
1. Run the bot:
```shell
python run.py
```
2. Start chatting with your bot on Telegram.



# Contributions
All contributions are welcome. Feel free to create a pull request or an issue.

# License
See the [LICENSE](https://github.com/Barabashka656/super-bot/blob/main/LICENSE) file for license rights and limitations (MIT).
