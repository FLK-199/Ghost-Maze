import os
import sys

def resource_path(relative_path):
    try:
        # Quando o PyInstaller roda o .exe, ele cria uma pasta temporária 
        # e armazena o caminho dela na variável sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver rodando como .exe, usa o caminho normal da pasta do projeto
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)