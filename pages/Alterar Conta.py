import streamlit as st 
from controllers.controllers import *

try:
    st.subheader(f'Olá, {st.session_state.selected_option}')
except:
    st.switch_page('Início.py')

tab1,tab2 = st.tabs(['Dados da Conta','Estatísticas'])


with tab1:
  
  Modicicacao = st.container(border=True)
  Modicicacao.title('Alterar Conta')
  senha = Modicicacao.text_input('Nova Senha',type='password',placeholder='Insira uma nova Senha')
  botao = Modicicacao.button('Alterar Conta')   
  Modicicacao.divider()
  botao_apagar = Modicicacao.button('Apagar Conta')

  if botao:
      if senha:
          status = Modicicacao.status(label='Processando...')
          with status:
              update_user(st.session_state.selected_option,senha.strip())
              status.update(label='Conta Alterada')
          Modicicacao.success('Conta Alterada')
      else:
          Modicicacao.error('Preencha todos os campos')
  if botao_apagar:
      status = Modicicacao.status('Processando...')
      with status:
          delete_user(st.session_state.selected_option)
          status.update('Conta Apagada')
      st.switch_page('Início.py')
with tab2:
  Estatisticas = st.container(border=True)
  Estatisticas.title('Estatísticas')
  Estatisticas.divider()
  col1,col2,col3,col4 = Estatisticas.columns(4)
  with col1:
    Estatisticas.subheader('Receitas Adicionadas')
    Estatisticas.metric(label='Total Receitass',value=len(session.query(Receitas).filter_by(usuario=st.session_state.selected_option).all()))
  with col2:  
    Estatisticas.subheader('Receitas Doces')
    Estatisticas.metric(label='Total Doces',value=len(session.query(Receitas).filter_by(tipo='Doce',usuario=st.session_state.selected_option).all()))
  with col3:
     Estatisticas.subheader('Receitas Salgadas')
     Estatisticas.metric(label='Total Salgadas',value=len(session.query(Receitas).filter_by(tipo='Salgado',usuario=st.session_state.selected_option).all()))
  with col4:
     Estatisticas.subheader('Receitas Bebidas')
     Estatisticas.metric(label='Total Bebidas',value=len(session.query(Receitas).filter_by(tipo='Bebida',usuario=st.session_state.selected_option).all()))