import tkinter
import time
import db_handler
from PIL import Image
from functools import partial
import random
from tkinter.font import Font


FNT = ("Yu Gothic UI", 30)
Q_FNT = ("Yu Gothic UI", 12)
question_list = db_handler.GetAllQuestions()
question_list_len = len(question_list)

# 持ち時間
tmr = 30
stop_counter = False

question_answered = []


class GameCharacter:
    def __init__(self, name, life, x, y, imgfile, tagname, screen_width, canvas, r0, r):
        self.name = name
        self.life = life
        self.lmax = life
        self.img = tkinter.PhotoImage(file=imgfile)
        self.x = x
        self.y = y
        self.tagname = tagname
        self.screen_width = screen_width
        self.stage = 1
        self.canvas = canvas
        self.r0 = r0
        self.r = r

    def draw(self):
        x = self.x
        y = self.y

        self.canvas.create_image(x, y, image=self.img,
                                 tag=self.tagname+"_image")
        self.canvas.create_text(x, y+120, text=self.name,
                                font=FNT, fill="red", tag=self.tagname+"_name")
        self.canvas.create_text(x, y+200, text="life{}".format(self.life,
                                self.lmax), font=FNT, fill="blue", tag=self.tagname+"_life")

    def draw_down_notification(self):
        self.canvas.create_text(self.x, self.y+120, text=self.name +
                                "は倒れた", font=FNT, fill="red", tag=self.tagname+"_dead")
        self.canvas.delete(self.tagname+"_dead")

    def attack(self):
        dir = 1
        if self.x >= self.screen_width/2:
            dir = -1
        for i in range(5):
            self.canvas.coords(self.tagname+"_image", self.x+i*10*dir, self.y)
            self.canvas.update()
            time.sleep(0.1)
        self.canvas.coords(self.tagname+"_image", self.x, self.y)
        # for b in range(4):
        #   button[b]["state"] = "disable"

    def damage(self):
        if(self.life > 0):
            for i in range(5):
                self.draw()
                self.canvas.update()
                time.sleep(0.1)
                self.canvas.delete(
                    self.tagname, self.tagname+"_life", self.tagname+"_image", self.tagname+"_name")
                self.canvas.update()
                time.sleep(0.1)
            self.life = self.life - 30

            if self.life > 0:
                self.draw()
            else:
                self.draw_down_notification()

                if self.tagname == "LC":
                    self.r.destroy()
                    self.r0.switch_frame(Result)

                if self.tagname == "RC":
                    self.newcharacter()

    def newcharacter(self):
        self.stage = self.stage + 1
        if self.stage >= 6:
            self.r.destroy()
            self.r0.switch_frame(Result)

            return

        self.canvas.itemconfig("RC_name", text="NextCharacter")

        self.lmax = life_list[self.stage]
        self.life = self.lmax
        # canvas.itemconfig("RC_life",text="life{}".format(self.life,self.lmax))

        self.canvas.delete("RC_image")
        self.img = tkinter.PhotoImage(file=file_list[self.stage])
        self.name = name_list[self.stage]
        self.draw()


def get_question():
    q_id = random.randint(1, question_list_len)
    return db_handler.GetQuestionByID(q_id)[0]


def choice_answer(user_ans, ans, ch_txt, button, choice_canvas, question_canvas, root, screen_height, screen_width, question_frame, choice_frame, label_timer, character, q):
    # 回答ボタンが押されるとタイマーをリセット
    reset(button, label_timer)
    for i in range(4):
        button[i]["state"] = "disable"
    if user_ans == ans:
        character[0].attack()
        character[1].damage()
    else:
        character[1].attack()
        character[0].damage()
    ql = list(q)
    ql.append(user_ans)
    question_answered.append(ql)

    if character[0].life > 0 and character[1].life > 0:
        for i in ch_txt:
            i.pack_forget()

        question = get_question()
        create_q_frame(question, choice_canvas, question_canvas, root, screen_height,
                       screen_width, question_frame, choice_frame, label_timer, character)


