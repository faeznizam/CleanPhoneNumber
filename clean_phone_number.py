# import
import pandas as pd
import datetime
import re

# function
def process_mobile_numbers(df):
  # set data type to string
  df['Mobile'] = df['Mobile'].astype(str)

  # remove empty space and hyphens
  df['Mobile'] = df['Mobile'].str.replace(r'[ +\-]', '', regex=True)

  # handle numbers starting with 60, 060, 600, 06001, 001, 1, 65
  df['Updated Mobile'] = df['Mobile'].apply(lambda x: process_prefix(x))

  # add 0 in front of the startswith 1 and lenght 9 and 10
  df['Updated Mobile'] = df['Updated Mobile'].apply(lambda x: '0' + x if x.startswith('1') and len(x) in {9, 10} else x)

  # add a hyphen after the 3rd digit for number startswith 0 and add hyphen after 2nd digit for number startwith 65
  df['Updated Mobile'] = df['Updated Mobile'].apply(lambda x: x[:3] + '-' + x[3:] if x.startswith('0') else (x[:2] + '-' + x[2:] if x.startswith('65') else x))
  
  return df

def process_prefix(x):
  if x.startswith('601'):
    return x[2:]
  elif x.startswith('0601'):
    return x[3:]
  elif x.startswith('61'):
    return x[1:]
  elif x.startswith('6001'):
    return x[3:]
  elif x.startswith('06001'):
    return x[4:]
  elif x.startswith('001'):
    return x[2:]
  elif x.startswith('0001'):
    return x[3:]
  elif x.startswith('1') and len(x) in {9,10}:
    return x
  elif x.startswith('65'):
    return x
  else:
    return ''

# input file path - change the file path accordingly
folder_path = r'c:\Users\mfmohammad\OneDrive - UNICEF\Desktop\Data Cleaning\Dec\27 Dec'
file_name = 'Donor With Invalid Phone Number.xlsx'
full_path = f'{folder_path}/{file_name}'

# read file
df = pd.read_excel(full_path)
df = process_mobile_numbers(df)

# output file
# Rename the output file
new_file_name = "Donor With Invalid Phone Number - Edited.xlsx"
new_full_path = f'{folder_path}/{new_file_name}'

# Save the file
df.to_excel(new_full_path, index=False)

print(f'Excel file cleaned and saved as {new_file_name} successfully')