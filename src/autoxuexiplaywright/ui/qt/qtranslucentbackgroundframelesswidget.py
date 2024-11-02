"""Simple sizable and draggable frameless QWidget taken from https://github.com/pedrolcl/frameless-qt-poc."""

from typing import final as _final
from typing import overload as _overload
from typing import override as _override
from PySide6.QtGui import QHoverEvent as _QHoverEvent
from PySide6.QtGui import QMouseEvent as _QMouseEvent
from PySide6.QtCore import Qt as _Qt
from PySide6.QtCore import QEvent as _QEvent
from PySide6.QtWidgets import QStyle as _QStyle
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QVBoxLayout as _QVBoxLayout
from PySide6.QtWidgets import QGraphicsDropShadowEffect as _QShadowEffect


class _CombinedEdge:
    LeftTopEdge = _Qt.Edge.LeftEdge | _Qt.Edge.TopEdge
    RightBottomEdge = _Qt.Edge.RightEdge | _Qt.Edge.BottomEdge
    LeftBottomEdge = _Qt.Edge.LeftEdge | _Qt.Edge.BottomEdge
    RightTopEdge = _Qt.Edge.RightEdge | _Qt.Edge.TopEdge


class QTranslicentBackgroundFramelessWidget[T: _QWidget](_QWidget):
    """Draggable, resizable, frameless and translucent-backgrounded widget."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent, _Qt.WindowType.FramelessWindowHint)
        self.setAttribute(_Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(_Qt.WidgetAttribute.WA_Hover)
        self.setLayout(_QVBoxLayout(self))
        self.__contentWidget: T | None = None
        self.__edge = _Qt.Edge(0)
        self.__pseudoCaptionWidget: _QWidget | None = None

        style = self.style()
        PM = _QStyle.PixelMetric
        topMarign = style.pixelMetric(PM.PM_LayoutTopMargin)
        bottomMarign = style.pixelMetric(PM.PM_LayoutBottomMargin)
        leftMarign = style.pixelMetric(PM.PM_LayoutLeftMargin)
        rightMarign = style.pixelMetric(PM.PM_LayoutRightMargin)
        self.layout().setContentsMargins(
            leftMarign,
            topMarign,
            rightMarign,
            bottomMarign,
        )

        shadow = _QShadowEffect(self)
        shadow.setOffset(0)
        shadow.setBlurRadius(25)
        self.setGraphicsEffect(shadow)

    @_final
    @_overload
    def contentWidget(self) -> T | None:
        pass

    @_final
    @_overload
    def contentWidget(self, assertNotNone: bool = True) -> T:
        pass

    @_final
    def contentWidget(self, assertNotNone: bool = False) -> T | None:
        """The content widget."""
        if assertNotNone and self.__contentWidget is None:
            raise TypeError("self.__contentWidget is None.")
        return self.__contentWidget

    @_final
    def setContentWidget(self, widget: T):
        """Set the content widget."""
        if self.__contentWidget is not None:
            self.layout().removeWidget(self.__contentWidget)
        self.__contentWidget = widget
        self.layout().addWidget(self.__contentWidget)

    @_final
    def pseudoCaptionWidget(self) -> _QWidget | None:
        """The widget used for checking if allowed to drag the widget."""
        return self.__pseudoCaptionWidget

    @_final
    def setPseudoCaptionWidget(self, widget: _QWidget | None):
        """Set the widget used for checking if allowed to drag the widget."""
        self.__pseudoCaptionWidget = widget

    @_final
    @_override
    def event(self, event: _QEvent) -> bool:
        if _Qt.WindowType.FramelessWindowHint in self.windowFlags():
            match event.type():
                case _QEvent.Type.MouseButtonPress if (
                    isinstance(event, _QMouseEvent)
                    and event.button() == _Qt.MouseButton.LeftButton
                ):
                    self.__updateCursor()
                    if (
                        self.__pseudoCaptionWidget is not None
                        and self.__pseudoCaptionWidget.underMouse()
                    ):
                        _ = self.windowHandle().startSystemMove()
                    elif self.__edge:
                        _ = self.windowHandle().startSystemResize(self.__edge)
                case _QEvent.Type.MouseButtonRelease if (
                    isinstance(event, _QMouseEvent)
                    and event.button() == _Qt.MouseButton.LeftButton
                ):
                    self.__edge = _Qt.Edge(0)
                    self.__updateCursor()
                    self.setFocus()
                case _QEvent.Type.HoverEnter | _QEvent.Type.HoverLeave:
                    self.__edge = _Qt.Edge(0)
                case _QEvent.Type.HoverMove if isinstance(event, _QHoverEvent):
                    position = event.position().toPoint()
                    style = self.style()
                    PM = _QStyle.PixelMetric
                    topMarign = style.pixelMetric(PM.PM_LayoutTopMargin)
                    bottomMarign = style.pixelMetric(PM.PM_LayoutBottomMargin)
                    leftMarign = style.pixelMetric(PM.PM_LayoutLeftMargin)
                    rightMarign = style.pixelMetric(PM.PM_LayoutRightMargin)
                    x = position.x()
                    y = position.y()
                    xMin = leftMarign
                    xMax = self.width() - rightMarign
                    yMin = bottomMarign
                    yMax = self.height() - topMarign

                    if x < xMin:
                        self.__edge |= _Qt.Edge.LeftEdge
                    elif x > xMax:
                        self.__edge |= _Qt.Edge.RightEdge
                    else:
                        self.__edge &= ~_Qt.Edge.LeftEdge
                        self.__edge &= ~_Qt.Edge.RightEdge

                    if y < yMin:
                        self.__edge |= _Qt.Edge.TopEdge
                    elif y > yMax:
                        self.__edge |= _Qt.Edge.BottomEdge
                    else:
                        self.__edge &= ~_Qt.Edge.TopEdge
                        self.__edge &= ~_Qt.Edge.BottomEdge

                    self.__updateCursor()
                case _:
                    pass
        return super().event(event)

    @_final
    def __updateCursor(self):
        if self.__edge:
            match self.__edge:
                case _Qt.Edge.LeftEdge | _Qt.Edge.RightEdge:
                    self.setCursor(_Qt.CursorShape.SizeHorCursor)
                case _Qt.Edge.TopEdge | _Qt.Edge.BottomEdge:
                    self.setCursor(_Qt.CursorShape.SizeVerCursor)
                case _CombinedEdge.LeftTopEdge | _CombinedEdge.RightBottomEdge:
                    self.setCursor(_Qt.CursorShape.SizeFDiagCursor)
                case _CombinedEdge.LeftBottomEdge | _CombinedEdge.RightTopEdge:
                    self.setCursor(_Qt.CursorShape.SizeBDiagCursor)
                case _:
                    pass
        else:
            self.setCursor(_Qt.CursorShape.ArrowCursor)
