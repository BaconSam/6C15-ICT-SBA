from functionsGUI import *
import csv, json
import PySimpleGUI as sg

def main():
    sg.theme('Dark2')

    layout = [[sg.Text('Input Student\'s Info here')],
            [sg.T('Name'), sg.Input(key= '-NAME-', do_not_clear = False)],
            [sg.T('Class'), sg.Input(key= '-CLASS-', enable_events=True, size = (10)), sg.Push(), sg.T('Class Number'), sg.Input(key= '-CNUM-', enable_events=True, size = (10))],
            [sg.T('House'), sg.Combo(['Red', 'Green','Blue','Yellow'], key ='-HOUSE-',  default_value = 'Red', tooltip = ' The House of the student ')],
            [sg.Checkbox('Seed Player?', key= '-SEED-', default=False, tooltip = ' Is the student the best 4 student from last year? ')],
            [sg.Button('Read', key = '-Read-'), sg.Exit()]]

    window = sg.Window('Badminton Matchmaking Generator Indev', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == '-CLASS-' and values['-CLASS-']:
            if values['-CLASS-'][-1] not in ('123456abcdABCD') or len(values['-CLASS-']) >= 3:
                window['-CLASS-'].update(values['-CLASS-'][:-1])
        
        if event == '-CNUM-' and values['-CNUM-'] :
            if values['-CNUM-'][-1] not in ('0123456789') or len(values['-CNUM-']) >= 3:
                window['-CNUM-'].update(values['-CNUM-'][:-1])
        
        print(event, values)

    window.close()

if __name__ == "__main__":
    main()