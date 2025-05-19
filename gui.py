from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QCheckBox, QMessageBox, QTextEdit, QMenu, QMenuBar
)
from PyQt6.QtGui import QPixmap
from logic import get_fields, calc, save, load


class ShapeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shape Calculator")
        self.resize(350, 500)
        self.history = load()

        self.page = QWidget()
        self.layout = QVBoxLayout()
        self.page.setLayout(self.layout)
        self.setCentralWidget(self.page)

        self.make_menu()
        self.start_screen()

    def make_menu(self):
        bar = QMenuBar(self)
        menu = QMenu("Menu", self)
        action = menu.addAction("History")
        action.triggered.connect(self.show_history)
        bar.addMenu(menu)
        self.setMenuBar(bar)

    def clear(self):
        while self.layout.count():
            stuff = self.layout.takeAt(0)
            if stuff.widget():
                stuff.widget().deleteLater()

    def start_screen(self):
        self.clear()

        lbl = QLabel("Pick shape:")
        self.shape_box = QComboBox()
        self.shape_box.addItems(["Circle", "Square", "Triangle"])
        self.shape_box.currentTextChanged.connect(self.show_pic)

        self.pic = QLabel()
        self.show_pic("Circle")

        btn = QPushButton("Next")
        btn.clicked.connect(self.ask_3d)

        self.layout.addWidget(lbl)
        self.layout.addWidget(self.shape_box)
        self.layout.addWidget(self.pic)
        self.layout.addWidget(btn)

    def show_pic(self, name):
        img = QPixmap(f"{name.lower()}.png")
        if img.isNull():
            self.pic.setText("No image")
        else:
            self.pic.setPixmap(img.scaledToHeight(100))

    def ask_3d(self):
        self.shape = self.shape_box.currentText().lower()
        self.clear()

        self.ans = QComboBox()
        self.ans.addItems(["No", "Yes"])

        btn = QPushButton("Next")
        btn.clicked.connect(self.choose_calc)

        self.layout.addWidget(QLabel("Is it 3D?"))
        self.layout.addWidget(self.ans)
        self.layout.addWidget(btn)

    def choose_calc(self):
        if self.ans.currentText() == "Yes":
            if self.shape == "circle":
                self.shape = "sphere"
            elif self.shape == "square":
                self.shape = "cube"
            elif self.shape == "triangle":
                self.shape = "pyramid"

        self.clear()

        self.area = QCheckBox("Area")
        self.surf = QCheckBox("Surface")
        self.vol = QCheckBox("Volume")

        btn = QPushButton("Next")
        btn.clicked.connect(self.get_inputs)

        self.layout.addWidget(QLabel("What do you wanna find?"))
        if self.shape in ["circle", "square", "triangle"]:
            self.layout.addWidget(self.area)
        else:
            self.layout.addWidget(self.surf)
            self.layout.addWidget(self.vol)

        self.layout.addWidget(btn)

    def get_inputs(self):
        self.goals = {
            "Area": self.area.isChecked() if hasattr(self, "area") else False,
            "Surface Area": self.surf.isChecked() if hasattr(self, "surf") else False,
            "Volume": self.vol.isChecked() if hasattr(self, "vol") else False,
        }

        self.clear()
        self.show_pic(self.shape.capitalize())
        self.layout.addWidget(self.pic)

        self.boxes = []
        self.names = []

        for f in get_fields(self.shape, self.goals):
            self.names.append(f)
            lbl = QLabel(f + ":")
            box = QLineEdit()
            self.layout.addWidget(lbl)
            self.layout.addWidget(box)
            self.boxes.append(box)

        btn = QPushButton("Calculate")
        btn.clicked.connect(self.go)
        self.layout.addWidget(btn)

        back = QPushButton("Back")
        back.clicked.connect(self.start_screen)
        self.layout.addWidget(back)

    def go(self):
        try:
            vals = {self.names[i]: float(self.boxes[i].text()) for i in range(len(self.names))}
        except:
            QMessageBox.warning(self, "Error", "Use numbers only.")
            return

        result = calc(self.shape, self.goals, vals)
        self.history.append(f"{self.shape.title()}:\n{result}")
        save(self.shape, result)
        QMessageBox.information(self, "Answer", result)

    def show_history(self):
        self.clear()
        lbl = QLabel("History:")
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setText("\n\n".join(self.history) if self.history else "No history yet.")

        btn = QPushButton("Back")
        btn.clicked.connect(self.start_screen)

        self.layout.addWidget(lbl)
        self.layout.addWidget(txt)
        self.layout.addWidget(btn)