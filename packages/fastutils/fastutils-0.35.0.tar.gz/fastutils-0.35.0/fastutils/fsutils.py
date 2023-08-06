# -*- coding: utf-8 -*-

import os
import datetime
import time
import tempfile
import shutil
from .randomutils import uuid4

def mkdir(folder):
    os.makedirs(folder, exist_ok=True)
    return os.path.exists(folder) and os.path.isdir(folder)

def rm(filename):
    """Make sure a file or a directory has been deleted.
    """
    if os.path.exists(filename):
        if os.path.isfile(filename):
            os.unlink(filename)
        else:
            shutil.rmtree(filename, ignore_errors=True, onerror=None)
        return not os.path.exists(filename)
    else:
        return True

def filecopy(src, dst, dst_is_a_folder=False):
    if dst_is_a_folder:
        src_name = os.path.basename(src)
        dst = os.path.join(dst, src_name)
    shutil.copy2(src, dst)

def treecopy(src, dst, keep_src_folder_name=True):
    if keep_src_folder_name:
        src_name = os.path.basename(src)
        dst = os.path.join(dst, src_name)
    shutil.copytree(src, dst)

def copy(src, dst, keep_src_folder_name=True, dst_is_a_folder=False):
    if os.path.exists(src):
        if os.path.isfile(src):
            filecopy(src, dst, dst_is_a_folder)
        else:
            treecopy(src, dst, keep_src_folder_name)

def pathjoin(path1, path2):
    return os.path.join(path1, path2)


def readfile(filename, binary=False, encoding="utf-8"):
    if binary:
        with open(filename, "rb") as fobj:
            return fobj.read()
    else:
        with open(filename, "r", encoding=encoding) as fobj:
            return fobj.read()

def write(filename, data, encoding="utf-8"):
    if isinstance(data, bytes):
        with open(filename, "wb") as fobj:
            fobj.write(data)
    else:
        with open(filename, "w", encoding="utf-8") as fobj:
            fobj.write(data)


def get_temp_workspace(prefix="", makedir=True):
    folder_name = prefix + str(uuid4())
    path = os.path.abspath(os.path.join(tempfile.gettempdir(), folder_name))
    if makedir:
        mkdir(path)
    return path

def rename(filepath, name):
    """Only change filename or directory name, but CAN not change the path, e.g. /a/b.txt -> /a/c.txt is ok, /a/b.txt -> /b/b.txt is NOT ok.
    """
    name = os.path.basename(name)
    folder = os.path.dirname(filepath)
    dst = os.path.abspath(os.path.join(folder, name))
    os.rename(filepath, dst)
    return dst

def move(src, dst):
    os.rename(src, dst)

def file_content_replace(filename, original, replacement, binary=False, encoding="utf-8", recursive=True, ignore_errors=True):
    file_replaced = []
    file_failed = {}

    def replace(filename, original, replacement, binary=False, encoding="utf-8"):
        content = readfile(filename, binary, encoding)
        content = content.replace(original, replacement)
        write(filename, content, encoding)

    if os.path.isfile(filename):
        try:
            replace(filename, original, replacement, binary, encoding)
            file_replaced.append(filename)
        except Exception as error:
            file_failed[path] = error
            if not ignore_errors:
                raise error
    else:
        folder = filename
        for root, dirs, files in os.walk(folder):
            for filename in files:
                path = os.path.abspath(os.path.join(root, filename))
                try:
                    replace(path, original, replacement, binary, encoding)
                    file_replaced.append(path)
                except Exception as error:
                    file_failed[path] = error
                    if not ignore_errors:
                        raise error

    return file_replaced, file_failed

def touch(filename):
    """Make sure a file exists
    """
    if os.path.exists(filename):
        os.utime(filename, (time.time(), time.time()))
    else:
        with open(filename, "wb") as fobj:
            pass
    return os.stat(filename)

def expand(filename):
    """Expand user and expand vars.
    """
    return os.path.abspath(os.path.expandvars(os.path.expanduser(filename)))

def expands(*filenames):
    """Expand user and expand vars for the given filenames.
    """
    results = []
    for filename in filenames:
        results.append(expand(filename))
    return results

def first_exists_file(*filenames, default=None):
    """Return the first exists file's abspath. If none file exists, return None.
    """
    for filename in filenames:
        filename = expand(filename)
        if os.path.exists(filename):
            return filename
    return default

def get_application_config_filepath(appname, name="config", suffix="yml"):
    """Get application config filepath by search these places:
        ./{appname}-{name}.{suffix}
        ./conf/{appname}-{name}.{suffix}
        ./etc/{appname}-{name}.{suffix}
        ~/.{appname}/{name}.{suffix}
        ~/{appname}/{name}.{suffix}
    """
    return first_exists_file(
        "./{0}-{1}.{2}".format(appname, name, suffix),
        "./conf/{0}-{1}.{2}".format(appname, name, suffix),
        "./etc/{0}-{1}.{2}".format(appname, name, suffix),
        "~/.{0}/{1}.{2}".format(appname, name, suffix),
        "~/{0}/{1}.{2}".format(appname, name, suffix),
    )

def info(filename):
    ext = os.path.splitext(filename)[1]
    stat = os.stat(filename)
    return {
        "ext": ext,
        "abspath": os.path.abspath(filename),
        "size": stat.st_size,
        "atime": datetime.datetime.fromtimestamp(stat.st_atime),
        "ctime": datetime.datetime.fromtimestamp(stat.st_ctime),
        "mode": stat.st_mode,
    }



size_unit_names = [
    "B",
    "KB",
    "MB",
    "GB",
    "TB",
    "PB",
    "EB",
    "ZB",
    "YB",
]

size_unit_upper_limit = [1024 ** (index+1) for index, _ in enumerate(size_unit_names)]

def get_size_deviation(unit_name):
    unit_name = unit_name.upper()
    x = size_unit_names.index(unit_name)
    return 1 - (1000 ** x) / (1024 ** x)

def get_unit_size(unit_name, kb_size=1024):
    """base is the size of KB, choices are 1000 or 1024.
    """
    unit_name = unit_name.upper()
    if not unit_name.endswith("B"):
        unit_name += "B"
    return kb_size ** size_unit_names.index(unit_name)

def get_size_display(size_in_bytes):
    """10 => 10B, 1024 => 1KB, 5.6*1024 => 5.6KB
    """
    final_index = 0
    final_upper_limit = 1
    for index, upper_limit in enumerate(size_unit_upper_limit[:-1]):
        if upper_limit > size_in_bytes:
            break
        final_index = index + 1
        final_upper_limit = upper_limit
    return "{0:.2f}".format(size_in_bytes/final_upper_limit).rstrip("0").rstrip(".") + size_unit_names[final_index]
