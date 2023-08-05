# axplus

Reactive template rendering from Django views.

## Installation

From pip:

```
pip install axplus
```

Add codes into settings.py of your Django project:

```python
INSTALLED_APPS = [
    ...
    'axplus',
]

MIDDLEWARE = [
    ...
    'axplus.middleware.VdomConverter',
]
```

## Basic Usage

Hello world:

```python
def index(request):
    return Div('Hello world')
```

More complex:

```python
from axplus.base import Component

class WelcomePage(Component):
    def render(self):
        return Div(
            H1('Welcome'),
            f'Hello, {self.props['yourname']}!'
        )

def index(request):
    return WelcomePage(
        yourname=request.GET.get('yourname')
    )
```

## References

-   [
    How To Package And Distribute Python Applications](https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications)
