"""Self-contained dark SVG compositions for the automated Mood Monitor."""

import base64
import math
import textwrap
from html import escape
from pathlib import Path


INK = "#F5F5F7"
MUTED = "#B9B9C0"
LINE = "#35353A"
BACKGROUND = "#171719"
RESULTS = {
    "W": ("#66DB91", "#2E794A"),
    "D": ("#F1C76B", "#8A6831"),
    "L": ("#F07D80", "#904446"),
}


def _text(value: str) -> str:
    return escape(str(value))


def _crest(name: str) -> str:
    """Embed logos so GitHub's image proxy needs no secondary image requests."""
    path = Path(__file__).resolve().parent.parent / "assets" / f"{name}-crest.png"
    return base64.b64encode(path.read_bytes()).decode("ascii")


def _description(score: int, status: str, barca: list, junior: list,
                 latest_fixture: str, generated_at: str, total: int = 100) -> str:
    barca_form = " ".join(m["outcome"] for m in barca) or "N/A"
    junior_form = " ".join(m["outcome"] for m in junior) or "N/A"
    return _text(
        f"Mood score {score} of {total}, status {status}. "
        f"Barcelona {barca_form}; Junior {junior_form}. "
        f"Latest result {latest_fixture}; updated {generated_at}."
    )


def _mood_color(score: int) -> str:
    if score >= 60:
        return "#69DB8B"
    if score >= 45:
        return "#F1C76B"
    return "#F07D80"


def _face_shapes(score: int, cx: int, cy: int, color: str) -> str:
    if score >= 90:
        eyes = (
            f'<path d="M{cx - 20} {cy - 8} Q{cx - 13} {cy - 17} {cx - 6} {cy - 8} '
            f'M{cx + 6} {cy - 8} Q{cx + 13} {cy - 17} {cx + 20} {cy - 8}" '
            f'stroke="{color}" stroke-width="3" stroke-linecap="round" fill="none"/>'
        )
    elif score < 25:
        eyes = (
            f'<path d="M{cx - 19} {cy - 13} l12 5 M{cx + 19} {cy - 13} l-12 5" '
            f'stroke="{color}" stroke-width="3" stroke-linecap="round" fill="none"/>'
        )
    else:
        eyes = (
            f'<circle cx="{cx - 13}" cy="{cy - 7}" r="2.5" fill="{color}"/>'
            f'<circle cx="{cx + 13}" cy="{cy - 7}" r="2.5" fill="{color}"/>'
        )
    if score >= 90:
        mouth = f'M{cx - 19} {cy + 8} Q{cx} {cy + 31} {cx + 19} {cy + 8}'
    elif score >= 75:
        mouth = f'M{cx - 18} {cy + 8} Q{cx} {cy + 26} {cx + 18} {cy + 8}'
    elif score >= 65:
        mouth = f'M{cx - 15} {cy + 10} Q{cx} {cy + 21} {cx + 15} {cy + 10}'
    elif score >= 60:
        mouth = f'M{cx - 12} {cy + 12} Q{cx} {cy + 17} {cx + 12} {cy + 12}'
    elif score >= 45:
        mouth = f'M{cx - 13} {cy + 13} H{cx + 13}'
    elif score >= 25:
        mouth = f'M{cx - 16} {cy + 18} Q{cx} {cy + 1} {cx + 16} {cy + 18}'
    else:
        mouth = f'M{cx - 14} {cy + 17} Q{cx} {cy + 5} {cx + 14} {cy + 17}'
    return (
        f'<g aria-hidden="true">{eyes}<path d="{mouth}" fill="none" '
        f'stroke="{color}" stroke-width="3.2" stroke-linecap="round"/></g>'
    )


