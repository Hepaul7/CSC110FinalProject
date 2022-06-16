"""
Name: The negative consequences of COVID-19 on NAICS categorized industries in Canada
Part: graph2

Module Description
===============================
The module of producing Industry GDP line graph over time.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please email Paul.He@mail.utoronto.ca.

This file is Copyright (c) 2021 Paul He, Jiawei Yu and Xiling Zhao
"""
import datetime
from dataclasses import dataclass

import pandas as pd
import plotly.express as px

from visualize import create_dataset


@dataclass
class Industry:
    """Dataclass Industry with attributes name and gdp"""
    name: str
    gdp: dict[datetime.date, int]


def plot_graph2_px(industries: list[Industry]) -> None:
    """Plot an interactive line graph given a list of Industry
    """
    # create a dataset by calling the function create_dataset
    dataset = create_dataset(industries)
    # use pandas to covert dataset into a dataframe
    dataframe = pd.DataFrame(data=dataset)
    # use plotly to create graph based on given dataframe
    figure = px.line(dataframe, x='Date', y='GDP', color='Industry',
                     title='Date and GDP per Industry')
    figure.show()


if __name__ == '__main__':
    import doctest
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['dash', 'pandas', 'numpy', 'datetime', 'dash.dependencies',
                          'plotly.express',
                          'dataclasses',
                          'open_up_the_file_for_industry', 'visualize', 'scoring'],
        'allowed-io': ['open_up_and_process_data_for_gdp_v1', 'scoring'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    doctest.testmod()
