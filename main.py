import pandas as pd
import numpy as np

def init_df():
    # Make creation date as first val and append on rest of mod dates
    # Convert dates to date data type with pd.to_datatime()

    # read data from csv file
    df = pd.read_csv('C:\\Users\\HaoliYin\\Documents\\Haoli Project Data\\Jan18AllData.csv')
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
    # df_org['ModDate'].replace('', np.nan, inplace=True)
    # df_org.dropna(subset=['ModDate'], inplace=True)

    # Change timestamp column to datetime variable type
    # df_org["ModDate"] = pd.to_datetime(df_org["ModDate"])

    save_df(df_org, 'organizedData.csv') # if want to save it

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
        modified_times.append(row.Timestamp)

    # Convert list to NumPy Object array (bc Timestamps have different dimensions)
    np_data = np.asarray(data, dtype=object)
    return np_data

if __name__ == "__main__":

    # reads and formats data csv file into dataframe
    df = init_df()

    # Turn DataFrame into NumPy array
    # np_data = to_numpy(df)

    # Split Data randomized (make sure not to mess up row vals tho) 70/30 into training and testing

    # Write function that takes in set of data and takes off final LastModifiedDate
    # to be put into separate prediction vector

