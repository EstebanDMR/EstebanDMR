#!/usr/bin/env python3
"""
The Mood Engine — Automated Football-Driven Developer Mood Telemetry
Author: Esteban Mercado Rachath (@EstebanDMR)

Fetches recent match outcomes for FC Barcelona and Junior FC via ESPN Web API,
computes a normalized mood score (0-100), and renders desktop/mobile SVG cards.
The README image reference stays between <!-- MOOD_START --> and <!-- MOOD_END -->.
Zero external dependencies — built entirely on the Python standard library.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

if __package__:
    from . import mood_visual
else:
    import mood_visual

# Ensure UTF-8 output across standard streams
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Configuration & Team IDs
TEAMS = {
    "barcelona": {
        "name": "FC BARCELONA",
        "league_code": "all",
        "team_id": 83,
    },
    "junior": {
        "name": "JUNIOR FC",
        "league_code": "all",
        "team_id": 4815,
    },
}

# Dynamic states calibrated to fit cleanly in a 64-column card
MOOD_STATES = [
    {
        "min": 90,
        "max": 100,
        "status": "UNSTOPPABLE",
        "quote": "Tactical masterclass. High spirits all around.",
    },
    {
        "min": 75,
        "max": 89,
        "status": "HAPPY",
        "quote": "Football is treating us well. High morale.",
    },
    {
        "min": 60,
        "max": 74,
        "status": "GOOD",
        "quote": "Holding ground. Steady pulse, shipping code.",
    },
    {
        "min": 45,
        "max": 59,
        "status": "SURVIVING",
        "quote": "Grinding through fixtures and edge cases.",
    },
    {
        "min": 25,
        "max": 44,
        "status": "NOT GREAT",
        "quote": "Tough fixtures. Seeking refuge in code.",
    },
    {
        "min": 0,
        "max": 24,
        "status": "DO NOT DISTURB",
        "quote": "Weekend redacted. Compiling in total silence.",
    },
]

DISPLAY_STATES = [
    (9, "UNSTOPPABLE", "The results are in. Energy is high."),
    (7, "GOOD", "A good run. Ready for the next challenge."),
    (5, "STEADY", "Mixed results. Keeping a steady pace."),
    (3, "NOT GREAT", "A rough stretch. Still showing up."),
    (1, "MATCHDAY BLUES", "Rough matchday. Still ready to build."),
]

HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_team_schedule(league_code: str, team_id: int) -> dict:
    """Fetch official schedule payload from ESPN web API."""
    url = f"https://site.web.api.espn.com/apis/site/v2/sports/soccer/{league_code}/teams/{team_id}/schedule"
    req = urllib.request.Request(url, headers=HTTP_HEADERS)
    with urllib.request.urlopen(req, timeout=12) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP error {response.status} fetching schedule for team {team_id}")
        return json.loads(response.read().decode("utf-8"))


def parse_completed_matches(data: dict, team_id: int, limit: int = 5) -> list:
    """
    Parse completed matches, sort chronologically, and extract W/D/L outcomes.
    Returns list of matches sorted oldest to newest (e.g. left-to-right form).
    """
    events = data.get("events", [])
    completed = []

    for event in events:
        competitions = event.get("competitions", [])
        if not competitions:
            continue
        comp = competitions[0]
        status = comp.get("status", {}).get("type", {})
        if not status.get("completed", False):
            continue

        competitors = comp.get("competitors", [])
        our_team = next((c for c in competitors if str(c.get("id")) == str(team_id)), None)
        opp_team = next((c for c in competitors if str(c.get("id")) != str(team_id)), None)

        if not our_team or not opp_team:
            continue

        def parse_score(val):
            if isinstance(val, dict):
                return int(val.get("value", 0))
            return int(val or 0)

        our_score = parse_score(our_team.get("score"))
        opp_score = parse_score(opp_team.get("score"))

        if our_score > opp_score:
            outcome = "W"
        elif our_score == opp_score:
            outcome = "D"
        else:
            outcome = "L"

        completed.append({
            "date": event.get("date", ""),
            "outcome": outcome,
            "score": f"{our_score}-{opp_score}",
            "opponent": opp_team.get("team", {}).get("displayName", "Opponent"),
        })

    # Sort descending by date to obtain the most recent matches
    completed.sort(key=lambda x: x["date"], reverse=True)
    recent = completed[:limit]

    # Reverse to present chronologically from left to right (oldest -> newest)
    recent.reverse()
    return recent


def calculate_mood(barca_matches: list, junior_matches: list) -> tuple:
    """
    Compute points, normalized 0-100 score, active status, and quote.
    Win = +2, Draw = 0, Loss = -2
    Min points = -20 (10 losses), Max points = +20 (10 wins).
    Range: 40 points -> normalized: round(((points + 20) / 40) * 100).
    """
    point_map = {"W": 2, "D": 0, "L": -2}

    barca_outcomes = [m["outcome"] for m in barca_matches]
    junior_outcomes = [m["outcome"] for m in junior_matches]
    all_outcomes = barca_outcomes + junior_outcomes

    if not all_outcomes:
        return 50, "STABLE", "Telemetry unavailable. Maintaining nominal baseline."

    total_points = sum(point_map.get(o, 0) for o in all_outcomes)

    normalized_score = round(((total_points + 20) / 40) * 100)
    normalized_score = max(0, min(100, normalized_score))

    selected_state = MOOD_STATES[-1]
    for state in MOOD_STATES:
        if state["min"] <= normalized_score <= state["max"]:
            selected_state = state
            break

    return normalized_score, selected_state["status"], selected_state["quote"]


def display_mood(raw_score: int) -> tuple:
    """Map the existing score to the playful 1–10 display and five states."""
    value = max(1, min(10, 1 + round(9 * raw_score / 100)))
    for minimum, status, quote in DISPLAY_STATES:
        if value >= minimum:
            return value, status, quote
    raise AssertionError("No display state matched")


def get_latest_fixture_date(barca_matches: list, junior_matches: list) -> str:
    """Find the most recent completed fixture date across both clubs."""
    dates = [m["date"] for m in barca_matches + junior_matches if m.get("date")]
    if not dates:
        return "N/A"

    latest_iso = max(dates)
    try:
        # e.g., '2026-09-20T21:10Z'
        cleaned = latest_iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        return dt.strftime("%d %b %Y").upper()
    except Exception:
        return latest_iso[:10]


def snapshot_key(barca_matches: list, junior_matches: list) -> str:
    """Track results and visual revisions without timestamp-only commits."""
    rows = [[m["date"], m["outcome"], m["score"]] for m in barca_matches + junior_matches]
    return json.dumps({"visual": 9, "matches": rows}, ensure_ascii=True, separators=(",", ":"))


def generate_dashboard(score: int, status: str, quote: str, barca_matches: list,
                       junior_matches: list, latest_fixture: str, generated_at: str) -> str:
    """Render the desktop SVG while preserving the public engine interface."""
    return mood_visual.render_desktop(
        score, status, quote, barca_matches, junior_matches,
        latest_fixture, generated_at, snapshot_key(barca_matches, junior_matches),
        total=10
    )


def generate_mobile_dashboard(score: int, status: str, quote: str, barca_matches: list,
                              junior_matches: list, latest_fixture: str, generated_at: str) -> str:
    """Render the phone composition from the same match data."""
    return mood_visual.render_mobile(
        score, status, quote, barca_matches, junior_matches,
        latest_fixture, generated_at, snapshot_key(barca_matches, junior_matches),
        total=10
    )


def update_readme(score: int, status: str, barca_matches: list, junior_matches: list,
                  readme_path: str = "README.md") -> bool:
    """Keep the image reference within the existing generated section markers."""
    path = Path(readme_path)
    if not path.is_file():
        raise FileNotFoundError(f"Target README not found: {path}")
    original = path.read_text(encoding="utf-8")
    pattern = r"<!-- MOOD_START -->.*?<!-- MOOD_END -->"
    if not re.search(pattern, original, flags=re.DOTALL):
        raise ValueError("Mood markers not found in README")
    barca_form = " ".join(m["outcome"] for m in barca_matches) or "N/A"
    junior_form = " ".join(m["outcome"] for m in junior_matches) or "N/A"
    alt = escape(f"Mood Monitor: {score}/10, {status}. Barcelona {barca_form}; Junior {junior_form}.", quote=True)
    image = ('<picture>\n'
             '  <source media="(max-width: 600px)" srcset="assets/mood-monitor-mobile.svg" />\n'
             f'  <img src="assets/mood-monitor.svg" alt="{alt}" />\n'
             '</picture>')
    replacement = f"<!-- MOOD_START -->\n{image}\n<!-- MOOD_END -->"
    updated = re.sub(pattern, replacement, original, flags=re.DOTALL)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def update_svg(svg_content: str, svg_path: Path, key: str) -> bool:
    """Write the card only when the match snapshot differs."""
    if svg_path.is_file():
        current = svg_path.read_text(encoding="utf-8")
        if f'data-snapshot="{escape(key, quote=True)}"' in current:
            return False
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg_content, encoding="utf-8")
    return True


def run(readme_path: str = "README.md") -> int:
    """Main execution flow with fault isolation."""
    print("=== The Mood Engine: Updating Football Results ===")
    try:
        # 1. Fetch FC Barcelona schedule
        print("Fetching FC Barcelona fixtures across competitions...")
        barca_data = fetch_team_schedule(
            TEAMS["barcelona"]["league_code"], TEAMS["barcelona"]["team_id"]
        )
        barca_matches = parse_completed_matches(barca_data, TEAMS["barcelona"]["team_id"], limit=5)
        print(f"  -> Extracted {len(barca_matches)} completed matches: {[m['outcome'] for m in barca_matches]}")

        # 2. Fetch Junior FC schedule
        print("Fetching Junior FC fixtures across competitions...")
        junior_data = fetch_team_schedule(
            TEAMS["junior"]["league_code"], TEAMS["junior"]["team_id"]
        )
        junior_matches = parse_completed_matches(junior_data, TEAMS["junior"]["team_id"], limit=5)
        print(f"  -> Extracted {len(junior_matches)} completed matches: {[m['outcome'] for m in junior_matches]}")

        if not barca_matches and not junior_matches:
            print("Warning: No match records parsed. Skipping README modification to preserve integrity.")
            return 0

        # 3. Calculate mood metrics
        raw_score, _, _ = calculate_mood(barca_matches, junior_matches)
        score, status, quote = display_mood(raw_score)
        print(f"\nCalculated Mood Score: {raw_score}/100 → {score}/10 | Status: {status}")
        print(f"Quote: \"{quote}\"")

        # 4. Render the card; the timestamp changes only when results change.
        latest_fixture = get_latest_fixture_date(barca_matches, junior_matches)
        generated_at = datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC").upper()
        svg = generate_dashboard(score, status, quote, barca_matches, junior_matches,
                                 latest_fixture, generated_at)
        mobile_svg = generate_mobile_dashboard(score, status, quote, barca_matches,
                                               junior_matches, latest_fixture, generated_at)
        svg_path = Path(readme_path).parent / "assets" / "mood-monitor.svg"
        readme_modified = update_readme(score, status, barca_matches, junior_matches, readme_path)
        svg_modified = update_svg(svg, svg_path, snapshot_key(barca_matches, junior_matches))
        mobile_modified = update_svg(mobile_svg, svg_path.with_name("mood-monitor-mobile.svg"),
                                     snapshot_key(barca_matches, junior_matches))
        print(f"Mood cards {'updated' if svg_modified or mobile_modified else 'unchanged'}; README {'updated' if readme_modified else 'unchanged'}.")
        print("=== Mood Engine completed successfully. ===")
        return 0

    except urllib.error.URLError as e:
        print(f"Network error accessing football telemetry API: {e}", file=sys.stderr)
        print("Safely bypassing update to prevent README corruption.")
        return 0
    except Exception as e:
        print(f"Unexpected error in Mood Engine: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    target_readme = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    sys.exit(run(target_readme))
