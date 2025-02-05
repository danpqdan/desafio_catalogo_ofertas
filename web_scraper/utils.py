import os
import time
import urllib.parse
import selenium.webdriver as wb
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from .models import ImagemProduto, Produto

URL_MERCADO_LIVRE = "https://lista.mercadolivre.com.br/"

load_dotenv()
navegador = os.getenv("BROWSER")

def escolher_navegador(browser):
    """ Inicia um driver Selenium compatível com Windows, macOS e Linux. """

    options = None

    if navegador.lower() == "firefox":
        options = wb.FirefoxOptions()
        options.add_argument("--headless")  # Modo sem interface gráfica
        service = FirefoxService(GeckoDriverManager().install())
        return wb.Firefox(service=service, options=options)

    elif navegador.lower() == "chrome":
        options = wb.ChromeOptions()
        options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        return wb.Chrome(service=service, options=options)

    elif navegador.lower() == "edge":
        options = wb.EdgeOptions()
        options.add_argument("--headless")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return wb.Edge(service=service, options=options)

    else:
        raise ValueError("Navegador não suportado. Use 'firefox', 'chrome' ou 'edge'.")


def buscar_mercado_livre(termo_busca):
    driver = escolher_navegador(browser=navegador)
    actions = ActionChains(driver)
    campo_busca_variavel = termo_busca.replace(" ", "-")
    campo_busca_parse_sem_espaco = urllib.parse.quote(campo_busca_variavel)
    print(f"URL carregado: {URL_MERCADO_LIVRE + campo_busca_parse_sem_espaco + '#D[A:' + termo_busca + ']'}")
    driver.get(URL_MERCADO_LIVRE + campo_busca_parse_sem_espaco + "#D[A:" + termo_busca + "]")
    time.sleep(4)    
    produtos = driver.find_elements(By.CSS_SELECTOR, ".ui-search-layout.ui-search-layout--grid li")
    
    for index, produto in enumerate(produtos):
        try:
            nome = produto.find_element(By.CSS_SELECTOR, ".poly-component__title").text
            link = produto.find_element(By.CSS_SELECTOR, ".poly-component__title").get_attribute('href')
            preco = produto.find_element(By.CSS_SELECTOR, ".poly-price__current .andes-money-amount__fraction").text
            preco = float(preco.replace('.', '').replace(',', '.'))
            div_portada = produto.find_element(By.CLASS_NAME, "poly-card__portada")
            div_portada = produto.find_element(By.CLASS_NAME, "poly-card__portada")
            driver.execute_script("arguments[0].scrollIntoView();", div_portada)
            actions.move_to_element(div_portada).perform()
            time.sleep(3)
            
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
                frete_gratis = "Frete grátis" in shipping_element or "Frete grátispor ser sua primeira compra" in shipping_element
                if "Enviado pelo" in tipo_entrega:
                    tipo_entrega = 'Full'
                if not frete_gratis and tipo_entrega != 'Full':
                    tipo_entrega = 'Padrao'
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

            for url_imagem in image_urls:
                ImagemProduto.objects.create(
                    produto=produto_model,
                    url_imagem=url_imagem
                )

        
        except Exception as e:
            print(f"Erro ao processar produto: {e}")

    driver.quit()
