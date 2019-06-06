"""Usage: counted_example.py --help
       counted_example.py -v...
       counted_example.py go [go]
       counted_example.py (--path=<path>)...
       counted_example.py <file> <file>

"""
from docopt import docopt


print(docopt(__doc__))