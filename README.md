# Overview

The data belongs to a dataset I got off of Kaggle, a popular website to download and view datasets. Here are the links to the datasets I downloaded: [Covid-19](https://www.kaggle.com/datasets/fireballbyedimyrnmom/us-counties-covid-19-dataset), [State Population](https://www.kaggle.com/datasets/alexandrepetit881234/us-population-by-state/data) 

Credit goes to PRIVACYMATTERS and ALEX for providing the datasets I used.

The Covid-19 dataset contains the number of Covid cases per day as well as the states and even counties. A unique column is the fips column that provides the last 5 digits that uniquely identify which county the data belongs to. Along with the number of deaths and date, I decided I wanted to use this data to make a timeline visualization of the US between the years of 2020-2022.

My purpose for creating the web app visiual was to help others understand how much impact Covid-19 had and its spread accross the US. This information is portrayed thanks to the Plotly Python library, and can be hosted on the web thanks to Dash which is another library provided by Plotly.

Here is a video demonstrasting the US visual and walkthrough of the code:

[US 2020-2022 Demo Video](https://youtu.be/BSfPIFSPDIo)

# Data Analysis Results

When you start the program, we are given a visual of the US states and the map of thier population density. I wanted this to be the first thing users saw to give them an idea how which states had the greater populations in 2020. When users select the visuals for COVID-19 Cases by State or by County, they can see that the majority of cases and even deaths will be greatly affected by the population density that we see from the default map. 

The data displayed in the 2020 Population map is a static map, but the visuals for COVID-19 Cases by State and COVID-19 Cases by County provide a timeline that users can interact with to see the spread of Covid-19 during the years 2020-2022. If users hover over the states or counties they will be able to see the state abbreviation/county code, as well as the number of cases and deaths the location had during the current date the timeline indicates. 

# Development Environment

The technologies used for this project:
- Visual Studio Code
- Python 3.12
- Git/ GitHub

The language I used for this project was Python and the following libraries:
- Pandas
- Plotly
- Dash


# Useful Websites

I found the following websites to be extremely helpful for this project:
* [Kaggle](https://www.kaggle.com/)
* [Plotly Documentation](https://plotly.com/python/getting-started/)
* [Dash Setup](https://dash.plotly.com/tutorial)
* [Color Palette Generator](https://coolors.co/)
* [Pandas Documentation](https://pandas.pydata.org/docs/user_guide/index.html)

# Future Work

Some things I wish to improve for this project:
* Add charts and visuals that update as time progresses on the timeline.
* At the time of this update there are currently five counties as far as I can tell that do not show results due to missing data. I hope to get more information to accurately portray the data.