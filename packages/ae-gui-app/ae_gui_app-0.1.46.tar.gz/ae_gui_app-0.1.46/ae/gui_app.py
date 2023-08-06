"""
base class for python applications with a graphical user interface
==================================================================

The abstract base class :class:`MainAppBase` provided by this ae namespace portion allows the integration of any Python
GUI framework into the ae namespace.

On overview about the available GUI-framework-specific ae namespace portion implementations can be found in the
documentation of the ae namespace portion :mod:`ae.lisz_app_data`.


extended console application environment
----------------------------------------

The abstract base class :class:`MainAppBase` inherits directly from the ae namespace class
:class:`ae console application environment class <ae.console.ConsoleApp>`. The so inherited helper methods are useful
for to log, configure and control the run-time of your GUI app via command line arguments.

.. hint::
    Please see the documentation of :ref:`config-options` and :ref:`config-files` in the :mod:`ae.console` namespace
    portion/module for more detailed information.

:class:`MainAppBase` adds on top of the :class:`~ae.console.ConsoleApp` the concepts of :ref:`application status` and
:ref:`application flow`, explained further down.


application events
------------------

The following application events are fired exactly one time in the lifetime of an app instance in the following order:

* `on_app_init`: fired **after** :class:`ConsoleApp`-parts of the app instance got initialized (detected config files)
  and **before** the image and sound resources and app states get loaded and the GUI framework app class instance gets
  initialized.
* `on_app_start`: fired **after** the call of the method :meth:`~MainAppBase.run_app` and **before** the command line
  options got parsed.
* `on_app_run`: fired **after** the parsing of the command line arguments and options and **before** the framework event
  loop of the used GUI framework gets started.
* `on_app_stop`: fired **after** the call of the method :meth:`~MainAppBase.stop_app` and **before** the framework win
  will be closed.
* `on_app_exit`: fired **after* framework win got closed and just **before** the event loop of the GUI framework will be
  stopped and the app shutdown.
* `on_app_quit`: fired **after** the event loop of the GUI framework got stopped and before the :meth:`AppBase.shutdown`
  method will be called.

.. note::
    The `on_app_stop` and `on_app_exit` events will only be fired if the app is explicitly calling the
    :meth:`~MainAppBase.stop_app` method.


application status
------------------

Any application- and user-specific configurations like e.g. the last window position/size, the app theme/font/language
or the last selected flow within your app, could be included in the application status.

This namespace portion introduces the section `aeAppState` in the app :ref:`config-files`, where any status values can
be stored persistently for to be recovered on the next startup of your application.

.. hint::
    The section name `aeAppState` is declared by the :data:`APP_STATE_SECTION_NAME` constant. If you need to access this
    config section directly then please use this constant instead of the hardcoded section name.


.. _app-state-variables:

app state variables
^^^^^^^^^^^^^^^^^^^

This module is providing/pre-defining the following application state variables:

    * :attr:`~MainAppBase.flow_id`
    * :attr:`~MainAppBase.flow_path`
    * :attr:`~MainAppBase.font_size`
    * :attr:`~MainAppBase.lang_code`
    * :attr:`~MainAppBase.light_theme`
    * :attr:`~MainAppBase.sound_volume`
    * :attr:`~MainAppBase.vibration_volume`
    * :attr:`~MainAppBase.win_rectangle`

Which app state variables are finally used by your app project is (fully data-driven) depending on the app state
:ref:`config-variables` detected in all the :ref:`config-files` that are found/available at run-time of your app.
The names of all the available application state variables can be determined with the main app helper method
:meth:`~MainAppBase.app_state_keys`.

If your application is e.g. supporting a user-defined font size, using the provided/pre-defined app state variable
:attr:`~MainAppBase.font_size`, then it has to call the method :meth:`change_app_state` with the
:paramref:`~MainAppBase.change_app_state.state_name` set to `font_size` every time when the user has changed the font
size of your app.

.. hint::
    The two built-in app state variables are :attr:`~MainAppBase.flow_id` and :attr:`~MainAppBase.flow_path` will be
    explained detailed in the next section.

The :meth:`~MainBaseApp.load_app_states` method is called on instantiation from the implemented main app class for to
load the values of all app state variables from the :ref:`config-files`, and is then calling
:meth:~MainAppBase.setup_app_states` for pass them into their corresponding instance attributes.

Use the main app instance attribute for to read/get the actual value of a single app state variable. The actual values
of all app state variables as a dict is determining the method :meth:`~MainBaseApp.retrieve_app_states`, and can be
saved into the :ref:`config-files` for the next app run via the method :meth:`~MainBaseApp.save_app_states` - this could
be done e.g. after the app state has changed or at least on quiting the application.

Changed app state values have to be saved always by calling the method :meth:`~MainBaseApp.change_app_state` (which
ensures (1) the propagation to any duplicated (observable/bound) framework property and (2) the event notification to
related the main app instance method).


.. _app-state-constants:

app state constants
^^^^^^^^^^^^^^^^^^^

This module is also providing some pre-defined constants that can be optionally used in your application in relation
to the app states data store and for the app state config variables :attr:`~MainAppBase.font_size` and
:attr:`~MainAppBase.light_theme`:

    * :data:`APP_STATE_SECTION_NAME`
    * :data:`APP_STATE_VERSION_VAR_NAME`
    * :data:`APP_STATE_CURRENT_VERSION`
    * :data:`MIN_FONT_SIZE`
    * :data:`MAX_FONT_SIZE`
    * :data:`THEME_LIGHT_BACKGROUND_COLOR`
    * :data:`THEME_LIGHT_FONT_COLOR`
    * :data:`THEME_DARK_BACKGROUND_COLOR`
    * :data:`THEME_DARK_FONT_COLOR`


app state change and save events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Notification events get fired when one of the app state variables gets changed - like e.g. the :ref:`application flow`
or if the user changes the font size.

The method name of the app state change notification event consists of the prefix ``on_`` followed by the variable name
of the app state. So e.g. on a change of the `font_size` app state the notification event `on_font_size` will be
fired/called (if exists as a method of the main app instance). These events don't provide any event arguments.

Another event gets fired for each app state value just after the app states getting retrieved from the app class
instance and before they get stored into the main config file.

This method name of this event includes the key/name of the app state using the format
:meth:`on_app_state_<app_state_key>_save`, so e.g. for the app state `flow_id` the method name will result in
:meth:`on_app_state_flow_id_save`.

The event is taking one event argument with the value of the app state and if it returns a value that is
not `None` then this value will be stored/saved.


application flow
----------------

For to control the current state and application/work flow (or context) of your application, and to persist it until
the next app start, :class:`MainBaseApp` provides two :ref:`app-state-variables`: :attr:`~MainAppBase.flow_id` for to
store the currently working flow and :attr:`~MainAppBase.flow_path` for to store the history of nested flows.

A application flow is represented by an id string that defines three things: (1) the action for to enter into the flow,
(2) the data or object that gets currently worked on and (3) an optional key string that is identifying/indexing a
widget or data item of your application context/flow.

.. note::
    Never concatenate a flow id string manually, use the :func:`id_of_flow` function instead.

The flow id is initially an empty string. As soon as the user is starting a new work flow or the current selection your
application should call the method :meth:`~MainBaseApp.change_flow` passing the flow id string into the
:paramref:`~MainAppBase.change_flow.new_flow_id` argument for to change the app flow.

For more complex applications you can specify a path of nested flows. This flow path gets represented by the app state
variable :attr:`~MainAppBase.flow_path`, which is a list of flow id strings.

For to enter into a deeper/nested flow you simply call :meth:`~MainBaseApp.change_flow` with one of the actions defined
in :data:`ACTIONS_EXTENDING_FLOW_PATH`.

For to go back to a previous flow in the flow path call :meth:`~MainBaseApp.change_flow` passing one of the actions
defined in :data:`ACTIONS_REDUCING_FLOW_PATH`.


application flow change events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The flow actions specified by :data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` don't need a flow change
confirmation event handler:

* `'enter'` or `'leave'` extend/reduce the flow path.
* `'focus'` pass/change the input focus.
* `'suggest'` for autocompletion or other suggestions.

All other flow actions need to confirmed for to be changed by :meth:`~MainAppBase.change_flow`, either by
a custom flow change confirmation method/event-handler or by declaring a popup class that has the same name
returned by :func:`flow_popup_class_name` if called with the new flow id.

The name of the flow change confirmation method that gets fired when the app want to change the flow (via the method
:meth:`~MainAppBase.change_flow`) depends on the new flow id and gets determined by the function
:func:`flow_change_confirmation_event_name`.

If the flow-specific change confirmation event handler does not exist or returns in a boolean `False` or `None`
then :meth:`~MainAppBase.on_flow_change` will be called. And if this call also returns `False` then the action
of the new flow id will be searched within :data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` and if not found
then the flow change will be rejected and :meth:`~MainAppBase.change_flow` returns `False`

If in contrary either the flow change confirmation event handler exists and does return `True` or
:meth:`~MainAppBase.on_flow_change` returns True or the flow action of the new flow id is in
:data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` then the flow id and path will be changed accordingly.

After the flow id/path change confirmation the method :meth:`~MainAppBase.change_flow` checks if the
optional event_kwargs key `changed_event_name` got specified and if yes then it calls this method.

Finally if a confirmed flow change is resulting in a `'focus'` flow action then the event `on_flow_widget_focused`
will be fired. This event can be used by the GUI framework for to set the focus to the widget associated with
the new focus flow id.


key press events
----------------

For to provide key press events to the applications that will use the new GUI framework you have to catch the key press
events of the framework, convert/normalize them and then call the :meth:`~MainAppBase.key_press_from_framework` with the
normalized modifiers and key args.

The :paramref:`~MainAppBase.key_press_from_framework.modifiers` arg is a string that can contain several of the
following sub-strings, always in the alphabetic order (like listed below):

* Alt
* Ctrl
* Meta
* Shift

The :paramref:`~MainAppBase.key_press_from_framework.key` arg is a string that is specifying the last pressed key. If
the key is not representing not a single character but a command key, then `key` will be one of the following strings:

* escape
* tab
* backspace
* enter
* del
* enter
* up
* down
* right
* left
* home
* end
* pgup
* pgdown

On call of :meth:`~MainAppBase.key_press_from_framework` this method will try to dispatch the key press event to your
application. First it will check the app instance if it has declared a method with the name
`on_key_press_of_<modifiers>_<key>` and if so it will call this method.

If this method does return False (or any other value resulting in False) then method
:meth:`~MainAppBase.key_press_from_framework` will check for a method with the same name in lower-case and if exits
it will call this method.

If also the second method does return False, then it will try to call the event method `on_key_press` of the app
instance (if exists) with the modifiers and the key as arguments.

If the `on_key_press` method does also return False then :meth:`~MainAppBase.key_press_from_framework` will finally pass
the key press event to the original key press handler of the GUI framework for further processing.


integrate new gui framework
---------------------------

For to integrate a new Python GUI framework you have to declare a new class that inherits from :class:`MainAppBase` and
implements at least the abstract method :meth:`~MainAppBase.init_app`.

A minimal implementation of this method would look like::

    def init_app(self):
        return None, None

Most GUI frameworks are providing classes that need to be instantiated for the application, the root layout of the app
and for each window. For to keep a reference to these instances within your main app class you can use the attributes
:attr:`~MainAppBase.framework_app`, :attr:`~MainAppBase.framework_root` and :attr:`~MainAppBase.framework_win` of
:class:`MainAppBase`.

The initialization of the attributes :attr:`~MainAppBase.framework_app`, :attr:`~MainAppBase.framework_root` and
:attr:`~MainAppBase.framework_win` is optional and can be done e.g. within :meth:`~MainAppBase.init_app` or in the later
called `build` method of the framework app instance.

.. note::
    If :attr:`~MainAppBase.framework_win` is set to a window instance, then the window instance has to provide a `close`
    method, which will be called automatically by the :meth:`~MainAppBase.stop_app`.

A typical implementation of a framework-specific main app class looks like::

    from new_gui_framework import NewFrameworkApp, MainWindowClassOfNewFramework

    class NewFrameworkMainApp(MainAppBase):
        def init_app(self):
            self.framework_app = NewFrameworkAppClass()
            self.framework_win = MainWindowClassOfNewFramework()

            return self.framework_app.start, self.framework_app.stop

:meth:`~MainAppBase.init_app` will be executed only once at the main app class instantiation. Only the main app instance
has to initialize the GUI framework for to prepare the app startup and has to return at least a callable for to start
the event loop of the GUI framework.

.. hint::
    Although not recommended because of possible namespace conflicts, one could e.g. alternatively integrate the
    framework application class as a mixin to the main app class.

For to finally startup the app the :meth:`~MainAppClass.run_app` method has to be called from the main module of your
app project. :meth:`~MainAppBase.run_app` will then start the GUI event loop by calling the first method that got
returned by :meth:`~MainAppBase.init_app`.


optional configuration and extension
------------------------------------

Most of the base implementation helper methods can be overwritten by either the inheriting framework portion or directly
by user main app class.
"""
from abc import ABC, abstractmethod
import re
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from ae.base import NAME_PARTS_SEP, snake_to_camel                  # type: ignore
from ae.updater import check_all                                    # type: ignore
from ae.inspector import stack_var                                  # type: ignore
from ae.files import FilesRegister, RegisteredFile                  # type: ignore
from ae.i18n import default_language                                # type: ignore
from ae.core import DEBUG_LEVELS                                    # type: ignore
from ae.console import ConsoleApp                                   # type: ignore


