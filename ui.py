import tkinter.messagebox
from tkinter import *
from tkinter import font

from PIL import ImageTk, Image
import random as rd

BACKGROUND_COLOR = "#5d6d7e"
FONT_COLOR = "#eca829"
SPEED_TIME_MIN = 1
BEGINNER_PARAGRAPHS = [
    "The sun shines in the blue sky. Birds sing sweet melodies. Children play in the park. Everything feels perfect this morning.",
    "The moon appears behind the clouds. The night is calm and cool. The stars light up the dark sky. It is a moment of peace and quiet.",
    "The cat sleeps next to the window. Its soft purring fills the room. Outside, the rain falls slowly. The sound is relaxing for everyone.",
    "Anna has a new book. She reads every page with attention. The story is very exciting. She can’t wait to know the ending."
]

INTERMEDIATE_PARAGRAPHS = [
    "Yesterday, the weather was so bad that many people decided to stay indoors. Heavy rain and strong winds made it impossible to go outside. Those who ventured out faced challenges like flooded streets and falling branches.",
    "The city park has become a popular spot for families on weekends. Parents can relax under the trees while children enjoy the playground. Occasionally, live music performances are organized, adding to the lively atmosphere.",
    "Sarah was nervous before her big presentation at work. She had spent weeks preparing and wanted everything to go perfectly. Despite her worries, she delivered her speech with confidence, earning praise from her colleagues.",
    "John's love for cooking began when he was a child. He used to watch his grandmother prepare delicious meals for the family. Now, he experiments with new recipes and shares his creations with friends.",
    "Learning a new language can be challenging, but it is also very rewarding. Many people find that practicing daily and engaging with native speakers helps them improve quickly. Persistence is the key to success.",
    "The small village was known for its beautiful scenery and friendly inhabitants. Tourists often visited to experience the peaceful lifestyle and enjoy traditional food. Over time, the village has become a cherished destination.",
    "Emma found an old diary while cleaning the attic. It belonged to her great-grandmother and was filled with stories from the past. Reading it gave her a deeper connection to her family's history."
]

ADVANCED_PARAGRAPHS = [
    "In the realm of quantum physics, the concept of superposition challenges traditional notions of reality. Particles can exist in multiple states simultaneously until observed, a phenomenon that has profound implications for our understanding of the universe.",
    "The economic policies implemented during the early 20th century laid the foundation for modern financial systems. These reforms, though controversial at the time, introduced stability and fostered growth in an era of uncertainty.",
    "Exploring the dense rainforests of the Amazon requires resilience and meticulous planning. Researchers must contend with unpredictable weather, dangerous wildlife, and the challenge of navigating an ever-changing landscape.",
    "The works of Shakespeare remain unparalleled in their ability to capture the complexities of human emotions. His plays continue to be studied and performed, revealing timeless themes that resonate across cultures and generations.",
    "Advancements in artificial intelligence have revolutionized industries such as healthcare and transportation. The ability to process vast amounts of data quickly has enabled breakthroughs that were once thought impossible.",
    "The construction of ancient pyramids is a testament to the ingenuity and perseverance of early civilizations. Despite limited technology, these architectural marvels have withstood the test of time, intriguing historians and engineers alike.",
    "The intricate balance of ecosystems is crucial for maintaining biodiversity. Disruptions caused by human activity can lead to cascading effects, highlighting the urgent need for sustainable practices to protect the environment."
]

