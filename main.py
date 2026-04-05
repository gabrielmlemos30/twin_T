import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class TWIN-T_NOTCH:
    """Classe feita para lidar com o TWIN T"""
    def __init__(self, fc=60, fs=64560, n=2056, k=0.9):

        self.K = k
        self.fc = fc
        self.w0 = self.fc * 2 * np.pi
        self.rc = 0
        self.R = 1000 #Valor inicial
        self.R3 = 0
        self.R4 = 0
        self.R5 = 100000
        self.C = 0
        self.C3 = 0
        self.Q = 0 # Fator de qualidade
        self.fs = fs
        self.N = n
        self.t = np.linspace(0, self.N/self.fs, self.N, endpoint=False)
        #Função de transferencia
        
        self.numerador = 0
        self.denominador =  0
        self.numeradorTF = []
        self.denominadorTF = []
        self.zero = 0
        self.pole = 0
        self.signalFilter = []
        self.signal = np.zeros_like(self.t)
        "Inicializa o sinal"
        for i, harmonic in enumerate([1, 3, 5, 7, 11]):
            f = 60
            # self.signal += 1/(i+1)*(np.cos(2 * np.pi * harmonic * f * self.t) + np.sin(2 * np.pi * harmonic * 2 * f * self.t)  )
            self.signal += 1/(i+1)*(np.cos(2 * np.pi * harmonic * f * self.t))
        "resposta em frequencia"

        self.w = []
        self.mag = []
        self.phase = []
               
          

        "INICIALIZA CÁLCULOS"
        self.run()

    def calculaHS(self):
        self.numerador = [1, 0, self.w0**2]
        self.denominador = [1, 4*self.w0*(1-self.K), self.w0**2]
        x = 0
        "Calcula polos e zeros"
        self.zero, self.pole, x= signal.tf2zpk(self.numerador, self.denominador)
        
        "Volta para a função de transferencia"
        self.numeradorTF, self.denominadorTF = signal.zpk2tf(self.zero, self.pole, self.K)


        "Aplica a transformada bilinear para ir para o dominio Z"

        self.numeradorTF, self.denominadorTF = signal.bilinear(self.numeradorTF, self.denominadorTF, fs=self.fs)

        return signal.lfilter(self.numeradorTF,self.denominadorTF, self.signal)

    def calculaComponentes(self):
        self.rc = 1/self.w0
        self.C = 10**9 * self.rc / self.R
        self.C3 = self.C * 2
        self.k = 0.99 if self.K >= 1 else self.K
        self.Q = 1/(4*(1-self.K))
        self.R3 = 2*self.R
        self.R4 = self.K*self.R5/(1-self.K)

    def emiteRelatorio(self):
        print("================================================================")
        print("======================FILTRO TWIN T NOTCH(======================")
        print("================================================================")
        print("R1=R2=",self.R,"ohm")
        print("R3=",self.R3, "ohm")
        print("C1 = C2=",f"{self.C:6f}","nF")
        print("C3",f"{self.C3:.6f}","nF")
        print("R4=",f"{self.R4:.1f}","ohm")
        print("R5=",self.R5,"ohm")
        print("frequência(rad/s)",self.w0, "rad/s")
        print("Seletividade k", self.K)
        print("fator de qualidade",self.Q)
        print("polos",self.pole)
        print("zeros",self.zero)
        print("ganho",self.K)
    
    def bode(self):
        sys = signal.lti(self.numerador, self.denominador)
        # Calculando a resposta em frequência
        self.w, self.mag, self.phase = signal.bode(sys)

    def plot(self):
        # Lógica de plotagem viria aqui
        # --- Visualização Opcional ---
        fig1,ax =  plt.subplots(2, 1, sharex=True, figsize=(10,8))
        ax[0].plot(self.signal, label="Sinal sem filtro", color="green")
        ax[1].plot(self.signalFilter,label="Sinal com filtro", color="blue")
        ax[0].set_title("Entrada do filtro")
        ax[1].set_title("Saída do filtro")
        ax[1].legend()
        ax[0].legend()
        plt.tight_layout()


        "DIAGRAMA DE BODE "
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Magnitude
        ax1.semilogx(self.w, self.mag, color='cyan', label='Magnitude (dB)')
        ax1.set_title("Diagrama de Bode - Filtro Twin-T")
        ax1.set_ylabel("Ganho (dB)")
        ax1.grid(True, which="both", ls="-", alpha=0.5)
        ax1.legend()

        # Fase
        ax2.semilogx(self.w, self.phase, color='magenta', label='Fase (graus)')
        ax2.set_ylabel("Fase (deg)")
        ax2.set_xlabel("Frequência (rad/s)")
        ax2.grid(True, which="both", ls="-", alpha=0.5)
        ax2.legend()

        plt.show()

    def run(self):
        # Lógica de execução viria aqui
        self.calculaComponentes()
        self.signalFilter = self.calculaHS()
        self.bode()
        self.emiteRelatorio()
        self.plot()

if __name__ == "__main__":
    fs = 3200
    n = 2056
    fc = 120
    k = 0.9
    processo = main(fc=fc, fs=fs, n=n, k=k)
    