__version__ = '0.1.46'


AppStateType = Dict[str, Any]                   #: app state config variable type

APP_STATE_SECTION_NAME = 'aeAppState'           #: config section name for to store app state

#: config variable name for to store the current application state version
APP_STATE_VERSION_VAR_NAME = 'app_state_version'
APP_STATE_CURRENT_VERSION: int = 3              #: current application state version

MIN_FONT_SIZE = 15.0                            #: minimum font size in pixels
MAX_FONT_SIZE = 99.0                            #: maximum font size in pixels

COLOR_BLACK = (0.009, 0.006, 0.003, 1.0)        # for to differentiate from framework pure black/white colors
COLOR_WHITE = (0.999, 0.996, 0.993, 1.0)
THEME_DARK_BACKGROUND_COLOR = COLOR_BLACK       #: dark theme background color in rgba(0.0 ... 1.0)
THEME_DARK_FONT_COLOR = COLOR_WHITE             #: dark theme font color in rgba(0.0 ... 1.0)
THEME_LIGHT_BACKGROUND_COLOR = COLOR_WHITE      #: light theme background color in rgba(0.0 ... 1.0)
THEME_LIGHT_FONT_COLOR = COLOR_BLACK            #: light theme font color in rgba(0.0 ... 1.0)


check_all()     # let ae_updater module check/install any outstanding updates or new app versions


