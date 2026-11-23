"""Genera las imagenes pixel art del README (hero, ficha del jugador y pie).

Uso: python assets/gen_pixel.py   (escribe assets/hero.svg, assets/player.svg, assets/footer.svg)
Todo es SVG con rects: sin fuentes externas, asi GitHub lo muestra igual en cualquier lado.
"""
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
random.seed(2099)

F = {
    'A': "01110 10001 10001 11111 10001 10001 10001", 'B': "11110 10001 10001 11110 10001 10001 11110",
    'C': "01110 10001 10000 10000 10000 10001 01110", 'D': "11110 10001 10001 10001 10001 10001 11110",
    'E': "11111 10000 10000 11110 10000 10000 11111", 'F': "11111 10000 10000 11110 10000 10000 10000",
    'G': "01110 10001 10000 10111 10001 10001 01111", 'H': "10001 10001 10001 11111 10001 10001 10001",
    'I': "01110 00100 00100 00100 00100 00100 01110", 'J': "00111 00010 00010 00010 00010 10010 01100",
    'K': "10001 10010 10100 11000 10100 10010 10001", 'L': "10000 10000 10000 10000 10000 10000 11111",
    'M': "10001 11011 10101 10101 10001 10001 10001", 'N': "10001 10001 11001 10101 10011 10001 10001",
    'O': "01110 10001 10001 10001 10001 10001 01110", 'P': "11110 10001 10001 11110 10000 10000 10000",
    'Q': "01110 10001 10001 10001 10101 10010 01101", 'R': "11110 10001 10001 11110 10100 10010 10001",
    'S': "01111 10000 10000 01110 00001 00001 11110", 'T': "11111 00100 00100 00100 00100 00100 00100",
    'U': "10001 10001 10001 10001 10001 10001 01110", 'V': "10001 10001 10001 10001 10001 01010 00100",
    'W': "10001 10001 10001 10101 10101 10101 01010", 'X': "10001 10001 01010 00100 01010 10001 10001",
    'Y': "10001 10001 01010 00100 00100 00100 00100", 'Z': "11111 00001 00010 00100 01000 10000 11111",
    '0': "01110 10001 10011 10101 11001 10001 01110", '1': "00100 01100 00100 00100 00100 00100 01110",
    '2': "01110 10001 00001 00010 00100 01000 11111", '3': "11110 00001 00001 01110 00001 00001 11110",
    '4': "00010 00110 01010 10010 11111 00010 00010", '5': "11111 10000 11110 00001 00001 10001 01110",
    '6': "00110 01000 10000 11110 10001 10001 01110", '7': "11111 00001 00010 00100 01000 01000 01000",
    '8': "01110 10001 10001 01110 10001 10001 01110", '9': "01110 10001 10001 01111 00001 00010 01100",
    ' ': "00000 00000 00000 00000 00000 00000 00000", ':': "00000 01100 01100 00000 01100 01100 00000",
    '.': "00000 00000 00000 00000 00000 01100 01100", '-': "00000 00000 00000 11111 00000 00000 00000",
    '/': "00001 00010 00010 00100 01000 01000 10000", '!': "00100 00100 00100 00100 00100 00000 00100",
    '>': "01000 00100 00010 00001 00010 00100 01000", '<': "00010 00100 01000 10000 01000 00100 00010",
    '*': "00000 00000 01110 01110 01110 00000 00000", '?': "01110 10001 00001 00010 00100 00000 00100",
    '+': "00000 00100 00100 11111 00100 00100 00000", ',': "00000 00000 00000 00000 01100 00100 01000",
    '(': "00010 00100 01000 01000 01000 00100 00010", ')': "01000 00100 00010 00010 00010 00100 01000",
    '_': "00000 00000 00000 00000 00000 00000 11111", '#': "01010 01010 11111 01010 11111 01010 01010",
}
F = {k: v.split() for k, v in F.items()}


