from typing import Dict, List

p25_tag_map: Dict[int, str] = {
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

sexo_map: Dict[int, str] = {
    1: "Hombre",
    2: "Mujer",
}


idioma_map: Dict[int, int] = {
    1: 1,
    2: 1,
    3: 2,
}

idioma_text_map: Dict[str, List[int]] = {
    "Todos": [1, 2, 3],
    "Euskera": [1, 2],
    "Castellano": [3],
}

sexo_map: Dict[int, str] = {
    1: "Hombre",
    2: "Mujer",
}

ordered_p25_list: List[str] = [
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


lickert_tag_map_5: Dict[int, str] = {
    1: "Muy buena",
    2: "Buena",
    3: "Mala",
    4: "Muy mala",
    5: "NS/NC",
}
lickert_tag_map_5_bastante: Dict[int, str] = {
    1: "Muy buena",
    2: "Bastante buena",
    3: "Bastante mala",
    4: "Muy mala",
    5: "NS/NC",
}
lickert_tag_map_6: Dict[int, str] = {
    1: "Muy buena",
    2: "Buena",
    3: "Regular",
    4: "Mala",
    5: "Muy mala",
    6: "NS/NC",
}

p32_tag_map: Dict[int, str] = {
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

p33_tag_map: Dict[int, str] = {
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

p34_tag_map: Dict[int, str] = {
    1: "Únicamente\nvasco/a",
    2: "Más vasco/a\nque español/a",
    3: "Tanto vasco/a\ncomo español/a",
    4: "Más español/a\nque vasco/a",
    5: "Únicamente\nespañol/a",
    6: "NS/NC",
}

p35_tag_map: Dict[int, str] = {
    1: "De acuerdo",
    2: "Según las\n circunstancias",
    3: "En desacuerdo",
    4: "NS/NC",
}


# P36: Competencia en euskera
p36_map = {
    1: "Bien",
    2: "Bastante bien",
    3: "Algo",
    4: "Sabe palabras",
    5: "Nada",
    6: "NS/NC",
}

# Agrupación Alto / Medio / Nulo
p36_grouped = {
    1: "Alto",  # Bien
    2: "Alto",  # Bastante bien
    3: "Medio/Bajo",  # Algo
    4: "Medio/Bajo",  # Sabe palabras
    5: "Ninguno",  # Nada
    6: "NS/NC",
}

p36_order = [
    "Ninguno",
    "Medio/Bajo",
    "Alto",
]
# P37: Nivel de estudios
p37_map = {
    1: "Menos que primarios",
    2: "Primarios / ESO",
    3: "FP Medio o Superior",
    4: "Secundarios / Bachiller",
    5: "Universitarios",
    6: "NS/NC",
}

# TODO: decidir cómo agrupar
p37_grouped = {
    1: "Ninguno",  # TODO: comprobar
    2: "Primarios",
    3: "Secundarios",
    4: "Secundarios",
    5: "Superiores",
    6: "NS/NC",
}
p37_order = [
    "Ninguno",
    "Primarios",
    "Secundarios",
    "Superiores",
]


# P38: Clase social
p38_map = {
    1: "Media-alta",
    2: "Media-media",
    3: "Media-baja",
    4: "NS/NC",
}
p38_order = ["Media-baja", "Media-media", "Media-alta"]

p39_map = {
    1: "Católico",
    2: "Católico",
    3: "Musulmán/a ",
    4: "Cristiano/a evangélico/a, protestante ",
    5: "Creyente de otra religión ",
    6: "Ateo/a ",
    7: "Agnóstico/a",
}
