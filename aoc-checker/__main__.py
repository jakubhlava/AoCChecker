import os
import time
from datetime import datetime, timezone, timedelta
import requests
import json
from dotenv import load_dotenv

load_dotenv()


def parse_data(data):
    users = {}
    for user in data["members"].values():
        parsed = {
            "name": user["name"],
            "stars": user["stars"],
            "newest": user["last_star_ts"],
            "days": {
                day: {
                    "1": datetime.fromtimestamp(
                        user["completion_day_level"][day]["1"]["get_star_ts"],
                        tz=timezone(timedelta(hours=1)),
                    ).strftime("%d. %m. %Y v %H:%M:%S"),
                    "2": datetime.fromtimestamp(
                        user["completion_day_level"][day]["2"]["get_star_ts"],
                        tz=timezone(timedelta(hours=1)),
                    ).strftime("%d. %m. %Y v %H:%M:%S")
                    if "2" in user["completion_day_level"][day].keys()
                    else None,
                }
                for day in sorted(user["completion_day_level"].keys())
            },
        }
        users[user["id"]] = parsed
    return users


with open(
    os.path.join(os.path.dirname(__file__), "saved.json"), "r", encoding="utf-8"
) as f:
    old_data = json.load(f)

s = requests.session()
s.cookies.set("session", os.getenv("SESSION"), domain="adventofcode.com")
new_data = s.get(
    f"https://adventofcode.com/{os.getenv('EVENT')}/leaderboard/private/view/{os.getenv('LEADERBOARD')}.json",
    headers={
        "User-Agent": "https://github.com/jakubhlava/AoCChecker by j.hlava (at) post.cz"
    },
).json()


parsed_data = parse_data(old_data)
new_parsed_data = parse_data(new_data)

for user_id in parsed_data.keys():
    fields = []
    if parsed_data[user_id]["newest"] != new_parsed_data[user_id]["newest"]:
        for d in new_parsed_data[user_id]["days"].keys():
            field = {"name": f"Den {d}"}
            if d not in parsed_data[user_id]["days"].keys():
                field[
                    "value"
                ] = f"**Část 1:** {new_parsed_data[user_id]['days'][d]['1']}\n"
                if new_parsed_data[user_id]["days"][d]["2"]:
                    field[
                        "value"
                    ] += f"**Část 2:** {new_parsed_data[user_id]['days'][d]['2']}"
                fields.append(field)
            else:
                if (
                    new_parsed_data[user_id]["days"][d]["2"]
                    and not parsed_data[user_id]["days"][d]["2"]
                ):
                    field[
                        "value"
                    ] = f"**Část 2:** {new_parsed_data[user_id]['days'][d]['2']}"
                    fields.append(field)
    if parsed_data[user_id]["stars"] != new_parsed_data[user_id]["stars"]:
        field = {
            "name": "Hvězdy",
            "value": f'{parsed_data[user_id]["stars"]} => **{new_parsed_data[user_id]["stars"]}**',
        }
        fields.append(field)

    if fields:
        request_data = {
            "embeds": [
                {
                    "color": 0xFCCF03,
                    "title": f"Paráda! {new_parsed_data[user_id]['name']} splnil další úkoly",
                    "fields": fields,
                    "footer": {
                        "text": f"Stav k {datetime.now(timezone(timedelta(hours=1))).strftime('%d. %m. %Y %H:%M:%S')}"
                    },
                }
            ],
            "username": "Advent of Code",
        }
        result = requests.post(
            os.getenv("WEBHOOK_CALLBACK_URL"),
            json=request_data,
            headers={"Content-Type": "application/json"},
        )
        time.sleep(0.5)

with open(os.path.join(os.path.dirname(__file__), "saved.json"), "w") as f:
    json.dump(new_data, f)
