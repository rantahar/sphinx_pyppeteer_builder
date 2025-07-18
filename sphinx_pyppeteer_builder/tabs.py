from docutils import nodes
from sphinx.util.docutils import SphinxDirective
import uuid


# Placeholder classes for the sphinx tags
class TabsNode(nodes.General, nodes.Element):
    pass

class GroupTabNode(nodes.General, nodes.Element):
    pass



class TabsDirective(SphinxDirective):
    """ Directive to process tabs. Does not do much, since 
        we don't need to change the order of the content.
    """
    has_content = True

    def run(self):
        self.assert_has_content()
        node = TabsNode()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class GroupTabDirective(SphinxDirective):
    """ Directive for the group-tab sphinx tag. Doesn not do much,
        since we don't need to change the order of the content.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        self.assert_has_content()
        node = GroupTabNode()
        node['title'] = self.arguments[0]
        node['tab_id'] = f"tab-{uuid.uuid4().hex}"
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_tabs_node_html(self, node):
    """ Create a div for the tabs """
    self.body.append(self.starttag(node, 'div', CLASS='group-tabs-container'))

def depart_tabs_node_html(self, node):
    """ Close the tabs container div """
    self.body.append('</div>')

def visit_group_tab_node_html(self, node):
    """ Process the group tab. Creates a title and a content div. """

    title_text = node.get('title', '')
    title_html = f'<h3 class="group-tab-title">{title_text}</h3>'
    self.body.append(title_html)
    
    panel_classes = 'group-tab-content'
    self.body.append(self.starttag(node, 'div', CLASS=panel_classes))

def depart_group_tab_node_html(self, node):
    """ Close the group tab content div. """
    self.body.append('</div>')

def setup(app):
    """ Setup section to make it a sphinx extension. Adds the tabs and group-tab directives. """

    app.add_node(TabsNode, html=(visit_tabs_node_html, depart_tabs_node_html))
    app.add_node(GroupTabNode, html=(visit_group_tab_node_html, depart_group_tab_node_html))

    app.add_directive('tabs', TabsDirective)
    app.add_directive('group-tab', GroupTabDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
