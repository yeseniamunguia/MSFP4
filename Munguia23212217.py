"""
Práctica 4: Sistema endocrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Yesenia Isamar Munguia Silva
Número de control: 23212217
Correo institucional: l23212217@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx


"""
import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3, 12, 7
N = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, N)


def sistema(R1, R2, L, C):
    num = [L, R2]
    den = [R1 * L * C, R1 * R2 * C + L, R1 + R2]
    sys = ctrl.tf(num, den)
    polos = np.roots(den)
    return sys, polos


R1, R2, L, C = 1E3, 100E3, 100E-3, 1E-6
syscontrol, polos = sistema(R1, R2, L, C)
print(f'Funcion de transferencia del control: {syscontrol}')
print(f'Polos del sistema: {polos}\n')


R1, R2, L, C = 1E3, 1E3, 100E-3, 1000E-6
syscaso, polos = sistema(R1, R2, L, C)
print(f'Funcion de transferencia del caso: {syscaso}')
print(f'Polos del sistema: {polos}\n')


def controlador(kP, kI, kD, Nf, sys):
    numPID = [kP + kD * Nf, kP * Nf + kI, kI * Nf]
    denPID = [1, Nf, 0]
    PIDF = ctrl.tf(numPID, denPID)
    sysPID = ctrl.feedback(ctrl.series(PIDF, sys), 1, sign=-1)
    return sysPID


casoPID = controlador(1332.4962, 328815.2294, 0.17972,
                     5093.3297, syscaso)
print(f'Funcion de transferencia del caso en lazo cerrado: {casoPID}')


F = np.zeros(N)
F[t >= 1] = 1
_, Fsx = ctrl.forced_response(syscontrol, t, F, x0)
_, Fsy = ctrl.forced_response(syscaso, t, F, x0)
_, PID = ctrl.forced_response(casoPID, t, Fsx, x0)
CE = Fsy.copy()
EID = Fsy.copy()


clr1 = np.array([149, 100, 221]) / 255
clr2 = np.array([255, 190, 145]) / 255
clr3 = np.array([118, 196, 87]) / 255
clr4 = np.array([100, 150, 200]) / 255
clr5 = np.array([97, 45, 83]) / 255
clr6 = np.array([44, 87, 69]) / 255


plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

fg1 = plt.figure(1, figsize=(w, h))
plt.plot(t, F, '-', linewidth=1.5, color=clr1,
         label=r'$V_e(t)$')
plt.plot(t, Fsx, '-', linewidth=1.5, color=clr2,
         label=r'$V_s(t)$: Control FT')
plt.plot(t, Fsy, '--', linewidth=1.5, color=clr3,
         label=r'$V_s(t)$: Caso FT')
plt.plot(t, PID, '--', linewidth=1.5, color=clr4,
         label='PID(t): Tratamiento')
plt.plot(t, CE, '-.', linewidth=1.5, color=clr5,
         label=r'$V_s(t)$: Caso CE')
plt.plot(t, EID, ':', linewidth=1.5, color=clr6,
         label=r'$V_s(t)$: Caso EID')

plt.grid(False)
plt.xlim(0, 10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.1, 1.2)
plt.yticks(np.round(np.arange(-0.1, 1.21, 0.1), 1))

plt.xlabel('t [s]')
plt.ylabel(r'$V_s(t)$ [V]')

plt.legend(bbox_to_anchor=(0.5, 1.12),
           loc='center', ncol=3, frameon=False)

fg1.savefig('Endocrino_python.pdf', bbox_inches='tight')
plt.show()