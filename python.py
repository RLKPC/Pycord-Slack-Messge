#Discord読み込み
import requests
import discord
from discord.ext import commands
from discord import option


bot = commands.Bot(
    command_prefix=".",
    case_insensitive=True,
    help_command=None,
    intents=discord.Intents.all()
)


slack_url = "https://slack.com/api/conversations.history"
slack_token = "すらっくとーくん"


#VTA-Check
@bot.slash_command(description="Slachのメッセージを出力します。")
@option("index",
        description="検索したいメッセージの数字を入力してください。",
        default="1"
        )


@option("sch",
        description="検索したいチャンネルを選択してください。）",
        choices=["TestChannel1",
                 "TestChannel2",
                 "TestChannel13",
                 "TestChannel4",
                 "TestChannel5"
                 ]
)
async def vtacheck(ctx,sch,index):

    channel_ids = {
                   "TestChannel1": "ちゃんねるあいでぃー",
                   "TestChannel2": "ちゃんねるあいでぃー",
                   "TestChannel3": "ちゃんねるあいでぃー",
                   "TestChannel4": "ちゃんねるあいでぃー",
                   "TestChannel5": "ちゃんねるあいでぃー"
                  }
    selected_channel_id = channel_ids[sch] 
    
    payload = {"channel": selected_channel_id}
    header = {"Authorization": "Bearer {}".format(slack_token)}

    index = int(index)
    res = requests.get(slack_url, headers=header, params=payload)
    data = res.json()

    if res.status_code == 200 and data["ok"]:
        if "messages" in data:
            message_count = len(data["messages"])
            
            if 1 <= index <= message_count:
                selected_message = data["messages"][index - 1]
                embed = discord.Embed(title=f"{sch}の{index}番目のメッセージを送信します。", color=discord.Color.green())
                embed.add_field(name="Text", value=selected_message["text"], inline=False)
                embed.add_field(name="User", value=selected_message["user"], inline=False)
                embed.add_field(name="Timestamp", value=selected_message["ts"], inline=False)
                await ctx.respond(embed=embed,ephemeral=True)
            else:
                await ctx.send("有効でないインデックス(番号)を入力されました。")
        else:
            await ctx.send("メッセージがレスポンス中に見つかリませんでした。")
    else:
        await ctx.send("メッセージ取得中にエラーが発生しました。")


bot.run("でぃすこーどとーくん")