from SQL_Access import get_data
import pandas as pd
from datetime import date, timedelta
# TODO: Format data to look like


def join_tables():
    """
        Joins tables to look like this for every project:
        Facility, Project, DirSizeMB, [LastModifiedTime...], [LastAccessTime...]

        Last_Times binned for the past 7 days

        returns: joined data
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

            # initialize empty lists
            last_modified_time = []
            last_access_time = []

            # get sub-table with rows from write_data matching the current project
            get_sub_write = write_data.loc[write_data['Project'] == current_project_name]

            # only use write times from the past 7 days
            write_week = get_sub_write[get_sub_write['LastModifiedTime'].dt.date >= (date.today() - timedelta(weeks=1))]

            # bin write times by days
            last_modified_time = write_week.groupby(pd.Grouper(key='LastModifiedTime', freq='D')).size()

            # TODO: Convert LastModifiedTime Object type to normal int list type, fill array up to size 7 with missing 0's at beginning of array

            project.append(last_modified_time)
            # get sub-table with rows from read_data matching the current project
            get_sub_read = read_data.loc[read_data['Project'] == current_project_name]

            # turn LastAccessTime column into a list and append to current project
            last_access_time = get_sub_read['LastAccessTime'].tolist()
            project.append(last_access_time)

            # add project to data
            data.append(project)

        count += 1

    return data

joined_data = join_tables()
print(joined_data)


# TODO: join dataframes to look like:
'''
    Facility, Project, DirSizeMB, [ModDay1Freq, ... ModDay7Freq], [AccessDay1Freq, ... AccessDay7Freq] 
'''

