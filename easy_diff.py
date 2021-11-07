'''
Easy diff tool made in python with Tkinter
'''
from functools import partial

import tkinter as tk

def make_error_list(file1_lines, file2_lines):
	'''Generates an error list of tuples.

	:param file1_lines: the first file's lines in a list
	:type file1_lines: list[str]
	:param file2_lines: the second file's lines in a list
	:type file2_lines: list[str]
	:returns: a list of tuples indicating the line number and error positions
	:rtype: list
	'''
	errors = []
	for linenum, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
		for posnum, (c1, c2) in enumerate(zip(line1, line2)):
			if c1 != c2:
				errors.append((linenum+1, posnum))
		if len(line1) < len(line2):
			errors.append((linenum+1, f'{len(line1)}-'))
	return errors

def color_error_text(text, errors, color):
	'''Colors the given text object at the specified positions with the given color
	
	:param text: a tkinter text object
	:type text: tkinter.Text
	:param errors: a list of error positions
	:type errors: list
	:param color: a color
	:type color: str
	'''
	for error in errors:
		match error[1]:
			case str():
				text.tag_add(str(error), f'{error[0]}.{int(error[1][:-1])}', tk.END)
			case _:
				text.tag_add(str(error), f'{error[0]}.{error[1]}', f'{error[0]}.{error[1]+1}')
		text.tag_config(str(error), background='white', foreground=color)

def show_report(text1, text2):
	'''Gets the text from the text widgets, generates the error list, and colors the text
	
	:param text1: text widget
	:type text1: tkinter.Text()
	:param text2: text widget
	:type text2: tkinter.Text()
	'''
	lines1 = text1.get('1.0', tk.END).split('\n')
	lines2 = text2.get('1.0', tk.END).split('\n')
	error_list = make_error_list(lines1, lines2)
	color_error_text(text2, error_list, 'red')
	color_error_text(text1, error_list, 'green')

def main():
	window = tk.Tk()
	window.title('Easy Diff')
	window.columnconfigure(0, weight=1)
	window.columnconfigure(1, weight=1)
	text1 = tk.Text()
	text2 = tk.Text()
	text1.grid(column=0, row=0, padx=5, pady=5)
	text2.grid(column=1, row=0, padx=5, pady=5)
	btn_show_diff = tk.Button(text='Show Changes', width=100, command=partial(show_report, text1, text2))
	btn_show_diff.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
	window.mainloop()

if __name__ == '__main__':
	main()