def ancho(s, esc):
    return (len(s) * 6 - 1) * esc


def texto(s, x, y, esc, color, centro=False, clase=""):
    """Texto pixel 5x7. Une los pixeles seguidos de cada fila en un solo rect."""
    if centro:
        x = x - ancho(s, esc) / 2
    rs = []
    for i, ch in enumerate(s.upper()):
        g = F.get(ch, F['?'])
        for fy, fila in enumerate(g):
            fx = 0
            while fx < 5:
                if fila[fx] == '1':
                    ini = fx
                    while fx < 5 and fila[fx] == '1':
                        fx += 1
                    rs.append(f'<rect x="{i * 6 + ini}" y="{fy}" width="{fx - ini}" height="1"/>')
                else:
                    fx += 1
    c = f' class="{clase}"' if clase else ''
    return f'<g{c} transform="translate({x:g},{y:g}) scale({esc})" fill="{color}">' + ''.join(rs) + '</g>'


def sprite(filas, pal, x, y, esc, clase=""):
    rs = []
    for fy, fila in enumerate(filas):
        fx = 0
        while fx < len(fila):
            ch = fila[fx]
            if ch in pal:
                ini = fx
                while fx < len(fila) and fila[fx] == ch:
                    fx += 1
                rs.append(f'<rect x="{ini}" y="{fy}" width="{fx - ini}" height="1" fill="{pal[ch]}"/>')
            else:
                fx += 1
    c = f' class="{clase}"' if clase else ''
    return f'<g{c}><g transform="translate({x},{y}) scale({esc})">' + ''.join(rs) + '</g></g>'


PAL = {'k': '#0a0a1a', 'h': '#2b1b17', 's': '#f1c27d', 'S': '#d9a066', 'e': '#0a0a1a', 'c': '#00e5ff',
       'b': '#1e3a8a', 'B': '#172554', 'p': '#111827', 'g': '#94a3b8', 'G': '#475569', 'y': '#7dd3fc',
       'r': '#ef4444', 'R': '#991b1b', 'w': '#ffffff'}

JUGADOR = [
    "......kkkk......", "....kkhhhhkk....", "...khhhhhhhhk...", "..kchhhhhhhhck..",
    "..kchsssssshck..", "..kcsessssesck..", "...kssssssssk...", "....kssSSssk....",
    "...kkbbccbbkk...", "..kbbbbccbbbbk..", ".kbbbbbccbbbbbk.", ".kbbBbbbbbbBbbk.",
    ".kbbBbbbbbbBbbk.", ".kssBbbbbbbBssk.", "..kkppppppppkk..", "...kppppkppppk..",
    "...kppppkppppk..", "...kkkkkkkkkkk..",
]
ROBOT = [
    ".....kk.....", ".....yy.....", "..kkkkkkkk..", ".kggggggggk.", ".kgkkkkkkgk.",
    ".kgkckkckgk.", ".kgkkkkkkgk.", ".kgkkyykkgk.", ".kggggggggk.", "..kkkkkkkk..",
    "...kGGGGk...", "....kkkk....",
]
BUG = [
    "..k......k..", "...k....k...", "..kkkkkkkk..", ".kRrrrrrrRk.", "kRrwkrrwkrRk",
    "kRrkkrrkkrRk", "kRrrrrrrrrRk", ".kRrrrrrrRk.", "k.kRRRRRRk.k", "..k.k..k.k..",
]

ESTILO = """<style>
.blink{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.flota{animation:flota 2.4s ease-in-out infinite}
@keyframes flota{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.brilla{animation:brilla 3s ease-in-out infinite}
@keyframes brilla{0%,100%{opacity:.25}50%{opacity:1}}
.salta{animation:salta 1.6s steps(2) infinite}
@keyframes salta{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.d{opacity:0;animation:cuenta 10s steps(1) infinite}
@keyframes cuenta{0%{opacity:1}10%{opacity:0}100%{opacity:0}}
</style>"""


