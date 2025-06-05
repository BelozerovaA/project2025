from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random


def load_image(image_path, size=None):
    try:
        image = Image.open(image_path)
        if size:
            image = image.resize(size)
        print(f"Изображение {image_path} успешно загружено.")
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None


# Список анекдотов про Штирлица
stirlitz_jokes = [
    "Штирлиц долго смотрел в одну точку. Потом в другую. Так он понял, что велосипед.",
    "Штирлиц стрелял вслепую. Слепая умерла.",
    "Штирлиц выстрелил в упор. Упор сгорел.",
    "Штирлиц шел по коридору, и вдруг его осенило. Он вернулся и закрыл дверь.",
    "Штирлиц уронил карандаш. Карандаш не поднялся. Так Штирлиц понял, что карандаш был мертв."
]


def show_completion_window(parent_window):
    completion_window = Toplevel(parent_window)
    completion_window.title("Уровень пройден!")
    completion_window.attributes('-fullscreen', True)
    completion_window.resizable(False, False)

    # Выбираем случайный анекдот
    joke = random.choice(stirlitz_jokes)

    # Увеличиваем шрифт анекдота
    joke_label = Label(completion_window, text=joke, font=('Arial', 36), bg='#f0f0f0', wraplength=1000)
    joke_label.place(relx=0.5, rely=0.4, anchor='center')

    # Кнопки с большим расстоянием между ними
    buttons_frame = Frame(completion_window, bg='#f0f0f0')
    buttons_frame.place(relx=0.5, rely=0.7, anchor='center')

    # Кнопка "Пройти заново"
    restart_btn = ttk.Button(buttons_frame, text='Пройти заново', style="Rounded.TButton",
                             command=lambda: [completion_window.destroy(), create_level_1()])
    restart_btn.pack(side='left', padx=50)

    # Кнопка "Следующий уровень"
    next_level_btn = ttk.Button(buttons_frame, text='Следующий уровень', style="Rounded.TButton",
                                command=lambda: [completion_window.destroy(), level_not_available()])
    next_level_btn.pack(side='left', padx=50)


def level_not_available():
    messagebox.showinfo("Информация", "Этот уровень пока недоступен")


def toggle_cell(cells, i, j):
    cell = cells[i][j]
    if hasattr(cell, 'square_id'):
        cell.delete(cell.square_id)
        delattr(cell, 'square_id')
    else:
        width = cell.winfo_width()
        height = cell.winfo_height()
        margin = 5  # Уменьшаем отступ для большего закрашивания
        square = cell.create_rectangle(margin, margin, width - margin, height - margin,
                                       fill='#8A2BE2', outline='#B23AEE')  # Фиолетовый цвет
        cell.square_id = square


def reset_level(cells):
    for row in cells:
        for cell in row:
            if hasattr(cell, 'square_id'):
                cell.delete(cell.square_id)
                delattr(cell, 'square_id')
            if hasattr(cell, 'cross_id'):
                for cross in cell.cross_id:
                    cell.delete(cross)
                delattr(cell, 'cross_id')


def check_solution(cells, level_window):
    solution = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]

    # Удаляем старые крестики
    for row in cells:
        for cell in row:
            if hasattr(cell, 'cross_id'):
                for cross in cell.cross_id:
                    cell.delete(cross)
                delattr(cell, 'cross_id')

    has_errors = False
    for i in range(3):
        for j in range(3):
            user_cell = 1 if hasattr(cells[i][j], 'square_id') else 0
            if user_cell != solution[i][j]:
                has_errors = True
                width = cells[i][j].winfo_width()
                height = cells[i][j].winfo_height()
                margin = 20

cross1 = cells[i][j].create_line(margin, margin, width - margin, height - margin,
                                                 fill='#FFB6C1', width=5)
                cross2 = cells[i][j].create_line(width - margin, margin, margin, height - margin,
                                                 fill='#FFB6C1', width=5)

                cells[i][j].cross_id = (cross1, cross2)

    if not has_errors:
        show_completion_window(level_window)