class TypeSpeedTest(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Typing Speed Test App")
        self.config(pady=40, padx=40, bg=FONT_COLOR)
        self.in_principal = True
        self.levels = ['Beginner','Intermediate','Advanced']
        self.index = 0
        self.correct_w = 0
        self.current_idx = '1.0'
        self.incorrect_w = 0
        self.running = False
        self.timer = None
        self.time_left = None
        self.random_paragraph = ""
        self.menu_principal()
        self.mainloop()

    def menu_principal(self):
        self.canvas = Canvas(width=700, height=600)
        self.app_text_menu = self.canvas.create_text(
            350, 70, text="Typing Speed Test", font=('TkMenuFont', 40, 'bold')
        )
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)

        try:
            self.image_1 = Image.open("images/type-fast-picture.png").resize((300, 300))
            self.test = ImageTk.PhotoImage(self.image_1)
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "Image file not found!")
            self.destroy()
            return

        self.label_image = Label(image=self.test, pady=15)
        self.label_image.grid(row=0, column=0, columnspan=2)

        self.start_button = Button(text="Start Test", width=8, command=self.change_board)
        self.start_button.place(x=300, y=480)

        self.select_difficult_label = Label(text="Select a difficult")
        self.select_difficult_label.place(x=300,y=530)

        self.listbox = Listbox(height=3,width=10)
        for level in self.levels:
            self.listbox.insert(self.levels.index(level), level)
        self.listbox.bind("<<ListboxSelect>>", self.get_level)
        self.listbox.place(x=430, y=530)

    def get_level(self,difficult):
            array_paragraph = []
            if difficult == 'Beginner':
                 array_paragraph = BEGINNER_PARAGRAPHS
            elif difficult == 'Intermediate':
                array_paragraph =  INTERMEDIATE_PARAGRAPHS
            elif difficult == "Advanced":
                array_paragraph = ADVANCED_PARAGRAPHS
            return array_paragraph

    def change_board(self):

        try:
            difficult = self.listbox.get(self.listbox.curselection())
            self.in_principal = False
            self.listbox.place_forget()
            self.select_difficult_label.place_forget()
            self.setting_buttons(self.in_principal)

            self.paragraph_difficult = self.get_level(difficult)
            self.random_paragraph = rd.choice(self.paragraph_difficult)
            self.setting_text_paragraph(self.random_paragraph)
            self.setting_entry_text()
            self.setting_time()
            self.set_scores()

        except TclError:
            tkinter.messagebox.showwarning(title='No difficult selected', message="Please. Select a difficult to continue.")
            return

    def setting_buttons(self, state):
        if not state:
            self.start_button.place_forget()
            self.canvas.itemconfig(self.app_text_menu, text="TYPING SPEED TEST", font=('Doto', 40, "normal"))
            self.label_image.destroy()

            self.restart_button = Button(text="Restart", command=self.restart_time, width=8)
            self.restart_button.place(x=15, y=350)

            self.wpm_label = Label(self.canvas,text="WPM:  0", font=('Arial',14),fg='white')
            self.wpm_label.place(x=15,y=400)

            self.cpm_label = Label(self.canvas,text="CPM:  0",font=('Arial',14), fg='white')
            self.cpm_label.place(x=15,y= 430)

    def setting_time(self):
        self.time_label = Label(text="Time Left: ", font=("Arial", 22, "bold"), highlightthickness=0)
        self.time_label.place(x=15, y=250)

        self.timer_text = self.canvas.create_text(150, 265, text="60", fill='White', font=('Arial', 20, 'bold'))

    def setting_entry_text(self):
        self.paragraph.focus()
        self.entry_text = Entry(width=30)
        self.entry_text.place(x=320, y=420)

        self.bind("<space>", self.on_space_pressed)
        self.bind("<Key>", lambda event: self.start_timer())

    def setting_text_paragraph(self, paragraph):
        font_paragraph = font.Font(family='Arial', size=12, weight='bold')

        frame = Frame(self)
        frame.place(x=250, y=180)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.paragraph = Text(
            frame,
            height=15,
            width=60,
            font=font_paragraph,
            wrap=WORD,
            yscrollcommand=scrollbar.set
        )
        self.paragraph.pack()

        scrollbar.config(command=self.paragraph.yview)

        self.paragraph.insert(END, paragraph)
        self.paragraph.mark_set("insert", "%d.%d" % (1, 0))
        self.paragraph.bind("<Key>", lambda e: "break")
        self.highlight_current_word()

    def on_space_pressed(self,event=None):
        self.compare_word(self.entry_text.get().strip(), self.random_paragraph)
        self.highlight_current_word()

    def compare_word(self, word, paragraph):
        paragraph = paragraph.split()
        if self.index < len(paragraph):
            if word == paragraph[self.index]:
                self.correct_w += 1
                self.correct_words_label.config(text=f"Correct words: {self.correct_w}")
            else:
                self.incorrect_w += 1
                self.incorrect_words_label.config(text=f"Incorrect words: {self.incorrect_w}")
            self.entry_text.delete("0", END)
            self.index += 1

            wpm = self.calculate_wpm()
            corrected_wpm = self.calculate_cpm()
            self.wpm_label.config(text=f"WPM: {wpm:.2f}")
            self.cpm_label.config(text=f"Corrected CPM: {corrected_wpm:.2f}")

        else:
            self.game_over()


    def highlight_current_word(self,event=None):

        self.paragraph.tag_remove('highlight','1.0',END)
        word_start = self.paragraph.search(r'\S', self.current_idx, regexp=True, stopindex=END)
        if not word_start:
            self.current_idx = '1.0'
            return

        word_end = self.paragraph.search(r'\s', word_start, regexp=True, stopindex=END)
        if not word_end:
            word_end = END

        self.paragraph.tag_add('highlight',word_start,word_end)
        self.paragraph.tag_config("highlight",foreground='black',background='green')
        self.current_idx = word_end

    def set_scores(self):
        self.correct_words_label = Label(text=f"Correct words: {self.correct_w}", highlightthickness=0)
        self.correct_words_label.place(x=200, y=500)

        self.incorrect_words_label = Label(text=f"Incorrect words: {self.incorrect_w}", highlightthickness=0)
        self.incorrect_words_label.place(x=400, y=500)

    def start_timer(self):
        if not self.running:
            self.running = True
            real_time = SPEED_TIME_MIN * 60
            self.count_down(real_time)

    def count_down(self, count):
        self.time_left = count
        count_sec = count % 60
        self.canvas.itemconfig(self.timer_text, text=f"{count_sec}")
        if count > 0:
            self.timer = self.after(1000, self.count_down, count - 1)
        else:
            self.game_over()
            self.entry_text.config(state='normal')

    def restart_time(self):
        self.after_cancel(self.timer)
        self.running = False
        self.entry_text.config(state='normal')
        if self.entry_text.get() != '':
            self.entry_text.delete('0',END)
        self.canvas.itemconfig(self.timer_text, text="60")
        self.paragraph.delete("1.0", END)
        self.random_paragraph = rd.choice(self.paragraph_difficult)

        self.paragraph.insert(END, self.random_paragraph)
        self.correct_w = 0
        self.incorrect_w = 0
        self.index = 0
        self.current_idx = '1.0'
        self.correct_words_label.config(text=f"Correct words: {self.correct_w}")
        self.incorrect_words_label.config(text=f"Incorrect words: {self.incorrect_w}")
        self.highlight_current_word()



    def game_over(self):
        self.entry_text.config(state='disabled')
        self.after_cancel(self.timer)
        wpm = self.calculate_wpm()
        cpm = self.calculate_cpm()
        tkinter.messagebox.showinfo(
            title="Results",
            message=f"Your score is: {cpm} CPM (that is {wpm} WPM)"
        )

    def calculate_wpm(self):
        total_time_min = (SPEED_TIME_MIN * 60 - self.time_left)/60
        wpm = self.correct_w / total_time_min
        return wpm

    def calculate_cpm(self):
        total_chars_correct = self.correct_w * 5
        total_time_min = (SPEED_TIME_MIN*60 - self.time_left)/60
        cpm = total_chars_correct/total_time_min
        return cpm


if __name__ == "__main__":
    TypeSpeedTest()
