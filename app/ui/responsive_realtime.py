"""Responsive and lightweight realtime presentation helpers.

Presentation-only layer: it never changes transaction, database, auth, or
printer behavior. It adapts shell geometry to the current window width and
refreshes dashboard presentation when local data changes.
"""

from PySide6.QtCore import QObject, QTimer, QEvent
from PySide6.QtWidgets import QFrame, QSplitter, QSizePolicy


class _ResponsiveRealtimeController(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self._refresh)
        self.timer.start()
        window.installEventFilter(self)
        self.apply_layout()

    def eventFilter(self, watched, event):
        if watched is self.window and event.type() == QEvent.Resize:
            self.apply_layout()
        return False

    def _refresh(self):
        refresh = getattr(self.window, "refresh_dashboard_data", None)
        if callable(refresh):
            try:
                refresh()
            except Exception:
                # Presentation refresh must never interrupt the POS session.
                pass

    def apply_layout(self):
        width = max(800, self.window.width())
        sidebar = self.window.findChild(QFrame, "modernSidebar")
        if sidebar is not None:
            sidebar_width = 190 if width < 1100 else 210 if width < 1400 else 230
            sidebar.setFixedWidth(sidebar_width)

        pay = self.window.findChild(QFrame, "premiumPayCard")
        if pay is not None:
            if width < 1000:
                pay.setMinimumWidth(250)
                pay.setMaximumWidth(285)
            elif width < 1250:
                pay.setMinimumWidth(275)
                pay.setMaximumWidth(310)
            else:
                pay.setMinimumWidth(290)
                pay.setMaximumWidth(330)

        # Let the main content breathe on smaller screens instead of forcing
        # fixed widths. Scroll areas remain the fallback for dense legacy pages.
        stack = getattr(self.window, "modern_stack", None)
        if stack is not None:
            for index in range(stack.count()):
                page = stack.widget(index)
                if page is None:
                    continue
                page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout = page.layout()
                if layout is not None:
                    margin = 10 if width < 1100 else 16
                    layout.setContentsMargins(margin, 6, margin, 10)


def apply_responsive_realtime(window):
    """Install one presentation controller per main window."""
    if getattr(window, "_wpos_responsive_realtime", None) is not None:
        return
    window._wpos_responsive_realtime = _ResponsiveRealtimeController(window)
