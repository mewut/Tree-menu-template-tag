from django import template
from tree.models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    # принимаем контекст и имя меню в качестве параметров
    menu_items = Menu.objects.filter(name=menu_name).select_related('parent')
    menu_tree = build_menu_tree(menu_items) # извлекаем текущий урл из запроса и строим из него дерево меню на основе элементов модели

    return draw_menu(menu_tree, current_url)


# сюда передали все, что выше. Из этого будем строить дерево. 
def build_menu_tree(menu_items):
    menu_tree = {}
    # создаем словарь, в котором ключи представляют идентификаторы родительских элементов меню, а значения представляют списки дочерних элементов
    # проходим по элементам меню и добавляем их в соответствующие списки дочерних элементов 
    for item in menu_items:
        if item.parent_id not in menu_tree:
            menu_tree[item.parent_id] = []
        menu_tree[item.parent_id].append(item)

    return menu_tree


def draw_menu(menu_tree, current_url, parent_id=None):
    menu_html = '<ul>'
    # коммент ниже. Идея в том, чтобы рекурсивиться до потери пульса, пока новые дети будут создаваться в родителе
    items = menu_tree.get(parent_id, [])
    for item in items:
        active_class = 'active' if item.is_active(current_url) else ''
        menu_html += f'<li class="{active_class}">'
        menu_html += f'<a href="{item.url}">{item.name}</a>'
        menu_html += draw_menu(menu_tree, current_url, item.id)
        menu_html += '</li>'

    menu_html += '</ul>'

    return menu_html

# открываем <ul> и получаем список элементов меню для заданного родительского элемента (parent_id) из menu_tree и проходим по ним. 
# Для каждого элемента меню определяем класс active,
# если элемент является активным (текущий урл соответствует урлу элемента), 
# и добавляем соответствующие теги <li> и <a> в menu_html. 
# Затем вызываем рекурсивно функцию render_menu, передавая ей дочерний элемент в качестве родительского элемента, 
# чтобы обработать вложенные подменю. 
# Наконец, закрываем <ul> и возвращаем HTML.
