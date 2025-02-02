
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
tab1, tab2 = st.tabs(['Login','Criar Conta'])


with tab1:
    if tab1:
        login = st.container(border=True)
        login.title('Bem vindo ao app de receitas')
        login.subheader('Faça seu login')
        login.divider()
        nome = login.text_input('Nome',placeholder='Nome').strip()
        senha = login.text_input('Senha',type='password',placeholder='Senha').strip()
        botao = login.button('Entrar')
        if botao:
            if nome and senha:
                if login_(nome,senha):
                    st.switch_page('pages/Receitas.py')
                else:
                    st.error('Usuário ou senha incorretos')
            else:
                st.error('Preencha todos os campos')
with tab2:
    if tab2:
        novo = st.container(border=True)
        novo.title("Seja Bem vindo")
        novo.subheader("Crie aqui seu usuário")
        nome_novo = novo.text_input('Novo Nome',placeholder='Insira um usuário').strip()
        senha_nova = novo.text_input('Nova Senha',type='password',placeholder='Insira uma nova Senha').strip()
        botao_novo = novo.button('Criar Conta')
        if botao_novo:
            if nome_novo and senha_nova:
                if add_user(nome_novo,senha_nova):
                    st.switch_page('pages/Receitas.py')
                else:
                    st.error('Usuário ou senha incorretos')
            else:
                st.error('Preencha todos os campos')