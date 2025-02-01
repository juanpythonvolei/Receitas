
from controllers.controllers import *
import datetime

try:
    st.subheader(f'Olá, {st.session_state.selected_option}')
except:
    st.switch_page('Início.py')

Cozinheiro = st.container(border=True)
Cozinheiro.subheader('Meu nome é Cozinheiro e estou pronto para te ajudar!')
pergunta = Cozinheiro.chat_input('Fale comigo!')
audio_ = Cozinheiro.audio_input('Se perferir, pode gravar a sua pergunta')

if audio_:
  pergunta = audio(audio_)
if pergunta:
  humano = st.chat_message('human')
  humano.write(pergunta)
  status = Cozinheiro.status('Processando...')
  with status:
    resposta = chat_message(pergunta)
    arquivo_audio = create_audio(resposta)
    status.update(label='Finalizado!')
  robo = st.chat_message('assistant')
  robo.write(resposta)
  ouvir = st.audio('./audio/audio.mp3',format='audio/mpeg')
  botao = st.button('Salvar Receita')
  if botao:
    add_receita('Receita do cozinheiro',str(datetime.now()),resposta)
    st.success('Receita salva com sucesso!')


