import logging

from django import shortcuts

from .htmlcomponents import HTMLComponent

__all__ = ['render']

logger = logging.getLogger(__name__)


class _Element:
    def __init__(self, tagname, **attrs):
        self.tagname = tagname
        self.children = []  # children or []
        self.attrs = attrs

    def __str__(self):
        attrs = ' '.join([f'{key}="{value}"' for key, value in self.attrs.items()])
        return f'<{self.tagname} {attrs}>'

    def tohtml(self):
        attrs = ' '.join([f'{key}="{value}"' for key, value in self.attrs.items()])
        result = [f'<{self.tagname} {attrs}>']

        def tohtml(c):
            if isinstance(c, _Element):
                return c.tohtml()

            return c

        result.extend([tohtml(c) for c in self.children])

        result.append(f'</{self.tagname}>')
        return ''.join(result)


def _convert_to_html_dom(virtual_dom_root):
    # iter dom tree
    htmlroot = _Element('body', style='height:100%')

    def plan_child_into(vnode, hnode):
        logger.debug(f'plan_child_into {vnode} {hnode}')
        if isinstance(vnode, HTMLComponent):
            # create new hnode
            tagname, attrs = vnode.gettag()
            newhnode = _Element(tagname, **attrs)  # 'div', **vnode.props)
            hnode.children.append(newhnode)

            for c in vnode.children:
                plan_child_into(c, newhnode)

        elif isinstance(vnode, (str, int, bool)):
            hnode.children.append(str(vnode))  # wrapping to str

        else:
            plan_child_into(vnode.render(), hnode)

    plan_child_into(virtual_dom_root, htmlroot)
    return htmlroot


def render(request, elm, title=None):
    # virtualdom = elm.render()
    logger.debug(f'elm={elm}')

    # todo: convert to html dom
    dom = _convert_to_html_dom(elm)

    # todo: convert html dom to html tree
    html = dom.tohtml()  # convert_to_html(dom)

    return shortcuts.render(
        request, 'axpluslib/base.html',
        context={
            'title': title,
            'body': html
        })
