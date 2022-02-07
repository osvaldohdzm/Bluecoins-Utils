
import xlsxwriter
import csv
import openpyxl
import numpy as np
from datetime import datetime
import pandas as pd
import os
from datetime import timedelta

pd.options.mode.chained_assignment = None 

bbva_credit_directory = os.path.join("Account-statements","BBVA-Credit")
bbva_debit_directory = os.path.join("Account-statements","BBVA-Debit")

bbva_debit_files = []

if len(os.listdir(bbva_debit_directory)) == 0:
  print("Theres no files in folder!")
else:
  for item in os.listdir(bbva_debit_directory):
    if item.endswith('.xlsx'):
      bbva_debit_files.append(item)
  print(bbva_debit_files)

bbva_debit_file_path = os.path.join("Account-statements","BBVA-Debit",bbva_debit_files[0])

#main_dataframe = pd.DataFrame(columns=['(1)Type','(2)Date','(3)Item or Payee','(4)Amount','(5)Parent Category','(6)Category','(7)Account Type','(8)Account','(9)Notes','(10) Label','(11) Status','(12) Split'])
columns_names = ['(1)Type','(2)Date','(3)Item or Payee','(4)Amount','(5)Parent Category','(6)Category','(7)Account Type','(8)Account','(9)Notes','(10) Label','(11) Status','(12) Split']
sheet_dataframe = pd.read_excel(bbva_debit_file_path, sheet_name=0, header=None)
for newcol in columns_names:
    sheet_dataframe[newcol]= None


sheet_dataframe.drop(sheet_dataframe.tail(2).index,inplace=True) # drop last n rows
sheet_dataframe = sheet_dataframe.iloc[4: , :]
sheet_dataframe[2] = sheet_dataframe[2].str.replace(',', '').astype(float)
sheet_dataframe[3] = sheet_dataframe[3].str.replace(',', '').astype(float)
sheet_dataframe[2] = sheet_dataframe[2].fillna(0)
sheet_dataframe[3] = sheet_dataframe[3].fillna(0)
sheet_dataframe[4] = sheet_dataframe[4].str.replace(',', '').astype(float)
sheet_dataframe[4] = sheet_dataframe[4].fillna(0)
sheet_dataframe['(4)Amount'] = sheet_dataframe[2]+sheet_dataframe[3]
sheet_dataframe['(1)Type'] = np.where(sheet_dataframe['(4)Amount'] > 0,  "i", "e")
sheet_dataframe['(2)Date'] = sheet_dataframe[0]
sheet_dataframe['(3)Item or Payee'] = sheet_dataframe[1]
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('SUBURBIA|SEARS|CCP|STEREN'), '(5)Parent Category'] = 'COMPRAS'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('SUBURBIA|SEARS|CCP|STEREN'), '(6)Category'] = 'COMPRAS'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('CEREAL|ADYENMX|ADYENMEX|WAFFLES|DIDI RIDES'), '(5)Parent Category'] = 'COMIDA'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('CEREAL|ADYENMX|ADYENMEX|WAFFLES|DIDI RIDES'), '(6)Category'] = 'COMIDA'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('UBER|DIDI MX'), '(5)Parent Category'] = 'TRANSPORTE'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('UBER|DIDI MX'), '(6)Category'] = 'TRANSPORTE'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('PARCO'), '(5)Parent Category'] = 'ESTACIONAMIENTO'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('PARCO'), '(6)Category'] = 'ESTACIONAMIENTO'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('PAGO CUENTA DE TERCERO|PAGO TARJETA DE CREDITO'), '(5)Parent Category'] = 'PAGO TARJETA DE CREDITO'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('PAGO CUENTA DE TERCERO|PAGO TARJETA DE CREDITO'), '(6)Category'] = 'PAGO TARJETA DE CREDITO'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('SPEI ENVIADO'), '(5)Parent Category'] = 'COMPRAS'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('SPEI ENVIADO'), '(6)Category'] = 'TRANSFERENCIA'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('RETIRO SIN TARJETA'), '(5)Parent Category'] = 'RETIRO'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('RETIRO SIN TARJETA'), '(6)Category'] = 'EFECTIVO'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('SPEI RECIBIDO|DEPOSITO EFECTIVO PRACTI'), '(5)Parent Category'] = 'HONORARIOS'
sheet_dataframe.loc[sheet_dataframe['(3)Item or Payee'].str.contains('SPEI RECIBIDO|DEPOSITO EFECTIVO PRACTI'), '(6)Category'] = 'HONORARIOS TRABAJO'
sheet_dataframe['(5)Parent Category'].replace(to_replace=[None], value="OTRAS COMPRAS", inplace=True)
sheet_dataframe['(6)Category'].replace(to_replace=[None], value="OTRAS COMPRAS", inplace=True)
sheet_dataframe['(7)Account Type'] = 'BANK'

first_row = sheet_dataframe.iloc[-1,:]
sheet_dataframe = sheet_dataframe.append(first_row, ignore_index=True)
sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(1)Type')] = "i"
sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(3)Item or Payee')]= "SALDO INICIAL"
sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(4)Amount')] =  sheet_dataframe.iloc[-2,3] - sheet_dataframe.iloc[-2,2] + sheet_dataframe.iloc[-2,4] 
sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(5)Parent Category')]= "HONORARIOS"
sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(6)Category')]= "PROYECTOS"

current_date_string =  sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(2)Date')]
current_date_temp = datetime.strptime(current_date_string , "%d/%m/%Y")
newdate = current_date_temp + timedelta(days=-1)
sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(2)Date')]= newdate.strftime('%d/%m/%Y')


#sheet_dataframe.iloc[-1, sheet_dataframe.columns.get_loc('(2)Date')]= date_str + datetime.timedelta(days=1)

#sheet_dataframe['(1)Type'][-1] = "i"
#sheet_dataframe['(3)Item or Payee'][-1] = "SALDO INICIAL"
#sheet_dataframe['(4)Amount'][-1] = sheet_dataframe[3][-1] - sheet_dataframe[2][-1] + sheet_dataframe[4][-1] 

sheet_dataframe.replace(to_replace=[None], value="", inplace=True)
sheet_dataframe['(4)Amount'] = sheet_dataframe['(4)Amount'].abs()
sheet_dataframe = sheet_dataframe.drop([0,1,2,3,4], axis = 1)
sheet_dataframe['(8)Account'] = "BBVA"

sheet_dataframe = sheet_dataframe.reset_index(drop=True)

#print(len(sheet_dataframe.columns))
#print(len(columns_names))
#while len(columns_names) >len(sheet_dataframe.columns):
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
print(sheet_dataframe)

sheet_dataframe.to_csv('BlueCoins {}.csv'.format(datetime.today().strftime('%Y-%m-%d')), index=False)


print(str())
#df["D"] = np.nan
#print(bbva_debit_file_path)
#dfs = pd.read_excel(bbva_debit_file_path, sheet_name=0)
#dfs.columns =['(1)Type','(2)Date','(3)Item or Payee','(4)Amount','(5)Parent Category','(6)Category','(7)Account Type','(8)Account','(9)Notes','(10) Label','(11) Status','(12) Split']
#print(type(main_dataframe))
#print(type(sheet_dataframe))
#print(sheet_dataframe)



#dfs = pd.read_excel(, sheet_name=None)