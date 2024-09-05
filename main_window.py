import os
from PyQt5.QtWidgets import QMainWindow, QShortcut, QFileDialog, QInputDialog, QMessageBox # type: ignore
from qt_designer_ui import Ui_MainWindow
from PyQt5.QtGui import QKeySequence, QPixmap # type: ignore
from PyQt5.QtCore import Qt # type: ignore
from image_handler import ImageHandler
import tensorflow as tf
from tensorflow import keras
import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(720, 480)
        self.close_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_W), self)
        self.close_shortcut.activated.connect(self.close)

        self.current_image_path = None
        self.image_directory = None
        self.image_handler = None
        self.model = None
        self.classes = None
        
        self.image_directory_button.clicked.connect(self.select_directory)
        self.choose_model_button.clicked.connect(self.choose_model)
        self.shuffle_button.clicked.connect(self.shuffle_button_clicked)
        self.predict_button.clicked.connect(self.predict_button_clicked)
        
        print("===  SUCCESS  ===")
        
        
    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory Containing Images")
        if not self.validate_directory(directory):
            QMessageBox.critical(self, "Directory Error", "The selected directory does not contain any image files.")
        else:
            self.image_directory = directory
            print(self.image_directory)
            self.image_handler = ImageHandler(self.image_directory)
            
            class_names, ok = QInputDialog.getText(self, "Enter Class Names", "Make sure that the individual classes are separated by a SPACE")
            if ok and class_names:
                self.classes = class_names.split()
        
    def validate_directory(self, directory):
        image_extensions = {".jpg", ".jpeg", ".png",
                            ".gif", ".bmp", ".tiff", ".webp"}
        for i in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, i)) == True:
                if os.path.splitext(os.path.join(directory, i))[1] in image_extensions:
                    return True
        return False
    
    def shuffle_button_clicked(self):
        self.current_image_path = self.image_handler.get_random_image()
        image = QPixmap(self.current_image_path).scaled(226, 226, Qt.IgnoreAspectRatio)
        self.image_container.setPixmap(image)
        
    def choose_model(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "")[0]
        self.model = keras.models.load_model(filename, compile=False)
        self.model.compile(optimizer='adam', loss="categorical_crossentropy", metrics=['accuracy'])
        
    def predict_button_clicked(self):
        prediction = np.argmax(self.model.predict(self.image_handler.get_image_as_numpy(self.current_image_path)), axis=1)[0]
        print(prediction)
        print(self.classes[prediction])
        
    def closeEvent(self, event):
        print("App Closed Successfuly.")
        event.accept()