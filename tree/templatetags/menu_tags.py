from django import template
from tree.models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path

    menu_items = Menu.objects.filter(name=menu_name).select_related('parent')
    menu_tree = build_menu_tree(menu_items)

    return render_menu(menu_tree, current_url)


def build_menu_tree(menu_items):
    menu_tree = {}

    for item in menu_items:
        if item.parent_id not in menu_tree:
            menu_tree[item.parent_id] = []
        menu_tree[item.parent_id].append(item)

    return menu_tree


def render_menu(menu_tree, current_url, parent_id=None):
    menu_html = '<ul>'

    items = menu_tree.get(parent_id, [])
    for item in items:
        active_class = 'active' if item.is_active(current_url) else ''
        menu_html += f'<li class="{active_class}">'
        menu_html += f'<a href="{item.url}">{item.name}</a>'
        menu_html += render_menu(menu_tree, current_url, item.id)
        menu_html += '</li>'

    menu_html += '</ul>'

    return menu_html
