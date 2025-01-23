##### python 3.10.6
##### ONLY FOR PERSONAL USE
##### CREATE BY 培根ඞාMea(thematt7378)
##### wade12345683@gmail.com
# 導入discord.py
import discord
from discord import Interaction
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import random
import math
import requests
import sqlite3
import pyimgur
import asyncio
import aiohttp
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
# 加載環境變數
load_dotenv()
#從.evn獲取TOKEN
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("無法取得TOKEN")
    exit(1)

# 設定指令前綴
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=['ඞ'], intents=intents)

# 機器人啟動事件
@bot.event
async def on_ready():    
    try:
        await bot.tree.sync()
        print(f"Slash Commands 已同步成功！")
    except Exception as e:
        print(f"同步指令時發生錯誤：{e}")
    print(f"已登入為 {bot.user}")

# 當有人加入伺服器
@bot.event
async def on_member_join(member):
    print(f'{member} 剛剛進入了哥布林洞穴')

# 當有人退出伺服器
@bot.event
async def on_member_(member):
    print(f'{member} 悄悄的走了，正如他悄悄的來')

##############################################################
##############################################################
#######################_其他指令集中區_########################
##############################################################
##############################################################

# 一般指令
@bot.tree.command(name="hello", description="說尼好")
async def hello(interaction: discord.Interaction):
    responses = [
        f"嗨，{interaction.user.name}!",
        f"你是給"
    ]
    probabilities = [0.9, 0.1]
    response = random.choices(responses, probabilities)[0]
    await interaction.response.send_message(response)

##############################################################
##############################################################
#######################_資料庫的集中區_########################
##############################################################
##############################################################

# 初始化 SQLite 資料庫
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 建立用戶資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    level INTEGER DEFAULT 1,
    exp INTEGER DEFAULT 0,
    exp_2 INTEGER DEFAULT 0,
    atk INTEGER DEFAULT 10,
    def_ INTEGER DEFAULT 5,
    coins INTEGER DEFAULT 0,
    last_checkin TEXT
)
''')

# 建立裝備資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    card_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# 建立用戶持有的卡片表
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_cards (
    user_id INTEGER,
    card_id INTEGER,
    count INTEGER DEFAULT 0,
    url_number INTEGER DEFAULT 1,
    PRIMARY KEY (user_id, card_id),
    FOREIGN KEY (card_id) REFERENCES cards (id)
)
''')

# 建立卡片資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_1 TEXT UNIQUE,
    name_2 TEXT,
    name_3 TEXT,
    category TEXT,
    album_id TEXT UNIQUE,
    atk INTEGER,
    def_ INTEGER
)
''')

# 新增 card_urls 表格，存儲每張卡片的多個 URL
cursor.execute('''
CREATE TABLE IF NOT EXISTS card_urls (
    card_id INTEGER,
    url_number INTEGER,
    url TEXT,
    PRIMARY KEY (card_id, url),
    FOREIGN KEY (card_id) REFERENCES cards (id)
)
''')

# 確保有必要的 categorie_2 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS category_2 (
    main_name TEXT,
    another_name TEXT,
    PRIMARY KEY (main_name, another_name)
    )
''')

