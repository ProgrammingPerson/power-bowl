from tkinter import *
from tkinter import ttk
from time import sleep
from random import randint

class TossUp:
    def __init__(self, question, answer, category):
        self.question = question
        self.answer = answer
        self.category = category

class App:

    def __init__(self, root):
        self.powers = 0
        self.tens = 0
        self.negs = 0
        self.points = self.powers * 15 + self.tens * 10 - self.negs * 5
        self.tu_seen = 0
        self.speed_score = 0
        self.speed = 0
        self.question_text = ""
        self.tossups = []
        self.read = False
        self.root = root
        self.random = BooleanVar()
        self.random.set(True)
        self.index = 0
        
        categories = ["science", "history", "fine_arts", "philosophy", "social_science", "religion", "mythology", "geography"]

        for c in categories:
            questions = open(f"hs_questions/{c}.txt", "r", encoding="utf-8")

            tus = questions.readlines()

            for i in range(0, len(tus), 2):
                q = tus[i].replace("Question: ", "")
                a = tus[i + 1].replace("Answer: ", "")
                self.tossups.append(TossUp(q, a, c))

            questions.close()

        self.tu = self.tossups[self.index]

        self.root.title("Power Bowl")

        frm = ttk.Frame(root, width=1800, height=700, padding=75)
        frm.grid(column=0, row=0, sticky=(N, W, E, S))
        frm.columnconfigure(0, weight=1)
        frm.rowconfigure(0, weight=1)

        self.stats = ttk.Label(frm, font=("", 16) , text=f"{self.points} pts. --- {self.powers}/{self.tens}/{self.negs} at {self.tu_seen} tossups seen with {self.speed:.2f} celerity")
        self.stats.grid(column=1, row=1, sticky=(S), padx=350, pady=10)

        self.question = ttk.Label(frm, text=self.question_text, wraplength=700, font=("", 16))
        self.question.grid(column=1, row=4)

        self.random_btn = ttk.Checkbutton(frm, text="Random", variable=self.random, offvalue=False, onvalue=True)
        self.random_btn.grid(column=2, row=0)

        self.next_btn = ttk.Button(frm, text="Next", command=self.read_tossup, width=20)
        self.next_btn.grid(column=2, row=1)
        self.buzz_btn = ttk.Button(frm, text="Buzz", command=self.buzz, width=20)
        self.buzz_btn.grid(column=2, row=2)
        self.pause_btn = ttk.Button(frm, text="Pause", command=self.pause, width=20)
        self.pause_btn.grid(column=2, row=3, pady=10)

        self.ans_label = ttk.Label(frm, text="Answer:", font=("", 16))
        self.ans_label.grid(column=1, row=5, pady=50)

        self.ans_form = ttk.Entry(frm, width=100)
        self.ans_form.grid(column=1, row=6)
        self.ans_form.bind("<Return>", self.check_answer)

    def read_tossup(self):
        self.hide_answer()
        if self.random:
            self.index = randint(0, len(self.tossups) - 1)
            self.tu = self.tossups[self.index]
        else:
            self.index += 1
            if self.index == len(self.tossups):
                self.index = 0
            self.tu = self.tossups[self.index]
        self.question_text = ""
        self.read = True
        self.update_question_text(0)

    def update_question_text(self, i):
        if i < len(self.tu.question) and self.read:
            self.question_text += self.tu.question[i]
            self.question.config(text=self.question_text)
            self.root.after(25, self.update_question_text, i + 1)

    def buzz(self):
        self.read = False
        self.ans_form.focus_set()

    def pause(self):
        if self.read:
            self.read = False
        else:
            self.read = True
            self.update_question_text(len(self.question_text))

    def show_answer(self):
        self.ans_label.config(text=f"Answer: {self.tu.answer}")
        self.question.config(text=self.tu.question)

    def hide_answer(self):
        self.ans_label.config(text="Answer:")

    def check_answer(self, event):
        user_answer = self.ans_form.get().strip().lower()
        correct_answer = self.tu.answer.strip().lower()

        if user_answer == correct_answer or user_answer in correct_answer:
            self.tu_seen += 1
            self.speed_score += (len(self.tu.question) - len(self.question_text)) / len(self.tu.question)
            self.speed = self.speed_score / self.tu_seen
            if not "*" in self.question_text:
                self.points += 15
                self.powers += 1
                self.show_answer()
            else:
                self.points += 10
                self.tens += 1
            self.stats.config(text=f"{self.points} pts. --- {self.powers}/{self.tens}/{self.negs} at {self.tu_seen} tossups seen with {self.speed:.2f} celerity")
            self.ans_form.delete(0, END)
            self.show_answer()
        else:
            self.negs += 1
            self.points -= 5
            self.stats.config(text=f"{self.points} pts. --- {self.powers}/{self.tens}/{self.negs} at {self.tu_seen} tossups seen with {self.speed:.2f} celerity")
            self.ans_form.delete(0, END)
            self.show_answer()

root = Tk()
root.state('zoomed')
App(root)
root.mainloop()