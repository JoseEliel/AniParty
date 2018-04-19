import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
import pyaudio

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

CHUNK = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 22050
RECORD_SECONDS=0.1
p = pyaudio.PyAudio()


def data_gen(k):


    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    
    data = stream.read(CHUNK)
    FactorInt=np.fromstring(data, dtype=np.int16)
    Factor=[float(i)/2000 for i in FactorInt]
    #print Factor[1], Factor[511]
    Kmod=2*np.cos(k*np.pi/100) + 2*np.sin(k*np.pi/100)**2 + Factor[500]*np.cos(k*np.pi/100)**2 + Factor[0]*np.sin(k*np.pi/100)**2
    
    rx =[(1+Factor[2])*np.sin(np.pi*(i+Kmod)*Kmod/100) for i in range(200)] 
    ry =[(1+Factor[200])*np.sin(np.pi*(i+Kmod)*Kmod/100)  for i in range(200)] 
    rz =[(1+Factor[450])*np.sin(np.pi*(i+Kmod)*Kmod/100)  for i in range(200)] 
    
    # #r=5
    u = np.linspace(0, 2.*np.pi, 200)
    v = np.linspace(0, np.pi, 200)
    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.cos(v)
    

    ax.clear()
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1,1)
    ax.set_zlim3d(-1,1)
    #HideTic
    ax.set_xticks([])                               
    ax.set_yticks([])                               
    ax.set_zticks([])
    # Get rid of the panes                          
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 

    # Get rid of the spines                         
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    ax.plot_wireframe(x,y,z,rstride=5, cstride=5, color='black')


ani=animation.FuncAnimation(fig, data_gen ,blit=False,interval=1)


plt.show()
