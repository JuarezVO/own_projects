import pickle, sys, re
from time import sleep
from bs4 import BeautifulSoup as bs
from requests import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# busca_id="downshift-0-input" 
# botao_sim ="emporiodacerveja-emporio-theme-3-x-ageGateButton"

# # Define as caracteristicas do browser, neste caso, não vai abrir.
# driver_exe = 'D:\jupyter\chromedriver'
# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Chrome(driver_exe,options=options)

# # Navega no link até chegar no resultado da busca
# link1 = 'https://www.emporiodacerveja.com.br/'
# driver.get(link1)
# driver.implicitly_wait(10)
# driver.find_element(by=By.CLASS_NAME,value=botao_sim).click()
# driver.implicitly_wait(10)
# driver.find_element(by=By.CLASS_NAME,value=botao_sim).click()
# driver.implicitly_wait(10)
# driver.find_element(by=By.ID,value=busca_id).send_keys('cerveja bohemia\n')
# sleep(5)
# busca = driver.page_source

# # Com o resultado da busca, organiza os itens de interesse
# soup = bs(busca,'lxml')
# descricao = soup.find_all('span',class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')
# valor_int = soup.find_all('span',class_="vtex-product-summary-2-x-currencyInteger")
# valor_dec = soup.find_all('span',class_="vtex-product-summary-2-x-currencyFraction")

# sys.setrecursionlimit(10000)
# produto = zip(descricao, valor_int, valor_dec)
# pickle.dump(produto,open('produtos.pkl','wb'))

produto = pickle.load(open('produtos.pkl','rb'))
for descricao,valor_int,valor_dec in produto:
    descricao = str(descricao).split('>')[len(descricao)].split('<')[0]
    ml_unidade = int(re.findall(r'\d+',descricao)[0])
    unidades = int(re.findall(r'\d+',descricao)[1])
    

    valor_int = int(str(valor_int).split('</span>')[0].split('>')[-1])
    valor_dec = int(str(valor_dec).split('</span>')[0].split('>')[-1])
    valor = float(f'{valor_int}.{valor_dec}')

    valor_ml = f'{round((ml_unidade*unidades)/valor,2)}ml/R$'
    print(descricao,valor_ml)
    # quit()

# ids = driver.find_elements_by_xpath('//*[@id]')
# for i in ids:
#     print(i.get_attribute('placeholder'),i.tag_name,i.get_attribute('id'))