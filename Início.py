
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

login.title('Login')
login.divider()
nome = login.text_input('Nome',placeholder='Nome').strip()
senha = login.text_input('Senha',type='password',placeholder='Senha').strip()
botao = login.button('Entrar')
botao_criar = login.button('Criar Conta')
if botao:
    if nome and senha:
        if login_(nome,senha):
            st.switch_page('pages/Receitas.py')
        else:
            st.error('Usuário ou senha incorretos')
    else:
        st.error('Preencha todos os campos')
if botao_criar:
    st.switch_page('pages/Criar Conta.py')