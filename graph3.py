"""
Name: The negative consequences of COVID-19 on NAICS categorized industries in Canada
Part: graph3

Module Description
===============================
The module of producing score bar chart for regular industries

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please email Paul.He@mail.utoronto.ca.

This file is Copyright (c) 2021 Paul He, Jiawei Yu and Xiling Zhao
"""
import pandas as pd
import plotly.express as px


import scoring


def create_dataset_score(filename: str) -> dict[str, list]:
    """Given a list of industries, it creates a dataset based on score calculated"""
    # calculate score producing a tuple consisting three lists
    score = scoring.output_score(filename)
    # assign each list to a variable
    x, y1, y2 = score
    # create a dataset
    dataset = {'Industry': [], 'Score1': [], 'Score2': []}
    for i in range(len(x)):
        dataset['Industry'].append(x[i])
        dataset['Score1'].append(y1[i])
        dataset['Score2'].append(y2[i])
    return dataset


def plot_graph3(dataset: dict[str, list]) -> None:
    """Plots the graph given the dataset"""
    # use pandas to convert dataset into dataframe
    dataframe = pd.DataFrame(data=dataset)
    # create figure (bar chart)
    figure = px.bar(
        dataframe, x='Industry', y=['Score1', 'Score2'],
        title='Industry and its Score (you may select which scores to display)')
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
