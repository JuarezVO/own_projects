# %%
import requests, pandas as pd, os, copy, mechanize, datetime as dt, numpy as np

# %% [markdown]
# ### Download dos dados do inmet

# %%
link = 'https://apitempo.inmet.gov.br/estacao/2021-01-01/2021-12-31/A201'
resp = requests.get(link)
if resp.status_code == 200:
   dados = pd.DataFrame.from_records(resp.json())
   dados = dados[['CHUVA','DT_MEDICAO','HR_MEDICAO']]
   dados['date'] = pd.to_datetime(dados['DT_MEDICAO'] + dados['HR_MEDICAO'],format='%Y-%m-%d%H%M')
   dados = dados.rename(columns={'CHUVA':'chuva'}).drop(['DT_MEDICAO','HR_MEDICAO'],axis=1)
   dados = dados.dropna()
   dados.to_csv('inmet_belem.csv',index=False)

# %% [markdown]
# ### Carrega os dados do inmet e seleciona n_imgs aleatoriamente

# %%
dados = pd.read_csv('org_1028_equip_898_hly.csv')
dados['prp_lag_1'] = dados['pl1'].shift(-1)

n_imgs = 432
com_prp = copy.deepcopy(dados[dados['prp_lag_1']>=1].sample(n=n_imgs,random_state=42))
sem_prp = copy.deepcopy(dados[dados['prp_lag_1']<1].sample(n=n_imgs,random_state=42))

# %% [markdown]
# ### Baixa a imagem de satelite correspondente a cada datetime de cada grupo (com/sem_prp)

# %%
ni = 0
for info in sem_prp.iterrows():
  dtime = dt.datetime.strptime(info[1]['measured_at'],'%Y-%m-%d %H:%M:%S')
  homepage="http://satelite.cptec.inpe.br/acervo/goes16.formulario.logic"
  br = mechanize.Browser()
  br.open(homepage)
  br.select_form('form')
  form_date = br.form.find_control(name='dtConsulta')
  form_date.value = dtime.strftime('%Y-%m-%d')
  br.submit()
  links = [i.url for i in br.links() if '.jpg' in i.url and 'ch16' in i.url]
  links_date = [(dt.datetime.strptime(i.split('_')[-1].split('.jpg')[0],'%Y%m%d%H%M') - dtime).seconds for i in links]
  url = links[np.argmin(links_date)]
  os.system(f'wget -q -P chapadão/sem_prp/ {url}')
  ni += 1
  print(f'Baixou {ni}/{n_imgs}, {dtime}')

# %%



