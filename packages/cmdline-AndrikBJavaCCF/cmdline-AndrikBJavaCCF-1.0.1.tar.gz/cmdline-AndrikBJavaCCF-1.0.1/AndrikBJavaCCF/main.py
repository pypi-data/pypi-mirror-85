import sys

from .file import File
from .formatter import get_files, get_files_rec, fix, validate, start_tests

__version__ = "1.0.1"


def print_help():
    print(
        """
***************** examples *****************
AndrikBJavaCCF --verify -(p|d|f) /..
AndrikBJavaCCF -v -(p|d|f) /..
AndrikBJavaCCF --fix -(p|d|f) /..
AndrikBJavaCCF -f  -(p|d|f) /..
AndrikBJavaCCF --help
AndrikBJavaCCF -h
AndrikBJavaCCF --test
AndrikBJavaCCF -t
where :
-p - project
-d - directory
-f - file
/.. - path to project, directory or file
        """
    )


def main():
    if len(sys.argv) == 1:
        print("Error! Please, write arguments", '\n')
        print_help()
    else:
        if sys.argv[1] in ('-h', '--help'):
            print_help()
        elif sys.argv[1] in ('-t', '--test'):
            start_tests()
        elif len(sys.argv) != 4:
            print("Error! Please, write arguments\n")
            print_help()
        else:
            mode = sys.argv[1]
            if len(mode) > 2:
                mode = mode[1:3]

            p_d_f = sys.argv[2]
            path = sys.argv[3]

            if p_d_f == '-p':
                files = get_files_rec(path)
            elif p_d_f == '-d':
                files = get_files(path)
            else:
                files = [path]

            for i in range(len(files)):
                files[i] = File(files[i])

            if mode == '-v':
                validate(files)
            else:
                fix(files)
