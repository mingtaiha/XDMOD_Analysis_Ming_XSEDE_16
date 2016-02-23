#!/usr/bin/env python


import radical.pilot as rp


if __name__ == '__main__':


	# List of the number of cores
	list_cores = [8]

	# List of the runtime (in minutes)
	list_runtime = [15]

	try:

		for i in range(len(list_cores)):

			print "Making Session"
			session = rp.Session()
			print "Making Pilot Manager"
			pmgr = rp.PilotManager(session=session)

			print "Instantiating Pilot Description List"
			pdescs = list()

			print "Defining Pilot Description"
			pd_init = {
				'resource' 			: 'xsede.gordon',
				'cores'				: list_cores[i],
				'runtime'			: list_runtime[i],
				'project'			: 'TG-MCB090174',
				'queue'				: 'normal',
			}

			print "Submitting CU Descriptions to Pilot Description List"
			pdescs.append(rp.ComputePilotDescription(pd_init))

			print "Submitting Pilot Description List"
			pilots = pmgr.submit_pilots(pdescs)

			print "Defining Unit Manager"
			umgr = rp.UnitManager(session=session)

			print "Adding Pilots to Umgr"
			umgr.add_pilots(pilots)

		
			print "Instantiating CU Description list "
			cuds = list()

			print "Defining CU Descriptions"
			cud = rp.ComputeUnitDescription()
			cud.pre_exec		= ['exit']
			cud.executable 		= '/bin/sleep'
			cud.arguments		= ['90']
			cuds.append(cud)

			print "Submitting the Units"
			umgr.submit_units(cuds)

			print "Waiting for all the Units to finish"
			umgr.wait_units()


			print "Session %d is done now! Killing Session" % i
			session.close()

	except Exception as e:
		print "Caught Exception %s\n" % e

	except(KeyboardInterrupt, System) as e:
		print "Caught A Keyboard Error"
