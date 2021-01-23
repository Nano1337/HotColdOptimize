import numpy as np

from main import init_df, to_numpy, to_datetime_differences

if __name__ == "__main__":
    # Get numpy array of project with most LastModifiedDates
    df = init_df()
    np_data = to_numpy(df)
    np_diff = to_datetime_differences(np_data)

    # Finding Project 201332-09 to experiment with Poisson Point Process
    project_info = []
    for project in np_diff:
        if '201332-09' in project[1]:
            project_info = project
    # Get list of relative modification dates without creation date
    modtimes = []
    initial = project_info[2][0]
    for i in range(1, len(project_info[2])):
        modtimes.append(round(project_info[2][i]-initial, 3))

    # Gets difference between modified days
    diff_times = [modtimes[0]]
    for i in range(len(modtimes)-1):
        diff_times.append(round(modtimes[i+1]-modtimes[i], 3))

    p_lambda = sum(diff_times)/len(diff_times)
    print(p_lambda)
    # Make function to calculate probability at least one event would occur in less than 30 days
    # Figure out how to calculate lambda

    # Create optimum binning algorithm function - on GitHub to get optimum lambda