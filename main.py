# ====================================================================================================
# ETS2 Company Tool - Ferramenta para auxiliar na criação de def companys para Euro Truck Simulator 2
# ====================================================================================================

#Imports
import customtkinter as ctk # Import da biblioteca da Interface
from tkinter import filedialog, messagebox # Diálogos nativos do sistema
import os   # Operações com arquivos e pastas (como 'fs' em Node.js)
from pathlib import Path # Manipulação de caminhos de arquivos

# Classe principal da aplicação #
class ETS2CompanyTool:

    def __init__(self):  # Em py se usa self ao invés de this como no js e o ___init___ é o construtor da classe

        ctk.set_appearance_mode("dark") # Define o modo escuro da interface
        ctk.set_default_color_theme("blue") # Define a cor padrão de destaque

        # Criação da janela
        self.janela = ctk.CTk()
        self.janela.title("ETS2 Company Tool") # Título da janela
        self.janela.geometry("900x900") # Largura x Altura
        self.janela.minsize(800, 800) # Define o tamanho mínimo da janela


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
        self._criar_secao_log()

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

        header = ctk.CTkFrame(frame_empresas, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            header,
            text="🏢 Empresas Encontradas",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="Selecionar Todas",
            width=120,
            command=self._selecionar_todas
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            header,
            text="Desmarcar Todas",
            width=120,
            command=self._desmarcar_todas
        ).pack(side="right", padx=5)

        # Frame com scroll para a lista de empresas
        self.frame_lista_empresas = ctk.CTkScrollableFrame(frame_empresas, height=150)
        self.frame_lista_empresas.pack(fill="both", expand=True, padx=10, pady=5)

        # Mensagem inicial
        self.label_sem_empresas = ctk.CTkLabel(
            self.frame_lista_empresas,
            text="Selecione uma pasta Company para ver as empresas disponíveis",
            text_color="gray"
        )
        self.label_sem_empresas.pack(pady=20)

    # Cria a seção de logs
    def _criar_secao_log(self):

        frame_log = ctk.CTkFrame(self.container)
        frame_log.pack(fill="both", pady=(0,10))

        ctk.CTkLabel(
            frame_log,
            text="📝 Logs de Ações",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.texto_log = ctk.CTkTextbox(frame_log, height=150)
        self.texto_log.pack(fill="both", expand=True, padx=10, pady=5)
        self._log("Programa iniciado. Selecione as pastas para começar.")

    # Cria os botões de ação
    def _criar_botoes_acao(self):

        frame_botoes = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_botoes.pack(fill="x")

        ctk.CTkButton(
            frame_botoes,
            text="👁️ Preview",
            width=150,
            command=self._mostrar_preview
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_botoes,
            text="🚀 Executar",
            width=150,
            fg_color="green",
            hover_color="dark green",
            command=self._executar
        ).pack(side="right", padx=5)

    # Métodos de Ação #
    def _selecionar_pasta_company(self):

        pasta = filedialog.askdirectory(title="Selecione a Pasta Company do Seu Mod")
        if pasta: # Se uma pasta foi selecionada
            self.pasta_company.set(pasta)
            self._log(f"Pasta Company selecionada: {pasta}")
            self._carregar_empresas()

    def _selecionar_pasta_in(self):
        pasta = filedialog.askdirectory(title="Selecione a Pasta IN que Contém seus Arquivos Modelo")
        if pasta:
            self.pasta_in_modelo.set(pasta)
            self._log(f"Pasta IN Modelo Selecionada: {pasta}")

    def _selecionar_pasta_out(self):
        pasta = filedialog.askdirectory(title="Selecione a Pasta OUT que Contém seus Arquivos Modelo")
        if pasta:
            self.pasta_out_modelo.set(pasta)
            self._log(f"Pasta OUT Modelo Selecionada: {pasta}")
    
    def _carregar_empresas(self):
        # Lógica que vai cerregar e ler a pasta company e identificar as empresas disponíveis
        pasta = self.pasta_company.get()

        # Limpa a lista atual se já possuia algum arquivo aberto
        for widget in self.frame_lista_empresas.winfo_children():
            widget.destroy()

        self.empresas = [] # Reseta a lista, array vazio
        self.empresas_selecionadas = {}

        if not pasta or not os.path.exists(pasta):
            self._log("ERRO: Caminho da pasta Company inválido ou não existe!")
            return

        # Lista todas as subpastas existentes na pasta principal da company
        for item in sorted(os.listdir(pasta)):
            caminho_completo = os.path.join(pasta, item)
            # Verifica se realmente é uma pasta
            if os.path.isdir(caminho_completo):
                self.empresas.append(item)

                # Variável booleana para os checkboxes
                var = ctk.BooleanVar(value=True) # Por padrão vem todas selecionadas
                self.empresas_selecionadas[item] = var

                checkbox = ctk.CTkCheckBox(
                    self.frame_lista_empresas,
                    text=item,
                    variable=var
                )
                checkbox.pack(anchor="w", pady=2)

            if self.empresas:
                self._log(f"Encontradas {len(self.empresas)} empresas na pasta Company.")
            else:
                ctk.CTkLabel(
                    self.frame_lista_empresas,
                    text="Nenhuma empresa encontrada na pasta Company selecionada.",
                    text_color="gray"
                ).pack(pady=20)

    def _selecionar_todas(self):
        for var in self.empresas_selecionadas.values():
            var.set(True)

    def _desmarcar_todas(self):
        for var in self.empresas_selecionadas.values():
            var.set(False)

    def _log(self, mensagem):
        self.texto_log.insert("end", f"{mensagem}\n")
        self.texto_log.see("end")  # Rola automaticamente para o final

    def _mostrar_preview(self):
        if not self._validar_selecoes():
            return
        
        empresas_marcadas = [
            nome for nome, var in self.empresas_selecionadas.items()
            if var.get()
        ]

        modo = self.modo_operacao.get()

        self._log("=" * 40)
        self._log(f"PREVIEW - Modo: {modo.upper()}")
        self._log(f"Empresas Selecionadas ({len(empresas_marcadas)})")
        for empresa in empresas_marcadas:
            self._log(f" -{empresa}")
        self._log("=" * 40)

    def _validar_selecoes(self):
        if not self.pasta_company.get():
            messagebox.showerror("Erro", "Por favor, selecione a pasta Company.")
        if not self.pasta_in_modelo.get():
            messagebox.showerror("Erro", "Por favor, selecione a pasta IN modelo.")
        if not self.pasta_out_modelo.get():
            messagebox.showerror("Erro", "Por favor, selecione a pasta OUT modelo.")

        empresas_marcadas = [
            nome for nome, var in self.empresas_selecionadas.items()
            if var.get()
        ]

        if not empresas_marcadas:
            messagebox.showerror("Erro", "Por favor, selecione ao menos uma empresa para processar.")
            return False
        return True

    def _executar(self):

        if not self._validar_selecoes():
            return
        
        empresas_marcadas = [
            nome for nome, var in self.empresas_selecionadas.items()
            if var.get()
        ]

        if not empresas_marcadas:
            messagebox.showwarning("Aviso", "Nenhuma empresa selecionada!")
            return
        
        modo = self.modo_operacao.get()
        resposta = messagebox.askyesno(
            "Confirmar",
            f"Você tem certeza que deseja executar a operação '{modo}' em {len(empresas_marcadas)} empresas?"
        )

        if resposta:
            self._log("Iniciando operação...")
            # TODO: Implementar a lógica de cópia real
            self._log("✅ Operação concluída!")
            messagebox.showinfo("Concluído", "Operação concluída com sucesso!")

    # Inicia a Aplicação
    def executar(self):
        self.janela.mainloop()

# Ponto de entrada do programa #
if __name__ == "__main__":
    # Cria uma instância da aplicação
    app = ETS2CompanyTool()
    # Inicia o loop de eventos (mantém a janela aberta)
    app.executar()