def _meter(score: int, cx: int, cy: int, radius: int) -> str:
    color = _mood_color(score)
    circumference = 2 * math.pi * radius
    filled = circumference * max(0, min(score, 100)) / 100
    arc = (
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
        f'stroke="{color}" stroke-width="9" stroke-linecap="round" '
        f'stroke-dasharray="{filled:.2f} {circumference:.2f}" '
        f'transform="rotate(-90 {cx} {cy})"/>'
        if score > 0 else ""
    )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
        f'stroke="#353539" stroke-width="9"/>'
        + arc
        + _face_shapes(score, cx, cy, color)
    )


def _result_marks(matches: list, centers: list[int], cy: int, radius: int) -> str:
    marks = []
    for index, cx in enumerate(centers):
        outcome = matches[index]["outcome"] if index < len(matches) else "–"
        color, subtle = RESULTS.get(outcome, (MUTED, "#626269"))
        marks.extend((
            f'<circle cx="{cx}" cy="{cy}" r="{radius + 2}" fill="none" '
            f'stroke="{color}" stroke-opacity=".54" stroke-width="3" filter="url(#result-glow)"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#222226" '
            f'stroke="{subtle}" stroke-width="1.5"/>',
            f'<text x="{cx}" y="{cy + radius * .34:.1f}" text-anchor="middle" '
            f'font-size="{int(radius * .83)}" font-weight="700" fill="{color}">{outcome}</text>',
        ))
    return "\n".join(marks)


def _team_badge(name: str, cx: int, cy: int, radius: int) -> str:
    if name == "barcelona":
        first, second = "#A60B35", "#2962B8"
    else:
        first, second = "#D52238", "#F1F1F1"
    size = radius * 1.65
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{radius + 3}" fill="#29292D"/>'
        f'<path d="M{cx} {cy - radius} A{radius} {radius} 0 0 1 {cx} {cy + radius}" '
        f'fill="none" stroke="{first}" stroke-width="3.2"/>'
        f'<path d="M{cx} {cy + radius} A{radius} {radius} 0 0 1 {cx} {cy - radius}" '
        f'fill="none" stroke="{second}" stroke-width="3.2"/>'
        f'<image x="{cx - size/2:.1f}" y="{cy - size/2:.1f}" width="{size:.1f}" '
        f'height="{size:.1f}" href="data:image/png;base64,{_crest(name)}"/>'
    )


def _base_style() -> str:
    return f'''<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; }}
.heading {{ font-size: 30px; font-weight: 650; letter-spacing: -1px; fill: {INK}; }}
.score {{ font-size: 99px; font-weight: 700; letter-spacing: -4px; fill: {INK}; }}
.denominator {{ font-size: 23px; font-weight: 600; fill: {MUTED}; }}
.status {{ font-size: 18px; font-weight: 650; fill: {INK}; }}
.quote {{ font-size: 16px; fill: {MUTED}; }}
.team {{ font-size: 18px; font-weight: 650; fill: {INK}; }}
.foot {{ font-size: 12px; fill: {MUTED}; }}
.fun {{ font-size: 11px; font-weight: 700; letter-spacing: 1px; fill: #A7A7AE; }}
</style>
<defs><filter id="result-glow" x="-80%" y="-80%" width="260%" height="260%">
<feGaussianBlur stdDeviation="4"/></filter></defs>'''


