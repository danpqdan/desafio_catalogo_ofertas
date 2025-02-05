# Desafio Catálogo de Ofertas

Este projeto é uma aplicação Django que realiza automação para coletar dados de outro site utilizando o Selenium.

## Requisitos

- Python >= 3.12
- Django
- Selenium
- Webdriver (Chrome, Firefox ou outro navegador)

## Configuração do Ambiente Virtual

### Passo 1: Criação de um Ambiente Virtual

1. Para iniciar, crie um ambiente virtual no diretório do projeto. Caso não tenha o `virtualenv` instalado, você pode instalar com o comando:

   ```bash
   pip install virtualenv
   ```

2. Crie o ambiente virtual com o Python 3:

    ```bash
    virtualenv -p python3 venv
    ```

3. Ative o ambiente virtual:
    - **No Windows:**

    ```bash
    .\venv\Scripts\activate
    ```

    - **No Linux**
    ```bash
    source venv/bin/activate
    ```


### Passo 2: Instalação das Dependências

**Instale as dependências do projeto com o comando:**
```bash
pip install -r requirements.txt
```

### Passo 3: Configuração do Arquivo .env

**Para que a automação do Selenium funcione corretamente deve ter por padrão o edge, caso não tenha você precisará configurar o navegador que o Selenium utilizará para coletar os dados. Para isso, crie um arquivo .env na raiz do projeto com o seguinte conteúdo:**
```bash
BROWSER=edge
```

**No campo BROWSER, você pode especificar o navegador que o Selenium deve utilizar. Os valores possíveis são:**

- chrome para o Google Chrome
- firefox para o Mozilla Firefox

### Passo 4: Rodando o Projeto

**Após configurar o ambiente virtual e o arquivo .env, você pode rodar o servidor Django com o seguinte comando:**

```bash
python manage.py runserver
```

**Acesse a rota:**
```bash
http://127.0.0.1:8000/
```



