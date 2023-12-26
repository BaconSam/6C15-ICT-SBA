from functionsGUI import *
import csv, json
import PySimpleGUI as sg
import pandas as pd
import numpy as np

# main
def main():
    # Define thme
    sg.theme('Dark2')

    # Initialization
    df_tmp = InitCSV('data/temp.csv')

    # menu layout
    menu_def = [['&File', ['&Open(O)', '&Save(S)', '&New(N)', 'E&xit(E)']],
                ['&Edit', ['Edit Me', 'Special', 'Normal',['Normal1', 'Normal2'] , 'Undo']],
                ['&Toolbar', ['---', 'Command &1::Command_Key', 'Command &2', '---', 'Command &3', 'Command &4']],
                ['&Help', ['&About...']] ]

    # input layout
    layout = [
            [sg.Text('Input Student\'s Info here')],
            [sg.T('Name'), sg.Input(key= '-NAME-')],
            [sg.T('Class'), sg.Input(key= '-CLASS-', size = (10)), sg.Push(), sg.T('Class Number'), sg.Input(key= '-CNUM-', size = (10))],
            [sg.T('House'), sg.Combo(['Red', 'Green','Blue','Yellow'], key ='-HOUSE-',  default_value = 'Red', tooltip = ' The House of the student ')],
            [sg.Checkbox('Seed Player?', key= '-SEED-', default=False, tooltip = ' Is the student the best 4 student from last year? ')],
            [sg.Button('Read', key = '-READ-'), sg.Exit()]]
    
    # https://stackoverflow.com/questions/66479847/making-a-table-with-pysimplegui-and-pandas
    headers = {'NAME':[], 'CLASS':[], 'C. NUM':[], 'HOUSE':[], 'SEED':[]}
    headings = list(headers)
    CSValues = df_tmp.values.tolist()


    Dtable =  [
              [sg.Table(values = CSValues, headings = headings,
              # Set column widths for empty record of table
              auto_size_columns=False,
              col_widths=list(map(lambda x:len(x)+1, headings)),
              key='-TABLE-')]
              ]

    # Start Window
    final = [
            [sg.MenubarCustom(menu_def, pad=(0,0), k='-CUST MENUBAR-')],
            [sg.Col(layout, p=0), sg.Col(Dtable, p=0)]
            ]
    window = sg.Window('Badminton Matchmaking Generator Indev', final)

    # Check & Write Data
    
    while True:
      event, values = window.read()
      
      if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Exit(E)':
          break
      
      if event == '-READ-':
        err_message = Validation(event, values, df_tmp)
          #sad
        if err_message == '':
          append = pd.Series(values, index=["-NAME-","-CLASS-","-CNUM-","-HOUSE-","-SEED-"])
          print(str(append))
          df_tmp = pd.concat([df_tmp, append.to_frame().T], ignore_index=True)
          print(df_tmp.head())
          CSValues = df_tmp.values.tolist()
          window['-TABLE-'].update(values=CSValues)
          
      MEvent = Menu_Fn(window,event,df_tmp)
      # match MEvent:
      #     case 'Open':
      #       window.close()
      #       break
            

      print(event, values)

    # Exit
    window.close()

if __name__ == "__main__":
    main()