import os
import random
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

pending_codes = {}


class VerifyView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                label="프로필 수정 방법",
                url="https://www.roblox.com/",
                style=discord.ButtonStyle.link,
            )
        )


async def get_roblox_description(username: str) -> str:
    url = f"https://api.roblox.com/users/get-by-username?username={username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            user_id = data.get("Id")
            if not user_id:
                return ""
        url = f"https://users.roblox.com/v1/users/{user_id}"
        async with session.get(url) as resp:
            profile = await resp.json()
            return profile.get("description", "")


async def start_verification(user: discord.User, roblox_username: str) -> str:
    code = str(random.randint(100000, 999999))
    pending_codes[user.id] = {"roblox_user": roblox_username, "code": code}
    return code


async def update_roles(member: discord.Member):
    data = pending_codes.get(member.id)
    if not data:
        return False, "먼저 `/verify` 또는 `!verify`로 코드를 발급받으세요."

    roblox_user = data["roblox_user"]
    code = data["code"]
    description = await get_roblox_description(roblox_user)

    if code in description:
        role = discord.utils.get(member.guild.roles, name="Verified")
        if role:
            await member.add_roles(role)
        pending_codes.pop(member.id, None)
        return True, f"인증 성공! 로블록스 계정: {roblox_user}"
    else:
        return False, "프로필에서 코드를 찾을 수 없습니다. 다시 시도해주세요."


@bot.command()
async def verify(ctx, roblox_username: str):
    code = await start_verification(ctx.author, roblox_username)
    embed = discord.Embed(
        title="Roblox Verification",
        description=(
            f"`{roblox_username}` 프로필 소개란에 아래 코드를 추가한 뒤 `!update` 또는 `/update` 명령을 실행하세요."
        ),
        color=discord.Color.blurple(),
    )
    embed.add_field(name="인증 코드", value=f"`{code}`", inline=False)
    await ctx.reply(embed=embed, mention_author=False, view=VerifyView())


@bot.command()
async def update(ctx):
    success, msg = await update_roles(ctx.author)
    color = discord.Color.green() if success else discord.Color.red()
    embed = discord.Embed(description=msg, color=color)
    await ctx.reply(embed=embed, mention_author=False)


@bot.tree.command(name="verify", description="로블록스 인증 시작")
@app_commands.describe(roblox_username="로블록스 사용자명")
async def slash_verify(interaction: discord.Interaction, roblox_username: str):
    code = await start_verification(interaction.user, roblox_username)
    embed = discord.Embed(
        title="Roblox Verification",
        description=(
            f"`{roblox_username}` 프로필 소개란에 아래 코드를 추가한 뒤 `/update` 명령을 실행하세요."
        ),
        color=discord.Color.blurple(),
    )
    embed.add_field(name="인증 코드", value=f"`{code}`", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True, view=VerifyView())


@bot.tree.command(name="update", description="인증된 역할 갱신")
async def slash_update(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("서버 내에서 실행해주세요.", ephemeral=True)
        return
    member = interaction.guild.get_member(interaction.user.id)
    success, msg = await update_roles(member)
    color = discord.Color.green() if success else discord.Color.red()
    embed = discord.Embed(description=msg, color=color)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


if __name__ == "__main__":
    bot.run(TOKEN)
