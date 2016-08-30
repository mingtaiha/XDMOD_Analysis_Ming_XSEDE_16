import csv
import os
import sys
import pprint
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from operator import itemgetter



pp = pprint.PrettyPrinter(indent=4)

def clean_csv_xdmod(mypath):

    csv_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) and "cleaned" not in f]
    csv_files.sort()

    for c in csv_files:
        csv_in = open(mypath + c, 'rb')
        csv_out = open(mypath + "cleaned_" + c, 'wb')
        reader = csv.reader(csv_in)
        writer = csv.writer(csv_out)

        row_ct = 0
        for row in reader:
            if row_ct < 7:
                row_ct += 1
                continue
            else:
                if "--" in row[0]:
                    continue
                else:
                    writer.writerow(row)

        csv_in.close()
        csv_out.close()



def aggregate_csv_xdmod(mypath, name):
    
    csv_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) and "cleaned" in f]
    csv_files.sort()

    csv_out = pd.DataFrame(index=[], columns=[])

    for c in csv_files:
        csv_in = pd.read_csv(mypath + c)
        csv_in = csv_in.set_index('Day')
        csv_out = csv_out.append(csv_in)

    csv_out.to_csv(name)



def csv_to_pd(filename):

#   Reading in the csv file
    pd_file = pd.read_csv(filename)
    
#   Formatting all the data frames
    new_cols = list(pd_file.columns.values)
    new_cols[0] = 'Day'
    pd_file.columns = new_cols
    pd_file = pd_file.set_index('Day')

    return pd_file



def cross_correlation(file1, file2):
   

#   Reading in the csv's of the specified metric, as well as the resource availability csv
    pd_x = csv_to_pd(file1)
    pd_y = csv_to_pd(file2)
    pd_avail = csv_to_pd('cleaned_resource_availability.csv')
    
#   Defining dictionary for easy mapping from number to (resource, metric)

    dict_x = dict(zip([i for i in range(len(pd_x.columns))], list(pd_x.columns.values)))
    dict_y = dict(zip([i for i in range(len(pd_y.columns))], list(pd_y.columns.values)))
    dict_avail = dict(zip([i for i in range(len(pd_avail.columns))], list(pd_avail.columns.values)))

#   Doing it for every resource

    for resource in range(len(pd_avail.columns)):

#   Removing the Nan entries of the series, as they symbolize days when the machine is
#   not in service (either the machine is running, or when the machine is no longer in 
#   service)
        series_x = pd_x[pd_x[dict_x[resource]].notnull()][dict_x[resource]]
        series_y = pd_y[pd_y[dict_y[resource]].notnull()][dict_y[resource]]
        series_avail = pd_avail[pd_avail[dict_avail[resource]].notnull()][dict_avail[resource]]
  
#   Removing the initial long sequence of 0's. Currently believe that a resource has a
#   long sequence of 0's initially because the machine is up and running, but not available
#   for XSEDE use
        start_date = series_avail.nonzero()[0][0]
        end_date = series_avail.nonzero()[0][-1] + 1
        series_x = series_x.iloc[start_date : end_date]
        series_y = series_y.iloc[start_date : end_date]
        series_avail = series_avail.iloc[start_date : end_date]

######   Beginning of the Cross-Correlation

#   Defining the Means

        mean_x = series_x.mean()
        mean_y = series_y.mean()

#   Defining the denominator of the sample cross-correlation, which is the product of the
#   standard deviations of random variables
        std_x = 0
        std_y = 0
        run_days = len(series_avail.index)
        for i in range(run_days):
            std_x += (series_x.iloc[i] - mean_x) * (series_x.iloc[i] - mean_x)
            std_y += (series_y.iloc[i] - mean_y) * (series_y.iloc[i] - mean_y)
        denom = sqrt(std_x * std_y)

#   Defining the numerator, which is the covariance of the two random variables
#   This will be done for all possible lag values to see any correlation for any
#   lag period

        lag_list = [i for i in range(run_days)]
        r_list = list()
   
        for lag in lag_list:
            numer = 0
            for i in range(run_days - lag):
                numer += (series_x.iloc[i] - mean_x) * (series_y.iloc[i + lag] - mean_y)

            r = numer / denom
            r_list.append(r)

        series_r = pd.Series(r_list)

#   Getting the parameter names for x, y, as well as the resource name

        param_x = filename1[8:]
        param_x = param_x[:len(param_x) - 4]
        param_y = filename2[8:]
        param_y = param_y[:len(param_y) - 4]
        res = dict_avail[resource].split('[')[1].split(']')[0]

#   Plotting and saving the image

        plt.figure()
        ax = series_r.plot(kind='line')
        ax.set_title(param_x + " vs " + param_y)
        ax.set_xlabel('Lag (Day)')
        ax.set_ylabel('R - (Cross or Auto) Correlation')
        ax.set_xlim(0, 7)
        ax.set_ylim(-1.0, 1)
        plt.savefig('correlogram_' + param_x + '_' + param_y + '_' + res + '_' + '.png', bbox_inches='tight')
        plt.close()



def avg_wall_time(wall_time_file, num_jobs_run_file):
    
    wall_time = csv_to_pd(wall_time_file)
    jobs_run = csv_to_pd(num_jobs_run_file)