# 創建 url_2 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS card_urls_2 (
    card_id INTEGER,
    url TEXT,
    PRIMARY KEY (card_id, url),
    FOREIGN KEY (card_id) REFERENCES cards (id)
)
''')

conn.commit()

# 定義檢查並添加欄位的函數
def add_column_if_not_exists(table_name, column_name, column_definition):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
        conn.commit()
        print(f"已新增 {column_name} 到 {table_name}")
    else:
        print(f"{column_name} 已存在於 {table_name}")

# 為現有的 URL 賦予連續的 url_number
cursor.execute('''
WITH RankedURLs AS (
    SELECT card_id, url, ROW_NUMBER() OVER (PARTITION BY card_id ORDER BY rowid) AS url_number
    FROM card_urls
)
UPDATE card_urls
SET url_number = (
    SELECT url_number
    FROM RankedURLs
    WHERE card_urls.card_id = RankedURLs.card_id AND card_urls.url = RankedURLs.url
)
''')

conn.commit()

# 如果需要確保其他表結構，類似的操作可以重複調用函數

##############################################################
##############################################################
#######################_如果你需要幫助_########################
##############################################################
##############################################################

# HELP
@bot.tree.command(name="help", description="也許你需要一點幫助?")
async def help(interaction: discord.Interaction):
    help_message = """
**Command profix:**

- ඞ (僅限某些指令 ඞhelp)

**Available Commands:**

- **一般指令** 

/hello: 說尼好
/help: 你現在正在看的東西

- **抽卡系統**

/cards: 查看已擁有的卡片
/category: 同步分類
/check_the_top_10_cards: 查詢持有數前10高的卡片與持有者(全伺服器)
/change_url_number: 更換卡片第一張顯示的圖片
/clone: 使用錢錢兌換已擁有的卡片
/daily: 每日簽到並儲值台灣價值
/deletecard: 刪除資料庫中指定的卡片
/deleterecord: 刪除所有紀錄⚠️只能對自己使用⚠️
/equip: 裝備卡片(最多3張)
/gacha: 抽卡，斗肉!
/profile: 查看個人檔案
/search_card: 查詢資料庫的卡片
/search_card_by_category: 以分類查詢資料庫的卡片
/trade: 卡片交易系統
/unequip: 取消裝備所有卡片

- **抽卡系統⚠️18+**

/match: 匹配系統進行對戰
/search_card_r18: 查詢特定卡片的瑟圖

- **管理資料庫**

/add_cardurl: 為卡片添加新圖 (支援Imgur與本地上傳)
/add_cardurl_r18: 添加特定卡片的瑟圖
/sync_albums: 同步IMGUR資料庫
"""
    await interaction.response.send_message(help_message)

##############################################################
##############################################################
#######################_輔助函數集中區_########################
##############################################################
##############################################################

# Imgur API 配置
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
IMGUR_CLIENT_SECRET = os.getenv("IMGUR_CLIENT_SECRET")
IMGUR_USER_NAME = os.getenv("IMGUR_USER_NAME")  # 從 .env 文件中獲取帳號名稱
ACCESS_TOKEN = os.getenv("IMGUR_ACCESS_TOKEN")  # 添加 Access Token
REFRESH_TOKEN = os.getenv("IMGUR_REFRESH_TOKEN")  # 若需要刷新令牌
imgur = pyimgur.Imgur(IMGUR_CLIENT_ID)

# 初始化 PyImgur 並設置 Token
imgur = pyimgur.Imgur(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, ACCESS_TOKEN)

# 等級所需exp計算邏輯
def calculate_exp_for_level(level):
    return math.ceil(10 * (1.5 ** (level-1)))

# 上傳到IMGUR
def upload_to_imgur(localdata, album_id=None):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"  # 使用 access token 進行授權
    }
    
    files = {'image': open(localdata, 'rb')}
    
    data = {}
    if album_id:
        data['album'] = album_id  # 使用相簿 ID 上傳圖片

    response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files, data=data)
    files['image'].close()

    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        raise Exception(f"Imgur 上傳失敗: {response.json()['data']['error']}")
    
# 上傳瑟瑟的圖到IMGUR
def upload_to_imgur_r18(localdata, album_id=None, description=None):
    """
    上傳圖片到 Imgur，並可選擇添加描述
    :param localdata: 本地圖片文件的路徑
    :param album_id: 圖片要添加到的相簿 ID
    :param description: 圖片的描述
    :return: 上傳成功後的圖片 URL
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"  # 使用 access token 進行授權
    }

    files = {'image': open(localdata, 'rb')}

    data = {}
    if album_id:
        data['album'] = album_id  # 添加相簿 ID
    if description:
        data['description'] = description  # 添加圖片描述

    try:
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files, data=data)
    finally:
        files['image'].close()  # 確保文件在請求後被正確關閉

    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        raise Exception(f"Imgur 上傳失敗: {response.json().get('data', {}).get('error', '未知錯誤')}")

# 抓圖片的 URL
def convert_imgur_url(url: str) -> str:
    """
    將 Imgur 頁面鏈接轉換為直接圖片鏈接。
    如果 URL 已是圖片鏈接則保持不變。
    """
    if url.startswith("https://imgur.com/") and not url.startswith("https://i.imgur.com/"):
        # 提取圖片 ID 並轉為直接圖片鏈接
        image_id = url.split("/")[-1]
        return f"https://i.imgur.com/{image_id}.jpg"
    return url

# 從 Imgur 相簿的 URL 獲取所有圖片的直接鏈接
def get_imgur_album_images(album_url: str) -> list:
    """
    從 Imgur 相簿 URL 獲取所有圖片的直接鏈接。
    """
    if not album_url.startswith("https://imgur.com/a/"):
        raise ValueError("提供的 URL 不是有效的 Imgur 相簿 URL")
    
    album_hash = album_url.split("/a/")[-1]
    album = imgur.get_album(album_hash)  # 確保 album_hash 是正確的
    # 只返回圖片的hash
    return [image.link for image in album.images if image.type.startswith("image/")]

# 用來刷新TOKEN (如果TOKEN失效)
def refresh_access_token():
    import requests
    response = requests.post(
        "https://api.imgur.com/oauth2/token",
        data={
            "refresh_token": REFRESH_TOKEN,
            "client_id": IMGUR_CLIENT_ID,
            "client_secret": IMGUR_CLIENT_SECRET,
            "grant_type": "refresh_token",
        },
    )
    if response.status_code == 200:
        tokens = response.json()
        print("新的 Access Token:", tokens["access_token"])
        return tokens["access_token"]
    else:
        print("刷新 Token 失敗:", response.json())
        return None

# 創建相簿的輔助函數
def create_imgur_album(title):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # 使用 JSON 格式發送請求資料
    data = {
        'title': title,  # 相簿標題
        'privacy': 'private',  # 設置為 public 或 private
    }

    response = requests.post('https://api.imgur.com/3/album', headers=headers, json=data)

    # 確認是否成功創建相簿
    if response.status_code == 200:
        album_id = response.json()['data']['id']
        return album_id  # 返回相簿 ID
    else:
        raise Exception(f"創建相簿失敗：{response.json()['data']['error']}")

# 計算使用者的總 ATK 和 DEF
def calculate_total_stats(user_id):
    """
    計算使用者的總 ATK 和 DEF
    """
    # 查詢基礎 ATK 和 DEF
    cursor.execute("SELECT atk, def_ FROM users WHERE id = ?", (user_id,))
    base_stats = cursor.fetchone()
    if not base_stats:
        return 0, 0  # 用戶不存在

    base_atk, base_def = base_stats

    # 查詢裝備的卡片
    cursor.execute("SELECT card_id FROM equipment WHERE user_id = ?", (user_id,))
    equipped_cards = cursor.fetchall()

    total_atk, total_def = base_atk, base_def
    category_counts = {}

    for (card_id,) in equipped_cards:
        # 查詢卡片屬性
        cursor.execute("SELECT atk, def_ FROM cards WHERE id = ?", (card_id,))
        card = cursor.fetchone()
        if not card:
            continue

        card_atk, card_def = card

        # 查詢持有次數，計算加權
        cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
        count_data = cursor.fetchone()
        count = count_data[0] if count_data else 0

        multiplier = 1 + 0.04 * (2 ** (count - 1).bit_length() - 1)
        total_atk += int(card_atk * multiplier)
        total_def += int(card_def * multiplier)

        # 統計分類
        cursor.execute("SELECT category FROM card_categories WHERE card_id = ?", (card_id,))
        categories = [row[0] for row in cursor.fetchall()]
        for category in categories:
            category_counts[category] = category_counts.get(category, 0) + 1

    # 計算分類加成
    for count in category_counts.values():
        if count >= 3:
            total_atk += 10
            total_def += 10

    return total_atk, total_def

# 定義階級計算函數
def get_rank(level):
    rank_mapping = {
        (-float('inf'), -6): "習近平",
        (-6, -5): "中共同路人",
        (-5, -4): "柯文哲",
        (-4, -3): "黃國昌",
        (-3, -2): "小草",
        (-2, -1): "民眾黨?",
        (-1, 0): "國民黨?",
        (0, 1): "普通市民",
        (1, 2): "1450",
        (2, 3): "覺青",
        (3, 4): "青鳥",
        (4, 5): "民進黨側翼",
        (5, 8): "民進黨黨員",
        (8, float('inf')): "民進黨幹部",
    }
    return next(rank for (low, high), rank in rank_mapping.items() if low < level <= high)

# 更新使用者 EXP 和等級
def update_user_exp(user_id, exp_change, exp_change_2):
    try:
        # 查詢當前的 exp 和 level
        cursor.execute(
            'SELECT exp, exp_2, level FROM users WHERE id = ?',
            (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            print("用戶不存在，無法更新經驗值。")
            return {"level_up": False, "level_down": False, "new_level": None}

        # 處理可能的 None 值
        current_exp = user[0] if user[0] is not None else 0
        current_exp_2 = user[1] if user[1] is not None else 0
        current_level = user[2] if user[2] is not None else 1

        new_exp = current_exp + exp_change
        new_exp_2 = current_exp_2 + exp_change_2
        level_up = False
        level_down = False

        # 降級邏輯
        while new_exp < 0 and current_level > -6:
            current_level -= 1
            new_exp += 5
            level_down = True

        # 升級邏輯
        while new_exp >= 5:
            new_exp -= 5
            current_level += 1
            level_up = True

        # 更新 atk 和 def
        new_atk = 10 + (new_exp_2 // 30) * 2
        new_def = 5 + (new_exp_2 // 30) * 1

        # 更新數據庫
        cursor.execute('''
            UPDATE users
            SET exp = ?, exp_2 = ?, level = ?, atk = ?, def_ = ?
            WHERE id = ?
        ''', (new_exp, new_exp_2, current_level, new_atk, new_def, user_id))
        conn.commit()

        print(f"更新成功：User ID={user_id}, New Level={current_level}, New Exp={new_exp}, New Exp_2={new_exp_2}")

        # 返回訊息
        return {
            "level_up": level_up,
            "level_down": level_down,
            "new_level": current_level
        }

    except Exception as e:
        print(f"Error in updating user exp: {e}")
        return {"level_up": False, "level_down": False, "new_level": None}

# 顯示冷卻時間
def get_remaining_time(current_time, next_time):
    remaining_time = next_time - current_time
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

##############################################################
##############################################################
#######################_斜線指令集中區_########################
##############################################################
##############################################################

# 每日簽到
@bot.tree.command(name="daily", description="每日簽到")
async def daily(interaction: discord.Interaction):
    await handle_daily(source=interaction, is_interaction=True)

async def handle_daily(source, is_interaction: bool):
    # 根據調用方式獲取用戶和回應方法
    if is_interaction:
        user_id = source.user.id
        name = source.user.name
        response = source.response.send_message
    else:
        user_id = source.author.id
        name = source.author.name
        response = source.send

    now = datetime.utcnow()
    cooldown = timedelta(days=1)

    # 簽到邏輯
    cursor.execute('SELECT coins, last_checkin FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        last_checkin = datetime.fromisoformat(result[1]) if result[1] else None
        if last_checkin and now - last_checkin < cooldown:
            remaining_time = cooldown - (now - last_checkin)
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await response(
                f"{name}，你今天已經簽到過了\n冷卻時間為 {hours} 小時 {minutes} 分鐘 {seconds} 秒",
                ephemeral=is_interaction
            )
            return
        cursor.execute(
            'UPDATE users SET coins = coins + 20, last_checkin = ? WHERE id = ?',
            (now.isoformat(), user_id)
        )
    else:
        cursor.execute(
            'INSERT INTO users (id, coins, last_checkin, exp, exp_2, atk, def_) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, 20, now.isoformat(), 0, 0, 10, 5)
        )

    conn.commit()

    # 更新經驗和等級
    level_up = update_user_exp(user_id, 0, 5)

    # 回應用戶
    if level_up:
        await response(f"{name} 獲得了 20 coin！\n積分+5！\n註冊成功！")
    else:
        await response(f"{name} 獲得了 20 coin！\n積分+5！")

# 為已存在的卡片添加圖片    
@bot.tree.command(name="add_cardurl", description="為已存在的卡片添加更多圖片")
@app_commands.describe(
    name="卡片名稱(英文)",
    urls="想要添加的圖片的 URL (可以一次上傳多個，使用,分隔 URL) 或 Imgur 相簿 URL",
    localdata="本地圖片文件或資料夾的路徑"
)
async def add_cardurl(interaction: Interaction, name: str, urls: str = '', localdata: str = ''):
    try:
        # 延遲回應
        await interaction.response.defer()

        # 確認卡片名稱是否存在
        cursor.execute('SELECT id, album_id FROM cards WHERE name_1 = ?', (name,))
        result = cursor.fetchone()
        if not result:
            await interaction.followup.send("找不到該名稱的卡片，請檢查名稱是否正確")
            return

        card_id, album_id = result
        url_list = []

        # 如果提供的是 Imgur 相簿 URL
        if "imgur.com/a/" in urls:
            try:
                album_images = get_imgur_album_images(urls)
                url_list.extend(album_images)
            except Exception as e:
                await interaction.followup.send(f"獲取相簿圖片失敗：{e}")
                return

        # 處理圖片 URL
        if urls:
            url_list.extend([convert_imgur_url(url.strip()) for url in urls.split(',')])  # 處理普通圖片 URL

        # 處理本地圖片或資料夾
        if localdata:
            local_path = Path(localdata)
            if not local_path.exists():
                await interaction.followup.send(f"找不到本地路徑：{localdata}")
                return

            # 如果是文件，直接上傳
            if local_path.is_file():
                try:
                    # 如果卡片沒有相簿，創建一個
                    if not album_id:
                        album = imgur.create_album(title=name)
                        album_id = album.id
                        cursor.execute('UPDATE cards SET album_id = ? WHERE id = ?', (album_id, card_id))

                    # 上傳圖片到相簿
                    imgur_url = upload_to_imgur(str(local_path), album_id=album_id)
                    url_list.append(imgur_url)
                except Exception as e:
                    await interaction.followup.send(f"上傳本地圖片到 Imgur 失敗：{e}")
                    return

            # 如果是資料夾，遍歷資料夾內所有圖片文件並上傳
            elif local_path.is_dir():
                image_files = list(local_path.glob("*.png")) + list(local_path.glob("*.jpg")) + list(local_path.glob("*.jpeg"))
                if not image_files:
                    await interaction.followup.send(f"資料夾中沒有找到圖片文件")
                    return

                for image_file in image_files:
                    try:
                        if not album_id:
                            album = imgur.create_album(title=name)
                            album_id = album.id
                            cursor.execute('UPDATE cards SET album_id = ? WHERE id = ?', (album_id, card_id))

                        imgur_url = upload_to_imgur(str(image_file), album_id=album_id)
                        url_list.append(imgur_url)
                    except Exception as e:
                        await interaction.followup.send(f"上傳本地圖片 {image_file.name} 到 Imgur 失敗：{e}")
                        continue

        # 若沒有圖片 URL，回傳錯誤
        if not url_list:
            await interaction.followup.send("未提供有效的圖片 URL 或本地圖片文件路徑")
            return

        # 插入圖片 URL 到 card_urls 表格
        for url in url_list:
            if cursor.execute('SELECT 1 FROM card_urls WHERE card_id = ? AND url = ?', (card_id, url)).fetchone():
                continue  # 跳過重複 URL
            elif url == f"https://i.imgur.com/{album_id}.jpg":
                continue  # 跳過包含 album_hash 的 URL
            else:
                cursor.execute(
                    'INSERT INTO card_urls (card_id, url) VALUES (?, ?)',
                    (card_id, url)
                )

        conn.commit()
        await interaction.followup.send(f"成功為卡片**'{name}'**添加圖片!")
    except sqlite3.Error as e:
        await interaction.followup.send(f"添加 URL 時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.followup.send(f"發生未知錯誤：{e}")

# 為已存在的卡片添加瑟圖
@bot.tree.command(name="add_cardurl_r18", description="為已存在的卡片添加更多**瑟圖**")
@app_commands.describe(
    name="卡片名稱(英文)",
    urls="想要添加的圖片的 URL (可以一次上傳多個，使用,分隔 URL) 或 Imgur 相簿 URL",
    localdata="本地圖片文件或資料夾的路徑"
)
async def add_cardurl_r18(interaction: Interaction, name: str, urls: str = '', localdata: str = ''):
    try:
        # 延遲回應
        await interaction.response.defer()

        # 確認卡片名稱是否存在
        cursor.execute('SELECT id, album_id FROM cards WHERE name_1 = ?', (name,))
        result = cursor.fetchone()
        if not result:
            await interaction.followup.send("找不到該名稱的卡片，請檢查名稱是否正確")
            return

        card_id, album_id = result
        url_list = []

        # 如果提供的是 Imgur 相簿 URL
        if "imgur.com/a/" in urls:
            try:
                album_images = get_imgur_album_images(urls)
                url_list.extend(album_images)
            except Exception as e:
                await interaction.followup.send(f"獲取相簿圖片失敗：{e}")
                return

        # 處理圖片 URL
        if urls:
            url_list.extend([convert_imgur_url(url.strip()) for url in urls.split(',')])  # 處理普通圖片 URL

        # 處理本地圖片或資料夾
        if localdata:
            local_path = Path(localdata)
            if not local_path.exists():
                await interaction.followup.send(f"找不到本地路徑：{localdata}")
                return

            # 如果是文件，直接上傳
            if local_path.is_file():
                try:
                    # 如果卡片沒有相簿，創建一個
                    if not album_id:
                        album = imgur.create_album(title=name)
                        album_id = album.id
                        cursor.execute('UPDATE cards SET album_id = ? WHERE id = ?', (album_id, card_id))

                    # 上傳圖片到相簿
                    imgur_url = upload_to_imgur_r18(str(local_path), album_id=album_id, description="r18")
                    url_list.append(imgur_url)
                except Exception as e:
                    await interaction.followup.send(f"上傳本地圖片到 Imgur 失敗：{e}")
                    return

            # 如果是資料夾，遍歷資料夾內所有圖片文件並上傳
            elif local_path.is_dir():
                image_files = list(local_path.glob("*.png")) + list(local_path.glob("*.jpg")) + list(local_path.glob("*.jpeg"))
                if not image_files:
                    await interaction.followup.send(f"資料夾中沒有找到圖片文件")
                    return

                for image_file in image_files:
                    try:
                        if not album_id:
                            album = imgur.create_album(title=name)
                            album_id = album.id
                            cursor.execute('UPDATE cards SET album_id = ? WHERE id = ?', (album_id, card_id))

                        imgur_url = upload_to_imgur_r18(str(image_file), album_id=album_id, description="r18")
                        url_list.append(imgur_url)
                    except Exception as e:
                        await interaction.followup.send(f"上傳本地圖片 {image_file.name} 到 Imgur 失敗：{e}")
                        continue

        # 若沒有圖片 URL，回傳錯誤
        if not url_list:
            await interaction.followup.send("未提供有效的圖片 URL 或本地圖片文件路徑")
            return

        # 插入圖片 URL 到 card_urls_2 表格
        for url in url_list:
            if cursor.execute('SELECT 1 FROM card_urls_2 WHERE card_id = ? AND url = ?', (card_id, url)).fetchone():
                continue  # 跳過重複 URL
            elif url == f"https://i.imgur.com/{album_id}.jpg":
                continue  # 跳過包含 album_hash 的 URL
            else:
                cursor.execute(
                    'INSERT INTO card_urls_2 (card_id, url) VALUES (?, ?)',
                    (card_id, url)
                )

        conn.commit()
        await interaction.followup.send(f"成功為卡片**'{name}'**添加圖片!")
    except sqlite3.Error as e:
        await interaction.followup.send(f"添加 URL 時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.followup.send(f"發生未知錯誤：{e}")

# 同步分類
@bot.tree.command(name="category", description="同步分類")
@app_commands.describe(
    main_name="主要分類名稱",
    another_name="要同步的另一分類名稱"
)
async def categorie(interaction: discord.Interaction, main_name: str, another_name: str):
    try:
        # 檢查是否已存在該同步關係
        cursor.execute('''
            SELECT 1 FROM category_2 
            WHERE main_name = ? AND another_name = ?
        ''', (main_name, another_name))
        if cursor.fetchone():
            await interaction.response.send_message(f"分類 '{main_name}' 與 '{another_name}' 已存在同步關係，無需重複添加。")
            return

        # 檢查 main_name 是否已存在於 category_2 或 card_categories
        cursor.execute('SELECT DISTINCT main_name FROM category_2 WHERE main_name = ?', (main_name,))
        main_exists = cursor.fetchone()

        cursor.execute('SELECT DISTINCT category FROM cards WHERE category = ?', (main_name,))
        main_category_exists = cursor.fetchone()

        if not main_exists and not main_category_exists:
            await interaction.response.send_message(f"主要分類 '{main_name}' 不存在，請先創建該分類。")
            return

        # 插入同步關係
        cursor.execute(
            'INSERT INTO category_2 (main_name, another_name) VALUES (?, ?)',
            (main_name, another_name)
        )
        conn.commit()

        await interaction.response.send_message(f"成功同步分類 '{main_name}' 與 '{another_name}'。")
    except sqlite3.IntegrityError:
        await interaction.response.send_message(f"分類 '{main_name}' 與 '{another_name}' 已存在同步關係，無需重複添加。")
    except sqlite3.Error as e:
        await interaction.response.send_message(f"同步分類時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤：{e}")

# 查詢單張卡片資訊
@bot.tree.command(name="search_card", description="按照名稱查詢卡片資訊 (ඞsc)")
@app_commands.describe(name="卡片名稱 (支援中日英語)")
async def search_card(interaction: discord.Interaction, name: str):
    try:
        # 查詢卡片資料，匹配 name_1、name_2 或 name_3
        cursor.execute('''
            SELECT cards.id, cards.name_1, cards.name_2, cards.name_3, cards.atk, cards.def_, card_urls.url, card_urls.url_number, cards.category
            FROM cards
            JOIN card_urls ON cards.id = card_urls.card_id
            WHERE cards.name_1 LIKE ? OR cards.name_2 LIKE ? OR cards.name_3 LIKE ?
            ORDER BY card_urls.url_number
        ''', (f'%{name}%', f'%{name}%', f'%{name}%'))
        results = cursor.fetchall()

        if not results:
            await interaction.response.send_message("找不到符合條件的卡片")
            return

        # 儲存同一卡片的所有URL
        card_urls_map = {}
        for row in results:
            card_id, name_1, name_2, name_3, atk, def_, url, url_number, category = row
            if card_id not in card_urls_map:
                card_urls_map[card_id] = {
                    'name_1': name_1, 'name_2': name_2, 'name_3': name_3,
                    'atk': atk, 'def_': def_, 'category': category, 'urls': []
                }
            card_urls_map[card_id]['urls'].append(url)

        # 如果匹配多個卡片，顯示清單
        if len(card_urls_map) > 1:
            mapping_list = "\n".join(
                f"- {card_info['name_1']} / {card_info['name_2']} / {card_info['name_3']}" for card_info in card_urls_map.values()
            )
            await interaction.response.send_message(
                f"找到以下多個卡片名稱匹配 '{name}'，請確認並選擇一個:\n{mapping_list}"
            )
            return

        # 查詢用戶持有的卡片資料，並獲取 url_number
        cursor.execute('''
            SELECT url_number FROM user_cards 
            WHERE user_id = ? AND card_id IN (
                SELECT id FROM cards WHERE name_1 LIKE ? OR name_2 LIKE ? OR name_3 LIKE ?
            )
        ''', (interaction.user.id, f'%{name}%', f'%{name}%', f'%{name}%'))
        user_card_data = cursor.fetchone()

        # 如果用戶沒有卡片或未設置 url_number，默認從第 1 頁開始
        if user_card_data:
            initial_page = max(user_card_data[0] - 1, 0)  # url_number 轉換為索引
        else:
            initial_page = 0  # 默認從第 1 頁開始

        class UrlNavigation(discord.ui.View):
            def __init__(self, initial_page):
                super().__init__()
                self.current_index = initial_page
                self.results = results

            async def update_embed(self, index: int):
                card_id, card_name_1, card_name_2, card_name_3, atk, def_, url, url_number, category = self.results[index]

                embed = discord.Embed(
                    title=card_name_1,
                    description=f"**{category}**\n**{card_name_2}**\n**{card_name_3}**\nATK: {atk} | DEF: {def_}"
                )
                embed.set_image(url=url)
                embed.set_footer(text=f"第 {index + 1} 張，共 {len(self.results)} 張")
                return embed

            @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary)
            async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current_index = (self.current_index - 1) % len(self.results)
                embed = await self.update_embed(self.current_index)
                await interaction.response.edit_message(embed=embed, view=self)

            @discord.ui.button(label="▶️", style=discord.ButtonStyle.primary)
            async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current_index = (self.current_index + 1) % len(self.results)
                embed = await self.update_embed(self.current_index)
                await interaction.response.edit_message(embed=embed, view=self)

        navigation_view = UrlNavigation(initial_page)
        embed = await navigation_view.update_embed(initial_page)
        await interaction.response.send_message(embed=embed, view=navigation_view)

    except sqlite3.Error as e:
        await interaction.response.send_message(f"查詢時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤：{e}")

# 查詢單張卡片的瑟圖
@bot.tree.command(name="search_card_r18", description="按卡片名稱查詢卡片的**瑟圖**")
@app_commands.describe(name="卡片名稱 (英文))")
async def search_card_r18(interaction: discord.Interaction, name: str):
    try:
        # 查詢符合條件的卡片及其所有 URL
        cursor.execute(''' 
            SELECT cards.id, cards.name_1, cards.atk, cards.def_, card_urls_2.url
            FROM cards
            JOIN card_urls_2 ON cards.id = card_urls_2.card_id
            WHERE cards.name LIKE ?
        ''', (f'%{name}%',))
        results = cursor.fetchall()

        if not results:
            await interaction.response.send_message("找不到符合條件的卡片")
            return

        # 提取所有 card_id 並去重
        card_ids = list({row[0] for row in results})

        if len(card_ids) > 2:
            # 如果查詢結果超過 2 種 card_id，顯示所有卡片名稱的清單
            card_names = sorted({row[1] for row in results})  # 提取並按字母排序卡片名稱
            card_list = "\n".join(f"- {name}" for name in card_names)

            embed = discord.Embed(
                title="查詢結果",
                description=f"找到多於 2 種卡片名稱（按字母排序）：\n{card_list}",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
            return

        class UrlNavigation(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.current_index = 0
                self.results = results

            async def update_embed(self, index: int):
                # 取得當前結果
                card_id, card_name, atk, def_, url = self.results[index]

                # 查詢該卡片的所有分類
                cursor.execute('SELECT category FROM cards WHERE card_id = ?', (card_id,))
                categories = [row[0] for row in cursor.fetchall()]
                category_str = ', '.join(categories) if categories else '無分類'

                # 建立 embed
                embed = discord.Embed(
                    title=card_name,
                    description=f"**{category_str}**\nATK: {atk}\nDEF: {def_}"
                )
                embed.set_image(url=url)  # 顯示對應的 URL
                embed.set_footer(text=f"第 {index + 1} 張，共 {len(self.results)} 張")
                return embed

            @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary)
            async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current_index = (self.current_index - 1) % len(self.results)
                embed = await self.update_embed(self.current_index)
                await interaction.response.edit_message(embed=embed, view=self)

            @discord.ui.button(label="▶️", style=discord.ButtonStyle.primary)
            async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current_index = (self.current_index + 1) % len(self.results)
                embed = await self.update_embed(self.current_index)
                await interaction.response.edit_message(embed=embed, view=self)

        # 初始化視圖，顯示第一張圖片
        navigation_view = UrlNavigation()
        embed = await navigation_view.update_embed(0)
        await interaction.response.send_message(embed=embed, view=navigation_view)

    except sqlite3.Error as e:
        await interaction.response.send_message(f"查詢時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤：{e}")

# 新增 /sca 指令，專門查詢分類
@bot.tree.command(name="search_card_by_category", description="按照分類查詢卡片資訊 (ඞsca)")
@app_commands.describe(category="分類 (可以使用部分名稱查詢)")
async def search_card_by_category(interaction: discord.Interaction, category: str):
    try:
        # 優先查詢分類對應的完全匹配的主分類
        cursor.execute('''
            SELECT category FROM cards WHERE category = ?
        ''', (category,))
        exact_match = cursor.fetchone()

        if exact_match:
            category = exact_match[0]
        else:
            # 如果沒有完全匹配，進行模糊匹配
            cursor.execute('''
                SELECT main_name FROM category_2 WHERE another_name LIKE ?
            ''', (f'%{category}%',))
            category_mappings = cursor.fetchall()

            # 去重處理，確保不列出重複的主分類
            unique_categories = list({row[0] for row in category_mappings})

            # 如果 another_name 沒有對應，直接檢查 cards 表
            if not unique_categories:
                cursor.execute('''
                    SELECT DISTINCT category FROM cards WHERE category LIKE ?
                ''', (f'%{category}%',))
                category_mappings = cursor.fetchall()

                # 去重處理
                unique_categories = list({row[0] for row in category_mappings})

            # 如果對應到多個主分類，列出所有匹配
            if len(unique_categories) > 1:
                mapping_list = "\n".join(f"- {main_name}" for main_name in unique_categories)
                await interaction.response.send_message(
                    f"**'{category}'** 對應到以下多個主分類：\n{mapping_list}"
                )
                return

            # 如果對應到一個主分類，使用該主分類作為查詢條件
            if unique_categories:
                category = unique_categories[0]
            else:
                await interaction.response.send_message("找不到對應的分類，請檢查輸入是否正確。")
                return

        # 搜尋符合分類的卡片及其第一張圖片和相簿 ID
        cursor.execute(''' 
        SELECT 
        cards.id, 
        cards.name_1, 
        cards.name_2, 
        cards.name_3, 
        cards.atk, 
        cards.def_, 
        cards.category, 
        COALESCE(user_cards.url_number, 1) AS url_number, 
        cards.album_id
        FROM cards
        LEFT JOIN user_cards ON user_cards.card_id = cards.id AND user_cards.user_id = ?
        WHERE cards.category LIKE ?
        ORDER BY cards.name_1 ASC
        ''', (interaction.user.id, f'%{category}%'))
        results = cursor.fetchall()

        if not results:
            await interaction.response.send_message("此分類下沒有卡片")
            return

        class CardNavigation(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.current_index = 0
                self.results = results

            async def update_embed(self, index: int):
                card_id, card_name_1, card_name_2, card_name_3, atk, def_, card_category, url_number, album_id = results[index]

                # 根據 user_cards 表的 url_number 查找卡片的對應圖片
                cursor.execute('SELECT url FROM card_urls WHERE card_id = ? AND url_number = ?', (card_id, url_number))
                card_url = cursor.fetchone()

                if not card_url:
                    cursor.execute("SELECT url FROM card_urls WHERE card_id = ? LIMIT 1", (card_id,))
                    card_url = cursor.fetchone()

                url = card_url[0] if card_url else None

                # 確保 URL 有效
                if not url or not url.startswith("http"):
                    url = "https://example.com/default_image.png"  # 預設圖片

                # 顯示卡片信息
                embed = discord.Embed(
                    title=card_name_1,
                    description=f"**{card_category}\n{card_name_2}\n{card_name_3}**\nATK: {atk}\nDEF: {def_}\n"
                )
                embed.set_footer(text=f"第 {index + 1} 張，共 {len(self.results)} 張")
                embed.set_image(url=url)

                return embed

            @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary)
            async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current_index = (self.current_index - 1) % len(results)
                embed = await self.update_embed(self.current_index)
                await interaction.response.edit_message(embed=embed, view=self)

            @discord.ui.button(label="▶️", style=discord.ButtonStyle.primary)
            async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current_index = (self.current_index + 1) % len(results)
                embed = await self.update_embed(self.current_index)
                await interaction.response.edit_message(embed=embed, view=self)

        navigation_view = CardNavigation()
        embed = await navigation_view.update_embed(0)
        await interaction.response.send_message(embed=embed, view=navigation_view)

    except sqlite3.Error as e:
        await interaction.response.send_message(f"查詢時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤：{e}")

# 記錄用戶的上次抽卡時間和剩餘次數
user_gacha_data = {}
# 顯示抽到的卡片和相關能力值的模塊
async def show_gacha_result(interaction, card_name_1, card_name_2, card_name_3, category, selected_url, count, atk, defense, remaining_draws, gacha_limit):
    embed = discord.Embed(
        title=f"{interaction.user.name} 抽到了 {card_name_1}！",
        description=(
            f"**{category}**\n"
            f"**{card_name_2}**\n"
            f"**{card_name_3}**\n"
            f"累計持有數量：{count}\n"
            f"ATK: {atk} | DEF: {defense}\n"
            f"剩餘抽卡次數：{remaining_draws}/{gacha_limit}"
        ),
    )
    embed.set_image(url=selected_url)
    await interaction.response.send_message(embed=embed)
# 抽卡系統
@bot.tree.command(name="gacha", description="抽卡，斗肉! (ඞgacha)")
async def gacha(interaction: discord.Interaction):
    user_id = interaction.user.id
    current_time = datetime.utcnow()

    # 計算下一個整點時間
    next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    # 檢查用戶的積分，順便檢查用戶是否存在於資料庫中，並初始化用戶數據
    cursor.execute("SELECT exp_2 FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        cursor.execute("INSERT INTO users (id, level, exp, exp_2, coins, atk, def_) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (user_id, 1, 0, 0, 0, 10, 5))
        conn.commit()
        exp_2 = 0
    else:
        exp_2 = user_data[0]

    # 計算抽卡次數限制
    gacha_limit = 3 + (exp_2 // 30)

    # 初始化用戶的抽卡數據
    if user_id not in user_gacha_data:
        user_gacha_data[user_id] = {'last_gacha_time': current_time, 'remaining_draws': gacha_limit}

    user_gacha = user_gacha_data[user_id]

    # 刷新抽卡次數如果跨過下一個整點
    if current_time >= user_gacha['last_gacha_time'].replace(minute=0, second=0, microsecond=0) + timedelta(hours=1):
        user_gacha['last_gacha_time'] = current_time
        user_gacha['remaining_draws'] = gacha_limit

    # 如果抽卡次數用完，告知用戶剩餘時間
    if user_gacha['remaining_draws'] <= 0:
        hours, minutes, seconds = get_remaining_time(current_time, next_hour)
        await interaction.response.send_message(
            f"{interaction.user.name}，你目前沒有抽卡次數，請等待 {hours} 小時 {minutes} 分鐘 {seconds} 秒！"
        )
        return

    # 獲取所有卡片資料
    cursor.execute('SELECT id, name_1, name_2, name_3, atk, def_, category FROM cards')
    cards = cursor.fetchall()

    if not cards:
        await interaction.response.send_message("目前沒有可用的卡片！請先新增卡片！")
        return

    # 隨機抽取一張卡片
    selected_card = random.choice(cards)
    card_id, name_1, name_2, name_3, base_atk, base_def, category = selected_card

    # 獲取 URL 編號和對應的 URL
    cursor.execute('SELECT url_number FROM user_cards WHERE user_id = ? AND card_id = ?', (user_id, card_id))
    url_number_data = cursor.fetchone()
    url_number = url_number_data[0] if url_number_data else 1

    cursor.execute('SELECT url FROM card_urls WHERE card_id = ? AND url_number = ?', (card_id, url_number))
    card_url = cursor.fetchone()

    if not card_url:
        cursor.execute("SELECT url FROM card_urls WHERE card_id = ? LIMIT 1", (card_id,))
        card_url = cursor.fetchone()

    selected_url = card_url[0] if card_url else None

    # 更新用戶持有的卡片數量
    cursor.execute(''' 
    INSERT INTO user_cards (user_id, card_id, count) 
    VALUES (?, ?, 1) 
    ON CONFLICT(user_id, card_id) 
    DO UPDATE SET count = user_cards.count + 1 
    ''', (user_id, card_id))
    conn.commit()

    # 獲取最新持有數量並計算能力值加成
    cursor.execute('SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?', (user_id, card_id))
    result = cursor.fetchone()
    count = result[0] if result else 1

    multiplier = 1 + 0.04 * (2 ** (count - 1).bit_length() - 1)
    atk = int(base_atk * multiplier)
    defense = int(base_def * multiplier)

    # 減少用戶的剩餘抽卡次數
    user_gacha['remaining_draws'] -= 1

    # 顯示抽卡結果
    await show_gacha_result(
        interaction,
        name_1, name_2, name_3,
        category,
        selected_url,
        count,
        atk,
        defense,
        user_gacha['remaining_draws'],
        gacha_limit
    )

# 裝備卡片
@bot.tree.command(name="equip", description="裝備卡片")
@app_commands.describe(card_name="要裝備的卡片名稱(英文)")
async def equip_card(interaction: discord.Interaction, card_name: str):
    user_id = interaction.user.id

    # 確認用戶是否存在
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        await interaction.response.send_message("用戶未註冊，請先使用/daily", ephemeral=True)
        return

    # 根據卡片名稱查找卡片
    cursor.execute("SELECT id, atk, def_ FROM cards WHERE name_1 = ?", (card_name,))
    card = cursor.fetchone()
    if not card:
        await interaction.response.send_message("找不到此卡片名稱", ephemeral=True)
        return

    card_id, card_atk, card_def = card

    # 確認用戶是否持有該卡片
    cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
    user_card = cursor.fetchone()
    if not user_card or user_card[0] <= 0:
        await interaction.response.send_message("你未持有該卡片，無法裝備", ephemeral=True)
        return

    card_count = user_card[0]

    # 檢查該卡片是否已經裝備
    cursor.execute("SELECT card_id FROM equipment WHERE user_id = ?", (user_id,))
    equipped_cards_ids = [row[0] for row in cursor.fetchall()]
    if card_id in equipped_cards_ids:
        await interaction.response.send_message("該卡片已經裝備，無需重複操作", ephemeral=True)
        return

    # 計算加權值
    multiplier = 1 + 0.04 * (2 ** (card_count - 1).bit_length() - 1)
    weighted_atk = int(card_atk * multiplier)
    weighted_def = int(card_def * multiplier)

    # 查詢已裝備的卡片數量
    cursor.execute("SELECT COUNT(*) FROM equipment WHERE user_id = ?", (user_id,))
    equipped_count = cursor.fetchone()[0]

    if equipped_count >= 3:
        # 顯示模塊，讓用戶選擇要替換的卡片
        cursor.execute('''SELECT e.card_id, c.name_1, c.atk, c.def_, uc.count
                           FROM equipment e
                           JOIN cards c ON e.card_id = c.id
                           JOIN user_cards uc ON e.card_id = uc.card_id
                           WHERE e.user_id = ?''', (user_id,))
        equipped_cards = cursor.fetchall()

        embed = discord.Embed(title="選擇要替換的卡片")
        embed.add_field(
            name="想要裝備的卡片",
            value=f"{card_name} (ATK: {weighted_atk}, DEF: {weighted_def}, 數量: {card_count})",
            inline=False,
        )

        card_details = ""
        # 根據 count 計算加權的 atk 和 def_
        for i, (equip_card_id, equip_card_name, equip_atk, equip_def, equip_count) in enumerate(equipped_cards):
            equip_multiplier = 1 + 0.04 * (2 ** (equip_count - 1).bit_length() - 1)
            equip_weighted_atk = int(equip_atk * equip_multiplier)
            equip_weighted_def = int(equip_def * equip_multiplier)

            card_details += (
                f"{i + 1}. {equip_card_name} - ATK: {equip_weighted_atk}, DEF: {equip_weighted_def}, 數量: {equip_count}\n"
            )

        embed.add_field(name="目前裝備卡片", value=card_details)

        # 使用 View 來包裝按鈕
        view = discord.ui.View()

        for i, (equip_card_id, equip_card_name, _, _, _) in enumerate(equipped_cards):
            button = discord.ui.Button(
                label=f"卡片 {i + 1}", custom_id=f"equip_card_{equip_card_id}_{card_id}_{card_name}"
            )
            view.add_item(button)

        await interaction.response.send_message(embed=embed, view=view)
        return

    # 裝備新卡片
    cursor.execute("INSERT INTO equipment (user_id, card_id) VALUES (?, ?)", (user_id, card_id))
    conn.commit()
    await interaction.response.send_message(f"成功裝備卡片 {card_name}！")
# 當按鈕被按下時處理替換邏輯
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component and interaction.data['custom_id'].startswith("equip_card_"):
        user_id = interaction.user.id

        # 解析 custom_id，獲取被選中的卡片的 card_id 和 card_name
        try:
            card_id_to_remove, new_card_id, new_card_name = interaction.data['custom_id'].split("_")[2:]
            card_id_to_remove = int(card_id_to_remove)
            new_card_id = int(new_card_id)
        except ValueError:
            await interaction.response.send_message("參數解析錯誤", ephemeral=True)
            return

        # 查詢該卡片是否已經裝備
        cursor.execute('''SELECT * FROM equipment WHERE user_id = ? AND card_id = ?''', (user_id, card_id_to_remove))
        if not cursor.fetchone():
            await interaction.response.send_message("該卡片並未裝備，替換失敗", ephemeral=True)
            return

        # 刪除裝備的卡片
        cursor.execute("DELETE FROM equipment WHERE user_id = ? AND card_id = ?", (user_id, card_id_to_remove))
        conn.commit()

        # 將新卡片插入裝備表
        cursor.execute("INSERT INTO equipment (user_id, card_id) VALUES (?, ?)", (user_id, new_card_id))
        conn.commit()

        # 收起按鈕
        await interaction.message.edit(view=None)

        await interaction.response.send_message(f"成功裝備卡片**{new_card_name}**！", ephemeral=True)

# 查看擁有的卡片
@bot.tree.command(name="cards", description="查看已擁有的卡片 (ඞcards)")
async def cards(interaction: discord.Interaction):
    user_id = interaction.user.id
    cursor.execute(''' 
        SELECT 
            user_cards.card_id, 
            user_cards.count, 
            user_cards.url_number, 
            cards.name_1, 
            cards.name_2, 
            cards.name_3, 
            cards.atk, 
            cards.def_, 
            cards.category
        FROM user_cards
        JOIN cards ON user_cards.card_id = cards.id
        WHERE user_cards.user_id = ?
        GROUP BY user_cards.card_id
    ''', (user_id,))
    records = cursor.fetchall()

    if not records:
        await interaction.response.send_message(f"{interaction.user.name}，你的庫存中沒有卡片！")
        return

    class CardNavigation(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.current_index = 0
            self.records = records

        async def update_embed(self, index: int):
            card_id, count, url_number, card_name_1, card_name_2, card_name_3, base_atk, base_def, category = records[index]

            # 根據 url_number 獲取對應的 URL
            cursor.execute("SELECT url FROM card_urls WHERE card_id = ? AND url_number = ?", (card_id, url_number))
            result = cursor.fetchone()
            selected_url = result[0] if result else None

            if selected_url is None:
                # 若找不到對應 URL，使用第一張圖片
                cursor.execute("SELECT url FROM card_urls WHERE card_id = ? ORDER BY url_number LIMIT 1", (card_id,))
                selected_url = cursor.fetchone()[0]

            # 計算最終的 ATK 和 DEF
            multiplier = 1 + 0.04 * (2 ** (count - 1).bit_length() - 1)
            final_atk = int(base_atk * multiplier)
            final_def = int(base_def * multiplier)

            embed = discord.Embed(
                title=f"**{card_name_1}**",
                description=f"**{category or '無分類'}\n{card_name_2}\n{card_name_3}**\n持有數：{count}\nATK: {final_atk}\nDEF: {final_def}"
            )
            if selected_url:
                embed.set_footer(text=f"第 {index + 1} 張，共 {len(self.records)} 張")
                embed.set_image(url=selected_url)
            return embed

        @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary)
        async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.current_index = (self.current_index - 1) % len(records)
            embed = await self.update_embed(self.current_index)
            await interaction.response.edit_message(embed=embed, view=self)

        @discord.ui.button(label="▶️", style=discord.ButtonStyle.primary)
        async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.current_index = (self.current_index + 1) % len(records)
            embed = await self.update_embed(self.current_index)
            await interaction.response.edit_message(embed=embed, view=self)

    navigation_view = CardNavigation()
    embed = await navigation_view.update_embed(0)
    await interaction.response.send_message(embed=embed, view=navigation_view)

# 查看個人檔案
@bot.tree.command(name="profile", description="查看個人資料")
async def profile(interaction: discord.Interaction):
    user_id = interaction.user.id

    try:
        # 查詢用戶基本資料
        cursor.execute("SELECT level, exp, exp_2, atk, def_, coins FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            await interaction.response.send_message("用戶未註冊，請先使用**/daily**", ephemeral=True)
            return

        level, exp, exp_2, base_atk, base_def, coins = user_data

        # 獲取階級
        rank = get_rank(level)

        # 查詢用戶裝備的卡片
        cursor.execute("SELECT card_id FROM equipment WHERE user_id = ?", (user_id,))
        equipped_cards = cursor.fetchall()

        if not equipped_cards:
            embed = discord.Embed(title=f"{interaction.user.display_name} 的個人資料")
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.add_field(name="等級", value=f"{level} ({rank})", inline=True)  # 顯示階級
            embed.add_field(name="台灣價值", value=str(exp), inline=True)
            embed.add_field(name="Coins", value=str(coins), inline=True)
            await interaction.response.send_message(embed=embed)
            return

        total_atk, total_def = base_atk, base_def
        equipped_card_details = []
        category_counts = {}

        for (card_id,) in equipped_cards:
            # 查詢卡片屬性
            cursor.execute("SELECT name_1, atk, def_ FROM cards WHERE id = ?", (card_id,))
            card = cursor.fetchone()

            if not card:
                continue

            card_name, card_atk, card_def = card

            # 查詢用戶持有卡片的次數
            cursor.execute("SELECT count, url_number FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
            user_card_data = cursor.fetchone()
            count = user_card_data[0] if user_card_data else 0
            url_number = user_card_data[1] if user_card_data else 1  # 預設為 1

            # 計算加權
            multiplier = 1 + 0.04 * (2 ** (count - 1).bit_length() - 1)
            weighted_atk = int(card_atk * multiplier)
            weighted_def = int(card_def * multiplier)

            total_atk += weighted_atk
            total_def += weighted_def

            # 查詢所有 URL
            cursor.execute("SELECT url_number FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
            url_number_data = cursor.fetchone()
            url_number = url_number_data[0] if url_number_data else 1  # 預設 url_number 為 1

            # 根據 url_number 選擇 URL
            cursor.execute("SELECT url FROM card_urls WHERE card_id = ? AND url_number = ?", (card_id, url_number))
            result = cursor.fetchone()

            if result:
                selected_url = result[0]  # 如果找到對應的 URL，使用它

            # 查詢卡片分類
            cursor.execute("SELECT category FROM cards WHERE id = ?", (card_id,))
            categories = [row[0] for row in cursor.fetchall()]
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1

            category_str = ', '.join(categories) if categories else "無分類"
            equipped_card_details.append((card_name, selected_url, category_str))

        # 計算額外加成
        extra_atk, extra_def = 0, 0
        for category, count in category_counts.items():
            if count >= 3:
                extra_atk += 10
                extra_def += 10

        total_atk += extra_atk
        total_def += extra_def

        # 構建嵌入消息
        embed = discord.Embed(title=f"{interaction.user.display_name} 的個人資料")
        embed.add_field(name="等級", value=f"{level} ({rank})", inline=True)  # 顯示階級
        embed.add_field(name="台灣價值", value=str(exp), inline=True)
        embed.add_field(name="積分", value=str(exp_2), inline=True)
        embed.add_field(name="ATK", value=f"{base_atk} (自身) + {total_atk - base_atk - extra_atk} (卡片) + {extra_atk} (額外加成)", inline=False)
        embed.add_field(name="DEF", value=f"{base_def} (自身) + {total_def - base_def - extra_def} (卡片) + {extra_def} (額外加成)", inline=False)
        embed.add_field(name="Coins", value=str(coins), inline=True)

        # 設置頭像
        if interaction.user.avatar:
            embed.set_thumbnail(url=interaction.user.avatar.url)

        for card_name, selected_url, category_str in equipped_card_details:
            if selected_url:
                embed.add_field(name=f"裝備卡片: {card_name}", value=category_str, inline=False)
                embed.set_image(url=selected_url)

        await interaction.response.send_message(embed=embed)

    except sqlite3.Error as e:
        await interaction.response.send_message(f"資料庫錯誤: {e}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤: {e}", ephemeral=True)

# 清除"自己"的所有紀錄
@bot.tree.command(name="deleterecord", description="清除**自己**的所有記錄")
async def deleterecord(interaction: discord.Interaction):
    user_id = interaction.user.id

    try:
        # 檢查是否存在於 users 表
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            await interaction.response.send_message("❌您尚未註冊，無需清除記錄❌", ephemeral=True)
            return

        # 確認操作
        await interaction.response.send_message(
            "⚠️確認要刪除所有記錄嗎？此操作無法復原！請在30秒內回覆**confirm**或忽略⚠️",
            ephemeral=True
        )

        def check(m):
            return (
                m.author == interaction.user and 
                m.channel == interaction.channel and 
                m.content.strip().lower() == "confirm"
            )

        try:
            confirmation = await bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await interaction.followup.send("操作超時，未收到確認。", ephemeral=True)
            return

        # 刪除相關記錄
        cursor.execute("DELETE FROM user_cards WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM equipment WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        await interaction.followup.send("✅所有記錄已成功刪除✅", ephemeral=True)

    except sqlite3.Error as e:
        await interaction.followup.send(f"資料庫錯誤: {e}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"發生未知錯誤: {e}", ephemeral=True)

# 刪除指定的卡片
@bot.tree.command(name="deletecard", description="刪除指定名稱的卡片")
@app_commands.describe(name="卡片名稱(英文)")
async def deletecard(interaction: discord.Interaction, name: str):
    try:
        # 查找資料庫中對應 name 的 id
        cursor.execute('SELECT id FROM cards WHERE name_1 = ? OR name_2 = ? OR name_3 = ?', (name, name, name))
        card = cursor.fetchone()

        if card:
            card_id = card[0]

            # 刪除所有與該卡片相關的紀錄
            cursor.execute('DELETE FROM user_cards WHERE card_id = ?', (card_id,))
            cursor.execute('DELETE FROM equipment WHERE card_id = ?', (card_id,))
            cursor.execute('DELETE FROM card_urls WHERE card_id = ?', (card_id,))
            cursor.execute('DELETE FROM card_urls_2 WHERE card_id = ?', (card_id,))
            
            # 刪除卡片資料
            cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
            conn.commit()  # 提交資料庫更改

            # 假設卡片檔案以 `id` 命名，並存儲在某個資料夾中
            file_path = f'cards/{card_id}.png'  # 假設卡片檔案是 .png 格式
            if os.path.exists(file_path):
                os.remove(file_path)  # 刪除檔案

            # 回應使用者
            await interaction.response.send_message(f"卡片 `{name}` 及其相關資料已成功刪除！", ephemeral=True)
        else:
            await interaction.response.send_message(f"找不到名為 `{name}` 的卡片！", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"發生錯誤: {e}", ephemeral=True)
        print(f"Error in /deletecard: {e}")

# 取消裝備所有卡片
@bot.tree.command(name="unequip", description="取消裝備所有卡片")
async def unequip(interaction: discord.Interaction):
    try:
        # 確認使用者存在於資料表
        user_id = interaction.user.id
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            await interaction.response.send_message("你尚未註冊為使用者，請先開始遊戲。")
            return

        # 刪除該用戶在 equipment 表中的所有裝備資料
        cursor.execute('DELETE FROM equipment WHERE user_id = ?', (user_id,))
        conn.commit()

        await interaction.response.send_message(f"{interaction.user.mention}，你已取消裝備所有卡片。")

    except sqlite3.Error as e:
        await interaction.response.send_message(f"取消裝備時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤：{e}")

# 每日挑戰次數限制
DAILY_LIMIT = 3
user_match_data = {}  # 用於追蹤用戶每日挑戰次數與上次刷新時間
# 對戰匹配系統
@bot.tree.command(name="match", description="匹配並挑戰其他玩家(全伺服器連動)")
async def match(interaction: discord.Interaction):
    user_id = interaction.user.id

    # 初始化用戶挑戰數據
    now = datetime.utcnow()
    user_data = user_match_data.get(user_id, {'last_reset': now, 'remaining': DAILY_LIMIT})

    # 每天早上 9 點刷新挑戰次數
    if now - user_data['last_reset'] >= timedelta(hours=24):
        next_reset = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now >= next_reset:
            next_reset += timedelta(days=1)
        user_data['last_reset'] = next_reset
        user_data['remaining'] = DAILY_LIMIT

    # 檢查剩餘挑戰次數
    if user_data['remaining'] <= 0:
        remaining_time = (user_data['last_reset'] - now).total_seconds()
        hours, minutes, seconds = int(remaining_time // 3600), int((remaining_time % 3600) // 60), int(remaining_time % 60)
        await interaction.response.send_message(
            f"你今天的挑戰次數已用完，將於 {hours} 小時 {minutes} 分鐘 {seconds} 秒後刷新次數。",
            ephemeral=True
        )
        return

    # 將用戶挑戰數據存回字典
    user_match_data[user_id] = user_data

    # 確認使用者存在於資料庫
    cursor.execute("SELECT id, level, atk, def_, exp_2 FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        await interaction.response.send_message("你尚未註冊，請先使用 /daily 註冊。")
        return

    user_level, user_atk, user_def, user_exp_2 = user[1:]

    # 隨機選擇一個已註冊且有裝備卡片的用戶
    cursor.execute('''
    SELECT u.id, u.level, u.atk, u.def_, u.exp_2, e.card_id
    FROM users u
    JOIN equipment e ON u.id = e.user_id
    WHERE u.id != ?
    GROUP BY u.id
    ORDER BY RANDOM()
    LIMIT 1
    ''', (user_id,))
    opponent = cursor.fetchone()

    if not opponent:
        await interaction.response.send_message("目前沒有其他玩家可以匹配！")
        return

    opponent_id, opponent_level, opponent_atk, opponent_def, opponent_exp_2, opponent_card_id = opponent

    # 根據 opponent_id 獲取對手的 username
    opponent_user = await bot.fetch_user(opponent_id)  # 獲取對手的 Discord 用戶資料
    opponent_username = opponent_user.display_name  # 使用 display_name

    # 獲取對手的裝備卡片資訊，包括對應的 url_number
    cursor.execute('''
    SELECT c.name_1, u.url
    FROM cards c
    JOIN card_urls u ON c.id = u.card_id
    JOIN user_cards uc ON c.id = uc.card_id
    WHERE c.id = ? AND uc.user_id = ? AND u.url_number = uc.url_number
    ''', (opponent_card_id, opponent_id))
    opponent_card = cursor.fetchone()

    # 如果未找到對應的 URL，使用第一張作為備選
    if not opponent_card:
        cursor.execute('''
        SELECT c.name_1, u.url
        FROM cards c
        JOIN card_urls u ON c.id = u.card_id
        WHERE c.id = ?
        ORDER BY u.url_number ASC
        LIMIT 1
        ''', (opponent_card_id,))
        opponent_card = cursor.fetchone()

    if not opponent_card:
        await interaction.response.send_message("對手的裝備卡片資訊不完整，無法匹配！")
        return

    opponent_card_name, opponent_card_url = opponent_card

    # 獲取自己的裝備卡片資訊
    cursor.execute('''
    SELECT c.name_1, u.url
    FROM cards c
    JOIN card_urls u ON c.id = u.card_id
    JOIN equipment e ON c.id = e.card_id
    WHERE e.user_id = ?
    ORDER BY e.id DESC
    LIMIT 1
    ''', (user_id,))
    user_card = cursor.fetchone()

    if not user_card:
        await interaction.response.send_message("你尚未裝備任何卡片，無法匹配！")
        return

    user_card_name, user_card_url = user_card

    # 構建初始嵌入
    opponent_total_atk, opponent_total_def = calculate_total_stats(opponent_id)
    user_total_atk, user_total_def = calculate_total_stats(user_id)
    embed = discord.Embed(title="匹配成功！", description=f"你的對手：{opponent_username}")
    embed.add_field(name="對戰績分", value=f"{opponent_exp_2}", inline=True)
    embed.add_field(name="ATK", value="???", inline=True)
    embed.add_field(name="DEF", value="???", inline=True)
    embed.add_field(name="裝備卡片", value=f"{opponent_card_name}", inline=False)
    embed.set_image(url=opponent_card_url)

    # 添加按鈕進行互動
    class MatchInteraction(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.attack_used = False
            self.defend_used = False

        async def disable_button(self, button: discord.ui.Button):
            """禁用按鈕，並更新視圖。"""
            button.disabled = True

        @discord.ui.button(label="攻擊", style=discord.ButtonStyle.danger)
        async def attack(self, interaction: discord.Interaction, button: discord.ui.Button):
            nonlocal user_exp_2, opponent_exp_2

            success_rate = user_total_atk / (opponent_total_def + user_total_atk)

            if random.random() <= success_rate:
                # 勝利邏輯
                user_exp_2 = max(0, user_exp_2 + 3)
                opponent_exp_2 = max(0, opponent_exp_2 - 1)

                def calculate_stats(exp_2):
                    return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                user_new_atk, user_new_def = calculate_stats(user_exp_2)
                opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                cursor.executemany(
                    "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                    [
                        (user_exp_2, user_new_atk, user_new_def, user_id),
                        (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                    ]
                )
                conn.commit()
                await self.show_victory(interaction, opponent_card_name, opponent_card_url)
                return

            # 攻擊失敗，判定是否觸發對方反擊
            counter_rate = opponent_total_def / (user_total_def + opponent_total_def)
            if random.random() <= counter_rate:
                # 對方成功觸發反擊
                counter_success_rate = opponent_total_def / (user_total_def + opponent_total_def)
                if random.random() <= counter_success_rate:
                    user_exp_2 = max(0, user_exp_2 - 2)
                    opponent_exp_2 = max(0, opponent_exp_2 + 3)

                    def calculate_stats(exp_2):
                        return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                    user_new_atk, user_new_def = calculate_stats(user_exp_2)
                    opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                    cursor.executemany(
                        "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                        [
                            (user_exp_2, user_new_atk, user_new_def, user_id),
                            (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                        ]
                    )
                    conn.commit()
                    await self.show_defeat_2(interaction, opponent_card_name, opponent_card_url)
                    return

            # 攻擊失敗但無反擊
            self.attack_used = True
            embed = discord.Embed(title="匹配成功！", description=f"你的對手：{opponent_username}")
            embed.add_field(name="對戰績分", value=f"{opponent_exp_2}", inline=True)
            embed.add_field(name="ATK", value="???", inline=True)
            embed.add_field(name="DEF", value="???", inline=True)
            embed.add_field(name="戰況", value="你的攻擊被格檔了，但對手的反擊無效！", inline=True)
            embed.add_field(name="裝備卡片", value=f"{opponent_card_name}", inline=False)
            embed.set_image(url=opponent_card_url)
            await self.disable_button(button)
            await interaction.response.edit_message(view=self)
            await self.check_buttons(interaction)

        @discord.ui.button(label="防禦", style=discord.ButtonStyle.primary)
        async def defend(self, interaction: discord.Interaction, button: discord.ui.Button):
            nonlocal user_exp_2, opponent_exp_2
            success_rate = opponent_total_atk / (user_total_def + opponent_total_atk)

            if random.random() > success_rate:
                # 敗北邏輯
                user_exp_2 = max(0, user_exp_2 - 2)
                opponent_exp_2 = max(0, opponent_exp_2 + 3)

                def calculate_stats(exp_2):
                    return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                user_new_atk, user_new_def = calculate_stats(user_exp_2)
                opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                cursor.executemany(
                    "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                    [
                        (user_exp_2, user_new_atk, user_new_def, user_id),
                        (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                    ]
                )
                conn.commit()
                await self.show_defeat(interaction, opponent_card_name, opponent_card_url)
                return

            # 防禦成功，判定是否觸發反擊
            counter_rate = user_total_def / (user_total_def + opponent_total_def)
            if random.random() <= counter_rate:
                counter_success_rate = user_total_def / (user_total_def + opponent_total_def)
                if random.random() <= counter_success_rate:
                    user_exp_2 = max(0, user_exp_2 + 3)
                    opponent_exp_2 = max(0, opponent_exp_2 - 1)

                    def calculate_stats(exp_2):
                        return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                    user_new_atk, user_new_def = calculate_stats(user_exp_2)
                    opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                    cursor.executemany(
                        "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                        [
                            (user_exp_2, user_new_atk, user_new_def, user_id),
                            (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                        ]
                    )
                    conn.commit()
                    await self.show_victory_2(interaction, opponent_card_name, opponent_card_url)
                    return

            # 防禦成功但無反擊
            self.attack_used = True
            embed = discord.Embed(title="匹配成功！", description=f"你的對手：{opponent_username}")
            embed.add_field(name="對戰績分", value=f"{opponent_exp_2}", inline=True)
            embed.add_field(name="ATK", value="???", inline=True)
            embed.add_field(name="DEF", value="???", inline=True)
            embed.add_field(name="戰況", value="防禦成功，但你的反擊無效！", inline=True)
            embed.add_field(name="裝備卡片", value=f"{opponent_card_name}", inline=False)
            embed.set_image(url=opponent_card_url)
            await self.disable_button(button)
            await interaction.response.edit_message(view=self)
            await self.check_buttons(interaction)

        async def check_buttons(self, interaction):
            # 檢查是否所有按鈕都被禁用
            if all(isinstance(child, discord.ui.Button) and child.disabled for child in self.children):
                # 將所有按鈕恢復為可用
                for child in self.children:
                    if isinstance(child, discord.ui.Button):
                        child.disabled = False

                # 更新訊息以恢復按鈕
                await interaction.message.edit(view=self)

        async def show_victory(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="WIN！", description=f"攻擊成功，對手的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

        async def show_victory_2(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="WIN！", description=f"反擊成功，對手的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

        async def show_defeat(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="LOSE...", description=f"防禦失敗，你的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

        async def show_defeat_2(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="LOSE...", description=f"對手反擊成功，你的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

    await interaction.response.send_message(embed=embed, view=MatchInteraction())

# 複製卡片指令
@bot.tree.command(name="clone", description="使用coins兌換卡片(aka.印卡)")
@app_commands.describe(
    card_name="卡片名稱(英文)",
    number="想兌換的數量"
)
async def clone(interaction: discord.Interaction, card_name: str, number: int):
    user_id = interaction.user.id

    try:
        # 檢查數量是否有效
        if number <= 0:
            await interaction.response.send_message("兌換數量必須為正整數", ephemeral=True)
            return

        # 確認用戶是否註冊
        cursor.execute("SELECT coins FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            await interaction.response.send_message("用戶未註冊，請先註冊 (/daily)", ephemeral=True)
            return

        user_coins = user_data[0]

        # 從 cards 表查詢 card_id
        cursor.execute("SELECT id FROM cards WHERE name_1 = ?", (card_name,))
        card_data = cursor.fetchone()

        if not card_data:
            await interaction.response.send_message("找不到指定名稱的卡片", ephemeral=True)
            return

        card_id = card_data[0]

        # 確認 coins 是否足夠
        cost = number * 2
        if user_coins < cost:
            await interaction.response.send_message(f"硬幣不足，需要 {cost} coins，但你只有 {user_coins} coins", ephemeral=True)
            return

        # 消耗硬幣
        cursor.execute("UPDATE users SET coins = coins - ? WHERE id = ?", (cost, user_id))

        # 更新 user_cards 的 count
        cursor.execute(
            '''
            INSERT INTO user_cards (user_id, card_id, count)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, card_id)
            DO UPDATE SET count = count + excluded.count
            ''',
            (user_id, card_id, number)
        )

        conn.commit()
        await interaction.response.send_message(f"成功兌換 {card_name}，你總共印了 {number} 卡片！")

    except sqlite3.Error as e:
        await interaction.response.send_message(f"兌換卡片時發生資料庫錯誤：{e}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤：{e}", ephemeral=True)

# 卡片交換系統 (沒測試過)
@bot.tree.command(name="trade", description="與其他人交換卡片")
@app_commands.describe(
    target_user="要交換卡片的對象",
    your_card_name="你提供的卡片名稱(英文)"
)
async def changecard(interaction: discord.Interaction, target_user: discord.Member, your_card_name: str):
    user_id = interaction.user.id
    target_user_id = target_user.id

    def get_card_details(user_id, card_name):
        """檢查用戶是否持有指定卡片"""
        cursor.execute("SELECT cards.id, user_cards.count FROM cards "
                       "JOIN user_cards ON cards.id = user_cards.card_id "
                       "WHERE user_cards.user_id = ? AND cards.name_1 = ?", (user_id, card_name))
        return cursor.fetchone()

    try:
        # 確認用戶是否註冊
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            await interaction.response.send_message("您尚未註冊，請先使用 /daily", ephemeral=True)
            return

        cursor.execute("SELECT id FROM users WHERE id = ?", (target_user_id,))
        if not cursor.fetchone():
            await interaction.response.send_message(f"{target_user.display_name} 尚未註冊，無法進行交易。", ephemeral=True)
            return

        # 檢查發起者的卡片
        your_card = get_card_details(user_id, your_card_name)
        if not your_card:
            await interaction.response.send_message("您的卡片名稱無效或您未持有該卡片，請檢查後再試。", ephemeral=True)
            return

        your_card_id, your_card_count = your_card

        # 提示對方選擇要交換的卡片
        await interaction.response.send_message(f"{target_user.display_name}，請選擇您希望交換的卡片名稱，並於30秒內回覆。")

        # 等待對方回覆
        def check(msg):
            return msg.author.id == target_user_id and msg.channel.id == interaction.channel.id

        try:
            target_card_message = await bot.wait_for("message", check=check, timeout=30.0)
            target_card_name = target_card_message.content.strip()

            # 檢查對方的卡片
            target_card = get_card_details(target_user_id, target_card_name)
            if not target_card:
                await interaction.followup.send(f"{target_user.display_name} 提供的卡片無效或未持有該卡片，終止交易。")
                return

            target_card_id, target_card_count = target_card

            # 確認交易
            await interaction.followup.send(
                f"{target_user.display_name}，是否確認用 **{target_card_name}** 與 "
                f"{interaction.user.display_name} 的 **{your_card_name}** 進行交換？（輸入 `confirm` 確認）"
            )

            try:
                confirm_message = await bot.wait_for("message", check=check, timeout=30.0)
                if confirm_message.content.strip().lower() != "confirm":
                    await interaction.followup.send(f"{target_user.display_name} 未確認交易，交易已取消。")
                    return
            except asyncio.TimeoutError:
                await interaction.followup.send("交易確認超時，交易已取消。")
                return

            # 執行交易
            cursor.execute("UPDATE user_cards SET count = count - 1 WHERE user_id = ? AND card_id = ?", (user_id, your_card_id))
            cursor.execute("UPDATE user_cards SET count = count + 1 WHERE user_id = ? AND card_id = ?", (target_user_id, your_card_id))
            cursor.execute("UPDATE user_cards SET count = count - 1 WHERE user_id = ? AND card_id = ?", (target_user_id, target_card_id))
            cursor.execute("UPDATE user_cards SET count = count + 1 WHERE user_id = ? AND card_id = ?", (user_id, target_card_id))

            # 移除數量為 0 的卡片
            cursor.execute("DELETE FROM user_cards WHERE user_id = ? AND card_id = ? AND count <= 0", (user_id, your_card_id))
            cursor.execute("DELETE FROM user_cards WHERE user_id = ? AND card_id = ? AND count <= 0", (target_user_id, target_card_id))
            conn.commit()

            # 成功訊息
            await interaction.followup.send(
                f"✅ 交易成功！\n{interaction.user.display_name} 提供的卡片：{your_card_name}\n"
                f"{target_user.display_name} 提供的卡片：{target_card_name}"
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("交易過程超時，交易已取消。", ephemeral=True)

    except sqlite3.Error as e:
        await interaction.response.send_message(f"交易過程中發生資料庫錯誤：{e}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"交易過程中發生未知錯誤：{e}", ephemeral=True)

# 更換第一張顯示的圖片
@bot.tree.command(name="change_url_number", description="更換卡片第1張顯示的圖片")
@app_commands.describe(
    card_name="卡片名稱(英文)",
    url_number="URL編號"
)
async def change_url_number(interaction: discord.Interaction, card_name: str, url_number: int):
    user_id = interaction.user.id

    try:
        # 確認用戶是否註冊
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            await interaction.response.send_message("您尚未註冊，請先使用 /daily", ephemeral=True)
            return

        # 確認卡片是否存在
        cursor.execute("SELECT id FROM cards WHERE name_1 = ?", (card_name,))
        card = cursor.fetchone()

        if not card:
            await interaction.response.send_message("卡片名稱無效", ephemeral=True)
            return

        card_id = card[0]

        # 檢查輸入的 url_number 是否有效
        cursor.execute("SELECT COUNT(*) FROM card_urls WHERE card_id = ?", (card_id,))
        url_count = cursor.fetchone()[0]

        if url_number < 0 or url_number > url_count:
            await interaction.response.send_message(f"URL編號無效，請輸入 0 到 {url_count} 之間的數字。", ephemeral=True)
            return

        # 檢查用戶是否已擁有該卡片
        cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
        user_card = cursor.fetchone()

        if not user_card:
            await interaction.response.send_message(f"您尚未擁有 {card_name}", ephemeral=True)
            return

        # 更新或插入 URL 編號
        cursor.execute('''
        UPDATE user_cards
        SET url_number = ?
        WHERE user_id = ? AND card_id = ?
        ''', (url_number, user_id, card_id))

        # 如果該紀錄不存在，則插入新的紀錄
        if cursor.rowcount == 0:
            cursor.execute('''
            INSERT INTO user_cards (user_id, card_id, url_number)
            VALUES (?, ?, ?)
            ''', (user_id, card_id, url_number))

        conn.commit()

        await interaction.response.send_message(f"成功更換 {card_name} 第一張顯示的圖片", ephemeral=True)

    except sqlite3.Error as e:
        await interaction.response.send_message(f"資料庫錯誤：{e}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"發生未知錯誤：{e}", ephemeral=True)

# 同步 Imgur 帳號中的所有相簿到資料庫
@bot.tree.command(name="sync_albums", description="UPDATE all the data from Imgur(from THEMATT account)")
async def sync_albums(interaction: discord.Interaction):
    if not IMGUR_USER_NAME:
        await interaction.response.send_message("未在環境變數中配置 IMGUR_USER_NAME，請檢查 .env 文件。", ephemeral=True)
        return

    try:
        await interaction.response.defer()  # 延遲回應

        albums_url = f"https://api.imgur.com/3/account/{IMGUR_USER_NAME}/albums"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        page = 0
        albums = []
        duplicates = []  # 儲存重複的 name_1 和 album_id 的清單
        added_count_r18 = 0
        total_skipped = 0
        added_count = 0

        # 使用 aiohttp 進行非同步請求
        async with aiohttp.ClientSession(headers=headers) as session:
            # 遍歷分頁
            while True:
                async with session.get(albums_url, params={"page": page}) as response:
                    if response.status != 200:
                        error_message = await response.json()
                        await interaction.followup.send(
                            f"獲取帳號相簿失敗（第 {page + 1} 頁）：{error_message.get('data', {}).get('error', '未知錯誤')}"
                        )
                        return

                    data = (await response.json()).get("data", [])
                    if not data:  # 如果當前頁沒有更多相簿，結束迴圈
                        break

                    albums.extend(data)
                    page += 1

            # 處理相簿數據
            for album in albums:
                album_id = album.get("id")
                title = album.get("title", "").strip()
                images = album.get("images_count", 0)

                # 檢查是否有標題和圖片
                if not title or images == 0:
                    total_skipped += 1
                    continue

                # 從相簿標題解析卡片名稱和分類
                try:
                    names, category = title.rsplit("(", 1)
                    category = category.strip(")")
                    name_parts = names.split("_")
                    name_1 = name_parts[0].strip() if len(name_parts) > 0 and name_parts[0] != "0" else None
                    name_2 = name_parts[1].strip() if len(name_parts) > 1 and name_parts[1] != "0" else None
                    name_3 = name_parts[2].strip() if len(name_parts) > 2 and name_parts[2].strip() != "0" else None
                except ValueError:
                    total_skipped += 1
                    continue

                # 檢查是否有重名情況（name_1 相同但 album_id 不同）
                cursor.execute('SELECT id, album_id FROM cards WHERE name_1 = ?', (name_1,))
                existing_card = cursor.fetchone()

                if existing_card:
                    existing_album_id = existing_card[1]
                    if existing_album_id != album_id:
                        duplicates.append((name_1, album_id))
                        total_skipped += 1
                        continue

                # 隨機生成 ATK 和 DEF，總和固定為 25
                atk = random.randint(0, 25)
                def_ = 25 - atk


                # 檢查 album_id 是否已存在
                cursor.execute("SELECT id FROM cards WHERE album_id = ?", (album_id,))
                card = cursor.fetchone()

                if card:
                    card_id = card[0]
                    # 如果 `album_id` 存在，更新 `card_urls`
                    album_images_url = f"https://api.imgur.com/3/album/{album_id}/images"
                    async with session.get(album_images_url) as album_response:
                        if album_response.status != 200:
                            total_skipped += 1
                            continue

                        album_images = (await album_response.json()).get("data", [])
                        for image in album_images:
                            url = image.get("link")
                            description = image.get("description") or ""  # 如果為 None，設為空字串
                            description = description.lower()  # 將描述轉為小寫
                            if url:
                                # 根據描述將 URL 插入正確的表
                                if "r18" in description:
                                    cursor.execute(
                                        "INSERT OR IGNORE INTO card_urls_2 (card_id, url) VALUES (?, ?)",
                                        (card_id, url)
                                    )
                                    added_count_r18 += 1
                                else:
                                    cursor.execute(
                                        "INSERT OR IGNORE INTO card_urls (card_id, url) VALUES (?, ?)",
                                        (card_id, url)
                                    )
                                    added_count += 1
                else:
                    # 如果 `album_id` 不存在，插入新的卡片數據
                    atk = random.randint(0, 25)
                    def_ = 25 - atk

                    cursor.execute(
                        '''INSERT INTO cards (name_1, name_2, name_3, category, album_id, atk, def_)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (name_1, name_2, name_3, category, album_id, atk, def_)
                    )
                    card_id = cursor.lastrowid

                    # 插入 URL
                    album_images_url = f"https://api.imgur.com/3/album/{album_id}/images"
                    async with session.get(album_images_url) as album_response:
                        if album_response.status != 200:
                            total_skipped += 1
                            continue

                        album_images = (await album_response.json()).get("data", [])
                        for image in album_images:
                            url = image.get("link")
                            description = image.get("description") or ""  # 如果為 None，設為空字串
                            description = description.lower()  # 將描述轉為小寫
                            if url:
                                # 根據描述將 URL 插入正確的表
                                if "r18" in description:
                                    cursor.execute(
                                        "INSERT INTO card_urls_2 (card_id, url) VALUES (?, ?)",
                                        (card_id, url)
                                    )
                                    added_count_r18 += 1
                                else:
                                    cursor.execute(
                                        "INSERT INTO card_urls (card_id, url) VALUES (?, ?)",
                                        (card_id, url)
                                    )
                                    added_count += 1

        conn.commit()

        # 構建清單文字
        duplicates_list = "\n".join([f"Name_3: {name_3}, Album ID: {album_id}" for name_3, album_id in duplicates])
        duplicates_message = f"\n\n以下卡片因 name_1 重複但 album_id 不同而跳過：\n{duplicates_list}" if duplicates else ""

        await interaction.followup.send(
            f"成功同步 {added_count} 張圖片，更新了 {added_count_r18} 張瑟圖，跳過 {total_skipped} 個相簿。{duplicates_message}"
        )

    except aiohttp.ClientError as e:
        await interaction.followup.send(f"請求 Imgur API 時發生錯誤：{e}")
    except sqlite3.Error as e:
        await interaction.followup.send(f"同步時發生資料庫錯誤：{e}")
    except Exception as e:
        await interaction.followup.send(f"發生未知錯誤：{e}")

