from functools import partial

import tkinter as tk

def make_error_list(file1_lines, file2_lines):
	errors = []
	for linenum, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
		for posnum, (c1, c2) in enumerate(zip(line1, line2)):
			if c1 != c2:
				errors.append((linenum+1, posnum))
		if len(line1) < len(line2):
			errors.append((linenum+1, f'{len(line1)}-'))
	return errors

def color_error_text(text2, errors):
	for error in errors:
		match error[1]:
			case str():
				text2.tag_add(str(error), f'{error[0]}.{int(error[1][:-1])}', tk.END)
			case _:
				text2.tag_add(str(error), f'{error[0]}.{error[1]}', f'{error[0]}.{error[1]+1}')
		text2.tag_config(str(error), background='white', foreground='red')

def show_report(text1, text2):
	lines1 = text1.get('1.0', tk.END).split('\n')
	lines2 = text2.get('1.0', tk.END).split('\n')
	color_error_text(text2, make_error_list(lines1, lines2))

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