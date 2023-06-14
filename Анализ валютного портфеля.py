'''https://apps.skillfactory.ru/learning/course/course-v1:SkillFactory+PDEV+2021/block-v1:SkillFactory+PDEV+2021+type@sequential+block@1cd5d2d0ce6b45489c146b7ff12c0f9f/block-v1:SkillFactory+PDEV+2021+type@vertical+block@02ade0920aaf41bea57d147e08b0155a'''
# dic = {
#     '20': [
#         {
#             'carency': 'Rub',
#             'rate': 0.013,
#             'amount': 1000
#         },
#         {
#             'carency': 'BTC',
#             'rate': 36000,
#             'amount': 0.003
#         }
#     ],
#     '21': [
#         {
#             'carency': 'Rub',
#             'rate': 0.014,
#             'amount': 2000
#         },
#         {
#             'carency': 'BTC',
#             'rate': 36200,
#             'amount': 0.005
#         }
#     ],
# }

# print(dic.items())
import json  # https://pythonworld.ru/moduli/modul-json.html
from copy import deepcopy


# print(json.dumps(dic, indent=2))
def safe_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)
        print('Data saved to file')


def load_data(file):
    with open(file) as f:
        data = json.load(f)
    return data


# safe_data(dic)


# print('File loaded: ', json.dumps(load_data(), indent=2))
# d = open('data.json')
# d = [line.strip() for line in d]
# print(d)


def show_currency(name, percent, bar=50):
    fill = 'Ж'
    empty = '-'
    bar_length = round(percent * bar)
    progress = fill * bar_length + empty * (bar - bar_length)
    print(f'{name:10} : {round(percent, 2) * 100:5} % |{progress}|')


def show_convert_to_usd(data):
    weeks = list(sorted(data.keys()))
    converted = []
    for week in weeks:
        currencies = data[week]
        total = 0
        for cur in currencies:
            total += cur['rate'] * cur['amount']
        converted.append(round(total, 2))
    plot_data(converted, weeks)


def show_status(data, weeknums):
    total = 0
    for curr in data[weeknums]:
        total += curr['rate'] * curr['amount']  # total in usd
    stat = []
    for curr in data[weeknums]:
        stat.append((curr['rate'] * curr['amount'] / total, curr['name']))
    stat = reversed(sorted(stat))
    for s, name in stat:
        show_currency(name, s)


# print(show_currency('Rub',0.6))
# print(show_currency('BCN',0.3))
def plot_data(data, signs, height=12):  # Plot the graphic
    for i in range(height):
        if i % 3 == 0:
            current = max(data) - (max(data) - min(data)) / height * i
            '''(max(data) - (max(data) - min(data)) / height) = цена деления столбца графика'''
            line = f"{str(round(current, 2)):10}"
        else:
            line = " " * 10
        for num in data:
            # print(f'i={i: 2},G={max(data) - (max(data) - min(data))/ height:2}',end=' ')
            if max(data) - (max(data) - min(data)) / height * (i + 1) <= num:
                line += "Ж   "
            else:
                line += "    "
        print(line)
    print(f'{str(round(min(data), 2)):9} ' + '-' * (len(line) - 13))
    print('Week:   ', *[(i + ' ') for i in signs])


# plot_data([10, 2, 3, 4, 5], ['A', 'B', 'C', 'D', 'E'])
def select_mode():
    print('*' * 30 + '\nВыберите режим работы:')
    print("1 Добавить новую неделю ")
    print("2 Скопировать новую неделю ")
    print("3 Добавить информацию о валюте ")
    print("4 Изменить информацию о валюте ")
    print("5 Вывести статистику за неделю ")
    print("6 Вывести распределение (в usd) за весь период ")
    print("7 Сохранить изменения ")
    print("8 Закрыть программу ")
    print("*" * 30)
    return int(input())


def loop():
    data = load_data('data.json')
    while True:
        mode = select_mode()
        if mode == 1:  # Добавить новую неделю
            week = input('Введите номер новой недели ')
            data[week] = []

        elif mode == 2:  # Скопировать новую неделю
            from_week = input('Введите номер недели, которую будем копировать ')
            week = input('Введите номер новой недели ')
            data[week] = deepcopy(data[from_week])

            '''как вариант без dipcopy
            sorce=[] 
            for current_dict in data[from_week]:
                sorce.append(current_dict.copy())'''

        elif mode == 3:  # Добавить информацию о валюте
            week = str(input('Введите номер недели    '))
            name = str(input('Введите имя валюты  '))
            rate = float(input('Введите курс к доллару    '))
            amount = float(input('Введите количество  '))
            data[week].append({
                'name': name,
                'rate': rate,
                'amount': amount
            })

        elif mode == 4:  # Изменить информацию о валюте
            week = str(input('Введите номер недели    '))
            name = str(input('Введите имя валюты  '))
            num = None  # Индекс искомой валюты
            for i, curr in enumerate(data[week]):

                if curr["name"] == name:
                    num = i
            if num == None:
                print('Нет такой валюты!')
            else:
                curr_rate = data[week][num]['rate']
                rate = input(f'Введите новый курс валюты  {curr_rate}   ')
                if rate:
                    data[week][num]['rate'] = float(rate)

                curr_amount = data[week][num]["amount"]
                amount = input(f"Введите количество {curr_amount}    ")
                if amount:
                    data[week][num]["amount"] = float(amount)

        elif mode == 5:  # Вывести статистику
            week = str(input('Введите номер недели    '))
            show_status(data, week)
        elif mode == 6:  # Вывести распределение валют
            show_convert_to_usd(data)
        elif mode == 7:  # Safe data
            safe_data(data)
        elif mode == 8:  # Exit
            print('Goodby!')
            break
        else:
            print('Не корректный ввод')
    safe_data(data)


loop()
