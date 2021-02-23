import pyodbc
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os

# Access .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def get_closed_projects():

    # Provide database specific information with Secure Authentication
    cnxn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=" + str(os.getenv("Server1")) + ";"
        "Database=" + str(os.getenv("Database1")) + ";"
        "UID=" + str(os.getenv("UID1")) + ";"
        "PWD=" + str(os.getenv("PWD1")) + ";"
    )

    # connect to database
    cnxn = pyodbc.connect(cnxn_str)

    # Define SQL Query for Project Management Database
    # Finds Distinct, non-ACTIVE ProjectFolder numbers
    SQL_Query = ("SELECT DISTINCT(ProjectFolder) FROM (\n"
                 "SELECT [Name], [ParentFolder], [ProjectFolder], [Status_Code]\n"
                 "  FROM [DataManagementSvc].[Project] t1\n"
                 "  WHERE NOT EXISTS \n"
                 "  (\n"
                 "  SELECT [Name], [ParentFolder], [ProjectFolder], [Status_Code]\n"
                 "  FROM [DataManagementSvc].Project t2\n"
                 "  WHERE Status_Code = 'ACTIVE'\n"
                 "  and t1.ProjectFolder = t2.ProjectFolder\n"
                 "  )\n"
                 ") as A")

    # Extract results of SQL Query using Pandas
    closed_list = pd.read_sql(SQL_Query, cnxn)

    # Close database connection
    del cnxn

    return closed_list

def get_read_write_data():
    cnxn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=" + str(os.getenv("Server2")) + ";"
            "Database=" + str(os.getenv("Database2")) + ";"
            "UID=" + str(os.getenv("UID2")) + ";"
            "PWD=" + str(os.getenv("PWD2")) + ";"
    )

    # connect to database
    cnxn = pyodbc.connect(cnxn_str)

    # Gets Facility, Project, LastModifiedTime, and DirSizeMB
    LastModifiedTimes_Query = ("SELECT Facility, Project, LastModifiedTime, DirSizeMB FROM (\n"
                               "SELECT Facility, Project, LastModifiedTime, DirSizeMB FROM (\n"
                               "SELECT DISTINCT Facility, Project, LastModifiedTime, DirSizeMB FROM (\n"
                               "SELECT [dbo].[Projects_Drive_Creation].Facility, \n"
                               "		[dbo].[Projects_Drive_Creation].Project, \n"
                               "		[dbo].[Projects_Drive_LastModified].LastModifiedTime,\n"
                               "		[dbo].[Projects_Drive_Creation].DirSizeMB\n"
                               "		FROM [dbo].[Projects_Drive_Creation]\n"
                               "\n"
                               "FULL JOIN [dbo].[Projects_Drive_LastModified] ON \n"
                               "			[dbo].[Projects_Drive_Creation].Facility = [dbo].[Projects_Drive_LastModified].Facility AND\n"
                               "			[dbo].[Projects_Drive_Creation].Project = [dbo].[Projects_Drive_LastModified].Project\n"
                               "\n"
                               ") AS A WHERE (SELECT COUNT(DISTINCT LastModifiedTime) FROM (\n"
                               "SELECT [dbo].[Projects_Drive_Creation].Facility, \n"
                               "		[dbo].[Projects_Drive_Creation].Project, \n"
                               "		[dbo].[Projects_Drive_LastModified].LastModifiedTime,\n"
                               "		[dbo].[Projects_Drive_Creation].DirSizeMB\n"
                               "		FROM [dbo].[Projects_Drive_Creation]\n"
                               "\n"
                               "FULL JOIN [dbo].[Projects_Drive_LastModified] ON \n"
                               "			[dbo].[Projects_Drive_Creation].Facility = [dbo].[Projects_Drive_LastModified].Facility AND\n"
                               "			[dbo].[Projects_Drive_Creation].Project = [dbo].[Projects_Drive_LastModified].Project\n"
                               ") AS B WHERE B.Project = A.Project) != 0\n"
                               ") AS NoNull WHERE LastModifiedTime is not null\n"
                               ") AS NoWeird WHERE LastModifiedTime <= GETDATE() ORDER BY Project\n")

    # Gets Facility, Project, and LastAccessTime
    LastAccessTimes_Query = ("SELECT Facility, Project, LastAccessTime FROM (\n"
                             "SELECT Facility, Project, LastAccessTime FROM (\n"
                             "SELECT [dbo].[Projects_Drive_LastModified].Facility, \n"
                             "		[dbo].[Projects_Drive_LastModified].Project, \n"
                             "		[dbo].[Projects_Drive_LastModified].LastAccessTime\n"
                             "		FROM [dbo].[Projects_Drive_LastModified]\n"
                             "\n"
                             "\n"
                             ") AS NoNull WHERE LastAccessTime is not null\n"
                             ") AS NoWeird WHERE LastAccessTime <= GETDATE() ORDER BY Project\n")

    # Extract results of SQL Query using Pandas
    modified_times_list = pd.read_sql(LastModifiedTimes_Query, cnxn)
    access_times_list = pd.read_sql_query(LastAccessTimes_Query, cnxn)

    # Close database connection
    del cnxn

    return modified_times_list, access_times_list

def correct_anomalies():
    closed_projects = get_closed_projects()
    write_times, read_times = get_read_write_data()

    # finds projects in closed_projects that don't exist in write_times
    # differences = set(closed_projects.ProjectFolder).difference(write_times.Project)
    # print(differences)

    # list of project IDs that need to be corrected in closed_projects
    correction_list = ['20113035', '19000100', '20112021', '20113018', '18115107', '20113108', '20113004', '20113002', '19120036', '20113014', '20113019', '20112004', '20113022', '20112011', '20112012', '20113011', '19000500']

    for i in range(len(correction_list)):
        corrected = correction_list[i][:6] + '-' + correction_list[i][6:]
        # if project column of write_times contains corrected then fix closed_project's ProjectFolders
        if corrected in write_times.Project.values:
            closed_projects['ProjectFolder'] = closed_projects['ProjectFolder'].replace([correction_list[i]], corrected)

    # write/read_times contains active and closed projects, use closed_projects to restrict write/read_times to closed projects only
    closed_projects_list = closed_projects['ProjectFolder'].tolist()
    boolean_series1 = write_times.Project.isin(closed_projects_list)
    boolean_series2 = read_times.Project.isin(closed_projects_list)
    filtered_write_times = write_times[boolean_series1]
    filtered_read_times = read_times[boolean_series2]

    return filtered_write_times, filtered_read_times

def get_data():
    return correct_anomalies()

