## Проста програма для малювання. Може знадобитись при створенні датасетів для анілізу письма.


Бібліотеки: \
pip install PyQt5 pyqt5-tools 


Для конвертації файла .ui в .py: \
pyuic5 -x WidgetDrawing.ui -o WidgetDrawing_ui.py \
Не забудьте підігнати main.py зміни після змін .ui та компілювання в .py


Для створення .exe: \
python -m PyInstaller --onefile --noconsole --name "Pencil drawing" --icon=Resource/pencil.ico --add-data "Resource/pencil.ico;." main.py

--add-data -> для підтягування іконки програми
