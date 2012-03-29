import os
import re
import sublime
import sublime_plugin
from recursive_glob import rglob
from lib.inflector import *

JS_EXTENSIONS = '(?:js|(?:js.)?coffee)(?:.erb)?'
TEMPLATE_EXTENSIONS = 'handlebars(?:.erb)?'


class EmberCommandBase(sublime_plugin.WindowCommand):
    def prepare_run(self):
        if hasattr(self, 'project_settings') and hasattr(self, 'root'):
            return True

        self.find_settings()
        return self.find_root()

    def find_settings(self):
        # Find project settings, if defined
        self.project_settings = None

        view = self.window.active_view()
        if view:
            settings = view.settings()
            if settings.has('SublimeEmberNav'):
                self.project_settings = settings.get('SublimeEmberNav')

        # Find user-specific or default settings
        self.sublime_settings = sublime.load_settings('SublimeEmberNav.sublime-settings')

    def find_root(self):
        folders = self.window.folders()
        if len(folders) == 0:
            sublime.error_message('Could not find project root')
            self.root = None
            return False

        self.root = os.path.join(folders[0], *self.get_setting('root'))
        return True

    def get_setting(self, key):
        if self.project_settings and key in self.project_settings:
            # Get project-specific setting
            value = self.project_settings[key]
        else:
            # Get user-specific or default setting
            value = self.sublime_settings.get(key)
        return value

    def get_location(self, key):
        if not self.root:
            return False  # probably unable to find project root

        if key == 'models':
            return os.path.join(self.root, *self.get_setting('models_location'))
        elif key == 'controllers':
            return os.path.join(self.root, *self.get_setting('controllers_location'))
        elif key == 'views':
            return os.path.join(self.root, *self.get_setting('views_location'))
        elif key == 'templates':
            return os.path.join(self.root, *self.get_setting('templates_location'))
        elif key == 'mixins':
            return os.path.join(self.root, *self.get_setting('mixins_location'))
        elif key == 'adapters':
            return os.path.join(self.root, *self.get_setting('adapters_location'))
        elif key == 'states':
            return os.path.join(self.root, *self.get_setting('states_location'))

    def show_files(self, path, file_pattern='\.' + JS_EXTENSIONS + '$'):
        self.files = rglob(path, file_pattern)

        view = self.window.active_view()
        if view:
            current_file = view.file_name()
            if self.is_listing_current_file_group(current_file):
                self.remove_from_list(current_file)
            else:
                self.move_related_files_to_top(current_file)

        start_index = len(path) + 1
        # Need to add a couple of spaces to avoid getting the file names cut off
        relative_paths = map(lambda x: x[start_index:] + '  ', self.files)

        self.window.show_quick_panel(relative_paths, self.file_selected)

    def file_selected(self, selected_index):
        if selected_index != -1:
            self.window.open_file(self.files[selected_index])

    def remove_from_list(self, current_file):
        if current_file in self.files:
            self.files.remove(current_file)

    def move_related_files_to_top(self, current_file):
        related_file_patterns = self.construct_related_file_patterns(current_file)

        for pattern in related_file_patterns:
            for file in self.files:
                if re.match(pattern, file):
                    i = self.files.index(file)
                    self.files.insert(0, self.files.pop(i))

    # Override in subclasses
    def is_listing_current_file_group(self, current_file):
        pass

    # Override in subclasses
    def construct_related_file_patterns(self, current_file):
        pass


class ListEmberModelsCommand(EmberCommandBase):
    def run(self):
        if not self.prepare_run():
            return

        self.models_location = self.get_location('models')
        self.controllers_location = self.get_location('controllers')

        if self.models_location and self.controllers_location:
            self.show_files(self.models_location)

    def is_listing_current_file_group(self, current_file):
        return self.models_location in current_file

    def construct_related_file_patterns(self, current_file):
        if self.controllers_location in current_file:
            m = re.search(r'(?:(?:selected|current)_)?(\w+)_controller\.\w+$', current_file)
            singular = Inflector().singularize(m.group(1))
            pattern = '{0}{1}.{2}'.format(
               os.path.join(self.models_location + '.*', ''),
               singular,
               JS_EXTENSIONS
            )
            return [pattern]
        else:
            return []


class ListEmberControllersCommand(EmberCommandBase):
    def run(self):
        if not self.prepare_run():
            return

        self.controllers_location = self.get_location('controllers')
        self.models_location = self.get_location('models')

        if self.controllers_location and self.models_location:
            self.show_files(self.controllers_location)

    def is_listing_current_file_group(self, current_file):
        return self.controllers_location in current_file

    def construct_related_file_patterns(self, current_file):
        if self.models_location in current_file:
            m = re.search(r'(\w+)\.\w+$', current_file)
            plural = Inflector().pluralize(m.group(1))
            pattern = '{0}(?:(?:selected|current)_)?{1}_controller.{2}'.format(
                os.path.join(self.controllers_location + '.*', ''),
                plural,
                JS_EXTENSIONS
            )
            return [pattern]
        else:
            return []


class ListEmberViewsCommand(EmberCommandBase):
    def run(self):
        if not self.prepare_run():
            return

        self.views_location = self.get_location('views')
        self.templates_location = self.get_location('templates')

        if self.views_location and self.templates_location:
            self.show_files(self.views_location)

    def is_listing_current_file_group(self, current_file):
        return self.views_location in current_file

    def construct_related_file_patterns(self, current_file):
        if self.templates_location in current_file:
            m = re.search(r'(?P<name>\w+)\.\w+$', current_file)
            name = m.group('name')
            if not name.endswith('_view'):
                name = name + '_view'
            pattern = '{0}{1}.{2}'.format(
                os.path.join(self.views_location + '.*', ''),
                name,
                JS_EXTENSIONS
            )
            return [pattern]
        else:
            return []


class ListEmberTemplatesCommand(EmberCommandBase):
    def run(self):
        if not self.prepare_run():
            return

        self.templates_location = self.get_location('templates')
        self.views_location = self.get_location('views')

        if self.templates_location and self.views_location:
            self.show_files(self.templates_location, '\.' + TEMPLATE_EXTENSIONS + '$')

    def is_listing_current_file_group(self, current_file):
        return self.templates_location in current_file

    def construct_related_file_patterns(self, current_file):
        if self.views_location in current_file:
            m = re.search(r'(?P<name>\w+)_view\.\w+$', current_file)
            pattern = '{0}{1}(?:_view)?.{2}'.format(
                os.path.join(self.templates_location + '.*', ''),
                m.group('name'),
                TEMPLATE_EXTENSIONS
            )
            return [pattern]
        else:
            return []
