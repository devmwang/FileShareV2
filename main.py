import os
import sys

from time import strftime, localtime, sleep
from pathlib import Path

from PySide6.QtCore import QObject, QUrl, Signal, Slot, QThread
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine


# Backend Object Class
class Backend(QObject):
    # Initialize Qt Signals
    currentDate = Signal(str, arguments=['currentDate'])
    currentTime = Signal(str, arguments=['currentTime'])
    currentMonthYear = Signal(str, arguments=['currentMonthYear'])

    # Class Init Method
    def __init__(self):
        super().__init__()

        # Initialize background workers and threads
        # Clock update worker and thread
        self.clockThread = QThread()
        self.clockWorker = ClockWorker()
        self.clockWorker.moveToThread(self.clockThread)
        self.clockWorker.finished.connect(self.clockThread.quit)
        self.clockWorker.runBackendUpdateClockMethod.connect(self.updateClock)
        self.clockThread.started.connect(self.clockWorker.long_running)
        self.clockThread.start()

    # Backend Helper Methods
    @Slot(list)
    def updateClock(self, msg):
        self.currentDate.emit(msg[0])
        self.currentTime.emit(msg[1])
        self.currentMonthYear.emit(msg[2])


# Application Background Worker Classes
class ClockWorker(QThread):
    runBackendUpdateClockMethod = Signal(list)

    def long_running(self):
        while (True):
            _currentDate = strftime('%A, %d', localtime()) # Verify if removing leading zero is necessary, code sample: strftime('%a, %d', localtime()).replace(' 0', ' ')
            _currentTime = strftime('%I:%M %S %p', localtime())
            _currentMonthYear = strftime('%B, %Y', localtime())

            self.runBackendUpdateClockMethod.emit([_currentDate, _currentTime, _currentMonthYear])
            sleep(0.1) # Increase delay if resources begin to run out


# Application Initialization
if __name__ == '__main__':
    # Initialize and configure application application
    app = QGuiApplication(sys.argv)

    app.setApplicationDisplayName('File Share')
    app.setWindowIcon(QIcon('FileShareIcon.ico'))

    app.setQuitOnLastWindowClosed(True)

    # Initialize and configure application engine
    engine = QQmlApplicationEngine()

    main_qml_file = Path(__file__).parent / 'main.qml'
    engine.load(main_qml_file)

    # Initialize backend
    backend = Backend()
    engine.rootObjects()[0].setProperty('backend', backend)

    # Check rootObjects
    if not engine.rootObjects():
        sys.exit(-1)

    # Execute app and cleanup
    sys.exit(app.exec())
