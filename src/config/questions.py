p25_tag_map: dict[int, str] = {
    0: "0 - Ninguna simpatía",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "Ns/Nc",
}


idioma_map: dict[int, int] = {
    1: 1,
    2: 1,
    3: 2,
}

idioma_text_map: dict[str, list[int]] = {
    "Todos": [1, 2, 3],
    "Euskera": [1, 2],
    "Castellano": [3],
}

sexo_map: dict[int, str] = {
    1: "Hombre",
    2: "Mujer",
}

ordered_p25_list: list[str] = [
    "0 - Ninguna simpatía",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Ns/Nc",
]


lickert_tag_map_5: dict[int, str] = {
    1: "Muy buena",
    2: "Buena",
    3: "Mala",
    4: "Muy mala",
    5: "NS-NC",
}
lickert_tag_map_5_bastante: dict[int, str] = {
    1: "Muy buena",
    2: "Bastante buena",
    3: "Bastante mala",
    4: "Muy mala",
    5: "NS-NC",
}
lickert_tag_map_6: dict[int, str] = {
    1: "Muy buena",
    2: "Buena",
    3: "Regular",
    4: "Mala",
    5: "Muy mala",
    6: "NS-NC",
}

p32_tag_map: dict[int, str] = {
    0: "0\nExt. Izquierda",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5\nCentro",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10\nExt. Derecha",
    11: "NS/NC",
}

p33_tag_map: dict[int, str] = {
    0: "0\nNada abertzale",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10\nMuy abertzale",
    11: "NS/NC",
}

p34_tag_map: dict[int, str] = {
    1: "ÚNICAMENTE\nVASCO/A",
    2: "MÁS VASCO/A\nQUE ESPAÑOL/A",
    3: "TANTO VASCO/A\nCOMO ESPAÑOL/A",
    4: "MÁS ESPAÑOL/A\nQUE VASCO/A",
    5: "ÚNICAMENTE\nESPAÑOL/A",
    6: "NS/NC",
}

p35_tag_map: dict[int, str] = {
    1: "DE ACUERDO",
    2: "SEGÚN LAS\n CIRCUNSTANCIAS",
    3: "EN DESACUERDO",
    4: "NS-NC",
}