def create_q_frame(q, choice_canvas, question_canvas, root, screen_height, screen_width, question_frame, choice_frame, label_timer, character):

    choice = q[3:7]
    choice_txt = []

    for ch in range(len(choice)):
        choice_canvas.itemconfig("choice_"+str(ch), text=choice[ch])

    question_canvas.itemconfig("question", text=q[2])

    button = []
    i = 0
    user_choice = ["ア", "イ", "ウ", "エ"]
    button_frame = tkinter.Frame(
        root, width=screen_width*2/3, height=screen_height*1/3, padx=3, pady=3)
    for u in user_choice:
        button.append(tkinter.Button(button_frame, text=u, width=5, height=3, command=partial(
            choice_answer, u, q[7], choice_txt, button, choice_canvas, question_canvas, root, screen_height, screen_width, question_frame, choice_frame, label_timer, character, q)))
        button[-1].pack(side=tkinter.LEFT)
        i += 1

    question_frame.grid(rowspan=2, column=0, row=1)
    choice_frame.grid(column=1, row=1)
    button_frame.grid(column=1, row=2)
    count_down(button, choice_canvas, question_canvas, root, screen_height,
               screen_width, question_frame, choice_frame, label_timer, character)


class choice_bg_image:
    def __init__(self, frame, canvas, screen_width, screen_height):
        self.frame = frame
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

    def show_choice_imge(self):
        # メッセージボックスのリサイズ
        ctb_filename = "./message.png"
        ctb = Image.open(ctb_filename)
        width_c = round(self.screen_width/2)
        height_c = round(self.screen_height/12)
        ctb_resize = ctb.resize((width_c, height_c))
        ctb_resize.save('./message_choice.png', quality=95)
        ctb_filename = "./message_choice.png"

        # 選択肢表示用のメッセージボックス配置
        global c_txtbox_img
        c_txtbox_img = tkinter.PhotoImage(file=ctb_filename)

        for ch in range(4):
            txtbox_id = self.canvas.create_image(
                round(self.screen_width*1/3),
                height_c/2+height_c*ch,
                image=c_txtbox_img,
                tag="textbox_"+str(ch)
            )
            # choice_txtbox_id.append(txtbox_id)
            # メッセージボックスの中心を取得
            txtbox_pos = self.canvas.bbox("textbox_"+str(ch))
            tb_x = txtbox_pos[2]-(txtbox_pos[2]-txtbox_pos[0])/2
            tb_y = txtbox_pos[3]-(txtbox_pos[3]-txtbox_pos[1])/2

            # 仮置きの選択肢を配置
            self.canvas.create_text(tb_x, tb_y, text="", font=Q_FNT, fill="white", width=round(
                self.screen_width*2/5), tag="choice_"+str(ch))

        self.canvas.pack(side=tkinter.TOP)


"""
def create_ending_frame():
    root.destroy()
    #ending_frame = tkinter.Frame(root0,width=screen_width,height=screen_height,bg="white")
    #endtxt = tkinter.Label(ending_frame,text="YOU DIED")
    #endtxt.pack()
    bi.show_image()
"""


# タイマーカウントダウン関数
def count_down(button, choice_canvas, question_canvas, root, screen_height, screen_width, question_frame, choice_frame, label_timer, character):
    global tmr, stop_counter
    if stop_counter:
        stop_counter = False
        return
    tmr -= 1
    label_timer["text"] = tmr
    if tmr == 0:
        for i in range(4):
            button[i]["state"] = "disable"
        label_timer["text"] = "Time Over"
        label_timer.update()
        tmr = 30
        label_timer["text"] = tmr
        label_timer.update()
        character[1].attack()
        character[0].damage()
        if character[0].life > 0 and character[1].life > 0:
            q_id = random.randint(1, question_list_len)
            q = db_handler.GetQuestionByID(q_id)[0]
            create_q_frame(q, choice_canvas, question_canvas, root, screen_height,
                           screen_width, question_frame, choice_frame, label_timer, character)
    else:
        root.after(1000, count_down, button, choice_canvas, question_canvas, root,
                   screen_height, screen_width, question_frame, choice_frame, label_timer, character)

# タイマーをリセットする関数


def reset(button, label_timer):
    global tmr, stop_counter
    tmr = 30
    label_timer["text"] = tmr
    label_timer.update()
    stop_counter = True


