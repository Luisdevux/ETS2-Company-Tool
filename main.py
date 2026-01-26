# ====================================================================================================
# ETS2 Company Tool - Ferramenta para auxiliar na criação de def companys para Euro Truck Simulator 2
# ====================================================================================================

#Imports
import customtkinter as ctk # Import da biblioteca da Interface
from tkinter import filedialog, messagebox # Diálogos nativos do sistema
import os   # Operações com arquivos e pastas (como 'fs' em Node.js)
from pathlib import Path # Manipulação de caminhos de arquivos
import shutil # Operações de cópia e movimentação de arquivos
import zipfile # Manipulação de arquivos zip

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
        self.pasta_empresas_fonte = ctk.StringVar(value="")
        self.pasta_company = ctk.StringVar(value="")
        self.pasta_in_modelo = ctk.StringVar(value="")
        self.pasta_out_modelo = ctk.StringVar(value="")

        # Variáveis para manipular arquivos zip/scs
        self.arquivo_scs = None
        self.pasta_temporaria = None

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

        # Selecão de pasta com as empresas fonte, dos mapas
        self._criar_secao_importar_empresas()

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

    # Cria a seção para importar empresas
    def _criar_secao_importar_empresas(self):

        frame_importar = ctk.CTkFrame(self.container)
        frame_importar.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_importar,
            text="📦 Importar Empresas (do mapa)",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        frame_selecao = ctk.CTkFrame(frame_importar, fg_color="transparent")
        frame_selecao.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(
            frame_selecao,
            text="Pasta com empresas:",
            width=180,
            anchor="w"
        ).pack(side="left")

        ctk.CTkEntry(
            frame_selecao,
            textvariable=self.pasta_empresas_fonte,
            width=400
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_selecao,
            text="Selecionar",
            width=100,
            command=self._selecionar_pasta_empresas_fonte
        ).pack(side="left")

        ctk.CTkButton(
            frame_selecao,
            text="Importar",
            width=100,
            fg_color="orange",
            hover_color="dark orange",
            command=self._importar_empresas
        ).pack(side="left", padx=5)

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

        escolha = messagebox.askquestion(
            "Tipo de Seleção",
            "Deseja selecionar um arquivo .scs?\n\nSim = Arquivo .scs\nNão = Pasta normal"
        )

        if escolha == "yes":
            arquivo = filedialog.askopenfilename(
                title="Selecione o arquivo .scs",
                filetypes=[("Arquivos SCS", "*.scs"), ("Arquivos Zip", "*.zip"), ("Todos os arquivos", "*.*")]
            )

            if arquivo:
                self._log(f"Arquivo .scs selecionado: {arquivo}")
                self._extrair_scs(arquivo)

        else:
            pasta = filedialog.askdirectory(title="Selecione a Pasta Company do Seu Mod")
            if pasta:
                self.arquivo_scs = None
                self.pasta_temporaria = None
                self.pasta_company.set(pasta)
                self._log(f"Pasta Company selecionada: {pasta}")
                self._carregar_empresas()
    
    def _extrair_scs(self, arquivo_scs):

        # Cria uma pasta temporária para extrair o conteúdo do SCS e adiciona "extrido" ao nome
        nome_sem_extensao = os.path.splitext(os.path.basename(arquivo_scs))[0]
        pasta_destino = nome_sem_extensao + "_extraido"

        self._log(f"Extraindo arquivo .scs para a pasta temporária: {pasta_destino}")

        try:
            with zipfile.ZipFile(arquivo_scs, 'r') as zip_ref:
                zip_ref.extractall(pasta_destino)

            self.arquivo_scs = arquivo_scs
            self.pasta_temporaria = pasta_destino
            self._log(f"Extração concluída com sucesso.")

            pasta_company = os.path.join(pasta_destino, "def", "company")

            if os.path.exists(pasta_company):
                self.pasta_company.set(pasta_company)
                self._log(f"Pasta Company encontrada em: {pasta_company}")
            else:
                # Pasta não existe, vamos criar!
                os.makedirs(pasta_company, exist_ok=True)
                self.pasta_company.set(pasta_company)
                self._log(f"📁 Pasta def/company criada em: {pasta_company}")
            
            self._carregar_empresas()
        
        except zipfile.BadZipFile:
            self._log("ERRO: Arquivo não é um ZIP/SCS válido!")
            messagebox.showerror("Erro", "O Arquivo não é um ZIP/SCS válido!")
        except Exception as e:
            self._log(f"ERRO: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro ao extrair o arquivo:\n{str(e)}")
    
    def _recompactar_scs(self):
        if not self.arquivo_scs or not self.pasta_temporaria:
            return  # Se não era um arquivo .scs, não precisa recompactar
        
        # Se for, continua o processo de recompactação
        pasta_arquivo = os.path.dirname(self.arquivo_scs)
        nome_original = os.path.basename(self.arquivo_scs)
        nome_sem_ext = os.path.splitext(nome_original)[0]
        novo_nome = nome_sem_ext + "_com_company.scs"
        caminho_novo = os.path.join(pasta_arquivo, novo_nome)

        self._log(f"Recompactando a pasta temporária para o arquivo .scs: {novo_nome}")
        self._log("⏳ Isso pode demorar um pouco, aguarde...")
        self.janela.update()  # Força atualização da interface

        try:
            # Primeiro conta quantos arquivos tem (para mostrar progresso)
            total_arquivos = sum(len(arquivos) for _, _, arquivos in os.walk(self.pasta_temporaria))
            arquivos_processados = 0
            
            with zipfile.ZipFile(caminho_novo, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Percorre todos os arquivos da pasta extraída
                for raiz, pastas, arquivos in os.walk(self.pasta_temporaria): # os.walk Percorre toda a árvore de pastas (recursivamente)
                    for arquivo in arquivos:
                        caminho_completo = os.path.join(raiz, arquivo)
                        # Calcula o caminho relativo (para manter a estrutura de pastas)
                        caminho_relativo = os.path.relpath(caminho_completo, self.pasta_temporaria)
                        zipf.write(caminho_completo, caminho_relativo)
                        
                        # Atualiza progresso a cada 50 arquivos
                        arquivos_processados += 1
                        if arquivos_processados % 50 == 0:
                            self._log(f"📦 Compactando... {arquivos_processados}/{total_arquivos}")
                            self.janela.update()  # Atualiza a interface
            
            self._log(f"✅ Arquivo criado: {caminho_novo}")
            messagebox.showinfo("Sucesso", f"Arquivo .scs criado!\n\n{novo_nome}")

        except Exception as e:
            self._log(f"Erro ao recompactar: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro ao recompactar:\n{str(e)}")

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

    def _selecionar_pasta_empresas_fonte(self):
        pasta = filedialog.askdirectory(title="Selecione a Pasta com as Empresas do Mapa")
        if pasta:
            self.pasta_empresas_fonte.set(pasta)

            empresas = [item for item in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, item))]
            self._log(f"Pasta de empresas selecionada: {pasta}")
            self._log(f"📦 Encontradas {len(empresas)} empresas para importar")

    def _importar_empresas(self):
        pasta_fonte = self.pasta_empresas_fonte.get()
        pasta_destino = self.pasta_company.get()

        if not pasta_fonte:
            messagebox.showerror("Erro", "Selecione a pasta com as empresas primeiro!")
            return
        
        if not pasta_destino:
            messagebox.showerror("Erro", "Selecione a pasta Company do mod primeiro!")
            return
        
        empresas = [item for item in os.listdir(pasta_fonte) if os.path.isdir(os.path.join(pasta_fonte, item))]

        if not empresas:
            messagebox.showwarning("Aviso", "Nenhuma empresa encontrada na pasta fonte selecionada!")
            return
        
        self._log(f"Iniciando importação de {len(empresas)} empresas...")

        for empresa in empresas:
            origem = os.path.join(pasta_fonte, empresa)
            destino = os.path.join(pasta_destino, empresa)

            if os.path.exists(destino):
                self._log(f"Empresa {empresa} já existe na pasta destino. Pulando importação.")
                continue

            shutil.copytree(origem, destino)
            self._log(f"Empresa {empresa} importada com sucesso.")
        
        self._log(f"Importação concluída!")
        messagebox.showinfo("Sucesso", f"{len(empresas)} empresas importadas!")

        # Atualiza a lista de empresas na interface
        self._carregar_empresas()

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
    
    def _copiar_arquivos_para_empresa(self, empresa):

        # Monta o caminho completo da empresa na pasta company
        caminho_empresa = os.path.join(self.pasta_company.get(), empresa)
        caminho_in = os.path.join(caminho_empresa, "in")
        caminho_out = os.path.join(caminho_empresa, "out")

        modo = self.modo_operacao.get()

        if modo == "substituir":
            if os.path.exists(caminho_in):
                shutil.rmtree(caminho_in)
            if os.path.exists(caminho_out):
                shutil.rmtree(caminho_out)

        # Cria as pastas caso não existam
        os.makedirs(caminho_in, exist_ok=True)
        os.makedirs(caminho_out, exist_ok=True)

        # Copia os arquivos da pasta IN modelo
        pasta_in_modelo = self.pasta_in_modelo.get()
        for arquivo in os.listdir(pasta_in_modelo):
            origem = os.path.join(pasta_in_modelo, arquivo)
            destino = os.path.join(caminho_in, arquivo)
            if os.path.isfile(origem):
                shutil.copy2(origem, destino)

        # Copia os arquivos da pasta OUT modelo
        pasta_out_modelo = self.pasta_out_modelo.get()
        for arquivo in os.listdir(pasta_out_modelo):
            origem = os.path.join(pasta_out_modelo, arquivo)
            destino = os.path.join(caminho_out, arquivo)
            if os.path.isfile(origem):
                shutil.copy2(origem, destino)

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
            for empresa in empresas_marcadas:
                self._log(f"Processando empresa: {empresa}...")
                self._copiar_arquivos_para_empresa(empresa)
            self._log("✅ Operação concluída!")
            messagebox.showinfo("Concluído", "Operação concluída com sucesso!")
            self._recompactar_scs()

    # Inicia a Aplicação
    def executar(self):
        self.janela.mainloop()

# Ponto de entrada do programa #
if __name__ == "__main__":
    # Cria uma instância da aplicação
    app = ETS2CompanyTool()
    # Inicia o loop de eventos (mantém a janela aberta)
    app.executar()