import pandas as pd
import numpy as np

from datetime import datetime
def init_df():
    # Make creation date as first val and append on rest of mod dates
    # Convert dates to date data type with pd.to_datatime()

    # read data from csv file
    df = pd.read_csv('C:\\Users\\HaoliYin\\Documents\\Haoli Project Data\\Jan22AllData.csv')
    # if need to add header: , names=["Facility", "Project", "ModifiedDate", "CreationTime"]
    # Create new DataFrame
    # put creation date as first value and append rest of mod dates
    # dataframe looks like [[facility, project, [creation date, moddate1, moddate2, ...]],
    #                      [...],
    #                     ]
    data = []
    previous_project_name = df.iloc[0, 1]
    count = 0
    for row in df.itertuples(index=True, name='Pandas'):

        current_project_name = row.Project

        # detect new project and reset counter
        if current_project_name != previous_project_name:
            count = 0
            previous_project_name = current_project_name

        # if new project then add both creation and first modification date
        if count == 0:
            temp = [row.Facility, row.Project, row.CreationTime]
            data.append(temp)
            temp1 = [row.Facility, row.Project, row.LastModifiedTime]
            data.append(temp1)
        # else append next modification date
        else:
            temp = [row.Facility, row.Project, row.LastModifiedTime]
            data.append(temp)
        count += 1
    df_org = pd.DataFrame(data, columns=["Facility", "Project", "ModDate"])
    # Get rid of empty/null spaces
    df_org['ModDate'].replace('', np.nan, inplace=True)
    df_org.dropna(subset=['ModDate'], inplace=True)

    # Change timestamp column to datetime variable type
    # df_org["ModDate"] = pd.to_datetime(df_org["ModDate"])

    return df_org

def save_df(df, name):
    df.to_csv(name)

def to_numpy(df):
    # Only add Facility and Project name once
    previous_project_name = df.iloc[0, 1]
    data = []
    project_info = []
    modified_times = []
    count = 0
    for row in df.itertuples(index=True, name='Pandas1'):

        # Get current project row
        current_project_name = row.Project

        # Start new row of project information
        if current_project_name != previous_project_name:

            # Accounts for first case
            if count == 0:
                count += 1
            else:
                # Add project data to main list
                project_info.append(modified_times)
                data.append(project_info)

            # Reset for new project
            modified_times = []
            project_info = [row.Facility, row.Project]
            previous_project_name = current_project_name

        # Add next modified time
        modified_times.append(row.ModDate)

    # Convert list to NumPy Object array (bc Timestamps have different dimensions)
    np_data = np.asarray(data, dtype=object)
    return np_data

def to_datetime_differences(data):

    # Converts all LastModifiedDates to datetime variable
    for x in data:
        times = []
        for time in x[2]:
            times.append(datetime.strptime(time[0:19], '%Y-%m-%d %H:%M:%S'))
        x[2] = times

    # Find time relative to creation date
    for x in data:
        diffs = []
        for i in range(len(x[2])):
            if i == 0:
                continue
            else:
                # converts to difference in days
                diffs.append(round((x[2][i] - x[2][0]).total_seconds()/86400, 3))
        x[2] = diffs
    return data
if __name__ == "__main__":

    # reads and formats data csv file into dataframe
    df = init_df()

    # if want to save it
    # save_df(df, 'organizedData.csv')

    # Turn DataFrame into NumPy array
    # np_data = to_numpy(df)

    # Turns dates list into datetime variables
    # datetime_data = to_datetime_differences(np_data)
