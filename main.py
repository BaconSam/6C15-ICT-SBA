from functionsGUI import *
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
    menu_def = [['&File', ['&Open(O)', '&Save(S)', '&New(N)', 'E&xit(X)']],
                ['&Edit', ['&Delete row(D)','&Generate(G)']],
                ['&Help', ['&About...']] ]

    # input layout
    layout = [
            [sg.Text('Input Student\'s Info here')],
            [sg.T('Name'), sg.Input(key= '-NAME-')],
            [sg.T('Class'), sg.Input(key= '-CLASS-', size = (10)), sg.Push(), sg.T('Class Number'), sg.Input(key= '-CNUM-', size = (10))],
            [sg.T('House'), sg.Combo(['Red', 'Green','Blue','Yellow'], key ='-HOUSE-',  default_value = 'Red', tooltip = ' The House of the student ')],
            [sg.Checkbox('Seed Player?', key= '-SEED-', default=False, tooltip = ' Is the student the best 4 student from last year? ')],
            [sg.Button('Read', key = '-READ-'), sg.Exit(), sg.Push(), sg.Button('Generate', key = '-GEN-')]]
    
    # https://stackoverflow.com/questions/66479847/making-a-table-with-pysimplegui-and-pandas
    headers = {'    NAME    ':[], 'CLASS':[], 'C. NUM':[], 'HOUSE':[], 'SEED':[]}
    headings = list(headers)
    CSValues = df_tmp.values.tolist()


    Dtable =  [
              [sg.Table(values = CSValues, headings = headings,
              # Set column widths for empty record of table
              auto_size_columns=False,
              col_widths=list(map(lambda x:len(x)+1, headings)),
              key='-TABLE-',
              alternating_row_color='lightyellow',
              enable_click_events=True)]]

    # Start Window
    final = [
            [sg.MenubarCustom(menu_def, pad=(0,0), k='-CUST MENUBAR-')],
            [sg.Col(layout, p=0), sg.Col(Dtable, p=0)]
            ]
    window = sg.Window('Badminton Matchmaking Generator Indev', final, return_keyboard_events=True)

    # Check & Write Data
    selected_row = None
    while True:
      event, values = window.read()
      
      if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Exit(E)':
          if not df_tmp.empty:
            if sg.popup_ok_cancel('Do you want to save your progress?') == 'OK':
              df_tmp.to_csv('data/temp.csv', index = False)
            else:
              df_tmp = pd.DataFrame(columns = ['-NAME-', '-CLASS-', '-CNUM-', '-HOUSE-', '-SEED-'])
              df_tmp.to_csv('data/temp.csv', index = False)

          break
      
      if event == '-READ-':
        err_message = Validation(event, values, df_tmp)
          #sad
        if err_message == '':
          values['-NAME-'] = values['-NAME-'].title()
          values['-CLASS-'] = values['-CLASS-'].upper()
          append = pd.Series(values, index=["-NAME-","-CLASS-","-CNUM-","-HOUSE-","-SEED-"])
          print(str(append))
          df_tmp = pd.concat([df_tmp, append.to_frame().T], ignore_index=True)
          print(df_tmp.head())
          CSValues = df_tmp.values.tolist()
          window['-TABLE-'].update(values=CSValues)
          
      if isinstance(event, tuple):
        if event[2][0] != -1:
          selected_row = event[2][0]
        elif event[2][0] == None:
          sg.popup_error('No row was selected')
      else:
        df_tmp = Menu_Fn(window,event,df_tmp,selected_row)
        if selected_row != None:
          selected_row = str(int(selected_row) -1)
      
      
      

      print(event, values)

    # Exit
    window.close()

if __name__ == "__main__":
    main()