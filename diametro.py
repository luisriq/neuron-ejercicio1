from matplotlib import pyplot
from neuron import h, gui
import numpy as np

#Constantes
#   Punto de corte para encontrar potencial de accion
puntoDeCorte = -60

axon = h.Section(name='axon')
axon.insert('hh')
axon.nseg = 100
axon.diam = 50
axon.L = 10000

# IClamp al inicio (0)
#   Delay = 50 para dar tiempo a inicializacion del resting potential
stim = h.IClamp(axon(0))
stim.delay = 50
stim.dur = 1
stim.amp = 2000

# Primer grafico
pyplot.subplot(2, 1, 1)
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
    
    t0 = calcularTiempo(voltage[0], time)
    t1 = calcularTiempo(voltage[1], time)
    if(t0 == None or t1 == None or (t1-t0 == 0)):
        return None
    return L/(t1-t0)


# Velocidades para cada diametro
velocidades = []
#   Diametros entre 10 y 100
diametros = np.linspace(10, 100, 10)
diametros = np.linspace(10, 1000, 100)
cmap = pyplot.get_cmap('tab20')


for index, diam in enumerate(diametros):
      
    volt_v0 = h.Vector()
    volt_v1 = h.Vector()
    time_v = h.Vector()
    
    volt_v0.record(axon(values[0])._ref_v)
    volt_v1.record(axon(values[1])._ref_v)
    time_v.record(h._ref_t)

    axon.diam = diam 
    h.run()
    h.psection()
    legends.append('$axon({:.2f}) | diam = {}$'.format(values[0], diam))
    legends.append('$axon({:.2f}) | diam = {}$'.format(values[1], diam))
    color = cmap(float(index)/len(diametros))
    #graficar(time_v, volt_v0, color)
    #graficar(time_v, volt_v1, color)
    velocidades.append(calcularVelocidad([volt_v0, volt_v1], time_v, axon.L))

pyplot.legend(legends, ncol=2)


#pyplot.show()

# Velocidad vs Diametro
print(velocidades)

pyplot.subplot(2, 1, 2)

def graficarDiametro(x, y):
    pyplot.plot(x, y)
    pyplot.xlabel('diam (μm)')
    pyplot.ylabel('vel (μm/ms)')
graficarDiametro(diametros, velocidades)#[v/1000 for v in velocidades])

pyplot.show()