# 查詢持有數前10高的卡片與持有者(全伺服器)
@bot.tree.command(name="check_the_top_10_cards", description="查詢全伺服器持有數前10高的卡片與持有者(ඞscs)")
async def check_the_top_10_cards(interaction: discord.Interaction):
    try:
        # 查詢 user_cards 中按 count 降序排序的前 10 條資料
        cursor.execute(''' 
            SELECT user_id, card_id, count FROM user_cards
            ORDER BY count DESC
            LIMIT 10
        ''')
        user_cards = cursor.fetchall()

        if not user_cards:
            await interaction.response.send_message("沒有找到用戶的卡片資料！")
            return

        # 準備顯示用戶卡片清單
        embed = discord.Embed(title="持有數前10高的持有者與卡片(全伺服器)", description="", color=0x00ff00)

        for user_id, card_id, count in user_cards:
            # 查詢對應卡片名稱
            cursor.execute('SELECT name_1 FROM cards WHERE id = ?', (card_id,))
            card_name = cursor.fetchone()
            if card_name:
                card_name = card_name[0]
            else:
                card_name = "未知卡片"  # 若無法找到該卡片，顯示 "未知卡片"

            # 使用用戶的 Discord 名稱作為替代
            user_catch = await bot.fetch_user(user_id)  # 獲取 Discord 用戶資料
            user_name = user_catch.display_name

            # 將每條紀錄顯示為單獨的條目
            embed.add_field(name=f"**{user_name}**", value=f"{card_name}｜{count}", inline=False)

        # 發送消息
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"發生錯誤: {e}")
        print(f"Error in /sc_server: {e}")

