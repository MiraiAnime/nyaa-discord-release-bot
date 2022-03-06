# nyaa-discord-release-bot

___

written in python

---

control the bot with the `.` option.

something like `.help` will get yourself a list of options

dont forget to set the notification channel with `.set_channel`, on every restart

---

bot reads token from `.env` file looking like this:

```
DISCORD_TOKEN=<put your token here>
```

later on the bot will add your settings to the .env file, f.e.
```
DISCORD_TOKEN=<put your token here>
SEARCH_REQUIREMENTS=<something like "['neoHEVC', 'judas']">
```
while you can write these settings to the file yourself, I would much rather just configure them using the bot commands (`.help`)

---