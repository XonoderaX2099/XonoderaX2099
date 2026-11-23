"""Genera las imagenes pixel art del README (hero, ficha del jugador y pie).

Uso: python assets/gen_pixel.py   (escribe assets/hero.svg, assets/player.svg, assets/footer.svg)
Todo es SVG con rects: sin fuentes externas, asi GitHub lo muestra igual en cualquier lado.
"""
import os
import random
import unicodedata

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
F['Ñ'] = "01110 00000 10001 11001 10101 10011 10001"
F = {k: v.split() for k, v in F.items()}


def _limpio(s):
    s = s.upper().replace('Ñ', '~')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.replace('~', 'Ñ')


def ancho(s, esc):
    return (len(_limpio(s)) * 6 - 1) * esc


def texto(s, x, y, esc, color, centro=False, clase=""):
    """Texto pixel 5x7. Une los pixeles seguidos de cada fila en un solo rect."""
    if centro:
        x = x - ancho(s, esc) / 2
    rs = []
    for i, ch in enumerate(_limpio(s)):
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


# Avatar basado en la foto: cabeza rapada, gafas rectangulares, barba corta, sonrisa,
# camiseta verde oliva con estampado y brazos tatuados.
def _f(a, b="", c=""):
    return a + b + c


AVATAR = [
    "........kkkkkkkk........",
    "......kkhhhhhhhhkk......",
    ".....khhhhhhhhhhhhk.....",
    "....khhhhhhhhhhhhhhk....",
    _f("....k", "ssssssssssssss", "k...."),
    _f("....k", "ssssssssssssss", "k...."),
    _f("....k", "gggggggggggggg", "k...."),
    _f("...Sk", "gllelgssglellg", "kS..."),
    _f("...Sk", "gllllgssgllllg", "kS..."),
    _f("....k", "ggggggssgggggg", "k...."),
    _f("....k", "ssesssSSssssss", "k...."),
    _f("....k", "SssssssssssssS", "k...."),
    _f("....k", "bsssmwwwwmsssb", "k...."),
    _f("....k", "bbsssmmmmsssbb", "k...."),
    _f("....k", "bbbssssssssbbb", "k...."),
    ".....kbbbbbbbbbbbbk.....",
    "......kkbbbbbbbbkk......",
    "........kssssssk........",
    "...kkttttTssssTttttkk...",
    "..kttttttTTTTTTttttttk..",
    _f(".k", "ttttpppppppppppptttt", "k."),
    _f(".k", "ttttpPpnppppnpPptttt", "k."),
    _f(".k", "ttttppPPnppnPPpptttt", "k."),
    _f(".kiik", "tpppnpPPpnpppt", "kiik."),
    _f(".kisk", "tppPpnppnpPppt", "ksik."),
    _f(".kiik", "tpPPpppppppPPt", "kiik."),
    _f(".kssk", "ttpppppppppptt", "kssk."),
    _f("..kk.", "kttttttttttttk", ".kk.."),
]
assert all(len(f) == 24 for f in AVATAR), [len(f) for f in AVATAR]
PAL_AV = {'k': '#1a1110', 'h': '#8c6b58', 's': '#e2a98a', 'S': '#c4876a', 'b': '#3b2a20', 'g': '#1f2430',
          'l': '#9fc3d4', 'e': '#1a1110', 'w': '#ffffff', 'm': '#8a3a3a', 't': '#6f7148', 'T': '#55573a',
          'p': '#e5e7eb', 'P': '#9ca3af', 'n': '#4ade80', 'i': '#3d4757'}

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



# ---------------------------------------------------------------- paleta sobria (tono GitHub oscuro)
BG, PANEL, BORDE = '#0d1117', '#161b22', '#30363d'
ACENTO, AZUL, TEXTO, GRIS, AMARILLO = '#00bfff', '#58a6ff', '#e6edf3', '#8b949e', '#e3b341'


def panel(x, y, w, h, titulo=None):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BORDE}"/>'
           f'<rect x="{x + 2}" y="{y + 2}" width="{w - 4}" height="{h - 4}" fill="{PANEL}"/>')
    # esquinas en pixel, el unico guino "retro" del marco
    for cx, cy in ((x, y), (x + w - 6, y), (x, y + h - 6), (x + w - 6, y + h - 6)):
        out += f'<rect x="{cx}" y="{cy}" width="6" height="6" fill="{ACENTO}"/>'
    if titulo:
        out += texto(titulo, x + 24, y + 20, 2, GRIS)
    return out


