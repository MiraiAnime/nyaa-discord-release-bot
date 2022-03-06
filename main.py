import os
import discord
import feedparser
import time
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
    global search_requirements, notif_channel
    try:
        with open(".requirements", "r+") as file:
            search_requirements = [line.rstrip('\n') for line in file]
        print(search_requirements)
    except:
        search_requirements = []
    notif_channel = 0
    print("Started")
    checking.start()


@bot.command(name="add", help="add a search requirement")
async def on_message(message):
    channel = message.channel
    await channel.send("Please enter what you want to monitor:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel
    msg = await bot.wait_for("message", check=check)
    search_requirements.append(msg.content.lower())
    with open(".requirements", "a+") as search:
        search.seek(0)
        search.truncate()
        search.writelines("%s\n" % i for i in search_requirements)
    await message.send("\"{}\" has been added.".format(msg.content.lower()))


@bot.command(name="remove", help="remove search requirement")
async def on_message(message):
    channel = message.channel
    await channel.send("Please enter what you no longer want to monitor:")

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    msg = await bot.wait_for("message", check=check)
    try:
        for i in search_requirements:
            if i == msg.content.lower():
                search_requirements.remove(i)
        with open(".requirements", "a+") as search:
            search.seek(0)
            search.truncate()
            search.writelines("%s\n" % i for i in search_requirements)
    except:
        await message.send("Action failed. Your input was probably not in the list to begin with.\nPlease try again.")
    else:
        await message.send("\"{}\" has been successfully removed.".format(msg.content.lower()))


@bot.command(name="list", help="list all active search requirements")
async def on_message(message):
    channel = message.channel
    await channel.send("Here is the list of words, which are currently being monitored for: {}".format(search_requirements))


@bot.command(name="set_channel", help="set the notification channel to the current one")
async def on_message(message):
    global notif_channel
    channel = message.channel
    notif_channel = message.channel
    await channel.send("Channel has been successfully changed.")


@tasks.loop(minutes=1)
async def checking():
    if notif_channel == 0:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                            name="for .set_channel command."))
        return
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name="this fucking mess."))
        channel = notif_channel
    timeout = 0
    connection = False
    while not connection:
        try:
            print("Checking at {}, for {}.".format(datetime.now().strftime("%H:%M:%S"), search_requirements))
            rss = feedparser.parse(url)
            timeout = 0
        except:
            print("Connection failed.")
            if timeout == 10:
                await channel.send("10th connection attempt failed. Please help!")
                timeout = 0
            time.sleep(5)
            timeout = timeout + 1
        else:
            print("  connected")
            entries = rss['entries']
            title_list = []
            link_list = []
            for item in entries:
                item_index = entries.index(item)
                item_title = entries[item_index]["title"]
                item_link = entries[item_index]["guid"]
                for x in search_requirements:
                    if x in item_title.lower():
                        title_list.append(item_title)
                        link_list.append(item_link)
            if not title_list:
                print("Nothing found.")
                return
            database = open("rss.db", "a+")
            database.seek(0)
            raw_db = str(database.read())
            releases = False
            new_titles = []
            new_links = []
            for entry in link_list:
                if entry not in raw_db.lower():
                    database.seek(0, 2)
                    database.write("{} - {}".format(title_list[link_list.index(entry)], entry))
                    database.write("\n")
                    new_titles.append(title_list[link_list.index(entry)])
                    new_links.append(entry)
                    releases = True
            database.close()
            if releases:
                embed = discord.Embed()
                embed.title = "Nyaa-Release-Notification"
                embed.set_thumbnail(url="https://i.imgur.com/3RS9unL.png")
                embed.set_footer(text="Watching: {}".format(url))
                for x in new_links:
                    embed.add_field(name=new_titles[new_links.index(x)], value=x, inline=False)
                await channel.send(embed=embed)
            else:
                print("nothing new")
            connection = True


if __name__ == '__main__':
    global url
    url = "https://nyaa.si/?page=rss&q=-ohys+-web+-TX&c=1_4&f=0"
    bot.run(TOKEN)
