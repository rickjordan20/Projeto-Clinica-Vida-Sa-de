import tkinter as tk # Janela principal e loop de eventos
from tkinter import ttk # Widgets com estilo moderno e nativo

#Importa as telas que você quer testar
from app.ui.tela_pacientes import TelaPacientes
from app.ui.tela_medicos import TelaMedicos
#from app.ui.tela_consultas import TelaConsultas

root = tk.Tk() # Cria um Frame(Janela)
root.title("Clínica Vida e Saúde - Tela de Teste") #Define o Título
root.geometry("820x520") # Define o Tamanho da Janela


#Container principal
container = ttk.Frame(root) 
#cria um container e coloca dentro da Janela Principal
container.pack(fill="both",expand=True) 
#Expande o container na Tela Principal

# TROQUE AQUI A TELA DESEJADA
TelaPacientes(container) #Mude para a TelaPacientes

root.mainloop()

 