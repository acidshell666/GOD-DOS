import tkinter as tk
from tkinter import ttk
import subprocess
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GOD-DOS")
        self.configure(bg="#252525")
        self.geometry("800x600")  # Definindo um tamanho padrão
        
        # Estilo
        style = ttk.Style(self)
        style.configure(".", foreground="white", background="#252525")
        style.configure("Red.TButton", foreground="white", background="#bf0000")
        style.configure("Dark.TCheckbutton", foreground="white", background="#252525")
        style.configure("Black.TEntry", foreground="white", fieldbackground="#333333", bordercolor="gray")
        
        # Estilo para a Treeview
        style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
        style.map("Treeview", background=[("selected", "#bf0000")])
        
        # Variáveis para armazenar a seleção do usuário
        self.host = tk.StringVar()
        self.encapsulated = tk.BooleanVar(value=False)
        self.bogus_csum = tk.BooleanVar(value=False)
        self.shuffle = tk.BooleanVar(value=False)
        self.quiet = tk.BooleanVar(value=False)
        self.turbo = tk.BooleanVar(value=False)
        self.protocol = tk.StringVar()
        self.threshold = tk.StringVar(value="1000")
        self.sport = tk.StringVar()
        self.dport = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Container principal
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill="both")
        
        # Entrada para o host
        host_label = ttk.Label(main_frame, text="Alvo:")
        host_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        host_label.configure(style="TLabel")
        self.host_entry = ttk.Entry(main_frame, textvariable=self.host, style="Black.TEntry")
        self.host_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.host_entry.focus()
        
        # Botão para iniciar
        self.start_button = ttk.Button(main_frame, text="Iniciar", command=self.start, style="Red.TButton")
        self.start_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Tabela de resultados
        self.result_table = ttk.Treeview(main_frame, columns=("packets_sent", "total_kb"))
        self.result_table.heading("#0", text="ID")
        self.result_table.heading("packets_sent", text="Pacotes Enviados")
        self.result_table.heading("total_kb", text="Total KB")
        self.result_table.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Configurar peso das linhas e colunas
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Opções avançadas
        advanced_frame = ttk.LabelFrame(main_frame, text="Opções Avançadas", padding=10)
        advanced_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Encapsulated
        self.encapsulated_check = ttk.Checkbutton(advanced_frame, text="Encapsulado", variable=self.encapsulated, style="Dark.TCheckbutton")
        self.encapsulated_check.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Bogus Checksum
        self.bogus_csum_check = ttk.Checkbutton(advanced_frame, text="Checksum Falso", variable=self.bogus_csum, style="Dark.TCheckbutton")
        self.bogus_csum_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Shuffle
        self.shuffle_check = ttk.Checkbutton(advanced_frame, text="Embaralhar", variable=self.shuffle, style="Dark.TCheckbutton")
        self.shuffle_check.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Quiet
        self.quiet_check = ttk.Checkbutton(advanced_frame, text="Silencioso", variable=self.quiet, style="Dark.TCheckbutton")
        self.quiet_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Turbo
        self.turbo_check = ttk.Checkbutton(advanced_frame, text="Turbo (apenas para flood)", variable=self.turbo, style="Dark.TCheckbutton")
        self.turbo_check.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Protocol
        protocol_label = ttk.Label(advanced_frame, text="Protocolo:")
        protocol_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        protocol_label.configure(style="TLabel")
        self.protocol_entry = ttk.Entry(advanced_frame, textvariable=self.protocol, style="Black.TEntry")
        self.protocol_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        
        # Threshold
        threshold_label = ttk.Label(advanced_frame, text="Limite de Pacotes:")
        threshold_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        threshold_label.configure(style="TLabel")
        self.threshold_entry = ttk.Entry(advanced_frame, textvariable=self.threshold, style="Black.TEntry")
        self.threshold_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        
        # Source Port
        sport_label = ttk.Label(advanced_frame, text="Porta de Origem:")
        sport_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        sport_label.configure(style="TLabel")
        self.sport_entry = ttk.Entry(advanced_frame, textvariable=self.sport, style="Black.TEntry")
        self.sport_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
        
        # Destination Port
        dport_label = ttk.Label(advanced_frame, text="Porta de Destino:")
        dport_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        dport_label.configure(style="TLabel")
        self.dport_entry = ttk.Entry(advanced_frame, textvariable=self.dport, style="Black.TEntry")
        self.dport_entry.grid(row=8, column=1, sticky="ew", padx=5, pady=5)
        
    def start(self):
        host = self.host.get()
        if host:
            command = ["t50", host]
            if self.encapsulated.get():
                command.append("--encapsulated")
            if self.bogus_csum.get():
                command.append("--bogus-csum")
            if self.shuffle.get():
                command.append("--shuffle")
            if self.quiet.get():
                command.append("-q")
            if self.turbo.get():
                command.append("--flood")
                command.append("--turbo")
            if self.protocol.get():
                command.extend(["--protocol", self.protocol.get()])
            if self.threshold.get():
                command.extend(["--threshold", self.threshold.get()])
            if self.sport.get():
                command.extend(["--sport", self.sport.get()])
            if self.dport.get():
                command.extend(["--dport", self.dport.get()])
                
            print("Comando:", " ".join(command))  # Mostra o comando no terminal
            
            # Iniciar o processo T50
            subprocess.Popen(command)
        else:
            print("Por favor, insira um alvo.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
