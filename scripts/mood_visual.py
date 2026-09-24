"""Quiet, Apple-inspired SVG compositions for the automated Mood Monitor."""

import textwrap
from html import escape


INK = "#F5F5F7"
SECONDARY = "#A7A7AE"
LINE = "#38383A"
BLUE = "#0A84FF"
RESULTS = {
    "W": ("#73DDA0", "#1B3A2B"),
    "D": ("#FFD078", "#43351C"),
    "L": ("#FF9292", "#442628"),
}


def _text(value: str) -> str:
    return escape(value)


def _outcome_marks(matches: list, y: int, first_x: int, step: int, size: int) -> str:
    marks = []
    for index in range(5):
        outcome = matches[index]["outcome"] if index < len(matches) else "–"
        ink, fill = RESULTS.get(outcome, ("#A7A7AE", "#303033"))
        x = first_x + index * step
        center = x + size / 2
        marks.append(f'<circle cx="{center}" cy="{y + size / 2}" r="{size / 2}" fill="{fill}"/>')
        marks.append(
            f'<text x="{center}" y="{y + size * .68:.1f}" text-anchor="middle" '
            f'font-size="{int(size * .46)}" font-weight="700" fill="{ink}">{outcome}</text>'
        )
    return "\n".join(marks)


def _description(score: int, status: str, barca: list, junior: list,
                 latest_fixture: str, generated_at: str) -> str:
    barca_form = " ".join(m["outcome"] for m in barca) or "N/A"
    junior_form = " ".join(m["outcome"] for m in junior) or "N/A"
    return _text(
        f"Mood score {score} out of 100, status {status}. "
        f"Barcelona {barca_form}; Junior {junior_form}. "
        f"Latest result {latest_fixture}; updated {generated_at}."
    )


def _status_size(status: str, mobile: bool = False) -> int:
    length = len(status)
    if mobile:
        return 34 if length > 13 else 40
    return 42 if length > 13 else 55 if length > 10 else 68


def render_desktop(score: int, status: str, quote: str, barca: list, junior: list,
                   latest_fixture: str, generated_at: str, snapshot: str) -> str:
    status_label = status.title()
    quote_lines = textwrap.wrap(quote, width=52, break_long_words=False)
    quote_svg = "\n".join(
        f'<text x="40" y="{216 + index * 21}" class="quote">{_text(line)}</text>'
        for index, line in enumerate(quote_lines[:2])
    )
    progress = round(680 * score / 100)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="468" viewBox="0 0 760 468" role="img" aria-labelledby="title desc" data-snapshot="{escape(snapshot, quote=True)}">
