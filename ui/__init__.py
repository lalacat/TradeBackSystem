import ctypes
import platform
import sys
import traceback

from PyQt5 import QtGui, QtWidgets


# from .mainwindow import MainWindow



def excepthook(exctype, value, tb):
    """
    Raise exception under debug mode, otherwise 
    show exception detail with QMessageBox.
    """
    sys.__excepthook__(exctype, value, tb)

    msg = "".join(traceback.format_exception(exctype, value, tb))
    QtWidgets.QMessageBox.critical(
        None, "Exception", msg, QtWidgets.QMessageBox.Ok
    )


def create_qapp(settings,app_name: str = "VN Trader"):
    """
    Create Qt Application.
    """
    sys.excepthook = excepthook

    qapp = QtWidgets.QApplication([])
    # qapp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    font = QtGui.QFont(settings["FONT_FAMILY"], settings["FONT_SIZE"])
    qapp.setFont(font)

    # icon = QtGui.QIcon(get_icon_path(__file__, "vnpy.ico"))
    # qapp.setWindowIcon(icon)

    if "Windows" in platform.uname():
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            app_name
        )

    return qapp
