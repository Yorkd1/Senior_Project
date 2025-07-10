
import pandas as pd
import plotly.express as px

# State name to abbreviation mapping
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Load CSV and parse dates
df = pd.read_csv('covid19.csv', parse_dates=['date'])

# Ensure date is datetime
df['date'] = pd.to_datetime(df['date'])

# Aggregate by state and date
state_df = df.groupby(['state', 'date'], as_index=False)[['cases', 'deaths']].sum()

# Map full state names to abbreviations
state_df['state_abbrev'] = state_df['state'].map(state_abbrev)

# Drop rows with missing abbreviations (in case of territories or typos)
state_df = state_df.dropna(subset=['state_abbrev'])

# Sort by date
state_df = state_df.sort_values('date')

# Remove duplicates if any (precaution)
state_df = state_df.drop_duplicates(subset=['state_abbrev', 'date'])


# Plot animated choropleth map
fig = px.choropleth(
    state_df,
    locations='state_abbrev',
    locationmode='USA-states',
    color='cases',
    animation_frame='date',
    scope='usa',
    color_continuous_scale='Reds',
    labels={'cases': 'Total Cases'},
    hover_data=['deaths']
)

fig.update_layout(title_text='COVID-19 Cases by US State (2020–2022)')
fig.show()

