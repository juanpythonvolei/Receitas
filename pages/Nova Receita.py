
from db.db import *
from controllers.acessory_controlers.acessory_controllers import *
from controllers.image_analiser.image_analiser import *
import streamlit as st
from controllers.receitas_controllers.receitas_controllers import *

try:
    st.subheader(f'Olá, {st.session_state.selected_option}')
except:
    st.switch_page('Início.py')

Adicao = st.container(border=True)
Adicao.title('Adicionar Receita')
Tipo = Adicao.pills(label='Selecione o tipo da receita',options=['Doce','Salgado','Bebida'])
if Tipo:
    Nome = Adicao.text_input('Nome da Receita',placeholder='Nome').strip()
    Data = Adicao.date_input('Data da Receita')
    Infos = Adicao.text_area('Informações da Receita',placeholder='Informações')
    audio_= Adicao.audio_input('Grave a receita')
    arquivo = Adicao.file_uploader('Carregue um arquivo',type=['pdf','xlsx','csv','jpg','jpeg','docx','txt'],accept_multiple_files=False)
    if audio_:
        Infos = audio(audio_)
    if arquivo:
      Infos = file('Faça a transcrição detalhada desse arquivo que contém uma receita',arquivo) 
    Adicionar = Adicao.button('Adicionar 📃')
    if Adicionar:
        outro_status = Adicao.status(label='Processando...')
        with outro_status:
            if Data and Infos and Nome:
              add_receita(Nome,Data,Infos,Tipo,st.session_state.selected_option)
              outro_status.update(label='Finalizado!')
              Adicao.info('Receita Adicionada')
            else:
              Adicao.error('Preencha todos os campos')
