

import pandas as pd
import plotly.express as px

# Example state-level dataset
# Replace this with your actual CSV file
df = pd.read_csv("us_pop_by_state.csv")  # should have a 'state' column with abbreviations like 'NY', 'FL', etc.


fig = px.choropleth(df,
                    locations='state_code',
                    locationmode="USA-states",
                    color='2020_census',
                    scope="usa",
                    color_continuous_scale="Viridis",
                    range_color=(1_000_000, 40_000_000),
                    labels={'2020_census':'Population by State in 2020'}
                   )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()