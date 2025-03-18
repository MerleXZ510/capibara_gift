import os
import subprocess
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot 已上線: {bot.user}')

@bot.command()
async def claim(ctx, code: str):
    await ctx.send(f'收到指令，開始嘗試兌換代碼：`{code}`...')
    try:
        # 呼叫 capibara_gift 的主程式
        result = subprocess.run(
            ['python3', 'main.py', code],
            capture_output=True,
            text=True
        )
        
        output = result.stdout or result.stderr or "沒有輸出"

        # 如果太長，截斷輸出
        if len(output) > 1900:
            output = output[:1900] + "... (已截斷)"

        await ctx.send(f'執行結果：\n```
{output}
```')

    except Exception as e:
        await ctx.send(f'執行時發生錯誤：{e}')

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❗️ DISCORD_TOKEN 未設定")