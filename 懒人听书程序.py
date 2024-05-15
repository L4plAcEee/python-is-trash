import tkinter as tk
import tkinter.filedialog as tkf
import pyttsx3


def open_file():
    global book_text # noqa
    book_text = ""
    try:
        path = tkf.askopenfilename()
        with open(path, "r", encoding="utf-8") as f:
            book_text = f.read()
        text.delete("1.0", tk.END)  # 清空文本框中的内容
        text.insert("end", book_text)  # 加载新的文件内容
    except FileNotFoundError:
        print("文件不存在")
    except Exception as e:
        print("发生错误:", e)


def read_book():
    try:
        book = pyttsx3.init()
        book.say(book_text)
        book.runAndWait()
    except Exception as e:
        print("发生错误:", e)


window = tk.Tk()
window.title("懒人听书程序")
window.geometry("640x480")

text = tk.Text()
text.place(x=20, y=20, width=600, height=400)

select_button = tk.Button(window, text="选择书籍文件", command=open_file)
select_button.place(x=100, y=430, width=150, height=30)

read_button = tk.Button(window, text="开始阅读", command=read_book)
read_button.place(x=300, y=430, width=150, height=30)

window.mainloop()

