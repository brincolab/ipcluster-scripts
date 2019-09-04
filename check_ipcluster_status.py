import ipyparallel as ipp

try:
	rc = ipp.Client(profile="brincolab-cluster")
	dview = rc[:]
	print("Available kernels: {}".format(len(rc.ids)))
except:
	print("Can't communicate with cluster")
