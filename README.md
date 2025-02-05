# Catálogo de Ofertas

**Este projeto é uma aplicação Django que realiza automação para coletar dados de outro site utilizando o Selenium.**

<details>
    <summary> Sobre desafio </summary>
Desafio Técnico
Você irá desenvolver uma aplicação para uma empresa de Catálogo de Ofertas, utilizando o framework Django, que deverá aplicar raspagem de dados (utilizando o framework Selenium) no site do Mercado Livre (https://www.mercadolivre.com.br) para o produto de “Computador Gamer i7 16gb ssd 1tb”. Após a obtenção dos resultados, devemos listar os produtos encontrados em uma página Web informando os campos:
- Imagem do Produto
- Nome do Produto
- Preço do Produto
- Opção de Parcelamento
- Link do Produto
- Preço sem Desconto (se houver)
- Percentual de Desconto (se houver)
- Tipo de Entrega (Full ou Normal)
- Frete Grátis (se houver)


Devemos adicionar as seguintes opções de filtragem dos produtos encontrados para a facilidade de busca do Usuário:
- Produtos com Frete Grátis
- Produtos Entregues pelo Full

Extra
Como forma de facilitar o entendimento do usuário sobre quais podem ser os melhores produtos, devemos informar os produtos que possuem:
- Maior Preço
- Menor Preço
- Maior Desconto Percentual

Além disso, é interessante que esses dados sejam salvos em uma Banco de Dados relacional (dê preferência ao PostgreSQL), para identificarmos a estrutura desenvolvida por você.

Referências:
https://comoferta.com 
https://ofertas.canaltech.com.br

</details>

--

## Requisitos

- Python >= 3.12
- Django
- Selenium
- Webdriver (Chrome, Firefox ou Edge)
- django-environ


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

**Lembre-se de configurar essas informações para conseguir iniciar a API**
```bash
DB_NAME="Nome-do-banco"
DB_USER="Nome-de-usuario"
DB_PASSWORD="Senha-do-banco"
DB_HOST=localhost
DB_PORT=5432
```

**Realizar as migrações:**
```bash
python manage.py migrate
```


### Passo 4: Rodando o Projeto

**Após configurar o ambiente virtual e o arquivo .env, você pode rodar o servidor Django com o seguinte comando:**

```bash
python manage.py runserver
```

**Acesse a rota:**
```bash
http://127.0.0.1:8000/
```



