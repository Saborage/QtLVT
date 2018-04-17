import sys
from PyQt5.QtWidgets import *

from app.views.core.low_voltage_window import LowVoltageWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = LowVoltageWindow()

    sys.exit(app.exec_())