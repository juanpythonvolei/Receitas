
from controllers.controllers import *

st.markdown("""
    <style>
       [aria-expanded='true'] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None


login = st.container(border=True)

login.title('Criaçã de Usuário')
login.divider()
nome = login.text_input('Novo Nome',placeholder='Insira um usuário').strip()
senha = login.text_input('Nova Senha',type='password',placeholder='Insira uma nova Senha').strip()
botao = login.button('Criar Conta')
botao_login = login.button('Já tem uma conta? Faça login')
if botao:
    if nome and senha:
        if add_user(nome,senha):
            st.switch_page('pages/Receitas.py')
        else:
            st.error('Usuário ou senha incorretos')
    else:
        st.error('Preencha todos os campos')
if botao_login:
      st.switch_page('Início.py')
