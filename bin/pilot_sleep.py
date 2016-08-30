import radical.pilot as rp
from math import ceil, floor
from random import seed, random, randint
import json
import sys
import os



r_dict = {
    'xsede.comet'       : 'comet',
    'xsede.gordon'      : 'gordon',
    'xsede.stampede'    : 'stampede',
    'xsede.supermic'    : 'supermic',
    'ncsa.bw'           : 'bluewaters'
}


def queue_pick(q_div):

    q_idx = 0

    if q_div == [-1]:
        return q_idx
    else:
        seed()
        choice = random() * 100
        for i in range(len(q_div)):
            if choice >= q_div[i]:
                q_idx += 1

        print q_div, choice, q_idx
        return q_idx


def jobs_pick(j_dist):

    seed()
    choice = random() * j_dist[-1]
    j_idx = 0

    for i in range(len(j_dist)):
        if choice >= j_dist[i]:
            j_idx += 1

    print choice, j_dist, j_idx
    return j_idx


def cores_pick(c_list, j_idx):

    seed()
    cores = randint(c_list[j_idx], c_list[j_idx + 1] - 1)
    return cores

def job_define(q_div, c_list, e_list, j_dist, n_sub, q_list):

    q_idx = queue_pick(q_div)
    queue = q_list[q_idx]

    j_idx = jobs_pick(j_dist[q_idx])
    print j_idx
    exec_time = exec_time_list[q_idx][j_idx] * 60.0

    if n_sub[q_idx] == 1:
        cores = c_list[q_idx][j_idx]
    else:
        cores = cores_pick(c_list[q_idx], j_idx)
    
    print queue, exec_time, cores
    return queue, exec_time, cores

def read_config(filename):
    with open(filename) as j_file:
        
        config = json.load(j_file)

        resource = config['resource']
        queue_div = config['queue_div']
        project = config['project']
        setup = config['setup']

        cores_list = list()
        jobs_dist = list()
        exec_time_list = list()
        node_sub = list()
        queue_list = list()

        for i in range(len(setup)):
            cores_list.append(setup[i]['cores'])
            exec_time_list.append(setup[i]['exec_time'])
            jobs_dist.append(setup[i]['jobs_dist'])
            node_sub.append(setup[i]['node_sub'])
            queue_list.append(setup[i]['queue'])

        print resource, project, queue_div, cores_list, exec_time_list, jobs_dist, node_sub, queue_list
        return resource, project, queue_div, cores_list, exec_time_list, jobs_dist, node_sub, queue_list



if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print "Usage python pilot_sleep.py <config_file>"
        sys.exit()

    resource, project, queue_div, cores_list, exec_time_list, jobs_dist, node_sub, queue_list = read_config(sys.argv[1])
    
    while 1:
        queue, exec_time, cores = job_define(queue_div, cores_list, exec_time_list, jobs_dist, node_sub, queue_list)

        session = rp.Session()
        sid = session.uid

        if (resource == 'xsede.comet') & (queue == 'shared'):
            cfg = session.get_resource_config(resource)
            new_cfg = rp.ResourceConfig(resource, cfg)
            new_cfg.cores_per_node = 1
            session.add_resource_config(new_cfg)

        try:
        
            pmgr = rp.PilotManager(session=session)

            pd_init = {
                'resource'      : resource,
                'cores'         : cores,
                'runtime'       : ceil(exec_time),
                'project'       : project,
                'queue'         : queue
            }

            pdesc = rp.ComputePilotDescription(pd_init)
            pilot = pmgr.submit_pilots(pdesc)

            umgr = rp.UnitManager(session=session)
            umgr.add_pilots(pilot)

            cuds = list()
            cud = rp.ComputeUnitDescription()
            cud.pre_exec = ['pip install radical.synapse']
            cud.executable = '/bin/sleep'
            cud.arguments = [str(floor(exec_time * 60.0))]
            cuds.append(cud)

            umgr.submit_units(cuds)

            umgr.wait_units()

        except Exception as e:
            print "Caught Exception"
            raise

        except (KeyboardInterrupt, SystemExit) as e:
            print "Exiting"

        finally:
            os.system("radicalpilot-close-session -m export -s %s" % sid)
            os.system("mv %s.json %s" % (sid, r_dict[resource] + "_" + queue))
            session.close()

