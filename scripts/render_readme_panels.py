#!/usr/bin/env python3
"""Render self-contained Technical Stack panels for the GitHub README.

Logo artwork in assets/skill-icons comes from https://skillicons.dev/.
The generated SVGs embed that artwork and need no external image requests.
"""

from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ICONS = ASSETS / "skill-icons"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

# Title, visible logos, display lines, complete accessible technology list.
STACK = [
    ("Languages", ["ts", "js", "py"],
     ["TypeScript · JavaScript", "Python · SQL"],
     ["TypeScript", "JavaScript", "Python", "SQL"]),
    ("Frontend", ["react", "tailwind", "vite"],
     ["React · Tailwind CSS", "Vite · Lucide React"],
     ["React", "Tailwind CSS", "Vite", "Lucide React"]),
    ("Backend", ["nodejs", "express", "prisma"],
     ["Node.js · Express.js", "Prisma ORM · REST APIs", "JWT · Zod"],
     ["Node.js", "Express.js", "Prisma ORM", "REST APIs", "JWT", "Zod"]),
    ("Databases", ["postgres", "firebase"],
     ["PostgreSQL", "Firebase Realtime", "Database"],
     ["PostgreSQL", "Firebase Realtime Database"]),
    ("Data / Analytics", ["py"],
     ["Pandas · Matplotlib", "Seaborn · Streamlit", "Jupyter"],
     ["Pandas", "Matplotlib", "Seaborn", "Streamlit", "Jupyter"]),
    ("Testing", ["vitest", "jest"],
     ["Vitest · Jest", "Supertest"],
     ["Vitest", "Jest", "Supertest"]),
    ("DevOps", ["docker", "githubactions", "vercel"],
     ["Docker · GitHub Actions", "Vercel · Render"],
     ["Docker", "GitHub Actions", "Vercel", "Render"]),
    ("Tooling", ["git", "postman"],
     ["Git · Postman", "Swagger / OpenAPI"],
     ["Git", "Postman", "Swagger / OpenAPI"]),
]


def icon(slug: str, x: int, y: int, size: int) -> str:
    file = ICONS / f"{slug}.svg"
    if not file.is_file():
        raise FileNotFoundError(f"Missing Skill Icons source: {file}")
    root = ET.parse(file).getroot()
    root.set("x", str(x))
    root.set("y", str(y))
    root.set("width", str(size))
    root.set("height", str(size))
    root.set("aria-hidden", "true")
    return ET.tostring(root, encoding="unicode")


def frame(width: int, height: int, description: str, content: str) -> str:
    return f'''<svg xmlns="{SVG_NS}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Technical stack</title>
<desc id="desc">{escape(description)}</desc>
<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; }}
.heading {{ fill: #F5F5F7; font-size: 17px; font-weight: 650; letter-spacing: -.3px; }}
.body {{ fill: #C6C6CC; font-size: 14px; font-weight: 450; }}
</style>
{content}
</svg>
'''


def stack_card(index: int, x: int, y: int, width: int, height: int,
               *, mobile: bool = False) -> str:
    title, icons, lines, _ = STACK[index]
    inset = 18 if mobile else 17
    parts = [
        (f'<rect x="{x + .5}" y="{y + .5}" width="{width - 1}" '
         f'height="{height - 1}" rx="16" fill="#171719" stroke="#35353A"/>'),
        f'<text x="{x + inset}" y="{y + 29}" class="heading">{escape(title)}</text>',
    ]
    if mobile:
        icon_y, icon_step, icon_size = y + 52, 36, 34
        icon_x = x + inset
        text_x, text_y, line_step = x + 132, y + 61, 19
        body_size = ""
    else:
        icon_y, icon_step, icon_size = y + 48, 52, 40
        icon_x = x + (width - icon_size - (len(icons) - 1) * icon_step) // 2
        text_x, text_y, line_step = x + width // 2, y + (105 if len(lines) == 3 else 116), 19
        body_size = ' font-size="14.5" text-anchor="middle"'
    parts.extend(icon(slug, icon_x + i * icon_step, icon_y, icon_size)
                 for i, slug in enumerate(icons))
    parts.extend(f'<text x="{text_x}" y="{text_y + i * line_step}" '
                 f'class="body"{body_size}>{escape(line)}</text>'
                 for i, line in enumerate(lines))
    return "\n".join(parts)


def render_stack() -> None:
    description = "; ".join(
        f"{title}: {', '.join(items)}" for title, _, _, items in STACK
    )
    desktop = [
        stack_card(index, (index % 4) * 222, (index // 4) * 172, 211, 160)
        for index in range(8)
    ]
    (ASSETS / "technical-stack.svg").write_text(
        frame(877, 332, description, "\n".join(desktop)), encoding="utf-8"
    )

    mobile = [
        stack_card(index, 0, index * 140, 340, 128, mobile=True)
        for index in range(8)
    ]
    (ASSETS / "technical-stack-mobile.svg").write_text(
        frame(340, 1108, description, "\n".join(mobile)), encoding="utf-8"
    )


if __name__ == "__main__":
    render_stack()
    print("Rendered desktop and mobile Technical Stack panels.")