# 確保指令不會被忽略
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

##############################################################
##############################################################
#######################_傳統指令集中區_########################
##############################################################
##############################################################

@bot.command(name="daily", help="每日簽到")
async def daily(ctx):
    await handle_daily(source=ctx, is_interaction=False)

@bot.command(name="sc", help="按照名稱查詢卡片資訊")
async def sc(ctx, *, name: str):  # 傳統指令使用 `ctx` 和 `name` 作為參數
    class FakeResponse:
        """模擬 Interaction.response 的對象"""
        def __init__(self, ctx):
            self.ctx = ctx
            self._deferred = False  # 用於跟踪是否已延遲回應

        async def defer(self):
            """模擬 Interaction.response.defer"""
            self._deferred = True
            await self.ctx.send("處理中...")

        async def send_message(self, content=None, **kwargs):
            """模擬 Interaction.response.send_message"""
            if self._deferred:
                # 如果已延遲回應，則編輯消息
                await self.ctx.send(f"(已延遲) {content}", **kwargs)
            else:
                await self.ctx.send(content, **kwargs)

    class FakeInteraction:
        """用於模擬 Interaction 的對象"""
        def __init__(self, ctx):
            self.user = ctx.author
            self.channel = ctx.channel
            self.guild = ctx.guild
            self.response = FakeResponse(ctx)

    fake_interaction = FakeInteraction(ctx)

    # 調用 search_card 的回調函數
    try:
        await search_card.callback(fake_interaction, name=name)
    except Exception as e:
        await ctx.send(f"執行 /searchcard 回調函數時發生錯誤：{e}")

