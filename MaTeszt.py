from asyncio import windows_events
from genericpath import isfile
from os import TMP_MAX
import PySimpleGUI as sg
import random
import os
from time import strftime, time

def create_window(window_name, results):
    button_size = (4,2)
    num_pad = [
        [sg.Button('7', key = '-SEVEN-', visible = False, size = button_size), sg.Button('8', key = '-EIGHT-', visible = False, size = button_size), sg.Button('9', key = '-NINE-', visible = False, size = button_size)],
        [sg.Button('4', key = '-FOUR-', visible = False, size = button_size), sg.Button('5', key = '-FIVE-', visible = False, size = button_size), sg.Button('6', key = '-SIX-', visible = False, size = button_size)],
        [sg.Button('1', key = '-ONE-', visible = False, size = button_size), sg.Button('2', key = '-TWO-', visible = False, size = button_size), sg.Button('3', key = '-THREE-', visible = False, size = button_size)],
        [sg.Button('<-', key = '-BACKSPACE-', visible = False, size = button_size),sg.Button('0', key = '-ZERO-', visible = False, size = button_size),sg.Button('OK', key = '-SEND_ANSWER-', visible = False, size = button_size)]
    ]
    layout =[
        [
            sg.Text('Üdvözöllek! Kérlek add meg a neved!', key = '-FIRST_LINE-'), sg.InputText(key = '-NAME-', size = (10,15)),
            sg.Spin(['Könnyű', 'Közepes', 'Nehéz', 'Kegyetlen'], key = '-DIFFICULTY-', visible = False),
            sg.Button('OK', key = '-FIRST_BUTTON-'), sg.Button('OK', key = '-SECOND_BUTTON-', visible=False),
            sg.Text(f'0/0',key = '-COUNTER-', visible = False), sg.Text('', key = '-TIME-', visible = False)
        ],
        [sg.Text(key = '-QUESTION-', visible = False),sg.Text(key = '-SOLUTION-', visible = False, size = (5,1))],
        [sg.Column(num_pad), sg.Text('|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n', visible = False, key = '-SEPARATOR-'), sg.Text('Korábbi eredmények: \n' + results, visible = False, key = '-RESULTS-', font = 'Franklin 10'), sg.VPush()]
    ]

    return sg.Window(window_name, layout, size = (600,350))

def create_variables(lo,hi):
        a = random.randint(lo,hi)
        b = random.randint(lo,hi)
        arr = ['+', '-', '*', '/']
        jel = random.choice(arr)
        if b>a:
            a, b = b, a
        if jel == '/':
            a = a*b
            while a>hi:
                a = a-b
        return [a, b, jel]

def create_question(lo,hi):
        arr = create_variables(lo,hi)
        a = arr[0]
        b = arr[1]
        jel = arr[2]
        if jel == '+':
            result = a+b
        elif jel == '-':
            result = a-b
        elif jel == '*':
            result = a*b
        else:
            result = int(a/b)
        kerdes = f'{a} {jel} {b} = '
        return [kerdes, result]

def check_answer(ans, sol):
    if int(ans) == int(sol):
        return True
    return False

def update_file(nev, pont, nehezseg, ido):
    if os.path.isfile('res.txt') == False:
        fc = open('res.txt', 'w+')
        fc.close()
    f = open('res.txt', 'a')
    f.write(f'{nev} {nehezseg} szinten: {pont}%, {ido}sec\n')
    f.close()

def take_question(dif, window, index):
        global kerdes
        match dif:
                case 'Könnyű':
                    kerdes = create_question(1,10)
                    window['-QUESTION-'].update(f'{index}. kérdés: {kerdes[0]}')

                case 'Közepes':
                    kerdes = create_question(1,100)
                    window['-QUESTION-'].update(f'{index}. kérdés: {kerdes[0]}')

                case 'Nehéz':
                    kerdes = create_question(1,1000)
                    window['-QUESTION-'].update(f'{index}. kérdés: {kerdes[0]}')

                case 'Kegyetlen':
                    kerdes = create_question(1,10000)
                    window['-QUESTION-'].update(f'{index}. kérdés: {kerdes[0]}')

def display_results():
        if os.path.isfile('res.txt'):
            f = open('res.txt', 'r')
            sorok = f.readlines()
            result = ''
            count = 1
            for e in sorok[-10:]:
                result = result + e
                count+=1
            return result
        return ''