FLOW_KEY_SEP = ':'

FLOW_ACTION_RE = re.compile("[a-z0-9]+")
FLOW_OBJECT_RE = re.compile("[A-Za-z0-9_]+")

ACTIONS_EXTENDING_FLOW_PATH = ['add', 'confirm', 'edit', 'enter', 'open', 'show', 'suggest']
ACTIONS_REDUCING_FLOW_PATH = ['close', 'leave']
ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION = ['', 'enter', 'focus', 'leave', 'suggest']


def id_of_flow(action: str, obj: str = "", key: str = "") -> str:
    """ create flow id string.

    :param action:      flow action string.
    :param obj:         flow object (defined by app project).
    :param key:         flow index/item_id/field_id/... (defined by app project).
    :return:            complete flow_id string.
    """
    assert action == '' or FLOW_ACTION_RE.fullmatch(action), \
        f"flow action only allows lowercase letters and digits: got '{action}'"
    assert obj == '' or FLOW_OBJECT_RE.fullmatch(obj), \
        f"flow object only allows letters, digits and underscores: got '{obj}'"
    cid = f'{action}{NAME_PARTS_SEP if action and obj else ""}{obj}'
    if key:
        cid += f'{FLOW_KEY_SEP}{key}'
    return cid


def flow_action(flow_id: str) -> str:
    """ determine the action string of a flow_id.

    :param flow_id:         flow id.
    :return:                flow action string.
    """
    return flow_action_split(flow_id)[0]


