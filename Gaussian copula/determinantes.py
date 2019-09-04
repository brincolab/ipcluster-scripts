import numpy as np
import itertools
from math import factorial, ceil
from itertools import islice, chain
from tqdm import tqdm
#import determinantes

def det2(N):
        dets = numpy.zeros(N,dtype=numpy.float32)
        if len(index_mat) > 0:
            idx_mat = index_mat[0]
        else:    
            return {'dets':[],'matrices':[],'idx':[]}
        matrices = []
        idxs = []
        i=0
        for ind in idx_mat:
            idx = list(ind)
            matrix = covmat[idx][:,idx]
            dets[i] = numpy.linalg.det(matrix)
            matrices.append(matrix)
            idxs.append(idx)
            i += 1
        return {'dets':dets,'idx':idxs}

def specific_index(matrix, shape, indexes_file, indexes_name, method = 1):
    import scipy.io as sio
    
    
    workspace = sio.loadmat(indexes_file)
    shape = int(shape)
    covmat = np.array(matrix)
    covmat = np.reshape(covmat,(shape,shape))
    
    det_method = """def det():
        N = len(indexes_list)
        dets = numpy.zeros(N,dtype=numpy.float32)
        ent = numpy.zeros(N,dtype=numpy.float32)
        dets[:] = 0 #numpy.nan 
        ent[:] = 0 #numpy.nan
        
        
        if len(indexes_list) > 0:
            idx_mat = indexes_list
        else:    
            return {'dets':[],'ents':[],'idx':[]}
        matrices = []
        idxs = []
        i=0
        for ind in idx_mat:
            idx = ind[0][0] - 1
            matrix = covmat[idx][:,idx]
            dets[i] = numpy.linalg.det(matrix)
            ent[i] = entropy(k,dets[i])
            matrices.append(matrix)
            idxs.append(ind)
            i += 1
        return {'dets':dets,'ents':ent,'idx':idxs}"""

    if method == 1:
        entropy_method = """def entropy(x,y):
        return 0.5*numpy.log((2*numpy.pi * numpy.exp(1))**(x)*y)
        """
    elif method == 2:
        entropy_method = """def entropy(x,y):
        return 0.5*numpy.log(numpy.abs((2*numpy.pi * numpy.exp(1))**(x)*y))
        """
    elif method == 3:
        entropy_method = """def entropy(x,y):
        return #0.5*numpy.log(numpy.abs((2*numpy.pi * numpy.exp(1))**(x)*y))
        """
    from ipyparallel import Client
    rc = Client(profile='brincolab-cluster')
    rc.purge_everything()  #Limpiar la sesion
    
    dview = rc[:] # use all engines
    #dview.use_pickle()
    print(len(dview))
    #dview.block = True #Modo block
    dview['covmat'] = covmat #Distribuimos la matriz de covarianza
    dview.execute(det_method)
    dview.execute(entropy_method)
    
    indexes_list = workspace[indexes_name]
    dview.scatter('indexes_list',indexes_list)
    dview.execute('res = det()', block=True)
    responses = dview.gather('res', block=True)
    
    dets = np.array([], dtype=np.float32)
    ents = np.array([], dtype=np.float32)
    idxs = []
    for el in responses:
        #print(el.keys())
        dets = np.append(dets,el['dets'])
        ents = np.append(ents,el['ents'])    
        for subel in el['idx']:
            idxs.append(subel)
            
    dets = dets[~np.isnan(dets)]
    ents = ents[~np.isnan(ents)]
    print(len(dets),len(ents),len(idxs))
    print()
    
    rc.purge_everything()  #Limpiar la sesion
    
    return (dets,ents,idxs)

    #ar = dview.apply_async(det)
    #ar.wait()
    #responses = ar.get()
    
    return 0