def main():
    sg.theme('dark')
    sg.set_options(font = 'Franklin 14')
    score = 0
    cnt = 0
    result = ''
    active = False
    start_time = 0
    eredmenyek = display_results()
    
    window = create_window('Mateszt', eredmenyek)
    while True:
        event, values = window.read(timeout = 10)
        if event == sg.WIN_CLOSED or event == '-CLOSE-':
            break
        
        if event == '-FIRST_BUTTON-':
            name = values['-NAME-']
            window['-FIRST_LINE-'].update('Válassz nehézséget ' + name +'! ')
            window['-NAME-'].update(visible = False)
            window['-FIRST_BUTTON-'].update(visible = False)
            window['-DIFFICULTY-'].update(visible = True)
            window['-SECOND_BUTTON-'].update(visible = True)
            
        if event == '-SECOND_BUTTON-':
            nehezseg = values['-DIFFICULTY-']
            take_question(nehezseg, window, cnt+1)
            window['-FIRST_LINE-'].update('Szurkolok ' + name + '!')
            window['-SECOND_BUTTON-'].update(visible=False)
            window['-DIFFICULTY-'].update(visible = False)
            window['-QUESTION-'].update(visible = True)
            window['-SOLUTION-'].update(visible = True)
            window['-COUNTER-'].update(visible = True)
            window['-ONE-'].update(visible = True)
            window['-TWO-'].update(visible = True)
            window['-THREE-'].update(visible = True)
            window['-FOUR-'].update(visible = True)
            window['-FIVE-'].update(visible = True)
            window['-SIX-'].update(visible = True)
            window['-SEVEN-'].update(visible = True)
            window['-EIGHT-'].update(visible = True)
            window['-NINE-'].update(visible = True)
            window['-BACKSPACE-'].update(visible = True)
            window['-ZERO-'].update(visible = True)
            window['-SEND_ANSWER-'].update(visible = True)
            window['-TIME-'].update(visible = True)
            start_time = time()
            active = True
        
        if active:
            elapsed_time = round(time() - start_time,1)
            window['-TIME-'].update(elapsed_time)
        
        if event == '-ZERO-':
            result = result + '0'
            window['-SOLUTION-'].update(result)
        
        if event == '-ONE-':
            result = result + '1'
            window['-SOLUTION-'].update(result)
            
        if event == '-TWO-':
            result = result + '2'
            window['-SOLUTION-'].update(result)
        
        if event == '-THREE-':
            result = result + '3'
            window['-SOLUTION-'].update(result)
        
        if event == '-FOUR-':
            result = result + '4'
            window['-SOLUTION-'].update(result)
            
        if event == '-FIVE-':
            result = result + '5'
            window['-SOLUTION-'].update(result)
            
        if event == '-SIX-':
            result = result + '6'
            window['-SOLUTION-'].update(result)
            
        if event == '-SEVEN-':
            result = result + '7'
            window['-SOLUTION-'].update(result)
            
        if event == '-EIGHT-':
            result = result + '8'
            window['-SOLUTION-'].update(result)
            
        if event == '-NINE-':
            result = result + '9'
            window['-SOLUTION-'].update(result)
            
        if event == '-BACKSPACE-':
            if len(result) != 0:
                result = result[:len(result)-1]
                window['-SOLUTION-'].update(result)
      
        if event == '-SEND_ANSWER-':
            if len(result) !=0:
                if (check_answer(result, kerdes[1])):
                    score += 1
                    cnt += 1
                else:
                    cnt +=1
                result = ''
                window['-SOLUTION-'].update(result)
                window['-COUNTER-'].update(f'{score}/{cnt}')
                take_question(nehezseg, window, cnt+1)
            
        if cnt == 10:
            window['-FIRST_LINE-'].update(f'Gratulálok {name}! Megcsináltad!')
            window['-QUESTION-'].update(f'Az eredményed a következő: {score/cnt*100}% {nehezseg.lower()} szinten.')
            window['-ZERO-'].update(visible = False)
            window['-ONE-'].update(visible = False)
            window['-TWO-'].update(visible = False)
            window['-THREE-'].update(visible = False)
            window['-FOUR-'].update(visible = False)
            window['-FIVE-'].update(visible = False)
            window['-SIX-'].update(visible = False)
            window['-SEVEN-'].update(visible = False)
            window['-EIGHT-'].update(visible = False)
            window['-NINE-'].update(visible = False)
            window['-BACKSPACE-'].update(visible = False)
            window['-SEND_ANSWER-'].update(visible = False)
            window['-COUNTER-'].update(visible = False)
            window['-SEPARATOR-'].update(visible = True)
            window['-RESULTS-'].update(visible = True)
            active = False

    window.close()
    update_file(name, score/cnt*100, nehezseg, elapsed_time)
    
if __name__ == "__main__":
    main()
