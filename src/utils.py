def sort_by_order(lst, order):
    """Ordena lst según el orden definido en order."""
    order_index = {v: i for i, v in enumerate(order)}
    return sorted(lst, key=lambda x: order_index.get(x, 100))


def make_dict_iterable(d: dict[str, str]) -> dict[int, str]:
    """Convierte en enteros los indices el diccionario"""
    d = {int(k): str(v) for k, v in d.items()}
    return d
