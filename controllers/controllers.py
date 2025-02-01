from db.db import *
import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
import tempfile
import os
from docx import Document
import pandas as pd
import openpyxl


key = st.secrets['api']
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash') 

def delete_user(nome):  
    usuario = session.query(Usuarios).filter_by(nome=nome).first()
    session.delete(usuario)
    session.commit()
    st.rerun()

def update_user(nome,senha):
    usuario = session.query(Usuarios).filter_by(nome=nome).first()
    usuario.senha = senha
    session.commit()
    st.rerun()

def add_user(nome,senha):
    if session.query(Usuarios).filter_by(nome=nome).first():
        return False
    session.add(Usuarios(nome=nome,senha=senha))
    session.commit()
    st.session_state.selected_option = nome
    return True

def login_(nome,senha):
    usuario = session.query(Usuarios).filter_by(nome=nome,senha=senha).first()
    if usuario:
        st.session_state.selected_option = nome
        return True
    return False

def delete_receita(id,user):
    receita = session.query(Receitas).filter_by(id=id,usuario=user).first()
    session.delete(receita)
    session.commit()
    st.rerun()

def add_receita(nome,data,infos,tipo='indefinido',usario='indefinido'):
    session.add(Receitas(nome=nome,data=data,infos=infos,tipo=tipo,usuario=usario))
    session.commit()

def update_receita(id,infos,tipo,user):
    receita = session.query(Receitas).filter_by(id=id,usuario=user).first()
    chat = model.start_chat(history=[]) 
    response = chat.send_message(f'''Você está recebendo dois textos.O primeiro é uma receita já exsitente e o segundo é uma alteração, que pode ser mínima, mediana ou total na receita anterior.
                                Sendo assim, analise os dois textos e veja quais elementos do segundo texto que é a alteração estão presente no segundo de forma a fazer a alteração no primeiro com tais informações. Se por acaso, o usuário inserir uma nova receita completa, substituir o texto original pelo de alteração
                                Texto de receita original: {receita.infos}\n 
                                Texto de alteração: {infos}.\n
                                Retorne, como resposta, um texto final com essas correções''') 
    receita.infos = response.text
    receita.tipo = tipo
    session.commit()

@st.dialog(title='Alterar Receita')
def dialog_alteracao(id):
    container = st.container(border=True)
    novo_tipo = container.pills('Selecione o tipo da receita',options=['Doce','Salgado','Bebida'],key='tipo_alteração')
    novas_infos = container.text_area("Nova informação",placeholder='informação')
    receita_gravada = container.audio_input('Grave a receita')
    botao_alterar = container.button('Alterar')
    if receita_gravada:
        novas_infos = audio(receita_gravada)
    if botao_alterar:
      if novas_infos:
              if novo_tipo:
                  status = container.status(label='Processando...')
                  with status:  
                    update_receita(id,novas_infos,novo_tipo,st.session_state.selected_option)
                    status.update(label='Finalizado!')
                  container.success('Receita atualizada')
              else:
                  container.error('Selecione o tipo da receita')
      else:
          container.error('Preencha todos os campos')

def audio(content):
    rec = sr.Recognizer()
    with sr.AudioFile(content) as arquivo_audio:
                    audio = rec.record(arquivo_audio)
                    texto = rec.recognize_google(audio,language ='pt-BR ')
    chat = model.start_chat(history=[]) 
    response = chat.send_message(f'Por favor, Faça uma correta correção e organização do segunite texto: {texto}. Por favor, retorne apenas o texto como resposta') 
    return response.text

def chat_message(message):
    receitas = session.query(Receitas).all()
    final = 'Receitas Anotadas:\n'
    for receita in receitas:
        final += f'Receita:\n{receita.nome}\n {receita.infos}\n {receita.tipo}\n '
        print(final)
    
    chat = model.start_chat(history=[{"role":"user","parts":[{'text':final}]}]) 
    response = chat.send_message(f'Você é um Cozinheiro Renomado e sua função é me auxiliar na criação ou na consulta de diversos pratos, sendo eles salgados, doces ou bebidas no geral. Sempre que possível, se baseie nas receitas que você está recebendo. Assim sendo responda a essa pergunta:{message}') 
    return response.text

def create_audio(text):
    audio = gTTS(text,lang='pt')
    if os.path.exists('./audio'):
          audio.save('./audio/audio.mp3')
    else:
          os.makedirs('./audio')
          audio.save('./audio/audio.mp3')

@st.dialog('Deseja realizar essa ação?')
def warning(id):
  if str(st.text_input(placeholder='Digite "sim" para confirmar',label='',value='')).casefold().strip() == 'sim':
        delete_receita(id,st.session_state.selected_option)
        return st.success('Receita descartada com sucesso!')