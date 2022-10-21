import os
import pathlib

PATH_HERE = pathlib.Path(__file__).parent

def rewrite(root):
    l = str(root).rsplit("/", maxsplit=1)
    start = l[0]
    end = l[1]
    if '"' in end:
        end = end.split('"', maxsplit=1)
        end = end[1].rsplit('"', maxsplit=1)[0]
    elif end != "timeseries_data":
        splitequals = end.split("=")
        if len(splitequals) == 2:
            end = splitequals[1]

    newpath = start + "/" + end
    os.rename(root, newpath)

def rewrite_dirs(path):
    for root, _, _ in os.walk(path, topdown=False):
        rewrite(root)

rewrite_dirs(PATH_HERE / "timeseries_boolean")
rewrite_dirs(PATH_HERE / "timeseries_double")