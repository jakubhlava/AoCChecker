# Advent of Code Leaderboard checker

A dead-simple script to notify about new stars on the [Advent of Code](https://adventofcode.com) leaderboard on our Discord server.

Apologies for Discord messages in Czech language without support for i18n. I am publishing this script primarily for the sake of transparency with AoC API usage.

## Configuration

Script is configured via environment variables:
```
    SESSION=... # AoC session cookie
    LEADERBOARD=... # AoC leaderboard ID
    DISCORD_WEBHOOK=... # Discord webhook URL
    EVENT=... # year (YYYY) - AoC event
```

## Usage

This script is meant to be run periodically, e.g. via cron:
```
    */20 * * * * /path/to/aoc-checker
```

Ensure you have created appropriate `venv` wherever are you going to run this script or install dependencies globally and install this package with `pip` from repository folder so that your cron user is able to launch the script.

## Contribution

This project was one-off fun solution for our small issue, created for our Discord group, but if you feel like it, you can use it or modify it for you purposes. 

Issues and pull requests are also welcome.

