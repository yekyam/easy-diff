'''
Simple diff tool for command line
TODO: Add a simple console support that has two panes, one per file side by side
TODO: Refactor to only open the files once
'''

import sys
from os.path import exists

from colorama import Fore, init, Style
from rich import print as rprint
from rich import columns

init()

def make_error_list(file1_lines, file2_lines):
	errors = []
	for linenum, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
		for posnum, (c1, c2) in enumerate(zip(line1, line2)):
			if c1 != c2:
				errors.append(f'{linenum}:{posnum}')
	return errors

def gen_report(file1_lines, file2_lines, errors):
	file1_chars = [list(x) for x in file1_lines]
	file2_chars = [list(x) for x in file2_lines]
	for error in errors:
		line_num, pos_num = error.split(':')
		line_num = int(line_num)
		pos_num = int(pos_num)
		correct_char = file1_chars[line_num][pos_num]
		if len(file2_chars[line_num])-1 >= pos_num:
			wrong_char = file2_chars[line_num][pos_num]
			file2_chars[line_num][pos_num] = f'{Fore.RED}{wrong_char}{Style.RESET_ALL}'
		file1_chars[line_num][pos_num] = f'{Fore.GREEN}{correct_char}{Style.RESET_ALL}'

	file1_list = [''.join(line) for line in file1_chars]
	file2_list = [''.join(line) for line in file2_chars]
	
	return '\n'.join(file1_list), '\n'.join(file2_list)

def main():
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	if not exists(file1) or not exists(file2):
		print(f"Couldn't find {file1} or {file2}")
	else:
		with open(file1) as f1, open(file2) as f2:
			file1_lines = f1.read().split('\n')
			file2_lines = f2.read().split('\n')
		errors = make_error_list(file1_lines, file2_lines)
		report1, report2 = gen_report(file1_lines, file2_lines, errors)
		print(f'{file1}:\n', report1)
		print(f'{file2}:\n', report2)

if __name__ == '__main__':
	main()