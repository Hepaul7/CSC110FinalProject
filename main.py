"""
Name: The negative consequences of COVID-19 on NAICS categorized industries in Canada
Part: main

Module Description
===============================
The main module of the 'The negative consequences of COVID-19 on NAICS categorized industries in
Canada' project.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please email Paul.He@mail.utoronto.ca.

This file is Copyright (c) 2021 Paul He, Jiawei Yu and Xiling Zhao
"""

from open_up_the_file_for_industry import open_up_and_process_gdp_data
from open_up_the_file_for_covid import final_covid_sum_up
from visualize import plot_covid_month
from graph3 import plot_graph3, create_dataset_score
from graph2 import plot_graph2_px

if __name__ == '__main__':
    # load data
    covid_data = final_covid_sum_up('covid19.csv')
    industries = open_up_and_process_gdp_data('gdp_data.csv')

    # plot graph 1
    plot_covid_month(covid_data)

    # plot graph 2 interactive
    plot_graph2_px(industries)

    # plot graph 3 interactive
    dataset_score = create_dataset_score('gdp_data.csv')
    plot_graph3(dataset_score)
