#Interface
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

from processador import processar_fitas

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AplicativoBuscador(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Buscador de Fitas")
        self.geometry("580x550")
        self.resizable(False, False)

        self.construir_interface()

    def construir_interface(self):
        # --- Frame Pasta ---
        frame_pasta = ctk.CTkFrame(self)
        frame_pasta.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(frame_pasta, text="1. Diretório dos Arquivos", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

        container_pasta = ctk.CTkFrame(frame_pasta, fg_color="transparent")
        container_pasta.pack(fill="x", padx=10, pady=10)

        self.entry_pasta = ctk.CTkEntry(container_pasta, width=350)
        self.entry_pasta.pack(side="left", padx=(0, 10))
        self.entry_pasta.insert(0, str(Path.home() / "Desktop"))

        btn_pasta = ctk.CTkButton(container_pasta, text="Procurar...", command=self.selecionar_pasta, width=100)
        btn_pasta.pack(side="left")

        # --- Frame Filtros ---
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(fill="x", padx=20, pady=10)

        # Mudei o título já que as 'ações' agora são automáticas
        ctk.CTkLabel(frame_filtros, text="2. Filtros de Busca", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(10, 5))

        ctk.CTkLabel(frame_filtros, text="Tipo de Arquivo:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.combo_tipo = ctk.CTkComboBox(frame_filtros, values=["PREVIA", "PROCESSAMENTO", "CONSOLIDADO"], width=150)
        self.combo_tipo.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.combo_tipo.set("PREVIA")

        ctk.CTkLabel(frame_filtros, text="Fita (De):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_inicio = ctk.CTkEntry(frame_filtros, width=80)
        # Adicionado um padding extra (espaço) embaixo para compensar a saída do checkbox
        self.entry_inicio.grid(row=2, column=1, sticky="w", padx=10, pady=(5, 15)) 

        ctk.CTkLabel(frame_filtros, text="Fita (Até):").grid(row=2, column=2, sticky="w", padx=10, pady=5)
        self.entry_fim = ctk.CTkEntry(frame_filtros, width=80)
        self.entry_fim.grid(row=2, column=3, sticky="w", padx=10, pady=(5, 15))

        # --- Botão Buscar ---
        btn_buscar = ctk.CTkButton(self, text="EXECUTAR BUSCA", command=self.executar_busca, height=40, font=("Arial", 14, "bold"))
        btn_buscar.pack(pady=15)

        # --- Frame Resultados ---
        self.text_resultado = ctk.CTkTextbox(self, width=540, height=150)
        self.text_resultado.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    # ==========================================
    # METODOS DE AÇÃO DA INTERFACE
    # ==========================================
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta com os arquivos")
        if pasta:
            self.entry_pasta.delete(0, 'end')
            self.entry_pasta.insert(0, pasta)

    def atualizar_log(self, mensagem):
        self.text_resultado.insert("end", mensagem)
        self.text_resultado.see("end") 
        self.update() 

    def executar_busca(self):
        diretorio = self.entry_pasta.get()
        tipo = self.combo_tipo.get()
        inicio = self.entry_inicio.get()
        fim = self.entry_fim.get()

        if not diretorio or not tipo or not inicio or not fim:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        try:
            numeros_para_buscar = [str(n) for n in range(int(inicio), int(fim) + 1)]
        except ValueError:
            messagebox.showerror("Erro", "Os campos 'De' e 'Até' devem conter apenas números inteiros.")
            return

        self.text_resultado.delete("0.0", "end")
        self.atualizar_log(f"Aguarde, buscando arquivos...\n{'-'*40}\n")

        # Chama o processador SEM a variável do checkbox
        processar_fitas(
            diretorio=diretorio,
            tipo_buscado=tipo,
            numeros_alvo=numeros_para_buscar,
            callback_log=self.atualizar_log
        )

if __name__ == "__main__":
    app = AplicativoBuscador()
    app.mainloop()