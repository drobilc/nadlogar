from .visitor import Visitor
from ..naloge import *

class HtmlGenerator(Visitor):
    
    @staticmethod
    def generate_html(test: Test):
        return ''