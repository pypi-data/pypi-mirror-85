from django.utils.deprecation import MiddlewareMixin

from .base import Component
from .django import render


class _HtmlWrapper:
    def __init__(self, root_vnode):
        self.root_vnode = root_vnode

    def render(self):
        return render(None, self.root_vnode, title=self.root_vnode.props.get('title'))


class VdomConverter(MiddlewareMixin):
    def process_template_response(self, request, response):
        if isinstance(response, Component):
            return _HtmlWrapper(response)

        return response  # do not support type
