#    Copyright(non) `Actaviys`    #                                             |
#                                                                               |
# Permission is hereby granted, free of charge, to any person obtaining a copy  |
# of this software and associated documentation files (the "Software"), to deal |
# in the Software without restriction, including without limitation the rights  |
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     |
# copies of the Software, and to permit persons to whom the Software is         |
# furnished to do so, subject to the following conditions:                      |
#                                                                               |
# The above copyright notice and this permission notice shall be included in    |
# all copies or substantial portions of the Software.                           |
#                                                                               |
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    |
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      |
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   |
# "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"      |
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, |
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE |
# SOFTWARE.                                                                     |
################################################################################|
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os


class DrawingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Зображення для малювання (ініціалізуємо з розміром віджета)
        self.image = QtGui.QImage(28, 28, QtGui.QImage.Format_RGB32)  # Початковий розмір, але він адаптується
        self.image.fill(QtCore.Qt.white)  # Заповнюємо білим фоном
        
        # Параметри пензля
        self.drawing = False
        self.brush_size = 45
        self.brush_color = QtCore.Qt.black
        self.last_point = QtCore.QPoint()
        self.is_erasing = False  # Режим гумки

#  Обробка курсора #
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QtGui.QPainter(self.image)
            color = QtCore.Qt.white if self.is_erasing else self.brush_color
            painter.setPen(QtGui.QPen(color, self.brush_size, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
        self.update()  # Оновлюємо віджет

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvas_painter = QtGui.QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def resizeEvent(self, event):
        # Адаптуємо зображення під новий розмір віджета (зберігаємо попередній малюнок)
        if self.width() > self.image.width() or self.height() > self.image.height():
            new_image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
            new_image.fill(QtCore.Qt.white)
            painter = QtGui.QPainter(new_image)
            painter.drawImage(QtCore.QPoint(0, 0), self.image)
            self.image = new_image
        super().resizeEvent(event)
#       #

    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.brush_color = color
            self.is_erasing = False  # Вимикаємо гумку при зміні кольору

    def choose_size(self, coun_size):
        size = coun_size.value()
        self.brush_size = size
    
    def clear_canvas(self):
        self.image.fill(QtCore.Qt.white)
        self.update()
    
    def toggle_eraser(self, state_eras):
        self.is_erasing = not self.is_erasing
        if self.is_erasing:
            state_eras.setText("Eraser `ON`") #
        else: state_eras.setText("Eraser `OFF`")
        
    def save_image(self, format_combo, width_edit, height_edit, name_file="") -> bool:
        # Отримуємо формат
        file_format = format_combo.currentText().lower()
        if not file_format:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Вибери формат!")
            return False

        # Отримуємо ширину/висоту
        try:
            width = int(width_edit.text()) if width_edit.text() else self.image.width()
            height = int(height_edit.text()) if height_edit.text() else self.image.height()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Невалідні значення ширини/висоти!")
            return False

        # Якщо потрібно, масштабуємо зображення
        save_image = self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # Якщо є то добавляю свою назву
        if name_file != "": #
            # Діалог збереження
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Зберегти зображення", f"{name_file}", f"Images (*.{file_format})")
        else:
            # Діалог збереження
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Зберегти зображення", "", f"Images (*.{file_format})")
        
        # Зберігаю забраження
        if file_path:
            if not file_path.endswith(f".{file_format}"):
                file_path += f".{file_format}"
            save_image.save(file_path)
            return True
        return False



textCombitationsKey = "Combinations Key:\n \
    Save image -> `Ctrl^S` or `Q`\n \
    Clear field -> `W`\n \
    Eraser -> `E`\n \
    Brush size -> more- `Ctrl^-` \n \
                          less- `Ctrl^+`"


def resource_path(relative_path):
    """ 
    Отримати абсолютний шлях до ресурсу, для PyInstaller. 
    Для успішного компілювання іконки в .exe файл.
    """
    try:
        # PyInstaller створює тимчасову папку і зберігає шлях у _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)




class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowTitle("Pencil drawing")
        Form.setMinimumSize(QtCore.QSize(800, 550)) # Мінімальний розмір вікна
        Form.setMaximumSize(QtCore.QSize(800, 550)) # Максимальний розмір вікна
        
        icon_path = resource_path("pencil.ico")  # Для компіляції ()
        # icon_path = "C:\\..SavingPencilDrawing\\Resource\\pencil.ico"  # Для розробки
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)

        self.counterSavedFileNamed = None # Для лічильника збережених файлів
        
        # Головний лейаут #
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        #   #

        # Кнопка очищення поля #
        self.ButtonClearField = QtWidgets.QPushButton(Form)
        self.ButtonClearField.setObjectName("ButtonClear")
        self.ButtonClearField.setText("Clean")
        self.verticalLayout.addWidget(self.ButtonClearField)
        #   #
        
        # Гумка #
        self.ButtonEraser = QtWidgets.QPushButton(Form) 
        self.ButtonEraser.setObjectName("ButtonEraser")
        self.ButtonEraser.setText("Eraser")
        self.verticalLayout.addWidget(self.ButtonEraser)
        #   #
        
        # Вибір кольору #
        self.ButtonSetColor = QtWidgets.QPushButton(Form)
        self.ButtonSetColor.setObjectName("ButtonSetColor")
        self.ButtonSetColor.setText("Set color")
        self.verticalLayout.addWidget(self.ButtonSetColor)
        #   #
        
        # Вибір розміру пензля #
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.SpinBoxChangeBrushSize = QtWidgets.QSpinBox(Form)
        self.SpinBoxChangeBrushSize.setObjectName("SpinBoxChangeBrushSize")
        self.SpinBoxChangeBrushSize.setMinimum(1)
        self.SpinBoxChangeBrushSize.setMaximum(400)
        self.horizontalLayout_2.addWidget(self.SpinBoxChangeBrushSize)
        
        self.LabelChangeBrushSize = QtWidgets.QLabel(Form)
        self.LabelChangeBrushSize.setObjectName("LabelChangeBrushSize")
        self.LabelChangeBrushSize.setText("Brush Size")
        self.horizontalLayout_2.addWidget(self.LabelChangeBrushSize)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        #   #
        
        # Лейбл для картинки #
        self.Label_IconW = QtWidgets.QLabel(Form)
        self.Label_IconW.setObjectName("Label_IconW")
        self.Label_IconW.setPixmap(QtGui.QPixmap(icon_path))
        self.verticalLayout.addWidget(self.Label_IconW)
        #   #
        
        # Роздільна лінія 1 #
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        #   #

        # Додаткові комбінації #
        self.LabelAdditionalCombinations = QtWidgets.QLabel(Form)
        self.LabelAdditionalCombinations.setObjectName("LabelAdditionalCombinations")
        self.LabelAdditionalCombinations.setText(textCombitationsKey)
        self.verticalLayout.addWidget(self.LabelAdditionalCombinations)
        #   #
        
        
        # Роздільна лінія 2 #
        self.line_1 = QtWidgets.QFrame(Form)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_1.setLineWidth(2)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setObjectName("line")
        self.verticalLayout.addWidget(self.line_1)
        #   #
        
        # Початок назви для зберігання картинок #
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LabelFileStartName = QtWidgets.QLabel(Form)
        self.LabelFileStartName.setObjectName("LabelFileStartName")
        self.horizontalLayout_3.addWidget(self.LabelFileStartName)
        self.LineFileStartName = QtWidgets.QLineEdit(Form)
        self.LineFileStartName.setObjectName("LineEditFileStartName")
        self.LabelFileStartName.setText("Start count name (integer)")
        self.horizontalLayout_3.addWidget(self.LineFileStartName)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        #   #

        # Авто-очищення поля #
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBoxAutoClean = QtWidgets.QCheckBox(Form)
        self.CheckBoxAutoClean.setObjectName("CheckBoxAutoClean")
        self.CheckBoxAutoClean.setText("Auto clear")
        self.horizontalLayout.addWidget(self.CheckBoxAutoClean)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        
        self.ButtonSaveImage = QtWidgets.QPushButton(Form)
        self.ButtonSaveImage.setObjectName("ButtonSaveImage")
        self.ButtonSaveImage.setText("Save image")
        self.horizontalLayout.addWidget(self.ButtonSaveImage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        #   #

        # Вибір формату для збереження #
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.LabelFormat = QtWidgets.QLabel(Form)
        self.LabelFormat.setObjectName("LabelFormat")
        self.LabelFormat.setText("Format")
        self.horizontalLayout_3.addWidget(self.LabelFormat)

        self.ComboBoxSetFormat = QtWidgets.QComboBox(Form)
        self.ComboBoxSetFormat.setObjectName("ComboBoxSetFormat")
        self.ComboBoxSetFormat.addItems(["PNG", "JPG", "BMP"])  # Додаємо формати
        self.horizontalLayout_3.addWidget(self.ComboBoxSetFormat)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        #   #

        # Введення ширини/висоти для збереження #
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.LabelWidth = QtWidgets.QLabel(Form)
        self.LabelWidth.setObjectName("LabelWidth")
        self.LabelWidth.setText("Width")
        self.gridLayout_2.addWidget(self.LabelWidth, 0, 0, 1, 1)

        self.LineSetWidth = QtWidgets.QLineEdit(Form)  # 
        self.LineSetWidth.setObjectName("LineSetWidth")
        self.LineSetWidth.setText("28")
        self.gridLayout_2.addWidget(self.LineSetWidth, 0, 1, 1, 1)

        self.LabelHeight = QtWidgets.QLabel(Form)
        self.LabelHeight.setObjectName("LabelHeight")
        self.LabelHeight.setText("Height")
        self.gridLayout_2.addWidget(self.LabelHeight, 1, 0, 1, 1)

        self.LineSetHeight = QtWidgets.QLineEdit(Form) # 
        self.LineSetHeight.setObjectName("LineSetHeight")
        self.LineSetHeight.setText("28")
        self.gridLayout_2.addWidget(self.LineSetHeight, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        #   #

        # Роздільна лінія 3 #
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 1, 1, 1)
        #   #
        
        # Замість простого QWidget створюємо наш кастомний DrawingWidget
        self.WidgetPainter = DrawingWidget(Form)
        self.WidgetPainter.setObjectName("WidgetPainter")
        self.WidgetPainter.setMinimumSize(550, 550)  # Мінімальний розмір для полотна
        self.gridLayout.addWidget(self.WidgetPainter, 0, 2, 1, 1)

        # Підключаємо сигнали до методів 'DrawingWidget'
        self.ButtonClearField.clicked.connect(self.WidgetPainter.clear_canvas)
        self.ButtonSetColor.clicked.connect(self.WidgetPainter.choose_color)
        self.ButtonSaveImage.clicked.connect(self.metodSaverImage)
        self.ButtonEraser.clicked.connect(lambda: self.WidgetPainter.toggle_eraser(self.ButtonEraser))
        self.SpinBoxChangeBrushSize.setValue(self.WidgetPainter.brush_size)
        self.SpinBoxChangeBrushSize.valueChanged.connect(lambda: self.WidgetPainter.choose_size(self.SpinBoxChangeBrushSize))
        self.LineFileStartName.textChanged.connect(self.metodCounterNameFiles)
        #   #

        self.metodHandlingKeyCombinations() # Підключаю обробку комбінацій клавіш
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    
    def metodCounterNameFiles(self):
        """ Метод для для початкової назви файлу """
        txrRf = self.LineFileStartName.text()
        if txrRf:
            try:
                self.counterSavedFileNamed = int(txrRf)
            except:
                self.LineFileStartName.clear()
        else: self.counterSavedFileNamed = None
    
    
    def metodSaverImage(self):
        """ Метод для збереження зображення з полотна та очищення полотна, якщо потрібно """
        if self.counterSavedFileNamed != None:
            resSave = self.WidgetPainter.save_image(self.ComboBoxSetFormat, self.LineSetWidth, self.LineSetHeight, self.counterSavedFileNamed)
            self.counterSavedFileNamed += 1
        else:
            resSave = self.WidgetPainter.save_image(self.ComboBoxSetFormat, self.LineSetWidth, self.LineSetHeight)
        if self.CheckBoxAutoClean.isChecked() and resSave:
            self.WidgetPainter.clear_canvas()

    
    def metodHandlingKeyCombinations(self):
        """ Метод для для додавання шорткатів """
        # Додаємо шорткат 'Ctrl+S, Q' для збереження
        self.shortcutSaveCombination_CtrS = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), Form)
        self.shortcutSaveCombination_CtrS.activated.connect(self.metodSaverImage)
        self.shortcutSaveCombination_Q = QtWidgets.QShortcut(QtGui.QKeySequence("Q"), Form)
        self.shortcutSaveCombination_Q.activated.connect(self.metodSaverImage)

        # Додаємо шорткат 'W' для очищення поля
        self.shortcutCleanField = QtWidgets.QShortcut(QtGui.QKeySequence("W"), Form)
        self.shortcutCleanField.activated.connect(self.WidgetPainter.clear_canvas)

        # Додаємо шорткат 'E' для гумки
        self.shortcutEraser = QtWidgets.QShortcut(QtGui.QKeySequence("E"), Form)
        self.shortcutEraser.activated.connect(lambda: self.WidgetPainter.toggle_eraser(self.ButtonEraser))
        
        # Додаємо шорткат 'R' для вобору кольору
        self.shortcutColorSet = QtWidgets.QShortcut(QtGui.QKeySequence("R"), Form)
        self.shortcutColorSet.activated.connect(self.WidgetPainter.choose_color)

        # Додаємо шорткат 'Ctrl+-' для зменшення розміру пензля
        self.shortcutDecreaseBrushSize = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+-"), Form)
        self.shortcutDecreaseBrushSize.activated.connect(lambda: self.SpinBoxChangeBrushSize.setValue(self.SpinBoxChangeBrushSize.value() - 1))

        # Додаємо шорткат 'Ctrl+=' для збільшення розміру пензля
        self.shortcutIncreaseBrushSize = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+="), Form)
        self.shortcutIncreaseBrushSize.activated.connect(lambda: self.SpinBoxChangeBrushSize.setValue(self.SpinBoxChangeBrushSize.value() + 1))
        


app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)


if __name__ == "__main__":
    Form.show()
    sys.exit(app.exec_())