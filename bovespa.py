#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from helper import *



connectTor()
#newidentity()


def parser(file_object,data_arquivo,hash):
    #if list(file_object.iloc[3:-1,0]) == [u'Tipos de', u'Investidores', u'Pessoa Física', u' - Inv Individuais', u' - Clubes de Inv', u'Institucional', u'Inves. Estrangeiro', u'Emp. Priv/Publ.', u'Instit. Financeiras',u'Outros']:
    if list(file_object.iloc[3:-1, 0]) == [u'Tipos de', u'Investidores', u'Pessoa Física' ,u' - Inv Individuais', u' - Clubes de Inv', u'Institucional', u'Inves. Estrangeiro', u'Empresas Públicas e Privadas', u'Instituições Finaceiras', u'Outros']:
        if file_object.iloc[3,1].strip().upper() == 'COMPRAS' and file_object.iloc[3,3].strip().upper() == 'VENDAS' and file_object.iloc[4,1].strip().upper() == 'R$ MIL' and file_object.iloc[4,3].strip().upper() == 'R$ MIL':
            compras = list(pd.read_excel(r"C:\Users\luiz\Desktop\temporarios\partdir_NOVOv2.xls",skiprows=5,usecols= range(1,5),dtype=str).iloc[0:8,0])
            vendas =  list(pd.read_excel(r"C:\Users\luiz\Desktop\temporarios\partdir_NOVOv2.xls",skiprows=5,usecols= range(1,5),dtype=str).iloc[0:8,2])
            tipos = [u'Pessoa Fisica', u'Inv Individuais', u'Clubes de Inv', u'Institucional', u'Inves. Estrangeiro', u'Emp. Priv/Publ.', u'Instit. Financeiras',u'Outros']
            for i in tipos:
                str_sql = "INSERT INTO bovespa (data,tipo,compravenda,financeiro,hash) values (%s,%s,%s,%s,%s)"
                cursor.execute(str_sql, (data_arquivo, str(i), 'C', compras[tipos.index(i)],hash))
                cursor.execute(str_sql, (data_arquivo, str(i), 'V', vendas[tipos.index(i)],hash))
            conn.commit()
        else:
            error("algum erro no 'subheader' do arquivo")
    else:
        error('algum erro no header do arquivo')




conn ,cursor,engine= conection("dados")
lista = contexto(cursor,"bovespa")



url = 'http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/participacao-dos-investidores/volume-total/'
r1 = requests.get(url)
soup = BeautifulSoup(r1.content, 'html.parser')
#e = soup.find_all('a',href='../../../../../../../../data/files/BF/27/E6/B2/E37D46101305DC46AC094EA8/partdir_NOVOv2.xls')[0]['href']
#e = soup.find_all('a',href='../../../../../../../../data/files/EE/A1/47/83/88AA8610B3B67986AC094EA8/__fscorpa_prod_TRANSFER_PROG_BDI_SI_partdir_NOVOv2.xls')[0]['href']
#e = soup.find_all('a',text="Volume total acumulado")[0]['href']
e = soup.find_all(href=re.compile(r'partdir_NOVOv2.xls'))[0]['href']

hash = e.split('../')[-1]
#print hash
url =  'http://www.b3.com.br/'+hash
r2 = requests.get(url, allow_redirects=True)
open(r"C:\Users\luiz\Desktop\temporarios\partdir_NOVOv2.xls", 'wb').write(r2.content)

file_object = pd.read_excel(r"C:\Users\luiz\Desktop\temporarios\partdir_NOVOv2.xls")
try:
    data_arquivo = '-'.join(file_object.iloc[1,0][-11:-1].split('/')[::-1])
    if data_arquivo not in lista:
        parser(file_object,data_arquivo,hash)
        with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'a') as checklist:
            checklist.writelines('bovespa\n')

except:
    error('algum erro do processo em geral')