name_list = ["あなた", "スライム", "ケルベロス", "スケルトン", "ドラゴン", "キングスライム"]
file_list = ["./armor.png", "./slime.png", "./kerberos.png",
             "./skeleton.png", "./dragon.png", "./lastbossf.png"]
life_list = [300, 40, 80, 120, 160, 200]
#life_list = [10, 10, 10, 10, 10, 10]


class Middle(tkinter.Frame):

    def __init__(self, root0):

        tkinter.Frame.__init__(self, root0)

        #root0 = tkinter.Tk()
        root0.title("test")
        root0.state('zoomed')

        screen_width = root0.winfo_screenwidth()
        screen_height = root0.winfo_screenheight()

        root = tkinter.Frame(root0, width=screen_width, height=screen_height)
        root.grid()
        battle_frame = tkinter.Frame(
            root, width=screen_width, height=screen_height/2, padx=3, pady=3)

        # タイマー用ラベル
        label_timer = tkinter.Label(
            root, text=tmr, font=("sys", 30), bg="white")
        label_timer.place(x=50, y=50)

        canvas = tkinter.Canvas(
            battle_frame, width=screen_width, height=screen_height/2, bg="white")
        canvas.pack()
        canvas.propagate(0)
        battle_frame.grid(columnspan=2, column=0, row=0,
                          sticky=tkinter.W+tkinter.E)

        # キャラクター画像のリサイズ
        for file_name in file_list:
            image_filename = file_name
            img = Image.open(image_filename)
            #height = round(screen_height/3)
            #width = round(img.width * height / img.height)
            width = round(screen_width/5)
            height = round(img.height * width / img.width)
            img_resize = img.resize((width, height))
            img_resize = img_resize.save(file_name, quality=100)
            image_filename_resize = file_name

        # キャラクターの表示
        character = [
            GameCharacter(name_list[0], life_list[0], screen_width/2 - width, screen_height/5,
                          file_list[0], "LC", screen_width, canvas, root0, root),  # 画像ファイルの情報を別途追加
            GameCharacter(name_list[1], life_list[1], screen_width/2 + width, screen_height/5,
                          file_list[1], "RC", screen_width, canvas, root0, root)  # 画像ファイルの情報を別途追加
        ]

        character[0].draw()
        character[1].draw()

        # 選択肢表示部分
        # 選択肢のフレーム
        choice_frame = tkinter.Frame(
            root, width=screen_width*2/3, height=screen_height*2/3, padx=3, pady=3)
        choice_canvas = tkinter.Canvas(
            choice_frame, width=screen_width*2/3, height=screen_height/3)

        choice_images = choice_bg_image(
            choice_frame, choice_canvas, screen_width, screen_height)
        choice_images.show_choice_imge()

        # 問題文表示部分
        question_frame = tkinter.Frame(
            root, width=screen_width*1/3, height=screen_height/3, padx=3, pady=3)
        question_canvas = tkinter.Canvas(
            question_frame, width=screen_width*1/3, height=screen_height/3)

        # メッセージボックスのリサイズ
        qtb_filename = "./message.png"
        qtb = Image.open(qtb_filename)
        width_q = round(screen_width*1/3)
        height_q = round(screen_height*1/4)
        qtb_resize = qtb.resize((width_q, height_q))
        qtb_resize = qtb_resize.save('./message_question.png', quality=95)
        qtb_filename_resize = "./message_question.png"

        global q_txtbox_img
        q_txtbox_img = tkinter.PhotoImage(file=qtb_filename_resize)

        # 問題文表示用のメッセージボックス配置
        question_canvas.create_image(
            round(screen_width*1/6),
            height_q/2,
            image=q_txtbox_img,
            tag="question_textbox"
        )
        question_canvas.pack(side=tkinter.TOP)

        # メッセージボックス上に問題文を配置
        qtxtbox_pos = question_canvas.bbox("question_textbox")
        qtb_x = qtxtbox_pos[2]-(qtxtbox_pos[2]-qtxtbox_pos[0])/2
        qtb_y = qtxtbox_pos[3]-(qtxtbox_pos[3]-qtxtbox_pos[1])/2
        question_txt_id = question_canvas.create_text(
            qtb_x,
            qtb_y,
            text="",
            font=Q_FNT,
            fill="white",
            width=round(screen_width*3/10),
            tag="question")

        question_canvas.pack(side=tkinter.TOP)

        q_id = random.randint(1, question_list_len)
        question = db_handler.GetQuestionByID(q_id)[0]

        create_q_frame(question, choice_canvas, question_canvas, root, screen_height,
                       screen_width, question_frame, choice_frame, label_timer, character)

        #bi = end_bg_image("./game_over.png",screen_width,screen_height)


