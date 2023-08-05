import matplotlib.pyplot as plt
import numpy as np
from pybk8500.utils import parse_number


__all__ = ['parse_csv', 'plot_csv_file', 'main']


def parse_csv(file, delimiter=','):
    """Parse the given csv resuls file.

    Args:
        file (str/FileObject/object): Filename or file object to read data from.
        delimiter (str)[',']: String separator for the csv.

    Returns:
        header (str)[None]: List of Header columns
    """
    header = None
    data = []
    filename_given = False
    if isinstance(file, str):
        file = open(file, 'r')
        filename_given = True

    idx = 0
    d = np.zeros(shape=(2*16, 4), dtype=np.float32)

    for line in file:
        if delimiter in line:
            v = [s.strip() for s in line.split(delimiter)]
            if 'Time' in v[0]:
                if header is None:
                    header = v
                if idx > 0:
                    data.append(d[:idx])
                idx = 0
                d = np.zeros(shape=(2*16, 4), dtype=np.float32)
            else:
                # Save values
                d[idx] = (parse_number(v[0]), parse_number(v[1]), parse_number(v[2]), parse_number(v[3]))
                idx += 1
                if idx >= len(d):
                    d = np.append(d, np.zeros(shape=(2*16, 4), dtype=np.float32), axis=0)

    # Append the last section of data
    data.append(d[:idx])

    if filename_given:
        file.close()

    return header, data


def plot_csv_file(filename, delimiter=','):
    header, data = parse_csv(filename, delimiter=delimiter)
    if not isinstance(filename, str):
        filename = filename.name

    plots = []
    for i, section in enumerate(data):
        fig, ax = plt.subplots()
        plots.append(fig)
        ax.set_xlabel(header[0])
        ax.set_ylabel('{}, {}, {}'.format(*header[1:]))
        if len(data) > 1:
            ax.set_title('Run {} [{}]'.format(i+1, filename))
        else:
            ax.set_title('{}'.format(filename))

        for j in range(1, section.shape[1]):
            ax.plot(section[:, 0], section[:, j], label=header[j])
        ax.legend()

    plt.show()
    return plots


main = plot_csv_file


if __name__ == '__main__':
    import argparse

    P = argparse.ArgumentParser(description='Plot an output CSV file.')
    P.add_argument('filename', default=None, type=str, help='Filename to read in and plot.')
    P.add_argument('-d', '--delimiter', default=',', type=str, help='Data separator (delimiter).')
    ARGS = P.parse_args()

    main(ARGS.filename, delimiter=ARGS.delimiter)
