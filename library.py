from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import tkinter as tk
import database

databaseName = 'dataBase.db'
currentUserID = 0
root = tk.Tk()
var1 = IntVar()
var2 = IntVar()
var3 = IntVar()

# region tables
frame = ttk.Treeview(root)
frame.place(relx=0.15, rely=0.05, relwidth=0.33, relheight=0.89)
frame2 = ttk.Treeview(root)
frame2.place(relx=0.65, rely=0.05, relwidth=0.33, relheight=0.89)
frame["columns"] = ("ID", "Название", "Автор", "Год издания", "Кол-во")
frame.column("#0", width=0, stretch=tk.NO)
frame.column("ID", width=40, stretch=tk.NO)
frame.column("Название", width=200, stretch=tk.NO)
frame.column("Автор", width=200, stretch=tk.NO)
frame.column("Год издания", width=80, stretch=tk.NO)
frame.column("Кол-во", width=50, stretch=tk.NO)

frame.heading("ID", text="ID", anchor=tk.W)
frame.heading("Название", text="Название", anchor=tk.W)
frame.heading("Автор", text="Автор", anchor=tk.W)
frame.heading("Год издания", text="Год издания", anchor=tk.W)
frame.heading("Кол-во", text="Кол-во", anchor=tk.W)

frame2["columns"] = ("ID", "Название", "Автор", "Год издания", "Идентификатор")
frame2.column("#0", width=0, stretch=tk.NO)
frame2.column("ID", width=40, stretch=tk.NO)
frame2.column("Название", width=200, stretch=tk.NO)
frame2.column("Автор", width=150, stretch=tk.NO)
frame2.column("Год издания", width=80, stretch=tk.NO)
frame2.column("Идентификатор", width=100, stretch=tk.NO)

frame2.heading("ID", text="ID", anchor=tk.W)
frame2.heading("Название", text="Название", anchor=tk.W)
frame2.heading("Автор", text="Автор", anchor=tk.W)
frame2.heading("Год издания", text="Год издания", anchor=tk.W)
frame2.heading("Идентификатор", text="Идентификатор", anchor=tk.W)
# endregion


def fill_LibTable():
    try:
        frame.delete(*frame.get_children())
        books = database.fill_libTable()
        for i in books:
            frame.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def fill_on_hand_table():
    try:
        frame2.delete(*frame2.get_children())
        books = database.fill_onHandTable()
        for i in books:
            frame2.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def sort_frame(byWhat):
    try:
        frame.delete(*frame.get_children())
        books = database.sort1(byWhat)
        for i in books:
            frame.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def sort_frame2(byWhat):
    try:
        frame2.delete(*frame2.get_children())
        books = database.sort2(byWhat)
        for i in books:
            frame2.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def add_book():
    try:
        if len(entry_id.get()) != 0 and len(entry_title.get()) != 0 and len(entry_author.get()) != 0 and \
                len(entry_year.get()) != 0 and len(entry_count.get()) != 0:
            if not database.check_id(int(entry_id.get())):
                messagebox.showerror("TypeError", "Введенный Id уже существует")
                return
            data = [entry_id.get(), entry_title.get(), entry_author.get(), entry_year.get(), entry_count.get()]
            if not data[0].isdigit():
                messagebox.showerror("TypeError", "Id должен быть указан числом")
                return
            if not data[3].isdigit():
                messagebox.showerror("TypeError", "Год издания должен быть указан числом")
                return
            if not data[4].isdigit():
                messagebox.showerror("TypeError", "Кол-во экземпляров должно быть указано числом")
                return
            frame.insert('', 'end', values=data)
            database.add_to_database(data)
        else:
            messagebox.showerror("InputError", "Все поля должны быть заполнены")
    except Exception as e:
        print(e)


def del_book():
    try:
        i = frame.selection()[0]
        book = frame.item(i).values()
        frame.delete(i)
        book = str(book).split()
        ID = book[2][1:-1]
        database.del_from_database(ID)
    except IndexError:
        messagebox.showerror('error', 'Вы не выбрали книгу')


def replace_book(table):
    try:
        if table == "Library":
            i = frame.selection()[0]
            book = frame.item(i).values()
            book = str(book).split()
            ID = book[2][1:-1]
            if database.give_book(int(ID), currentUserID) > 1:
                frame.item(i, values=database.get_book(ID))
                frame2.insert('', 'end', values=database.get_book_onHand(ID))
            else:
                frame.delete(i)
        elif table == "NotInLibrary":
            i = frame2.selection()[0]
            book = frame2.item(i).values()
            book = str(book).split()
            ID = book[2][1:-1]
            takeID = book[len(book)-3][:-2]
            database.take_book(ID, takeID)
            frame2.delete(i)
            fill_LibTable()
        else:
            print('Где-то закралась ошибочка')
    except IndexError:
        messagebox.showerror('error', 'Вы не выбрали книгу')


