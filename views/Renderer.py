from PySide2 import QtCore

from models import Visitor

from .ConditionView import ConditionView
from .ContextView import ContextView
from .LabelView import LabelView
from .MenuView import MenuView
from .JumpView import JumpView
from .CallView import CallView
from .CubicConnection import CubicConnection

class Renderer(Visitor):
    def __init__(self, organiser, browser):
        self.organiser = organiser
        self.browser = browser
    
    def create_connection(self, start, end):
        connection = CubicConnection(start, end, self.browser)
        self.browser.addItem(connection)
    
    # conditions
    def visit_condition_block(self, block):
        node = ConditionView(block, self.browser)
        self.browser.addItem(node)
        self.organiser.add_node(node)

        with self.organiser:
            child = block.if_condition.accept(self)
            start = node.getSocket(block.if_condition)
            end = child.getSocket("root")
            self.create_connection(start, end)

            for elif_condition in block.elif_conditions:
                child = elif_condition.accept(self)
                start = node.getSocket(elif_condition)
                end = child.getSocket("root")
                self.create_connection(start, end)

            if block.else_condition:
                child = block.else_condition.accept(self)
                start = node.getSocket(block.else_condition)
                end = child.getSocket("root")
                self.create_connection(start, end)

        return node

    def visit_if_condition(self, con):
        return con.context.accept(self)

    def visit_elif_condition(self, con):
        return con.context.accept(self)

    def visit_else_condition(self, con):
        return con.context.accept(self)

    # context
    def visit_context(self, context):
        node = ContextView(context, self.browser) 
        self.browser.addItem(node)
        self.organiser.add_node(node)
        with self.organiser:
            for content in context.contents:
                if isinstance(content, str):
                    continue
                child = content.accept(self)
                if child:
                    start = node.getSocket(content)
                    end = child.getSocket("root")
                    self.create_connection(start, end)
        
        return node

    # renpy directives
    def visit_label(self, label):
        node = LabelView(label, self.browser) 
        self.browser.addItem(node)
        self.organiser.add_node(node)
        with self.organiser:
            context = label.context.accept(self)

        start = node.getSocket("root")
        end = context.getSocket("root")
        self.create_connection(start, end)

        return node
        

    def visit_jump(self, jump):
        node = JumpView(jump, self.browser)
        self.browser.addItem(node)
        self.organiser.add_node(node)
        return node

    def visit_call(self, call):
        node = CallView(call, self.browser)
        self.browser.addItem(node)
        self.organiser.add_node(node)
        return node

    def visit_script(self, script):
        pass

    def visit_python_block(self, block):
        pass

    # menu
    def visit_menu(self, menu):
        node = MenuView(menu, self.browser)
        self.browser.addItem(node)
        self.organiser.add_node(node)
        with self.organiser:
            for choice in menu.choices:
                child = choice.accept(self)
                start = node.getSocket(choice)
                end = child.getSocket("root")
                self.create_connection(start, end)

        return node

    def visit_choice(self, choice):
        return choice.context.accept(self)
    

    


