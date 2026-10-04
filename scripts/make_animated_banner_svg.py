import html
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "wordmark.svg"

# Character slices for each letter of "S U B H A M"
# S: 0:8, gap: 8:9
# U: 9:18, gap: 18:20
# B: 20:30, gap: 30:32
# H: 32:41, gap: 41:43
# A: 43:53, gap: 53:55
# M: 55:69
FULL_LINES = [
    "███████╗ ██╗   ██╗ ██████╗  ██╗  ██╗  █████╗  ███╗   ███╗",
    "██╔════╝ ██║   ██║ ██╔══██╗ ██║  ██║ ██╔══██╗ ████╗ ████║",
    "███████╗ ██║   ██║ ██████╔╝ ███████║ ███████║ ██╔████╔██║",
    "╚════██║ ██║   ██║ ██╔══██╗ ██╔══██║ ██╔══██║ ██║╚██╔╝██║",
    "███████║ ╚██████╔╝ ██████╔╝ ██║  ██║ ██║  ██║ ██║ ╚═╝ ██║",
    "╚══════╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝     ╚═╝",
]

# Slices (start_char, end_char) for each letter:
# S: cols 0..8
# U: cols 9..19
# B: cols 20..31
# H: cols 32..42
# A: cols 43..54
# M: cols 55..69
LETTERS = [
    ("S", 0, 8),
    ("U", 9, 19),
    ("B", 20, 31),
    ("H", 32, 42),
    ("A", 43, 54),
    ("M", 55, 69)
]

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
CYAN_BRIGHT = "#67e8f9"
GREEN = "#39d353"

start_y = 80
line_h = 24
banner_font_size = 14.5
char_w = 7.9  # approx monospace char width at 14.5px in 580px canvas

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">'
)
parts.append('<defs>')
parts.append(f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient>')

# Glow filter for pulsing effect
parts.append(
    '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">'
    '<feGaussianBlur stdDeviation="3" result="blur"/>'
    '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
    '</filter>'
)
parts.append('</defs>')

# Styles for continuous neon pulse and typewriter
css = """
@keyframes pulseGlow {
  0%, 100% { opacity: 0.88; filter: drop-shadow(0 0 1px rgba(34, 211, 238, 0.4)); }
  50% { opacity: 1; filter: drop-shadow(0 0 7px rgba(34, 211, 238, 0.85)); }
}
@keyframes letterFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
}
.pulsing-banner {
  animation: pulseGlow 3.5s ease-in-out infinite;
}
.letter-0 { animation: letterFloat 3.0s ease-in-out 0.0s infinite; }
.letter-1 { animation: letterFloat 3.0s ease-in-out 0.2s infinite; }
.letter-2 { animation: letterFloat 3.0s ease-in-out 0.4s infinite; }
.letter-3 { animation: letterFloat 3.0s ease-in-out 0.6s infinite; }
.letter-4 { animation: letterFloat 3.0s ease-in-out 0.8s infinite; }
.letter-5 { animation: letterFloat 3.0s ease-in-out 1.0s infinite; }
"""
parts.append(f'<style>{css}</style>')

# Window frame & title bar
parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">'
             f'subham@github: ~$ ./wordmark.sh</text>')

# Render each letter in its own animated group with staggered entry and then floating loop
parts.append('<g class="pulsing-banner">')
for li, (char_name, c_start, c_end) in enumerate(LETTERS):
    # Staggered pop-in for each letter (S, U, B, H, A, M)
    delay = 0.15 + li * 0.20  # letter enters at delay
    x_pos = PAD + c_start * char_w
    letter_w = (c_end - c_start) * char_w

    # Each letter has a typing drop-in clip or opacity reveal
    parts.append(f'<g class="letter-{li}">')
    for row_idx, row_text in enumerate(FULL_LINES):
        slice_str = row_text[c_start:c_end]
        y_pos = start_y + row_idx * line_h
        escaped = html.escape(slice_str)
        parts.append(
            f'<text xml:space="preserve" x="{x_pos:.1f}" y="{y_pos}" fill="{CYAN}" font-size="{banner_font_size}" '
            f'font-weight="600" opacity="0">'
            f'{escaped}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{delay:.2f}s" fill="freeze"/>'
            f'<animate attributeName="fill" values="{CYAN_BRIGHT};{CYAN}" dur="0.8s" begin="{delay:.2f}s" fill="freeze"/>'
            f'</text>'
        )
    parts.append('</g>')

parts.append('</g>')

# Laser cursor that rides across as S U B H A M gets typed out
total_reveal_dur = 0.15 + len(LETTERS) * 0.20
parts.append(
    f'<rect x="{PAD}" y="{start_y-18}" width="14" height="{len(FULL_LINES)*line_h + 24}" fill="{CYAN_BRIGHT}" opacity="0">'
    f'<animate attributeName="opacity" values="0;0.75;0.75;0" keyTimes="0;0.05;0.95;1" dur="{total_reveal_dur}s" begin="0.1s" fill="freeze"/>'
    f'<animate attributeName="x" from="{PAD}" to="{PAD + 69*char_w}" dur="{total_reveal_dur}s" begin="0.1s" fill="freeze"/>'
    f'</rect>'
)

# Divider line
div_y = start_y + len(FULL_LINES) * line_h + 30
parts.append(f'<line x1="{PAD}" y1="{div_y}" x2="{CANVAS_W-PAD}" y2="{div_y}" stroke="{FRAME}" stroke-dasharray="4,4"/>')

# Interactive status command & whoami response
cmd_y = div_y + 36
parts.append(
    f'<g opacity="0">'
    f'<text x="{PAD}" y="{cmd_y}" fill="{TITLE_TEXT}" font-size="13">'
    f'<tspan fill="{GREEN}">➜</tspan> ~ <tspan fill="{INK}">whoami --verbose</tspan></text>'
    f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{total_reveal_dur + 0.2:.2f}s" fill="freeze"/>'
    f'</g>'
)

out_y = cmd_y + 30
parts.append(
    f'<g opacity="0">'
    f'<text x="{PAD}" y="{out_y}" fill="{INK}" font-size="13.5" font-weight="500">'
    f'Subham Sagar <tspan fill="{TITLE_TEXT}">|</tspan> <tspan fill="{CYAN}">AI &amp; Fullstack Engineer</tspan></text>'
    f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{total_reveal_dur + 0.6:.2f}s" fill="freeze"/>'
    f'</g>'
)

# Active blinking terminal cursor at the end
parts.append(
    f'<rect x="{PAD + 370}" y="{out_y - 12}" width="8" height="15" fill="{CYAN}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" begin="{total_reveal_dur + 0.9:.2f}s" repeatCount="indefinite"/>'
    f'</rect>'
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {len(svg)} bytes, {CANVAS_W}x{CANVAS_H}")
