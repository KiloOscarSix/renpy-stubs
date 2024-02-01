from typing import Optional
from renpy.common.library import DictEquality
from renpy.display.transition import Transition
from renpy.ui import Action
import renpy.exports as renpy

class NullAction(Action, DictEquality):
    """
    :doc: control_action

    Does nothing.

    This can be used to make a button responsive to hover/unhover events,
    without actually doing anything.
    """

    def __call__(self):
        return

@renpy.pure
class Return(Action, DictEquality):
    """
    :doc: control_action

    Causes the current interaction to return the supplied non-None value.
    This is often used with menus and imagemaps, to
    select what the return value of the interaction is. If the screen
    was called using the ``call screen`` statement, the return value
    is placed in the `_return` variable.

    When in a menu, this returns from the menu. (The value should be
    None in this case.)
    """

    def __init__(self, value=None):
        self.value = value
    def __call__(self):
        if self.value is None:
            if main_menu:
                ShowMenu("main_menu")()
            else:
                return True

        else:
            return self.value

@renpy.pure
class Jump(Action, DictEquality):
    """
    :doc: control_action

    Causes control to transfer to `label`, given as a string.
    """

    def __init__(self, label):
        self.label = label
    def __call__(self):
        renpy.jump(self.label)

@renpy.pure
class Call(Action, DictEquality):
    """
    :doc: control_action

    Ends the current statement, and calls `label`, given as a string.
    Arguments and keyword arguments are passed to :func:`renpy.call`.
    """

    args = tuple()
    kwargs = dict()

    def __init__(self, label, *args, **kwargs):
        self.label = label
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        renpy.call(self.label, *self.args, **self.kwargs)

@renpy.pure
class Show(Action, DictEquality):
    """
    :doc: control_action
    :args: (screen, transition=None, *args, **kwargs)

    This causes another screen to be shown. `screen` is a string
    giving the name of the screen. The arguments are
    passed to the screen being shown.

    If not None, `transition` is used to show the new screen.

    This action takes the `_layer`, `_zorder` and `_tag` keyword
    arguments, which have the same meaning as in the
    :func:`renpy.show_screen` function.
    """

    args = None

    def __init__(self, screen, transition=None, *args, **kwargs):
        self.screen = screen
        self.transition = transition
        self.args = args
        self.kwargs = kwargs
    def predict(self):
        renpy.predict_screen(self.screen, *self.args, **self.kwargs)
    def __call__(self):
        renpy.show_screen(self.screen, *self.args, **self.kwargs)

        if self.transition is not None:
            renpy.transition(self.transition)

        renpy.restart_interaction()
    def get_selected(self):
        return (
            renpy.get_screen(self.screen, self.kwargs.get("_layer", None)) is not None
        )

@renpy.pure
class ToggleScreen(Action, DictEquality):
    """
    :doc: control_action

    This toggles the visibility of `screen`. If it is not currently
    shown, the screen is shown with the provided arguments. Otherwise,
    the screen is hidden.

    If not None, `transition` is use to show and hide the screen.

    This action takes the `_layer`, `_zorder` and `_tag` keyword
    arguments, which have the same meaning as in the
    :func:`renpy.show_screen` function.
    """

    args = None

    def __init__(self, screen, transition=None, *args, **kwargs):
        self.screen = screen
        self.transition = transition
        self.args = args
        self.kwargs = kwargs
    def predict(self):
        renpy.predict_screen(self.screen, *self.args, **self.kwargs)
    def __call__(self):
        if renpy.get_screen(self.screen, layer=self.kwargs.get("_layer", None)):
            renpy.hide_screen(self.screen, layer=self.kwargs.get("_layer", None))
        else:
            renpy.show_screen(self.screen, *self.args, **self.kwargs)

        if self.transition is not None:
            renpy.transition(self.transition)

        renpy.restart_interaction()
    def get_selected(self):
        return (
            renpy.get_screen(self.screen, self.kwargs.get("_layer", None)) is not None
        )

@renpy.pure
def ShowTransient(screen, transition=None, *args, **kwargs):
    """
    :doc: control_action

    Shows a transient screen. A transient screen will be hidden when
    the current interaction completes. The arguments are
    passed to the screen being shown.

    If not None, `transition` is use to show the new screen.

    This action takes the `_layer`, `_zorder` and `_tag` keyword
    arguments, which have the same meaning as in the
    :func:`renpy.show_screen` function.
    """

    return Show(screen, transition, *args, _transient=True, **kwargs)

class Hide(Action, DictEquality):
    _layer: Optional[str] = None

    def __init__(
        self,
        screen: Optional[str] = None,
        transition: Optional[Transition] = None,
        _layer: Optional[str] = None,
    ) -> None: ...
    def __call__(self) -> None: ...
