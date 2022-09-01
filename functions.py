from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton

grid = QGridLayout()
grid.setHorizontalSpacing(0)

def frame1(target_color, best_color, text_left, text_right):
    
    target_label = QLabel("Target Color:")
    grid.addWidget(target_label, 0, 0)
    button1 = QPushButton()
    button1.setStyleSheet(f"border: 4px solid {target_color}; background-color: {target_color}; padding: 25px 0;")
    grid.addWidget(button1, 1, 0)
    target_desc = QLabel(text_left)
    grid.addWidget(target_desc, 2, 0)

    best_label = QLabel("Best Color:")
    grid.addWidget(best_label, 0, 1)
    button2 = QPushButton()
    button2.setStyleSheet(f"border: 4px solid {best_color}; background-color: {best_color}; padding: 25px 0;")
    grid.addWidget(button2, 1, 1)
    best_desc = QLabel(text_right)
    grid.addWidget(best_desc, 2, 1)