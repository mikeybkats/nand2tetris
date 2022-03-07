# Process file: LBYL (look before you leap)

import os

p = './myFile.txt'


def read_LBYL():
	if os.path.exists(p):
		process_file(p)
	else:
		print(f'No such file as {p}')


# Process file: EAFP (easier to ask forgiveness than permission)
# EAFP works because it removes the error handing from the program flow
def read_EAFP():
	try:
		process_file(f)
	except OSError as e:
		print(f'Error: {e}')
