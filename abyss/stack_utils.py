import os
import re
from collections import namedtuple
from inspect import getfile

LIB_RE = re.compile("^.*site-packages/", re.I)

FrameInfo = namedtuple("FrameInfo", "id filename func lineno is_generator classname")


CLASSNAME_CACHE = {}


def get_classname(filename, frame):
    if frame.f_locals:
        key = (filename, frame.f_lineno)
        if key in CLASSNAME_CACHE:
            return CLASSNAME_CACHE[key]
        self = frame.f_locals.get("self")
        if self is not None:
            cls = getattr(self, "__class__", None)
        else:
            cls = frame.f_locals.get("cls")
        CLASSNAME_CACHE[key] = classname = getattr(cls, "__name__", None)
        return classname


def format_frames(frame, offset=0, with_class=False):
    formatted = []
    while frame:
        filename = LIB_RE.sub("%/", getfile(frame).replace(os.sep, "/"))
        classname = with_class and get_classname(filename, frame)
        formatted.append(
            FrameInfo(
                id(frame),
                filename,
                frame.f_code.co_name,
                frame.f_lineno,
                (frame.f_code.co_flags & 0x20),
                classname,
            )
        )
        frame = frame.f_back
    return formatted[offset:]


def remove_common(stacks):
    """
    :type stacks: list[list[FrameInfo]]
    """
    while all(stacks) and all((stack[0].id == stacks[0][0].id) for stack in stacks):
        for stack in stacks:
            stack.pop(0)
    return stacks


def diff_stacks(old_stack, new_stack):
    for old_frame in old_stack:
        yield ("exit", old_frame)

    for new_frame in new_stack:
        yield ("enter", new_frame)
