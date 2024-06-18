import discord
import os
from discord import Intents, Client, Interaction
from discord.app_commands import CommandTree
from keep_alive import keep_alive

class MyClient(Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)
        self.tree = CommandTree(self)
        
    async def setup_hook(self) -> None:
        await self.tree.sync()

intents = Intents.all()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.tree.command()
async def hello(interaction: Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$reaction'):
        emoji ="👍"
        await message.add_reaction(emoji)
        
# 募集テンプレート　コマンド
rankEmoji = {"アイアン": ":iron:", "ブロンズ": ":bronze:", "シルバー": ":silver:", "ゴールド": ":gold:", "プラチナ": ":platinum:",
             "ダイヤモンド": ":diamond:", "アセンダント": ":ascendant:", "イモータル": ":immortal:", "レディアント": ":radiant:"}
@client.tree.command(name="rank_recruit",description="ランク募集用テンプレートを作ります。")
async def rank_recruit(interaction: Interaction, lowest_role: discord.Role, highest_role: discord.Role, amount: int):
    if (lowest_role.name in rankEmoji) and (highest_role.name in rankEmoji):
        lowestRankEmoji = rankEmoji[lowest_role.name]
        highestRankEmoji = rankEmoji[highest_role.name]
        await interaction.response.send_message(f"{interaction.user.mention} からのコンペ募集が来ました！ \n ランク: {lowest_role.name}{lowestRankEmoji} - {highest_role.name}{highestRankEmoji} \n 人数: @{amount}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} エラーが発生しました。もう一度試すか、ランクのロールを指定してください。", ephemeral=True)



# 観戦モード　コマンド
class SampleView(discord.ui.View): # 観戦ボタンのview
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="観戦モード ON", style=discord.ButtonStyle.success)
    async def observe_on(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_nick = interaction.user.nick or interaction.user.global_name
        if ' //' in user_nick:
            await interaction.response.send_message(f"{interaction.user.mention} すでに観戦中です！", ephemeral=True)
        else:
            try:
                await interaction.user.edit(nick=user_nick + " //観戦中")
                await interaction.response.send_message(f"{interaction.user.mention} 観戦モードにしました！", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message(f"{interaction.user.mention} ごめんね。僕たちが持つ権限が不足しています。自分で名前変えてね！", ephemeral=True)

    @discord.ui.button(label="観戦モード OFF", style=discord.ButtonStyle.danger)
    async def observe_off(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_nick = interaction.user.nick or interaction.user.global_name
        if ' //' in user_nick:
            try: 
                new_nick = user_nick.split(" //")[0]
                await interaction.user.edit(nick=new_nick)
                await interaction.response.send_message(f"{interaction.user.mention} 観戦モードを解除しました！", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message(f"{interaction.user.mention} ごめんね。僕たちが持つ権限が不足しています。自分で名前変えてね！", ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} 観戦モードではありません！", ephemeral=True)

@client.tree.command(name="observer_button", description="観戦モード ON/OFFを追加します")
async def observer_button(interaction: Interaction):
    view = SampleView(timeout=None)
    await interaction.response.send_message(content="観戦モード設定", view=view)

TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)

