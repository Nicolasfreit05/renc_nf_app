import os
import streamlit as st
from tkinter import Tk, filedialog

def renomear_arquivos(pasta):
    contador = 1
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith('.pdf'):
            caminho_pdf = os.path.join(pasta, nome_arquivo)
            novo_nome_base = nome_arquivo.rsplit('.', 1)[0]
            novo_nome = f"{novo_nome_base} ({contador})"
            caminho_novo = os.path.join(pasta, f"{novo_nome}.pdf")
            os.rename(caminho_pdf, caminho_novo)
            contador += 1
    return "Processo finalizado com sucesso!"

def selecionar_pasta():
    root = Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title="Selecione a pasta com os PDFs")
    root.destroy()
    return pasta

st.title("🔄 RENC_NF - Renomeador de Cartas")
st.write("Clique no botão abaixo para selecionar uma pasta com arquivos PDF e renomeá-los.")

if st.button("Selecionar pasta e renomear PDFs"):
    pasta = selecionar_pasta()
    if pasta:
        mensagem = renomear_arquivos(pasta)
        st.success(mensagem)
    else:
        st.warning("Nenhuma pasta selecionada.")
