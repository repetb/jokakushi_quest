from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import font
from PIL import Image
from tkinter.font import Font, families

class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        # super().__init__(root)
        # self.pack()
        self._frame = None
        self.switch_frame(Result)
        # root.title("some title")
        # root.minsize(100, 100)
        # screen_width = root.winfo_screenwidth()
        # screen_height = root.winfo_screenheight()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Result(tkinter.Frame):
    def __init__(self, master):
        # Frame
        tkinter.Frame.__init__(self, master)
        # frame = tkinter.Frame(root)
        # frame.pack()

        # Button
        button1 = tkinter.Button(
            self, text='タイトルへ戻る',
            command=lambda: master.switch_frame(Top))
        button1.pack(side=tkinter.BOTTOM)

        # Message
        fontstyle = tkinter.font.Font(
            self, family="Helvetica", size=20, weight="bold")
        msg = tkinter.Label(self, text="RESULT", font=fontstyle)
        msg.pack(side=tkinter.TOP)

        # Text
        f = Font(family='Helvetica', size=16)
        v1 = StringVar()
        txt = Text(self, height=15, width=70)
        txt.configure(font=f)
        for i in range(0, 101):
            txt.insert(1.0, "Hello!\n")
        txt.pack(side=tkinter.LEFT)

        # Scrollbar
        scrollbar = tkinter.Scrollbar(
            self,
            orient=VERTICAL,
            command=txt.yview)
        txt['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tkinter.RIGHT, expand=True, fill=tkinter.Y)


class Top(tkinter.Frame):
    def __init__(self, master):
        # Frame
        tkinter.Frame.__init__(self, master)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # キャンバスを設置
        title_canvas = tkinter.Canvas(
            self,
            width=screen_width,
            height=screen_height,
            bg="white",
            relief=tkinter.RAISED)
        title_canvas.pack()

        # 背景画像のリサイズ
        title_img_filename = "./mountain.png"
        img = Image.open(title_img_filename)
        width = round(screen_width)
        height = round(screen_height)
        img_resize = img.resize((width, height))
        img_resize = img_resize.save('./mountain_re.png', quality=95)
        title_img_filename_re = "./mountain_re.png"
        title_img = tkinter.PhotoImage(file=title_img_filename_re)

        # 背景画像をキャンバスに設置
        title_img_id = title_canvas.create_image(
            round(screen_width/2),
            round(screen_height/2),
            image=title_img,
            tag="title_img"
        )
        title_canvas.pack()

        # 背景画像の上にタイトルを表示
        title_id = title_canvas.create_text(
            screen_width/2,
            screen_height/5,
            text="Jokakushi Quest",
            font=("Yu Gothic UI", 80),
            fill="black"
        )
        title_canvas.pack()

        # Button
        button1 = tkinter.Button(
            self, text='RESULTへ戻る',
            command=lambda: master.switch_frame(Result))
        button1.pack(side=tkinter.BOTTOM)


if __name__ == "__main__":
    app = App()
    app.mainloop()
