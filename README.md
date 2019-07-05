# brincolab-ipcluster-scripts

## Contenidos
En este repositorio hay 3 script de python que nos permiten realizar distintas acciones (auto explicativas):

1. `check_ipcluster_status.py`: Nos permite obtener el estado del cluster de ipython. En el caso de que este andando correctamente, mostrara la cantidad de kernels del cluster. En el caso contrario aparecera el mensaje `Can't communicate with cluster`.

2. `start_script.py`: Inicializa el controlador `ipcontroller` y los motores `ipengine` tanto en el servidor`brincolab1` y `brincolab2`. Solo utilizar en el caso de que `check_ipcluster_status.py` no puede comunicarse con el servidor.

3. `shutdown.py`: Apaga el controlador y los motores asociados al cluster

-------
## Instrucciones
#### Desde brincolab1

1. Activar el entorno virtual `ipynode` (contiene las librerias necesarias para ejecutar los archivos)
```
source activate ipynode
```

2. Copiar los archivos de configuración para acceder al cluster, al directorio `~/.ipython`
```
cp -r /opt/ipython_profile/profile_brincolab-cluster ~/.ipython/
```

3. Revisar que el cluster esta andando
```
python check_ipcluster_status.py
```

4. Si el cluster no esta andando, iniciarlo
```
python start_script.py
```

5. Si no necesita seguir utilizando el cluster, apaguelo.
```
python shutdown.py
```

#### Desde brincolab2 y otros pcs que no sean brincolab1

TODO: llenar esta info. pero principalmente tener:
1. ipython instalado
2. ipyparallel instalado
3. spur instalado
```
pip install spur ipython ipyparallel jupyter notebook
```
4. Descargar y copiar los archivos de configuracion para acceder al cluster, a la maquina de origen (ver paso 2 desde brincolab1)
5. editar archivo de hosts añadiendo la direccion ip de brincolab1 a este archivo

Ojo que hay que estar dentro de la red interna de la UV para poder utilizar los servidores.

