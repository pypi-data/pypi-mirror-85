import unittest

from blazeweb.globals import settings
from blazeweb.config import QuickSettings, EnabledSettings
from blazeweb.hierarchy import listapps
from nose.tools import eq_
from minimal2.application import make_wsgi as make_wsgi_min2
from blazewebtestapp.applications import make_wsgi


class Base(QuickSettings):

    def __init__(self):
        QuickSettings.__init__(self)

        # name of the website/application
        self.name.full = 'full'
        self.name.short = 'short'

        # application modules from our application or supporting applications
        self.modules = EnabledSettings()
        self.modules.users.enabled = True
        self.modules.users.var2 = 'not bar'
        self.modules.users.routes = []
        self.modules.users.level2.var2 = 'not bar'
        self.modules.users.level3 = 'string value to merge'
        self.modules.users.level4 = (('var2', 'not bar'), ('var3', 'baz'))
        self.modules.users.level5.level1.var1.notlikely = 'foo'
        self.modules.users.level5.level2.var1 = 'not_bar'
        self.modules.apputil.enabled = True
        self.modules.inactivemod.enabled = False

        #######################################################################
        # ROUTING
        #######################################################################
        # default routes
        self.routing.routes = [1, 2]

        # route prefix
        self.routing.prefix = ''

        #######################################################################
        # DATABASE
        #######################################################################
        self.db.echo = False

        #######################################################################
        # SESSIONS
        #######################################################################
        # beaker session options
        # http://wiki.pylonshq.com/display/beaker/Configuration+Options
        self.beaker.type = 'dbm'
        self.beaker.data_dir = 'session_cache'

        #######################################################################
        # TEMPLATE & VIEW
        #######################################################################
        self.template.default = 'default.html'
        self.template.admin = 'admin.html'
        self.trap_view_exceptions = True

        #######################################################################
        # LOGGING & DEBUG
        #######################################################################
        # currently support 'debug' & 'info'
        self.logging.levels = ()

        # no more values can be added
        self.lock()


class Default(Base):

    def __init__(self):
        Base.__init__(self)

        # supporting applications
        self.supporting_apps = ['rcsappbase']

        # application modules from our application or supporting applications
        self.unlock()
        self.modules.contentbase.enabled = True
        self.modules.lagcontent.enabled = True
        self.lock()

        #######################################################################
        # ROUTING
        #######################################################################
        self.routing.routes.extend([3, 4])

        #######################################################################
        # DATABASE
        #######################################################################
        self.db.echo = True

        #######################################################################
        # LOGGING & DEBUG
        #######################################################################
        self.logging.levels = ('info', 'debug')
        self.trap_view_exceptions = False
        self.hide_exceptions = False


class UserSettings(QuickSettings):

    def __init__(self):
        QuickSettings.__init__(self)

        self.routes = ([
            '/test1',
            '/test2',
        ])

        self.var1 = 'foo'
        self.var2 = 'bar'

        self.level2.var1 = 'foo'
        self.level2.var2 = 'bar'

        self.level3.var1 = 'foo'
        self.level3.var2 = 'bar'

        self.level4.var1 = 'foo'
        self.level4.var2 = 'bar'

        self.level5.level1.var1 = 'foo'
        self.level5.level2.var1 = 'bar'
        self.level5.level2.var2 = 'baz'
        self.level5.level3.var1 = 'bob'

        # no more values can be added
        self.lock()