class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        # super().__init__(root)
        # self.pack()
        self._frame = None
        self.switch_frame(Top)
        # root.title("some title")
        # root.minsize(100, 100)
        # screen_width = root.winfo_screenwidth()
        # screen_height = root.winfo_screenheight()

    def switch_frame(self, frame_class, fin=""):
        new_frame = frame_class(self)
        if self._frame is not None or fin == "fin":
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


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
        button1.pack(side=tkinter.BOTTOM, expand=True)
        # button1.grid()
        # Message
        fontstyle = tkinter.font.Font(
            self, family="Helvetica", size=20, weight="bold")
        msg = tkinter.Label(self, text="RESULT", font=fontstyle)
        msg.pack(side=tkinter.TOP, expand=True)
        # msg.grid()
        # Text
        f = Font(family='Helvetica', size=16)
        v1 = tkinter.StringVar()
        #txt = tkinter.Text(self, height=round(master.winfo_screenheight()*3/10), width=round(master.winfo_screenwidth()*3/10))
        txt = tkinter.Text(self, height=15, width=60)
        txt.configure(font=f)
        for i in question_answered:
            if i[7] == i[-1]:
                mark = "〇"
            else:
                mark = "✖"
            txt.insert(
                1.0, f"{i[1]} : {i[2]}\n 正解{i[7]} あなたの解答{i[-1]}  {mark}\n\n")
        txt.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)
        # txt.grid()
        # Scrollbar
        scrollbar = tkinter.Scrollbar(
            self,
            orient=tkinter.VERTICAL,
            command=txt.yview)
        txt['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tkinter.RIGHT, expand=True, fill=tkinter.Y)
        # scrollbar.grid()


class Top(tkinter.Frame):
    def __init__(self, master):
        # Frame
        tkinter.Frame.__init__(self, master)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # self.grid()
        # キャンバスを設置

        title_canvas = tkinter.Canvas(
            self,
            width=screen_width,
            height=screen_height,
            bg="white",
            relief=tkinter.RAISED)
        title_canvas.grid()
        global title_img
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

        # 背景画像の上にタイトルを表示
        title_id = title_canvas.create_text(
            screen_width/2,
            screen_height/5,
            text="Jokakushi Quest",
            font=("Yu Gothic UI", 80),
            fill="black"
        )

        # 背景画像の上にタイトルを表示
        syutten_id = title_canvas.create_text(
            screen_width/2,
            screen_height*4/5,
            text="キャラクター画像出典:星乃だーつ　グーテンベルグの娘​  http://darts.kirara.st/​\n 空想曲線 https://kopacurve.blog.fc2.com/",
            font=("Yu Gothic UI", 15),
            fill="white"
        )

        # 開始ボタンを配置
        button_width = screen_width/6
        button_height = screen_height/12
        button = title_canvas.create_rectangle(
            screen_width*1/2 - button_width,
            screen_height*2/3 - button_height,
            screen_width*1/2 + button_width,
            screen_height*2/3 + button_height,
            fill="blue",
            tag="start_button"
        )

        # 背景画像の上にタイトルを表示
        start_id = title_canvas.create_text(
            screen_width/2,
            screen_height*2/3,
            text="Game Start!",
            font=("Yu Gothic UI", 40),
            fill="black",
            tag="start_text"
        )

        def start_game(event):
            master.switch_frame(Middle)

        # ボタンが押されたときに関数を呼び出す
        title_canvas.tag_bind(
            "start_button",
            "<ButtonPress>",
            start_game
        )
        # ボタンの文字部分が押されたときにも関数を呼び出す
        title_canvas.tag_bind(
            "start_text",
            "<ButtonPress>",
            start_game
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()

    #root0 = tkinter.Tk()
    #m = Middle(root0)
    # m.mainloop()
