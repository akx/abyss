from inspect import getfile
import os
import re

LIB_RE = re.compile("^.*site-packages/", re.I)


def format_frames(frame, offset=0):
    formatted = []
    while frame:
        filename = LIB_RE.sub("%/", getfile(frame).replace(os.sep, "/"))
        formatted.append((filename, frame.f_code.co_name, frame.f_lineno))
        frame = frame.f_back
    return formatted[offset:]


def remove_common(stacks, ignore_lines=False):
    cut = (2 if ignore_lines else 3)
    while all(stacks) and all((stack[0][:cut] == stacks[0][0][:cut]) for stack in stacks):
        for stack in stacks:
            stack.pop(0)
    return stacks


def diff_stacks(old_stack, new_stack):
    for old_frame in old_stack:
        yield ("exit", old_frame)

    for new_frame in new_stack:
        yield ("enter", new_frame)
