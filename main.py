from argparse import ArgumentParser
from os import listdir
from os.path import join
import re
import pypdf as pdf
from subprocess import call,run, Popen, PIPE
URI_REGEX="((\w+:\/\/).+)"
class MainArgs:
    files: list[str]
    verbose: bool = False

def main(args: MainArgs) -> int:
    files = args.files
    urls = dict()
    for file in files:
        lines = Popen(f"strings {file} | grep URI", shell=True, stdout=PIPE, encoding='utf-8').stdout.readlines()
        urls[file] = []
        for line in lines:
            result = re.findall(URI_REGEX, line)
            if len(result) == 0:
                continue

            link = result[0][0].split('>>')[0][:-1]
            link = link.replace('\\(', '$$')
            link = link.replace('\\)', '%%')
            link = link.split(')')[0]
            link = link.replace('$$','(' )
            
            link = link.replace('%%',')' )
            urls[file].append(link)
            
    for file, links in urls.items():
        print("In file:", file, "found", len(links), "links")

    return 0


if __name__ == '__main__':
    parser = ArgumentParser(
        'doDOI', description="Parse PDFs to find DOI urls", add_help=True)
        
    parser.add_argument('-v', '--verbose',
                        help="Output verbosity", action='store_true')
    
    parser.add_argument('-f', '--files',
                        help="Search only these PDF files", action='store', nargs='*')
    
    parser.add_argument('-d', '--directory',
                        help="Search all PDFs in this directory", action='store', type=str)
    

    args = parser.parse_args()
    if args.files is None:
        args.files = []

    if args.directory is not None:
        for filename in listdir(args.directory):
            filename = join(args.directory, filename)
            if filename.endswith('.pdf') and filename not in args.files:
                args.files.append(filename)

    ret = main(args)
    exit(ret)
