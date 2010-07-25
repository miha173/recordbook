# -*- coding: utf-8 -*-

import string
from plasTeX.Renderers import Renderer

class Renderer(Renderer):
    
    def default(self, node):
        """ Rendering method for all non-text nodes """
        s = []

        # Handle characters like \&, \$, \%, etc.
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)

        # Start tag
        s.append('<%s>' % node.nodeName)

        # See if we have any attributes to render
        if node.hasAttributes():
            s.append('<attributes>')
            for key, value in node.attributes.items():
                # If the key is 'self', don't render it
                # these nodes are the same as the child nodes
                if key == 'self':
                    continue
                s.append('<%s>%s</%s>' % (key, unicode(value), key))
            s.append('</attributes>')

        # Invoke rendering on child nodes
        s.append(unicode(node))

        # End tag
        s.append('</%s>' % node.nodeName)

        return u'\n'.join(s)

    def textDefault(self, node):
        """ Rendering method for all text nodes """
        return node.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')






#from MyRenderer import Renderer

from plasTeX.TeX import TeX

def handle_equation(node):
    return u'<div><img src="%s"/></div>' % node.image.url

# Instantiate a TeX processor and parse the input text
tex = TeX()
tex.input(r'''
\documentclass[40pt]{extreport}
\usepackage[russian]{babel}
\begin{document}

Previous paragraph.

\begin{equation}
    log_{a}b = \frac{log_{c}a}{log_{c}b}
\end{equation}

\begin{equation}
    sin2\alpha = 2sin\alpha cos\alpha
\end{equation}

Next paragraph.

\end{document}
''')
document = tex.parse()

# Instantiate the renderer
renderer = Renderer()

# Insert the rendering method into all of the environments that might need it
renderer['equation'] = handle_equation
renderer['displaymath'] = handle_equation
renderer['eqnarray'] = handle_equation

# Render the document
renderer.render(document)