def add_count(count):
    try:
        i = frame.selection()[0]
        book = frame.item(i).values()
        book = str(book).split()
        ID = book[2][1:-1]
        database.add_countBooks(ID, count)
        fill_LibTable()
    except IndexError:
        messagebox.showerror('error', 'Вы не выбрали книгу')


def middleTime():
    try:
        i = frame.selection()[0]
        book = frame.item(i).values()
        book = str(book).split()
        ID = book[2][1:-1]
        time = database.get_middleTime(ID)
        label_middle.config(text="Среднее время книги\n с ID: {0} на руках: {1} дней".format(ID, time))
    except IndexError:
        messagebox.showerror('error', 'Вы не выбрали книгу')


fill_LibTable()
fill_on_hand_table()
# region UI создание графического интерфейса
button_add = tk.Button(root, text="Добавить", bg='#BDBDBD', command=lambda: add_book())
button_add.place(relx=0.045, rely=0.40, relwidth=0.1, relheight=0.05)

button_del = tk.Button(root, text="Удалить", bg='#BDBDBD', command=lambda: del_book())
button_del.place(relx=0.045, rely=0.46, relwidth=0.1, relheight=0.05)

button_give = tk.Button(root, text="->Выдать книгу->", bg='#BDBDBD', command=lambda: replace_book("Library"))
button_give.place(relx=0.52, rely=0.05, relwidth=0.1, relheight=0.05)

button_take = tk.Button(root, text="<-Вернуть книгу<-", bg='#BDBDBD', command=lambda: replace_book("NotInLibrary"))
button_take.place(relx=0.52, rely=0.12, relwidth=0.1, relheight=0.05)

button_middle = tk.Button(root, text="Среднее время на руках", bg='#BDBDBD', command=lambda: middleTime())
button_middle.place(relx=0.52, rely=0.57, relwidth=0.1, relheight=0.05)

button_sortID = tk.Button(root, text="ID", bg='#BDBDBD', command=lambda: sort_frame("ID"))
button_sortID.place(relx=0.15, rely=0.945, relwidth=0.03, relheight=0.05)

button_sortName = tk.Button(root, text="Названию", bg='#BDBDBD', command=lambda: sort_frame("Name"))
button_sortName.place(relx=0.185, rely=0.945, relwidth=0.05, relheight=0.05)

button_sortAuthor = tk.Button(root, text="Автору", bg='#BDBDBD', command=lambda: sort_frame("Author"))
button_sortAuthor.place(relx=0.24, rely=0.945, relwidth=0.05, relheight=0.05)

button_sortYear = tk.Button(root, text="Году", bg='#BDBDBD', command=lambda: sort_frame("Year"))
button_sortYear.place(relx=0.295, rely=0.945, relwidth=0.05, relheight=0.05)

button_sortCount = tk.Button(root, text="Количеству", bg='#BDBDBD', command=lambda: sort_frame("Count"))
button_sortCount.place(relx=0.35, rely=0.945, relwidth=0.05, relheight=0.05)

button_sortID2 = tk.Button(root, text="ID", bg='#BDBDBD', command=lambda: sort_frame2("ID"))
button_sortID2.place(relx=0.65, rely=0.945, relwidth=0.03, relheight=0.05)

button_sortName2 = tk.Button(root, text="Названию", bg='#BDBDBD', command=lambda: sort_frame2("Name"))
button_sortName2.place(relx=0.685, rely=0.945, relwidth=0.05, relheight=0.05)

button_sortAuthor2 = tk.Button(root, text="Автору", bg='#BDBDBD', command=lambda: sort_frame2("Author"))
button_sortAuthor2.place(relx=0.74, rely=0.945, relwidth=0.05, relheight=0.05)

button_sortYear2 = tk.Button(root, text="Году", bg='#BDBDBD', command=lambda: sort_frame2("Year"))
button_sortYear2.place(relx=0.795, rely=0.945, relwidth=0.05, relheight=0.05)

