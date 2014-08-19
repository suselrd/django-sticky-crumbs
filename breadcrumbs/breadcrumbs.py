"""
Classes to add request.breadcrumbs as one class to have a list of breadcrumbs
TODO: maybe is better to move to contrib/breadcrumbs
"""

from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class BreadcrumbsInvalidFormat(Exception):
    """
    Simple exception that can be extended
    """
    pass


class BreadcrumbsNotSet(Exception):
    """
    Raised in utils.breadcrumbs_for_flatpages when we not have breadcrumbs in
    request.
    """
    pass


class Breadcrumb(object):
    """
    Breadcrumb can have methods to customize breadcrumb object, Breadcrumbs
    class send to us name and url.
    """
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s,%s" % (self.name, self.url)

    def __repr__(self):
        return u"Breadcrumb <%s,%s>" % (self.name, self.url)


class Breadcrumbs(object):
    """
    Breadcrumbs maintain a list of breadcrumbs that you can get interating with
    class or with get_breadcrumbs().
    """

    def __fill_home(self):
        # fill home if settings.BREADCRUMBS_AUTO_HOME is True
        if self.__autohome and len(self.__bds) == 0:
            home_title = getattr(settings, 'BREADCRUMBS_HOME_TITLE', _(u'Home'))
            self.__fill_bds((home_title, u"/"))

    def _reset(self):
        self.__bds = []
        self.__urls = []
        self.__autohome = getattr(settings, 'BREADCRUMBS_AUTO_HOME', False)
        self.__fill_home()

    def __init__(self, init_dict=None):
        if not init_dict:
            self._reset()
        else:
            self.__bds = init_dict.get('bds', [])
            self.__urls = init_dict.get('urls', [])
            self.__autohome = init_dict.get('autohome', getattr(settings, 'BREADCRUMBS_AUTO_HOME', False))

    def __validate(self, obj, index):
        """
        check for object type and return a string as name for each item of a
        list or tuple with items, if error was found raise
        BreadcrumbsInvalidFormat
        """
        # for list or tuple
        if type(obj) in (list, tuple):
            if len(obj) == 2:
                if ((not obj[0] and not obj[1]) or
                        (type(obj[0]) not in (str, unicode) and
                        type(obj[1]) not in (str, unicode))):
                    raise BreadcrumbsInvalidFormat(
                        u"Invalid format for breadcrumb %s in %s" % (index, type(obj).__name__)
                    )
            if len(obj) != 2:
                raise BreadcrumbsInvalidFormat(
                    u"Wrong itens number in breadcrumb %s in %s. You need to send as example (name,url)"
                    % (index, type(obj).__name__)
                )
        # for objects and dicts
        else:
            if isinstance(obj, dict) and obj.get('name') and obj.get('url'):
                obj = Breadcrumb(obj['name'], obj['url'])
            if not hasattr(obj, 'name') and not hasattr(obj, 'url'):
                raise BreadcrumbsInvalidFormat(u"You need to use a tuple like "
                    "(name, url) or dict or one object with name and url "
                    "attributes for breadcrumb.")
        return True

    def __fill_bds(self, bd):
        """
        simple interface to add Breadcrumb to bds
        """
        if hasattr(bd, 'name') and hasattr(bd, 'url'):
            bd = {
                'name': bd.name,
                'url': bd.url
            }
        else:
            bd = {
                'name': bd[0],
                'url': bd[1]
            }
        if bd['url'] not in self.__urls:
            self.__bds.append(bd)
            self.__urls.append(bd['url'])
        else:
            l = len(self.__urls)
            i = self.__urls.index(bd['url'])
            del self.__urls[i+1:l]
            del self.__bds[i+1:l]

    def __iter__(self):
        return iter(self.__bds)

    def __getitem__(self, key):
        return self.__bds[key]

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"Breadcrumbs <%s>" % u", ".join([mark_safe(item.name)
                                                 for item in self[:10]] + [u' ...'])

    def add(self, *a, **kw):

        # match **{'name': name, 'url': url}
        if kw.get('name') and kw.get('url'):
            self.__validate((kw['name'], kw['url']), 0)
            self.__fill_bds((kw['name'], kw['url']))
        # match Breadcrumbs( 'name', 'url' )
        if len(a) == 2 and type(a[0]) not in (list, tuple):
            if(self.__validate(a, 0)):
                self.__fill_bds(a)
        # match ( ( 'name', 'url'), ..) and samething with list
        elif len(a) == 1 and type(a[0]) in (list, tuple) \
                and len(a[0]) > 0:
            for i, arg in enumerate(a[0]):
                if isinstance(arg, dict):
                    self.add(**arg)
                elif self.__validate(arg, i):
                    self.__fill_bds(arg)
        # try to ( obj1, obj2, ... ) and samething with list
        else:
            for arg in a:
                if type(arg) in (list, tuple):
                    self.add(arg)
                elif isinstance(arg, dict):
                    self.add(**arg)
                else:
                    raise BreadcrumbsInvalidFormat(_("We accept lists of "
                        "tuples, lists of dicts, or two args as name and url, "
                        "not '%s'") % a)

    def all(self):
        return self.__bds

    def clear(self):
        return self._reset()

    def dict_repr(self):
        return {
            'bds': self.__bds,
            'urls': self.__urls,
            'autohome': self.__autohome
        }