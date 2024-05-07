import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=None, intents=intents)

appeared_names = set()

def update_bans():
    url = "https://id.heromc.net/vi-pham/bans.php"
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all("td")
        ten = cells[0].text.strip()

        if ten in appeared_names:
            continue

        bi_khoa_boi = cells[1].text.strip()
        ly_do = cells[2].text.strip()
        khoa_vao_luc = cells[3].text.strip()
        ngay_duoc_tha = cells[4].text.strip()

        appeared_names.add(ten)

        channel = bot.get_channel(1147538103771344926) 
        
        embed = discord.Embed(title=f"Vấn đề kĩ năng: {ten}", color=discord.Color.yellow())
        embed.add_field(name="Bị ban bởi", value=bi_khoa_boi, inline=False)
        embed.add_field(name="Lý do", value=ly_do, inline=False)
        embed.add_field(name="Bị ban vào lúc", value=khoa_vao_luc, inline=False)
        embed.add_field(name="Ngày được unban", value=ngay_duoc_tha, inline=False)
        asyncio.ensure_future(channel.send(embed=embed))

@tasks.loop(seconds=10)
async def update_bans_loop():
    update_bans()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_bans_loop.start()

bot.run('') 
