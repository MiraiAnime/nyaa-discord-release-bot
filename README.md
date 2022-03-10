# nyaa-discord-release-bot

___

written in python

---

`.help` will get yourself a list of options

dont forget to activate your notification channel with `.activate_channel`

since I have no hobbies, the bot now supports multiple different channels at the same time

be aware the `.now` command can make nyaa go cry, just dont please

---

bot reads token from `.env` file looking like this:

```
DISCORD_TOKEN=<put your token here>
```

after activating your channel the bot will create a file and add search patterns to it

these will be removed after deactivating the channel

regex should be supported but limited due to the environment, but could look as easy as this

```
BDMV
Moozzi2
```

while you can write these settings to the file yourself, I would much rather just configure them using the bot commands (`.help`)

---