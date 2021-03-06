.. _templatetags:

Templatetags
============

Before you can use the template tags, you need to load them with
``{% load disqus_tags %}``.

set_disqus_developer
--------------------

Adds ``disqus_deveoper`` variable to the context for the current block. The context variable is used in the :ref:`disqus_show_comments` and :ref:`disqus_num_replies` templatetags for signaling Disqus you are in testing mode. See 
`JavaScript configuration vairables documentation <http://docs.disqus.com/help/2/>`_ for more information.

Example::

	{% load disqus_tags %}
	{% set_disqus_developer 1 %}

set_disqus_identifier
---------------------

Adds ``disqus_identifier`` variable to the context for the current block. The context variable is used in the :ref:`disqus_show_comments` and :ref:`disqus_num_replies` templatetags to assign a unique value for this page. The value can be a static value or a variable.  See 
`JavaScript configuration vairables documentation <http://docs.disqus.com/help/2/>`_ for more information.

Example::

	{% load disqus_tags %}
	{% set_disqus_identifier object.id %}

You may also pass in multiple arguments, which will then be concatenated::

	{% load disqus_tags %}
	{% set_disqus_identifier "blogentry_" object.id %}

This results in ``disqus_identifier`` set to ``blogentry_25``\ , if the object's id is 25.

set_disqus_url
--------------

Adds ``disqus_url`` variable to the context for the current block. The context variable is used in the :ref:`disqus_show_comments` and :ref:`disqus_num_replies` templatetags to assign a the URL for this page. This is very important if there are several ways to reach this page (mobile and desktop versions, for example). The value can be a static value or a variable.  See 
`JavaScript configuration vairables documentation <http://docs.disqus.com/help/2/>`_ for more information.

Example::

	{% load disqus_tags %}
	{% set_disqus_url object.get_absolute_url %}

set_disqus_title
----------------

Adds ``disqus_title`` variable to the context for the current block. The context variable is used in the :ref:`disqus_show_comments` and :ref:`disqus_num_replies` templatetags to assign a title for this page. If your ``<title>`` tag contains extra cruft, this is useful for setting a easier to read title. The value can be a static value or a variable.  See 
`JavaScript configuration vairables documentation <http://docs.disqus.com/help/2/>`_ for more information.

Example::

	{% load disqus_tags %}
	{% set_disqus_title object.headline %}

disqus_dev
----------

Return the HTML/Javascript code to enable DISQUS comments on a local
development server. This template tag will only return a value
if the ``settings.DEBUG`` setting is set to ``True``. If you don't
include this, the comment form will not show up on a local development server.

Example::

    {% load disqus_tags %}
    {% disqus_dev %}

Result::
    
    <script type="text/javascript">
      var disqus_developer = 1;
      var disqus_url = 'http://arthurkoziel.com/';
    </script>

disqus_show_comments
--------------------

Renders the ``disqus/show_comments.html`` template to display DISQUS comments, including any configuration variables set in this template block. The comments for the current Thread and the comment form are displayed to the user. See the 
`embed code <http://docs.disqus.com/developers/universal/>`_ for more information.

Example::

    {% load disqus_tags %}
    {% disqus_show_comments %}

Result::
    
    <div id="disqus_thread"></div>
    <script type="text/javascript" src="http://disqus.com/forums/arthurkozielsblog/embed.js"></script>
    <noscript><p><a href="http://arthurkozielsblog.disqus.com/?url=ref">View the discussion thread.</a></p></noscript>
    <p><a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a></p>

**Options**:

 - ``shortname``: DISQUS website shortname that should be used. The
   ``settings.DISQUS_WEBSITE_SHORTNAME`` setting takes precedence
   over this parameter. Example: ``{% disqus_show_comments "foobar" %}``

disqus_num_replies
------------------

Renders the ``disqus/num_replies.html`` template, including any configuration variables set in this template block. This code that transforms links which end with a ``#disqus_thread`` anchor into the thread's comment count.

Disqus recommends including a ``data-disqus-identifier`` parameter to the ``<a>`` tag for consistent lookup. Make sure you also use :ref:`set_disqus_identifier` on the page it links to, as well.

Example::

    {% load disqus_tags %}
    <a href="{{ object.get_absolute_url }}#disqus_thread" data-disqus-identifier="{{ object.id }}">View Comments</a>
    {% disqus_num_replies %}

Template Tag output::
    
    <script type="text/javascript">
    ...
    </script>

The javascript will then transform the link to::

    <a href="foobar/">2 Comments</a>

**Options**:

 - ``shortname``: DISQUS website shortname that should be used. The 
   ``settings.DISQUS_WEBSITE_SHORTNAME`` setting takes precedence over this
   parameter. Example: ``{% disqus_num_replies "foobar" %}``
