import saga
import time
import csv
import random

cores_num = [16, 32, 48, 64, 128, 192, 256, 384, 512]
cores_list = [176.25, 352.50, 528.75, 705, 779.33, 847.67, 919, 935, 951]

run_time = [1, 30, 60, 300, 600]
run_time_small = [0, 412, 470, 623, 681] # 9-64 cores
run_time_med   = [0, 470, 614, 657, 748] # 65-256 cores
run_time_large = [0, 370, 419, 587, 659] # 257-512 cores

cores_rand = 0
time_rand = 0
cores = 0
runtime = 0
run_time_tmp = []

for i in range(1000000):

    cores_rand = random.random() * 951
    for j in range(len(cores_num)):
        if cores_rand < cores_list[j]:
            cores = cores_num[j]
            break

    if cores <= 64:
        run_time_tmp = run_time_small
    elif cores <= 256:
        run_time_tmp = run_time_med
    else:
        run_time_tmp = run_time_large


    time_rand = random.random() * run_time_tmp[-1]
    for k in range(1, len(run_time)):
        if time_rand < run_time_tmp[k + 1]:
            runtime = run_time[k] + ((run_time[k] - run_time[k - 1]) * (time_rand - run_time_tmp[k - 1]) / \
                    (run_time_tmp[k] - run_time_tmp[k -1]))
            runtime = int(runtime)
            break


    start = time.time()		#Initialize time for timing jobs
#    js    = saga.job.Service('pbs+ssh://mingtha@gordon.sdsc.xsede.org')
    js    = saga.job.Service('slurm+ssh://tg829619@stampede.tacc.utexas.edu')	#Defining 

    jd    = saga.job.Description()			#	Initializing SAGA

    jd.executable      = '/bin/true'		#	Defining mandatory executable, the POSIX empty workload
    jd.queue           = 'normal'			#	Defining the queue
    jd.project         = 'TG-MCB090174'		#	Defining the Allocation
    jd.total_cpu_count = cores				# 	Defining the Number of Cores
    jd.wall_time_limit = runtime   			#	Defining the Wall Time in Minutes
    
    j = js.create_job(jd)					#	Create the Job

    j.run()									#	Run the Job
    j.wait()								#	Wait for the job to run
    stop = time.time()						#	Stop the timer

    write_tmp = []

    print 'created:%s,started:%s,finished:%s,timed:%10.10f,cores:%d,wall_time:%d' \
        %(j.created, j.started, j.finished, stop - start, jd.total_cpu_count, jd.wall_time_limit)

    write_tmp.append([j.created, j.started, j.finished, (stop - start), jd.total_cpu_count, jd.wall_time_limit])
    
    with open("queue_time.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(write_tmp)

# print 'started %s :', j.started	# PENDING_ACTIVE
# print 'finished :', j.finished	# ACTIVE
# print 'Queue Time:', float(j.finished) - float(j.started)

# print 'timed    :', stop - start


