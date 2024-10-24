from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from memo_app import app
from memo_data import *
from memo_main_layout import *
from memo_card_layout import *
from memo_edit_layout import txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3

######################################              Константи:              #############################################
main_width, main_height = 1000, 450  # початкові розміри головного вікна
card_width, card_height = 600, 500  # початкові розміри вікна "картка"
time_unit = 1000  # тривалість однієї одиниці часу, на яку потрібно "заснути"
# (в робочій версії програми збільшити в 60 разів!)

######################################          Глобальні змінні:      #############################################
questions_listmodel = FormListModel()  # список питань
frm_edit = FormEdit(0, txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2,
                        txt_Wrong3)  # запам'ятовуємо, що у формі редагування питання з чим пов'язано
radio_list = [rbtn_1, rbtn_2, rbtn_3,
              rbtn_4]  # список віджетів, які треба перемішувати (для випадкового розміщення відповідей)
frm_card = 0  # тут буде пов'язуватись питання з формою тесту
timer = QTimer()  # таймер для можливості "заснути" на деякий час і прокинутися
win_card = QWidget()  # вікно картки
win_card.setStyleSheet(QSS)
win_card.setObjectName("cardWindow")
win_main = QWidget()  # вікно редагування питань, основне в програмі
win_main.setObjectName("mainWindow")
win_main.setStyleSheet(QSS)

######################################             Тестові дані:         #############################################
def testlist():
    frm = Form('Коли почалася перша світова війна?', '28 липня 1914 року',
               '1 серпня 1915 року', '11 листопада 1918 року', '23 червня 1913 року')
    questions_listmodel.form_list.append(frm)

    frm = Form('яка країна перша оголосила війну в ході першої світової?', 'Австро-Угорщина',
               'Німеччина', 'Велика Британія',
               'росія')
    questions_listmodel.form_list.append(frm)

    frm = Form('яка подія сьала приводом початку війни?', 'Вбивство Франца Фердинанда',
               'Початок війни між Росією та Японією', 'Окупація Бельгії Німеччиною', 'Революція в НІМЕЧЧИНІ')
    questions_listmodel.form_list.append(frm)

    frm = Form('Які країни складали Троїстий союз на початку війни?', 'Німеччина, Австро-Угорщина, Італія',
               'Німеччина, Франція, Велика Британія', 'росія, Велика Британія , Франція', 'Австро-Угорщина, росія, Османська імперія')
    questions_listmodel.form_list.append(frm)

    frm = Form('Який вид зброї вперше массово використався під час першої світової?', 'Хімічна',
               'Ядерна', 'Лазерна', 'Зенітні')
    questions_listmodel.form_list.append(frm)

    frm = Form('який фронт вважався основним у ході першої світової війни?', 'західний',
               'східний', 'Італійський', 'Балканський')
    questions_listmodel.form_list.append(frm)

    frm = Form('яке місто було головним обєктом німецької атаки на західному фронті?', 'Верден',
               'Париж', 'Лондон', 'Берлін')
    questions_listmodel.form_list.append(frm)

    frm = Form('коли закінчилася перша світова війна?', '11 листопада 1918 року',
               '28 липня 1919 року', '1 травня 1917 року', '14 серпня 1916 року')
    questions_listmodel.form_list.append(frm)

    frm = Form('який договір завершив Першу світову війну?', 'Версальський',
               'Брест-Литовський', 'Мюнхенська уогда', 'Варщавський договір')
    questions_listmodel.form_list.append(frm)

    frm = Form('яка імперія розпалася після першої світової війни ?', 'Австро-Угорська',
               'Британська', 'Французька', 'російська')
    questions_listmodel.form_list.append(frm)


######################################     Функції для проведення тесту:    #############################################

def set_card():
    ''' задає, як виглядає вікно картки '''
    win_card.resize(card_width, card_height)
    win_card.move(300, 300)
    win_card.setWindowTitle('Memory Card')
    win_card.setLayout(layout_card)


def sleep_card():
    ''' картка ховається на час, вказаний у таймері '''
    win_card.hide()
    timer.setInterval(time_unit * box_Minutes.value())
    timer.start()


