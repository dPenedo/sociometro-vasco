# %%
# Imports
import pandas as pd
from src.config import df

# %%
# Data types
for col in df.columns.to_list():
    print(f"Data type of {col} is {df[col].dtypes}")

# %%
# Convert
df.p32[pd.isnull(df.p32)]
# %%
#
