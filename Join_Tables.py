from SQL_Access import get_data
import pandas as pd
from datetime import date, timedelta
import pickle
import numpy as np


def get_binned_times(data, current_project_name, time_type):
    # get sub-table with rows from write_data matching the current project
    sub_table = data.loc[data['Project'] == current_project_name]

    # only use write times from the past 7 days
    past_week = sub_table[sub_table[time_type].dt.date > (date.today() - timedelta(weeks=1))]

    # bin write times by days
    last_data_time = past_week.groupby(pd.Grouper(key=time_type, freq='D')).size().tolist()

    # Fill with zeros before first day of week so that 7 values can be in the array
    num_zeros = 7 - len(last_data_time)
    zeros_list = [0] * num_zeros
    last_data_time = zeros_list + last_data_time

    return last_data_time


def join_tables():
    """
        Joins tables to look like this for every project:
        Facility, Project, DirSizeMB, [ModDay1Freq, ... ModDay7Freq], [AccessDay1Freq, ... AccessDay7Freq]

        Last_Times binned for the past 7 days

        returns: joined data (nested List)
    """

    write_data, read_data = get_data()
    data = []
    previous_project_name = write_data.iloc[0, 1]
    count = 0

    for row in write_data.itertuples(index=True, name='Pandas'):
        current_project_name = row.Project

        # detect new project and reset counter
        if current_project_name != previous_project_name:
            count = 0
            previous_project_name = current_project_name

        if count == 0:
            # if new project, then add basic project info
            project = [row.Facility, row.Project, row.DirSizeMB]

            last_modified_time = get_binned_times(write_data, current_project_name, 'LastModifiedTime')
            project += last_modified_time

            last_access_time = get_binned_times(read_data, current_project_name, 'LastAccessTime')
            project += last_access_time

            # add project to data
            data.append(project)

        count += 1

    return data


def export_data():
    data = join_tables()
    data_numpy = np.array(data)
    np.save("weekdata.npy", data_numpy)

export_data()
