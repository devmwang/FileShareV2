QML_IMPORT_NAME = "FileShareV2"
QML_IMPORT_MAJOR_VERSION = 1

import os
import sys

from time import strftime, localtime, sleep
from pathlib import Path

from PySide6.QtCore import Signal, Slot, QObject, QThread
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, QmlElement


## Backend Object Class
class Backend(QObject):
    ## Initialize Qt Signals
    currentDate = Signal(str, arguments=['currentDate'])
    currentTime = Signal(str, arguments=['currentTime'])
    currentMonthYear = Signal(str, arguments=['currentMonthYear'])

    ## Class Init Method
    def __init__(self):
        super().__init__()

        ## Initialize background workers and threads
        # Initialize clock update worker and thread
        self.clockThread = QThread()
        self.clockWorker = ClockWorker()
        self.clockWorker.moveToThread(self.clockThread)

        self.clockWorker.runBackendUpdateClockMethod.connect(self.updateClock)

        self.clockWorker.finished.connect(self.clockThread.quit)
        self.clockThread.started.connect(self.clockWorker.long_running)

        self.clockThread.start()

        #### Move this out of init to other method, shouldn't run on start, should run when needed
        # Initialize server worker and thread
        # self.serverThread = QThread()
        # self.serverWorker = ServerWorker()
        # self.serverWorker.moveToThread(self.serverThread)

        # self.serverWorker.runBackendUpdateClockMethod.connect(self.updateClock)

        # self.serverWorker.finished.connect(self.serverThread.quit)
        # self.serverThread.started.connect(self.serverWorker.long_running)

        # self.serverThread.start()

    ## Backend Helper Methods
    # Clock Update Helper
    @Slot(list)
    def updateClock(self, clockVars):
        # Receive datetime data and push to UI
        self.currentDate.emit(clockVars[0])
        self.currentTime.emit(clockVars[1])
        self.currentMonthYear.emit(clockVars[2])


## Application Background Worker Classes
# Clock Worker
class ClockWorker(QThread):
    runBackendUpdateClockMethod = Signal(list)

    def long_running(self):
        while (True):
            _currentDate = strftime('%A, %d', localtime()) # Verify if removing leading zero is necessary, sample: strftime('%a, %d', localtime()).replace(' 0', ' ')
            _currentTime = strftime('%I:%M %S %p', localtime()) # Use %S to test if updating every second
            _currentMonthYear = strftime('%B, %Y', localtime())

            self.runBackendUpdateClockMethod.emit([_currentDate, _currentTime, _currentMonthYear])
            sleep(0.1) # Increase delay if resources begin to run out

# Server Worker
class ServerWorker(QThread):
    status = Signal()

    # def long_running(self):
       # do something 


## QML Frontend Bridge
@QmlElement
class Bridge(QObject):
    # Send File
    @Slot(list)
    def sendFile(list):
        return # Add send logic

    # Receive File
    def receiveFile(list):
        return # Add receive logic


## Application Initialization
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
