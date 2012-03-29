# Sublime Text 2 plugin: Simple Ember.js Navigator

Simple plugin for navigating Ember.js applications (http://emberjs.com/). It
works in a similar way as my [Simple Rails
Navigator](https://github.com/noklesta/SublimeRailsNav) and can be used in
combination with that plugin to navigate the Ember.js part of a Rails
application, but it can also be used for any other Ember.js project.

The plugin provides commands for listing the following file types in a quick
panel for easy selection: models, controllers, views, templates, mixins, data
adapters, stores, statechart files, the main application file, and any other
file located in the root directory of an Ember.js application. Both JavaScript
and CoffeeScript are supported.

Your are free to name your files however you want, and the location of each
type of file can be customized either per user or per project (see below).
However, if you choose to follow certain conventions (heavily inspired by Ruby
on Rails), certain related files will be located at the top of the list so
that they can be selected simply by pressing Enter. For instance, if the
active view is an Ember model and you request a list of controllers, the
controller(s) corresponding to the model will be listed at the top.

The following examples illustrate the conventions needed for the related files
feature to work (the file names can end in either `.js`, `.coffee` or
`.js.coffee`, possibly with an additional `.erb` suffix for Rails, and the
files may be located in subfolders):

A `Post` model, a corresponding controller for listing posts, and a controller
for the currently selected post:

    post.js
    posts_controller.js
    selected_post_controller.js or current_post_controller.js

A RecentPostsView and a corresponding handlebars template:

    recent_posts_view.js
    recent_posts_view.handlebars or recent_posts.handlebars

## Installation

### Package Control

The easiest way to install this is with [Package
Control](http://wbond.net/sublime\_packages/package\_control).

 * If you just went and installed Package Control, you probably need to restart Sublime Text 2 before doing this next bit.
 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package" (it'll take a few seconds)
 * Select Simple Ember.js Navigator when the list appears.

Package Control will automatically keep SublimeEmberNav up to date with the latest
version.

### Clone from GitHub

Alternatively, you can clone the repository directly from GitHub into your Packages directory:

    git clone http://github.com/noklesta/SublimeEmberNav

## Key bindings

The plugin does not install any key bindings automatically. You can set up
your own key bindings like this:

    { "keys": ["super+ctrl+m"], "command": "list_ember_models" },
    { "keys": ["super+ctrl+c"], "command": "list_ember_controllers" },
    etc...

If you are using Vintage mode and want to use sequences of non-modifier keys,
you can restrict the key bindings to command mode like this:

    { "keys": [" ", "m"], "command": "list_ember_models", "context": [{"key": "setting.command_mode"}] },
    { "keys": [" ", "c"], "command": "list_ember_controllers", "context": [{"key": "setting.command_mode"}] },
    etc...

All commands are also available from the Command Palette (search for commands
beginning with "Simple Ember.js Navigator").

## File locations

By default, the different files are assumed to be located in folders at the
root of the project that are named after their type. Locations are specified
as regular expressions that will automatically by anchored to the beginning
and end of the path (with the root location prepended to all the other paths).
The defaults are as follows:

    "root":                 [""],

    "models_location":      ["models"],
    "controllers_location": ["controllers"],
    "views_location":       ["views"],
    "templates_location":   ["templates"],
    "mixins_location":      ["mixins"],
    "data_location":        ["data"],
    "states_location":      ["states"],

    "application_file":     ["app.(?:js|(?:js.)?coffee)(?:.erb)?"]

These settings are found in SublimeEmberNav.sublime-settings and may be
overridden either in Packages/User/SublimeEmberNav.sublime-settings or, for a
particular project, in the project file under a top-level "settings" key.

For instance, if your Ember.js applications are normally part of a Rails app,
you can set the root location in your user preferences file
(Packages/User/SublimeEmberNav.sublime-settings) like this:

    {
      "root": ["app", "assets", "javascripts"]
    }

To customize the file locations for a particular project, you can put
something like this in your project file (select "Edit project" from the
Project menu):

    "settings":
    {
      "SublimeEmberNav":
      {
        "root":   ["app", "assets", "javascripts", "ember"],
        "states": ["statecharts"]
      }
    }

## Credits

- Python version of the Rails inflector: <https://bitbucket.org/ixmatus/inflector>

## Licence

All of SublimeEmberNav is licensed under the MIT licence.

  Copyright (c) 2012 Anders Nøklestad

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.