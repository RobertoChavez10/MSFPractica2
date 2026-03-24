"""
Práctica 2: Sistema cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Chávez González Roberto
Número de control: 22210884
Correo institucional: l22210884@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerias en consola
#!pip install control
#!pip install slycot

import control as ctrl
 
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

u = np.array(pd.read_excel('signal.xlsx',header=None))
x0,t0,tend,dt,w,h = 0,0,15,1E-3,10,5
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u = np.reshape(signal.resample(u,len(t)),-1)


def cardio(Z,C,R,L):

    num = [L*R,R*Z]
    den = [C*L*R*Z,L*R+L*Z,R*Z]
    sys = ctrl.tf(num,den)
    return sys

#Funcion de transferencia: Normotenso
Z,C,R,L = 0.033,1.5,0.95,0.01
sysnormo = cardio(Z,C,R,L)
print(f'Funcion de transferencia del normotenso (control): {sysnormo}')


#Funcion de trnasferencia: Hipotenso
Z,C,R,L = 0.02,0.25,0.6,0.005
syshipo = cardio(Z,C,R,L)
print(f'Funcion de transferencia del hipotenso (caso 1): {syshipo}')


#Funcion de trnasferencia: Hipertenso
Z,C,R,L = 0.05,2.5,1.4,0.02
syshiper = cardio(Z,C,R,L)
print(f'Funcion de transferencia del hipertenso (caso 2): {syshiper}')




#Respuestas en lazo abierto
_,Pp0 = ctrl.forced_response(sysnormo,t,u,x0)
_,Pp1 = ctrl.forced_response(syshipo,t,u,x0)
_,Pp2 = ctrl.forced_response(syshiper,t,u,x0)

fg1 = plt.figure()
plt.plot(t,Pp0,'-',linewidth=1, color= np.array([11,45,114])/255, label = 'Pp(t): Normotenso')
plt.plot(t,Pp1,'-',linewidth=1, color= np.array([10,196,224])/255, label = 'Pp(t): Hipotenso')
plt.plot(t,Pp2,'-',linewidth=1, color=np.array([255,155,81])/255, label = 'Pp(t): Hipertenso')
plt.grid(False)
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))

plt.xlabel('Pp(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('Sistema cardiovascular Lazo abierto python.png', dpi=600, bbox_inches='tight')


#Controlador PID
def controlador(kP,kI,kD,sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    Ce = kD/Rr

    numPID = [Re*Rr*Ce*Cr,(Re*Ce + Rr*Cr),1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    X = ctrl.series(PID,sys)
    sysPID = ctrl.feedback(X,1,sign= -1)
    return sysPID

hipoPID = controlador(0.0327153147045264,195.032869191362,0,syshipo)
print (f'Funcion de transferencia del hipotenso en lazo cerrado: {hipoPID}')

hiperPID = controlador(0.0327153147045264,195.032869191362,0,syshiper)
print (f'Funcion de transferencia del hipertenso en lazo cerrado: {hipoPID}')

#Respuestas del sistema de control en lazo cerrado
_,Pp3 = ctrl.forced_response(hipoPID,t,Pp0,x0)
_,Pp4 = ctrl.forced_response(hiperPID,t,Pp0,x0)




fg2 = plt.figure()
plt.plot(t,Pp0,'-',linewidth=1, color= np.array([11,45,114])/255, label = 'Pp(t): Normotenso')
plt.plot(t,Pp3,':',linewidth=3, color= np.array([10,196,224])/255, label = 'Pp(t): Hipotenso PID')
plt.plot(t,Pp2,'-',linewidth=1, color= np.array([255,155,81])/255, label = 'Pp(t): Hipertenso')

plt.grid(False)
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('Pp(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('Sistema cardiovascular python hipo PI.png', dpi=600, bbox_inches='tight')

    
# sola figura con dos subgráficas (fg1 arriba, fg2 abajo)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(w, h*2))

# Primera gráfica (fg1 arriba) - Lazo abierto
ax1.plot(t,Pp0,'-',linewidth=1, color= np.array([11,45,114])/255, label = 'Pp(t): Normotenso')
ax1.plot(t,Pp1,'-',linewidth=1, color= np.array([10,196,224])/255, label = 'Pp(t): Hipotenso PID')
ax1.plot(t,Pp2,'-',linewidth=1, color=np.array([255,155,81])/255, label = 'Pp(t): Hipertenso')
ax1.grid(False)
ax1.set_xlim(0,15)
ax1.set_xticks(np.arange(0,16,1))
ax1.set_ylim(-0.6,1.4)
ax1.set_yticks(np.arange(-0.6,1.6,0.2))
ax1.set_ylabel('Pp(t) [V]')
ax1.set_title('Normotenso vs Hipotenso') # Lazo abierto 
ax1.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)

# Segunda gráfica (fg2 abajo) - Control PID
ax2.plot(t,Pp0,'-',linewidth=1, color= np.array([11,45,114])/255, label = 'Pp(t): Normotenso')
ax2.plot(t,Pp3,':',linewidth=3, color= np.array([10,196,224])/255, label = 'Pp(t): Hipertenso PID')
ax2.plot(t,Pp2,'-',linewidth=1, color= np.array([255,155,81])/255, label = 'Pp(t): Hipertenso')
ax2.grid(False)
ax2.set_xlim(0,15)
ax2.set_xticks(np.arange(0,16,1))
ax2.set_ylim(-0.6,1.4)
ax2.set_yticks(np.arange(-0.6,1.6,0.2))
ax2.set_xlabel('t [s]')
ax2.set_ylabel('Pp(t) [V]')
ax2.set_title('Normotenso vs Hipotenso') # Control PID
ax2.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)

# Ajustar el espaciado
plt.tight_layout()

# Guardar la figura combinada
plt.savefig('Sistema_cardiovascular_combinado.png', dpi=600, bbox_inches='tight')
plt.show()












