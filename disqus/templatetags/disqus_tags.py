from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.functional import curry
from django.utils.encoding import force_unicode

register = template.Library()

VALID_SIZES = {'small':24, 'medium': 32, 'large':48, 'x-large': 96, 'ginormous': 128}
VALID_TRUE = ['1', 'True', 'true', 'T', 't', 1, True]
VALID_COLORS = ['blue', 'grey', 'green', 'red', 'orange']
VALID_TABS = ['people', 'recent', 'popular']

class ContextSetterNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
    
    def _get_value(self, value, context):
        """
        Attempts to resolve the value as a variable. Failing that, it returns
        its actual value
        """
        try:
            var_value = template.Variable(value).resolve(context)
        except template.VariableDoesNotExist:
            var_value = self.var_value.var
        return var_value
    
    def render(self, context):
        if isinstance(self.var_value, (list, tuple)):
            var_value = ''.join([force_unicode(self._get_value(x, context)) for x in self.var_value])
        else:
            var_value = self._get_value(self.var_value, context)
        context[self.var_name] = var_value
        return ''

def generic_setter_compiler(var_name, name, node_class, parser, token):
    """
    Returns a ContextSetterNode.
    
    For calls like {% set_this_value "My Value" %}
    """
    bits = token.split_contents()
    if(len(bits) < 2):
        message = "%s takes at least one argument" % name
        raise template.TemplateSyntaxError(message)
    return node_class(var_name, bits[1:])

# Set the disqus_developer variable to 0/1. Default is 0
set_disqus_developer = curry(generic_setter_compiler, 'disqus_developer', 'set_disqus_developer', ContextSetterNode)

# Set the disqus_identifier variable to some unique value. Defaults to page's URL
set_disqus_identifier = curry(generic_setter_compiler, 'disqus_identifier', 'set_disqus_identifier', ContextSetterNode)

# Set the disqus_url variable to some value. Defaults to page's location
set_disqus_url = curry(generic_setter_compiler, 'disqus_url', 'set_disqus_url', ContextSetterNode)

# Set the disqus_title variable to some value. Defaults to page's title or URL
set_disqus_title = curry(generic_setter_compiler, 'disqus_title', 'set_disqus_title', ContextSetterNode)

def get_config(context):
    """
    return the formatted javascript for any disqus config variables
    """
    conf_vars = ['disqus_developer', 'disqus_identifier', 'disqus_url', 'disqus_title']
    
    output = []
    for item in conf_vars:
        if item in context:
            output.append('\tvar %s = "%s";' % (item, context[item]))
    return '\n'.join(output)

def disqus_dev():
    """
    Return the HTML/js code to enable DISQUS comments on a local
    development server if settings.DEBUG is True.
    """
    if settings.DEBUG:
        return """<script type="text/javascript">
    var disqus_developer = 1;
    var disqus_url = 'http://%s/';
</script>""" % Site.objects.get_current().domain
    return ""

def disqus_num_replies(context, shortname=''):
    """
    Return the HTML/js code which transforms links that end with an
    #disqus_thread anchor into the threads comment count.
    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)
    
    return {
        'shortname': shortname,
        'config': get_config(context),
    }

def disqus_combination_widget(context, shortname='', num_items=5, 
    hide_mods=False, color="blue", default_tab="people", excerpt_length=200):
    """
    Return the HTML code to display the combination widget
    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)
    if color not in VALID_COLORS:
        color = VALID_COLORS[0]
    if default_tab not in VALID_TABS:
        default_tab = VALID_TABS[0]
    return {
        'shortname': shortname,
        'num_items': int(num_items),
        'hide_mods': int(hide_mods in VALID_TRUE),
        'color': color,
        'default_tab': default_tab,
        'excerpt_length': int(excerpt_length),
    }

def disqus_recent_comments_widget(context, shortname='', num_items=5, 
    hide_avatars=False, avatar_size=32, excerpt_length=200):
    """
    Return the HTML code to display the recent comments widget
    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)
    if isinstance(avatar_size, int):
        if avatar_size not in VALID_SIZES.values():
            avatar_size = 32
    elif avatar_size in VALID_SIZES.keys():
        avatar_size = VALID_SIZES[avatar_size]
    else:
        avatar_size = 32
    return {
        'shortname': shortname,
        'num_items': int(num_items),
        'hide_avatars': int(hide_avatars in VALID_TRUE),
        'avatar_size': avatar_size,
        'excerpt_length': int(excerpt_length),
    }

def disqus_popular_threads_widget(context, shortname='', num_items=5):
    """
    Return the HTML code to display the recent comments widget
    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)
    return {
        'shortname': shortname,
        'num_items': int(num_items),
    }

def disqus_top_commenters_widget(context, shortname='', num_items=5, 
    hide_mods=False, hide_avatars=False, avatar_size=32):
    """
    Return the HTML to display the top commenters widget
    """
    if isinstance(avatar_size, int):
        if avatar_size not in VALID_SIZES.values():
            avatar_size = 32
    elif avatar_size in VALID_SIZES.keys():
        avatar_size = VALID_SIZES[avatar_size]
    else:
        avatar_size = 32
    return {
        'shortname': shortname,
        'num_items': int(num_items),
        'hide_mods': int(hide_mods in VALID_TRUE),
        'hide_avatars': int(hide_mods in VALID_TRUE),
        'avatar_size': avatar_size,
    }

def disqus_show_comments(context, shortname=''):
    """
    Return the HTML code to display DISQUS comments.
    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)
    return {
        'shortname': shortname,
        'config': get_config(context),
    }

register.tag('set_disqus_developer', set_disqus_developer)
register.tag('set_disqus_identifier', set_disqus_identifier)
register.tag('set_disqus_url', set_disqus_url)
register.tag('set_disqus_title', set_disqus_title)
register.simple_tag(disqus_dev)
register.inclusion_tag('disqus/top_commenters_widget.html', takes_context=True)(disqus_top_commenters_widget)
register.inclusion_tag('disqus/recent_comments_widget.html', takes_context=True)(disqus_recent_comments_widget)
register.inclusion_tag('disqus/popular_threads_widget.html', takes_context=True)(disqus_popular_threads_widget)
register.inclusion_tag('disqus/combo_widget.html', takes_context=True)(disqus_combination_widget)
register.inclusion_tag('disqus/num_replies.html', takes_context=True)(disqus_num_replies)
register.inclusion_tag('disqus/show_comments.html', takes_context=True)(disqus_show_comments)
