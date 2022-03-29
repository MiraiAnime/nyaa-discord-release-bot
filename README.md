# nyaa-discord-release-bot

___

written in python

---

### Latest update:
#### Blacklist support using the following command: `.add_blacklist`/`.remove_blacklist`/`black_list`.

###### Now there are two files for each activated channel: `watch_<id>` and `blacklist_<id>`. 

---

`.help` will get yourself a list of options

don't forget to activate your notification channel with `.activate_channel`

be aware the `.now` command can make nyaa go cry, just dont please

---

bot reads token from `.env` file looking like this:

```
DISCORD_TOKEN=<put your token here>
```

after activating your channel the bot will create two files and add search/blacklist patterns to it

(these will be removed when deactivating the channel)

regex should be supported, but is limited due to the environment; could look as easy as this

```
BDMV
Moozzi2
Leadale.*ENG.*NanDesuKa
```

while you can write these settings to the file yourself, I would much rather just configure them using the bot commands (`.help`)

---

Command notes:
+ `.add` and `.add_blacklist` supports code blocks -> (``)