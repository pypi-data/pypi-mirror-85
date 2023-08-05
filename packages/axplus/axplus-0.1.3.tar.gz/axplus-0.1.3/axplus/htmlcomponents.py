from .base import Component


class HTMLComponent(Component):

    def __init__(self, tagname, *children, **attrs):
        super().__init__(*children, **attrs)
        self.tagname = tagname

    def gettag(self):
        return self.tagname, self.props


class Div(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('div', *children, **attrs)


class Span(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('span', *children, **attrs)


class Button(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('button', *children, **attrs)


class Hr(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('hr', *children, **attrs)


class Svg(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('svg', *children, **attrs)


class H1(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('h1', *children, **attrs)


class H5(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('h5', *children, **attrs)


class A(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('a', *children, **attrs)


class Form(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('form', *children, **attrs)


class Input(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('input', *children, **attrs)


class Iframe(HTMLComponent):
    def __init__(self, *children, **attrs):
        super().__init__('iframe', *children, **attrs)
