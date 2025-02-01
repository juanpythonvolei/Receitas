<<<<<<< HEAD
# Para criar uma imagem do script num container docker, utilizar esse comando no terminal e dentro da pasta em que estiver o ou os scripts: docker build -t nome_do_container .
# Para rodar o container, utilizar esse comando: docker run nome_do_container



# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /pasta

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o script Python para o contêiner
COPY main.py .

# Execute o script quando o contêiner iniciar
CMD ["python", "main.py"]
=======
# Para criar uma imagem do script num container docker, utilizar esse comando no terminal e dentro da pasta em que estiver o ou os scripts: docker build -t nome_do_container .
# Para rodar o container, utilizar esse comando: docker run nome_do_container



# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /pasta

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o script Python para o contêiner
COPY main.py .

# Execute o script quando o contêiner iniciar
CMD ["python", "main.py"]
>>>>>>> 238bc3820ded5dc36be31bbaf652ca4e569b4458