def puntos(w, h):
    out = []
    for x in range(12, w, 24):
        for y in range(12, h, 24):
            out.append(f'<rect x="{x}" y="{y}" width="2" height="2" fill="#21262d"/>')
    return ''.join(out)


def hero():
    W, H = 960, 320
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', puntos(W, H)]
    p.append(panel(40, 40, 200, 248))
    p.append(f'<rect x="42" y="42" width="196" height="212" fill="#0f2a33"/>')
    p.append(sprite(AVATAR, PAL_AV, 56, 50, 7))
    p.append(f'<rect x="42" y="254" width="196" height="32" fill="#0b1220"/>')
    p.append(texto("XONODERAX2099", 140, 264, 2, ACENTO, centro=True))
    x = 280
    p.append(texto("SEBASTIAN RIASCOS", x, 52, 5, TEXTO))
    p.append(f'<rect x="{x}" y="100" width="120" height="4" fill="{ACENTO}"/>')
    p.append(texto("DESARROLLADOR DE SOFTWARE", x, 122, 3, ACENTO))
    p.append(texto("EN LA INSTITUCION UNIVERSITARIA DE COLOMBIA", x, 160, 2, TEXTO))
    p.append(texto("BACKEND  *  IA APLICADA  *  MICROSERVICIOS", x, 186, 2, GRIS))
    t = "> STATUS: CONSTRUYENDO PLATAFORMAS CON IA"
    p.append(texto(t, x, 222, 2, '#3fb950'))
    p.append(f'<rect class="blink" x="{x + ancho(t, 2) + 8}" y="222" width="10" height="14" fill="#3fb950"/>')
    p.append(texto("> PRESS START <", x, 262, 3, AMARILLO, clase="blink"))
    return svg(W, H, ''.join(p))


def barra(x, y, valor, color):
    out = []
    for i in range(20):
        lleno = i < round(valor / 5)
        out.append(f'<rect x="{x + i * 12}" y="{y}" width="10" height="12" fill="{color if lleno else "#21262d"}"/>')
    return ''.join(out)


