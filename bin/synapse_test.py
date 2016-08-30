import os
import radical.pilot as rp
import radical.utils as ru

TIME = 15
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
    'cleanup'       : 'False'
    #'queue'         : 'normal'
}

session = rp.Session()

try:

    pmgr = rp.PilotManager(session)

    pdescs = list()

    #pdescs.append(rp.ComputePilotDescription(pdesc_stampede))
    #pdescs.append(rp.ComputePilotDescription(pdesc_comet_compute))
    #pdescs.append(rp.ComputePilotDescription(pdesc_comet_shared))
    #pdescs.append(rp.ComputePilotDescription(pdesc_gordon))
    #pdescs.append(rp.ComputePilotDescription(pdesc_supermic))
    #pdescs.append(rp.ComputePilotDescription(pdesc_bw))
    pdescs.append(rp.ComputePilotDescription(pdesc_osg))

    pilots = pmgr.submit_pilots(pdescs)


    cuds = list()
    for i in range(1):
        cud = rp.ComputeUnitDescription()
        #cud.pre_exec = ['pip install radical.synapse']
        cud.pre_exec = [ 'echo $PWD'
                         #'curl -O https://pypi.python.org/packages/5c/79/5dae7494b9f5ed061cff9a8ab8d6e1f02db352f3facf907d9eb614fb80e9/virtualenv-15.0.2.tar.gz#md5=0ed59863994daf1292827ffdbba80a63'
                         #'mv $HOME/virtualenv-15.0.2.tar.gz#md5=0ed59863994daf1292827ffdbba80a63 $HOME/virtualenv-15.0.2.tar.gz',
                         #'tar xvfz virtualenv-15.0.2.tar.gz',
                         #'cd virtualenv-15.0.2',
                         #'python virtualenv.py ve.timings_osg',
                         #'source $PWD/virtualenv-15.0.2/ve.timings_osg/bin/activate'
                         #'pip install -e git://github.com:radical-cybertools/radical.synapse.git@feature/named_storage'
                         ]
        #cud.input_staging = ['get_timings_84.sh', '84.json']
        #cud.executable = './get_timings_84.sh'
        #cud.executable = '/bin/date'
        cud.executable = '/bin/date'
        cuds.append(cud)

    umgr = rp.UnitManager(session=session, scheduler='round_robin')
    umgr.add_pilots(pilots)
    units = umgr.submit_units(cuds)
    umgr.wait_units()

except Exception as e:
    print e
finally:
    session.close(cleanup=False)

os.system('radicalpilot-close-session -m export -s %s' %session.uid)
