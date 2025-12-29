import streamlit as st
import fitz  # PyMuPDF
import os
import io
import zipfile
import re

st.set_page_config(page_title="Renomeador de PDFs - C/C", layout="centered")
st.title("📄 RENC_NF - Renomeador de Cartas")
st.write("Faça upload dos arquivos PDF abaixo. O nome será extraído do conteúdo após 'C/C' ou 'C/C:'")

uploaded_files = st.file_uploader("Selecione os arquivos PDF", type="pdf", accept_multiple_files=True)

def extrair_nome(texto):
    padroes = [r"C/C[:\s]+([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç\s]+)"]
    for padrao in padroes:
        match = re.search(padrao, texto)
        if match:
            return match.group(1).strip().replace(" ", "_")
    return None

def processar_pdfs(arquivos):
    arquivos_renomeados = []
    for arquivo in arquivos:
        nome_original = arquivo.name
        try:
            with fitz.open(stream=arquivo.read(), filetype="pdf") as doc:
                texto = ""
                for pagina in doc:
                    texto += pagina.get_text()

            novo_nome_base = extrair_nome(texto)
            if not novo_nome_base:
                novo_nome_base = os.path.splitext(nome_original)[0] + "_SEM_NOME"

            novo_nome = f"{novo_nome_base}.pdf"

            with fitz.open(stream=arquivo.getvalue(), filetype="pdf") as doc:
                pdf_bytes = doc.write()
                arquivos_renomeados.append((novo_nome, pdf_bytes))

        except Exception as e:
            st.error(f"Erro ao processar {nome_original}: {e}")

    return arquivos_renomeados

if uploaded_files:
    st.write("🔄 Processando arquivos...")
    resultados = processar_pdfs(uploaded_files)

    if resultados:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for nome_arquivo, conteudo in resultados:
                zip_file.writestr(nome_arquivo, conteudo)

        st.success("✅ Arquivos renomeados com sucesso!")
        st.download_button(
            label="📥 Baixar arquivos renomeados (.zip)",
            data=zip_buffer.getvalue(),
            file_name="cartas_renomeadas.zip",
            mime="application/zip"
        )
    else:
        st.warning("Nenhum arquivo válido foi processado.")
