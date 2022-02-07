
import xlsxwriter
import csv
import openpyxl
import numpy as np
from datetime import datetime
import pandas as pd
import os


bbva_credit_directory = os.path.join("Account-statements","BBVA-Credit")
bbva_debit_directory = os.path.join("Account-statements","BBVA-Debit")


if len(os.listdir(bbva_debit_directory)) == 0:
  print("Theres no files in folder!")
else:
  for item in os.listdir(bbva_debit_directory):
    print(item)

  for item in os.listdir(bbva_debit_directory):
    print(item)





#dfs = pd.read_excel(, sheet_name=None)