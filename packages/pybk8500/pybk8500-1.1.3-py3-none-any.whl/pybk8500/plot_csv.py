import os
import numpy as np
import matplotlib.pyplot as plt
from pybk8500.utils import parse_number


__all__ = ['parse_csv', 'plot_csv_file', 'plot_csv_files', 'main']


def parse_csv(file, delimiter=','):
    """Parse the given csv results file.

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


def plot_csv_file(filename, title=None, xlabel=None, ylabel=None, legend=True, delimiter=',', split=True, show=True):
    """Plot a single csv file.

    Args:
        filename (str/FileObject/io.BytesIO): filename or file object to read in and plot.
        title (str)[None]: Plot title
        xlabel (str)[None]: Plot X axis label
        ylabel (str)[None]: Plot Y axis label
        legend (bool)[True]: Show the legend.
        delimiter (str)[',']: CSV Delimiter
        split (bool)[True]: If True Split each file and each section of data into a new plot.
        show (bool)[True]: If True show the plots (possibly blocking).

    Returns:
        plots (list): List of plot figures.
    """
    header, data = parse_csv(filename, delimiter=delimiter)
    if not isinstance(filename, str):
        try:
            filename = filename.name
        except (AttributeError, Exception):
            filename = 'Input Data'
    filename = os.path.basename(filename)

    plots = []
    if split:
        # Split every section of data into a separate plot
        for i, section in enumerate(data):
            fig, ax = plt.subplots()
            plots.append(fig)
            ax.set_xlabel(xlabel or header[0])
            ax.set_ylabel(ylabel or '{}, {}, {}'.format(*header[1:]))
            if len(data) > 1:
                ax.set_title(title or 'Run {} [{}]'.format(i+1, filename))
            else:
                ax.set_title(title or '{}'.format(filename))

            for j in range(1, len(header)):
                ax.plot(section[:, 0], section[:, j], label=header[j])

            if legend:
                ax.legend()

    else:
        # Show a single plot for all sections of data.
        fig, ax = plt.subplots()
        plots.append(fig)

        # Title, X and Y Label
        ax.set_title(title or '{}'.format(filename))
        ax.set_xlabel(xlabel or header[0])
        ax.set_ylabel(ylabel or '{}, {}, {}'.format(*header[1:]))

        data = np.vstack(data)
        for j in range(1, len(header)):
            ax.plot(data[:, 0], data[:, j], label=header[j])

        if legend:
            ax.legend()

    if show:
        plt.show()
    return plots


def plot_csv_files(*files, title=None, xlabel=None, ylabel=None, legend=True, delimiter=',', split=False, show=True):
    """Plot the given csv files.

    Args:
        *files (str/FileObject/io.BytesIO): filenames or file object to read in and plot.
        title (str)[None]: Plot title
        xlabel (str)[None]: Plot X axis label
        ylabel (str)[None]: Plot Y axis label
        legend (bool)[True]: Show the legend.
        delimiter (str)[',']: CSV Delimiter
        split (bool)[False]: If True Split each file and each section of data into a new plot.
        show (bool)[True]: If True show the plots (possibly blocking).

    Returns:
        plots (list): List of plot figures.
    """
    plots = []

    if split:
        # Plot every file separately
        for file in files:
            ps = plot_csv_file(file, title=title, xlabel=xlabel, ylabel=ylabel, legend=legend,
                               delimiter=delimiter, show=False)
            plots.extend(ps)

    else:
        # Plot every file and section of data in a single plot.
        header = None
        data = None
        folder = None
        for file in files:
            h, d = parse_csv(file, delimiter=delimiter)
            if folder is None:
                if not isinstance(file, str):
                    try:
                        file = file.name
                    except (AttributeError, Exception):
                        file = 'Input Data'
                folder = os.path.basename(os.path.dirname(os.path.abspath(file)))
            if header is None:
                header = h
            if data is not None:
                data = np.vstack([data] + d)
            else:
                data = np.vstack(d)

        # Create the plot
        fig, ax = plt.subplots()
        plots.append(fig)

        # Title, X and Y Label
        ax.set_title(title or '{}'.format(folder))
        ax.set_xlabel(xlabel or header[0])
        ax.set_ylabel(ylabel or '{}, {}, {}'.format(*header[1:]))

        for j in range(1, len(header)):
            ax.plot(data[:, 0], data[:, j], label=header[j])

        if legend:
            ax.legend()

    if show:
        plt.show()
    return plots


main = plot_csv_files


if __name__ == '__main__':
    import argparse

    P = argparse.ArgumentParser(description='Plot an output CSV file.')
    P.add_argument('filenames', type=str, nargs='+', help='Filenames to read in and plot.')
    P.add_argument('-t', '--title', default=None, type=str, help='Plot Title')
    P.add_argument('-x', '--xlabel', default=None, type=str, help='X Axis Label')
    P.add_argument('-y', '--ylabel', default=None, type=str, help='Y Axis Label')
    P.add_argument('-l', '--legend', default=True, type=bool, help='Show the plot legend.')
    P.add_argument('-d', '--delimiter', default=',', type=str, help='Data separator (delimiter).')
    P.add_argument('-s', '--split', default=False, type=bool, help='Split each file into different lines.')
    ARGS = P.parse_args()

    main(*ARGS.filenames, title=ARGS.title, xlabel=ARGS.xlabel, ylabel=ARGS.ylabel, legend=ARGS.legend,
         delimiter=ARGS.delimiter, split=ARGS.spit, show=True)