<title id="title">Matchday mood</title>
<desc id="desc">{_description(score, status, barca, junior, latest_fixture, generated_at)}</desc>
<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Arial, sans-serif; font-optical-sizing: auto; }}
.heading {{ font-size: 32px; font-weight: 650; letter-spacing: -1.1px; fill: {INK}; }}
.meta {{ font-size: 12px; font-weight: 600; letter-spacing: .5px; fill: {SECONDARY}; }}
.status {{ font-weight: 650; letter-spacing: -2px; fill: {INK}; }}
.score {{ font-size: 98px; font-weight: 650; letter-spacing: -4px; fill: {INK}; }}
.unit {{ font-size: 17px; font-weight: 550; fill: {SECONDARY}; }}
.quote {{ font-size: 17px; font-weight: 450; fill: #C6C6CC; }}
.team {{ font-size: 18px; font-weight: 650; letter-spacing: -.2px; fill: {INK}; }}
.league {{ font-size: 13px; fill: {SECONDARY}; }}
.foot {{ font-size: 12px; font-weight: 550; fill: {SECONDARY}; }}
</style>
<rect x="0.5" y="0.5" width="759" height="467" rx="25" fill="#1C1C1E" stroke="{LINE}"/>
<text x="40" y="57" class="heading">Matchday mood</text>
<text x="720" y="53" text-anchor="end" class="meta">BARCELONA × JUNIOR</text>
<path d="M40 84H720" stroke="{LINE}"/>
<text x="40" y="174" class="status" font-size="{_status_size(status)}">{_text(status_label)}.</text>
<text x="720" y="174" text-anchor="end" class="score">{score}</text>
<text x="720" y="200" text-anchor="end" class="unit">out of 100</text>
{quote_svg}
<rect x="40" y="264" width="680" height="7" rx="3.5" fill="#3A3A3C"/>
<rect x="40" y="264" width="{progress}" height="7" rx="3.5" fill="{BLUE}"/>
<path d="M40 293H720" stroke="{LINE}"/>
<text x="40" y="335" class="team">FC Barcelona</text>
<text x="40" y="353" class="league">LaLiga</text>
{_outcome_marks(barca, 311, 397, 67, 42)}
<text x="40" y="393" class="team">Junior FC</text>
<text x="40" y="411" class="league">BetPlay</text>
{_outcome_marks(junior, 369, 397, 67, 42)}
<path d="M40 424H720" stroke="{LINE}"/>
<text x="40" y="449" class="foot">Latest result · {_text(latest_fixture)}</text>
<text x="720" y="449" text-anchor="end" class="foot">Updated · {_text(generated_at)}</text>
</svg>
'''


def render_mobile(score: int, status: str, quote: str, barca: list, junior: list,
                  latest_fixture: str, generated_at: str, snapshot: str) -> str:
    status_label = status.title()
    quote_lines = textwrap.wrap(quote, width=42, break_long_words=False)
    quote_svg = "\n".join(
        f'<text x="24" y="{267 + index * 19}" class="quote">{_text(line)}</text>'
        for index, line in enumerate(quote_lines[:2])
    )
    progress = round(342 * score / 100)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="390" height="604" viewBox="0 0 390 604" role="img" aria-labelledby="title desc" data-snapshot="{escape(snapshot, quote=True)}">
<title id="title">Matchday mood</title>
<desc id="desc">{_description(score, status, barca, junior, latest_fixture, generated_at)}</desc>
<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Arial, sans-serif; font-optical-sizing: auto; }}
.heading {{ font-size: 29px; font-weight: 650; letter-spacing: -.9px; fill: {INK}; }}
.score {{ font-size: 105px; font-weight: 650; letter-spacing: -4px; fill: {INK}; }}
.unit {{ font-size: 15px; font-weight: 550; fill: {SECONDARY}; }}
.status {{ font-weight: 650; letter-spacing: -1px; fill: {INK}; }}
.quote {{ font-size: 14px; fill: #C6C6CC; }}
.team {{ font-size: 17px; font-weight: 650; fill: {INK}; }}
.league {{ font-size: 13px; fill: {SECONDARY}; }}
.foot {{ font-size: 11px; font-weight: 550; fill: {SECONDARY}; }}
</style>
<rect x="0.5" y="0.5" width="389" height="603" rx="23" fill="#1C1C1E" stroke="{LINE}"/>
<text x="24" y="51" class="heading">Matchday mood</text>
<path d="M24 73H366" stroke="{LINE}"/>
<text x="24" y="179" class="score">{score}</text>
<text x="{199 if score == 100 else 157}" y="175" class="unit">out of 100</text>
<text x="24" y="229" class="status" font-size="{_status_size(status, mobile=True)}">{_text(status_label)}.</text>
{quote_svg}
<rect x="24" y="318" width="342" height="7" rx="3.5" fill="#3A3A3C"/>
<rect x="24" y="318" width="{progress}" height="7" rx="3.5" fill="{BLUE}"/>
<path d="M24 348H366" stroke="{LINE}"/>
<text x="24" y="380" class="team">FC Barcelona</text>
<text x="366" y="380" text-anchor="end" class="league">LaLiga</text>
{_outcome_marks(barca, 394, 25, 70, 42)}
<text x="24" y="470" class="team">Junior FC</text>
<text x="366" y="470" text-anchor="end" class="league">BetPlay</text>
{_outcome_marks(junior, 484, 25, 70, 42)}
<path d="M24 547H366" stroke="{LINE}"/>
<text x="24" y="571" class="foot">Latest result · {_text(latest_fixture)}</text>
<text x="24" y="589" class="foot">Updated · {_text(generated_at)}</text>
</svg>
'''