@bot.command(name="sca", help="按照分類查詢卡片資訊")
async def sc(ctx, *, category: str):  # 傳統指令使用 `ctx` 和 `name` 作為參數
    class FakeResponse:
        """模擬 Interaction.response 的對象"""
        def __init__(self, ctx):
            self.ctx = ctx
            self._deferred = False  # 用於跟踪是否已延遲回應

        async def defer(self):
            """模擬 Interaction.response.defer"""
            self._deferred = True
            await self.ctx.send("處理中...")

        async def send_message(self, content=None, **kwargs):
            """模擬 Interaction.response.send_message"""
            if self._deferred:
                # 如果已延遲回應，則編輯消息
                await self.ctx.send(f"(已延遲) {content}", **kwargs)
            else:
                await self.ctx.send(content, **kwargs)

    class FakeInteraction:
        """用於模擬 Interaction 的對象"""
        def __init__(self, ctx):
            self.user = ctx.author
            self.channel = ctx.channel
            self.guild = ctx.guild
            self.response = FakeResponse(ctx)

    fake_interaction = FakeInteraction(ctx)

    # 調用 search_card 的回調函數
    try:
        await search_card_by_category.callback(fake_interaction, category=category)
    except Exception as e:
        await ctx.send(f"執行 /searchcard 回調函數時發生錯誤：{e}")

