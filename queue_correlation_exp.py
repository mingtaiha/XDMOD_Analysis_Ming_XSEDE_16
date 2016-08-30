import sys
import json
import time
import random

import saga
import karnak_reader as kr

SLEEP_TIME = 60 

res_to_karnak_map = { 'stampede'    : 'stampede.tacc.xsede.org',
                      'gordon'      : 'gordon.sdsc.xsede.org',
                      'comet'       : 'comet.sdsc.xsede.org'
                    }

def rand_select(cores_node_map, job_dist, avg_exec_dist):

    rng = random.uniform(0, 100)

    cores_list = list()
    for key in cores_node_map:
        cores_list.append(int(key))
    cores_list.sort()

    job_dist_list = list()

    choice = -1
    for cores in range(len(cores_list)):
        if rng <= job_dist[str(cores_list[cores])]:
            choice = cores
            break

    return cores_node_map[str(cores_list[choice])], avg_exec_dist[str(cores_list[choice])]


if sys.argv[1] == "help":
    print "python queue_correlation_exp <resource>"
    print "\n\n"
    print "resource = {stampede, gordon, comet}"
    sys.exit()

if sys.argv[1] == "stampede" or sys.argv[1] == "gordon" or sys.argv[1] == "comet": 
    res = sys.argv[1]
    random.seed()

else:
    sys.exit


with open('resource_handle.json') as j_file:
    conf = json.load(j_file)

res_conf = conf[res]

cores, exec_time = rand_select(res_conf['cores_node_map'], res_conf['cores_job_dist'], res_conf['avg_exec_time'])

js = saga.job.Service(res_conf['access_schema']+"://"+res_conf["username"]+"@"+res_conf["saga_id"])
jd = saga.job.Description()

jd.executable = "/bin/sleep"
jd.arguments = ['-m', str(SLEEP_TIME)]
jd.queue = res_conf["queue"]
jd.project = res_conf["project"]
jd.total_cpu_count = res_conf["cores_job_dist"][str(cores)]
jd.wall_time_limit = SLEEP_TIME
#jd.wall_time_limit = exec_time * 60 * 60

j = js.create_job(jd)

start = time.time()


j.run()
print j.id

karnak_query = kr.karnak_query(res, j.id)
print karnak_query

j.wait()
