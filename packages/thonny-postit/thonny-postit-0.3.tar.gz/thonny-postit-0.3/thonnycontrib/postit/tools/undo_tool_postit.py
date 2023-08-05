import tkinter as tk
from tkinter import ttk

from thonny.codeview import CodeViewText
from thonny.shell import ShellText
from thonny import get_workbench, get_shell

from .tool_postit import ToolWidget, ToolCodeMixin
from ..base_postit import BaseCode, BasePost, BasePopup


class UndoToolPostMixin:
    def insert_into_editor(self, editor_text, 
                           pressing=False, dragging=False,
                           selecting=False, hovering=False):
        
        editor_text.edit_undo()

    def insert_into_shell(self, shell_text, 
                           pressing=False, dragging=False,
                           selecting=False, hovering=False):
        if shell_text.compare('input_start', '==','end-1c'):
            # empty line
            shell_text.event_generate("<Up>")
        else: # not empty line
            shell_text.edit_undo()

class RedoToolPostMixin:
    def insert_into_editor(self, editor_text, 
                           pressing=False, dragging=False,
                           selecting=False, hovering=False):
        
        editor_text.edit_redo()

    def insert_into_shell(self, shell_text, 
                           pressing=False, dragging=False,
                           selecting=False, hovering=False):
        shell_text.edit_redo()


class UndoToolPostit(ToolWidget, 
                 ToolCodeMixin, BaseCode,
                 UndoToolPostMixin, BasePost, 
                 BasePopup):
    """ composite and mixin approach postit"""
    def __init__(self, master):
        self.widget_init(master, 'undo')
        self.code_init()
        self.post_init()
        #self.popup_init()

class RedoToolPostit(ToolWidget, 
                 ToolCodeMixin, BaseCode,
                 RedoToolPostMixin, BasePost, 
                 BasePopup):
    """ composite and mixin approach postit"""
    def __init__(self, master):
        self.widget_init(master, 'redo')
        self.code_init()
        self.post_init()
        #self.popup_init()