def render_desktop(score: int, status: str, quote: str, barca: list, junior: list,
                   latest_fixture: str, generated_at: str, snapshot: str,
                   total: int = 100) -> str:
    score_text = str(score)
    denominator_x = 218 if score == 100 else 158 if score >= 10 else 102
    quote_lines = textwrap.wrap(quote, width=50, break_long_words=False)
    quotes = "".join(
        f'<text x="42" y="{246 + i * 20}" class="quote">{_text(line)}</text>'
        for i, line in enumerate(quote_lines[:2])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="468" viewBox="0 0 760 468" role="img" aria-labelledby="title desc" data-snapshot="{escape(snapshot, quote=True)}">
<title id="title">Matchday mood</title>
<desc id="desc">{_description(score, status, barca, junior, latest_fixture, generated_at, total)}</desc>
{_base_style()}
<rect x=".5" y=".5" width="759" height="467" rx="24" fill="{BACKGROUND}" stroke="{LINE}"/>
<text x="42" y="61" class="heading">Matchday mood</text>
<text x="718" y="55" text-anchor="end" class="fun">JUST FOR FUN</text>
<path d="M42 84H718" stroke="{LINE}"/>
<text x="42" y="192" class="score">{score_text}</text>
<text x="{denominator_x}" y="184" class="denominator">/{total}</text>
<text x="43" y="218" class="status">{_text(status.title())}</text>
{quotes}
{_meter(round(score * 100 / total), 626, 186, 59)}
<path d="M42 287H718" stroke="{LINE}"/>
{_team_badge("barcelona", 66, 332, 24)}
<text x="106" y="339" class="team">FC Barcelona</text>
{_result_marks(barca, [418, 480, 542, 604, 666], 332, 18)}
<path d="M42 365H718" stroke="#2C2C30"/>
{_team_badge("junior", 66, 397, 24)}
<text x="106" y="404" class="team">Junior FC</text>
{_result_marks(junior, [418, 480, 542, 604, 666], 397, 18)}
<path d="M42 429H718" stroke="{LINE}"/>
<text x="42" y="451" class="foot">Latest result · {_text(latest_fixture)}</text>
<text x="718" y="451" text-anchor="end" class="foot">Updated · {_text(generated_at)}</text>
</svg>
'''


def render_mobile(score: int, status: str, quote: str, barca: list, junior: list,
                  latest_fixture: str, generated_at: str, snapshot: str,
                  total: int = 100) -> str:
    denominator_x = 185 if score == 100 else 129 if score >= 10 else 80
    quote_lines = textwrap.wrap(quote, width=40, break_long_words=False)
    quotes = "".join(
        f'<text x="25" y="{247 + i * 19}" class="quote" style="font-size:14px">{_text(line)}</text>'
        for i, line in enumerate(quote_lines[:2])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="390" height="594" viewBox="0 0 390 594" role="img" aria-labelledby="title desc" data-snapshot="{escape(snapshot, quote=True)}">
<title id="title">Matchday mood</title>
<desc id="desc">{_description(score, status, barca, junior, latest_fixture, generated_at, total)}</desc>
{_base_style()}
<rect x=".5" y=".5" width="389" height="593" rx="23" fill="{BACKGROUND}" stroke="{LINE}"/>
<text x="25" y="53" class="heading">Matchday mood</text>
<text x="365" y="49" text-anchor="end" class="fun">JUST FOR FUN</text>
<path d="M25 74H365" stroke="{LINE}"/>
<text x="25" y="177" class="score" style="font-size:91px">{score}</text>
<text x="{denominator_x}" y="170" class="denominator" style="font-size:18px">/{total}</text>
{_meter(round(score * 100 / total), 303, 157, 50)}
<text x="25" y="217" class="status">{_text(status.title())}</text>
{quotes}
<path d="M25 292H365" stroke="{LINE}"/>
{_team_badge("barcelona", 48, 325, 21)}
<text x="85" y="331" class="team" style="font-size:17px">FC Barcelona</text>
{_result_marks(barca, [47, 115, 183, 251, 319], 383, 19)}
<path d="M25 422H365" stroke="#2C2C30"/>
{_team_badge("junior", 48, 456, 21)}
<text x="85" y="462" class="team" style="font-size:17px">Junior FC</text>
{_result_marks(junior, [47, 115, 183, 251, 319], 514, 19)}
<path d="M25 550H365" stroke="{LINE}"/>
<text x="25" y="568" class="foot" style="font-size:11px">Latest result · {_text(latest_fixture)}</text>
<text x="25" y="584" class="foot" style="font-size:11px">Updated · {_text(generated_at)}</text>
</svg>
'''
