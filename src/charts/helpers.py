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


def generate_hovertemplate(show_y_as_name: bool = False) -> str:
    """
    Hovertemplate estándar.
    """
    hover = "<b>%{customdata[0]}</b><br>"
    if show_y_as_name:
        hover += "%{y}<br>"
    hover += "Porcentaje: %{customdata[2]:.1f}%<br>"
    hover += "Conteo: %{customdata[1]}<extra></extra>"
    return hover
