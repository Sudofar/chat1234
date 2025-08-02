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

async def start_verification(user: discord.User, roblox_username: str):
    code = str(random.randint(100000, 999999))
    pending_codes[user.id] = {"roblox_user": roblox_username, "code": code}
    await user.send(
        f"로블록스 계정 인증을 위해 아래 코드를 {roblox_username} 프로필 소개란에 추가한 뒤 `/update` 또는 `!update` 명령을 실행하세요.\n"
        f"인증 코드: `{code}`"
    )

async def update_roles(member: discord.Member):
    data = pending_codes.get(member.id)
    if not data:
        await member.send("먼저 `/verify` 또는 `!verify`로 코드를 발급받으세요.")
        return

    roblox_user = data["roblox_user"]
    code = data["code"]
    description = await get_roblox_description(roblox_user)

    if code in description:
        role = discord.utils.get(member.guild.roles, name="Verified")
        if role:
            await member.add_roles(role)
        await member.send(f"인증 성공! 로블록스 계정: {roblox_user}")
        pending_codes.pop(member.id, None)
    else:
        await member.send("프로필에서 코드를 찾을 수 없습니다. 다시 시도해주세요.")

@bot.command()
async def verify(ctx, roblox_username: str):
    await start_verification(ctx.author, roblox_username)
    await ctx.send(f"{ctx.author.mention} DM을 확인해주세요!")

@bot.command()
async def update(ctx):
    await update_roles(ctx.author)
    await ctx.send(f"{ctx.author.mention} 인증 확인을 시도했습니다. DM을 확인하세요.")

@bot.tree.command(name="verify", description="로블록스 인증 시작")
@app_commands.describe(roblox_username="로블록스 사용자명")
async def slash_verify(interaction: discord.Interaction, roblox_username: str):
    await start_verification(interaction.user, roblox_username)
    await interaction.response.send_message("DM을 확인해주세요!", ephemeral=True)

@bot.tree.command(name="update", description="인증된 역할 갱신")
async def slash_update(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("서버 내에서 실행해주세요.", ephemeral=True)
        return
    member = interaction.guild.get_member(interaction.user.id)
    await update_roles(member)
    await interaction.response.send_message("인증 확인을 시도했습니다. DM을 확인하세요.", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    bot.run(TOKEN)
