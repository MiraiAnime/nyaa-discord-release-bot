import io
import os
import discord
import feedparser
import time
import re
import urllib.request
import urllib.parse
import bencode
import hashlib
import base64
import requests
from datetime import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PASTEBIN_TOKEN = os.getenv("PASTEBIN_TOKEN")
PASTEBIN_USER = os.getenv("PASTEBIN_USER")
PASTEBIN_PASSWORD = os.getenv("PASTEBIN_PASSWORD")
help_command = commands.DefaultHelpCommand(
    no_category="Release-Notifications"
)
bot = commands.Bot(
    command_prefix=".",
    help_command=help_command
)


@bot.event
async def on_ready():
    global notif_channel
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=".help"))
    print("Started")
    checking.start()


@bot.command(name="add", help="Add a search requirement")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("watch_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    await channel.send("Please enter what you want to monitor:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    msg = await bot.wait_for("message", check=check)
    with open("watch_{}".format(channel_id), "a+") as search:
        search.seek(0)
    # print(msg.content.lower(), "\n", search.read())
        if msg.content.lower() in search.read():
            await message.send("This search request is already being indexed. Check out \".list\"")
            return
        elif "\"" in msg.content.lower():
            await message.send("Make sure not to include this character:\"")
            return
        elif "\n" in msg.content.lower():
            await message.send("Your message mustn't persist of more than one line!")
            return
        user_input = (msg.content.lower()).replace("`", "")
        search.seek(0, io.SEEK_END)
        search.write("{}\n".format(user_input))
    await message.send("`{}` has been added to the watchlist.".format(user_input))


@bot.command(name="remove", help="Remove search requirement")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("watch_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    await channel.send("Please enter what you no longer want to monitor:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    msg = await bot.wait_for("message", check=check)
    with open("watch_{}".format(channel_id), "r") as remove_file:
        lines = remove_file.readlines()
    if msg.content.lower() not in str(lines):
        await message.send("This search request was not being indexed. Check out `.list`")
        return
    elif "\"" in msg.content.lower():
        await message.send("Make sure not to include this character: \"")
        return
    elif "\n" in msg.content.lower():
        await message.send("Your message mustn't persist of more than one line!")
        return
    line = ""
    remove = False
    for i in lines:
        if msg.content.lower() != i[:-1]:
            line = line + i
        else:
            remove = True
    with open("watch_{}".format(channel_id), "w+") as remove_file_write:
        remove_file_write.write(line)
        if remove:
            await message.send("\"{}\" has been successfully removed.".format(msg.content.lower()))
        else:
            await message.send(
                "Action failed. Your input was not being indexed to begin with.")


@bot.command(name="add_blacklist", help="Add something to the blacklist")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("blacklist_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    await channel.send("Please enter what you want to blacklist:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    msg = await bot.wait_for("message", check=check)
    with open("blacklist_{}".format(channel_id), "a+") as blacklist:
        blacklist.seek(0)
        if msg.content.lower() in blacklist.read():
            await message.send("This is already in your blacklist. Check out \".black_list\"")
            return
        elif "\"" in msg.content.lower():
            await message.send("Make sure not to include this character:\"")
            return
        elif "\n" in msg.content.lower():
            await message.send("Your message mustn't persist of more than one line!")
            return
        blacklist.seek(0, io.SEEK_END)
        blacklist.write("{}\n".format(msg.content.lower()))
    await message.send("\"{}\" has been added to your blacklist.".format(msg.content.lower()))


@bot.command(name="remove_blacklist", help="Remove blacklist item")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("blacklist_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    await channel.send("Please enter what you no longer want to ignore:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    msg = await bot.wait_for("message", check=check)
    with open("blacklist_{}".format(channel_id), "r") as remove_file:
        lines = remove_file.readlines()
    if msg.content.lower() not in str(lines):
        await message.send("This was not in your blacklist. Check out `.black_list`")
        return
    elif "\"" in msg.content.lower():
        await message.send("Make sure not to include this character: \"")
        return
    elif "\n" in msg.content.lower():
        await message.send("Your message mustn't persist of more than one line!")
        return
    line = ""
    remove = False
    for i in lines:
        if msg.content.lower() != i[:-1]:
            line = line + i
        else:
            remove = True
    with open("blacklist_{}".format(channel_id), "w+") as remove_file_write:
        remove_file_write.write(line)
        if remove:
            await message.send("\"{}\" has been successfully removed.".format(msg.content.lower()))
        else:
            await message.send(
                "Action failed. Your input was not being ignored to begin with.")


@bot.command(name="list", help="List all active search requirements")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("watch_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    with open("watch_{}".format(channel_id), "r") as search:
        ahaha = []
        for x in search.readlines():
            ahaha.append(x[:-1])
    await channel.send("Here is the list of words, which are currently being monitored for: `{}`".format(ahaha))


@bot.command(name="black_list", help="List all items on your blacklist")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("blacklist_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    with open("blacklist_{}".format(channel_id), "r") as search:
        ahaha = []
        for x in search.readlines():
            ahaha.append(x[:-1])
    await channel.send("Here is the list of words, which are currently being ignored: `{}`".format(ahaha))


@bot.command(name="activate_channel", help="Active notifications for this channel")
async def on_message(message):
    global notif_channel
    channel = message.channel
    channel_id = message.message.channel.id
    try:
        open("watch_{}".format(channel_id), "x")
        open("blacklist_{}".format(channel_id), "x")
        await channel.send("This channel has been successfully activated.")
    except:
        await channel.send("This channel has already been activated.")


@bot.command(name="deactivate_channel", help="Remove any notification settings for the current channel")
async def on_message(message):
    global notif_channel
    channel = message.channel
    channel_id = message.message.channel.id
    if os.path.isfile("watch_{}".format(channel_id)):
        os.remove("watch_{}".format(channel_id))
        os.remove("blacklist_{}".format(channel_id))
        await channel.send("This channel has been successfully deactivated.")
    else:
        await channel.send("This channel wasn't activated.")


@bot.command(name="now", help="Search the url right now, disregarding the one minute waiting-time")
async def on_message(message):
    channel = message.channel
    await channel.send("Searching `{}` right now.".format(url))
    await checking()


@tasks.loop(minutes=1)
async def checking():
    def torrentfile_to_pastebin(torrent_link, torrent_name):
        if not os.path.isdir("torrent_files"):
            os.makedirs("torrent_files")
        filename = torrent_link.replace("https://nyaa.si/download/", "")
        urllib.request.urlretrieve(torrent_link, "torrent_files/{}".format(filename))
        torrent_file = open("./torrent_files/{}".format(filename), 'rb').read()
        torrent_metadata = bencode.bdecode(torrent_file)
        hash_content = bencode.bencode(torrent_metadata["info"])
        digest = hashlib.sha1(hash_content).digest()
        b32hash = base64.b32encode(digest)
        try:
            params = {'xt': 'urn:btih:%s' % b32hash,
                      'dn': torrent_metadata['info']['name'],
                      'tr': torrent_metadata['announce'],
                      'xl': torrent_metadata['info']['length']}
        except KeyError:
            params = {'xt': 'urn:btih:%s' % b32hash,
                      'dn': torrent_metadata['info']['name'],
                      'tr': torrent_metadata['announce']}
        param_str = urllib.parse.urlencode(params)
        magnet_link = 'magnet:?%s' % param_str
        post_data = {
            "api_dev_key": PASTEBIN_TOKEN,
            "api_user_key": api_user_key,
            "api_option": "paste",
            "api_paste_private": "0",
            "api_paste_expire_date": "N",
            "api_paste_name": "Nyaa-Torrent {}".format(filename),
            "api_paste_code": "{}\n{}".format(torrent_name, magnet_link)
        }
        magnet_pastebin = requests.post("https://pastebin.com/api/api_post.php", post_data).text
        return magnet_pastebin
    post_data = {
        "api_dev_key": PASTEBIN_TOKEN,
        "api_user_name": PASTEBIN_USER,
        "api_user_password": PASTEBIN_PASSWORD
    }
    api_user_key = requests.post("https://pastebin.com/api/api_login.php", post_data)
    id_watch_list = []
    watch_list = []
    id_ignore_list = []
    ignore_list = []
    for x in re.findall("watch_[0-9]+", str(os.listdir())):
        with open(x, 'r') as file:
            x = x.replace("watch_", "")
            lines = file.readlines()
            for i in lines:
                id_watch_list.append(x)
                watch_list.append(i[:-1])
        with open("blacklist_{}".format(x), "r") as blacklist:
            lines = blacklist.readlines()
            for i in lines:
                id_ignore_list.append(x)
                ignore_list.append(i[:-1])
    timeout = 0
    connection = False
    while not connection:
        try:
            print("Checking at {}.".format(datetime.now().strftime("%H:%M:%S")))
            rss = feedparser.parse(url)
            timeout = 0
        except:
            print("Connection failed.")
            if timeout == 10:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name="CONNECTION FAILURES :("))
                timeout = 0
            time.sleep(5)
            timeout = timeout + 1
        else:
            print("  connected")
            entries = rss['entries']
            title_list = []
            link_list = []
            id_notif = []
            torrent_file_list = []
            # skip_list = []
            for item in entries:
                item_index = entries.index(item)
                if entries[item_index]["nyaa_categoryid"] == "1_3":
                    continue
                item_title = entries[item_index]["title"]
                item_link = entries[item_index]["guid"]
                item_torrent_file = entries[item_index]["link"]
                for x in watch_list:
                    blacklist_status = False
                    if re.findall(x, item_title.lower()):
                        id_index = 0
                        for y in id_ignore_list:
                            # if "{}-{}".format(id_watch_list[watch_list.index(x)], item_title) in skip_list:
                            #     continue
                            if y == id_watch_list[watch_list.index(x)]:
                                if re.findall(ignore_list[id_index], item_title.lower()):
                                    # skip_list.append("{}-{}".format(id_watch_list[watch_list.index(x)], item_title))
                                    # print(skip_list)
                                    blacklist_status = True
                                    continue
                                # else:
                                #     print("{} does not match {}".format(item_title.lower(), ignore_list[id_index]))
                            id_index = id_index + 1
                        if not blacklist_status:
                            title_list.append(item_title)
                            link_list.append(item_link)
                            torrent_file_list.append(item_torrent_file)
                            id_notif.append(id_watch_list[watch_list.index(x)])
            if not title_list:
                print("Nothing found.")
                return
            database = open("rss.db", "a+")
            database.seek(0)
            raw_db = str(database.read())
            releases = False
            new_torrent_links = []
            new_titles = []
            new_links = []
            new_id = []
            for entry in link_list:
                if entry not in raw_db.lower() and entry not in new_links:
                    database.seek(0, 2)
                    database.write("{} - {}".format(title_list[link_list.index(entry)], entry))
                    database.write("\n")
                    new_titles.append(title_list[link_list.index(entry)])
                    new_torrent_links.append(torrentfile_to_pastebin(torrent_file_list[link_list.index(entry)],
                                                                     title_list[link_list.index(entry)]))
                    new_id.append(id_notif[link_list.index(entry)])
                    new_links.append(entry)
                    releases = True
            database.close()
            if releases:
                index = 0
                for what in new_id:
                    embed = discord.Embed()
                    embed.title = "Nyaa-Release-Notification"
                    embed.set_thumbnail(url="https://i.imgur.com/3RS9unL.png")
                    embed.set_footer(text="Watching: {}".format(url))
                    embed.add_field(name=new_titles[index], value=new_links[index]
                                    , inline=False)
                    embed.add_field(name="Magnet-Link - Pastebin:", value=new_torrent_links[index], inline=False)
                    channel = bot.get_channel(int(what))
                    await channel.send(embed=embed)
                    index = index + 1
                    time.sleep(2)
            else:
                print("nothing new")
            connection = True


if __name__ == '__main__':
    global url
    url = "https://nyaa.si/?page=rss"
    bot.run(TOKEN)