@bot.command(name="scs", help="查詢持有數前10高的卡片與持有者(全伺服器)")
async def scs(ctx):
    try:
        # 查詢 user_cards 中按 count 降序排序的前 10 條資料
        cursor.execute(''' 
            SELECT user_id, card_id, count FROM user_cards
            ORDER BY count DESC
            LIMIT 10
        ''')
        user_cards = cursor.fetchall()

        if not user_cards:
            await ctx.send("沒有找到用戶的卡片資料！")
            return

        # 準備顯示用戶卡片清單
        embed = discord.Embed(title="持有數前10高的持有者與卡片(全伺服器)", description="", color=0x00ff00)

        for user_id, card_id, count in user_cards:
            # 查詢對應卡片名稱
            cursor.execute('SELECT name_1 FROM cards WHERE id = ?', (card_id,))
            card_name = cursor.fetchone()
            if card_name:
                card_name = card_name[0]
            else:
                card_name = "未知卡片"  # 若無法找到該卡片，顯示 "未知卡片"

            # 使用用戶的 Discord 名稱作為替代
            user_catch = await bot.fetch_user(user_id)  # 獲取 Discord 用戶資料
            user_name = user_catch.display_name

            # 將每條紀錄顯示為單獨的條目
            embed.add_field(name=f"**{user_name}**", value=f"{card_name}｜{count}", inline=False)

        # 發送消息
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"發生錯誤: {e}")
        print(f"Error in scs: {e}")

