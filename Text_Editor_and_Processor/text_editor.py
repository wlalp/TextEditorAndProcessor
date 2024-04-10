'''This is the module housing the text editor window'''
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as tksc
from tkinter import filedialog, font
import time
from text_processor import TextProcessor
from pathlib import PurePath

class TextEditor(tk.Tk):
    '''
        A class for a Tkinter window containing a text editor with word processing capabilities

        Attributes:
        open_file : str -- the path of the current open file
        processor: Text_Processor -- the text processor used for processing the text files
        filename : str -- the name of the current file
    '''
    _open_file = False
    _tp = TextProcessor('')
    _dir = _tp.file

    def __init__(self)->None:
        '''Constructor for the text editor window'''
        super().__init__()
        self.occ_window = None
        self.font_window = None
        self.font_box = None
        
        ico_dir = PurePath(__file__).parent
        ico_dir = ico_dir / 'mruler.ico'

        self.title('M-Ruler')
        self.geometry("1600x900")
        self.resizable(True,True)
        self.iconbitmap(ico_dir)

        main_frame = Frame(self)
        main_frame.pack()

        text_frame = Frame(main_frame,width=600,height=700)
        text_frame.propagate(0)
        text_frame.pack(pady=5,side=TOP)

        self.font = font.Font(family="Arial",size=12)

        self.main_text = tksc.ScrolledText(text_frame, width =1,height = 1,wrap="none",
        font = self.font,selectbackground = "blue",undo = True)

        horizontal_scrollbar = Scrollbar(text_frame, orient="horizontal",
        command= self.main_text.xview)

        self.main_text.configure(xscrollcommand= horizontal_scrollbar.set)
        self.main_text.pack(fill="both",expand=True)
        horizontal_scrollbar.pack(fill= X)

        main_menu = Menu(self)
        self.config(menu= main_menu)

        file_menu = Menu(main_menu, tearoff = False)
        main_menu.add_cascade(label="File", menu = file_menu)
        self.character_counter_label = Label(self,text="chars:", anchor= W)

        self.status_bar = Label(self, text='Ready     ',anchor = E)
        self.status_bar.pack(fill=X,side=BOTTOM,ipady=5)

        self.character_counter_label.pack(side=BOTTOM)

        self.processing_label = Label(self,text='Ready to Process')
        self.processing_label.pack(side=TOP,fill=X,pady=5)

        autosave_button = Button(main_frame,text= "Autosave",command= self.autosave)
        autosave_button.pack(side = LEFT,anchor= W,fill=Y,pady=3)

        file_menu.add_command(label="New",command = self.new_file)
        file_menu.add_command(label="Open",command = self.open_text_file)
        file_menu.add_command(label="Save",command = self.save_file,accelerator= "Ctrl+S")

        file_menu.bind_all('<Control-s>',self.save_file)

        file_menu.add_command(label="Save As",command = self.save_as)

        file_menu.add_separator()
        file_menu.add_command(label="Exit",command = self.quit)

        edit_menu = Menu(main_menu, tearoff = False)
        main_menu.add_cascade(label="Edit", menu = edit_menu)

        edit_menu.add_command(label="Undo", command= self.main_text.edit_undo,accelerator= "Ctrl+Z")
        edit_menu.add_command(label="Redo", command= self.main_text.edit_redo,accelerator= "Ctrl+Y")

        edit_menu.bind_all('<Control-z>',lambda e: self.main_text.edit_undo)
        edit_menu.bind_all('<Control-y>', lambda e: self.main_text.edit_redo)

        function_menu = Menu(main_menu,tearoff = False)

        main_menu.add_cascade(label="Processing", menu = function_menu)

        function_menu.add_command(label="Count Lines",command = self.count_lines)
        function_menu.add_command(label="Count Words",command = self.count_words)
        function_menu.add_command(label="Count Occurences",command = self.open_occurence_window)

        preference_menu = Menu(main_menu,tearoff = False)
        main_menu.add_cascade(label="Preferences",menu= preference_menu)
        preference_menu.add_checkbutton(label="Toggle Word Wrap",command= self.toggle_word_wrap)

        font_menu = Menu(preference_menu,tearoff=False)
        preference_menu.add_cascade(label="Font",menu=font_menu)
        font_menu.add_checkbutton(label="Bold Text",command=self.set_bold)
        font_menu.add_checkbutton(label="Italic Text",command=self.set_italics)
        font_menu.add_command(label="Font Size",command= self.open_font_dialog)
        self.new_file()

    @property
    def open_file(self)->str:
        '''Getter for the current open file'''
        return self._open_file

    @open_file.setter
    def open_file(self,file: str)->None:
        '''Setter for the current open file

            Parameters:
            file : str -- A string representing the new desired open file
        '''
        self._open_file = file

    @property
    def processor(self)-> TextProcessor:
        '''Getter for the text processor'''
        return self._tp

    @property
    def filename(self)->str:
        '''Attribute containing the name of the file to be edited'''
        name = self.open_file
        if self.open_file:
            text_file = self.open_file
            name = text_file
            paths = name.split("/")
            name = paths.pop()
        return name

    def new_file(self)->None:
        '''Clears the main textbox and is representative of a new file.'''
        self.main_text.delete(1.0,END)
        self.title('New File - M-Ruler')
        self.status_bar.config(text ="New File     ")
        self.processing_label.config(text ="Ready to Process")
        self.open_file = False
        self.show_character_count()

    def open_text_file(self)->None:
        '''Opens a chosen file as text within the editor'''
        self.main_text.delete(1.0,END)
        try:
            text_file = filedialog.askopenfilename(initialdir= self._dir,title = "Open File",
            filetypes=(("Text Files","*.txt"),("CSV Files","*.csv"),
            ("JSON Files","*.json"),("Python Files","*.py")))
            name = None
            if text_file:
                self.open_file = text_file
                name = text_file
            self.status_bar.config(text=name)
            paths = name.split("/")
            name = paths.pop()

            self.title(f'{name} - M-Ruler')

            self.processing_label.config(text = f'Ready to Process: {name}')

            with open(text_file,'r',encoding="UTF-8") as file:
                text = file.read()
            self.main_text.insert(END,text)
            self.update_processor()
            self.show_character_count()
        except FileNotFoundError:
            print("Unable to find the file to open")
        except:
            print("Unable to open the text file, file dialog was most likely aborted before selecting a file")

    def save_as(self)->None:
        '''Saves the contents of the main textbox as a text file'''
        try:
            text_file = filedialog.asksaveasfilename(
            initialdir= self._dir,defaultextension=".*",title = "Save File As",
            filetypes=(("Text Files","*.txt"),("CSV Files","*.csv"),
            ("JSON Files","*.json"),("Python Files","*.py")))

            if text_file:
                name = text_file
                self.status_bar.config(text=f'Saved: {name}')
                paths = name.split("/")
                name = paths.pop()
                self.title(f'{name} - M-Ruler')

                self.processing_label.config(text = f'Able to Process: {name}')

                with open(text_file,'w',encoding="UTF-8") as file:
                    file.write(self.main_text.get(1.0,END))
                    self.open_file = text_file
                self.update_processor()
                self.show_character_count()
        except FileNotFoundError:
            print("File does not exist")

    def save_file(self,event = None)->None:
        '''Saves the open file. If the file does not exist, a save-as file dialog will show'''
        if self.open_file:
            with open(self.open_file,'w',encoding="UTF-8") as file:
                file.write(self.main_text.get(1.0,END))

            self.status_bar.config(text=f'Saved: {self.open_file}')
            name = self.open_file
            paths = name.split("/")
            name = paths.pop()
            self.processing_label.config(text = f'Able to Process: {name}')
        else:
            self.save_as()

    def update_processor(self)->None:
        '''Updates the text processor with the current filename'''
        self._tp = TextProcessor(self.filename)

    def count_lines(self)->None:
        '''Displays the number of lines in the current file'''
        self.update_processor()
        if self.check_file() is False:
            self.save_as()
        self.update_processor()
        try:
            num_of_lines = self._tp.count_lines()
            self.processing_label.config(text= f'Number of lines = {num_of_lines}')
        except FileNotFoundError:
            print(f"The file {self.processor.fname} does not exist.")


    def count_occurence(self,word: str)->None:
        '''Displays the number of occurences of a given word

            Parameters:
            word : str -- the desired word to be counted
        '''

        self.update_processor()
        if self.check_file() is False:
            self.save_as()
        self.update_processor()
        try:
            occs = self._tp.count_occurences(word)
            self.processing_label.config(text= f'Number of occurences of "{word}" = {occs}')
            self.occ_window.destroy()
        except Exception:
            print("Something went wrong, make sure you have a file open.")

    def count_words(self)->None:
        '''Displays the number of words in the current file'''
        self.update_processor()
        if self.check_file() is False:
            self.save_as()
        self.update_processor()
        try:
            words = self._tp.count_words()
            self.processing_label.config(text= f'Word Count = {words}')
        except FileNotFoundError:
            print("The file does not exist.")
        except Exception:
            print("Something went wrong, make sure you have a file open.")

    def check_file(self)->bool:
        '''Checks whether or not the processor's filename is an empty string,
        and whether or not it is existent'''
        if(self.processor.fname == '' or not self.processor.fname):
            isfile = False
        else:
            isfile = True
        return isfile

    def autosave(self)-> None:
        '''Automatically saves the file every ten seconds'''
        if self.check_file() is False:
            self.save_as()
            self.after(10000,self.autosave)
        else:
            self.save_file()
            save_time = time.localtime()
            save_time = time.strftime('%H :%M :%S  [%p] of %a, %b %d')
            self.status_bar.config(text=f'Auto-saved: {self.open_file} at {save_time}')
            self.after(10000,self.autosave)

    def open_occurence_window(self)->None:
        '''Opens a window to accept user input for a desired word to count'''
        self.occ_window = tk.Toplevel(self)
        self.occ_window.title("Count Occurences")
        self.occ_window.geometry("300x200")
        entry_box = Entry(self.occ_window,bd= 5)
        entry_box.pack()

        submit_button = Button(self.occ_window,text="Submit" ,
        command=lambda: self.count_occurence(entry_box.get()))

        submit_button.pack()
        self.occ_window.mainloop()

    def show_character_count(self)->None:
        '''Updates the character counter'''
        count = len(self.main_text.get(1.0,END))
        self.character_counter_label.config(text=f"characters: {str(count)}")
        self.after(2000,self.show_character_count)

    def no_space_character_count(self)-> None:
        '''Updates the character counter without including spaces'''
        txt = [char for char in self.main_text.get(1.0,END) if char.isspace() is False and char != "\n"]
        count = len(txt)
        self.character_counter_label.config(text=f"characters: {str(count)}")
        self.after(2000,self.no_space_character_count)

    def set_bold(self)->None:
        '''Toggles bold text'''
        if self.font.cget("weight") == "bold":
            self.font.config(weight=NORMAL)
        else:
            self.font.config(weight="bold")

    def set_italics(self)->None:
        '''Toggles italic text'''
        if self.font.cget("slant") == "italic":
            self.font.config(slant= "roman")
        else:
            self.font.config(slant= "italic")

    def change_font_size(self,event)->None:
        '''Changes the size of the text box's font'''
        self.font.configure(size=self.font_box.get(self.font_box.curselection()))

    def open_font_dialog(self)->None:
        '''Creates font dialog popup window'''
        self.font_window = tk.Toplevel(self)
        self.font_window.title("Change Font Size")
        self.font_window.geometry("100x200")
        font_sizes = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
        size_var = tk.Variable(value= font_sizes)
        self.font_box = Listbox(self.font_window,listvariable=size_var,selectmode=SINGLE)
        self.font_box.pack()
        self.font_box.bind('<ButtonRelease-1>',self.change_font_size)
        

    def toggle_word_wrap(self)->None:
        '''Toggles word wrapping in textbox'''
        if self.main_text.cget("wrap") ==  WORD:
            self.main_text.config(wrap= "none")
        else:
            self.main_text.config(wrap= WORD)
