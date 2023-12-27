import PySimpleGUI as sg
import pandas as pd
import numpy as np
import os
import math
import random


def InitCSV(pathname):
    if os.path.exists(pathname):
      try:
        df_tmp = pd.read_csv(pathname)
      except pd.errors.EmptyDataError:
        df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
        df_tmp.to_csv('data/temp.csv', index = False)
        return df_tmp

      if set(['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-']).issubset(df_tmp.columns):
        if not df_tmp.empty:
          if pathname == 'data/temp.csv':
            if sg.popup_ok_cancel('Work in progress detected.\nDo you want to resume?') == 'OK':
              df_tmp.to_csv('data/temp.csv', index = False)
              return df_tmp
            else:
              df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
              df_tmp.to_csv('data/temp.csv', index = False)
              return df_tmp
          else:
              df_tmp.to_csv('data/temp.csv', index = False)
              return df_tmp
        else:
            df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
            df_tmp.to_csv('data/temp.csv', index = False)
            return df_tmp
      else:
        df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
        df_tmp.to_csv('data/temp.csv', index = False)
    else:
      df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
      df_tmp.to_csv('data/temp.csv', index = False)
      return df_tmp



#define suitable class
ClassList = ['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', '3A', '3B', '3C', '3D', '4A', '4B', '4C', '4D', '5A', '5B', '5C', '5D', '6A', '6B', '6C', '6D']

def Validation(event, values,df):
  err_message = ''

  if values['-NAME-'] != '':
    if any(char.isdigit() for char in values['-NAME-']):
      err_message += 'Name should not contain any numbers. \n'
  elif values['-NAME-'] in ('bye','Bye'):
    err_message += 'Name "Bye" is not allowed. \n'
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


def clearInput(window):
   window['-NAME-']('')
   window['-CLASS-']('')
   window['-CNUM-']('')
   window['-HOUSE-']('Red')
   window['-SEED-'](False)
   


def Menu_Fn(window,event,df_tmp,row):
  if event == 'About...':
            window.disappear()
            sg.popup('About this program', 'This is a program for the Badminton Competition', 'NLSI LKPFC F6 ICT SBA','Ver 1.0',
                     'PySimpleGUI Version', sg.get_versions(),  grab_anywhere=True, keep_on_top=True)
            window.reappear()

  elif event.startswith('Open'):
            filename = sg.popup_get_file('file to open', no_window=True, file_types=(("CSV Files", "*.csv*"),))
            if filename:
              try:
                df_tmp = InitCSV(filename)
                CSValues = df_tmp.values.tolist()
                window['-TABLE-'].update(values=CSValues)
                return df_tmp
              except pd.errors.EmptyDataError:
                 sg.popup_error('Failed to open file.\nThe CSV is empty.')

  elif event.startswith('New'):
            if not df_tmp.empty:
              if sg.popup_ok_cancel('Will clear CSV in progress and Create new one.\nThis process can not be undone.') == 'OK':
                clearInput(window)
                df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
                df_tmp.to_csv('data/temp.csv', index = False)
                df_tmp = InitCSV('data/temp.csv')
                CSValues = df_tmp.values.tolist()
                window['-TABLE-'].update(values=CSValues)
                return df_tmp
              
  elif event.startswith('Save'):
            df_tmp.to_csv('data/temp.csv', index = False)
            return df_tmp
  elif event.startswith('Delete'):
      if row != None:
        if int(row) < 0:
          sg.popup_error('Reached the top of the table')
        else:
          print(row)
          df_tmp = df_tmp.drop(labels=int(row),axis=0)
          df_tmp = df_tmp.reset_index(drop=True)
          print(df_tmp.head(10))
          CSValues = df_tmp.values.tolist()
          window['-TABLE-'].update(values=CSValues)
      else:
         sg.popup_error('No row was selected.')
      return df_tmp
  else:
     return df_tmp
            

def Generate(df_tmp):
  df = df_tmp

  df_final = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
  while math.log(len(df),2)%1 != 0:
    dummy = pd.DataFrame({'-NAME-':['bye'],'-CLASS-':['None'],'-CNUM-':['None'],'-HOUSE-':['None'],'-SEED-':[False]})
    line = random.randrange(0,len(df))
    df = pd.concat([df.iloc[:line], dummy, df.iloc[line:]], ignore_index=True)

  while not df.empty:
    idx = len(df)-1
    begin = df.iloc[idx]
    df_final = pd.concat([df_final, begin.to_frame().T], ignore_index=True)

    df = df.drop(labels=idx,axis=0)
    df = df.reset_index(drop=True)
    print(begin['-HOUSE-'])
    for i in range(idx):
      if df.iloc[i, 3] != begin['-HOUSE-']:
        if df.iloc[i, 4] != begin['-SEED-']:
            df_final = pd.concat([df_final, df.iloc[i].to_frame().T], ignore_index=True)
            df = df.drop(labels=i,axis=0)
            df = df.reset_index(drop=True)
            break
  moveSeed = int(math.ceil(float(len(df_final[df_final["-SEED-"] == True]))/2)*2)
  for j in range(moveSeed):
    sad = [k for k in range(len(df_final)) if k != 0] + [0]
    df_final = df_final.iloc[sad].reset_index(drop=True)



  print(df_final)
  return df_final

def finalPopup(df_final, df_tmp):
    headers = {'    NAME    ': []}
    headings = list(headers)
    
    # Convert the values in the "-NAME-" column to a list, handling float values appropriately
    CSValues = df_final["-NAME-"].apply(lambda x: [x] if isinstance(x, float) else x).values.tolist()

    table = [
        [sg.Table(values=CSValues, headings=headings,
                  auto_size_columns=False,
                  col_widths=list(map(lambda x: len(x) + 1, headings)),
                  key='-PTABLE-',
                  alternating_row_color='gray')],
        [sg.T('*Only the position of "bye" will change while regenerating')],
        [sg.B('Confirm'), sg.B('Regenerate'), sg.B('Cancel')]
    ]
    Pwindow = sg.Window('POPUP', table, modal=True)

    while True:
        event, value = Pwindow.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        print(event)
        if event == 'Confirm':
            df_final[["-NAME-", "-CLASS-", "-HOUSE-"]].to_csv('output.csv', index=False)
            sg.popup('Output Successful\nCheck output.csv in the root folder.')
            break
        elif event == 'Cancel':
            break
        elif event == 'Regenerate':
            df_final = Generate(df_tmp)
            CSValues = df_final.values.tolist()
            Pwindow['-PTABLE-'].update(values=CSValues)

    Pwindow.close()