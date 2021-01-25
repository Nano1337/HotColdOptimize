import numpy as np
import scipy
import array
import math
from matplotlib import rcParams
from matplotlib.pyplot import figure, plot, xlabel, ylabel, title, show, savefig, hist

from main import init_df, to_numpy, to_datetime_differences

def optimize_bin(diffs):
    data = diffs
    data_max = max(data)  # lower end of data
    data_min = min(data)  # upper end of data
    n_min = 2  # minimum number of bins
    n_max = 200  # maximum number of bins
    n_shift = 30  # number of shifts
    N = np.array(range(n_min, n_max))
    D = float(data_max-data_min)/N  # Bin width vector
    Cs = np.zeros((len(D), n_shift))  # Cost function vector

    # Computation of the cost function
    for i in range(np.size(N)):
        shift = np.linspace(0, D[i], n_shift)
        for j in range(n_shift):
            edges = np.linspace(data_min+shift[j]-D[i]/2, data_max+shift[j]-D[i]/2, N[i]+1)  # shift the Bin edges
            binindex = np.digitize(data, edges)  # Find binindex of each data point
            ki = np.bincount(binindex)[1:N[i]+1]  # Find number of points in each bin
            k = np.mean(ki)  # Mean of event count
            v = sum((ki-k)**2)/N[i]  # Variance of event count
            Cs[i,j] += (2*k-v)/((D[i])**2)  # The Cost Function
    C = Cs.mean(1)

    # Optimal Bin Size Selection
    loc = np.argwhere(Cs == Cs.min())[0]
    cmin = C.min()
    idx = np.where(C == cmin)
    idx = idx[0][0]
    optD = D[idx]

    # print('Optimal Bin Number : ', N[idx])
    # print('Optimal Bin Width :', optD)
    # plot_graphs(data, data_min, data_max, N, C, D, idx, shift, loc, cmin)

    return N[idx]


def plot_graphs(data, data_min, data_max, N, C, D, idx, shift, loc, cmin):
    # Plot
    edges = np.linspace(data_min + shift[loc[1]] - D[idx] / 2, data_max + shift[loc[1]] - D[idx] / 2, N[idx] + 1)
    rcParams.update({'figure.autolayout': True})
    fig = figure()
    ax = fig.add_subplot(111)
    ax.hist(data, edges)
    title(u"Histogram")
    ylabel(u"Frequency")
    xlabel(u"Value")
    show()
    fig = figure()
    plot(N, C, '.b', N[idx], cmin, '*r')
    xlabel('Number of bins')
    ylabel('Cobj')
    show()

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

    # Make function to calculate probability at least one event would occur in less than 30 days
    # Figure out how to calculate lambda

    # Create optimum binning algorithm function - on GitHub to get optimum lambda
    opt_bin = optimize_bin(diff_times)

    # Calculate Lambda
    p_lambda = len(diff_times)/opt_bin

    # Apply Probability Mass Function formula to find P(T <= 7 days)
    prob = 1-math.exp(-1*p_lambda*7)
    print(prob)
