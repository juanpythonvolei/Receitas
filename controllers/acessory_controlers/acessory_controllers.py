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
from controllers.serializers.serializer import *
from io import BytesIO
key = st.secrets['api']
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash') 







def audio(content):
    rec = sr.Recognizer()
    with sr.AudioFile(content) as arquivo_audio:
                    audio = rec.record(arquivo_audio)
                    texto = rec.recognize_google(audio,language ='pt-BR ')
    chat = model.start_chat(history=[]) 
    response = chat.send_message(f'Por favor, Faça uma correta correção e organização do segunite texto: {texto}. Por favor, retorne apenas o texto como resposta') 
    return response.text

def chat_message(message,user):
    receitas = session.query(Receitas).filter_by(usuario=user).all()
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

@st.cache_data
def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data 

def donwload(user,tipo):
    dataframes = []
    if session.query(Usuarios).filter_by(nome=user):
        Dados = session.query(Receitas).filter_by(usuario=user).all()
        for i,dado in enumerate(Dados):
            schema = ReceitaSchema(many=False)
            dict_dado = schema.dump(dado)
            dataframes.append(pd.DataFrame(dict_dado,index=[i]))
    tabela_final = pd.concat(dataframes)
    if str(tipo) == 'xlsx':
        return convert_df_to_excel(tabela_final)
    elif str(tipo) == 'csv':
         return tabela_final.to_csv(index=False)
    else:
         return tabela_final.to_string(index=False)
         
    