@bot.command(name="gacha", help="抽卡，斗肉!")
async def gacha(ctx):
    user_id = ctx.author.id
    current_time = datetime.utcnow()

    # 計算下一個整點時間
    next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    # 檢查用戶是否存在於資料庫中，並初始化用戶數據
    cursor.execute("SELECT exp_2 FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        cursor.execute("INSERT INTO users (id, level, exp, exp_2, coins, atk, def_) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (user_id, 1, 0, 0, 0, 10, 5))
        conn.commit()
        exp_2 = 0
    else:
        exp_2 = user_data[0]

    # 計算抽卡次數限制
    gacha_limit = 3 + (exp_2 // 30)

    # 初始化用戶的抽卡數據
    if user_id not in user_gacha_data:
        user_gacha_data[user_id] = {'last_gacha_time': current_time, 'remaining_draws': gacha_limit}

    user_gacha = user_gacha_data[user_id]

    # 刷新抽卡次數如果跨過下一個整點
    if current_time >= user_gacha['last_gacha_time'].replace(minute=0, second=0, microsecond=0) + timedelta(hours=1):
        user_gacha['last_gacha_time'] = current_time
        user_gacha['remaining_draws'] = gacha_limit

    # 如果抽卡次數用完，告知用戶剩餘時間
    if user_gacha['remaining_draws'] <= 0:
        remaining_time = next_hour - current_time
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(
            f"{ctx.author.name}，你目前沒有抽卡次數，請等待 {hours} 小時 {minutes} 分鐘 {seconds} 秒！"
        )
        return

    # 獲取所有卡片資料
    cursor.execute('SELECT id, name_1, name_2, name_3, atk, def_, category FROM cards')
    cards = cursor.fetchall()

    if not cards:
        await ctx.send("目前沒有可用的卡片！請先新增卡片！")
        return

    # 隨機抽取一張卡片
    selected_card = random.choice(cards)
    card_id, name_1, name_2, name_3, base_atk, base_def, category = selected_card

    # 獲取 URL 編號和對應的 URL
    cursor.execute('SELECT url_number FROM user_cards WHERE user_id = ? AND card_id = ?', (user_id, card_id))
    url_number_data = cursor.fetchone()
    url_number = url_number_data[0] if url_number_data else 1

    cursor.execute('SELECT url FROM card_urls WHERE card_id = ? AND url_number = ?', (card_id, url_number))
    card_url = cursor.fetchone()

    if not card_url:
        cursor.execute("SELECT url FROM card_urls WHERE card_id = ? LIMIT 1", (card_id,))
        card_url = cursor.fetchone()

    selected_url = card_url[0] if card_url else None

    # 更新用戶持有的卡片數量
    cursor.execute(''' 
    INSERT INTO user_cards (user_id, card_id, count) 
    VALUES (?, ?, 1) 
    ON CONFLICT(user_id, card_id) 
    DO UPDATE SET count = user_cards.count + 1 
    ''', (user_id, card_id))
    conn.commit()

    # 獲取最新持有數量並計算能力值加成
    cursor.execute('SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?', (user_id, card_id))
    result = cursor.fetchone()
    count = result[0] if result else 1

    multiplier = 1 + 0.04 * (2 ** (count - 1).bit_length() - 1)
    atk = int(base_atk * multiplier)
    defense = int(base_def * multiplier)

    # 減少用戶的剩餘抽卡次數
    user_gacha['remaining_draws'] -= 1

    # 顯示抽卡結果
    await show_gacha_result(
        ctx,
        name_1, name_2, name_3,
        category,
        selected_url,
        count,
        atk,
        defense,
        user_gacha['remaining_draws'],
        gacha_limit
    )

@bot.command(name="cards", help="查看已擁有的卡片")
async def cards(ctx):  # 傳統指令使用 `ctx` 作為參數
    class FakeResponse:
        """模擬 Interaction.response 的對象"""
        def __init__(self, ctx):
            self.ctx = ctx
            self._deferred = False  # 用於跟踪是否已延遲回應

        async def defer(self):
            """模擬 Interaction.response.defer"""
            self._deferred = True
            await self.ctx.send("處理中...", ephemeral=True)

        async def send_message(self, content=None, **kwargs):
            """模擬 Interaction.response.send_message"""
            if self._deferred:
                # 如果已延遲回應，則編輯消息
                await self.ctx.send(f"(已延遲) {content}", **kwargs)
            else:
                await self.ctx.send(content, **kwargs)

    class FakeInteraction:
        """用於模擬 Interaction 的對象"""
        def __init__(self, ctx):
            self.user = ctx.author
            self.channel = ctx.channel
            self.guild = ctx.guild
            self.response = FakeResponse(ctx)

    fake_interaction = FakeInteraction(ctx)

    # 調用 /cards 的回調函數
    try:
        await cards.callback(fake_interaction)
    except Exception as e:
        await ctx.send(f"執行 /cards 回調函數時發生錯誤：{e}")

@bot.command(name="profile", help="查看個人資料")
async def profile(ctx):
    user_id = ctx.author.id

    try:
        # 查詢用戶基本資料
        cursor.execute("SELECT level, exp, exp_2, atk, def_, coins FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            await ctx.send("用戶未註冊，請先使用**/daily**")
            return

        level, exp, exp_2, base_atk, base_def, coins = user_data

        # 獲取階級
        rank = get_rank(level)

        # 查詢用戶裝備的卡片
        cursor.execute("SELECT card_id FROM equipment WHERE user_id = ?", (user_id,))
        equipped_cards = cursor.fetchall()

        if not equipped_cards:
            embed = discord.Embed(title=f"{ctx.author.display_name} 的個人資料")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.add_field(name="等級", value=f"{level} ({rank})", inline=True)  # 顯示階級
            embed.add_field(name="台灣價值", value=str(exp), inline=True)
            embed.add_field(name="Coins", value=str(coins), inline=True)
            await ctx.send(embed=embed)
            return

        total_atk, total_def = base_atk, base_def
        equipped_card_details = []
        category_counts = {}

        for (card_id,) in equipped_cards:
            # 查詢卡片屬性
            cursor.execute("SELECT name_1, atk, def_ FROM cards WHERE id = ?", (card_id,))
            card = cursor.fetchone()

            if not card:
                continue

            card_name, card_atk, card_def = card

            # 查詢用戶持有卡片的次數
            cursor.execute("SELECT count, url_number FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
            user_card_data = cursor.fetchone()
            count = user_card_data[0] if user_card_data else 0
            url_number = user_card_data[1] if user_card_data else 1  # 預設為 1

            # 計算加權
            multiplier = 1 + 0.04 * (2 ** (count - 1).bit_length() - 1)
            weighted_atk = int(card_atk * multiplier)
            weighted_def = int(card_def * multiplier)

            total_atk += weighted_atk
            total_def += weighted_def

            # 查詢所有 URL
            cursor.execute("SELECT url_number FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
            url_number_data = cursor.fetchone()
            url_number = url_number_data[0] if url_number_data else 1  # 預設 url_number 為 1

            # 根據 url_number 選擇 URL
            cursor.execute("SELECT url FROM card_urls WHERE card_id = ? AND url_number = ?", (card_id, url_number))
            result = cursor.fetchone()

            if result:
                selected_url = result[0]  # 如果找到對應的 URL，使用它

            # 查詢卡片分類
            cursor.execute("SELECT category FROM cards WHERE id = ?", (card_id,))
            categories = [row[0] for row in cursor.fetchall()]
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1

            category_str = ', '.join(categories) if categories else "無分類"
            equipped_card_details.append((card_name, selected_url, category_str))

        # 計算額外加成
        extra_atk, extra_def = 0, 0
        for category, count in category_counts.items():
            if count >= 3:
                extra_atk += 10
                extra_def += 10

        total_atk += extra_atk
        total_def += extra_def

        # 構建嵌入消息
        embed = discord.Embed(title=f"{ctx.author.display_name} 的個人資料")
        embed.add_field(name="等級", value=f"{level} ({rank})", inline=True)  # 顯示階級
        embed.add_field(name="台灣價值", value=str(exp), inline=True)
        embed.add_field(name="積分", value=str(exp_2), inline=True)
        embed.add_field(name="ATK", value=f"{base_atk} (自身) + {total_atk - base_atk - extra_atk} (卡片) + {extra_atk} (額外加成)", inline=False)
        embed.add_field(name="DEF", value=f"{base_def} (自身) + {total_def - base_def - extra_def} (卡片) + {extra_def} (額外加成)", inline=False)
        embed.add_field(name="Coins", value=str(coins), inline=True)

        # 設置頭像
        if ctx.author.avatar:
            embed.set_thumbnail(url=ctx.author.avatar.url)

        for card_name, selected_url, category_str in equipped_card_details:
            if selected_url:
                embed.add_field(name=f"裝備卡片: {card_name}", value=category_str, inline=False)
                embed.set_image(url=selected_url)

        await ctx.send(embed=embed)

    except sqlite3.Error as e:
        await ctx.send(f"資料庫錯誤: {e}")
    except Exception as e:
        await ctx.send(f"發生未知錯誤: {e}")

@bot.command(name="match", help="匹配並挑戰其他玩家(全伺服器)")
async def match(ctx):
    user_id = ctx.author.id

    # 初始化用戶挑戰數據
    now = datetime.utcnow()
    user_data = user_match_data.get(user_id, {'last_reset': now, 'remaining': DAILY_LIMIT})

    # 每天早上 9 點刷新挑戰次數
    if now - user_data['last_reset'] >= timedelta(hours=24):
        next_reset = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now >= next_reset:
            next_reset += timedelta(days=1)
        user_data['last_reset'] = next_reset
        user_data['remaining'] = DAILY_LIMIT

    # 檢查剩餘挑戰次數
    if user_data['remaining'] <= 0:
        remaining_time = (user_data['last_reset'] - now).total_seconds()
        hours, minutes, seconds = int(remaining_time // 3600), int((remaining_time % 3600) // 60), int(remaining_time % 60)
        await ctx.send(
            f"你今天的挑戰次數已用完，將於 {hours} 小時 {minutes} 分鐘 {seconds} 秒後刷新次數。",
            ephemeral=True
        )
        return

    # 將用戶挑戰數據存回字典
    user_match_data[user_id] = user_data

    # 確認使用者存在於資料庫
    cursor.execute("SELECT id, level, atk, def_, exp_2 FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        await ctx.send("你尚未註冊，請先使用 /daily 註冊。")
        return

    user_level, user_atk, user_def, user_exp_2 = user[1:]

    # 隨機選擇一個已註冊且有裝備卡片的用戶
    cursor.execute('''
    SELECT u.id, u.level, u.atk, u.def_, u.exp_2, e.card_id
    FROM users u
    JOIN equipment e ON u.id = e.user_id
    WHERE u.id != ?
    GROUP BY u.id
    ORDER BY RANDOM()
    LIMIT 1
    ''', (user_id,))
    opponent = cursor.fetchone()

    if not opponent:
        await ctx.send("目前沒有其他玩家可以匹配！")
        return

    opponent_id, opponent_level, opponent_atk, opponent_def, opponent_exp_2, opponent_card_id = opponent

    # 根據 opponent_id 獲取對手的 username
    opponent_user = await bot.fetch_user(opponent_id)  # 獲取對手的 Discord 用戶資料
    opponent_username = opponent_user.display_name  # 使用 display_name

    # 獲取對手的裝備卡片資訊，包括對應的 url_number
    cursor.execute('''
    SELECT c.name_1, u.url
    FROM cards c
    JOIN card_urls u ON c.id = u.card_id
    JOIN user_cards uc ON c.id = uc.card_id
    WHERE c.id = ? AND uc.user_id = ? AND u.url_number = uc.url_number
    ''', (opponent_card_id, opponent_id))
    opponent_card = cursor.fetchone()

    # 如果未找到對應的 URL，使用第一張作為備選
    if not opponent_card:
        cursor.execute('''
        SELECT c.name_1, u.url
        FROM cards c
        JOIN card_urls u ON c.id = u.card_id
        WHERE c.id = ?
        ORDER BY u.url_number ASC
        LIMIT 1
        ''', (opponent_card_id,))
        opponent_card = cursor.fetchone()

    if not opponent_card:
        await ctx.send("對手的裝備卡片資訊不完整，無法匹配！")
        return

    opponent_card_name, opponent_card_url = opponent_card

    # 獲取自己的裝備卡片資訊
    cursor.execute('''
    SELECT c.name_1, u.url
    FROM cards c
    JOIN card_urls u ON c.id = u.card_id
    JOIN equipment e ON c.id = e.card_id
    WHERE e.user_id = ?
    ORDER BY e.id DESC
    LIMIT 1
    ''', (user_id,))
    user_card = cursor.fetchone()

    if not user_card:
        await ctx.send("你尚未裝備任何卡片，無法匹配！")
        return

    user_card_name, user_card_url = user_card

    # 構建初始嵌入
    opponent_total_atk, opponent_total_def = calculate_total_stats(opponent_id)
    user_total_atk, user_total_def = calculate_total_stats(user_id)
    embed = discord.Embed(title="匹配成功！", description=f"你的對手：{opponent_username}")
    embed.add_field(name="對戰績分", value=f"{opponent_exp_2}", inline=True)
    embed.add_field(name="ATK", value="???", inline=True)
    embed.add_field(name="DEF", value="???", inline=True)
    embed.add_field(name="裝備卡片", value=f"{opponent_card_name}", inline=False)
    embed.set_image(url=opponent_card_url)

    # 添加按鈕進行互動
    class MatchInteraction(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.attack_used = False
            self.defend_used = False

        async def disable_button(self, button: discord.ui.Button):
            """禁用按鈕，並更新視圖。"""
            button.disabled = True

        @discord.ui.button(label="攻擊", style=discord.ButtonStyle.danger)
        async def attack(self, interaction: discord.Interaction, button: discord.ui.Button):
            nonlocal user_exp_2, opponent_exp_2

            success_rate = user_total_atk / (opponent_total_def + user_total_atk)

            if random.random() <= success_rate:
                # 勝利邏輯
                user_exp_2 = max(0, user_exp_2 + 3)
                opponent_exp_2 = max(0, opponent_exp_2 - 1)

                def calculate_stats(exp_2):
                    return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                user_new_atk, user_new_def = calculate_stats(user_exp_2)
                opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                cursor.executemany(
                    "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                    [
                        (user_exp_2, user_new_atk, user_new_def, user_id),
                        (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                    ]
                )
                conn.commit()
                await self.show_victory(interaction, opponent_card_name, opponent_card_url)
                return

            # 攻擊失敗，判定是否觸發對方反擊
            counter_rate = opponent_total_def / (user_total_def + opponent_total_def)
            if random.random() <= counter_rate:
                # 對方成功觸發反擊
                counter_success_rate = opponent_total_def / (user_total_def + opponent_total_def)
                if random.random() <= counter_success_rate:
                    user_exp_2 = max(0, user_exp_2 - 2)
                    opponent_exp_2 = max(0, opponent_exp_2 + 3)

                    def calculate_stats(exp_2):
                        return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                    user_new_atk, user_new_def = calculate_stats(user_exp_2)
                    opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                    cursor.executemany(
                        "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                        [
                            (user_exp_2, user_new_atk, user_new_def, user_id),
                            (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                        ]
                    )
                    conn.commit()
                    await self.show_defeat_2(interaction, opponent_card_name, opponent_card_url)
                    return

            # 攻擊失敗但無反擊
            self.attack_used = True
            embed = discord.Embed(title="匹配成功！", description=f"你的對手：{opponent_username}")
            embed.add_field(name="對戰績分", value=f"{opponent_exp_2}", inline=True)
            embed.add_field(name="ATK", value="???", inline=True)
            embed.add_field(name="DEF", value="???", inline=True)
            embed.add_field(name="戰況", value="你的攻擊被格檔了，但對手的反擊無效！", inline=True)
            embed.add_field(name="裝備卡片", value=f"{opponent_card_name}", inline=False)
            embed.set_image(url=opponent_card_url)
            await self.disable_button(button)
            await interaction.response.edit_message(view=self)
            await self.check_buttons(interaction)

        @discord.ui.button(label="防禦", style=discord.ButtonStyle.primary)
        async def defend(self, interaction: discord.Interaction, button: discord.ui.Button):
            nonlocal user_exp_2, opponent_exp_2
            success_rate = opponent_total_atk / (user_total_def + opponent_total_atk)

            if random.random() > success_rate:
                # 敗北邏輯
                user_exp_2 = max(0, user_exp_2 - 2)
                opponent_exp_2 = max(0, opponent_exp_2 + 3)

                def calculate_stats(exp_2):
                    return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                user_new_atk, user_new_def = calculate_stats(user_exp_2)
                opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                cursor.executemany(
                    "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                    [
                        (user_exp_2, user_new_atk, user_new_def, user_id),
                        (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                    ]
                )
                conn.commit()
                await self.show_defeat(interaction, opponent_card_name, opponent_card_url)
                return

            # 防禦成功，判定是否觸發反擊
            counter_rate = user_total_def / (user_total_def + opponent_total_def)
            if random.random() <= counter_rate:
                counter_success_rate = user_total_def / (user_total_def + opponent_total_def)
                if random.random() <= counter_success_rate:
                    user_exp_2 = max(0, user_exp_2 + 3)
                    opponent_exp_2 = max(0, opponent_exp_2 - 1)

                    def calculate_stats(exp_2):
                        return 10 + (exp_2 // 30) * 2, 5 + (exp_2 // 30) * 1

                    user_new_atk, user_new_def = calculate_stats(user_exp_2)
                    opponent_new_atk, opponent_new_def = calculate_stats(opponent_exp_2)

                    cursor.executemany(
                        "UPDATE users SET exp_2 = ?, atk = ?, def_ = ? WHERE id = ?",
                        [
                            (user_exp_2, user_new_atk, user_new_def, user_id),
                            (opponent_exp_2, opponent_new_atk, opponent_new_def, opponent_id),
                        ]
                    )
                    conn.commit()
                    await self.show_victory_2(interaction, opponent_card_name, opponent_card_url)
                    return

            # 防禦成功但無反擊
            self.attack_used = True
            embed = discord.Embed(title="匹配成功！", description=f"你的對手：{opponent_username}")
            embed.add_field(name="對戰績分", value=f"{opponent_exp_2}", inline=True)
            embed.add_field(name="ATK", value="???", inline=True)
            embed.add_field(name="DEF", value="???", inline=True)
            embed.add_field(name="戰況", value="防禦成功，但你的反擊無效！", inline=True)
            embed.add_field(name="裝備卡片", value=f"{opponent_card_name}", inline=False)
            embed.set_image(url=opponent_card_url)
            await self.disable_button(button)
            await interaction.response.edit_message(view=self)
            await self.check_buttons(interaction)

        async def check_buttons(self, interaction):
            # 檢查是否所有按鈕都被禁用
            if all(isinstance(child, discord.ui.Button) and child.disabled for child in self.children):
                # 將所有按鈕恢復為可用
                for child in self.children:
                    if isinstance(child, discord.ui.Button):
                        child.disabled = False

                # 更新訊息以恢復按鈕
                await interaction.message.edit(view=self)

        async def show_victory(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="WIN！", description=f"攻擊成功，對手的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

        async def show_victory_2(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="WIN！", description=f"反擊成功，對手的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

        async def show_defeat(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="LOSE...", description=f"防禦失敗，你的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

        async def show_defeat_2(self, interaction, card_name, card_url):
            cursor.execute(''' 
            SELECT id FROM cards WHERE name_1 = ?
            ''', (card_name,))
            card_id_result = cursor.fetchone()
            card_id = card_id_result[0]

            cursor.execute(''' 
            SELECT url FROM card_urls_2 
            WHERE card_id = ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (card_id,))
    
            result = cursor.fetchone()
            if result:
                final_url = result[0]  # 从查询结果中提取 URL
            else:
                final_url = card_url  # 如果没有找到，使用默认的 URL
            user_data['remaining'] -= 1
            remaining = user_data['remaining']

            embed = discord.Embed(title="LOSE...", description=f"對手反擊成功，你的卡片 {card_name} 大破了！")
            embed.set_image(url=final_url)
            embed.set_footer(text=f"剩餘匹配次數：{remaining}/{DAILY_LIMIT}")
            await interaction.response.edit_message(embed=embed, view=None)

    await ctx.send(embed=embed, view=MatchInteraction())

@bot.command(name="unequip", help="取消裝備所有卡片")
async def unequip(ctx):
    try:
        # 確認使用者存在於資料表
        user_id = ctx.author.id
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            await ctx.send("你尚未註冊為使用者，請先註冊 (/daily)")
            return

        # 刪除該用戶在 equipment 表中的所有裝備資料
        cursor.execute('DELETE FROM equipment WHERE user_id = ?', (user_id,))
        conn.commit()

        await ctx.send("卡片取消裝備成功")

    except sqlite3.Error as e:
        await ctx.send(f"取消裝備時發生資料庫錯誤：{e}")
    except Exception as e:
        await ctx.send(f"發生未知錯誤：{e}")

@bot.command(name="equip", help="裝備卡片")
async def equip(ctx, card_name: str):
    user_id = ctx.author.id

    try:
        # 確認用戶是否存在
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            await ctx.send("用戶未註冊，請先使用/daily")
            return

        # 根據卡片名稱查找卡片
        cursor.execute("SELECT id, atk, def_ FROM cards WHERE name_1 = ?", (card_name,))
        card = cursor.fetchone()
        if not card:
            await ctx.send("找不到此卡片名稱")
            return

        card_id, card_atk, card_def = card

        # 確認用戶是否持有該卡片
        cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
        user_card = cursor.fetchone()
        if not user_card or user_card[0] <= 0:
            await ctx.send("你未持有該卡片，無法裝備")
            return

        card_count = user_card[0]

        # 檢查該卡片是否已經裝備
        cursor.execute("SELECT card_id FROM equipment WHERE user_id = ?", (user_id,))
        equipped_cards_ids = [row[0] for row in cursor.fetchall()]
        if card_id in equipped_cards_ids:
            await ctx.send("該卡片已經裝備，無需重複操作")
            return

        # 計算加權值
        multiplier = 1 + 0.04 * (2 ** (card_count - 1).bit_length() - 1)
        weighted_atk = int(card_atk * multiplier)
        weighted_def = int(card_def * multiplier)

        # 查詢已裝備的卡片數量
        cursor.execute("SELECT COUNT(*) FROM equipment WHERE user_id = ?", (user_id,))
        equipped_count = cursor.fetchone()[0]

        if equipped_count >= 3:
            # 顯示模塊，讓用戶選擇要替換的卡片
            cursor.execute('''SELECT e.card_id, c.name_1, c.atk, c.def_, uc.count
                               FROM equipment e
                               JOIN cards c ON e.card_id = c.id
                               JOIN user_cards uc ON e.card_id = uc.card_id
                               WHERE e.user_id = ?''', (user_id,))
            equipped_cards = cursor.fetchall()

            embed = discord.Embed(title="選擇要替換的卡片")
            embed.add_field(
                name="想要裝備的卡片",
                value=f"{card_name} (ATK: {weighted_atk}, DEF: {weighted_def}, 數量: {card_count})",
                inline=False,
            )

            card_details = ""
            # 根據 count 計算加權的 atk 和 def_
            for i, (equip_card_id, equip_card_name, equip_atk, equip_def, equip_count) in enumerate(equipped_cards):
                equip_multiplier = 1 + 0.04 * (2 ** (equip_count - 1).bit_length() - 1)
                equip_weighted_atk = int(equip_atk * equip_multiplier)
                equip_weighted_def = int(equip_def * equip_multiplier)

                card_details += (
                    f"{i + 1}. {equip_card_name} - ATK: {equip_weighted_atk}, DEF: {equip_weighted_def}, 數量: {equip_count}\n"
                )

            embed.add_field(name="目前裝備卡片", value=card_details)

            # 使用 View 來包裝按鈕
            view = View()

            for i, (equip_card_id, equip_card_name, _, _, _) in enumerate(equipped_cards):
                async def button_callback(interaction, equip_card_id=equip_card_id):
                    # 替換裝備邏輯
                    cursor.execute("DELETE FROM equipment WHERE user_id = ? AND card_id = ?", (user_id, equip_card_id))
                    cursor.execute("INSERT INTO equipment (user_id, card_id) VALUES (?, ?)", (user_id, card_id))
                    conn.commit()

                    await interaction.response.edit_message(content=f"成功裝備卡片 {card_name}，替換掉 {equip_card_name}！", view=None)

                button = Button(label=f"卡片 {i + 1}", custom_id=f"equip_card_{equip_card_id}")
                button.callback = button_callback
                view.add_item(button)

            await ctx.send(embed=embed, view=view)
            return

        # 裝備新卡片
        cursor.execute("INSERT INTO equipment (user_id, card_id) VALUES (?, ?)", (user_id, card_id))
        conn.commit()
        await ctx.send(f"成功裝備卡片 {card_name}！")

    except Exception as e:
        await ctx.send(f"發生錯誤: {e}")

@bot.command(name="c", help="更換卡片第1張顯示的圖片")
@app_commands.describe(
    card_name="卡片名稱(英文)",
    url_number="URL編號"
)
async def change_url_number(ctx, card_name: str, url_number: int):
    user_id = ctx.author.id

    try:
        # 確認用戶是否註冊
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            await ctx.send("您尚未註冊，請先使用 /daily", ephemeral=True)
            return

        # 確認卡片是否存在
        cursor.execute("SELECT id FROM cards WHERE name_1 = ?", (card_name,))
        card = cursor.fetchone()

        if not card:
            await ctx.send("卡片名稱無效", ephemeral=True)
            return

        card_id = card[0]

        # 檢查輸入的 url_number 是否有效
        cursor.execute("SELECT COUNT(*) FROM card_urls WHERE card_id = ?", (card_id,))
        url_count = cursor.fetchone()[0]

        if url_number < 0 or url_number > url_count:
            await ctx.send(f"URL編號無效，請輸入 0 到 {url_count} 之間的數字。", ephemeral=True)
            return

        # 檢查用戶是否已擁有該卡片
        cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
        user_card = cursor.fetchone()

        if not user_card:
            await ctx.send(f"您尚未擁有 {card_name}", ephemeral=True)
            return

        # 更新或插入 URL 編號
        cursor.execute('''
        UPDATE user_cards
        SET url_number = ?
        WHERE user_id = ? AND card_id = ?
        ''', (url_number, user_id, card_id))

        # 如果該紀錄不存在，則插入新的紀錄
        if cursor.rowcount == 0:
            cursor.execute('''
            INSERT INTO user_cards (user_id, card_id, url_number)
            VALUES (?, ?, ?)
            ''', (user_id, card_id, url_number))

        conn.commit()

        await ctx.send(f"成功更換 {card_name} 第一張顯示的圖片", ephemeral=True)

    except sqlite3.Error as e:
        await ctx.send(f"資料庫錯誤：{e}", ephemeral=True)
    except Exception as e:
        await ctx.send(f"發生未知錯誤：{e}", ephemeral=True)

@bot.command(name="clone", help="使用coins兌換卡片(aka.印卡)")
@app_commands.describe(
    card_name="卡片名稱(英文)",
    number="想兌換的數量"
)
async def clone(ctx, card_name: str, number: int):
    user_id = ctx.author.id

    try:
        # 檢查數量是否有效
        if number <= 0:
            await ctx.send("兌換數量必須為正整數", ephemeral=True)
            return

        # 確認用戶是否註冊
        cursor.execute("SELECT coins FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            await ctx.send("用戶未註冊，請先註冊 (/daily)", ephemeral=True)
            return

        user_coins = user_data[0]

        # 從 cards 表查詢 card_id
        cursor.execute("SELECT id FROM cards WHERE name_1 = ?", (card_name,))
        card_data = cursor.fetchone()

        if not card_data:
            await ctx.send("找不到指定名稱的卡片", ephemeral=True)
            return

        card_id = card_data[0]

        # 確認 coins 是否足夠
        cost = number * 2
        if user_coins < cost:
            await ctx.send(f"硬幣不足，需要 {cost} coins，但你只有 {user_coins} coins", ephemeral=True)
            return

        # 消耗硬幣
        cursor.execute("UPDATE users SET coins = coins - ? WHERE id = ?", (cost, user_id))

        # 更新 user_cards 的 count
        cursor.execute(
            '''
            INSERT INTO user_cards (user_id, card_id, count)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, card_id)
            DO UPDATE SET count = count + excluded.count
            ''',
            (user_id, card_id, number)
        )

        conn.commit()
        await ctx.send(f"成功兌換 {card_name}，你總共印了 {number} 張卡片！")

    except sqlite3.Error as e:
        await ctx.send(f"兌換卡片時發生資料庫錯誤：{e}", ephemeral=True)
    except Exception as e:
        await ctx.send(f"發生未知錯誤：{e}", ephemeral=True)

@bot.command(name="trade", help="與其他人交換卡片")
async def trade(ctx, target_user: discord.Member, your_card_name: str):
    user_id = ctx.author.id
    target_user_id = target_user.id

    try:
        # 確認用戶是否註冊
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            await ctx.send("您尚未註冊，請先使用 /daily")
            return

        cursor.execute("SELECT id FROM users WHERE id = ?", (target_user_id,))
        if not cursor.fetchone():
            await ctx.send(f"{target_user.display_name} 尚未註冊，無法進行交易。")
            return

        # 確認卡片是否存在
        cursor.execute("SELECT id FROM cards WHERE name_1 = ?", (your_card_name,))
        your_card = cursor.fetchone()
        if not your_card:
            await ctx.send("您的卡片名稱無效，請檢查後再試。")
            return

        your_card_id = your_card[0]

        # 確認持有數量
        cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, your_card_id))
        your_card_count = cursor.fetchone()
        if not your_card_count or your_card_count[0] <= 0:
            await ctx.send(f"您沒有足夠的 {your_card_name} 可供交換。")
            return

        # 提示對方選擇要交換的卡片
        await ctx.send(f"{target_user.display_name}，請選擇要交換的卡片名稱，並於30秒內回覆。")

        # 等待對方回覆
        def check(msg):
            return msg.author == target_user and msg.channel == ctx.channel

        try:
            target_card_message = await bot.wait_for("message", check=check, timeout=30.0)
            target_card_name = target_card_message.content.strip()

            # 確認對方卡片是否存在
            cursor.execute("SELECT id FROM cards WHERE name_1 = ?", (target_card_name,))
            target_card = cursor.fetchone()
            if not target_card:
                await ctx.send(f"{target_user.display_name} 提供的卡片名稱無效，終止交易。")
                return

            target_card_id = target_card[0]

            # 確認對方持有數量
            cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (target_user_id, target_card_id))
            target_card_count = cursor.fetchone()
            if not target_card_count or target_card_count[0] <= 0:
                await ctx.send(f"{target_user.display_name} 沒有足夠的 {target_card_name} 可供交換。")
                return

            # 確認對方是否同意交易
            await ctx.send(f"{target_user.display_name}，是否同意用 {target_card_name} 與 {ctx.author.display_name} 的 {your_card_name} 進行交換？（輸入 `confirm` 同意）")

            try:
                confirm_message = await bot.wait_for("message", check=check, timeout=30.0)
                if confirm_message.content.strip().lower() != "confirm":
                    await ctx.send(f"{target_user.display_name} 沒有確認交易，終止交易。")
                    return
            except asyncio.TimeoutError:
                await ctx.send("⚠️有內鬼，終止交易⚠️")
                return

            # 執行交換
            cursor.execute("UPDATE user_cards SET count = count - 1 WHERE user_id = ? AND card_id = ?", (user_id, your_card_id))
            cursor.execute("UPDATE user_cards SET count = count + 1 WHERE user_id = ? AND card_id = ?", (target_user_id, your_card_id))

            cursor.execute("UPDATE user_cards SET count = count - 1 WHERE user_id = ? AND card_id = ?", (target_user_id, target_card_id))
            cursor.execute("UPDATE user_cards SET count = count + 1 WHERE user_id = ? AND card_id = ?", (user_id, target_card_id))

            # 檢查是否有卡片數量變為 0，若為 0 則刪除該卡片
            cursor.execute("DELETE FROM user_cards WHERE user_id = ? AND card_id = ? AND count <= 0", (user_id, your_card_id))
            cursor.execute("DELETE FROM user_cards WHERE user_id = ? AND card_id = ? AND count <= 0", (target_user_id, target_card_id))
            conn.commit()

            # 成功訊息
            await ctx.send(f"✅ 交易成功！\n\n{ctx.author.display_name} 提供的卡片：{your_card_name}\n{target_user.display_name} 提供的卡片：{target_card_name}")
        except asyncio.TimeoutError:
            await ctx.send("⚠️有內鬼，終止交易⚠️")
    except sqlite3.Error as e:
        await ctx.send(f"交易過程中發生資料庫錯誤：{e}")
    except Exception as e:
        await ctx.send(f"交易過程中發生未知錯誤：{e}")

@bot.command(name="deleterecord", help="清除**自己**的所有記錄")
async def deleterecord(ctx):
    user_id = ctx.author.id

    try:
        # 檢查是否存在於 users 表
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            await ctx.send("❌您尚未註冊，無需清除記錄❌")
            return

        # 確認操作
        await ctx.send(
            "⚠️確認要刪除所有記錄嗎？此操作無法復原！請在30秒內回覆**confirm**或忽略⚠️"
        )

        def check(m):
            return (
                m.author == ctx.author and 
                m.channel == ctx.channel and 
                m.content.strip().lower() == "confirm"
            )

        try:
            confirmation = await bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("操作超時，未收到確認。")
            return

        # 刪除相關記錄
        cursor.execute("DELETE FROM user_cards WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM equipment WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        await ctx.send("✅所有記錄已成功刪除✅")

    except sqlite3.Error as e:
        await ctx.send(f"資料庫錯誤: {e}")
    except Exception as e:
        await ctx.send(f"發生未知錯誤: {e}")

##############################################################
##############################################################
#######################_偵測訊息集中區_########################
##############################################################
##############################################################

# 偵測訊息事件
async def handle_triggers(message, triggers_responses, probabilities=None):
    """
    處理訊息中的觸發關鍵字並回應。
    :param message: Discord訊息對象
    :param triggers_responses: 關鍵字及對應回應的字典
    :param probabilities: (可選) 每個回應的機率
    """
    for triggers, responses in triggers_responses.items():
        # 檢查訊息中是否包含觸發關鍵字
        if any(trigger in message.content for trigger in triggers):
            # 如果有機率設定，使用 random.choices
            if probabilities and triggers in probabilities:
                response = random.choices(responses, probabilities[triggers])[0]  # 根據機率選擇回應
            else:
                response = random.choice(responses)  # 隨機選擇回應
            await message.channel.send(response)
            return  # 回應一次後跳出

@bot.event
async def on_message(message):
    try:
        if message.author.bot:
            return

        server_id = str(message.guild.id) if message.guild else None
        if not server_id:
            return  # 忽略非伺服器訊息

        # 定義觸發的關鍵字和對應回應
        triggers_responses = {
            ("靈零", "零靈", "夜零", "遠嶺", "零零", "靈靈"): [
                "00，15歲，是個律師",
                "00，15歲，是個臭甲"
            ],
            ("Kagura Mea", "kaguramea", "kagura mea", "Mea", "mea"): ["我婆"],
            ("mmi",): ["曹氏宗親會，啟動!"],
            ("Emerald I bonus", "Emerald II bonus", "Emerald III bonus", "Emerald IV bonus"): ["又你婆，每個都你婆"],
            ("美味"): ["蟹堡", "謝秉利"],
            ("觘機掰"): ["<@552059583569330187> 觘機掰"]
        }

        probabilities = {
            ("靈零", "零靈", "夜零", "遠嶺", "零零", "靈靈"): [0.99, 0.01],
            ("mmi",): [0.05],
            ("Emerald I bonus", "Emerald II bonus", "Emerald III bonus", "Emerald IV bonus"): [0.3],
            ("美味"): [0.99, 0.01],
            ("觘機掰"): [0.3]
        }

        # 檢查並確保機率為單一值時，不改變填寫的機率
        for key, value in probabilities.items():
            if len(value) == 1:
                continue  # 單一值時，保留原機率
            else:
                # 多值時，確保機率總和為 1，若需要修正可在此處加邏輯
                total_probability = sum(value)
                if total_probability != 1.0:
                    probabilities[key] = [p / total_probability for p in value]  # 正規化機率

        # EXP 獎勳的觸發詞
        exp_changes = {
            "青鳥": -1,
            "覺青": -1,
            "我支持柯文哲": -1,
            "死忠": -1,
            "蟾蜍": -1,
            "1450": -1,
            "ㄌㄨㄚˋ": -1,
            "ㄘㄨㄚˋ": -1,
            "台灣缺電": -1,
            "賴皇": 1,
            "清德宗": 1,
            "民進黨萬歲": 1,
            "台灣不缺電": 1,
            "藍白不倒 台灣不好": 1,
            "我支持民進黨": 1,
            "中共同路人": 1,
            "在那叫什麼": 1,
            "武漢肺炎": 1,
            "重啟個屁": 1,
            "抗中保台": 1,
            "時空背景不同": 1
        }

        # 檢查訊息內容是否包含觸發詞並更新 EXP
        for word, exp_change in exp_changes.items():
            if word in message.content.lower():
                result = update_user_exp(message.author.id, exp_change, 0)  # 呼叫函數並獲取結果
                level_up = result["level_up"]
                level_down = result["level_down"]
                new_level = result["new_level"]

                if exp_change > 0:
                    response = f"做得好！{message.author.mention}的台灣價值+{exp_change}！"
                else:
                    response = f"{message.author.mention}的台灣價值{exp_change}，民進黨將把你列為重點觀察人物"

                # 升級或降級的額外消息
                if level_up:
                    response += f"，恭喜升級到等級 {new_level}，民進黨感謝你對黨的貢獻"
                elif level_down:
                    response += f"，很遺憾，你降級到等級 {new_level}，民進黨總有一天會把你抓去關"

                await message.channel.send(response)
                break

        conn.commit()
        await handle_triggers(message, triggers_responses, probabilities)
        await bot.process_commands(message)

    except Exception as e:
        print(f"Error in on_message: {e}")

##############################################################
##############################################################
###########################_尾端_#############################
##############################################################
##############################################################

# 啟動機器人
if __name__ == '__main__':
    bot.run(TOKEN)