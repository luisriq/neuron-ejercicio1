# -*- coding: utf-8 -*-
from neuron import h, gui
import numpy as np
from matplotlib import pyplot

#Constantes
#   Punto de corte para encontrar potencial de accion
puntoDeCorte = 0

axon = h.Section(name='axon')
axon.insert('hh')
axon.nseg = 100
axon.diam = 50
axon.L = 80000
axon.Ra = 15
# IClamp al inicio (0)
#   Delay = 50 para dar tiempo a inicializacion del resting potential
stim = h.IClamp(axon(0))
stim.delay = 50
stim.dur = 1
stim.amp = 5000

# Primer grafico
def graficar(x, y, color):
    pyplot.plot(x, y, color=color)
    #pyplot.ylim(-70, 70)
    pyplot.xlim(45, 70)
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

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


# Velocidades para cada diametro
velocidades = []
#   Diametros entre 10 y 100
diametros = np.linspace(10, 100, 10)
diametros = np.linspace(10, 1000, 100)
#cmap = pyplot.get_cmap('tab20')


for index, diam in enumerate(diametros):
      
    volt_v0 = h.Vector()
    volt_v1 = h.Vector()
    time_v = h.Vector()
    
    volt_v0.record(axon(values[0])._ref_v)
    volt_v1.record(axon(values[1])._ref_v)
    time_v.record(h._ref_t)

    axon.diam = diam 
    h.run()
    #h.psection()
    legends.append('$axon({:.2f}) | diam = {}$'.format(values[0], diam))
    legends.append('$axon({:.2f}) | diam = {}$'.format(values[1], diam))
    #color = cmap(float(index)/len(diametros))
    velocidades.append(calcularVelocidad([volt_v0, volt_v1], time_v, axon.L))

# Velocidad vs Diametro
#print(velocidades)

def graficarDiametro(x, y):
    pyplot.plot(x, y)
    pyplot.xlabel(u'diam (µm)')
    pyplot.ylabel(u'vel (m/s)')
graficarDiametro(diametros, velocidades)

pyplot.show()