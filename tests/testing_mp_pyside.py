import sys
import multiprocessing
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Signal, QObject, Qt
from time import sleep

class ChildProcess(QObject):
    finished = Signal(str)

    def run(self):
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Multiprocessing with PySide6")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.start_button = QPushButton("Start Child Process", self)
        self.start_button.clicked.connect(self.start_child_process)
        self.layout.addWidget(self.start_button)

        self.child_process = None

    def start_child_process(self):
        if not self.child_process or not self.child_process.is_alive():
            self.child_process = multiprocessing.Process(target=self.run_child_process)
            self.child_process.start()
            self.start_button.setEnabled(False)

    def run_child_process(self):
        child = ChildProcess()
        child.finished.connect(self.handle_child_signal)
