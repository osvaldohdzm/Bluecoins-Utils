
import xlsxwriter
import csv
import openpyxl
import numpy as np
from datetime import datetime

with open('bbvad-tsns-'+ datetime.today().strftime('%Y-%m-%d') + '.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(['John Smith', 'Accounting', 'November'])
    employee_writer.writerow(['Erica Meyers', 'IT', 'March'])

# Open Workbook
wb = openpyxl.load_workbook(filename='bbva-as-2021-05-05.xlsx', data_only=True)

o_sheet = wb['Movimientos']

start_row = 5
i = 0
o_cell = o_sheet['A5']
while o_cell.value is not None:
  print(o_cell.value)
  i += 1
  o_cell = o_sheet['A'+str(start_row + i)]

print("Celda de inicial y final de datos: " + 'A'+str(start_row)+ " then " + 'A' + str(start_row+i-1))

data_rows = []
for row in o_sheet['A'+str(start_row) :'E'+str(start_row+i-1)]:
    data_cols = []
    for cell in row:
        if cell.value:
            data_cols.append(cell.value)
        else:
            data_cols.append(0)
    data_rows.append(data_cols)

# Transform into dataframe
import pandas as pd

df = pd.DataFrame(data_rows)
cols = [2, 3, 4]
df[cols] = df[cols].apply(lambda x: pd.to_numeric(x.astype(str)
                                                   .str.replace(',',''), errors='coerce'))

df[5] = np.where(df[2] == 0, 'i', np.where(df[2] < 0, 'e',"-"))
df[0] = pd.to_datetime(df[0], dayfirst=True)
df[0] = df[0].dt.strftime('%d/%m/%Y')


# Amount for transaction
df[6] = df[3] - df[2]
df[7] = "-"
df[8] = "-"
df[9] = "-"
df[10] = "-"
# Order by date
df = df.sort_values(by=0)

# Entradas

df.loc[df[1].str.contains('SPEI RECIBIDOSANTANDER'), 5] = 't'
df.loc[df[1].str.contains('SPEI RECIBIDOSANTANDER'), 7] = '(Transferencia)'
df.loc[df[1].str.contains('SPEI RECIBIDOSANTANDER'), 8] = '(Transferencia)'

# print(df.iloc[2]['price'])
# df=df.append({1 : 'Apple' , 2 : 23, 3 : 'No'} , ignore_index=True)


df.loc[df[1].str.contains('SPEI RECIBIDOACTINVER'), 5] = 't'
df.loc[df[1].str.contains('SPEI RECIBIDOACTINVER'), 7] = '(Transferencia)'
df.loc[df[1].str.contains('SPEI RECIBIDOACTINVER'), 8] = '(Transferencia)'


df.loc[df[1].str.contains('DEPOSITO EN EFECTIVO'), 5] = 't'
df.loc[df[1].str.contains('DEPOSITO EN EFECTIVO'), 7] ='(Transferencia)'
df.loc[df[1].str.contains('DEPOSITO EN EFECTIVO'), 8] ='(Transferencia)'



# Salidas

df.loc[df[1].str.contains('RETIRO CAJERO AUTOMATICO'), 5] = 't'
df.loc[df[1].str.contains('RETIRO CAJERO AUTOMATICO'), 7] = '(Transferencia)'
df.loc[df[1].str.contains('RETIRO CAJERO AUTOMATICO'), 8] = '(Transferencia)'
df.loc[df[1].str.contains('RETIRO CAJERO AUTOMATICO'), 9] = 'Cash'
df.loc[df[1].str.contains('RETIRO CAJERO AUTOMATICO'), 10] = 'Cartera'


df.loc[df[1].str.contains('SPEI ENVIADO ACTINVER'), 5] = 't'
df.loc[df[1].str.contains('SPEI ENVIADO ACTINVER'), 7] = '(Transferencia)'
df.loc[df[1].str.contains('SPEI ENVIADO ACTINVER'), 8] = '(Transferencia)'
df.loc[df[1].str.contains('SPEI ENVIADO ACTINVER'), 9] = 'Bank'
df.loc[df[1].str.contains('SPEI ENVIADO ACTINVER'), 10] = 'Inversion DINN'

df.loc[df[1].str.contains('SPEI ENVIADO SANTANDER'), 5] = 't'
df.loc[df[1].str.contains('SPEI ENVIADO SANTANDER'), 7] ='(Transferencia)'
df.loc[df[1].str.contains('SPEI ENVIADO SANTANDER'), 8] ='(Transferencia)'
df.loc[df[1].str.contains('SPEI ENVIADO SANTANDER'), 9] ='Bank'
df.loc[df[1].str.contains('SPEI ENVIADO SANTANDER'), 10] ='Gastos SANTANDER'


#df.loc[df[1].str.contains('SUBURBIA | SEARS'), 7] = 'Compras'
df.loc[df[1].str.contains('SUBURBIA|SEARS|CCP|STEREN'), 8] = 'Compras'
df.loc[df[1].str.contains('SUBURBIA|SEARS|CCP|STEREN'), 9] ='Bank'
df.loc[df[1].str.contains('SUBURBIA|SEARS|CCP|STEREN'), 10] ='Ingresos BBVA'

df.loc[df[1].str.contains('CEREAL|ADYENMX|ADYENMEX'), 8] = 'Comida'
df.loc[df[1].str.contains('CEREAL|ADYENMX|ADYENMEX'), 9] = 'Bank'
df.loc[df[1].str.contains('CEREAL|ADYENMX|ADYENMEX'), 10] = 'Ingresos BBVA'


df.loc[df[7] == '-' , 7] ='Otro'
df.loc[df[8] == '-' , 8] ='Otro'
df.loc[df[9] == '-' , 9] ='Bank'
df.loc[df[10] == '-' , 10] ='Ingresos BBVA'



nf = df.loc[df[5] == 't']
# Negative numbers
nf[6] *= -1

nf[9] = 'Bank'
nf[10] = 'Ingresos BBVA'

nf.loc[nf[1].str.contains('SPEI RECIBIDOSANTANDER'), 9] = 'Bank'
nf.loc[nf[1].str.contains('SPEI RECIBIDOSANTANDER'), 10] = 'Gastos SANTANDER'
nf.loc[nf[1].str.contains('DEPOSITO EN EFECTIVO'), 9] ='Cash'
nf.loc[nf[1].str.contains('DEPOSITO EN EFECTIVO'), 10] = 'Cartera'
nf.loc[nf[1].str.contains('SPEI RECIBIDOACTINVER'), 9] = 'Bank'
nf.loc[nf[1].str.contains('SPEI RECIBIDOACTINVER'), 10] = 'Inversion DINN'


df = df.append(nf)

# Order by two columns
df = df.sort_values([0,1,6], ascending = (True, True, True))


df = df[[5, 0, 1, 6,7,8,9,10]]

df.to_csv(r'Name.csv')

print(df)