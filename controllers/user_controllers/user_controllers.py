from db.db import *
from controllers.acessory_controlers.acessory_controllers import *
import streamlit as st

def delete_user(nome):  
    usuario = session.query(Usuarios).filter_by(nome=nome).first()
    session.delete(usuario)
    session.commit()
    st.switch_page("Início.py")

def update_user(nome,senha):
    usuario = session.query(Usuarios).filter_by(nome=nome).first()
    usuario.senha = senha
    session.commit()
    st.rerun()

def login_(nome,senha):
    usuario = session.query(Usuarios).filter_by(nome=nome,senha=senha).first()
    if usuario:
        st.session_state.selected_option = nome
        return True
    return False

def add_user(nome,senha):
    if session.query(Usuarios).filter_by(nome=nome).first():
        return False
    session.add(Usuarios(nome=nome,senha=senha))
    session.commit()
    st.session_state.selected_option = nome
    return True

@st.dialog('Deseja realizar essa ação?')
def warning_delete(user):
  if str(st.text_input(placeholder='Digite "sim" para confirmar',label='',value='')).casefold().strip() == 'sim':
        delete_user(user)
        return st.success('Receita descartada com sucesso!')