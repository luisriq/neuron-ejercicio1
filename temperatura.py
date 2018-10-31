from matplotlib import pyplot
from neuron import h, gui
import numpy as np

#Constantes
#   Punto de corte para encontrar potencial de accion
puntoDeCorte = 0

axon = h.Section(name='axon')
axon.insert('hh')
axon.nseg = 100
axon.diam = 50
axon.L = 50000
axon.Ra = 15
# IClamp al inicio (0)
#   Delay = 50 para dar tiempo a inicializacion del resting potential
stim = h.IClamp(axon(0))
stim.delay = 50
stim.dur = 1
stim.amp = 2000

# Correr Simulacion
h.tstop = 100.0
values = [0.001,1]

# Leyenda grafico
legends = []

# Funciones calculo velocidad
#   Se calcula el tiempo en que se encuentra el potencial de ac
def calcularTiempo(voltage, time):
    #Se recorre el vector buscando pasar el 0
    for v, t in zip(voltage, time):
        #print(v)
        if(v >= puntoDeCorte):
            return t
    return None
#   Se encuentra la velocidad entre 2 vectores de voltaje
def calcularVelocidad(voltage, time, L):
    L = L/1000000
    t0 = calcularTiempo(voltage[0], time)
    t1 = calcularTiempo(voltage[1], time)
    #diferencia de t en segundos
    if(t0 == None or t1 == None or (t1-t0 == 0)):
        return None
    tf = (t1-t0)/1000
    return L/(tf)



def generarVelocidades(diametros, temperatura):
    velocidades = []
    h.celsius = temperatura
    time_v1 = h.Vector()
    for index, diam in enumerate(diametros):
        volt_v0 = h.Vector()
        volt_v1 = h.Vector()
        time_v = h.Vector()
        
        volt_v0.record(axon(values[0])._ref_v)
        volt_v1.record(axon(values[1])._ref_v)
        time_v.record(h._ref_t)
        if(index == 0):
            time_v1.record(h._ref_t)

        axon.diam = diam 
        h.run()
        #h.psection()
        velocidades.append(calcularVelocidad([volt_v0, volt_v1], time_v, axon.L))
    return velocidades, time_v1


#   Diametros entre 10 y 100
diametros = np.linspace(10, 100, 10)
diametros = np.linspace(10, 1000, 30)
velocidades = []
tiempos = []
celsius = np.linspace(0, 15, 10)

legend = []
ax = pyplot.figure(figsize=(8,4)) # Default figsize is (8,6)
for t in celsius:
    velocidades, tiempo = generarVelocidades(diametros,t)
    print(velocidades, diametros)
    pyplot.plot(diametros, velocidades)
    legend.append("{:.2f}ºC".format(t))

pyplot.legend(legend)
# Velocidad vs Diametro
pyplot.xlabel('diam (μm)')
pyplot.ylabel('vel (m/s)')

pyplot.show()
