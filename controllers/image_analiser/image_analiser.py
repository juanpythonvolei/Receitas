from controllers.acessory_controlers.acessory_controllers import *


def file(pergunta,file):
            uploaded_parts = []
            final = ''
            if '.pdf' in file.name:
                tempfile = create_temporary_file(tipo='.pdf',file=file)
                arquivo_carregado = genai.upload_file(tempfile,mime_type='application/pdf')
                uploaded_parts.append(arquivo_carregado)
                delete_temp_file(tempfile)
            elif '.xlsx' in file.name or '.csv' in file.name :   
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    try:
                        data  = pd.read_excel(tempfile)
                    except:
                          data = pd.read_csv(tempfile)
                    texto = data.to_string()
                    final += f'''Dados do arquivo {tempfile}:\n
                    {texto}
                    \n'''
                    delete_temp_file(tempfile)
            elif '.jpg' in file.name or '.jpeg' in file.name:
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    arquivo_carregado = genai.upload_file(tempfile,mime_type='image/jpeg')
                    uploaded_parts.append(arquivo_carregado)
                    delete_temp_file(tempfile)
            elif '.docx' in file.name:
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    doc = Document(tempfile)
                    for paragraph in doc.paragraphs:
                        final += f'{paragraph.text}\n'
                    delete_temp_file(tempfile)
            else:
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    with open(tempfile,'rb') as tmp:
                        txt = tmp.read()
                    final += str(f'''Conteúdo código {tempfile}:\n
                                     {txt}
\n''')
                    delete_temp_file(tempfile)
            uploaded_parts.append({'text':final})
            model = genai.GenerativeModel('gemini-1.5-flash') 
            chat = model.start_chat(history=[{"role":"user","parts":uploaded_parts}]) 
            response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
            return response.text

def delete_temp_file(file):
    if os.path.exists(file): 
        os.remove(file)


def create_temporary_file(tipo,file):
  with tempfile.NamedTemporaryFile(delete=False, suffix=tipo) as tmp_file:
        tmp_file.write(file.read())
        return tmp_file.name
  