def get_all_determinants(matrix, shape, method = 1):
    
    det_method = """def det(N):
        dets = numpy.zeros(N,dtype=numpy.float32)
        ent = numpy.zeros(N,dtype=numpy.float32)
        dets[:] = -1 #numpy.nan 
        ent[:] = -1 #numpy.nan
        
        if len(index_mat) > 0:
            idx_mat = index_mat[0]
        else:    
            return {'dets':[],'ents':[],'idx':[]}
        matrices = []
        idxs = []
        i=0
        for ind in idx_mat:
            idx = list(ind)
            matrix = covmat[idx][:,idx]
            dets[i] = numpy.linalg.det(matrix)
            ent[i] = entropy(k,dets[i])
            matrices.append(matrix)
            idxs.append(ind)
            i += 1
        return {'dets':dets,'ents':ent,'idx':idxs}"""

    if method == 1:
        entropy_method = """def entropy(x,y):
        return 0.5*numpy.log((2*numpy.pi * numpy.exp(1))**(x)*y)
        """
    elif method == 2:
        entropy_method = """def entropy(x,y):
        return 0.5*numpy.log(numpy.abs((2*numpy.pi * numpy.exp(1))**(x)*y))
        """
    ## Funcion para calcular el determinante
    
    shape = int(shape)
    covmat = np.array(matrix)
    covmat = np.reshape(covmat,(shape,shape))
    
    N = covmat.shape[0] ## Cambiar lectura de matriz
    k = N-1
     #Aca corresponde ingresar la matriz de covarianzas ya calculada
    arr = list(range(0,N)) #Arreglo para generar las mascaras de las submatrices cuadradas

    from ipyparallel import Client
    rc = Client(profile='brincolab-cluster')
    rc.purge_everything()  #Limpiar la sesion
    
    dview = rc[:] # use all engines
    #dview.use_pickle()
    print(len(dview))
    #dview.block = True #Modo block
    dview['covmat'] = covmat #Distribuimos la matriz de covarianza
    dview['k'] = k # N-1
    dview.execute(det_method)
    dview.execute(entropy_method)
    

    iteraciones = {}
    det_calcular = {}
    indices_scatter = {}
    for i in range(2,N):
        iteraciones[i] = itertools.combinations(arr, i)
        iters = itertools.combinations(arr, i)
        n = int(factorial(N) / factorial(i) / factorial(N-i))
        n_per_process = ceil(int(n)/len(rc.ids) )
        print(i, n, n_per_process)
        det_calcular[i] = (n,n_per_process)
        indexes = []
        for j in range(0,n,n_per_process):
            sl = islice(iters, j , j + n_per_process )
            indexes.append(sl)
        indices_scatter[i] = indexes
    
    with dview.sync_imports():
        import numpy
        #import determinantes
    
    responses = {}
    for i in range(2,N):
        n_dets = det_calcular[i][0]
        n_scatters = det_calcular[i][1]
        print(n_scatters)
        dview.scatter('index_mat', indices_scatter[i], block=True)
        dview.execute('res = det({})'.format(n_scatters), block=True)
        responses[i] = dview.gather('res', block=True)
        
    dets = np.array([], dtype=np.float32)
    ents = np.array([], dtype=np.float32)
    idxs = []
    #print(idxs)
    for i in tqdm(range(2,N)):
        for el in responses[i]:
            #print(el.keys())
            if -1 in el['dets']:
                mask = np.array(el['dets']) == -1
                #print(mask)
                dets = np.append(dets,el['dets'][~mask])
                ents = np.append(ents,el['ents'][~mask])
            else:
                dets = np.append(dets,el['dets'])
                ents = np.append(ents,el['ents'])
            for subel in el['idx']:
                idxs.append(subel)
        #for j in responses[i]['dets']:
        #    print(j)
        
    dets = dets[~numpy.isnan(dets)]
    ents = ents[~numpy.isnan(ents)]
    
    
    print(len(dets),len(ents),len(idxs))
    mask = dets == -1
    print(len(dets[mask]))
    
    rc.purge_everything()  #Limpiar la sesion
    
    return (dets,ents,idxs)

if __name__ == "__main__":
    
    N_default = 20
    covmat = np.random.rand(N_default,N_default)
    covmat[[range(0,N_default)],[range(0,N_default)]] = N_default
    res = get_all_determinants(covmat,N_default)
    print(res[0][:45])
    print(res[1][:45])
    print(res[2][:45])
