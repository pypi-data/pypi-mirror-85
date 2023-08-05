import os
import sys
import tempfile
import warnings
from django.test import TestCase
from django.conf import settings
from django_distill.distill import urls_to_distill
from django_distill.renderer import DistillRender, render_to_dir
from django_distill.errors import DistillError


class DjangoDistillRendererTestSuite(TestCase):

    def setUp(self):
        output_dir = None
        self.renderer = DistillRender(output_dir, urls_to_distill)

    def _get_view(self, name):
        for u in urls_to_distill:
            if u[2] == name:
                return u
        return False

    def _skip(self, what):
        sys.stdout.write('Missing {}, skipping test... '.format(what))
        sys.stdout.flush()

    def test_is_str(self):
        self.assertTrue(self.renderer._is_str('a'))
        self.assertFalse(self.renderer._is_str(None))
        self.assertFalse(self.renderer._is_str(1))
        self.assertFalse(self.renderer._is_str([]))
        self.assertFalse(self.renderer._is_str(()))
        self.assertFalse(self.renderer._is_str({}))
        self.assertFalse(self.renderer._is_str({'a':'a'}))
        self.assertFalse(self.renderer._is_str(object()))

    def test_get_uri_values(self):
        test = ()
        check = self.renderer.get_uri_values(lambda: test)
        self.assertEqual(check, (None,))
        test = ('a',)
        check = self.renderer.get_uri_values(lambda: test)
        self.assertEqual(check, test)
        test = (('a',),)
        check = self.renderer.get_uri_values(lambda: test)
        self.assertEqual(check, test)
        test = []
        check = self.renderer.get_uri_values(lambda: test)
        self.assertEqual(check, (None,))
        test = ['a']
        check = self.renderer.get_uri_values(lambda: test)
        self.assertEqual(check, test)
        test = [['a']]
        check = self.renderer.get_uri_values(lambda: test)
        self.assertEqual(check, test)
        for invalid in ('a', 1, b'a', {'s'}, {'a':'a'}, object()):
            with self.assertRaises(DistillError):
                self.renderer.get_uri_values(lambda: invalid)

    def test_url_no_param(self):
        view = self._get_view('url-no-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        if not param_set:
            param_set = ()
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/url/')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'test')

    def test_url_positional_param(self):
        view = self._get_view('url-positional-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/url/12345')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'test12345')

    def test_url_named_param(self):
        view = self._get_view('url-named-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/url/test')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'testtest')

    def test_re_path_no_param(self):
        if not settings.HAS_RE_PATH:
            self._skip('django.urls.re_path')
            return
        view = self._get_view('re_path-no-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        if not param_set:
            param_set = ()
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/re_path/')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'test')

    def test_re_path_positional_param(self):
        if not settings.HAS_RE_PATH:
            self._skip('django.urls.re_path')
            return
        view = self._get_view('re_path-positional-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/re_path/12345')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'test12345')

    def test_re_path_named_param(self):
        if not settings.HAS_RE_PATH:
            self._skip('django.urls.re_path')
            return
        view = self._get_view('re_path-named-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/re_path/test')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'testtest')

    def test_re_broken(self):
        if not settings.HAS_RE_PATH:
            self._skip('django.urls.re_path')
            return
        view = self._get_view('re_path-broken')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        if not param_set:
            param_set = ()
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/re_path/broken')
        with self.assertRaises(DistillError):
            self.renderer.render_view(uri, param_set, args)

    def test_path_no_param(self):
        if not settings.HAS_PATH:
            self._skip('django.urls.path')
            return
        view = self._get_view('path-no-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        if not param_set:
            param_set = ()
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/path/')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'test')

    def test_path_positional_param(self):
        if not settings.HAS_PATH:
            self._skip('django.urls.path')
            return
        view = self._get_view('path-positional-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/path/12345')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'test12345')

    def test_path_named_param(self):
        if not settings.HAS_PATH:
            self._skip('django.urls.path')
            return
        view = self._get_view('path-named-param')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/path/test')
        render = self.renderer.render_view(uri, param_set, args)
        self.assertEqual(render.content, b'testtest')

    def test_path_broken(self):
        if not settings.HAS_PATH:
            self._skip('django.urls.path')
            return
        view = self._get_view('path-broken')
        assert view
        view_func, file_name, view_name, args, kwargs = view
        param_set = self.renderer.get_uri_values(view_func)[0]
        if not param_set:
            param_set = ()
        uri = self.renderer.generate_uri(view_name, param_set)
        self.assertEqual(uri, '/path/broken')
        with self.assertRaises(DistillError):
            self.renderer.render_view(uri, param_set, args)

    def test_render_paths(self):
        def _blackhole(_):
            pass
        expected_files = (
            ('test',),
            ('url', '12345'),
            ('url', 'test'),
            ('re_path', '12345'),
            ('re_path', 'test'),
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            with self.assertRaises(DistillError):
                render_to_dir(tmpdirname, urls_to_distill, _blackhole)
            written_files = []
            for (root, dirs, files) in os.walk(tmpdirname):
                for f in files:
                    filepath = os.path.join(root, f)
                    written_files.append(filepath)
            for expected_file in expected_files:
                filepath = os.path.join(tmpdirname, *expected_file)
                self.assertIn(filepath, written_files)

    def test_sessions_are_ignored(self):
        if settings.HAS_PATH:
            view = self._get_view('path-ignore-sessions')
            assert view
            view_func, file_name, view_name, args, kwargs = view
            param_set = self.renderer.get_uri_values(view_func)[0]
            if not param_set:
                param_set = ()
            uri = self.renderer.generate_uri(view_name, param_set)
            self.assertEqual(uri, '/path/ignore-sessions')
            with warnings.catch_warnings(record=True) as w:
                render = self.renderer.render_view(uri, param_set, args)
                self.assertEqual(len(w), 1)
                caught_warning = w[0]
                self.assertEqual(caught_warning.category, RuntimeWarning)
            self.assertEqual(render.content, b'test')
        uri = self.renderer.generate_uri(view_name, param_set)
        if settings.HAS_RE_PATH:
            view = self._get_view('re_path-ignore-sessions')
            assert view
            view_func, file_name, view_name, args, kwargs = view
            param_set = self.renderer.get_uri_values(view_func)[0]
            if not param_set:
                param_set = ()
            uri = self.renderer.generate_uri(view_name, param_set)
            self.assertEqual(uri, '/re_path/ignore-sessions')
            with warnings.catch_warnings(record=True) as w:
                render = self.renderer.render_view(uri, param_set, args)
                self.assertEqual(len(w), 1)
                caught_warning = w[0]
                self.assertEqual(caught_warning.category, RuntimeWarning)
            self.assertEqual(render.content, b'test')
