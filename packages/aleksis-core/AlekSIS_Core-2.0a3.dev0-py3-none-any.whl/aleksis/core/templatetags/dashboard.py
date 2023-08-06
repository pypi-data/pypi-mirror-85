from django.template import Library, loader

register = Library()


@register.simple_tag
def include_widget(widget) -> dict:
    """Render a template with context from a defined widget."""
    template = loader.get_template(widget.get_template())
    context = widget.get_context()

    return template.render(context)
