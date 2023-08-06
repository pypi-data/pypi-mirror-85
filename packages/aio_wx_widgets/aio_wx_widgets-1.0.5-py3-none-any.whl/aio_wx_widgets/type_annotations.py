"""All type annotations go here."""


from typing import TYPE_CHECKING, Any, TypeVar, Union

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    import wx

    from aio_wx_widgets.controller import BaseController
    from aio_wx_widgets.core.base_widget import BaseWidget
    from aio_wx_widgets.core.binding import Binding
    from aio_wx_widgets.core.sizers import SizerMixin

    try:
        import Protocol  # type: ignore
    except ImportError:
        from typing_extensions import Protocol

    assert BaseController
    assert AbstractEventLoop
    assert Binding
    assert wx
    assert BaseWidget

    class Choice(Protocol):
        """Typing protocol to be used for static type checking."""

        label: str
        value: Any

    T = TypeVar("T")  # pylint: disable=invalid-name

    Widget = Union[BaseWidget, wx.Window, wx.BoxSizer, SizerMixin]
