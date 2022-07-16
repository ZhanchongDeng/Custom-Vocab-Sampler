#!/usr/bin/env python3
##coding=gbk
import pandas as pd
import numpy as np
from pathlib import Path
#from tkinter import *
import tkinter
from tkinter import N,W,E,S
from tkinter import ttk
from tkinter import font as tkFont

class CustomQuizlet:
    def __init__(self, root):
        self.root = root
        root.title("Custom Quizlet")

        mainframe = ttk.Frame(root)
        mainframe.grid(column=3, row=3, sticky=(N, W, E, S), padx=10, pady=5)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.word_definition = tkinter.StringVar()
        self.display_current_word()
        self.mistakes = []

        tkinter.Label(mainframe, 
            textvariable=self.word_definition, 
            height=20, 
            width=100,
            borderwidth=3, 
            relief="ridge",
            font = tkinter.font.Font(size=18)
        ).grid(column=2, row=2, sticky = (W,E))

        tkinter.Button(mainframe, text="Next", command=self.next).grid(column=3, row=2)
        tkinter.Button(mainframe, text="Previous", command=self.previous).grid(column=1, row=2)
        tkinter.Button(mainframe, text="flip", command=self.flip_word).grid(column=2, row=3)
        tkinter.Button(mainframe, text="star", command=self.star).grid(column=3, row=1)

        self.progress_bar = tkinter.StringVar()
        self.update_progress_bar()
        tkinter.Label(mainframe, textvariable=self.progress_bar).grid(column=2, row=1)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=10, pady=10)

        root.bind("<space>", self.flip_word)
        root.bind("<Left>", self.previous)
        root.bind("<Right>", self.next)
        root.bind("<Return>", self.star)

    def flip_word(self, *args):
        try:
            if not self.showWord:
                self.display_current_word()
            else:
                self.display_current_definition()
                
        except:
            print("flip word failed")
            pass

    def next(self, *args):
        try:
            if self.root.idx + 1 < len(self.root.df):
                self.root.idx += 1
                self.display_current_word()
                self.update_progress_bar()
            else:
                if len(self.mistakes):
                    self.root.df = self.mistakes
                    self.mistakes = []
                    self.root.idx = 0
                    self.display_current_word()
                    print(f"Well done, you have {len(self.root.df)} mistakes. Keep going.")
                else:
                    self.word_definition.set("You are done!!!")
                self.update_progress_bar()
        except:
            print("next failed")
            pass

    def previous(self, *args):
        try:
            if self.root.idx - 1 >= 0:
                self.root.idx -= 1
                self.display_current_word()
                self.update_progress_bar()
        except:
            print("next failed")
            pass
    
    def star(self, *args):
        print("star called")
        entry = self.root.df[self.root.idx]
        if not entry[2]:
            print(f"starring {entry[0]}")
            self.mistakes.append(np.copy(entry))
            print(self.mistakes)
            self.root.df[self.root.idx][2] = True

    def update_progress_bar(self, *args):
        progress_bar_str = f"{self.root.idx+1} of {len(self.root.df)}"
        self.progress_bar.set(progress_bar_str)

    def display_current_word(self, *args):
        word = self.root.df[self.root.idx][0]
        try:
            self.word_definition.set(word)
            self.showWord = True
        except:
            print("display_current_word failed")
            pass

    def display_current_definition(self, *args):
        definition = self.root.df[self.root.idx][1]
        try:
            self.word_definition.set(definition)
            self.showWord = False
        except:
            print("display_current_word failed")
            pass


def main():
    vocab_fp = Path("data.csv")
    df_vocab = pd.read_csv(vocab_fp, encoding="GBK")
    print("���������˹�")
    print()

    start = input("where to start(count from 0)?\n")
    start = int(start)
    num_words = input("how many words?\n")
    end = start + int(num_words)
    df = df_vocab.iloc[start:end][["����","����"]]
    df['starred'] = False
    print(f"memorizing {start} to {end}")
    df = df.sample(frac=1).reset_index(drop=True).to_numpy()

    root = tkinter.Tk()
    root.df = df
    root.idx = 0
    CustomQuizlet(root)
    root.mainloop()

if __name__ == "__main__":
    main()




'''

self.sw = "short word"
self.ld = "1)long definition\n2)you really think it's this easy huh, well sike.\n3)I am stilllll goinggggggggggggggggkafjaklj sakdjflaj jk;kja kjf ljkjlaljk"

prompt="\n\
h   -   show this prompt\n\
w   -   show current word\n\
f   -   show definition\n\
n   -   move to next word (need to do w again after this)\n\
b   -   move to previous word (need to w again)\n\
s   -   move word to mistakes\n\
end -   I am done :(\n\n"

def get_day_vocab(df, day):
    start, end = (day-1) * 300, day * 300
    return df.iloc[start:end]

def command_prompt():
    vocab_fp = Path("data.csv")
    df_vocab = pd.read_csv(vocab_fp, encoding="GBK")
    print("���������˹�")
    print()

    #day = input("����������")
    #df = get_day_vocab(df_vocab, int(day))[["����","����"]]
    start = input("where to start(count from 0)?\n")
    start = int(start)
    num_words = input("how many words?\n")
    end = start + int(num_words)
    df = df_vocab.iloc[start:end][["����","����"]]
    print(f"memorizing {start} to {end}")
    df = df.sample(frac=1).reset_index(drop=True).to_numpy()
    idx = 0
    starred = False
    mistakes = []
    
    print(prompt)

    while True:
        if idx >= len(df):
            if len(mistakes) == 0:
                print("congrats, u r truly done")
                return
            df = mistakes
            idx = 0
            print(f"congrats! u finished, u have {len(mistakes)} mistakes word. press w")
            mistakes = []
        command = input()
        if command == "end":
            break
        elif command == "w":
            print("-" * 10)
            print()

            print(df[idx][0])

            print()
            print("-" * 10)
        elif command == "f":
            print("-" * 10)
            print()

            print(df[idx][1])

            print()
            print("-" * 10)
        elif command == "n":
            idx += 1
            print("press w again for me :)")
            starred = False
        elif command == "b":
            idx -= 1
            print("press w again for me :)")
            starred = False
        elif command == "h":
            print(prompt)
        elif command == "s":
            if not starred:
                mistakes.append(df[idx])
                starred = True
                print("added to mistakes")
            else:
                print("already starred move on bro")
        else:
            print("invalid command talk to tech support aka ur bf")
'''