def create_level_1():
    level_window = Toplevel(root)
    level_window.title('Уровень 1')
    level_window.attributes('-fullscreen', True)
    level_window.resizable(False, False)

    # Загрузка фонового изображения
    bg_image = load_image(r'C:\Users\user\OneDrive\Рабочий стол\2 курс\Нонограмм\фон.png', (1920, 1200))
    if bg_image:
        bg_label = Label(level_window, image=bg_image)
        bg_label.place(relx=0.5, rely=0.5, anchor='center')
        bg_label.image = bg_image

    # Основной контейнер с отступами
    main_container = Frame(level_window, bg='#f0f0f0')
    main_container.place(relx=0.5, rely=0.5, anchor='center')

    # Контейнер для подсказок столбцов и игрового поля
    game_container = Frame(main_container, bg='#f0f0f0')
    game_container.pack()

    # Подсказки для столбцов (над игровым полем)
    col_hints_frame = Frame(game_container, bg='#f0f0f0')
    col_hints_frame.pack(side='top')

    col_hints = [[3], [2], [3]]
    for j, hint in enumerate(col_hints):
        hint_frame = Frame(col_hints_frame, bg='#f0f0f0', padx=5, pady=5)
        hint_frame.pack(side='left', expand=True)

        hint_label = Label(hint_frame, text='\n'.join(map(str, hint)),
                           font=('Arial', 36, 'bold'), bg='#f0f0f0')
        hint_label.pack()

    # Контейнер для строк и игрового поля
    row_game_frame = Frame(game_container, bg='#f0f0f0')
    row_game_frame.pack()

    # Подсказки для строк (слева от игрового поля)
    row_hints_frame = Frame(row_game_frame, bg='#f0f0f0')
    row_hints_frame.pack(side='left')

    row_hints = [[3], [2], [3]]
    for i, hint in enumerate(row_hints):
        hint_frame = Frame(row_hints_frame, bg='#f0f0f0', padx=5, pady=5)
        hint_frame.pack(expand=True, fill='both')

        hint_label = Label(hint_frame, text=' '.join(map(str, hint)),
                           font=('Arial', 36, 'bold'), bg='#f0f0f0')
        hint_label.pack()

    # Игровое поле
    game_frame = Frame(row_game_frame, bg='white', width=600, height=600)
    game_frame.pack()

    # Создаем сетку 3x3 для нонограммы
    cell_size = 200
    cells = []
    for i in range(3):
        row = []
        for j in range(3):
            cell = Canvas(game_frame, width=cell_size, height=cell_size, bg='white',
                          highlightthickness=1, highlightbackground='black')
            cell.grid(row=i, column=j, sticky='nsew')
            cell.bind('<Button-1>', lambda e, i=i, j=j: toggle_cell(cells, i, j))
            row.append(cell)
        cells.append(row)

    # Кнопки управления
    buttons_frame = Frame(main_container, bg='#f0f0f0')
    buttons_frame.pack(pady=20)

    reset_btn = ttk.Button(buttons_frame, text='Сброс', style="Rounded.TButton",
                           command=lambda: reset_level(cells))
    reset_btn.pack(side='left', padx=10)

    menu_btn = ttk.Button(buttons_frame, text='Выход в меню', style="Rounded.TButton",
                          command=level_window.destroy)
    menu_btn.pack(side='left', padx=10)

    check_btn = ttk.Button(buttons_frame, text='Проверка', style="Rounded.TButton",
                           command=lambda: check_solution(cells, level_window))
    check_btn.pack(side='left', padx=10)


def open_tutorial():
    tutorial_window = Toplevel(root)
    tutorial_window.title("Обучение")
    tutorial_window.attributes('-fullscreen', True)
    tutorial_window.resizable(False, False)

tutorial_bg = load_image('C:/Users/user/OneDrive/Рабочий стол/2 курс/Нонограмм/3.png', (1920, 1200))
    if tutorial_bg:
        print("Фоновое изображение для обучения загружено.")
        bg_label = Label(tutorial_window, image=tutorial_bg)
        bg_label.place(relx=0.5, rely=0.5, anchor='center')
        bg_label.image = tutorial_bg
    else:
        print("Фоновое изображение для обучения не загружено.")
        tutorial_window.config(bg='white')

    tutorial_text = """
        Добро пожаловать в обучение по игре Нонограмм!

        Цель игры:
        Заполните клеточки на поле, основываясь на 
        числовых подсказках.
        Числа указывают, сколько клеток необходимо 
        заполнить в строке или столбце.

        Правила:
        1. Клетки, которые необходимо заполнить, 
        отмечаются цветом.
        2. Сначала подумайте, как лучше всего заполнить 
        клетки, используя подсказки.
        3. Удачи в игре!

        Пример 1:
        - Если в строке указано число "5", это означает, 
        что в этой строке нужно закрасить 5 клеток подряд.
        Пример 2:
        - Если в строке указано "2 1", это означает, что 
        нужно закрасить две группы клеток: первую из 2 
        клеток и вторую из 1 клетки, с хотя бы одной 
        пустой клеткой между ними.

        Советы:
        - Начинайте с строк и столбцов, где есть только 
        одна группа клеток.
        - Используйте карандаш для пометок, чтобы не 
        ошибиться.
        """

    label = Label(tutorial_window, text=tutorial_text, justify="left", padx=20, pady=10, font=('Cascadia Code', 14),
                  bg='white')
    label.place(relx=0.25, rely=0.44, anchor='center')

    example_images = [
        'C:/Users/user/OneDrive/Рабочий стол/2 курс/Нонограмм/пример1.png',
        'C:/Users/user/OneDrive/Рабочий стол/2 курс/Нонограмм/пример2.png',
        'C:/Users/user/OneDrive/Рабочий стол/2 курс/Нонограмм/пример3.png',
    ]
    current_image_index = 0

    def show_next_image():
        nonlocal current_image_index
        current_image_index = (current_image_index + 1) % len(example_images)
        image = load_image(example_images[current_image_index], (600, 600))
        if image:
            image_label.config(image=image)
            image_label.image = image

    image = load_image(example_images[current_image_index], (600, 600))
    image_label = Label(tutorial_window, image=image, bg='white')
    image_label.image = image
    image_label.place(relx=0.75, rely=0.35, anchor='center')

    next_button = ttk.Button(tutorial_window, text="Далее", style="Rounded.TButton",
                             command=show_next_image)
    next_button.place(relx=0.75, rely=0.75, anchor='center')

    close_button = ttk.Button(tutorial_window, text='Закрыть обучение', style="Rounded.TButton", width=20,
                              padding=5,
                              command=tutorial_window.destroy)
    close_button.place(relx=0.25, rely=0.9, anchor='center')