def flow_action_split(flow_id: str) -> Tuple[str, str]:
    """ split flow id string into action part and the rest.

    :param flow_id:         flow id.
    :return:                tuple of (flow action string, flow obj and key string)
    """
    idx = flow_id.find(NAME_PARTS_SEP)
    if idx != -1:
        return flow_id[:idx], flow_id[idx + 1:]
    return flow_id, ""


def flow_key(flow_id: str) -> str:
    """ return the key of a flow id.

    :param flow_id:         flow id string.
    :return:                flow key string.
    """
    _action_object, index = flow_key_split(flow_id)
    return index


def flow_key_split(flow_id: str) -> Tuple[str, str]:
    """ split flow id into action with object and flow key.

    :param flow_id:         flow id to split.
    :return:                tuple of (flow action and object string, flow key string).
    """
    idx = flow_id.find(FLOW_KEY_SEP)
    if idx != -1:
        return flow_id[:idx], flow_id[idx + 1:]
    return flow_id, ""


def flow_change_confirmation_event_name(flow_id: str) -> str:
    """ determine the name of the event method for the change confirmation of the passed flow_id.

    :param flow_id:         flow id.
    :return:                tuple with 2 items containing the flow action and the object name (and id).
    """
    flow, _index = flow_key_split(flow_id)
    action, obj = flow_action_split(flow)
    return f'on_{obj}_{action}'


def flow_popup_class_name(flow_id: str) -> str:
    """ determine name of the Popup class for the given flow id.

    :param flow_id:         flow id.
    :return:                name of the Popup class.
    """
    flow, _index = flow_key_split(flow_id)
    action, obj = flow_action_split(flow)
    return f'{snake_to_camel(obj)}{action.capitalize()}Popup'


def replace_flow_action(flow_id: str, new_action: str):
    """ replace action in given flow id.

    :param flow_id:         flow id.
    :param new_action:      action to be set/replaced within passed flow id.
    :return:                flow id with new action and object/key from passed flow id.
    """
    return id_of_flow(new_action, *flow_key_split(flow_action_split(flow_id)[1]))


