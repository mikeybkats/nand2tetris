# with blocks and with keyword
# file like objects
# context managers
# binary vs text mode

import sys
# sys.getdefaultencoding()
# // utf-8

# modes:
# r, w, a – read, write, append
# selector:
# b, t – binary mode, text mode
# wt = write text mode
f = open('wasteland.txt', mode='wt', encoding='utf-8')
# move to the end of the file with read()
f.read()
# append to the file
f.write('What are the roots that clutch')

# seek sends the pointer back to the beginning of the file.
f.seek(0)
# seek cannot move to arbitrary offset. 0 and values from tell() are the only values allowed.
# readline is much better than read
f.readline()
f.readline()
f.seek(0)
f.readlines()  # returns all the lines as a list

# notice at append mode active
h = open('wasteland.txt', mode='at', encoding='utf-8')
h.writelines()
# close must be called to write the file
h.close()
