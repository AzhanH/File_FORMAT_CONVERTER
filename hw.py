import sys
import os

args = sys.argv
arg = args[1] 
prog_file = args[0]
print(f'Hello {arg} from {prog_file}')

host = os.environ.get('HOST')
print(f'Connecting to host: {host}')


# print(f'Hello {arg}')