import os
import asyncio
from discord.ext import commands
import discord
from redeem_logic import redeem_code_for_user

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Discord Bot 已上線: {bot.user}')

@bot.command()
async def claim(ctx, code: str):
    await ctx.send(f'🎫 收到禮品碼 `{code}`，開始為所有帳號兌換...')

    user_ids = os.getenv("DEFAULT_USER_IDS", "")
    user_list = [uid.strip() for uid in user_ids.split(",") if uid.strip()]

    if not user_list:
        await ctx.send("❌ 沒有設定帳號（DEFAULT_USER_IDS）")
        return

    results = await asyncio.gather(*(redeem_code_for_user(uid, code) for uid in user_list))

    response = "\n".join(results)
    if len(response) > 1900:
        response = response[:1900] + "\n...(已截斷)"

    await ctx.send(f"🎁 結果如下：\n```\n{response}\n```")

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❗️ 未設定環境變數 DISCORD_TOKEN")
    else:
        bot.run(token)
