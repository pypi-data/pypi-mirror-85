#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import codecs
import argparse
import time
import json
import traceback


QUESTION_LABELS = ['handout', 'question', 'answer',
                   'zachet', 'nezachet', 'comment',
                   'source', 'author', 'number',
                   'setcounter']
SEP = os.linesep
ENC = sys.stdout.encoding or 'utf8'

lastdir = os.path.join(os.path.dirname(os.path.abspath('__file__')),
                       'lastdir')


def get_chgksuite_dir():
    chgksuite_dir = os.path.join(os.path.expanduser("~"), ".chgksuite")
    if not os.path.isdir(chgksuite_dir):
        os.mkdir(chgksuite_dir)
    return chgksuite_dir


def get_source_dirs():
    if getattr(sys, "frozen", False):
        sourcedir = os.path.dirname(sys.executable)
        resourcedir = os.path.join(sourcedir, "resources")
    else:
        sourcedir = os.path.dirname(
            os.path.abspath(os.path.realpath(__file__))
        )
        resourcedir = os.path.join(sourcedir, "resources")
    return sourcedir, resourcedir


def set_lastdir(path):
    chgksuite_dir = get_chgksuite_dir()
    lastdir = os.path.join(chgksuite_dir, "lastdir")
    with codecs.open(lastdir, 'w', 'utf8') as f:
        f.write(path)


def bring_to_front(root):
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)


def get_lastdir():
    chgksuite_dir = get_chgksuite_dir()
    lastdir = os.path.join(chgksuite_dir, "lastdir")
    if os.path.isfile(lastdir):
        with codecs.open(lastdir, 'r', 'utf8') as f:
            return f.read().rstrip()
    return '.'


def retry_wrapper_factory(logger):
    def retry_wrapper(func, args=None, kwargs=None, retries=3):
        cntr = 0
        ret = None
        if not args:
            args = []
        if not kwargs:
            kwargs = {}
        while not ret and cntr < retries:
            try:
                ret = func(*args, **kwargs)
            except:
                logger.error(traceback.format_exc())
                time.sleep(5)
                cntr += 1
        return ret
    return retry_wrapper


def ensure_utf8(s):
    if isinstance(s, bytes):
        return s.decode("utf8", errors="replace")
    return s


class DummyLogger(object):

    def info(self, s):
        pass

    def debug(self, s):
        pass

    def error(self, s):
        pass

    def warning(self, s):
        pass


class DefaultNamespace(argparse.Namespace):

    def __init__(self, *args, **kwargs):
        for ns in args:
            if isinstance(ns, argparse.Namespace):
                for name in vars(ns):
                    setattr(self, name, vars(ns)[name])
        else:
            for name in kwargs:
                setattr(self, name, kwargs[name])

    def __getattribute__(self, name):
        try:
            return argparse.Namespace.__getattribute__(self, name)
        except AttributeError:
            return


def on_close(root):
    root.quit()
    root.destroy()


def log_wrap(s, pretty_print=True):
    try_to_unescape = True
    if pretty_print and isinstance(s, (dict, list)):
        s = json.dumps(s, indent=2, ensure_ascii=False, sort_keys=True)
        try_to_unescape = False
    s = format(s)
    if sys.version_info.major == 2 and try_to_unescape:
        try:
            s = s.decode('unicode_escape')
        except UnicodeEncodeError:
            pass
    return s.encode(ENC, errors='replace').decode(ENC)


def toggle_factory(intvar, strvar, root):
    def toggle():
        if intvar.get() == 0:
            intvar.set(1)
        else:
            intvar.set(0)
        root.ret[strvar] = bool(intvar.get())
    return toggle


def button_factory(strvar, value, root):
    def button():
        root.ret[strvar] = value
        root.quit()
        root.destroy()
    return button


def check_question(question, logger=None):
    warnings = []
    for el in {'question', 'answer', 'source', 'author'}:
        if el not in question:
            warnings.append(el)
    if len(warnings) > 0:
        logger.warning('WARNING: question {} lacks the following fields: {}{}'
                       .format(log_wrap(question), ', '.join(warnings), SEP))
