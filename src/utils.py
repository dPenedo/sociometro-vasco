def sort_by_order(lst, order):
    """Ordena lst según el orden definido en order."""
    order_index = {v: i for i, v in enumerate(order)}
    return sorted(lst, key=lambda x: order_index.get(x, 100))
