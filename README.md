# RoWifi Alpha Modules

This repository contains sample modules for a Roblox verification bot built with **DSharpPlus** and examples in **Python** using
 `discord.py`.

## Available Modules

- `Blacklists.cs` – Provides commands to manage user, group, and custom blacklists within a guild.
- `bot.py` – Stand‑alone script demonstrating Roblox verification via prefix commands (`!verify`, `!update`) and slash commands
(`/verify`, `/update`). Verification codes arrive in embeds and include a helper button, with ephemeral channel responses when DMs are blocked.

## Building

These files are provided as examples and are not part of a complete project. To compile `Blacklists.cs`, integrate the module in
to your existing DSharpPlus bot project. For `bot.py`, install `discord.py` and `aiohttp` and run the script with `python bot.py`
 after setting the `DISCORD_BOT_TOKEN` environment variable.
