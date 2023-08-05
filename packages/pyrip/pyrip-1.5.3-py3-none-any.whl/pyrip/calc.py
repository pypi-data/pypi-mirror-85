import string
from .util import run_command


def calculate(infiles, outfile, expr, dtype=None):
    args = ['gdal_calc.py']
    asciis = string.ascii_uppercase
    for idx, infile in enumerate(infiles):
        args.extend(['-{}'.format(asciis[idx]), infile])
    args.append('--outfile={}'.format(outfile))
    args.append('--calc={}'.format(expr))
    if dtype is not None:
        args.append('--type={}'.format(dtype))
    run_command(args)
    return outfile
