'''This module contains a class with text processing capabilites'''
from pathlib import PurePath

class TextProcessor():
    '''
    A class for processing text files

    Attributes:
    fname : str -- the name of the given file
    file : str -- the path of the given file
    '''
    def __init__(self,filename : str) -> None:
        '''Constructor for text processor object

            Parameters:
            file : str -- the name of the file to be processed
        '''
        try:
            self._fname = filename
            _dir = PurePath(__file__)
            _dir = _dir.parent
            _dir = _dir / "Text Files" /self._fname
            self._file = _dir
        except TypeError:
            print("There is no file to process, please save the file before processing")
    def __repr__(self) -> str:
        '''Returns a string representation of the processor,
        and the name of the file to be processed.'''

        tp_str = f"Processing file: {self._fname}"
        return tp_str

    @property
    def fname(self)->str:
        '''Getter for filename'''
        return self._fname

    @fname.setter
    def fname(self,file_name)-> None:
        '''Setter for filename'''
        self._fname = file_name

    @property
    def file(self)->PurePath:
        '''Getter for file attribute, a value containing the file's path'''
        return self._file

    def count_words(self)->int:
        '''Counts the number of words in the document'''
        words = self.get_words()
        return len(words)

    def count_chars(self)->int:
        '''Counts the number of characters in the file'''
        fstr = self.to_string()
        count = len(fstr)
        return count

    def reverse(self)->str:
        '''Reverses the file's text'''
        fstr = self.to_string()
        rstr = ''.join(reversed(fstr))
        return rstr

    def count_empty_lines(self)->int:
        '''Reads the file and counts the number of blank lines'''
        count = 0
        with open(self._file,'r', encoding="UTF-8") as file:
            for line in file:
                if(line.isspace() or len(line) == 0):
                    count = count + 1
        return count

    def count_whitespace(self)->int:
        '''Counts how many characters in the file are whitespace'''
        count = 0
        fstr = self.to_string()
        for char in fstr:
            if char.isspace():
                count = count+1
        return count

    def get_ascii_vals(self)->list[int]:
        '''Returns the ascii values of all characters in the file'''
        values = []
        fstr = self.to_string()
        for char in fstr:
            values.append(ord(char))
        return values

    def is_empty(self)->bool:
        '''Checks whether or not the file is completely empty'''
        is_empty = None
        with open(self._file, 'r',encoding="UTF-8") as file:
            is_empty = bool(file.read() == '')
        return is_empty

    def count_lines(self)->int:
        '''This method counts the number of lines in the given text file.'''
        try:
            with open(self._file, 'r',encoding="UTF-8") as file:
                lines = file.readlines()
                num_lines = len(lines)
            return num_lines
        except FileNotFoundError:
            print("The given file does not exist")
            return 0
        except PermissionError:
            print("Permission Denied: The given file is most likely a folder, please use a text file")
            return 0
        except AttributeError:
            print("No file is prepared for processing")

    def to_string(self)->str:
        '''Reads the file as a string'''
        try:
            with open(self._file, 'r',encoding="UTF-8") as file:
                fstr = file.read()
            return fstr
        except FileNotFoundError:
            print("The given file does not exist")
            return None
        except PermissionError:
            print("The given file is most likely a folder, please use a text file")
            return None
    def strip_punct(self):
        '''Removes punctuation from the files text'''
        punc = ['.',',','!','?',':',';','(',')','"']
        fstr = self.to_string()
        for p_mark in punc:
            fstr = fstr.translate({ord(p_mark): None})
        fstr = fstr.replace(' - ',' ')
        return fstr
    def get_words(self)->list[str]:
        '''Builds a list of the words in the text file'''
        words = self.strip_punct()
        words = words.replace('\n'," ")
        word_list =  words.split(" ")
        word_list = [word for word in word_list if word != '']
        for word in word_list:
            if(word.isspace() or word == '-'):
                word_list.remove(word)
            word = word.strip().lower()
        return word_list
    def most_frequent(self)-> tuple[str,int]:
        '''Finds the most frequent word in the file'''
        word_counts = self.get_word_counts()
        most_freq = max(word_counts, key =lambda count: count[1])
        return most_freq
    def top_most_frequent(self) ->list[tuple]:
        '''Returns the top ten most frequent words in the file'''
        most_frequent = self.get_word_counts()
        sorted_freq = sorted(most_frequent,key =lambda count: count[1], reverse= True)
        top_ten = []
        count = 0
        try:
            while count < 10:
                top_ten.append(sorted_freq[count])
                count += 1
        except IndexError:
            print("There are less than 10 words in this file")
        return top_ten
    def get_word_counts(self)-> list[tuple]:
        '''Creates a list of tuples containing (word,count) pairs'''
        words = self.get_words()
        word_set = set(words)
        word_counts = []
        for word in word_set:
            num = words.count(word)
            word_counts.append((word,num))
        return word_counts
    def count_occurences(self, word: str) -> int:
        '''Counts the number of occurences of a given word

            Parameters:
            word : str -- the given word for counting
        '''
        word = word.lower()
        words = [word.lower() for word in self.get_words()]
        count = 0
        if word in words:
            count = words.count(word)
        else:
            print(f"The given word [{word}] was not found.")
        return count
    def no_space_count_chars(self)-> int:
        '''Counts the characters in the file without including spaces'''
        fstr = self.to_string()
        count = 0
        for char in fstr:
            if char.isspace() or char == "\n":
                continue
            count += 1
        return count

    def get_unique_characters(self)->set[str]:
        '''Returns a set of all unique characters in the file'''
        char_set= [char.lower() for char in self.to_string()]
        char_set = set(char_set)
        return char_set