class TestQuickSettings(unittest.TestCase):

    def test_level1(self):
        es = QuickSettings()
        es.a = 1
        assert es.a == 1

    def test_level2(self):
        es = QuickSettings()
        es.a.a = 1
        assert es.a.a == 1

    def test_email(self):
        es = QuickSettings()
        es.email.smtp.server = 'example.com'
        es.email.smtp.user_name = 'myself'
        es.email.smtp.password = 'pass'

        assert es.email.smtp.server == 'example.com'
        assert es.email.smtp.user_name == 'myself'
        assert es.email.smtp.password == 'pass'

    def test_settings(self):
        s = Default()

        assert s.name.full == 'full'
        assert s.name.short == 'short'
        assert s.modules.keys() == ['users', 'apputil', 'contentbase', 'lagcontent']
        assert s.routing.routes == [1, 2, 3, 4]

        assert s.db.echo is True

        assert s.logging.levels == ('info', 'debug')
        assert s.trap_view_exceptions is False
        assert s.hide_exceptions is False

        assert s.template.default == 'default.html'
        assert s.template.admin == 'admin.html'

        assert s.beaker.type == 'dbm'
        assert s.beaker.data_dir == 'session_cache'

    def test_lock(self):
        s = Default()

        try:
            s.not_there
        except AttributeError as e:
            assert str(e) == "object has no attribute 'not_there' (object is locked)"
        else:
            self.fail("lock did not work, expected AttributeError")

        # make sure lock went to children
        try:
            s.db.not_there
        except AttributeError as e:
            assert str(e) == "object has no attribute 'not_there' (object is locked)"
        else:
            self.fail("lock did not work on child, expected AttributeError")

    def test_unlock(self):
        s = Default()
        s.unlock()

        s.new_attr = 'new_attr'
        s.db.new_attr = 'new_attr'

        assert s.db.new_attr == 'new_attr'
        assert s.new_attr == 'new_attr'

        s.lock()

        try:
            s.not_there
        except AttributeError as e:
            assert str(e) == "object has no attribute 'not_there' (object is locked)"
        else:
            self.fail("lock did not work, expected AttributeError")

        # make sure lock went to children
        try:
            s.db.not_there
        except AttributeError as e:
            assert str(e) == "object has no attribute 'not_there' (object is locked)"
        else:
            self.fail("lock did not work on child, expected AttributeError")

    def test_dict_convert(self):
        s = Default()

        # beaker would need a dictionary, so lets see if it works
        d = {
            'type': 'dbm',
            'data_dir': 'session_cache'
        }

        assert dict(s.beaker) == d
        assert s.beaker.todict() == d

    def test_hasattr(self):
        s = Default()

        assert hasattr(s, 'alajsdf') is False
        assert hasattr(s, 'alajsdf') is False

        s.unlock()
        assert hasattr(s, 'alajsdf') is True

    def test_modules(self):
        s = Default()

        s.unlock()
        try:
            s.modules.badmod = False
        except TypeError:
            pass
        else:
            self.fail('expected TypeError when non QuickSettings object assigned to '
                      'EnabledSettings object')
        s.modules.fatfingeredmod.enabledd = True
        s.lock()

        mods = ['users', 'apputil', 'contentbase', 'lagcontent']
        allmods = ['users', 'apputil', 'inactivemod', 'contentbase', 'lagcontent',
                   'fatfingeredmod']
        self.assertEqual(mods, s.modules.keys())
        self.assertEqual(allmods, s.modules.keys(showinactive=True))

        self.assertEqual(len(mods), len([v for v in s.modules]))
        self.assertEqual(len(mods), len(s.modules))
        self.assertEqual(len(mods), len(s.modules.values()))
        self.assertEqual(len(allmods), len(s.modules.values(showinactive=True)))

        self.assertEqual(len(mods), len(s.modules.todict()))
        self.assertEqual(len(allmods), len(s.modules.todict(showinactive=True)))

        self.assertTrue('users' in s.modules)
        self.assertFalse('inactivemod' in s.modules)

    def test_merge(self):
        s = Default()
        us = UserSettings()

        try:
            self.assertEqual(s.modules.users.var1, 'foo')
        except AttributeError as e:
            assert str(e) == "object has no attribute 'var1' (object is locked)"
        else:
            self.fail("expected AttributeError for 'var1'")

        self.assertEqual(s.modules.users.var2, 'not bar')
        self.assertEqual(us.var2, 'bar')
        self.assertEqual(len(us.routes), 2)
        self.assertEqual(us.level2.var1, 'foo')
        self.assertEqual(us.level2.var2, 'bar')
        self.assertEqual(us.level3.var2, 'bar')
        self.assertEqual(us.level4.var2, 'bar')
        self.assertEqual(us.level5.level1.var1, 'foo')
        self.assertEqual(us.level5.level2.var1, 'bar')
        self.assertEqual(us.level5.level2.var2, 'baz')
        self.assertEqual(us.level5.level3.var1, 'bob')

        us.update(s.modules.users)
        s.modules['users'] = us

        self.assertEqual(s.modules.users.var2, 'not bar')
        self.assertEqual(s.modules.users.var1, 'foo')
        self.assertEqual(len(s.modules.users.routes), 0)
        self.assertEqual(s.modules.users.level2.var1, 'foo')
        self.assertEqual(s.modules.users.level2.var2, 'not bar')
        self.assertEqual(s.modules.users.level3, 'string value to merge')
        self.assertEqual(s.modules.users.level4.var1, 'foo')
        self.assertEqual(s.modules.users.level4.var2, 'not bar')
        self.assertEqual(s.modules.users.level4.var3, 'baz')
        self.assertEqual(s.modules.users.level5.level1.var1.notlikely, 'foo')
        self.assertEqual(s.modules.users.level5.level2.var1, 'not_bar')
        self.assertEqual(s.modules.users.level5.level2.var2, 'baz')

        self.assertEqual(s.modules.users.enabled, True)


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.app = make_wsgi('Testruns')

    def test_appslist(self):
        self.assertEqual(['blazewebtestapp', 'blazewebtestapp2'], listapps())
        self.assertEqual(['blazewebtestapp2', 'blazewebtestapp'], listapps(reverse=True))

    def test_settings(self):
        self.assertEqual(settings.foo, 'bar')

    def test_modsettings(self):
        self.assertEqual(settings.components.tests.foo, 'baz')

    def test_settingslock(self):
        """ tests the lock() in appinit() """
        try:
            settings.notthere
        except AttributeError as e:
            assert str(e) == "object has no attribute 'notthere' (object is locked)"
        else:
            self.fail("expected AttributeError for 'notthere'")

    def test_modulesettingslock(self):
        """ tests the lock() in appinit() for module settings """
        try:
            settings.components.tests.notthere
        except AttributeError as e:
            assert str(e) == "object has no attribute 'notthere' (object is locked)"
        else:
            self.fail("expected AttributeError for 'notthere'")


class TestDefaultSettings(object):

    @classmethod
    def setup_class(cls):
        make_wsgi_min2('TestStorageDir')

    def test_storage_dir(self):
        # assume we are in a virtualenv
        assert settings.dirs.storage.endswith('storage-minimal2')


class TestComponentSettings(object):

    @classmethod
    def setup_class(cls):
        make_wsgi_min2('Dispatching')

    def test_components(self):
        pm = settings.componentmap.minimal2
        assert pm.internalonly.enabled is True
        assert pm.internalonly.packages == [None]
        assert pm.news.enabled is True
        assert pm.news.packages == [None, 'newscomp4']
        assert pm.foo.enabled is True
        assert pm.foo.packages == ['foobwp']
        assert settings.component_packages.newscomp4 == 'news'
        assert settings.component_packages.foobwp == 'foo'
        eq_(settings.component_packages.todict().keys(), ['newscomp4', 'foobwp'])
