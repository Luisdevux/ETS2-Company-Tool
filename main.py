# ====================================================================================================
# ETS2 Company Tool - Ferramenta para auxiliar na criação de def companys para Euro Truck Simulator 2
# ====================================================================================================

#Imports
# Import da biblioteca da Interface
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from pathlib import Path

# Configuração do tema
ctk.set_appearance_mode("dark")

# Classe principal da aplicação
class ETS2CompanyTool:

    def ___init___(self):  # Em py se usa self ao invés de this como no js e o ___init___ é o construtor da classe

        ctk.set_appearance_mode("dark") # Define o modo escuro da interface
        ctk.set_default_color_theme("blue") # Define a cor padrão de destaque

        # Criação da janela
        self.janela = ctk.CTk()
        self.janela.title("ETS2 Company Tool") # Título da janela
        self.janela.geometry("800x800") # Largura x Altura
        self.janela.minsize(700, 700) # Define o tamanho mínimo da janela


        # Variaveis que vão armazenar os caminhos dos arquiivos selecionaveis
        # StringVar é como um "state" reativo, quando muda, a UI atualiza automaticamente
        self.pasta_company = ctk.StringVar(value="")
        self.pasta_in_modelo = ctk.StringVar(value="")
        self.pasta_out_modelo = ctk.StringVar(value="")

        # Variável para o modo de operação (Adicionar ou Substituir)
        self.modo_operacao = ctk.StringVar(value="substituir") # Modo padrão selecionado é substituir

        self.empresas = []  # Lista para armazenar as empresas carregadas
        self.empresas_selecionadas = {} # Dicionario para armazenar as seleções das empresas

        # Configuração dos componentes da interface
        self._criar_interface()

    def _criar_interface(self):

        # Container principal
        self.container = ctk.CTkFrame(self.janela)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Aqui começa a estilização e elementos que terão na janela
        
        # Título #
        titulo = ctk.CTkLabel(
            self.container,
            text="🚛 ETS2 Company Tool",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=(0, 20))

        # Seleção de Pastas
        self._criar_secao_pastas()

        # Seleção de Modo (Adicionar ou Substituir)
        self._criar_secao_modo()

        # Lista de Empresas Encontradas nas Companys
        self._criar_secao_empresas()

        # Logs
        self._criar_secao_logs()

        # Botões das Ações
        self._criar_botoes_acao()

    def _criar_secao_pastas(self):
        # Seção da seleção de pastas
        frame_pastas = ctk.CTkFrame(self.container)
        frame_pastas.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_pastas,
            text="📁 Seleção de Pastas",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        # Pasta Company
        self._criar_seletor_pasta(
            frame_pastas,
            "Pasta Company (do mod):",
            self.pasta_company,
            self._selecionar_pasta_company
        )

        # Pasta IN Modelo
        self._criar_seletor_pasta(
            frame_pastas,
            "Pasta IN Modelo (com os arquivos modelo a serem inseridos):",
            self.pasta_in_modelo,
            self._selecionar_pasta_in
        )

        # Pasta OUT Modelo
        self._criar_seletor_pasta(
            frame_pastas,
            "Pasta OUT Modelo (com os arquivos modelo a serem inseridos):",
            self.pasta_out_modelo,
            self._selecionar_pasta_out
        )

    # Cria a seção para criar o seletor de pastas
    def _criar_seletor_pasta(self, parent, label_text, variavel, comando):

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(frame, text=label_text, width=180, anchor="w").pack(side="left")

        entrada = ctk.CTkEntry(frame, textvariable=variavel, width=400)
        entrada.pack(side="left", padx=5)

        ctk.CTkButton(
            frame,
            text="Selecionar",
            width=100,
            command=comando
        ).pack(side="left")
    
    # Cria a seção para selecionar a pasta Company
    def _criar_secao_modo(self):

        frame_modo = ctk.CTkFrame(self.container)
        frame_modo.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_modo,
            text="⚙️ Modo de Operação",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        frame_radios = ctk.CTkFrame(frame_modo, fg_color="transparent")
        frame_radios.pack(fill="x", padx=10, pady=5)

        # Radio Button para selecão do modo
        ctk.CTkRadioButton(
            frame_radios,
            text="Substituir (remove pastas in/out existentes)",
            variable=self.modo_operacao,
            value="substituir"
        ).pack(side="left", padx=20)

        ctk.CTkRadioButton(
            frame_radios,
            text="Adicionar (matém pastas in/out existentes, caso existam)",
            variable=self.modo_operacao,
            value="adicionar"
        ).pack(side="left", padx=20)

    # Cria onde vai aparecer a lista das empresas encontradas na pasta company
    def _criar_secao_empresas(self):

        frame_empresas = ctk.CTkFrame(self.container)
        frame_empresas.pack(fill="both", expand=True, pady=(0, 10))

        

    # Inicia a Aplicação
    def executar(self):
        self.janela.mainloop()

# Ponto de entrada do programa
if __name__ == "__main__":
    # Cria uma instância da aplicação
    app = ETS2CompanyTool()
    # Inicia o loop de eventos (mantém a janela aberta)
    app.executar()