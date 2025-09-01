def add_bar_labels(fig, df, x_col, y_col, y_shift=10):
    for _, row in df.iterrows():
        fig.add_annotation(
            x=row[x_col],
            y=row[y_col] + 0.5,
            text=f"{row[y_col]:.1f}%",
            showarrow=False,
            font=dict(size=10),
            yshift=y_shift,
        )
    return fig


def generate_hovertemplate(
    percent_label: str = "Porcentaje",
    count_label: str = "Conteo",
    show_y_as_name: bool = False,
) -> str:
    """
    Hovertemplate estándar que admite etiquetas dinámicas y traducciones.
    """
    if show_y_as_name:
        template = (
            "<b>%{x}</b><br>"
            f"{percent_label}: %{{customdata[2]:.1f}}%<br>"
            f"{count_label}: %{{customdata[0]}}<extra></extra>"
        )
    else:
        template = (
            "<b>%{customdata[0]}</b><br>"
            f"{percent_label}: %{{customdata[2]:.1f}}%<br>"
            f"{count_label}: %{{customdata[1]}}<extra></extra>"
        )
    return template
