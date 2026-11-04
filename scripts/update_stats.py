"""Update the stats badges in profile/README.md from OSTDB's all-games.json."""
import json
import re
import urllib.request
from pathlib import Path

DATA_URL = "https://raw.githubusercontent.com/OSTDB/soundtracks/main/all-games.json"
README = Path(__file__).resolve().parent.parent / "profile" / "README.md"


def badge(label: str, value: int, color: str, link: str) -> str:
    text = f"{value:,}"
    encoded = text.replace(",", "%2C")
    return (
        f'<a href="{link}"><img alt="{label}: {text}" '
        f'src="https://img.shields.io/badge/{label}-{encoded}-{color}'
        f'?style=for-the-badge&labelColor=161718" /></a>'
    )


def main() -> None:
    with urllib.request.urlopen(DATA_URL, timeout=60) as resp:
        data = json.load(resp)

    soundtracks = int(data["total_soundtracks"])
    games = len(data["games"])

    block = "\n".join([
        "<!-- STATS:START -->",
        "<p>",
        badge("soundtracks", soundtracks, "E2B714", "https://ostdb.net"),
        badge("games", games, "ECECEE", "https://github.com/OSTDB/soundtracks/tree/main/games"),
        "</p>",
        "<!-- STATS:END -->",
    ])

    text = README.read_text(encoding="utf-8")
    new = re.sub(r"<!-- STATS:START -->.*?<!-- STATS:END -->", block, text, flags=re.S)
    if new == text:
        print("No change.")
        return
    README.write_text(new, encoding="utf-8")
    print(f"Updated: {soundtracks} soundtracks, {games} games.")


if __name__ == "__main__":
    main()
