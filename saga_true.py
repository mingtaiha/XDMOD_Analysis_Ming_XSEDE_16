import saga
import time



start = time.time()		#Initialize time for timing jobs
js    = saga.job.Service('pbs+ssh://mingtha@gordon.sdsc.xsede.org')
#	js    = saga.job.Service('slurm+ssh://tg829619@stampede.tacc.utexas.edu')	#Defining 

jd    = saga.job.Description()			#	Initializing SAGA

jd.executable      = '/bin/true'		#	Defining mandatory executable, the POSIX empty workload
jd.queue           = 'normal'			#	Defining the queue
jd.project         = 'TG-MCB090174'		#	Defining the Allocation
jd.total_cpu_count = 8					# 	Defining the Number of Cores
jd.wall_time_limit = 1					#	Defining the Wall Time
    
j = js.create_job(jd)					#	Create the Job

j.run()									#	Run the Job
j.wait()								#	Wait for the job to run
stop = time.time()						#	Stop the timer



print 'created  :', j.created	# 

print 'started  :', j.started	# PENDING_ACTIVE

print 'finished :', j.finished	# ACTIVE

print 'Queue Time:', float(j.finished) - float(j.started)

#print 'timed    :', stop - start