button_sortCount2 = tk.Button(root, text="Идентификатору", bg='#BDBDBD', command=lambda: sort_frame2("takeID"))
button_sortCount2.place(relx=0.85, rely=0.945, relwidth=0.06, relheight=0.05)

button_plusOne = tk.Button(root, text="+1", bg='#BDBDBD', command=lambda: add_count(1))
button_plusOne.place(relx=0.03, rely=0.6, relwidth=0.03, relheight=0.05)

button_plusTwo = tk.Button(root, text="+2", bg='#BDBDBD', command=lambda: add_count(2))
button_plusTwo.place(relx=0.065, rely=0.6, relwidth=0.03, relheight=0.05)

button_plusFive = tk.Button(root, text="+5", bg='#BDBDBD', command=lambda: add_count(5))
button_plusFive.place(relx=0.1, rely=0.6, relwidth=0.03, relheight=0.05)

button_plusTen = tk.Button(root, text="+10", bg='#BDBDBD', command=lambda: add_count(10))
button_plusTen.place(relx=0.03, rely=0.665, relwidth=0.03, relheight=0.05)

button_plusFT = tk.Button(root, text="+15", bg='#BDBDBD', command=lambda: add_count(15))
button_plusFT.place(relx=0.065, rely=0.665, relwidth=0.03, relheight=0.05)

button_plusTwenty = tk.Button(root, text="+20", bg='#BDBDBD', command=lambda: add_count(20))
button_plusTwenty.place(relx=0.1, rely=0.665, relwidth=0.03, relheight=0.05)

entry_id = tk.Entry(root, font=12)
entry_id.place(relx=0.045, rely=0.05, relwidth=0.1, relheight=0.05)

entry_title = tk.Entry(root, font=12)
entry_title.place(relx=0.045, rely=0.12, relwidth=0.1, relheight=0.05)

entry_author = tk.Entry(root, font=12)
entry_author.place(relx=0.045, rely=0.19, relwidth=0.1, relheight=0.05)

entry_year = tk.Entry(root, font=12)
entry_year.place(relx=0.045, rely=0.26, relwidth=0.1, relheight=0.05)

entry_count = tk.Entry(root, font=12)
entry_count.place(relx=0.045, rely=0.33, relwidth=0.1, relheight=0.05)

label_id = tk.Label(root, font=12, text="Id:", fg='black')
label_id.place(relx=0.023, rely=0.05)

label_title = tk.Label(root, font=12, text="Назв:", fg='black')
label_title.place(relx=0.01, rely=0.12)

label_author = tk.Label(root, font=12, text="Автор:", fg='black')
label_author.place(relx=0.005, rely=0.19)

label_year = tk.Label(root, font=12, text="Год:", fg='black')
label_year.place(relx=0.015, rely=0.26)

label_count = tk.Label(root, font=12, text="Кол-во:", fg='black')
label_count.place(relx=0.005, rely=0.33)

label_sort = tk.Label(root, font=12, text="Сортировка по:", fg='black')
label_sort.place(relx=0.081, rely=0.945)

label_sort2 = tk.Label(root, font=12, text="Сортировка по:", fg='black')
label_sort2.place(relx=0.58, rely=0.945)

label_fill = tk.Label(root, font=12, text="Пополнение", fg='black')
label_fill.place(relx=0.05, rely=0.55)

label_func = tk.Label(root, font=12, text="Другие функции", fg='black')
label_func.place(relx=0.52, rely=0.25, relwidth=0.1, relheight=0.05)

label_middle = tk.Label(root, font=12, text="Среднее время книги\n с ID: 0 на руках: 0 дней", fg='black', bg='white')
label_middle.place(relx=0.49, rely=0.31, relwidth=0.15, relheight=0.25)

label_func = tk.Label(root, font=12, text="Тип пользователя", fg='black')
label_func.place(relx=0.04, rely=0.73)

user = Checkbutton(root, font=12, text="Пользователь", fg='black', variable=var1)
user.place(relx=0.03, rely=0.78, relwidth=0.1, relheight=0.05)

lib_worker = Checkbutton(root, font=12, text="Библиотекарь", fg='black', variable=var2)
lib_worker.place(relx=0.03, rely=0.83, relwidth=0.1, relheight=0.05)

admin = Checkbutton(root, font=12, text="Админ", fg='black', variable=var3)
admin.place(relx=0.014, rely=0.88, relwidth=0.1, relheight=0.05)
# endregion
if __name__ == "__main__":
    root.title("Библиотека")
    root.geometry("1750x500")
    root.resizable(False, False)
    root.mainloop()
