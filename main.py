import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QMessageBox, QMainWindow, QTextEdit, QMenuBar,
    QMenu, QCheckBox
)
from PyQt6.QtGui import QPixmap


class ShapeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shape Calculator")
        self.history = []

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.make_menu()
        self.show_start()

    def make_menu(self):
        bar = QMenuBar(self)
        menu = QMenu("Menu", self)
        view = menu.addAction("View History")
        view.triggered.connect(self.show_history)
        bar.addMenu(menu)
        self.setMenuBar(bar)

    def clear(self):
        while self.layout.count():
            thing = self.layout.takeAt(0)
            if thing.widget():
                thing.widget().deleteLater()

    def show_start(self):
        self.clear()

        self.pick_label = QLabel("Pick a shape:")
        self.shape_box = QComboBox()
        self.shape_box.addItems(["Circle", "Square", "Triangle"])
        self.shape_box.currentTextChanged.connect(self.load_image)

        self.shape_pic = QLabel()
        self.load_image("Circle")

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.ask_3d)

        self.layout.addWidget(self.pick_label)
        self.layout.addWidget(self.shape_box)
        self.layout.addWidget(self.shape_pic)
        self.layout.addWidget(self.next_btn)

    def load_image(self, name):
        pic = QPixmap(f"{name.lower()}.png")
        if not pic.isNull():
            self.shape_pic.setPixmap(pic.scaledToHeight(100))
        else:
            self.shape_pic.setText("No image")

    def ask_3d(self):
        self.shape = self.shape_box.currentText().lower()
        self.clear()

        self.ask_label = QLabel("Is it 3D?")
        self.option_box = QComboBox()
        self.option_box.addItems(["No", "Yes"])
        self.continue_btn = QPushButton("Next")
        self.continue_btn.clicked.connect(self.ask_goal)

        self.layout.addWidget(self.ask_label)
        self.layout.addWidget(self.option_box)
        self.layout.addWidget(self.continue_btn)

    def ask_goal(self):
        if self.option_box.currentText() == "Yes":
            if self.shape == "circle":
                self.shape = "sphere"
            elif self.shape == "square":
                self.shape = "cube"
            elif self.shape == "triangle":
                self.shape = "pyramid"

        self.clear()

        self.goal_label = QLabel("What do you want to solve?")
        self.area_check = QCheckBox("Area")
        self.surface_check = QCheckBox("Surface Area")
        self.volume_check = QCheckBox("Volume")
        self.go_btn = QPushButton("Continue")
        self.go_btn.clicked.connect(self.show_inputs)

        self.layout.addWidget(self.goal_label)

        if self.shape in ["circle", "square", "triangle"]:
            self.layout.addWidget(self.area_check)
        elif self.shape in ["sphere", "cube", "pyramid"]:
            self.layout.addWidget(self.surface_check)
            self.layout.addWidget(self.volume_check)

        self.layout.addWidget(self.go_btn)

    def show_inputs(self):
        self.goals = {
            "Area": self.area_check.isChecked(),
            "Surface Area": self.surface_check.isChecked(),
            "Volume": self.volume_check.isChecked()
        }

        self.clear()

        self.shape_pic = QLabel()
        self.load_image(self.shape.capitalize())
        self.layout.addWidget(self.shape_pic)

        self.inputs = []
        self.labels = []

        if self.shape in ["circle", "sphere"]:
            fields = ["Radius"]
        elif self.shape in ["square", "cube"]:
            fields = ["Side Length"]
        elif self.shape == "triangle":
            fields = ["Base", "Height"]
        elif self.shape == "pyramid":
            if self.goals["Volume"] and self.goals["Surface Area"]:
                fields = ["Base Length", "Height", "Slant Height"]
            elif self.goals["Volume"]:
                fields = ["Base Length", "Height"]
            elif self.goals["Surface Area"]:
                fields = ["Base Length", "Slant Height"]
            else:
                fields = []
        else:
            fields = []

        self.input_vals = {}
        for f in fields:
            label = QLabel(f"{f}:")
            box = QLineEdit()
            self.layout.addWidget(label)
            self.layout.addWidget(box)
            self.inputs.append(box)
            self.labels.append(f)

        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.clicked.connect(self.do_math)
        self.layout.addWidget(self.calc_btn)

        self.back_btn = QPushButton("Back to Start")
        self.back_btn.clicked.connect(self.show_start)
        self.layout.addWidget(self.back_btn)

    def do_math(self):
        try:
            values = [float(x.text()) for x in self.inputs]
            for i in range(len(self.labels)):
                self.input_vals[self.labels[i]] = values[i]
        except:
            QMessageBox.warning(self, "Oops", "Put in numbers only")
            return

        results = []

        if self.shape == "circle" and self.goals["Area"]:
            r = self.input_vals["Radius"]
            results.append(f"Circle Area: {3.1416 * r ** 2:.2f}")

        elif self.shape == "square" and self.goals["Area"]:
            s = self.input_vals["Side Length"]
            results.append(f"Square Area: {s ** 2:.2f}")

        elif self.shape == "triangle" and self.goals["Area"]:
            b = self.input_vals["Base"]
            h = self.input_vals["Height"]
            results.append(f"Triangle Area: {0.5 * b * h:.2f}")

        elif self.shape == "sphere":
            r = self.input_vals["Radius"]
            if self.goals["Surface Area"]:
                results.append(f"Sphere Surface: {4 * 3.1416 * r ** 2:.2f}")
            if self.goals["Volume"]:
                results.append(f"Sphere Volume: {(4/3) * 3.1416 * r ** 3:.2f}")

        elif self.shape == "cube":
            s = self.input_vals["Side Length"]
            if self.goals["Surface Area"]:
                results.append(f"Cube Surface: {6 * s ** 2:.2f}")
            if self.goals["Volume"]:
                results.append(f"Cube Volume: {s ** 3:.2f}")

        elif self.shape == "pyramid":
            b = self.input_vals["Base Length"]
            if self.goals["Volume"]:
                h = self.input_vals["Height"]
                results.append(f"Pyramid Volume: {(1/3) * b**2 * h:.2f}")
            if self.goals["Surface Area"]:
                sl = self.input_vals["Slant Height"]
                results.append(f"Pyramid Surface: {b**2 + 2 * b * sl:.2f}")

        final = "\n".join(results)
        self.history.append(f"{self.shape.capitalize()} →\n{final}")
        QMessageBox.information(self, "Answer", final)

    def show_history(self):
        self.clear()

        label = QLabel("History:")
        box = QTextEdit()
        box.setReadOnly(True)
        box.setText("\n\n".join(self.history) if self.history else "No history yet.")

        self.layout.addWidget(label)
        self.layout.addWidget(box)

        back = QPushButton("Back to Start")
        back.clicked.connect(self.show_start)
        self.layout.addWidget(back)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ShapeApp()
    win.show()
    sys.exit(app.exec())