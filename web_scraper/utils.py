import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver as wb
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import urllib.parse
from .models import ImagemProduto, Produto

URL_MERCADO_LIVRE = "https://lista.mercadolivre.com.br/"

def iniciar_driver():
    options = wb.FirefoxOptions()
    options.add_argument("--disable-gpu")  # Desabilitar GPU
    options.add_argument("--headless")  #  Não carrega UI
    return webdriver.Firefox(options=options)

def buscar_mercado_livre(termo_busca):
    driver = iniciar_driver()
    actions = ActionChains(driver)
    campo_busca_variavel = termo_busca.replace(" ", "-")
    campo_busca_parse_sem_espaco = urllib.parse.quote(campo_busca_variavel)
    print(f"URL carregado: {URL_MERCADO_LIVRE + campo_busca_parse_sem_espaco + '#D[A:' + termo_busca + ']'}")
    driver.get(URL_MERCADO_LIVRE + campo_busca_parse_sem_espaco + "#D[A:" + termo_busca + "]")
    time.sleep(4)    
    produtos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-layout.ui-search-layout--grid li")
    
    for index, produto in enumerate(produtos):
        try:
            nome = produto.find_element(By.XPATH, ".//h3/a").text
            link = produto.find_element(By.XPATH, "//a[contains(@class, 'poly-component__title')]").get_attribute('href')
            preco = produto.find_element(By.CSS_SELECTOR, ".poly-price__current .andes-money-amount__fraction").text
            preco = float(preco.replace('.', '').replace(',', '.'))
            div_portada = produto.find_element(By.CLASS_NAME, "poly-card__portada")
            
            # Passar o mouse sobre o botão
            div_portada = produto.find_element(By.CLASS_NAME, "poly-card__portada")
            driver.execute_script("arguments[0].scrollIntoView();", div_portada)
            actions.move_to_element(div_portada).perform()
            time.sleep(2)

            # Ajuste o XPath para encontrar todas as imagens do produto
            carousel = div_portada.find_element(By.CLASS_NAME, "andes-carousel-snapped__wrapper")
            imagens = carousel.find_elements(By.TAG_NAME, "img")
            image_urls = [img.get_attribute("src") for img in imagens]

            try:
                preco_sem_desconto = produto.find_element(By.CSS_SELECTOR, '.andes-money-amount__fraction').text
                preco_sem_desconto = float(preco_sem_desconto.replace('.', '').replace(',', '.'))
                percentual_desconto = round((1 - (preco / preco_sem_desconto)) * 100, 2)
            except:
                preco_sem_desconto = None
                percentual_desconto = None
            try:
                
                frete_gratis = False
                tipo_entrega = 'Padrao'
                parcelamento = produto.find_element(By.XPATH, "//span[@class='poly-price__installments']").text
                shipping_element = produto.find_element(By.CSS_SELECTOR, '.poly-component__shipping').text
                try:
                    tipo_entrega = produto.find_element(By.CSS_SELECTOR, '.poly-component__shipped-from').text
                except NoSuchElementException:
                    tipo_entrega = 'Padrao'
                shipping_element_additional_text = produto.find_element(By.CSS_SELECTOR, '.poly-shipping__additional_text').text

                # Verifica se o texto "Chegará grátis amanhã" ou "por ser sua primeira compra" está presente
                if "Frete grátis" in shipping_element or 'Frete grátispor ser sua primeira compra' in shipping_element:
                    frete_gratis = True
                    if "por ser sua primeira compra" in shipping_element_additional_text:
                        frete_gratis = True  # Se ambos os textos estiverem presentes
                    elif "Enviado pelo " in tipo_entrega:
                        tipo_entrega = 'Full' # Caso o texto "Enviado pelo" seja encontrado
                else:
                    tipo_entrega = 'Padrao'  # Caso o "Frete grátis" não esteja presente
                    frete_gratis = False  # Define que não é frete grátis

            except:
                tipo_entrega = "Padrao"
                frete_gratis = False


            # Criando o produto no banco de dados
            produto_model = Produto.objects.create(
                nome=nome,
                preco=preco,
                preco_sem_desconto=preco_sem_desconto,
                percentual_desconto=percentual_desconto,
                parcelamento=parcelamento,
                link=link,
                tipo_entrega=tipo_entrega,
                frete_gratis=frete_gratis
            )

            # Itere sobre os elementos do Selenium e extraia o atributo 'src' para obter a URL da imagem
            for url_imagem in image_urls:  # Lista com as URLs das imagens
                ImagemProduto.objects.create(
                    produto=produto_model,  # Associando a imagem ao produto
                    url_imagem=url_imagem  # A URL da imagem
                )

        
        except Exception as e:
            print(f"Erro ao processar produto: {e}")

    driver.quit()
