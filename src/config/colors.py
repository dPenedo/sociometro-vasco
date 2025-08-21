red_blue_color_list: list[str] = [
    "#A50026",  # 0 - Ext. Izquierda (rojo intenso)
    "#D73027",  # 1
    "#F46D43",  # 2
    "#FDAE61",  # 3
    "#FEE090",  # 4
    "#FFFFBF",  # 5 - Centro (amarillo muy claro)
    "#E0F3F8",  # 6
    "#ABD9E9",  # 7
    "#74ADD1",  # 8
    "#4575B4",  # 9
    "#313695",  # 10 - Ext. Derecha (azul intenso)
    "#808080",  # 11 - NS/NC (gris neutral)
]


provincias_map: dict[int, dict[str, str]] = {
    1: {"name": "Araba", "color": "#A31182"},
    2: {"name": "Bizkaia", "color": "#A71E23"},
    3: {"name": "Gipuzkoa", "color": "#1772B3"},
}
party_colors: dict[str, dict[str, str]] = {
    "PNV/EAJ": {"colormap": "Greens", "color": "green", "textcolor": "black"},
    "EH BILDU": {"colormap": "PuBuGn", "color": "darkcyan", "textcolor": "black"},
    "PARTIDO SOCIALISTA DE EUSKADI": {
        "colormap": "Reds",
        "color": "red",
        "textcolor": "black",
    },
    "SUMAR": {"colormap": "RdPu", "color": "crimson", "textcolor": "black"},
    "PP": {"colormap": "Blues", "color": "dodgerblue", "textcolor": "black"},
    "VOX": {"colormap": "Greens", "color": "limegreen", "textcolor": "black"},
}

parties_map_and_colors_p25: dict[int, dict[str, str]] = {
    1: {"question": "p2501", "name": "PNV/EAJ", "color": "#02451F"},
    2: {"question": "p2502", "name": "EH Bildu", "color": "#006155"},
    3: {"question": "p2503", "name": "PSE-EE", "color": "#AE0A14"},
    4: {"question": "p2504", "name": "Sumar", "color": "#850F33"},
    5: {"question": "p2505", "name": "Partido Popular", "color": "#1D3F77"},
    6: {"question": "p2506", "name": "VOX", "color": "#486D1C"},
}