#    pp.pprint(zip([i for i in range(len(wall_time.columns))], list(wall_time.columns.values)))
#    pp.pprint(zip([i for i in range(len(jobs_run.columns))], list(jobs_run.columns.values)))

    wall_time_res_mask = [7, 8, 12]
    jobs_run_res_mask = [26, 28, 37]
    mask_to_res = { 7: "Comet", 8: "Gordon", 12: "Stampede" }
    
    start_date = wall_time.index[0]
    stop_date = wall_time.index[-1]

    jobs_run = jobs_run[start_date:stop_date]
    print jobs_run.index[0], jobs_run.index[-1]

    avg_jobs_run = dict()
    total_sum = list()
    total_jobs = list()
    for i in range(len(wall_time_res_mask)):
        tmp_sum_by_res = 0
        for j in range(len(jobs_run.index)):
            tmp_sum_by_res += wall_time.iloc[j, wall_time_res_mask[i]] * jobs_run.iloc[j, jobs_run_res_mask[i]]
        
        total_sum.append(tmp_sum_by_res)
        total_jobs.append(jobs_run.iloc[:, jobs_run_res_mask[i]].sum())
        tmp_sum_by_res /= total_jobs[i]
        avg_jobs_run[mask_to_res[wall_time_res_mask[i]]] = tmp_sum_by_res
    
    avg_jobs_run["Average across resources"] = sum(total_sum) / sum(total_jobs)
    pp.pprint(avg_jobs_run) 



def avg_wall_time_node(wall_time_file, num_jobs_run_file, dict_filename):

    wall_time = csv_to_pd(wall_time_file)
    jobs_run = csv_to_pd(num_jobs_run_file)

    wall_time_col = [wall_time.columns[i].split(']')[0].split('[')[1] for i in range(len(wall_time.columns))]
    jobs_run_col = [jobs_run.columns[i].split(']')[0].split('[')[1] for i in range(len(jobs_run.columns))]
    
    wall_time.columns = wall_time_col
    jobs_run.columns = jobs_run_col

    node_count = wall_time_col
    total_sum = list()
    avg_job_run = list()
    
    for nc in range(len(node_count)):
        tmp_sum_by_nc = 0
        for day in range(len(jobs_run.index)):
            tmp_sum_by_nc += wall_time.iloc[day, nc] * jobs_run.iloc[day, nc]
        
        total_sum.append(tmp_sum_by_nc)
        tmp_total_jobs = jobs_run.iloc[:, nc].sum()
        tmp_sum_by_nc /= tmp_total_jobs
        avg_job_run.append((int(node_count[nc]), tmp_sum_by_nc, tmp_total_jobs))
    
    avg_job_run.sort(key=itemgetter(0))
#    pp.pprint(avg_job_run)

    with open(dict_file, 'wb') as c:
        writer = csv.writer(c)
        writer.writerow(['Node Count', 'Average Execution Time', 'Number of Jobs'])
        for i in range(len(avg_job_run)):
            writer.writerow(avg_job_run[i])



def plot(filename):
    
    df = csv_to_pd(filename)
    pd_avail = csv_to_pd('cleaned_resource_availability.csv')
    col_name = df.columns[26]
    series = df.iloc[:,26]
    series_avail = pd_avail.iloc[:,26]

    series = series[series.notnull()]
    series_avail = series_avail[series_avail.notnull()]
    
    start_date = series_avail.nonzero()[0][0]
    end_date = series_avail.nonzero()[0][-1] + 1
    series = series.iloc[start_date : end_date]
    series_avail = series_avail.iloc[start_date : end_date]
    
    print series

    plt.figure()
    ax = series.plot(kind='scatter')


filename = sys.argv[1]
plot(filename)


"""
def avg_wall_time_agg(*filenames):

    res = list()
    for i in range(1, len(filenames[0])):
        filename = filenames[0][i]
        tmp_res = list()
        
        with open(filename, 'r') as c:
            reader = csv.reader(c)
            for row in reader:
                tmp_res.append(row)
            del tmp_res[0]
            res.append(tmp_res)
    pp.pprint(res)

    agg_res = list()
    for j in range(30):
        total_jobs = 0
        avg_exec_time = 0
        for i in range(len(filenames[0]) - 1):
            #print float(res[i][j][1]), float(res[i][j][2])
            total_jobs += float(res[i][j][2])
            avg_exec_time += float(res[i][j][1]) * float(res[i][j][2])
        avg_exec_time /= total_jobs
        print avg_exec_time
"""
    

"""
if len(sys.argv) == 2 :
    folderpath = sys.argv[1]
    clean_csv_xdmod(folderpath)
if len(sys.argv) == 3:
    aggr_name = sys.argv[2]
    folderpath = sys.argv[1]
    aggregate_csv_xdmod(folderpath, aggr_name)
if len(sys.argv) == 4:
"""

"""
folderpath = sys.argv[1]
clean_csv_xdmod(folderpath)

folderpath = sys.argv[1]
aggr_name = sys.argv[2]
aggregate_csv_xdmod(folderpath, aggr_name)
"""


#filename1 = sys.argv[1]
#filename2 = sys.argv[2]
#dict_file = sys.argv[3]
#cross_correlation(filename1, filename2)
#avg_wall_time_node(filename1, filename2, dict_file)
#avg_wall_time_agg(sys.argv)
