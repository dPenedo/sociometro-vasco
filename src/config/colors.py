red_blue_color_list: list[str] = [
    "#800000",  # 0 - Rojo oscuro
    "#701010",  # 1 - Rojo oscuro
    "#9D1F1F",  # 2 - Rojo intenso
    "#C23F3F",  # 3 - Rojo medio
    "#A14E6E",  # 4 - Rosado oscuro
    "#864186",  # 5 - Púrpura (punto medio perfecto)
    "#5C5D9D",  # 6 - Púrpura azulado
    "#4A4A8B",  # 7 - Púrpura azul oscuro
    "#3535A8",  # 8 - Azul violáceo
    "#1F1FCD",  # 9 - Azul medio oscuro
    "#000080",  # 10 - Azul muy oscuro
    "#808080",  # 11 - NS/NC gris
]


red_green_color_list: list[str] = [
    "#800000",  # 0 - Rojo oscuro
    "#9D1F1F",  # 1 - Rojo intenso
    "#C23F3F",  # 2 - Rojo medio
    "#D46A4C",  # 3 - Rojo anaranjado
    "#E59459",  # 4 - Naranja
    "#F0BD66",  # 5 - Amarillo anaranjado (punto medio)
    "#D9D567",  # 6 - Amarillo verdoso
    "#A8C97F",  # 7 - Verde amarillento
    "#78BD97",  # 8 - Verde medio
    "#4AB0AF",  # 9 - Verde azulado
    "#00A080",  # 10 - Verde oscuro
]

provincias_map: dict[int, dict[str, str]] = {
    1: {"name": "Araba", "color": "#3E938D"},
    2: {"name": "Bizkaia", "color": "#FF6B6B"},
    3: {"name": "Gipuzkoa", "color": "#1772B3"},
}

parties_map_and_colors_p25: dict[int, dict[str, str]] = {
    1: {"question": "p2501", "name": "PNV/EAJ", "color": "#02451F"},
    2: {"question": "p2502", "name": "EH Bildu", "color": "#006155"},
    3: {"question": "p2503", "name": "PSE-EE", "color": "#AE0A14"},
    4: {"question": "p2504", "name": "Sumar", "color": "#850F33"},
    5: {"question": "p2505", "name": "PP", "color": "#1D3F77"},
    6: {"question": "p2506", "name": "VOX", "color": "#486D1C"},
}