def player():
    W, H = 960, 430
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', panel(0, 0, W, H)]
    p.append(texto("PLAYER PROFILE", 32, 30, 3, TEXTO))
    p.append(texto("SAVE 01", W - 32 - ancho("SAVE 01", 2), 34, 2, GRIS))
    p.append(f'<rect x="32" y="66" width="{W - 64}" height="2" fill="{BORDE}"/>')
    filas = [("ROL", "DESARROLLADOR DE SOFTWARE"), ("TRABAJO", "INSTITUCION UNIVERSITARIA DE COLOMBIA"),
             ("ESTUDIO", "INGENIERIA DE SOFTWARE"), ("ENFOQUE", "BACKEND, IA (RAG Y AGENTES) Y MICROSERVICIOS"),
             ("META", "GAME DEVELOPMENT Y GERENCIA DE PROYECTOS"), ("UBICACION", "COLOMBIA")]
    y = 90
    for et, val in filas:
        p.append(texto(et, 32, y, 2, AMARILLO))
        p.append(texto(val, 190, y, 2, TEXTO))
        y += 28
    p.append(f'<rect x="32" y="262" width="{W - 64}" height="2" fill="{BORDE}"/>')
    p.append(texto("STATS", 32, 282, 2, GRIS))
    stats = [("BACKEND", 90, ACENTO), ("FRONTEND", 78, AZUL), ("IA / RAG", 80, '#bc8cff'),
             ("DEVOPS", 75, '#3fb950'), ("GAME DEV", 55, AMARILLO), ("EQUIPO", 85, '#f0883e')]
    for i, (et, v, col) in enumerate(stats):
        cx = 32 if i % 2 == 0 else 492
        cy = 312 + (i // 2) * 30
        p.append(texto(et, cx, cy, 2, TEXTO))
        p.append(barra(cx + 120, cy, v, col))
        p.append(texto(str(v), cx + 372, cy, 2, col))
    return svg(W, H, ''.join(p))


def footer():
    W, H = 960, 90
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', puntos(W, H)]
    t = "> CONSTRUYAMOS ALGO JUNTOS"
    p.append(texto(t, W / 2 - 8, 30, 3, TEXTO, centro=True))
    cur = W / 2 - 8 + ancho(t, 3) / 2 + 10
    p.append(f'<rect class="blink" x="{cur:.0f}" y="30" width="14" height="21" fill="{ACENTO}"/>')
    return svg(W, H, ''.join(p))


def banner(titulo, nombre_icono):
    W, H = 960, 56
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', icono(nombre_icono, 0, 12, 4)]
    p.append(texto(titulo, 48, 16, 3, TEXTO))
    p.append(f'<rect x="0" y="{H - 4}" width="{W}" height="2" fill="{BORDE}"/>')
    p.append(f'<rect x="0" y="{H - 4}" width="{48 + ancho(titulo, 3)}" height="2" fill="{ACENTO}"/>')
    return svg(W, H, ''.join(p))


def quest(num, nombre, sub, estado, area, color, stack):
    W, H = 960, 150
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', panel(0, 0, W, H)]
    p.append(f'<rect x="2" y="2" width="8" height="{H - 4}" fill="{color}"/>')
    p.append(texto(f"PROYECTO {num:02d}", 32, 22, 2, GRIS))
    p.append(texto(nombre, 32, 46, 4, TEXTO))
    p.append(texto(sub, 32, 86, 2, '#c9d1d9'))
    p.append(texto(stack, 32, 114, 2, color))
    vivo = estado == "EN PRODUCCION"
    chip = '#238636' if vivo else '#1f6feb' if estado == "EN DESARROLLO" else '#6e7681'
    cw = ancho(estado, 2) + 40
    p.append(f'<rect x="{W - 28 - cw}" y="20" width="{cw}" height="28" fill="{chip}"/>')
    p.append(f'<rect class="{"blink" if vivo else ""}" x="{W - 28 - cw + 12}" y="30" width="8" height="8" fill="#ffffff"/>')
    p.append(texto(estado, W - 28 - cw + 28, 27, 2, '#ffffff'))
    p.append(texto(area, W - 28 - ancho(area, 2), 62, 2, GRIS))
    return svg(W, H, ''.join(p))


def side_quests(items):
    W = 960
    H = 32 + ((len(items) + 1) // 2) * 48 + 12
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', panel(0, 0, W, H)]
    for i, (nombre, stack) in enumerate(items):
        x = 32 if i % 2 == 0 else 496
        y = 28 + (i // 2) * 48
        p.append(f'<rect x="{x}" y="{y + 3}" width="8" height="8" fill="{ACENTO}"/>')
        p.append(texto(nombre, x + 22, y, 2, TEXTO))
        p.append(texto(stack, x + 22, y + 20, 2, GRIS))
    return svg(W, H, ''.join(p))


def inventario(grupos):
    W = 960
    p = []
    y = 26
    for titulo, color, items in grupos:
        p.append(texto(titulo, 32, y, 2, GRIS))
        y += 24
        x = 32
        for it in items:
            w = ancho(it, 2) + 24
            if x + w > W - 32:
                x, y = 32, y + 42
            p.append(f'<rect x="{x}" y="{y}" width="{w}" height="34" fill="{BORDE}"/>'
                     f'<rect x="{x + 2}" y="{y + 2}" width="{w - 4}" height="30" fill="#0d1117"/>'
                     f'<rect x="{x + 2}" y="{y + 2}" width="4" height="30" fill="{color}"/>')
            p.append(texto(it, x + 14, y + 11, 2, TEXTO))
            x += w + 10
        y += 56
    H = y
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="{BG}"/>' + panel(0, 0, W, H) + ''.join(p))


def logros(items):
    W = 960
    filas = (len(items) + 1) // 2
    H = 64 + filas * 34 + 16
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', panel(0, 0, W, H)]
    tot = f"{len(items)} COMPLETADAS"
    p.append(texto("CERTIFICACIONES", 32, 24, 2, GRIS))
    p.append(texto(tot, W - 32 - ancho(tot, 2), 24, 2, '#3fb950'))
    p.append(f'<rect x="32" y="48" width="{W - 64}" height="2" fill="{BORDE}"/>')
    for i, (txt, color) in enumerate(items):
        col, fila = (0, i) if i < filas else (1, i - filas)
        x = 32 + col * 464
        y = 68 + fila * 34
        filas_t, _ = ICONOS["trofeo"]
        p.append(sprite(filas_t, {'y': color, 'b': '#484f58'}, x, y, 3))
        p.append(texto(txt, x + 36, y + 5, 2, TEXTO))
    return svg(W, H, ''.join(p))


def mapa(nodos):
    W, H = 960, 200
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', panel(0, 0, W, H)]
    paso = (W - 240) // (len(nodos) - 1)
    pts = [(120 + i * paso, 76) for i in range(len(nodos))]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        for xx in range(x1 + 24, x2 - 18, 16):
            p.append(f'<rect x="{xx}" y="{y1 - 3}" width="8" height="6" fill="{BORDE}"/>')
    for i, ((x, y), (nombre, sub)) in enumerate(zip(pts, nodos)):
        col = ACENTO if i == 0 else PANEL
        borde = ACENTO if i == 0 else GRIS
        p.append(f'<rect x="{x - 16}" y="{y - 16}" width="32" height="32" fill="{borde}"/>'
                 f'<rect x="{x - 12}" y="{y - 12}" width="24" height="24" fill="{col}"/>')
        p.append(texto(nombre, x, y + 32, 2, TEXTO, centro=True))
        p.append(texto(sub, x, y + 54, 2, GRIS, centro=True))
    x0, y0 = pts[0]
    p.append(texto("AHORA", x0, y0 - 44, 2, ACENTO, centro=True, clase="blink"))
    return svg(W, H, ''.join(p))



def detalle(titulo, desc, puntos_, color):
    """Ficha de detalle de un proyecto, como pantalla de descripcion de mision."""
    W = 960
    H = 96 + len(puntos_) * 30 + 20
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', panel(0, 0, W, H)]
    p.append(f'<rect x="2" y="2" width="8" height="{H - 4}" fill="{color}"/>')
    p.append(texto("DETALLES / " + titulo, 32, 22, 2, GRIS))
    p.append(texto(desc, 32, 50, 2, TEXTO))
    p.append(f'<rect x="32" y="80" width="{W - 64}" height="2" fill="{BORDE}"/>')
    y = 98
    for t in puntos_:
        p.append(f'<rect x="32" y="{y + 3}" width="8" height="8" fill="{color}"/>')
        p.append(texto(t, 54, y, 2, '#c9d1d9'))
        y += 30
    return svg(W, H, ''.join(p))


def boton_detalles():
    W, H = 228, 40
    p = [f'<rect width="{W}" height="{H}" fill="{BORDE}"/>', f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" fill="{PANEL}"/>',
         f'<rect x="2" y="{H - 6}" width="{W - 4}" height="4" fill="#0b1220"/>']
    p.append(texto("> VER DETALLES", 16, 13, 2, ACENTO))
    return svg(W, H, ''.join(p))


def dialogo(quien, lineas):
    """Cuadro de dialogo tipo RPG para la bio."""
    W = 960
    H = 70 + len(lineas) * 28 + 24
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', panel(0, 0, W, H)]
    nw = ancho(quien, 2) + 28
    p.append(f'<rect x="24" y="18" width="{nw}" height="30" fill="{ACENTO}"/>')
    p.append(texto(quien, 38, 26, 2, BG))
    y = 66
    for l in lineas:
        p.append(texto(l, 32, y, 2, TEXTO))
        y += 28
    p.append(f'<g class="blink"><rect x="{W - 44}" y="{H - 30}" width="14" height="4" fill="{AMARILLO}"/>'
             f'<rect x="{W - 42}" y="{H - 26}" width="10" height="4" fill="{AMARILLO}"/>'
             f'<rect x="{W - 40}" y="{H - 22}" width="6" height="4" fill="{AMARILLO}"/></g>')
    return svg(W, H, ''.join(p))


DETALLES = {
    1: ("SOFIA", "PLATAFORMA PARA EL CONSULTORIO JURÍDICO UNIVERSITARIO", ACENTO, [
        "CHATBOT WEB CON IA CONVERSACIONAL MULTIESTADO",
        "RAG CON OPENAI: BÚSQUEDA SEMÁNTICA, RE-RANKING Y GENERACIÓN",
        "AGENDAMIENTO COMPLETO POR CHAT",
        "MULTI-TENANCY CON AISLAMIENTO POR TENANT",
        "DASHBOARD CON MÉTRICAS Y EXPORTACIÓN PDF / EXCEL",
        "6 MICROSERVICIOS NODE + 1 FASTAPI * POSTGRES, PGVECTOR, QDRANT"]),
    2: ("SICOP", "SISTEMA ADMINISTRATIVO PARA CONSULTORIOS JURÍDICOS", AZUL, [
        "CASOS, CITAS, DOCUMENTOS Y CERTIFICACIONES",
        "RBAC CON 6 ROLES Y JWT CON REFRESH TOKENS",
        "PDFS CON VERIFICACIÓN POR QR",
        "FIRMAS MULTIROL ORDENADAS POR JERARQUÍA",
        "RECORDATORIOS AUTOMÁTICOS 24 H Y 15 MIN ANTES",
        "SEMÁFORO DE PLAZOS, AUDITORÍA E INTEGRACIÓN CON SOFIA"]),
    3: ("APP PSICOLOGÍA", "SALUD MENTAL UNIVERSITARIA CON IA Y APP MÓVIL", '#bc8cff', [
        "CHATBOT EMOCIONAL CON GPT-4O-MINI + RAG",
        "COPILOTO CLÍNICO PARA PRACTICANTES DE PSICOLOGÍA",
        "APP FLUTTER CON GOOGLE SIGN-IN (ANDROID, IOS Y WEB)",
        "PUSH CON FIREBASE Y MENSAJERÍA CON RABBITMQ",
        "+10 MICROSERVICIOS NESTJS * MYSQL, REDIS Y MINIO",
        "TESTS CON JEST, VITEST Y PLAYWRIGHT"]),
    4: ("KIVO", "PERSONAJES E HISTORIAS CON IA, INSTALABLE COMO PWA", '#f778ba', [
        "CREADOR DE PERSONAJES POR PASOS, CON SECUNDARIOS Y LORE",
        "CHAT NARRATIVO CON MEMORIA, VOCES Y RAMAS DE LA HISTORIA",
        "LOGIN CON GOOGLE Y VERIFICACIÓN POR CÓDIGO",
        "POSTGRES CON ROW LEVEL SECURITY",
        "VARIOS IDIOMAS, CATÁLOGO CON BÚSQUEDA Y MODERACIÓN"]),
    5: ("CONNEXIA", "MENSAJES, LEADS Y VENTAS DE UN NEGOCIO EN UN SOLO LUGAR", '#3fb950', [
        "WHATSAPP, MESSENGER, INSTAGRAM, CORREO, SMS Y LLAMADAS",
        "LEADS DESDE META ADS Y TIKTOK ADS CON FLUJOS AUTOMÁTICOS",
        "PAGOS, CATÁLOGO Y AGENDA DE RESERVAS",
        "+20 MICROSERVICIOS .NET 9 CON GATEWAY GRAPHQL + GRPC"]),
    6: ("PYTHONESCAPE", "APRENDE PYTHON JUGANDO: EL JUEGO QUE DESPERTÓ UN SUEÑO", AMARILLO, [
        "7 ESCENARIOS CONECTADOS CON MINIMAPA",
        "AUDIO AMBIENTAL POR HABITACIÓN",
        "PYGAME CON FÍSICA Y COLISIONES",
        "TESTS CON PYTEST Y ARQUITECTURA SOLID"]),
}


def todo():
    salida = {"hero.svg": hero(), "player.svg": player(), "footer.svg": footer()}
    for clave, titulo, ic in [("perfil", "PERFIL", "corazon"), ("quests", "PROYECTOS", "espada"),
                              ("side", "PROYECTOS IUDC", "pergamino"), ("inventario", "STACK", "cofre"),
                              ("stats", "ESTADISTICAS", "rayo"), ("logros", "CERTIFICACIONES", "trofeo"),
                              ("mapa", "ROADMAP", "mapa")]:
        salida[f"banner-{clave}.svg"] = banner(titulo, ic)
    misiones = [
        (1, "SOFIA", "CONSULTORIO JURIDICO CON CHATBOT Y RAG", "EN PRODUCCION", "BACKEND + IA", ACENTO,
         "NODE  EXPRESS  FASTAPI  PGVECTOR  QDRANT  OPENAI"),
        (2, "SICOP", "GESTION DE CASOS DEL CONSULTORIO JURIDICO", "EN PRODUCCION", "FULL STACK", AZUL,
         "NEXT 16  TYPESCRIPT  PRISMA  POSTGRES  NGINX"),
        (3, "APP PSICOLOGIA", "SALUD MENTAL CON IA Y APP MOVIL", "COMPLETADO", "BACKEND + MOBILE", '#bc8cff',
         "NESTJS  FLUTTER  MYSQL  REDIS  RABBITMQ"),
        (4, "KIVO", "HISTORIAS INTERACTIVAS CON IA", "EN PRODUCCION", "FULL STACK", '#f778ba',
         "NEXT 16  REACT 19  POSTGRES  DRIZZLE"),
        (5, "CONNEXIA", "CRM OMNICANAL CON IA", "EN DESARROLLO", "BACKEND", '#3fb950',
         ".NET 9  GRAPHQL  GRPC  DOCKER"),
        (6, "PYTHONESCAPE", "JUEGO EDUCATIVO PARA APRENDER PYTHON", "COMPLETADO", "GAME DEV", AMARILLO,
         "PYTHON  PYGAME  PYTEST"),
    ]
    for m in misiones:
        salida[f"quest-{m[0]}.svg"] = quest(*m)
    salida["side-quests.svg"] = side_quests([
        ("AULA INTELIGENTE", "PYTHON"), ("CITAS IUDC", "TYPESCRIPT"),
        ("INVENTARIO IUDC", "TYPESCRIPT"), ("BOLSA DE EMPLEO", "JAVASCRIPT"),
        ("PAGOCONTROL", "TYPESCRIPT"), ("UVETERINARIA", "PYTHON")])
    salida["inventory.svg"] = inventario([
        ("BACKEND", ACENTO, ["TYPESCRIPT", "NODE", "NESTJS", "EXPRESS", "PYTHON", "FASTAPI",
                             ".NET 9", "C#", "GRAPHQL", "GRPC"]),
        ("FRONTEND Y MOBILE", AZUL, ["REACT", "NEXT.JS", "VITE", "TAILWIND", "SHADCN", "FLUTTER", "DART"]),
        ("DATOS", '#bc8cff', ["POSTGRES", "MYSQL", "PRISMA", "DRIZZLE", "REDIS", "QDRANT", "PGVECTOR"]),
        ("DEVOPS", '#3fb950', ["DOCKER", "DOKPLOY", "RAILWAY", "NGINX", "RABBITMQ", "GH ACTIONS",
                               "FIREBASE", "GIT", "PLAYWRIGHT"]),
        ("IA", AMARILLO, ["OPENAI", "CLAUDE", "RAG", "AGENTES", "MCP", "CHATBOTS"]),
    ])
    A, S, C = '#bc8cff', AZUL, '#f85149'
    salida["achievements.svg"] = logros([
        ("AI FLUENCY: FOUNDATIONS", A), ("AI FLUENCY FOR STUDENTS", A), ("AI FLUENCY FOR EDUCATORS", A),
        ("AI FLUENCY FOR NONPROFITS", A), ("TEACHING AI FLUENCY", A), ("CLAUDE 101", A),
        ("CLAUDE CODE IN ACTION", A), ("INTRO TO AGENT SKILLS", A), ("INTRO TO MCP", A),
        ("MCP: ADVANCED TOPICS", A), ("CLAUDE + VERTEX AI", A), ("CLAUDE + AMAZON BEDROCK", A),
        ("ARQUITECTURA DE SOFTWARE", S), ("ESTRUCTURAS DE DATOS IA", S), ("PATRONES DE DISENO", S),
        ("FRONT-END DEVELOPMENT", S), ("CISCO LINUX ESSENTIALS", C), ("CISCO HACKER ETICO", C),
    ])
    salida["world-map.svg"] = mapa([("IUDC", "BACKEND + IA"), ("AI ENGINEER", "AGENTES"),
                                    ("FRONTEND", "DISENO Y UI"), ("GAME DEV", "VIDEOJUEGOS"),
                                    ("PROJECT LEAD", "GERENCIA")])
    for n, (t, d, col, pts) in DETALLES.items():
        salida[f"detalle-{n}.svg"] = detalle(t, d, pts, col)
    salida["ver-detalles.svg"] = boton_detalles()
    salida["bio.svg"] = dialogo("SEBASTIÁN", [
        "DESARROLLADOR DE SOFTWARE EN LA INSTITUCIÓN UNIVERSITARIA DE",
        "COLOMBIA Y ESTUDIANTE DE INGENIERÍA DE SOFTWARE.",
        "CONSTRUYO PLATAFORMAS REALES CON IA: CHATBOTS, SISTEMAS PARA",
        "CONSULTORIOS Y HERRAMIENTAS PARA ESTUDIANTES.",
        "ME APASIONAN EL DISEÑO, EL FRONTEND Y LOS VIDEOJUEGOS,",
        "Y HACIA ALLÁ VOY."])
    return salida


if __name__ == "__main__":
    for nombre, contenido in todo().items():
        with open(os.path.join(AQUI, nombre), "w", encoding="utf-8") as fh:
            fh.write(contenido)
        print("OK", nombre)
