import discord
import os
import traceback
token = os.environ['DISCORD_BOT_TOKEN']  # トークンを入力してください。

client = discord.Client()

ngwords = list()
prefix = ('&')
users = {}

@client.event
async def on_message(message):
    global users
    if message.author.bot:
        return

    for n in ngwords:
        if n in message.content.replace(' ', '').replace('　', ''):
            await message.delete()
            if str(message.author.id) not in users:
                users[str(message.author.id)] = 1
            else:
                users[str(message.author.id)] += 1
            await message.channel.send('その発言は許可されていません！')
            break
    else:
        if not message.author.permissions_in(message.channel).administrator:
            return
        if message.content.split()[0] == prefix + 'addword':
            ngwords.append(message.content.split()[1])
            await message.channel.send(message.content.split()[1] + 'をngワードに追加しました')
        if message.content.split()[0] == prefix + 'wordlist':
            await message.channel.send(ngwords)
        if message.content.split()[0] == prefix + 'violator' and len(message.content.split()) == 2:
            ans = {}
            for u, p in users.items():
                if int(message.content.split()[1]) < p:
                    ans[u] = p
            await  message.channel.send(ans)
        elif message.content.split()[0] == prefix + 'violator':
            await message.channel.send(users)
        if message.content.split()[0] == prefix + 'purge':
            users = {}
        if message.content.split()[0] == prefix + 'help':
            await  message.channel.send('ヘルプ\n'+
                                        'addword <text>:ngワードを追加します。\n'+
                                        'wordlist:ngワードの一覧を表示します\n'+
                                        'violator <number>指定した回数以上ngワードを言った人を表示します。何も指定しないと0回以上になります。\n'+
                                        'purge:ngワードを言った回数をリセットします\n'+
                                        'help:helpを表示します。')


client.run(token)
