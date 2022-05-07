# nyaa-discord-release-bot

___

written in python

---

### Latest update:

Realized, none of the created magnet links work.

-> fixed.

Now each tracker is also appended instead of just the first one.

Bb.
___

### Archiving and processing whatever the bot picked up:

The bot will now download each torrent file from the releases that matched the regex.
It appends data like title, checksum and the first tracker concluding in a magnet-url.
That url will be be posted on pastebin made available to the public, since why the fuck not.
This should give someone the chance to retrieve data even if the release has been deleted/hidden on nyaa.

This will however require you to create a pastebin account to retrieve your API token.

#### !!! See `.env` documentation below !!!

If you are having problems running, even after installing the new requirements,
try to install bencode using this command -> `python -m pip install bencode.py` (including the `.py`-extension)

___

### Blacklists

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