class MainAppBase(ConsoleApp, ABC):
    """ abstract base class for to implement a GUIApp-conform app class """
    # app states
    app_state_version: int = 0                              #: version number of the app state variables in <config>.ini
    flow_id: str = ""                                       #: id of the current app flow (entered by the app user)
    flow_path: List[str]                                    #: list of flow ids, reflecting recent user actions
    font_size: float = 21.0                                 #: font size used for toolbar and flow screens
    lang_code: str = ""                                     #: optional language code (e.g. 'es_ES' for Spanish)
    light_theme: bool = False                               #: True=light theme/background, False=dark theme
    sound_volume: float = 0.12                              #: sound volume of current app (0.0=mute, 1.0=max)
    vibration_volume: float = 0.3                           #: vibration volume of current app (0.0=mute, 1.0=max)
    win_rectangle: tuple = (0, 0, 800, 600)                 #: window coordinates (x, y, width, height)

    # optional generic run-time shortcut references
    framework_app: Any = None                               #: app class instance of the used GUI framework
    framework_win: Any = None                               #: window instance of the used GUI framework
    framework_root: Any = None                              #: app root layout widget

    # optional app resources caches
    image_files: Optional[FilesRegister] = None             #: image/icon files
    sound_files: Optional[FilesRegister] = None             #: sound/audio files

    def __init__(self, **console_app_kwargs):
        """ create instance of app class.

        :param console_app_kwargs:  kwargs to be passed to the __init__ method of :class:`~ae.console_app.ConsoleApp`.
        """
        self._exit_code: int = 0                            #: init by stop_app() and passed onto OS by run_app()
        self._last_focus_flow_id: str = id_of_flow('')      #: id of the last valid focused window/widget/item/context

        self._start_event_loop: Optional[Callable]          #: callable to start event loop of GUI framework
        self._stop_event_loop: Optional[Callable]           #: callable to start event loop of GUI framework

        self.flow_path = list()  # init for Literal type recognition - will be overwritten by setup_app_states()

        super().__init__(**console_app_kwargs)

        self.call_method('on_app_init')

        self.load_images()
        self.load_sounds()

        self._start_event_loop, self._stop_event_loop = self.init_app()

        self.load_app_states()

    @abstractmethod
    def init_app(self, framework_app_class: Any = None) -> Tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and root window/layout, return GUI event loop start/stop methods.

        :param framework_app_class:     class to create app instance (optionally extended by app project).
        :return:                        tuple of two callable, the 1st for to start and the 2nd for to stop/exit
                                        the GUI event loop.
        """

    # app state helper methods

    def app_state_keys(self) -> Tuple[str, ...]:
        """ determine current config variable names/keys of the app state section :data:`APP_STATE_SECTION_NAME`.

        :return:                tuple of all app state item keys (config variable names).
        """
        return self.cfg_section_variable_names(APP_STATE_SECTION_NAME)

    def change_app_state(self, state_name: str, state_value: Any, send_event: bool = True):
        """ change app state to :paramref:`~change_app_state.state_value` in self.<state_name> and app_state dict item.

        :param state_name:      name of the app state to change.
        :param state_value:     new value of the app state to change.
        :param send_event:      pass False to prevent to send/call the on_<state_name> event to the main app instance.
        """
        self.vpo(f"MainAppBase.change_app_state({state_name}, {state_value}, {send_event})"
                 f" flow={self.flow_id} last={self._last_focus_flow_id} path={self.flow_path}")
        self.change_observable(state_name, state_value, is_app_state=True)
        if send_event:
            self.call_method('on_' + state_name)

    def change_observable(self, name: str, value: Any, is_app_state: bool = False):
        """ change observable attribute/member/property in framework_app instance (and shadow copy in main app).

        :param name:            name of the observable attribute/member or key of an observable dict property.
        :param value:           new value of the observable.
        :param is_app_state:    pass True for an app state observable.
        """
        setattr(self, name, value)
        if is_app_state:
            if hasattr(self.framework_app, 'app_states'):       # has observable DictProperty duplicates
                self.framework_app.app_states[name] = value
            name = 'app_state_' + name
        if hasattr(self.framework_app, name):                   # has observable attribute duplicate
            setattr(self.framework_app, name, value)

    def load_app_states(self):
        """ load application state from the config files for to prepare app.run_app """
        app_states = dict()
        for key in self.app_state_keys():
            app_states[key] = self.get_var(key, section=APP_STATE_SECTION_NAME)

        self.setup_app_states(app_states)

    def on_app_init(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_init default/fallback flow change confirmation event handler called")

    def on_app_start(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_start default/fallback flow change confirmation event handler called")

    def on_app_run(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_run default/fallback flow change confirmation event handler called")

    def on_app_stop(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_stop default/fallback flow change confirmation event handler called")

    def on_app_exit(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_exit default/fallback flow change confirmation event handler called")

    def on_app_quit(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_quit default/fallback flow change confirmation event handler called")

    def on_debug_level_change(self, debug_level: str, _event_kwargs: Dict[str, Any]) -> bool:
        """ debug level app state change flow change confirmation event handler.

        :param debug_level:     the new debug level name to be set (passed as flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                True for to confirm the debug level change.
        """
        level = next(num for num, name in DEBUG_LEVELS.items() if name == debug_level)
        self.vpo(f"MainAppBase.on_debug_level_change to {debug_level} -> {level}")
        self.set_opt('debug_level', level)
        return True

    def on_lang_code_change(self, lang_code: str, _event_kwargs: Dict[str, Any]) -> bool:
        """ language app state change flow change confirmation event handler.

        :param lang_code:       the new language code to be set (passed as flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                True for to confirm the language change.
        """
        self.vpo(f"MainAppBase.on_lang_code_change to {lang_code}")
        self.change_app_state('lang_code', lang_code)
        if lang_code:
            default_language(lang_code)
            self.set_var('lang_code', lang_code, section=APP_STATE_SECTION_NAME)  # add optional app state var to config
        return True

    def on_light_theme_change(self, _flow_key: str, event_kwargs: Dict[str, Any]) -> bool:
        """ app theme app state change flow change confirmation event handler.

        :param _flow_key:       flow key.
        :param event_kwargs:    event kwargs with key `'light_theme'` containing True|False for light|dark theme.
        :return:                True for to confirm change of flow id.
        """
        light_theme: bool = event_kwargs['light_theme']
        self.vpo(f"MainAppBase.on_light_theme_change to {light_theme}")
        self.change_app_state('light_theme', light_theme)
        return True

    def retrieve_app_states(self) -> AppStateType:
        """ determine the state of a running app from the main app instance and return it as dict.

        :return:                dict with all app states available in the config files.
        """
        app_state = dict()
        for key in self.app_state_keys():
            app_state[key] = getattr(self, key)

        self.dpo(f"MainAppBase.retrieve_app_states {app_state}")
        return app_state

    def save_app_states(self) -> str:
        """ save app state in config file.

        :return:                empty string if app status could be saved into config files else error message.
        """
        err_msg = ""

        app_state = self.retrieve_app_states()

        for key, state in app_state.items():
            if isinstance(state, (list, dict)):
                state = deepcopy(state)

            new_state = self.call_method(f'on_app_state_{key}_save', state)
            if new_state is not None:
                state = new_state

            if key == 'flow_id' and flow_action(state) != 'focus':
                state = id_of_flow('')
            elif key == 'flow_path':
                state = [flow_id for flow_id in state if flow_action(flow_id) == 'enter']

            err_msg = self.set_var(key, state, section=APP_STATE_SECTION_NAME)
            self.vpo(f"MainAppBase.save_app_state {key}={state} {err_msg or 'OK'}")
            if err_msg:
                break
        self.load_cfg_files()

        if self.debug_level:
            self.play_sound('error' if err_msg else 'debug_save')
        return err_msg

    def setup_app_states(self, app_states: AppStateType):
        """ put app state variables into main app instance for to prepare framework app.run_app.

        :param app_states:      dict of app states.
        """
        self.vpo(f"MainAppBase.setup_app_states {app_states}")
        for key, val in app_states.items():
            self.change_app_state(key, val, send_event=False)   # don't send on_-events as framework is not initialized
            if key == 'flow_id' and flow_action(val) == 'focus':
                self._last_focus_flow_id = val

        def upd_app_state(upd_key, upd_val, old_name=''):
            """ update and optionally rename app state in app instance and config file. """
            self.change_app_state(upd_key, upd_val, send_event=False)
            self.set_var(upd_key, upd_val, section=APP_STATE_SECTION_NAME, old_name=old_name)

        config_file_version = app_states.get(APP_STATE_VERSION_VAR_NAME, 0)
        for version in range(config_file_version, APP_STATE_CURRENT_VERSION):
            if version == 0:
                upd_app_state('light_theme', True)
            elif version == 1:
                upd_app_state('sound_volume', 0.96)
            elif version == 2:
                if 'context_id' not in app_states:
                    continue    # update - only needed for LiszApp apps

                def mig_node(parent_node):
                    """ recursively migrate sub_list to node key. """
                    new_parent_node = list()
                    for item in parent_node:
                        node = item.pop('sub_list', None)
                        if node is not None:
                            item['node'] = mig_node(node)
                        new_parent_node.append(item)
                    return new_parent_node
                upd_app_state('root_node', mig_node(app_states['data_tree']), 'data_tree')
                upd_app_state('flow_path_ink', app_states['context_path_ink'], 'context_path_ink')
                upd_app_state('flow_id_ink', app_states['context_id_ink'], 'context_id_ink')
                upd_app_state('flow_path', [], 'context_path')
                upd_app_state('flow_id', '', 'context_id')

        if config_file_version < APP_STATE_CURRENT_VERSION:
            upd_app_state(APP_STATE_VERSION_VAR_NAME, APP_STATE_CURRENT_VERSION)

    # flow helper methods

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ search class name in framework modules as well as in app main.py for to return class object.

        dirty fallback using the inspect module - implemented as method for to allow overwrite in your app project.

        :param class_name:      name of the class.
        :return:                class object with the specified class name or None if not found.
        """
        return stack_var(class_name)

    def change_flow(self, new_flow_id: str, **event_kwargs) -> bool:
        """ try to change/switch the current flow id to the value passed in :paramref:`~change_flow.new_flow_id`.

        :param new_flow_id:     new flow id (maybe overwritten by flow change confirmation event handlers by
                                assigning a flow id to event_kwargs['flow_id']).

        :param event_kwargs:    optional args to pass additional data or info onto and from the flow change
                                confirmation event handler.

                                The following keys are currently supported/implemented by this module/portion
                                (additional keys can be added by the modules/apps using this method):

                                * `changed_event_name`: optional main app event method name to be called
                                  if the flow got confirmed and changed.
                                * `count`: optional number used for to render a pluralized help text
                                  for this flow change (for this gets also passed to the help text renderer by/in
                                  :meth:`~ae.gui_help.HelpAppBase.change_flow`).
                                * `edit_widget`: optional widget instance for edit/input.
                                * `flow_id`: process :attr:`~MainAppBase.flow_path` as specified by the
                                  :paramref:`~change_flow.new_flow_id` argument, but then overwrite this
                                  flow id with this event arg value for to set :attr:`~MainAppBase.flow_id`.
                                * `popup_kwargs`: optional dict passed to the Popup `__init__` method,
                                  like e.g. dict(parent=parent_widget_of_popup, data=...).
                                * `popups_to_close`: optional sequence of widgets to be closed by this
                                  method after flow change got confirmed. For to prevent weakref-errors
                                  the `attach_to` attribute of each widget will additionally be reset to None.
                                * 'reset_last_focus_flow_id': pass `True` for to reset the last focus flow id
                                  to an empty flow id, pass `False` or `None` for to ignore the last focus id
                                  (and not use for to set flow id) or pass a flow id string value
                                  for to change the last focus flow id to the passed value.
                                * `tap_widget`: optional tapped button widget instance (initiating this
                                  flow change).

                                Some of these keys get passed directly on the call of this method, e.g.
                                via :attr:`~ae.kivy_app.FlowButton.tap_kwargs` or
                                :attr:`~ae.kivy_app.FlowToggler.tap_kwargs`, where others get added by the
                                flow change confirmation handlers/callbacks.

        :return:                True if flow got confirmed by a declared custom flow change confirmation event handler
                                (either event method or Popup class) of the app and changed accordingly, else False.

                                Some flow actions are handled internally independent from the
                                return value of a found/declared custom event handler, like e.g. `'enter'` or `'leave'`
                                will always extend/reduce the flow path and the action `'focus'` will give the
                                indexed widget the input focus (these exceptions are configurable via
                                the list :data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION`).
        """
        self.vpo(f"MainAppBase.change_flow '{new_flow_id}'/'{self.flow_id}' path={self.flow_path} kwa={event_kwargs}")

        action = flow_action(new_flow_id)
        if not self.call_method(flow_change_confirmation_event_name(new_flow_id), flow_key(new_flow_id), event_kwargs) \
                and not self.on_flow_change(new_flow_id, event_kwargs) \
                and action not in ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION:
            self.vpo(f"MainAppBase.change_flow REJECTED '{new_flow_id}'/'{self.flow_id}' path={self.flow_path}"
                     f" kwa={event_kwargs}")
            return False

        has_flow_focus = flow_action(self.flow_id) == 'focus'
        empty_flow = id_of_flow('')
        if action in ACTIONS_EXTENDING_FLOW_PATH:
            if action == 'edit' and self.flow_path_action() == 'edit' \
                    and flow_key_split(self.flow_path[-1])[0] == flow_key_split(new_flow_id)[0]:
                self.flow_path.pop()
            self.flow_path.append(new_flow_id)
            self.change_app_state('flow_path', self.flow_path)
            flow_id = empty_flow if action == 'enter' else new_flow_id
        elif action in ACTIONS_REDUCING_FLOW_PATH:
            # dismiss gets sent sometimes twice (e.g. on heavy double-clicking on drop-down-open-buttons)
            # .. therefore prevent run-time error
            if not self.flow_path:
                self.dpo(f"MainAppBase.change_flow: ignoring multiple dismiss on empty flow path; action='{action}'")
                return False
            ended_flow_id = self.flow_path.pop()
            self.change_app_state('flow_path', self.flow_path)
            if action == 'leave':
                flow_id = replace_flow_action(ended_flow_id, 'focus')
            else:
                flow_id = self.flow_id if has_flow_focus else empty_flow
        else:
            flow_id = new_flow_id if action == 'focus' else (self.flow_id if has_flow_focus else empty_flow)

        popups_to_close = event_kwargs.get('popups_to_close', ())
        for widget in reversed(popups_to_close):
            widget.close()
            widget.attach_to = None     # mainly for DropDown widgets to prevent weakref-error/-exception

        if action not in ACTIONS_REDUCING_FLOW_PATH or not has_flow_focus:
            flow_id = event_kwargs.get('flow_id', flow_id)  # update flow_id from event_kwargs
        if 'reset_last_focus_flow_id' in event_kwargs:
            last_flow_id = event_kwargs['reset_last_focus_flow_id']
            if last_flow_id is True:
                self._last_focus_flow_id = empty_flow
            elif isinstance(last_flow_id, str):
                self._last_focus_flow_id = last_flow_id
        elif flow_id == empty_flow and self._last_focus_flow_id and action not in ACTIONS_EXTENDING_FLOW_PATH:
            flow_id = self._last_focus_flow_id
        self.change_app_state('flow_id', flow_id)

        changed_event_name = event_kwargs.get('changed_event_name', '')
        if changed_event_name:
            self.call_method(changed_event_name)

        if flow_action(flow_id) == 'focus':
            self.call_method('on_flow_widget_focused')
            self._last_focus_flow_id = flow_id

        self.vpo(f"MainAppBase.change_flow CHANGED '{new_flow_id}'/'{self.flow_id}'/'{self._last_focus_flow_id}'"
                 f" path={self.flow_path} kwa={event_kwargs}")

        return True

    def flow_path_action(self, flow_path: Optional[List[str]] = None, path_index: int = -1) -> str:
        """ determine the action of the last/newest entry in the flow_path.

        :param flow_path:       flow path to get the flow action from (default=self.flow_path).
        :param path_index:      index in the flow_path.
        :return:                flow action string or empty string if index does not exist.
        """
        if flow_path is None:
            flow_path = self.flow_path
        if len(flow_path) >= (abs(path_index) if path_index < 0 else path_index + 1):
            return flow_action(flow_path[path_index])
        return ''

    def flow_path_strip(self, flow_path: List[str]) -> List[str]:
        """ return flow_path copy with all non-enter actions stripped from the end.

        :param flow_path:       flow path list to strip.
        :return:                stripped flow path copy.
        """
        deep = len(flow_path)
        while deep and self.flow_path_action(flow_path=flow_path, path_index=deep - 1) != 'enter':
            deep -= 1
        return flow_path[:deep]

    def on_flow_change(self, flow_id: str, event_kwargs: Dict[str, Any]) -> bool:
        """ checking if exists a Popup class for the new flow and if yes then open it.

        :param flow_id:         new flow id.
        :param event_kwargs:    optional event kwargs; the optional item with the key `popup_kwargs`
                                will be passed onto the `__init__` method of the found Popup class.
        :return:                True if Popup class was found and displayed.

        This method is mainly used as the last fallback clicked flow change confirmation event handler of a FlowButton.
        """
        class_name = flow_popup_class_name(flow_id)
        self.vpo(f"MainAppBase.on_flow_change '{flow_id}' {event_kwargs} lookup={class_name}")

        if flow_id:
            popup_class = self.class_by_name(class_name)
            if popup_class:
                popup_kwargs = event_kwargs.get('popup_kwargs', dict())
                self.show_popup(popup_class, **popup_kwargs)
                return True
        return False

    @staticmethod
    def on_flow_popup_close(_flow_key: str, _popup_args: Dict[str, Any]) -> bool:
        """ default popup close handler of FlowPopup widget, ensuring update of :attr:`flow_path`.

        :param _flow_key:       unused flow key.
        :param _popup_args:     unused popup args.
        :return:                always returning True.
        """
        return True

    # other helper methods and default event handlers

    def find_image(self, image_name: str, height: float = 32.0, light_theme: bool = True) -> Optional[RegisteredFile]:
        """ find best fitting image in img app folder (see also :meth:`~MainAppBase.img_file` for easier usage).

        :param image_name:      name of the image (file name without extension).
        :param height:          preferred height of the image/icon.
        :param light_theme:     preferred theme (dark/light) of the image.
        :return:                image file object (RegisteredFile/CachedFile) if found else None.
        """
        def property_matcher(file) -> bool:
            """ find images with matching theme.

            :param file:        RegisteredFile instance.
            :return:            True if theme is matching.
            """
            return bool(file.properties.get('light', 0)) == light_theme

        def file_sorter(file) -> float:
            """ sort images files by height delta.

            :param file:        RegisteredFile instance.
            :return:            height delta.
            """
            return abs(file.properties.get('height', -MAX_FONT_SIZE) - height)

        if self.image_files:
            return self.image_files(image_name, property_matcher=property_matcher, file_sorter=file_sorter)
        return None

    def find_sound(self, sound_name: str) -> Optional[RegisteredFile]:
        """ find sound by name.

        :param sound_name:      name of the sound to search for.
        :return:                cached sound file object (RegisteredFile/CachedFile) if sound name was found else None.
        """
        if self.sound_files:    # prevent error on app startup (setup_app_states() called before load_images()
            return self.sound_files(sound_name)
        return None

    def img_file(self, image_name: str, font_size: Optional[float] = None, light_theme: Optional[bool] = None) -> str:
        """ shortcutting :meth:`~MainAppBase.find_image` method w/o bound property for to get image file path.

        :param image_name:      image name (file name stem).
        :param font_size:       optional font size in pixels.
        :param light_theme:     optional theme (True=light, False=dark).
        :return:                file path of image file or empty string if image file not found.
        """
        if font_size is None:
            font_size = self.font_size
        if light_theme is None:
            light_theme = self.light_theme

        img_obj = self.find_image(image_name, height=font_size, light_theme=light_theme)
        if img_obj:
            return img_obj.path
        return ''

    def key_press_from_framework(self, modifiers: str, key: str) -> bool:
        """ dispatch key press event, coming normalized from the UI framework.

        :param modifiers:       modifier keys.
        :param key:             key character.
        :return:                True if key got consumed/used else False.
        """
        self.vpo(f"MainAppBase.key_press_from_framework({modifiers}+{key})")
        event_name = f'on_key_press_of_{modifiers}_{key}'
        en_lower = event_name.lower()
        if self.call_method(en_lower):
            return True
        if event_name != en_lower and self.call_method(event_name):
            return True
        # call default handler; pass lower key code (enaml/Qt sends upper-case key code if Shift modifier is pressed)
        return self.call_method('on_key_press', modifiers, key.lower()) or False

    def load_images(self):
        """ load images from app folder img. """
        self.image_files = FilesRegister('img/**')

    def load_sounds(self):
        """ load audio sounds from app folder snd. """
        self.sound_files = FilesRegister('snd/**')

    def play_beep(self):
        """ make a short beep sound, should be overwritten by GUI framework. """
        self.po(chr(7), "MainAppBase.BEEP")

    def play_sound(self, sound_name: str):
        """ play audio/sound file, should be overwritten by GUI framework.

        :param sound_name:  name of the sound to play.
        """
        self.po(f"MainAppBase.play_sound {sound_name}")

    def play_vibrate(self, pattern: Tuple = (0.0, 0.3)):
        """ play vibrate pattern, should be overwritten by GUI framework.

        :param pattern:     tuple of pause and vibrate time sequence.
        """
        self.po(f"MainAppBase.play_vibrate {pattern}")

    def run_app(self):
        """ startup main and framework applications. """
        self.dpo("MainAppBase.run_app")

        self.call_method('on_app_start')

        super().run_app()                               # parse command line arguments into config options

        self.call_method('on_app_run')

        if self._start_event_loop:                      # not needed for SubApp or additional Window instances
            try:
                self._start_event_loop()
            finally:
                self.call_method('on_app_quit')
                self.shutdown(self._exit_code or None)  # don't call sys.exit() for zero exit code

    def show_popup(self, popup_class: Type, **popup_kwargs) -> Any:
        """ open Popup or DropDown by calling `show` method of passed instance.

        Overwrite this method if framework is using different method to open popup window or if
        a widget in the Popup/DropDown need to get the input focus.

        :param popup_class:     class of the Popup/DropDown widget/window.
        :param popup_kwargs:    args for to instantiate and show/open the popup.
        :return:                created and displayed/opened popup class instance.
        """
        self.dpo(f"MainAppBase.show_popup {popup_class} {popup_kwargs}")
        popup_instance = popup_class(**popup_kwargs)
        popup_instance.show()
        return popup_instance

    def stop_app(self, exit_code: int = 0):
        """ quit this application.

        :param exit_code:   optional exit code.
        """
        self.dpo(f"MainAppBase.stop_app {exit_code}")
        self._exit_code = exit_code

        self.call_method('on_app_stop')

        if self.framework_win:
            self.framework_win.close()      # close window to save app state data

        self.call_method('on_app_exit')

        if self._stop_event_loop:
            self._stop_event_loop()         # will exit the self._start_event_loop() method called by self.run_app()

    def widget_by_attribute(self, att_name: str, att_value: str) -> Optional[Any]:
        """ determine the widget referenced by the passed attribute name and value.

        :param att_name:        name of the attribute of the searched widget.
        :param att_value:       attribute value of the searched widget.
        :return:                widget that has the specified attribute with the specified value.
        """
        def child_wid(children):
            """ bottom up search within children for a widget with matching attribute name and value. """
            for widget in children:
                found = child_wid(widget.children)
                if found:
                    return found
                if getattr(widget, att_name, None) == att_value:
                    return widget
            return None

        return child_wid(self.framework_win.children)

    def widget_by_flow_id(self, flow_id: str) -> Optional[Any]:
        """ determine the widget having the passed flow_id.

        :param flow_id:         flow id value of the searched widget's `tap_flow_id` attribute.
        :return:                widget that has a `tap_flow_id` attribute with the value of the passed flow id.
        """
        return self.widget_by_attribute('tap_flow_id', flow_id)

    def widget_by_state_name(self, state_name: str) -> Optional[Any]:
        """ determine the widget having the passed app state name (app_state_name).

        :param state_name:      app state name of the widget's `app_state_name` attribute.
        :return:                widget that has a `app_state_name` attribute with the passed app state name.
        """
        return self.widget_by_attribute('app_state_name', state_name)

    def win_pos_size_change(self, *win_pos_size):
        """ screen resize handler (called on window resize or when app will exit/stop via closed event.

        :param win_pos_size:    window geometry/coordinates: x, y, width, height.
        """
        self.framework_app.landscape = win_pos_size[2] >= win_pos_size[3]
        self.vpo(f"MainAppBase.win_pos_size_change landscape={self.framework_app.landscape}, {win_pos_size}")
        self.change_app_state('win_rectangle', win_pos_size)
        self.call_method('on_win_pos_size')


module_globals = globals()
#: used. e.g. by :mod:`ae.gui_help` for execution/evaluation of dynamic code, expressions and f-strings
