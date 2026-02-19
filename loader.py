import os
import tkinter as tk
from tkinter import filedialog


def choose_game():
    root = tk.Tk()
    root.withdraw()

    initial_dir = os.path.join(os.getcwd(), ".")
    if not os.path.exists(initial_dir):
        os.makedirs(initial_dir)

    arquivo_selecionado = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="Selecione a ROM do Game Boy",
        filetypes=[("Game Boy ROMs", "*.gb *.gbc"), ("Todos os arquivos", "*.*")]
    )

    root.destroy()

    if arquivo_selecionado:
        return arquivo_selecionado
    else:
        print("Nenhuma ROM selecionada. Encerrando o emulador.")
        return 0
