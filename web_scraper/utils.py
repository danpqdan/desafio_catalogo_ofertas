import re
from selenium import webdriver
import selenium.webdriver as wb
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import urllib.parse
from .models import Produto

URL_MERCADO_LIVRE = "https://lista.mercadolivre.com.br/"

def iniciar_driver():
    options = wb.FirefoxOptions()
    options.add_argument("--disable-gpu")  # Desabilitar GPU
    options.add_argument("--headless")  #  Não carrega UI
    return webdriver.Firefox(options=options)

def buscar_mercado_livre():
    driver = iniciar_driver()
    actions = ActionChains(driver)
    campo_busca = 'Computador Gamer i7 16gb ssd 1tb'
    campo_busca_variavel = campo_busca.replace(" ", "-")
    campo_busca_parse_sem_espaco = urllib.parse.quote(campo_busca_variavel)
    campo_busca_parse_com_espaco = urllib.parse.quote(campo_busca)
    print(f"URL carregado: {URL_MERCADO_LIVRE + campo_busca_parse_sem_espaco + '#D[A:' + campo_busca + ']'}")
    driver.get(URL_MERCADO_LIVRE + campo_busca_parse_sem_espaco + "#D[A:" + campo_busca + "]")

    # hrefs = driver.find_elements(By.XPATH, "//a[contains(@class, 'poly-component__title')]")
    # produtos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-layout__item")
    
    produtos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-layout.ui-search-layout--grid li")
    
    for index, produto in enumerate(produtos[:10]):
        try:
            nome = produto.find_element(By.XPATH, ".//h3/a").text
            link = produto.find_element(By.XPATH, "//a[contains(@class, 'poly-component__title')]").get_attribute('href')
            # link = hrefs[index].get_attribute('href')
            preco = produto.find_element(By.CSS_SELECTOR, ".poly-price__current .andes-money-amount__fraction").text
            preco = float(preco.replace('.', '').replace(',', '.'))
            div_portada = produto.find_element(By.CLASS_NAME, "poly-card__portada")


            # Passar o mouse sobre o botão
            actions.move_to_element(div_portada).perform()

            # Ajuste o XPath para encontrar todas as imagens do produto
            carousel = div_portada.find_element(By.CLASS_NAME, "andes-carousel-snapped__wrapper")
            imagens = carousel.find_elements(By.TAG_NAME, "img")
            image_urls = [img.get_attribute("src") for img in imagens]

            # Exibir os links das imagens
            for i, url in enumerate(image_urls, 1):
                print(f"Imagem {i}: {url}")

            try:
                preco_sem_desconto = produto.find_element(By.CSS_SELECTOR, '.andes-money-amount__fraction').text
                preco_sem_desconto = float(preco_sem_desconto.replace('.', '').replace(',', '.'))
                percentual_desconto = round((1 - (preco / preco_sem_desconto)) * 100, 2)
            except:
                preco_sem_desconto = None
                percentual_desconto = None
            try:
                # tipo_entrega = produto.find_element(By.CSS_SELECTOR, "span.poly-component__shipped-from")         try:
                # print(parcelamento)
                parcelamento = produto.find_element(By.XPATH, "//span[@class='poly-price__installments']").text
                
                
                shipping_element = produto.find_element(By.CSS_SELECTOR, '.poly-component__shipping')
                shipping_element_from = produto.find_element(By.CSS_SELECTOR, '.poly-component__shipped-from')
                shipping_element_additional_text = produto.find_element(By.CSS_SELECTOR, '.poly-shipping__additional_text')

                # Verifica se o texto "Chegará grátis amanhã" ou "por ser sua primeira compra" está presente
                if "Frete grátis" in shipping_element.text:
                    frete_gratis = 'Sim'
                    if "por ser sua primeira compra" in shipping_element_additional_text:
                        frete_gratis = 'Sim/Nao'  # Se ambos os textos estiverem presentes
                    elif "Enviado pelo" in shipping_element_from:
                        tipo_entrega = 'Full' # Caso o texto "Enviado pelo" seja encontrado
                else:
                    tipo_entrega = 'Padrao'  # Caso o "Frete grátis" não esteja presente
                    frete_gratis = 'Nao'  # Define que não é frete grátis

            except:
                tipo_entrega = "Padrao"
                frete_gratis = "Nao"
            
            
            for i in range(10):
                print(
                nome=nome,
                # imagem=imagens_formatada,  # Aqui você pode salvar as URLs das imagens
                preco=preco,
                preco_sem_desconto=preco_sem_desconto,
                percentual_desconto=percentual_desconto,
                parcelamento=parcelamento,
                link=link,
                tipo_entrega=tipo_entrega,
                frete_gratis=frete_gratis    
                )


            # Criando o produto no banco de dados
            Produto.objects.create(
                nome=nome,
                # imagem=imagens_formatada,  # Aqui você pode salvar as URLs das imagens
                preco=preco,
                preco_sem_desconto=preco_sem_desconto,
                percentual_desconto=percentual_desconto,
                parcelamento=parcelamento,
                link=link,
                tipo_entrega=tipo_entrega,
                frete_gratis=frete_gratis
            )
        
        except Exception as e:
            print(f"Erro ao processar produto: {e}")

    driver.quit()
