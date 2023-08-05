import csv
import datetime
import inspect
import os
import shutil
import sys


def remove_file(file: str) -> None:
    """
    Removes file

    Parameters
    ----------
    file :
        path to file

    Returns
    -------

    """
    if os.path.isfile(file):
        os.remove(file)


def remove_all_files_from(directory: str) -> None:
    """
    Function to remove all files from a directory

    Parameters
    ----------
    directory : folder path

    Returns
    -------

    """
    try:
        for item in os.listdir(directory):
            file = os.path.join(directory, item)
            remove_file(file)
    except FileNotFoundError:
        print(directory + ' does not exist')


def copy_all_files(source: str, target: str):
    """
    Function to copy all files in a new folder

    Parameters
    ----------
    source : path (string) to the source folder
    target : path (string) to the target folder

    Returns
    -------

    """

    for item in os.listdir(source):
        path = os.path.join(source, item)
        if os.path.isfile(path):
            shutil.copy(path, target)


def create_directory_for(path: str, warn: bool = False) -> None:
    """
    Function to create a folder at a specific path

    Parameters
    ----------
    path : str

    Returns
    -------

    """
    if not os.path.exists(path):
        os.makedirs(path)
    elif warn:
        sys.stderr.write('WARNING: ' + path + ' exists already')
        sys.stderr.flush()


def format_float(value: float, decimals: int = 2) -> str:
    """
    Formatting value to string with given decimals

    Parameters
    ----------
    value :
        given value
    decimals :
        round to number of decimals

    Returns
    -------
    str:
        value as string
    """
    return f"{value:.{decimals}f}"


def write_to_file(filename: str, _list: [str], append: bool = False) -> None:
    """
    Writes given list of strings to file

    Parameters
    ----------
    filename :
        path to file
    _list :
        list with values as strings
    append :
        flag to append to file or (over)write file

    Returns
    -------
    None:
        None
    """
    with open(filename, 'a' if append else 'w', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=',')
        writer.writerow(_list)
    writeFile.close()


def all_non_abstract_subclasses_of(cls) -> list:
    """
    Generates a list of non-abstract subclass from given class

    Parameters
    ----------
    cls :
        given class

    Returns
    -------
    list:
        list with non-abstract subclasses
    """
    res = list()
    subs = set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_non_abstract_subclasses_of(c)])
    for sub in subs:
        if not inspect.isabstract(sub):
            res.append(sub)
    return res


def add_month_to(date: datetime.datetime) -> datetime.datetime:
    """
    Generates a new datetime object from given datetime object with a month added.
    If month is last month of year, it returns first month of next year.

    Parameters
    ----------
    date :
        given datetime object

    Returns
    -------
    datetime:
        new datetime object
    """
    if date.month == 12:
        date = date.replace(year=date.year + 1, month=1)
    else:
        date = date.replace(month=date.month + 1)
    return date


def add_year_to(date: datetime.datetime) -> datetime.datetime:
    """
    Generates a new datetime object from given datetime object with a year added.

    Parameters
    ----------
    date :
        given datetime object

    Returns
    -------
    datetime:
        new datetime object
    """
    return date.replace(year=date.year + 1)


def get_year_from(tstmp: float) -> float:
    """
    Calculates year from given timestamp

    Parameters
    ----------
    tstmp :
        given timestamp in epoch time

    Returns
    -------
    float :
        year of given epoch timestamp
    """
    return datetime.datetime.fromtimestamp(tstmp).year


def get_maximum_from(values: list) -> float:
    """
    Gets maximum value from given values

    Parameters
    ----------
    values :
        list of values

    Returns
    -------
    float:
        maximum value from given list
    """
    if values:
        max_value: float = max(values)
    else:
        max_value: float = 0.0
    return max_value


def get_average_from(values: list) -> float:
    """
    Calculates average from given value list

    Parameters
    ----------
    values :
        list of values

    Returns
    -------
    float:
        average from values
    """
    if values:
        average_value: float = sum(values) / len(values)
    else:
        average_value: float = 0.0
    return average_value