def show_card():
    ''' показує вікно (за таймером), таймер зупиняється '''
    win_card.show()
    timer.stop()


def show_random():
    ''' показати випадкове питання '''
    global frm_card  # як властивість вікна - поточна форма з даними картки
    # отримуємо випадкові дані і випадково розміщуємо варіанти відповідей по радіокнопках:
    frm_card = random_AnswerCheck(questions_listmodel, lb_Question, radio_list, lb_Correct, lb_Result)
    # ми будемо запускати функцію, коли вікно вже є. Тому показуємо:
    frm_card.show()  # завантажити потрібні дані у відповідні віджети
    show_question()  # показати на формі панель питань


def click_OK():
    ''' перевіряє питання або завантажує нове питання '''
    if btn_OK.text() != 'Наступне питання':
        frm_card.check()
        show_result()
    else:
        # напис на кнопці "Наступне", отже створюємо наступне випадкове питання:
        show_random()


def back_to_menu():
    ''' повернення з тесту у вікно редактора '''
    win_card.hide()
    win_main.showNormal()


######################################     Функції для редагування питань:    ######################################
def set_main():
    ''' задає, як виглядає основне вікно '''
    win_main.resize(main_width, main_height)
    win_main.move(100, 100)
    win_main.setWindowTitle('Список питань')
    win_main.setLayout(layout_main)


def edit_question(index):
    ''' завантажує у форму редагування питання і відповіді, відповідні переданому рядку '''
    if index.isValid():
        i = index.row()
        frm = questions_listmodel.form_list[i]
        frm_edit.change(frm)
        frm_edit.show()


def add_form():
    ''' додає нове питання і пропонує його змінити '''
    questions_listmodel.insertRows()  # Нове питання з'явилось у даних і автоматично в списку на екрані
    last = questions_listmodel.rowCount(0) - 1  # Нове питання - останнє у списку. Знайдемо його позицію.
    index = questions_listmodel.index(
        last)  # отримуємо об'єкт класу QModelIndex, що відповідає останньому елементу у даних
    list_questions.setCurrentIndex(index)  # робимо відповідний рядок списку на екрані поточним
    edit_question(index)  # це питання треба завантажити у форму редагування
    txt_Question.setFocus(
        Qt.TabFocusReason)  # переводимо фокус на поле редагування питання, щоб одразу прибирати шаблони


def del_form():
    ''' видаляє питання і переключає фокус '''
    questions_listmodel.removeRows(list_questions.currentIndex().row())
    edit_question(list_questions.currentIndex())


def start_test():
    ''' при початку тесту форма пов'язується з випадковим питанням і показується '''
    show_random()
    win_card.show()
    win_main.showMinimized()


######################################      Встановлення потрібних з'єднань:    #############################################
def connects():
    list_questions.setModel(questions_listmodel)  # зв'язати список на екрані зі списком питань
    list_questions.clicked.connect(
        edit_question)  # при натисканні на елемент списку відкриватиметься для редагування відповідне питання
    btn_add.clicked.connect(add_form)  # з'єднали натискання кнопки "нове питання" з функцією додавання
    btn_delete.clicked.connect(del_form)  # з'єднали натискання кнопки "видалити питання" з функцією видалення
    btn_start.clicked.connect(start_test)  # натискання кнопки "почати тест"
    btn_OK.clicked.connect(click_OK)  # натискання кнопки "OK" на формі тесту
    btn_Menu.clicked.connect(back_to_menu)  # натискання кнопки "Меню" для повернення з форми тесту до редактора питань
    timer.timeout.connect(show_card)  # показуємо форму тесту після завершення таймера
    btn_Sleep.clicked.connect(sleep_card)  # натискання кнопки "спати" у картці-тесті


######################################            Запуск програми:         #############################################
# Основний алгоритм іноді оформлюють у функцію, яка запускається, тільки якщо код виконується з цього файлу,
# а не при підключенні як модуль. Це не потрібно для учнів.
testlist()
set_card()
set_main()
connects()
win_main.show()
app.exec_()
