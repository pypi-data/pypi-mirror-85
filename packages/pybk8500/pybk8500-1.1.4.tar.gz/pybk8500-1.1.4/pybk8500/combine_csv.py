import os


__all__ = ['combine_csv_files', 'main']


def get_filename(*files, default='output.csv', suffix='_combined'):
    """Return the filename from the given tuple of files."""
    for f in files:
        if isinstance(f, str):
            split = os.path.splitext(str(f))
            return split[0] + suffix + split[1]
    return default


def combine_csv_files(*files, output=None, skip_headers=True):
    """Combine csv files into one file.

    Args:
        *files (tuple): Tuple of filenames, file objects, or io.BytesIO objects to read data from.
        output (str)[None]: Output filename.
        skip_headers (bool)[True]: Do not write CSV headers to the new file. If this is false groups of data will be
            separated by the header.

    Returns:
        output (str): Output filename that the data was written to.
    """
    if len(files) < 2:
        raise ValueError('Must give at least 2 files in order to combine them.')

    if output is None:
        output = get_filename(*files)

    with open(output, 'wb') as o:
        for file in files:
            if isinstance(file, str):
                # Open the file and write contents
                with open(file, 'rb') as f:
                    for line in f:
                        if not skip_headers or b'Time' not in line:
                            o.write(line)
            else:
                # File object, io.BytesIO as binary. You need to close it yourself.
                for line in file:
                    if not isinstance(line, bytes):
                        line = line.encode('utf-8')
                    if not skip_headers or b'Time' not in line:
                        o.write(line)

    return output


main = combine_csv_files


if __name__ == '__main__':
    import argparse

    P = argparse.ArgumentParser(description='Plot an output CSV file.')
    P.add_argument('filenames', type=str, nargs='+', help='Filenames to read in and plot.')
    P.add_argument('-o', '--output', default=None, type=str, help='Output filename.')
    P.add_argument('-s', '--skip_headers', default=True, type=bool,
                   help='Skip writing the headers to file. This makes the file one giant CSV with no separators.')
    ARGS = P.parse_args()

    main(*ARGS.filenames, output=ARGS.output, skip_headers=ARGS.skip_headers)
