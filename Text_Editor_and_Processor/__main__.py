'''
This is the main module, it demonstrates the text processor
as well as opens the text editor window.
'''

from text_processor import TextProcessor
from text_editor import TextEditor

def main():
    '''Main method demonstrating the capabilities of the text processor class'''
    print("The following is a demonstration of the methods in the text_processor class on the file 'test7.txt'")
    print("---")

    ex_text_processor = TextProcessor('test7.txt')
    my_str = ex_text_processor.to_string()
    lines = ex_text_processor.count_lines()
    print("There are this many lines in the file:",lines)

    occurences = ex_text_processor.count_occurences('text')
    print("The file contains the word 'text' this many times:",occurences)
    print("The file as a string:\n",my_str)
    print("Is the file empty?",ex_text_processor.is_empty())
    print("This is the file without punctuation:\n",ex_text_processor.strip_punct())
    print("The file has this many words:",ex_text_processor.count_words())
    print("Number of characters =",ex_text_processor.count_chars())
    print("This is the file in reverse:\n",ex_text_processor.reverse())
    print("This is a list of this files ascii values:\n",ex_text_processor.get_ascii_vals())
    print("The file has this many whitespaces:",ex_text_processor.count_whitespace())
    print("The file contains this many empty lines:",ex_text_processor.count_empty_lines())

    print("This is the most frequent word and it's count:",ex_text_processor.most_frequent())
    print(ex_text_processor.top_most_frequent())


if __name__ == "__main__":
    main()
    te = TextEditor()
    te.mainloop()
