import time
from pyqtgraph import PlotWidget, mkPen, mkBrush
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from lib.capture import Capture


class GraphWidget(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.graph = PlotWidget()
		self.graph.setAntialiasing(True)
		self.graph.showGrid(x=True, y=True)
		self.graph.setLabel('bottom', 'Milliseconds')
		self.graph.mouseTrail = True

		self.pen = mkPen(color=(0, 255, 0))
		self.brush = mkBrush(color=(0, 255, 0, 100))

		layout.addWidget(self.graph)

	def handle_capture(self, capture: Capture):
		self.has_capture = True
		self.graph.clear()
		self.graph.plot(
			capture.get_x_values(),
			capture.get_y_values(),
			pen=self.pen,
			fillLevel=0,
			fillBrush=self.brush
		)
