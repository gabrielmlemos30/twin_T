import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class main:
    """Classe feita para lidar com o TWIN T"""
    def __init__(self, fc):

        self.K = float(input("Valor de k > 1 para seletividade maxima"))
        self.fc = fc
        self.w0 = self.fc * 2 * np.pi
        self.rc = 0
        self.R = 10000 #Valor inicial
        self.R3 = 0
        self.R4 = 0
        self.R5 = 100000
        self.C = 0
        self.C3 = 0
        self.Q = 0 # Fator de qualidade

        #Função de transferencia
        
        self.numerador = 0
        self.denominador =  0
        self.zero = 0
        self.pole = 0


        "INICIALIZA CÁLCULOS"
        self.run()


    def calculaHS(self):
        self.numerador = [1, 0, self.w0**2]
        self.denominador = [1, 4*self.w0*(1-self.K), self.w0**2]
        self.zero, self.pole, self.K= signal.tf2zpk(self.numerador, self.denominador)

    def calculaComponentes(self):
        self.rc = 1/(self.w0**2)
        self.C = self.rc / self.R * 10**6
        self.C3 = self.C * 2 * 10**6
        self.Q = 1/4 * 1/(1-self.K)

    def emiteRelatorio(self):
        print("================================================================")
        print("======================FILTRO TWIN T NOTCH(======================")
        print("================================================================")
        print("R1=R2=",self.R,"ohm")
        print("R3=",self.R3, "ohm")
        print("C1 = C2=",self.C,"uF")
        print("C3",self.C3,"uF")
        print("R4=",self.R4,"ohm")
        print("R5=",self.R5,"ohm")
        print("frequência(rad/s)",self.w0, "rad/s")
        print("Seletividade k", self.K)
        print("fator de qualidade",self.Q)
        print("polos",self.pole)
        print("zeros",self.zero)
        print("ganho",self.K)

    def plot(self):
        # Lógica de plotagem viria aqui
        pass

    def run(self):
        # Lógica de execução viria aqui
        self.calculaComponentes()
        self.calculaHS()
        self.emiteRelatorio()
        self.plot()

if __name__ == "__main__":
    # 1. Primeiro pegamos o dado
    valor_fc = int(input("Qual a frequência de corte desejada? (Hz): "))
    
    processo = main(valor_fc)
    