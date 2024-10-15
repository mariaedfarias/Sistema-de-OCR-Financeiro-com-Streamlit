import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
import cv2
import pandas as pd
import io

#Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
l
#Layout
st.set_page_config(page_title="Sistema de OCR Financeiro", layout="wide")

st.title("🏦 Gerenciamento de Documentos Financeiros")
st.markdown("Automatize a leitura e o processamento de cheques, faturas e outros documentos financeiros.")

#Upload de arquivo e ajustes
with st.sidebar:
    st.header("Configurações")
    uploaded_file = st.file_uploader("Escolha um arquivo de imagem", type=["jpg", "png", "jpeg"])
    brightness = st.slider("Brilho", 0.0, 2.0, 1.0)
    contrast = st.slider("Contraste", 0.0, 2.0, 1.0)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagem carregada', use_column_width=True)

    #Converter a imagem
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    #Ajuste Brilho
    img_cv = cv2.convertScaleAbs(img_cv, alpha=contrast, beta=(brightness - 1) * 255)

    #Convertendo imagem para exibição
    processed_image = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    st.image(processed_image, caption='Imagem Processada', use_column_width=True)

    #Extraindo texto com OCR
    text = pytesseract.image_to_string(processed_image)
    st.subheader("Texto Extraído:")
    st.write(text)

    #Busca por valores monetários
    if any(char.isdigit() for char in text):
        st.success("Dados extraídos com sucesso!")
    else:
        st.warning("Nenhum valor monetário encontrado. Verifique a imagem.")

    st.subheader("Exportar Texto")
    export_format = st.selectbox("Escolha o formato de exportação:", ['Texto (.txt)', 'CSV (.csv)'])
    
    if export_format == 'Texto (.txt)':
        txt_buffer = io.StringIO()
        txt_buffer.write(text)
        st.download_button("Baixar como .txt", txt_buffer.getvalue(), "texto_extraido.txt")

    elif export_format == 'CSV (.csv)':
        df = pd.DataFrame({'Texto Extraído': [text]})
        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar como .csv", csv_buffer, "texto_extraido.csv")
