import pandas as pd
import numpy as np

def init_df():
    # Make creation date as first val and append on rest of mod dates
    # Convert dates to date data type with pd.to_datatime()

    # read data from csv file
    df = pd.read_csv('C:\\Users\\HaoliYin\\Documents\\Haoli Project Data\\Jan16AllData.csv',
                     names=["Facility", "Project", "ModifiedDate", "CreationDate"])
    # Create new DataFrame
    # put creation date as first value and append rest of mod dates
    # dataframe looks like [[facility, project, [creation date, moddate1, moddate2, ...]],
    #                      [...],
    #                     ]
    data = []
    previous_project_name = df.iloc[0, 1]
    count = 0
    for row in df.itertuples(index=True, name='Pandas'):
        # if current is different from previous, reset count to 0
        current_project_name = row.Project
        if current_project_name != previous_project_name:
            count = 0
            previous_project_name = current_project_name
        if count == 0:
            temp = [row.Facility, row.Project, row.CreationDate]
            data.append(temp)
            temp1 = [row.Facility, row.Project, row.ModifiedDate]
            data.append(temp1)
        else:
            temp = [row.Facility, row.Project, row.ModifiedDate]
            data.append(temp)
        count += 1
    df_org = pd.DataFrame(data, columns=["Facility", "Project", "Timestamp"])

    # Get rid of empty spaces
    df_org['Timestamp'].replace('', np.nan, inplace=True)
    df_org.dropna(subset=['Timestamp'], inplace=True)

    # Change timestamp column to datetime variable type
    df_org["Timestamp"] = pd.to_datetime(df_org["Timestamp"])

    # save_df(df_org, 'organizedData.csv') if want to save it

    return df_org

def save_df(df, name):
    df.to_csv(name)


if __name__ == "__main__":

    # reads and formats data csv file into dataframe
    df = init_df()

    # Split Data randomized (make sure not to mess up row vals tho) 70/30 into training and testing

    # Write function that takes in set of data and takes off final LastModifiedDate
    # to be put into separate prediction vector

