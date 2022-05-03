# nyaa-discord-release-bot

___

written in python

---

### Latest update:

#### Archiving and processing whatever the bot picked up:

Since yesterday's Teasing Master-san's BDMV got removed, I decided to make the bot do the following with matches:

Match -> Downloads torrent-file to disk -> extracts hash and (first) tracker-url -> creates pastebin dumb with magnet-link.

... pastebin link will be shown in the embed.

This will however require you to create a pastebin account and/to retrieve your API token.

### !! See `.env` documentation below !!

If you are having problems running, even after installing the new requirements,
try to install bencode using this command -> `python -m pip install bencode.py` (including the `.py`-extension)

___

Blacklist support using the following command: `.add_blacklist`/`.remove_blacklist`/`.black_list`.

###### Now there are two files for each activated channel: `watch_<channel_id>` and `blacklist_<channel_id>`. 

---

`.help` will get yourself a list of options

don't forget to activate your notification channel with `.activate_channel`

be aware the `.now` command can make nyaa go cry, just dont please

---

### `.env` documentation:

bot reads token from `.env` file looking like this:

```
DISCORD_TOKEN=<put your token here>
PASTEBIN_TOKEN=<pastebin api token>
PASTEBIN_USER=<pastebin username (not email)>
PASTEBIN_PASSWORD=<pastebin password to account (yes, the api requires all these information)>
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