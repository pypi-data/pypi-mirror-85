import string
from .util import run_command


def calculate(infiles, outfile, expr, nodata_val=None, dtype=None, all_bands=None):
    args = ['gdal_calc.py']
    asciis = string.ascii_uppercase
    for idx, infile in enumerate(infiles):
        args.extend(['-{}'.format(asciis[idx]), infile])
    args.append('--outfile={}'.format(outfile))
    args.append('--calc={}'.format(expr))
    if nodata_val is not None:
        args.append('--NoDataValue={}'.format(nodata_val))
    if dtype is not None:
        args.append('--type={}'.format(dtype))
    if all_bands is not None:
        args.append('--allBands={}'.format(all_bands))
    args.append('--overwrite')
    run_command(args)
    return outfile
