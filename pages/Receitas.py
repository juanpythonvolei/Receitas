import streamlit as st 
from db.db import *
from controllers.controllers import *

try:
    st.subheader(f'Olá, {st.session_state.selected_option}')
except:
    st.switch_page('Início.py')

filtros = st.container(border=True)
filtros.subheader('Filtros')
tipos = filtros.popover('🔍')
nomes = filtros.popover('📛')
data = filtros.popover('📅')
with tipos:
    filtro_tipo = st.pills('Selecione o tipo da receita',options=['Doce','Salgado','Bebida'])
with nomes:
    filtro_nome = st.text_input('Nome da receita').strip()
with data:
    filtro_data = st.date_input('Data da receita',value=None)

status = st.status(label='Carregando Receitas...')
with status:
    if filtro_tipo:
        receitas = session.query(Receitas).filter_by(tipo=filtro_tipo,usuario=st.session_state.selected_option).all()
        status.update(label='Receitas Carregadas!')
    elif filtro_nome:
        receitas = session.query(Receitas).filter_by(usuario=st.session_state.selected_option).all()
        receitas = [receita for receita in receitas if filtro_nome.lower() in receita.nome.lower()]
        status.update(label='Receitas Carregadas!')
    elif filtro_data:  
        receitas = session.query(Receitas).filter_by(data=str(filtro_data),usuario=st.session_state.selected_option).all()
        status.update(label='Receitas Carregadas!')
    elif not filtro_data and not filtro_nome and not filtro_tipo:
        receitas = session.query(Receitas).filter_by(usuario=st.session_state.selected_option).all()
        status.update(label='Receitas Carregadas!')



if not receitas:
    st.warning('Nenhuma receita encontrada')
    st.stop()
for i,receita in enumerate(receitas):
    container = st.container(border=True)
    container.title(f'{receita.nome}   {receita.data}')
    container.subheader(f'Tipo: {receita.tipo}')
    vizualizar = container.button('Ver Receita 📕',key=i+1*2)
    alteracao = container.button('Alterar Receita ⚙️',key=i+2*4)
    descarte = container.button('Descartar Receita 🗑️',key=i+3*6)
    if vizualizar:
        container.info(receita.infos)
    elif alteracao:
        dialog_alteracao(receita.id)
    elif descarte:
        warning(receita.id)
    

