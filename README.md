# RoWifi Alpha Modules

This repository contains sample modules for a Roblox verification bot built with **DSharpPlus** and examples in **Python** using `discord.py`.

## Available Modules

- `Blacklists.cs` – Provides commands to manage user, group, and custom blacklists within a guild.
- `bot.py` – Stand‑alone script demonstrating Roblox verification via prefix commands (`!verify`, `!update`) and slash commands (`/verify`, `/update`). The bot tries to send verification codes by DM and falls back to an ephemeral embed in the channel when DMs are blocked. A helper button links to the Roblox site, and `/update` refreshes roles after the code is placed in the profile.

## Building

These files are provided as examples and are not part of a complete project. To compile `Blacklists.cs`, integrate the module into your existing DSharpPlus bot project.

## Running the sample bot

1. Install requirements: `pip install discord.py aiohttp`
2. Set the `DISCORD_BOT_TOKEN` environment variable with your bot token.
3. Run the script with `python bot.py`.
4. Use `!verify <RobloxUser>` or `/verify roblox_username:<RobloxUser>` to receive a verification code.
5. Add the code to the Roblox profile description and run `!update` or `/update` to receive the `Verified` role.

