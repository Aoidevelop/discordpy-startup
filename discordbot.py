from discord.ext import commands
from janome.tokenizer import Tokenizer
import os
t = Tokenizer()
token = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix='/')

prefix = '&'
ngword = []
users = {}


print('起動しました')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content[0] == prefix:
        cmd = message.content.split()
        if cmd[0] == prefix + 'help':
            await message.channel.send('addword:NGワードを追加します'
                                       'delword:NGワードを削除します'
                                       'listword:NGワードの一覧を表示します'
                                       'users:NGワードを発言したユーザーを表示します'
                                       'help:このヘルプを表示します')
        if cmd[0] == prefix + 'addword':
            for arg in cmd[1::]:
                if arg not in ngword:
                    ngword.append(arg)
            await message.channel.send(str(message.content.split()[1::]) + 'をNGワードに追加しました')
        if cmd[0] == prefix + 'delword':
            for arg in cmd[1::]:
                if arg in ngword:
                    ngword.remove(arg)
            await message.channel.send(str(message.content.split()[1::]) + 'をNGワードから除外しました')
        if cmd[0] == prefix + 'listword':
            await message.channel.send(ngword)
        if cmd[0] == prefix + 'users':
            ans = ''
            for u, c in users.items():
                ans += bot.get_user(u).name + 'さん '+ str(c) + '回'
            await message.channel.send(ans)
    else:
        tokens = t.tokenize(message.content, wakati=True)
        for token in tokens:
            print(token)
            if token in ngword:
                await message.delete()
                await message.channel.send('その発言は許可されていません')
                if message.author.id not in users:
                    users[message.author.id] = 1
                else:
                    users[message.author.id] += 1

bot.run(token)
