import sys
from PyQt6.QtWidgets import QApplication
from lib.main_window import MainWindow

if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
