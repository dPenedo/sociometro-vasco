import plotly.colors as pc
from src.config.colors import red_green_color_list


default_layout = dict(
    font=dict(size=14),
    height=500,
    hoverlabel=dict(font_size=14),
    margin=dict(l=10, r=10, t=60, b=40),
)


def apply_default_layout(fig, custom_layout=None):
    layout = default_layout.copy()
    if custom_layout:
        layout.update(custom_layout)
    fig.update_layout(**layout)
    return fig


def get_color_map_from_scale(
    categories, scale=red_green_color_list, special_label="Ns/Nc"
):
    numeric_values = [v for v in categories if v != special_label]
    colors = pc.sample_colorscale(scale, len(numeric_values))
    color_map = {v: colors[i] for i, v in enumerate(numeric_values)}
    color_map[special_label] = "#808080"
    return color_map
