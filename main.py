import os
import discord
import feedparser
import time
import re
from datetime import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
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
    if not os.path.isfile("channel_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    await channel.send("Please enter what you want to monitor:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    msg = await bot.wait_for("message", check=check)
    with open("channel_{}".format(channel_id), "a+") as search:
        if msg.content.lower() in search.read():
            await message.send("This search request is already being indexed. Check out \".list\"")
            return
        elif "\"" in msg.content.lower():
            await message.send("Make sure not to include this character:\"")
            return
        elif "\n" in msg.content.lower():
            await message.send("Your message mustn't persist of more than one line!")
            return
        search.write("{}\n".format(msg.content.lower()))
    await message.send("\"{}\" has been added.".format(msg.content.lower()))


@bot.command(name="remove", help="Remove search requirement")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("channel_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    await channel.send("Please enter what you no longer want to monitor:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    msg = await bot.wait_for("message", check=check)
    with open("channel_{}".format(channel_id), "r") as remove_file:
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
    with open("channel_{}".format(channel_id), "w+") as remove_file_write:
        remove_file_write.write(line)
        if remove:
            await message.send("\"{}\" has been successfully removed.".format(msg.content.lower()))
        else:
            await message.send(
                "Action failed. Your input was not being indexed to begin with.")


@bot.command(name="list", help="List all active search requirements")
async def on_message(message):
    channel = message.channel
    channel_id = message.message.channel.id
    if not os.path.isfile("channel_{}".format(channel_id)):
        await message.send("Action failed. Please run `.activate_channel` to set your notification channel.")
        return
    with open("channel_{}".format(channel_id), "r") as search:
        ahaha = []
        for x in search.readlines():
            ahaha.append(x[:-1])
    await channel.send("Here is the list of words, which are currently being monitored for: {}".format(ahaha))


@bot.command(name="activate_channel", help="Active notifications for this channel")
async def on_message(message):
    global notif_channel
    channel = message.channel
    channel_id = message.message.channel.id
    try:
        open("channel_{}".format(channel_id), "x")
        await channel.send("This channel has been successfully activated.")
    except:
        await channel.send("This channel has already been activated.")


@bot.command(name="deactivate_channel", help="Remove any notification settings for the current channel")
async def on_message(message):
    global notif_channel
    channel = message.channel
    channel_id = message.message.channel.id
    if os.path.isfile("channel_{}".format(channel_id)):
        os.remove("channel_{}".format(channel_id))
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
    id_list = []
    other_list = []
    for x in re.findall("channel_[0-9]+", str(os.listdir())):
        with open(x, 'r') as file:
            x = x.replace("channel_", "")
            lines = file.readlines()
            for i in lines:
                id_list.append(x)
                other_list.append(i[:-1])
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
            for item in entries:
                item_index = entries.index(item)
                item_title = entries[item_index]["title"]
                item_link = entries[item_index]["guid"]
                for x in other_list:
                    if re.findall(x, item_title.lower()):
                        title_list.append(item_title)
                        link_list.append(item_link)
                        id_notif.append(id_list[other_list.index(x)])
            if not title_list:
                print("Nothing found.")
                return
            database = open("rss.db", "a+")
            database.seek(0)
            raw_db = str(database.read())
            releases = False
            new_titles = []
            new_links = []
            new_id = []
            for entry in link_list:
                if entry not in raw_db.lower():
                    database.seek(0, 2)
                    database.write("{} - {}".format(title_list[link_list.index(entry)], entry))
                    database.write("\n")
                    new_titles.append(title_list[link_list.index(entry)])
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