def change_image():
    new_window = Toplevel(root)
    new_window.title('Главное меню')
    new_window.attributes('-fullscreen', True)
    new_window.resizable(False, False)

    new_photo = load_image(r'C:\Users\user\OneDrive\Рабочий стол\2 курс\Нонограмм\2.png', (1920, 1200))
    if new_photo:
        label = Label(new_window, image=new_photo)
        label.place(relx=0.5, rely=0.5, anchor='center')
        label.image = new_photo
    else:
        label = Label(new_window, text="Изображение не загружено", font=('Cascadia Code', 20))
        label.pack()

    create_level_buttons(new_window)
    exit_main_btn = ttk.Button(new_window, text='Выход на главную', style="Exit.TButton", width=18,
                               command=new_window.destroy)
    exit_main_btn.place(relx=0.5, rely=0.85, anchor='center')


def create_level_buttons(window):
    training_button = ttk.Button(window, text='ОБУЧЕНИЕ', width=20, style="Rounded.TButton", command=open_tutorial)
    training_button.place(relx=0.5, y=50, anchor='center')

levels = [
        (90, 210), (440, 210), (790, 210), (1140, 210),
        (90, 470), (440, 470), (790, 470), (1140, 470)
    ]

    for i, (x, y) in enumerate(levels):
        level_num = i + 1
        if level_num == 1:
            button = ttk.Button(window, text=f'Уровень {level_num}', width=12, padding=30,
                                style="Rounded.TButton", command=create_level_1)
        else:
            button = ttk.Button(window, text=f'Уровень {level_num}', width=12, padding=30,
                                style="Rounded.TButton", command=level_not_available)
        button.place(x=x, y=y)


def go_to_main_menu():
    btn.place(relx=0.5, rely=0.5, anchor='center')
    exit_btn.place(relx=0.5, rely=0.6, anchor='center')
    clear_level_buttons()
    label.config(image=photo)
    if 'exit_main_btn' in globals():
        exit_main_btn.place_forget()


def clear_level_buttons():
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Button) and ('Уровень' in widget.cget("text") or widget.cget("text") == "ОБУЧЕНИЕ"):
            widget.destroy()


# Создание главного окна
root = Tk()
root.title('Нонограмм')
root.attributes('-fullscreen', True)
root.resizable(False, False)

# Стили для кнопок
style = ttk.Style()
btn_font = ('Cascadia Code', 24)
level_btn_font = ('Cascadia Code', 14)

style.configure("Rounded.TButton", padding=10, relief="flat", background="#666FFF", borderwidth=1,
                focusthickness=1,
                font=btn_font)
style.map("Rounded.TButton", background=[("active", "#666FFF")], foreground=[("active", "black")])
style.configure("Exit.TButton", padding=10, relief="flat", background="#666FFF", borderwidth=1,
                focusthickness=1,
                font=btn_font)
style.map("Exit.TButton", background=[("active", "#666FFF")], foreground=[("active", "black")])

# Загрузка фонового изображения
photo = load_image('C:/Users/user/OneDrive/Рабочий стол/2 курс/Нонограмм/1.png', (1920, 1200))
if photo:
    label = Label(root, image=photo)
    label.place(relx=0.5, rely=0.5, anchor='center')
else:
    label = Label(root, text="Изображение не загружено", font=('Cascadia Code', 20))
    label.pack()

# Кнопки главного меню
btn = ttk.Button(root, text='Начать игру', style="Rounded.TButton", width=20, command=change_image)
btn.place(relx=0.5, rely=0.5, anchor='center')

exit_btn = ttk.Button(root, text='Выход из игры', style="Exit.TButton", width=18, command=root.quit)
exit_btn.place(relx=0.5, rely=0.6, anchor='center')

root.mainloop()