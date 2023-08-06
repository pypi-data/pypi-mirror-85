import re
from pyparsing import *

# a stack to use during parsing
stack = []

def parse(text):
    """
    Parse fusion builder text and return a root Element for the parse tree.
    """

    # add a new root element to the stack
    global stack
    root = Element('root')
    stack = [root]

    if '[fusion_' in text:
        newText = grammar.transformString(text)
        newText = re.sub('  +', ' ', newText)
        return root, newText
    else:
        return None, text

class Element:
    """
    A class for representing a FusionBuilder element.
    """

    def __init__(self, name, attrs={}, text=None):
        self.name = name
        self.attrs = attrs
        self.text = text
        self.children = []

    def __repr__(self):
        if self.text:
            s = '[{0.name} attrs={0.attrs}]{0.text}[/{0.name}]'.format(self)
        else:
            s = '[{0.name} attrs={0.attrs}]'.format(self)
            for c in self.children:
               s += repr(c)
            s += '[/{0.name}]'.format(self)
        return s

def setStartTag(s, loc, toks):
    name = toks[0]
    attrs = getAttrs(toks[1:])
    el = Element(name, attrs)

    stack[-1].children.append(el)
    stack.append(el)
    return ''

def setEndTag(s, loc, toks):
    stack.pop()
    return ''

def setSelfClosingTag(s, loc, toks):
    name = toks[0]
    attrs = getAttrs(toks[1:])
    el = Element(name, attrs=attrs)
    stack[-1].children.append(el)
    return ''

def setText(s, loc, toks):
    stack[-1].text = toks[0]
    # strip out fusion text code from transformed text
    return toks[0] if stack[-1].name != 'fusion_code' else ''

def getAttrs(l):
    attrs = {}
    for i in range(0, len(l), 2):
        k = l[i]
        v = l[i + 1]
        attrs[k] = v
    return attrs

# The Grammar

nameChars = alphas + nums + '_'

name = Word(nameChars)

attr = Word(nameChars) + Suppress('=') + (QuotedString('"') ^ QuotedString("'"))

startTag = Suppress('[') + name + ZeroOrMore(attr) + Suppress(']')
startTag.setParseAction(setStartTag)

endTag = Suppress('[/') + name + Suppress(']')
endTag.setParseAction(setEndTag)

selfClosingTag = Suppress('[') + name + ZeroOrMore(attr) + Suppress('/]')
selfClosingTag.setParseAction(setSelfClosingTag)

char = ~endTag + Regex(r'[\s\S]') 
chars = OneOrMore(char)
text = Combine(chars)
text.setParseAction(setText)

textElement = startTag + (text ^ Empty()) + endTag 

# recursive since elements can contain elements!
element = Forward()
element <<= selfClosingTag ^ textElement ^ (startTag + OneOrMore(element) + endTag)

grammar = OneOrMore(SkipTo('[') + element)

