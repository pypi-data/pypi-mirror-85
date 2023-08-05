def _unescape_attr_key(key):
    return key.replace('_', '')


class Component:
    def __init__(self, *children, **props):
        self.children = children

        self.props = self.parse_props(**props)

    def parse_props(self, **props):
        return {
            _unescape_attr_key(key): value
            for key, value in props.items()
        }

    def render(self):
        pass
