from . import htmlcomponents
from .base import Component
from .htmlcomponents import Div, Span


def prepend_attr(origin_attr_value, new_value):
    origin_values = origin_attr_value.split(' ')
    if new_value in origin_values:
        return origin_attr_value

    return ' '.join([new_value] + origin_values)


class Container(Component):
    def render(self):
        fluid = self.props.get('fluid')
        if fluid:
            c = 'container-fluid'
        else:
            c = 'container'
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), c)

        return Div(
            *self.children,
            **self.props
        )


class Row(Component):
    def render(self):
        self.props['class'] = prepend_attr(self.props.get('class', ''), 'row')
        return Div(
            *self.children,
            **self.props)


class Col(Component):
    def render(self):
        width = self.props.get('width')
        if width:
            c = f'col-{width}'
        else:
            c = 'col'
        self.props['class'] = prepend_attr(self.props.get('class', ''), c)
        return Div(
            *self.children,
            **self.props)


class Button(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'btn')
        return htmlcomponents.Button(
            *self.children,
            **self.props)


class Card(Component):
    def render(self):
        self.props['class'] = prepend_attr(self.props.get('class', ''), 'card')
        return Div(
            *self.children,
            **self.props)


class CardBody(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'card-body')
        return Div(
            *self.children,
            **self.props)


class CardTitle(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'card-title')
        return Div(
            *self.children,
            **self.props)


class CardText(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'card-text')
        return Div(
            *self.children,
            **self.props)


class Badge(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'badge')
        return Span(
            *self.children,
            **self.props)


class Breadcrumb(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'breadcrumb')
        return Div(
            *self.children,
            **self.props)


class BreadcrumbItem(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'breadcrumb-item')
        return Div(
            *self.children,
            **self.props)


class ListGroup(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'list-group')
        return Div(
            *self.children,
            **self.props)


class ListGroupItem(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'list-group-item')
        return Div(
            *self.children,
            **self.props)


class Form(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'form')
        return htmlcomponents.Form(
            *self.children,
            **self.props)


class InputGroup(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'input-group')
        return Div(
            *self.children,
            **self.props)


class Input(Component):
    def render(self):
        self.props['class'] = prepend_attr(
            self.props.get('class', ''), 'form-control')
        return htmlcomponents.Input(
            *self.children,
            **self.props)
