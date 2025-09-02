sexo_map: dict[int, str] = {
    1: "Hombre",
    2: "Mujer",
}

# sexo_map_filter: dict[int, str] = {
#     1: "Todos",
#     2: "Hombre",
#     3: "Mujer",
# }

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

p25_tag_map: dict[int, str] = {
    0: "0",
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

lickert_tag_map_5: dict[int, str] = {
    1: "Muy buena",
    2: "Buena",
    3: "Mala",
    4: "Muy mala",
    5: "NS/NC",
}
lickert_tag_map_5_bastante: dict[int, str] = {
    1: "Muy buena",
    2: "Bastante buena",
    3: "Bastante mala",
    4: "Muy mala",
    5: "NS/NC",
}
lickert_tag_map_6: dict[int, str] = {
    1: "Muy buena",
    2: "Buena",
    3: "Regular",
    4: "Mala",
    5: "Muy mala",
    6: "NS/NC",
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
    1: "Únicamente\nvasco/a",
    2: "Más vasco/a\nque español/a",
    3: "Tanto vasco/a\ncomo español/a",
    4: "Más español/a\nque vasco/a",
    5: "Únicamente\nespañol/a",
    6: "NS/NC",
}

p35_tag_map: dict[int, str] = {
    1: "De acuerdo",
    2: "Según las\n circunstancias",
    3: "En desacuerdo",
    4: "NS/NC",
}


# t36: Competencia en euskera
p36_map: dict[int, str] = {
    1: "Bien",
    2: "Bastante bien",
    3: "Algo",
    4: "Sabe palabras",
    5: "Nada",
    6: "NS/NC",
}

# Agrupación Alto / Medio / Nulo
p36_grouped: dict[int, str] = {
    1: "Alto",  # Bien
    2: "Alto",  # Bastante bien
    3: "Medio/Bajo",  # Algo
    4: "Medio/Bajo",  # Sabe palabras
    5: "Ninguno",  # Nada
    6: "NS/NC",
}

p36_order: list[str] = ["Ninguno", "Medio/Bajo", "Alto", "NS/NC"]
# P37: Nivel de estudios
p37_map = {
    1: "Menos que primarios",
    2: "Primarios / ESO",
    3: "FP Medio o Superior",
    4: "Secundarios / Bachiller",
    5: "Universitarios",
    6: "NS/NC",
}

p37_grouped: dict[int, str] = {
    1: "Ninguno",  # TODO: comprobar
    2: "Primarios",
    3: "Secundarios",
    4: "Secundarios",
    5: "Superiores",
    6: "NS/NC",
}
p37_order: list[str] = ["Ninguno", "Primarios", "Secundarios", "Superiores", "NS/NC"]


# P38: Clase social
p38_map: dict[int, str] = {
    1: "Media-alta",
    2: "Media-media",
    3: "Media-baja",
    4: "NS/NC",
}
p38_order: list[str] = ["Media-baja", "Media-media", "Media-alta", "NS/NC"]

p39_map: dict[int, str] = {
    1: "Católico",
    2: "Católico",
    3: "Musulmán/a ",
    4: "Cristiano/a evangélico/a, protestante ",
    5: "Creyente de otra religión ",
    6: "Ateo/a ",
    7: "Agnóstico/a",
}
