import os
import radical.pilot as rp

TIME = 10
pdesc_stampede = {
    'resource'      : 'xsede.stampede',
    'cores'         : 16,
    'runtime'       : TIME,
    'project'       : "TG-MCB090174",
    'queue'         : 'normal'
}

pdesc_comet_compute = {
    'resource'      : 'xsede.comet',
    'cores'         : 24,
    'runtime'       : TIME,
    'project'       : 'unc100',
    'queue'         : 'compute'
}

pdesc_comet_shared = {
    'resource'      : 'xsede.comet',
    'cores'         : 1,
    'runtime'       : TIME,
    'project'       : 'unc100',
    'queue'         : 'shared'
}

pdesc_gordon = {
    'resource'      : 'xsede.gordon',
    'cores'         : 16,
    'runtime'       : TIME,
    'project'       : "TG-MCB090174",
    'queue'         : 'normal'
}

pdesc_supermic = {
    'resource'      : 'xsede.supermic',
    'cores'         : 20,
    'runtime'       : TIME,
    'project'       : 'TG-MCB090174',
    'queue'         : 'workq'
}

pdesc_bw = {
    'resource'      : 'ncsa.bw',
    'cores'         : 32,
    'runtime'       : TIME,
    'project'       : 'gkd',
    'queue'         : 'normal'
}

pdesc_osg = {
    'resource'      : 'osg.xsede-virt-clust',
    'cores'         : 1,
    'runtime'       : TIME,
    'project'       : 'TG-CCR140028',
    'queue'         : 'normal'
}

try:
    session = rp.Session()

    pmgr = rp.PilotManager(session)

    pdescs = list()

    #pdescs.append(rp.ComputePilotDescription(pdesc_stampede))
    #pdescs.append(rp.ComputePilotDescription(pdesc_comet_compute))
    #pdescs.append(rp.ComputePilotDescription(pdesc_comet_shared))
    pdescs.append(rp.ComputePilotDescription(pdesc_gordon))
    #pdescs.append(rp.ComputePilotDescription(pdesc_supermic))
    #pdescs.append(rp.ComputePilotDescription(pdesc_bw))
    #pdescs.append(rp.ComputePilotDescription(pdesc_osg))

    pilots = pmgr.submit_pilots(pdescs)


    cuds = list()
    for i in range(1):
        cud = rp.ComputeUnitDescription()
        #cud.pre_exec = ['pip install radical.synapse']
        cud.pre_exec = [ 'source ~/bin/ve.timings/bin/activate']
        cud.input_staging = ['get_timings_84.sh', '84.json']
        cud.executable = './get_timings_84.sh'
        cuds.append(cud)

    umgr = rp.UnitManager(session=session, scheduler=rp.SCHED_ROUND_ROBIN)
    umgr.add_pilots(pilots)
    units = umgr.submit_units(cuds)
    umgr.wait_units()


finally:
    os.system('radicalpilot-close-session -m export -s %s' %session.uid)
    session.close()
