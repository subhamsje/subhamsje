import html
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "wordmark.svg"

# High-clarity ANSI shadow block font
LINES = [
    "███████╗ ██╗   ██╗ ██████╗  ██╗  ██╗  █████╗  ███╗   ███╗",
    "██╔════╝ ██║   ██║ ██╔══██╗ ██║  ██║ ██╔══██╗ ████╗ ████║",
    "███████╗ ██║   ██║ ██████╔╝ ███████║ ███████║ ██╔████╔██║",
    "╚════██║ ██║   ██║ ██╔══██╗ ██╔══██║ ██╔══██║ ██║╚██╔╝██║",
    "███████║ ╚██████╔╝ ██████╔╝ ██║  ██║ ██║  ██║ ██║ ╚═╝ ██║",
    "╚══════╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝     ╚═╝",
]

SUBTITLE_CMD = "subham@github: ~$ echo $NAME && echo $ROLE"
SUBTITLE_OUT = "Subham Sagar · Software Engineer & AI Specialist"

# Terminal canvas dimensions
# Portrait rendered height at 370px width is: 370 * (875 / 840) = 385.4px
# Wordmark is placed at width 490px in README table.
# To match 385.4px: canvas height should be 490 * (CANVAS_H / CANVAS_W) = 385.4px
# So CANVAS_H / CANVAS_W = 385.4 / 490 = 0.7865
CANVAS_W = 580
CANVAS_H = 456

TITLEBAR_H = 32
PAD = 24
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#111722"
TITLE_TEXT = "#7d8590"
INK = "#e6edf3"
CYAN = "#22d3ee"
GREEN = "#39d353"

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">'
)
parts.append('<defs>')
parts.append(f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient>')
parts.append('</defs>')

# Window frame & title bar
parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">'
             f'subham@github: ~$ ./wordmark.sh</text>')

# Content positioning
start_y = 75
line_h = 24
banner_font_size = 14.5

# Animated reveal clip path for the banner
parts.append(
    f'<clipPath id="wipe_banner"><rect x="{PAD}" y="{start_y-20}" width="0" height="{len(LINES)*line_h + 30}">'
    f'<animate attributeName="width" from="0" to="{CANVAS_W-PAD*2}" dur="1.2s" begin="0.2s" fill="freeze"/>'
    f'</rect></clipPath>'
)

# Text lines inside clipPath
parts.append('<g clip-path="url(#wipe_banner)">')
for idx, line in enumerate(LINES):
    y = start_y + idx * line_h
    # Render with glowing cyan/white style
    parts.append(
        f'<text xml:space="preserve" x="{PAD}" y="{y}" fill="{CYAN}" font-size="{banner_font_size}" '
        f'letter-spacing="0.5px" font-weight="600">{html.escape(line)}</text>'
    )
parts.append('</g>')

# Soft horizontal scanline bar during wipe
parts.append(
    f'<rect x="{PAD}" y="{start_y-20}" width="12" height="{len(LINES)*line_h + 30}" fill="{CYAN}" opacity="0.4">'
    f'<animate attributeName="x" from="{PAD}" to="{CANVAS_W-PAD}" dur="1.2s" begin="0.2s" fill="freeze"/>'
    f'<set attributeName="opacity" to="0" begin="1.4s"/>'
    f'</rect>'
)

# Subtitle section below the banner
div_y = start_y + len(LINES) * line_h + 30
parts.append(f'<line x1="{PAD}" y1="{div_y}" x2="{CANVAS_W-PAD}" y2="{div_y}" stroke="{FRAME}" stroke-dasharray="4,4"/>')

cmd_y = div_y + 36
parts.append(
    f'<g opacity="0">'
    f'<text x="{PAD}" y="{cmd_y}" fill="{TITLE_TEXT}" font-size="13">'
    f'<tspan fill="{GREEN}">➜</tspan> ~ <tspan fill="{INK}">whoami --verbose</tspan></text>'
    f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.4s" fill="freeze"/>'
    f'</g>'
)

out_y = cmd_y + 30
parts.append(
    f'<g opacity="0">'
    f'<text x="{PAD}" y="{out_y}" fill="{INK}" font-size="13.5" font-weight="500">'
    f'Subham Sagar <tspan fill="{TITLE_TEXT}">|</tspan> <tspan fill="{CYAN}">AI &amp; Fullstack Engineer</tspan></text>'
    f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.8s" fill="freeze"/>'
    f'</g>'
)

# Terminal status cursor blinking
parts.append(
    f'<rect x="{PAD + 370}" y="{out_y - 12}" width="8" height="15" fill="{CYAN}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" begin="2.2s" repeatCount="indefinite"/>'
    f'</rect>'
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {CANVAS_W}x{CANVAS_H} (rendered height at 490px: {490 * CANVAS_H / CANVAS_W:.1f}px)")
