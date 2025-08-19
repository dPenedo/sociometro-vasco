# %%
# Imports
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
from src.charts.plotly import create_0_to_10_percentage_bar_chart2
from src.config import df, p32_tag_map

import plotly.io as pio

# %%
#
df_filtered = df
print(
    type(
        create_0_to_10_percentage_bar_chart2(
            df_filtered,
            "p32",
            "Eje izquierda-derecha",
            "Ubicación ideológica en el eje izquierda-derecha",
            p32_tag_map,
        )
    )
)


# %%
#