def svg(w, h, cuerpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges">{ESTILO}{cuerpo}</svg>\n')


def estrellas(w, h, n):
    out = []
    for i in range(n):
        x, y = random.randrange(0, w), random.randrange(0, h)
        t = random.choice([2, 2, 2, 3, 4])
        col = random.choice(['#ffffff', '#87ceeb', '#7dd3fc', '#e879f9'])
        if i % 3 == 0:
            out.append(f'<rect class="brilla" style="animation-delay:-{random.uniform(0, 3):.2f}s" '
                       f'x="{x}" y="{y}" width="{t}" height="{t}" fill="{col}"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{t}" height="{t}" fill="{col}" opacity=".7"/>')
    return ''.join(out)


def hero():
    W, H = 960, 400
    horiz = 300
    p = ['<defs><linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#05050f"/><stop offset=".75" stop-color="#0d1b4b"/>'
         '<stop offset="1" stop-color="#3b0764"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#cielo)"/>', estrellas(W, horiz - 20, 90)]
    # Sol synthwave pixelado detras del horizonte, en franjas.
    cx, r = 480, 120
    for i, yy in enumerate(range(horiz - r, horiz, 6)):
        dy = horiz - yy
        if dy < 60 and i % 2:
            continue
        half = int((r * r - (r - (r - dy)) ** 2) ** 0.5) if dy < r else 0
        half = int(max(0, r * r - (dy) ** 2) ** 0.5)
        col = '#facc15' if dy > 80 else '#fb923c' if dy > 40 else '#f472b6'
        p.append(f'<rect x="{cx - half}" y="{yy}" width="{2 * half}" height="6" fill="{col}" opacity=".45"/>')
    # Suelo con grilla en perspectiva.
    p.append(f'<rect x="0" y="{horiz}" width="{W}" height="{H - horiz}" fill="#0a0420"/>')
    for k in range(-12, 13):
        p.append(f'<line x1="{480 + k * 40}" y1="{horiz}" x2="{480 + k * 160}" y2="{H}" '
                 f'stroke="#7c3aed" stroke-width="2" opacity=".5"/>')
    yy, paso = horiz + 8, 6
    while yy < H:
        p.append(f'<rect x="0" y="{yy}" width="{W}" height="2" fill="#7c3aed" opacity=".5"/>')
        paso += 5
        yy += paso
    p.append(f'<rect x="0" y="{horiz}" width="{W}" height="3" fill="#e879f9"/>')
    # HUD
    p.append(texto("1UP", 24, 20, 2, '#ff4d6d'))
    p.append(texto("000042", 24, 40, 2, '#ffffff'))
    p.append(texto("HI-SCORE", W / 2, 20, 2, '#ff4d6d', centro=True))
    p.append(texto("2099", W / 2, 40, 2, '#ffffff', centro=True))
    p.append(texto("STAGE", W - 24 - ancho("STAGE", 2), 20, 2, '#ff4d6d'))
    p.append(texto("IUDC-01", W - 24 - ancho("IUDC-01", 2), 40, 2, '#ffffff'))
    # Titulo con doble sombra.
    t = "SEBASTIAN RIASCOS"
    p.append(texto(t, W / 2 + 6, 86 + 6, 6, '#3b0764', centro=True))
    p.append(texto(t, W / 2 + 3, 86 + 3, 6, '#e879f9', centro=True))
    p.append(texto(t, W / 2, 86, 6, '#00e5ff', centro=True))
    p.append(texto("BACKEND DEV * AI BUILDER * FUTURE GAME DEV", W / 2, 150, 2, '#bae6fd', centro=True))
    p.append(texto("> PRESS START <", W / 2, 188, 3, '#facc15', centro=True, clase="blink"))
    # Jugador, su companero IA y el jefe final: un bug.
    p.append(sprite(JUGADOR, PAL, 110, horiz - 18 * 5, 5, clase="salta"))
    p.append(sprite(ROBOT, PAL, 200, 222, 4, clase="flota"))
    bx, by = 254, 232
    p.append(f'<rect x="{bx}" y="{by}" width="196" height="26" fill="#ffffff"/>'
             f'<rect x="{bx + 2}" y="{by + 2}" width="192" height="22" fill="#0a0a1a"/>'
             f'<rect x="{bx - 6}" y="{by + 14}" width="8" height="4" fill="#ffffff"/>')
    p.append(texto("AI: LISTO, P1!", bx + 98, by + 6, 2, '#00e5ff', centro=True))
    p.append(sprite(BUG, PAL, 790, horiz - 10 * 6, 6, clase="salta"))
    p.append(texto("BOSS: BUG", 776, 204, 2, '#ff4d6d'))
    p.append('<rect x="776" y="224" width="124" height="12" fill="#ffffff"/>'
             '<rect x="778" y="226" width="120" height="8" fill="#1f2937"/>'
             '<rect x="778" y="226" width="30" height="8" fill="#ef4444"/>')
    p.append(texto("(C) 2026 XONODERAX2099 * COLOMBIA", W / 2, 370, 2, '#a78bfa', centro=True))
    return svg(W, H, ''.join(p))


def ventana(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff"/>'
            f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" fill="#0a0a1a"/>'
            f'<rect x="{x + 8}" y="{y + 8}" width="{w - 16}" height="{h - 16}" fill="#0b1640"/>')


def barra(x, y, valor, color):
    out = []
    for i in range(20):
        lleno = i < round(valor / 5)
        out.append(f'<rect x="{x + i * 12}" y="{y}" width="10" height="14" fill="{color if lleno else "#1e293b"}"/>')
    return ''.join(out)


def player():
    W, H = 960, 500
    p = [f'<rect width="{W}" height="{H}" fill="#05050f"/>', ventana(0, 0, W, H)]
    p.append(texto("PLAYER STATUS", 32, 28, 3, '#facc15'))
    p.append(texto("SAVE 01", W - 32 - ancho("SAVE 01", 2), 32, 2, '#a78bfa'))
    p.append(f'<rect x="24" y="64" width="{W - 48}" height="4" fill="#ffffff"/>')
    p.append(ventana(28, 86, 184, 214))
    p.append(sprite(JUGADOR, PAL, 48, 98, 9, clase="salta"))
    p.append(sprite(ROBOT, PAL, 168, 92, 3, clase="flota"))
    p.append(texto("PLAYER 1", 120, 266, 3, '#00e5ff', centro=True))
    filas = [("NAME", "SEBASTIAN RIASCOS"), ("ALIAS", "XONODERAX2099"), ("CLASS", "SOFTWARE ENGINEER"),
             ("GUILD", "INST. UNIVERSITARIA DE COLOMBIA"), ("SPECIAL", "AI BUILDER / RAG / AGENTS"),
             ("MAIN QUEST", "SER GAME DEVELOPER"), ("SIDE QUEST", "GERENCIA DE PROYECTOS"),
             ("COMPANION", "AI-BOT (ONLINE)")]
    y = 92
    for et, val in filas:
        p.append(texto(et, 240, y, 2, '#facc15'))
        p.append(texto(val, 392, y, 2, '#ffffff'))
        y += 26
    p.append(f'<rect x="24" y="318" width="{W - 48}" height="4" fill="#ffffff"/>')
    stats = [("BACKEND", 90, '#00e5ff'), ("FRONTEND", 78, '#38bdf8'), ("AI / RAG", 80, '#e879f9'),
             ("DEVOPS", 75, '#84cc16'), ("GAME DEV", 55, '#facc15'), ("TEAMWORK", 85, '#fb923c')]
    for i, (et, v, col) in enumerate(stats):
        cx = 36 if i % 2 == 0 else 492
        cy = 342 + (i // 2) * 32
        p.append(texto(et, cx, cy, 2, '#ffffff'))
        p.append(barra(cx + 120, cy - 2, v, col))
        p.append(texto(str(v), cx + 372, cy, 2, col))
    p.append(texto("EQUIP: TS NODE NEST REACT NEXT PYTHON .NET DOCKER", 36, 452, 2, '#bae6fd'))
    return svg(W, H, ''.join(p))


def footer():
    W, H = 960, 150
    p = [f'<rect width="{W}" height="{H}" fill="#05050f"/>', estrellas(W, H, 50)]
    p.append(texto("CONTINUE?", W / 2 - 30, 26, 4, '#ff4d6d', centro=True))
    for i, n in enumerate("9876543210"):
        p.append(f'<g class="d" style="animation-delay:{i}s">'
                 + texto(n, W / 2 - 30 + ancho("CONTINUE?", 4) / 2 + 24, 26, 4, '#ffffff') + '</g>')
    p.append(texto("INSERT COIN", W / 2, 80, 3, '#facc15', centro=True, clase="blink"))
    p.append(texto("THANKS FOR PLAYING", W / 2, 118, 2, '#a78bfa', centro=True))
    return svg(W, H, ''.join(p))


# ---------------------------------------------------------------- iconos 8x8
ICONOS = {
    "espada": (["......ww", ".....wgw", "....wgw.", "y..wgw..", ".yyww...", "..yy....", ".y.yy...", "y...y..."],
               {'w': '#ffffff', 'g': '#94a3b8', 'y': '#facc15'}),
    "cofre": (["........", ".kkkkkk.", "kyyyyyyk", "kbbbbbbk", "kkkyykkk", "kbbyybbk", "kbbbbbbk", "kkkkkkkk"],
              {'k': '#0a0a1a', 'y': '#facc15', 'b': '#b45309'}),
    "trofeo": (["yyyyyyyy", "yyyyyyyy", ".yyyyyy.", "..yyyy..", "...yy...", "...yy...", "..yyyy..", ".bbbbbb."],
               {'y': '#facc15', 'b': '#b45309'}),
    "mapa": (["wwwwwwww", "wgggwggw", "wgrgwgww", "wgggwggw", "wwgwwwgw", "wggggggw", "wgggwrgw", "wwwwwwww"],
             {'w': '#fef3c7', 'g': '#84cc16', 'r': '#ef4444'}),
    "corazon": ([".rr..rr.", "rrrrrrrr", "rrrrrrrr", "rrrrrrrr", ".rrrrrr.", "..rrrr..", "...rr...", "........"],
                {'r': '#ef4444'}),
    "estrella": (["...yy...", "...yy...", "yyyyyyyy", ".yyyyyy.", "..yyyy..", ".yy..yy.", "yy....yy", "........"],
                 {'y': '#facc15'}),
    "pergamino": (["wwwwwww.", "wgggggw.", "wwwwwww.", "wgggggw.", "wwwwwww.", "wgggw...", "wwwww...", "........"],
                  {'w': '#fef3c7', 'g': '#92400e'}),
    "rayo": (["....yyy.", "...yyy..", "..yyy...", ".yyyyyy.", "...yyy..", "..yyy...", ".yy.....", "y......."],
             {'y': '#00e5ff'}),
}


def icono(nombre, x, y, esc, clase=""):
    filas, pal = ICONOS[nombre]
    return sprite(filas, pal, x, y, esc, clase)


def banner(titulo, nombre_icono, color):
    """Encabezado de seccion: icono + titulo pixel + linea punteada."""
    W, H = 960, 70
    p = [f'<rect width="{W}" height="{H}" fill="#05050f"/>', icono(nombre_icono, 16, 14, 5, "salta")]
    p.append(texto(titulo, 76, 18, 4, '#3b0764'))
    p.append(texto(titulo, 74, 16, 4, color))
    x0 = 76 + ancho(titulo, 4) + 24
    for x in range(x0, W - 16, 16):
        p.append(f'<rect x="{x}" y="30" width="8" height="8" fill="{color}" opacity=".5"/>')
    p.append(f'<rect x="0" y="{H - 6}" width="{W}" height="2" fill="{color}" opacity=".4"/>')
    return svg(W, H, ''.join(p))


def estrellas_dificultad(x, y, n):
    out = []
    for i in range(5):
        filas, pal = ICONOS["estrella"]
        pal = pal if i < n else {'y': '#334155'}
        out.append(sprite(filas, pal, x + i * 22, y, 2))
    return ''.join(out)


def quest(num, nombre, sub, estado, dificultad, color, stack):
    W, H = 960, 170
    p = [ventana(0, 0, W, H)]
    p.append(f'<rect x="8" y="8" width="10" height="{H - 16}" fill="{color}"/>')
    p.append(texto(f"QUEST {num:02d}", 36, 24, 2, '#facc15'))
    p.append(texto(nombre, 36, 50, 4, color))
    p.append(texto(sub, 36, 92, 2, '#ffffff'))
    p.append(texto("STACK: " + stack, 36, 126, 2, '#bae6fd'))
    hecho = estado in ("COMPLETADA", "EN PRODUCCION")
    chip = '#16a34a' if hecho else '#0891b2'
    cw = ancho(estado, 2) + 28
    p.append(f'<rect x="{W - 32 - cw}" y="20" width="{cw}" height="30" fill="{chip}"/>')
    p.append(texto(estado, W - 32 - cw + 14, 28, 2, '#ffffff', clase="" if hecho else "blink"))
    p.append(texto("DIFICULTAD", W - 254, 72, 2, '#a78bfa'))
    p.append(estrellas_dificultad(W - 254, 94, dificultad))
    return svg(W, H, ''.join(p))


def side_quests(items):
    W = 960
    H = 40 + ((len(items) + 1) // 2) * 46 + 16
    p = [ventana(0, 0, W, H)]
    for i, (nombre, stack) in enumerate(items):
        x = 32 if i % 2 == 0 else 496
        y = 32 + (i // 2) * 46
        p.append(icono("estrella", x, y + 2, 2))
        p.append(texto(nombre, x + 28, y, 2, '#ffffff'))
        p.append(texto(stack, x + 28, y + 20, 2, '#7dd3fc'))
    return svg(W, H, ''.join(p))


def inventario(grupos):
    W = 960
    p = []
    y = 24
    for titulo, color, items in grupos:
        p.append(texto(titulo, 32, y, 2, color))
        y += 26
        x = 32
        for it in items:
            w = ancho(it, 2) + 24
            if x + w > W - 32:
                x, y = 32, y + 44
            p.append(f'<rect x="{x}" y="{y}" width="{w}" height="36" fill="{color}"/>'
                     f'<rect x="{x + 2}" y="{y + 2}" width="{w - 4}" height="32" fill="#0a0a1a"/>'
                     f'<rect x="{x + 2}" y="{y + 2}" width="{w - 4}" height="4" fill="{color}" opacity=".35"/>')
            p.append(texto(it, x + 12, y + 12, 2, '#ffffff'))
            x += w + 10
        y += 58
    H = y + 6
    return svg(W, H, ventana(0, 0, W, H) + ''.join(p))


def logros(items):
    W = 960
    filas = (len(items) + 1) // 2
    H = 76 + filas * 36 + 20
    p = [ventana(0, 0, W, H)]
    p.append(texto("ACHIEVEMENTS", 32, 26, 3, '#facc15'))
    tot = f"{len(items)}/{len(items)} UNLOCKED"
    p.append(texto(tot, W - 32 - ancho(tot, 2), 30, 2, '#84cc16'))
    p.append(f'<rect x="24" y="60" width="{W - 48}" height="4" fill="#ffffff"/>')
    for i, (txt, color) in enumerate(items):
        col, fila = (0, i) if i < filas else (1, i - filas)
        x = 32 + col * 464
        y = 80 + fila * 36
        filas_t, pal = ICONOS["trofeo"]
        p.append(sprite(filas_t, {'y': color, 'b': '#475569'}, x, y, 3))
        p.append(texto(txt, x + 36, y + 5, 2, '#ffffff'))
    return svg(W, H, ''.join(p))


def mapa(nodos):
    W, H = 960, 280
    p = [f'<rect width="{W}" height="{H}" fill="#052e16"/>']
    random.seed(7)
    for _ in range(140):
        x, y = random.randrange(0, W, 8), random.randrange(0, H, 8)
        p.append(f'<rect x="{x}" y="{y}" width="8" height="8" fill="{random.choice(["#14532d", "#166534", "#15803d"])}"/>')
    paso = (W - 160) // (len(nodos) - 1)
    pts = [(80 + i * paso, 150 + (30 if i % 2 else -10)) for i in range(len(nodos))]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        for t in range(0, 21):
            x = x1 + (x2 - x1) * t / 20
            y = y1 + (y2 - y1) * t / 20
            if t % 2 == 0:
                p.append(f'<rect x="{x - 4:.0f}" y="{y - 4:.0f}" width="8" height="8" fill="#fef3c7"/>')
    for i, ((x, y), (nombre, sub)) in enumerate(zip(pts, nodos)):
        actual = i == 0
        col = '#facc15' if actual else '#e879f9' if i == len(nodos) - 1 else '#ffffff'
        p.append(f'<rect x="{x - 18}" y="{y - 18}" width="36" height="36" fill="#0a0a1a"/>'
                 f'<rect x="{x - 14}" y="{y - 14}" width="28" height="28" fill="{col}"/>')
        p.append(texto(nombre, x, y + 30, 2, '#ffffff', centro=True))
        p.append(texto(sub, x, y + 50, 2, '#86efac', centro=True))
    x0, y0 = pts[0]
    p.append(sprite(JUGADOR, PAL, x0 - 24, y0 - 84, 3, clase="salta"))
    p.append(texto("YOU ARE HERE", x0 + 34, y0 - 66, 2, '#facc15', clase="blink"))
    p.append(texto("WORLD MAP", W - 32 - ancho("WORLD MAP", 3), 16, 3, '#fef3c7'))
    return svg(W, H, ''.join(p))


def todo():
    salida = {"hero.svg": hero(), "player.svg": player(), "footer.svg": footer()}
    for clave, titulo, ic, col in [("perfil", "PLAYER PROFILE", "corazon", '#ff4d6d'),
                                   ("quests", "QUEST LOG", "espada", '#00e5ff'),
                                   ("side", "SIDE QUESTS", "pergamino", '#fef3c7'),
                                   ("inventario", "INVENTORY", "cofre", '#facc15'),
                                   ("stats", "BATTLE STATS", "rayo", '#00e5ff'),
                                   ("logros", "ACHIEVEMENTS", "trofeo", '#facc15'),
                                   ("mapa", "NEXT LEVELS", "mapa", '#84cc16')]:
        salida[f"banner-{clave}.svg"] = banner(titulo, ic, col)
    misiones = [
        (1, "SOFIA", "CONSULTORIO JURIDICO CON CHATBOT Y RAG", "EN PRODUCCION", 5, '#00e5ff',
         "NODE EXPRESS FASTAPI PGVECTOR QDRANT OPENAI"),
        (2, "SICOP", "GESTION DE CASOS DEL CONSULTORIO JURIDICO", "EN PRODUCCION", 4, '#38bdf8',
         "NEXT 16 TS PRISMA POSTGRES NGINX"),
        (3, "APP PSICOLOGIA", "SALUD MENTAL CON IA Y APP MOVIL", "COMPLETADA", 5, '#e879f9',
         "NESTJS FLUTTER MYSQL REDIS RABBITMQ"),
        (4, "KIVO", "HISTORIAS INTERACTIVAS CON IA", "EN PRODUCCION", 4, '#f472b6',
         "NEXT 16 REACT 19 POSTGRES DRIZZLE"),
        (5, "CONNEXIA", "CRM OMNICANAL CON IA", "EN CURSO", 5, '#84cc16',
         ".NET 9 GRAPHQL GRPC DOCKER"),
        (6, "PYTHONESCAPE", "JUEGO EDUCATIVO PARA APRENDER PYTHON", "COMPLETADA", 2, '#facc15',
         "PYTHON PYGAME PYTEST"),
    ]
    for m in misiones:
        salida[f"quest-{m[0]}.svg"] = quest(*m)
    salida["side-quests.svg"] = side_quests([
        ("AULA INTELIGENTE", "PYTHON"), ("CITAS IUDC", "TYPESCRIPT"),
        ("INVENTARIO IUDC", "TYPESCRIPT"), ("BOLSA DE EMPLEO", "JAVASCRIPT"),
        ("PAGOCONTROL", "TYPESCRIPT"), ("UVETERINARIA", "PYTHON")])
    salida["inventory.svg"] = inventario([
        ("WEAPONS - BACKEND", '#00e5ff', ["TYPESCRIPT", "NODE", "NESTJS", "EXPRESS", "PYTHON", "FASTAPI",
                                          ".NET 9", "C#", "GRAPHQL", "GRPC"]),
        ("ARMOR - FRONTEND Y MOBILE", '#38bdf8', ["REACT", "NEXT.JS", "VITE", "TAILWIND", "SHADCN",
                                                  "FLUTTER", "DART"]),
        ("POTIONS - DATOS", '#e879f9', ["POSTGRES", "MYSQL", "PRISMA", "DRIZZLE", "REDIS", "QDRANT",
                                        "PGVECTOR"]),
        ("TOOLS - DEVOPS", '#84cc16', ["DOCKER", "DOKPLOY", "RAILWAY", "NGINX", "RABBITMQ",
                                       "GH ACTIONS", "FIREBASE", "GIT", "PLAYWRIGHT"]),
        ("MAGIC - IA", '#facc15', ["OPENAI", "CLAUDE", "RAG", "AGENTES", "MCP", "CHATBOTS"]),
    ])
    A, S, C = '#a78bfa', '#38bdf8', '#ef4444'
    salida["achievements.svg"] = logros([
        ("AI FLUENCY: FOUNDATIONS", A), ("AI FLUENCY FOR STUDENTS", A), ("AI FLUENCY FOR EDUCATORS", A),
        ("AI FLUENCY FOR NONPROFITS", A), ("TEACHING AI FLUENCY", A), ("CLAUDE 101", A),
        ("CLAUDE CODE IN ACTION", A), ("INTRO TO AGENT SKILLS", A), ("INTRO TO MCP", A),
        ("MCP: ADVANCED TOPICS", A), ("CLAUDE + VERTEX AI", A), ("CLAUDE + AMAZON BEDROCK", A),
        ("ARQUITECTURA DE SOFTWARE", S), ("ESTRUCTURAS DE DATOS IA", S), ("PATRONES DE DISENO", S),
        ("FRONT-END DEVELOPMENT", S), ("CISCO LINUX ESSENTIALS", C), ("CISCO HACKER ETICO", C),
    ])
    salida["world-map.svg"] = mapa([("IUDC", "BACKEND + IA"), ("AI ENGINEER", "AGENTES"),
                                    ("FRONTEND", "DISENO Y UI"), ("GAME DEV", "EL SUENO"),
                                    ("PROJECT LEAD", "GERENCIA")])
    return salida


if __name__ == "__main__":
    for nombre, contenido in todo().items():
        with open(os.path.join(AQUI, nombre), "w", encoding="utf-8") as fh:
            fh.write(contenido)
        print("OK", nombre)
