import PySimpleGUI as sg
import pandas as pd
import numpy as np


def InitCSV():
    df_tmp = pd.read_csv('data/temp.csv')
    if not df_tmp.empty:
        df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', 'CNUM', '-HOUSE-', '-SEED-'])
        df_tmp.to_csv('data/temp.csv', index = False)
    else:
      print("Initialization failed\nContent in temp.csv is not cleared")
      sg.popup_error("Initialization failed\nContent in temp.csv is not cleared")
    return df_tmp



#define suitable class
ClassList = ['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', '3A', '3B', '3C', '3D', '4A', '4B', '4C', '4D', '5A', '5B', '5C', '5D', '6A', '6B', '6C', '6D']

def Validation(event, values,df):
  err_message = ''

  if values['-NAME-'] != '':
    if any(char.isdigit() for char in values['-NAME-']):
      err_message += 'Name should not contain any numbers. \n'
  else:
    err_message += 'Name field should not be empty. \n'
  
  # if event == '-CLASS-' and values['-CLASS-']:
  if values['-CLASS-'] != '':
    if values['-CLASS-'].upper() not in ClassList:
      err_message += 'Class field contains unrelated characters. \n'
    if len(values['-CLASS-']) != 2:
      err_message += 'Class field should be only 2 characters. \n'
  else:
    err_message += 'Class field should not be empty. \n'

  # if event == '-CNUM-' and values['-CNUM-']:
  if values['-CNUM-'] != '':
    try:
      if int(values['-CNUM-']) <= 0:
          err_message += 'Class Number should be greater than zero. \n'
    except:
      err_message += 'Class Number should be a number. \n'
    
    if len(values['-CNUM-']) > 2:
        err_message += 'Class Number should be fewer than 2 characters. \n'
  else:
    err_message += 'Class Number field should not be empty. \n'

  #check if max 4 students from each house, max 4 seed
  num_house = df[df['-HOUSE-'] == str(values['-HOUSE-'])].shape[0]
  if num_house >= 4:
    err_message += 'The maximum number of students from one house is 4. \n'
  if values['-SEED-'] == True:
    num_seed = df[df['-SEED-'] == True].shape[0]
    if num_seed >= 4:
      err_message += 'The maximum number of seed players is 4. \n'
  

  if err_message != '':
    sg.popup_error(err_message)
    print('popup \n' + err_message)
  return err_message



  