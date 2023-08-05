"""
Various utilities that could be useful in several modules.
"""
import numbers
import sys
import os
import logging
import logging.config
import datetime
import time
from functools import wraps


def match_substrings(text, items, getstr=None, cmp=None, unmatched=False):
    """
    Matches each item from the items sequence with sum substring of the text
    in a greedy fashion. An item is either already a string or getstr is used
    to retrieve a string from it. The text and substrings are normally
    compared with normal string equality but cmp can be replaced with
    a two-argument function that does the comparison instead.
    This function expects that all items are present in the text, in their order
    and without overlapping! If this is not the case, an exception is raised.

    Args:
      text: the text to use for matching
      items: items that are or contains substrings to match
      getstr: a function that retrieves the text from an item (Default value = None)
      cmp: a function that compares to strings and returns a boolean \
    that indicates if they should be considered to be equal. (Default value = None)
      unmatched: if true returns two lists of tuples, where the second list\
    contains the offsets of text not matched by the items (Default value = False)

    Returns:
      a list of tuples (start, end, item) where start and end are the\
      start and end offsets of a substring in the text and item is the item for that substring.

    """
    if getstr is None:
        getstr = lambda x: x
    if cmp is None:
        cmp = lambda x,y: x == y
    ltxt = len(text)
    ret = []
    ret2 = []
    item_idx = 0
    start = 0
    lastunmatched = 0
    while start < ltxt:
        itemorig = items[item_idx]
        item = getstr(itemorig)
        end = start + len(item)
        if end > ltxt:
            raise Exception("Text too short to match next item: {}".format(item))
        if cmp(text[start:end], item):
            if unmatched and start > lastunmatched:
                ret2.append((lastunmatched, start))
                lastunmatched = start + len(item)
            ret.append((start, end, itemorig))
            start += len(item)
            item_idx += 1
            if item_idx == len(items):
                break
        else:
            start += 1
    if item_idx != len(items):
        raise Exception("Not all items matched but {} of {}".format(item_idx, len(items)))
    if unmatched and lastunmatched != ltxt:
        ret2.append((lastunmatched, ltxt))
    if unmatched:
        return ret, ret2
    else:
        return ret


start = 0
LOGGING_FORMAT = '%(asctime)s|%(levelname)s|%(name)s|%(message)s'


def init_logger(name=None, file=None, lvl=None, config=None, args=None):
    """
    Configure the root logger (this only works the very first time, all subsequent
    invocations will not modify the root logger). The root logger is initialized
    with a standard format the given log level and, if specified the outputs to the
    given file.

    The get a new logger for the given name is retrieved using the given name or
    the invoking command if None. It is also set to the given logging leve and returned.

    TODO: If file is not given but args is given and has "outpref" parameter, log to
    file "outpref.DATETIME.log" as well.

    Args:
        name: name to use in the log, if None, __name__
        file: if given, log to this destination in addition to stderr
        lvl: set logging level
        config: if specified, set logger config from this file
        args: not used yet

    Returns:
        A logger instance for name (always the same instance for the same name)
    """

    if name is None:
        name = sys.argv[0]
    if lvl is None:
        lvl = logging.INFO
    if config:
        # NOTE we could also configure from a yaml file or a dictionary, see
        # http://zetcode.com/python/logging/
        # see doc on logging.config
        logging.config.fileConfig(fname=config)
    # get the root logger
    rl = logging.getLogger()
    # NOTE: basicConfig does nothing if there is already a handler, so it only runs once, but we create the additional
    # handler for the file, if needed, only if the root logger has no handlers yet as well
    addhandlers = []
    fmt = logging.Formatter(LOGGING_FORMAT)
    hndlr = logging.StreamHandler(sys.stderr)
    hndlr.setFormatter(fmt)
    addhandlers.append(hndlr)
    if file and len(logging.getLogger().handlers) == 0:
        hndlr = logging.FileHandler(file)
        hndlr.setFormatter(fmt)
        addhandlers.append(hndlr)
    logging.basicConfig(level=lvl, handlers=addhandlers)
    # now get the handler for name
    logger = logging.getLogger(name)
    return logger


def run_start(logger=None, name=None, lvl=None):
    """
    Define time when running starts.

    Returns:
        system time in seconds
    """
    global start
    if logger is None:
        logger = init_logger(name=name, lvl=lvl)
    logger.info("Started: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")))
    start = time.time()
    return start


def run_stop(logger=None, name=None):
    """
    Log and return formatted elapsed run time.

    Returns:
        tuple of formatted run time, run time in seconds
    """
    if logger is None:
        logger = init_logger(name=name)
    logger.info("Stpped: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")))
    if start == 0:
        logger.warning("Run timing not set up properly, no time!")
        return "",0
    stop = time.time()
    delta = stop - start
    deltastr = str(datetime.timedelta(seconds=delta))
    logger.info(f"Runtime: {deltastr}")
    return deltastr, delta


def file4logger(thelogger, noext=False):
    """
    Return the first logging file found for this logger or None if there is no file handler.

    Args:
        thelogger: logger

    Returns:
        file path (string)
    """
    lpath = None
    for h in thelogger.handlers:
        if isinstance(h, logging.FileHandler):
            lpath = h.baseFilename
            if noext:
                lpath = os.path.splitext(lpath)[0]
            break
    return lpath


def support_annotation_or_set(method):
    """
    Decorator to allow a method that normally takes a start and end
    offset to take an annotation or annotation set, or any other object that has
    "start" and "end" attributes, or a pair of offsets instead.
    It also allows to take a single offset instead which will then be used
    to create a length one span (start is the original offset, end is the original offset plus one)

    Args:
      method: the method that gets converted by this decorator.

    Returns:
        the adapted method which now takes an annotation or annotation set as well as start/end offsets.
    """
    @wraps(method)
    def _support_annotation_or_set(self, *args, **kwargs):
        from gatenlp.annotation import Annotation
        annid = None
        if len(args) == 1:
            obj = args[0]
            if hasattr(obj, "start") and hasattr(obj, "end"):
                left, right = obj.start, obj.end
            elif isinstance(obj, (tuple, list)) and len(obj) == 2:
                left, right = obj
            elif isinstance(obj, numbers.Integral):
                left, right = obj, obj+1
            else:
                raise Exception("Not an annotation or an annotation set or pair: {}".format(args[0]))
            if isinstance(obj, Annotation):
                annid = obj.id
        else:
            assert len(args) == 2
            left, right = args
        # if the called method/function does have an annid keyword, pass it, otherwise omit
        if "annid" in method.__code__.co_varnames:
            return method(self, left, right, annid=annid, **kwargs)
        else:
            return method(self, left, right, **kwargs)

    return _support_annotation_or_set

