import sys
import csv
import sqlite3 as sl
from ui_file import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from calculate_coordinates import calculate_without_air_resistance as noairres, calculate_with_air_resistance as airres
from pyqtgraph import PlotWidget, exporters, LegendItem, mkPen


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = sl.connect("Physical_values.db")
        self.fill_phys_table()
        self.fill_boxes_with_starting_values_and_turn_on_radiobuttons()
        self.connect_buttons()
        self.configure_plot()

    def fill_boxes_with_starting_values_and_turn_on_radiobuttons(self):
        self.startspeedbox.setValue(100)
        self.anglebox.setValue(45)
        self.comboBox_planet.setCurrentIndex(8)
        self.comboBox_density.setCurrentIndex(7)
        self.comboBox_environment.setCurrentIndex(5)
        self.massBox.setValue(100)
        self.metresps.setChecked(True)
        self.degrees.setChecked(True)
        self.kilograms.setChecked(True)
        self.airresistanceoffbut.setChecked(True)
        self.pngbut.setChecked(True)

    def connect_buttons(self):
        self.calculate.clicked.connect(self.build_plot)
        self.airresistanceonbut.toggled.connect(self.air_resistance_on_checked)
        self.airresistanceoffbut.toggled.connect(self.air_resistance_off_checked)
        self.comparisonbut.toggled.connect(self.air_resistance_on_checked)
        self.savecsv.clicked.connect(self.save_csv_table)
        self.savedb.clicked.connect(self.save_db_table)
        self.saveimage.clicked.connect(self.save_plot_image)

    def configure_plot(self):
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel(axis="left", text="Y", units="m")
        self.plot.setLabel(axis="bottom", text="X", units="m")
        self.plot.setTitle(title="Задача внешней баллистики")
        self.plot.setBackground(background="#080808")
        self.noairres_pen = mkPen(color="#f05438", width=3)
        self.airres_pen = mkPen(color="#5762db", width=3)
        self.plot_legend = LegendItem(offset=(80, 50), pen="w", brush="grey", labelTextColor="#FF8C00",
                                      labelTextSize="14pt")
        self.plot_legend.setParentItem(self.plot.plotItem)

    def get_image_format(self):
        if self.pngbut.isChecked():
            return ".png"
        elif self.jpgbut.isChecked():
            return ".jpg"
        elif self.bmpbut.isChecked():
            return ".bmp"
        else:
            return ".svg"

    def save_plot_image(self):
        fname = "IMAGES/" + self.imagefilename.text().strip() + self.get_image_format()
        if len(fname) == 11:
            self.savetextedit.setPlainText("Не введено имя файла.")
            return
        plotdata = self.plot.plotItem.listDataItems()
        if len(plotdata) == 0:
            self.savetextedit.setPlainText(self.savetextedit.toPlainText() + "\n" + "Не построен график.")
            return
        try:
            f = open(fname)
            f.close()
        except FileNotFoundError:
            if fname[-4:] == ".svg":
                export = exporters.SVGExporter(self.plot.plotItem)
                width = export.parameters()["width"]
            else:
                export = exporters.ImageExporter(self.plot.plotItem)
                width = export.parameters()["width"] * 2
            export.parameters()["width"] = width
            export.export(fileName=fname)
            self.savetextedit.setPlainText(f"Файл {fname[7:]} успешно сохранен.\n Вы можете найти его в папке IMAGES")
        else:
            self.savetextedit.setPlainText(f"Изображение{fname[7:]} уже существует. Введите другое название.")

    def save_csv_table(self):
        fname = "CSVS/" + self.csvfilename.text().strip() + ".csv"
        if fname == "CSVS/.csv":
            self.savetextedit.setPlainText("Не введено имя файла.")
        rows1 = self.coords_table1.rowCount()
        rows2 = self.coords_table2.rowCount()
        if rows1 == 0 and rows2 == 0:
            self.savetextedit.setPlainText("Таблицы не заполнены. Создайте график.")
        try:
            f = open(fname)
            f.close()
        except FileNotFoundError:
            with open(fname, "w", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=";", quotechar="'")
                if rows2 != 0:
                    writer.writerow(["t, с", "X, м", "Y, м"])
                    for i in range(rows1):
                        row = [0] * 3
                        row[0] = self.coords_table1.item(i, 0).text()
                        row[1] = self.coords_table1.item(i, 1).text()
                        row[2] = self.coords_table1.item(i, 2).text()
                        writer.writerow(row)
                writer.writerow([])
                if rows1 != 0:
                    writer.writerow(["t, с", "X, м", "Y, м"])
                    for i in range(rows2):
                        row = [0] * 3
                        row[0] = self.coords_table2.item(i, 0).text()
                        row[1] = self.coords_table2.item(i, 1).text()
                        row[2] = self.coords_table2.item(i, 2).text()
                        writer.writerow(row)
                self.savetextedit.setPlainText(f"Файл {fname[5:]} успешно сохранен.\n"
                                               f"Разделитель = ';'\n"
                                               f"{'Таблица 1 и таблица 2 разделены знаком переноса строки' if rows1 != 0 and rows2 != 0 else ''}\n"
                                               f"Файл можно найти в папке CSVS")
        else:
            self.savetextedit.setPlainText("Файл уже существует. Введите другое название.")

    def save_db_table(self):
        fname = "DATABASES/" + self.dbfilename.text() + ".db"
        if fname == "DATABASES/.db":
            self.savetextedit.setPlainText("Не введено имя файла.")
        try:
            f = open(fname)
            f.close()
        except FileNotFoundError:
            db = sl.connect(fname)
            rows1 = self.coords_table1.rowCount()
            rows2 = self.coords_table2.rowCount()
            if rows1 != 0:
                with db:
                    db.execute("""CREATE TABLE Координаты_без_силы_сопротивления_воздуха (
                    _id INTEGER,
                    t FLOAT,
                    X FLOAT,
                    Y FLOAT);""")
                    data = []
                    for i in range(rows1):
                        row = [0] * 4
                        row[0] = i + 1
                        row[1] = float(self.coords_table1.item(i, 0).text())
                        row[2] = float(self.coords_table1.item(i, 1).text())
                        row[3] = float(self.coords_table1.item(i, 2).text())
                        data.append(row)
                    request = """INSERT INTO Координаты_без_силы_сопротивления_воздуха (_id, t, X, Y) values(?, ?, ?, ?);"""
                    db.executemany(request, data)
            if rows2 != 0:
                with db:
                    db.execute("""CREATE TABLE Координаты (
                                    _id INTEGER,
                                    t FLOAT,
                                    X FLOAT,
                                    Y FLOAT); """)
                    data = []
                    for i in range(rows2):
                        row = [0] * 4
                        row[0] = i + 1
                        row[1] = float(self.coords_table2.item(i, 0).text())
                        row[2] = float(self.coords_table2.item(i, 1).text())
                        row[3] = float(self.coords_table2.item(i, 2).text())
                        data.append(row)
                    request = """INSERT INTO Координаты
                                     (_id, t, X, Y) values(?, ?, ?, ?);"""
                    db.executemany(request, data)
            self.savetextedit.setPlainText(f"База данных {fname[10:]} успешно создана\n"
                                           f"")
            db.close()
        else:
            self.savetextedit.setPlainText("Файл уже существует. Введите другое название.")

    def fill_phys_table(self):
        curs = self.db.execute("SELECT * FROM MATERIAL_DENSITY")
        lst = curs.fetchall()
        self.material_table.setRowCount(len(lst))
        for elem in lst:
            self.material_table.setItem(int(elem[0]) - 1, 0, QTableWidgetItem(elem[1]))
            self.material_table.setItem(int(elem[0]) - 1, 1, QTableWidgetItem(str(elem[2]) + " кг/м3"))

        curs = self.db.execute("SELECT * FROM PLANETS")
        lst = curs.fetchall()
        self.planet_table.setRowCount(len(lst))
        for elem in lst:
            self.planet_table.setItem(int(elem[0]) - 1, 0, QTableWidgetItem(elem[1]))
            self.planet_table.setItem(int(elem[0]) - 1, 1, QTableWidgetItem(str(elem[2]) + " м/с2"))

        curs = self.db.execute("SELECT * FROM AIR_ENVIRONMENTS")
        lst = curs.fetchall()
        self.environment_table.setRowCount(len(lst))
        for elem in lst:
            self.environment_table.setItem(int(elem[0]) - 1, 0, QTableWidgetItem(elem[1]))
            self.environment_table.setItem(int(elem[0]) - 1, 1, QTableWidgetItem(str(elem[2]) + " кг/м3"))

    def air_resistance_on_checked(self):
        self.massBox.setEnabled(True)
        self.comboBox_environment.setEnabled(True)
        self.massframe.setEnabled(True)
        self.kilograms.setEnabled(True)
        self.grams.setEnabled(True)
        self.pounds.setEnabled(True)
        self.tons.setEnabled(True)
        self.comboBox_density.setEnabled(True)

    def air_resistance_off_checked(self):
        self.massBox.setEnabled(False)
        self.comboBox_environment.setEnabled(False)
        self.massframe.setEnabled(False)
        self.kilograms.setEnabled(False)
        self.grams.setEnabled(False)
        self.pounds.setEnabled(False)
        self.tons.setEnabled(False)
        self.comboBox_density.setEnabled(False)

    def get_height_in_meters(self):
        return self.start_height.value()

    def get_speed_in_metersps(self):
        if self.metresps.isChecked():
            speed = self.startspeedbox.value()
        elif self.kilometresph.isChecked():
            speed = self.startspeedbox.value() * 1000 / 3600
        elif self.milesph.isChecked():
            speed = self.startspeedbox.value() * 0.44704
        else:
            speed = self.startspeedbox.value() * 0.9144
        return speed

    def get_mass_in_kilograms(self):
        if self.kilograms.isChecked():
            mass = self.massBox.value()
        elif self.grams.isChecked():
            mass = self.massBox.value() / 1000
        elif self.pounds.isChecked():
            mass = self.massBox.value() * 0.45
        else:
            mass = self.massBox.value() * 1000
        return mass

    def get_angle_in_degrees(self):
        if self.degrees.isChecked():
            angle = self.anglebox.value()
        elif self.radians.isChecked():
            angle = self.anglebox.value() * 57.3
        elif self.minutes.isChecked():
            angle = self.anglebox.value() / 60
        else:
            angle = self.anglebox.value() / 3600
        return angle

    def get_material_density(self):
        if self.comboBox_density.currentText() != "":
            with self.db:
                curs = self.db.execute(
                    f"SELECT density FROM MATERIAL_DENSITY WHERE material == '{self.comboBox_density.currentText()}'")
                density = curs.fetchone()[0]
                return density
        return -1

    def get_planet_acceleration(self):
        if self.comboBox_planet.currentText() != "":
            with self.db:
                curs = self.db.execute(
                    f"SELECT acceleration FROM PLANETS WHERE planet == '{self.comboBox_planet.currentText()}'")
                acceleration = curs.fetchone()[0]
                return acceleration
        return -1

    def get_air_environment_density(self):
        if self.comboBox_environment.currentText() != "":
            with self.db:
                curs = self.db.execute(
                    f"SELECT density FROM AIR_ENVIRONMENTS WHERE air == '{self.comboBox_environment.currentText()}'")
                density = curs.fetchone()[0]
                return density
        return -1

    def check_errors_in_input(self):
        no_errors = True
        errors_text = []
        if self.comboBox_planet.currentText() == "":
            no_errors = False
            errors_text.append(" - Не выбрана планета")
        if self.get_speed_in_metersps() == 0:
            no_errors = False
            errors_text.append(" - Не задана начальная скорость")
        angle = self.get_angle_in_degrees()
        if angle == 0 or angle > 90:
            no_errors = False
            errors_text.append(" - Неверное значение угла(угол может быть от 0 до 90 градусов)")
        if self.airresistanceonbut.isChecked():
            if self.comboBox_density.currentText() == "":
                no_errors = False
                errors_text.append(" - Не выбрана плотность вещества")
            if self.comboBox_environment.currentText() == "":
                no_errors = False
                errors_text.append(" - Не выбрана воздушная среда")
            if self.massBox.value() == 0:
                no_errors = False
                errors_text.append(" - Не задана масса тела")
        if not no_errors:
            text = "Программа не запущена так как были найдены следующие ошибки в исходных данных:\n"
            text += "\n".join(errors_text)
            self.errorscreen.setPlainText(text)
        return no_errors

    def add_noairres_plot_to_plot(self, speed, angle, accel, height, pen="r"):
        x, y, t = noairres(
            start_speed=speed,
            angle=angle,
            g=accel,
            start_height=height
        )
        self.coords_table1.setRowCount(len(t))
        for i in range(len(t)):
            self.coords_table1.setItem(i, 0, QTableWidgetItem(str(t[i])))
            self.coords_table1.setItem(i, 1, QTableWidgetItem(str(x[i])))
            self.coords_table1.setItem(i, 2, QTableWidgetItem(str(y[i])))
        self.plot.plot(x, y, pen=pen)
        self.plot_legend.addItem(self.plot.plotItem.listDataItems()[-1], "Без учета сопротивления воздуха")
        return x, y, t

    def add_airres_plot_to_plot(self, speed, angle, accel, height, air_dens, mat_dens, mass, pen="b"):
        x, y, t = airres(start_speed=speed,
                         angle=angle,
                         g=accel,
                         start_height=height,
                         air_density=air_dens,
                         material_density=mat_dens,
                         mass=mass
                         )
        self.coords_table2.setRowCount(len(t))
        for i in range(len(t)):
            self.coords_table2.setItem(i, 0, QTableWidgetItem(str(t[i])))
            self.coords_table2.setItem(i, 1, QTableWidgetItem(str(x[i])))
            self.coords_table2.setItem(i, 2, QTableWidgetItem(str(y[i])))
        self.plot.plot(x, y, pen=pen)
        self.plot_legend.addItem(self.plot.plotItem.listDataItems()[-1], "С учетом сопротивления воздуха")
        return x, y, t

    def build_plot(self):
        if self.check_errors_in_input():
            self.errorscreen.setPlainText("Ошибок в данных нет, начинаю вычисление траектории падения тела.\n"
                                          "Построение графика....")
            self.plot.clear()
            self.plot_legend.clear()
            self.coords_table1.clear()
            self.coords_table1.setRowCount(0)
            self.coords_table2.clear()
            self.coords_table2.setRowCount(0)
            speed = self.get_speed_in_metersps()
            angle = self.get_angle_in_degrees()
            acceleration = self.get_planet_acceleration()
            start_height = self.get_height_in_meters()
            air_density = self.get_air_environment_density()
            material_density = self.get_material_density()
            mass = self.get_mass_in_kilograms()
            if self.airresistanceoffbut.isChecked():
                x1, y1, t1 = self.add_noairres_plot_to_plot(
                    speed=speed,
                    angle=angle,
                    accel=acceleration,
                    height=start_height,
                    pen=self.noairres_pen
                )
                x2, y2, t2 = [(0,) for _ in range(3)]
                self.plot.setTitle(title="Параболическая кривая")
            elif self.airresistanceonbut.isChecked():
                x2, y2, t2 = self.add_airres_plot_to_plot(
                    speed=speed,
                    angle=angle,
                    accel=acceleration,
                    height=start_height,
                    air_dens=air_density,
                    mat_dens=material_density,
                    mass=mass,
                    pen=self.airres_pen
                )
                x1, y1, t1 = [(0,) for _ in range(3)]
                self.plot.setTitle(title="Баллистическая кривая")
            else:
                x1, y1, t1 = self.add_noairres_plot_to_plot(
                    speed=speed,
                    angle=angle,
                    accel=acceleration,
                    height=start_height,
                    pen=self.noairres_pen
                )
                x2, y2, t2 = self.add_airres_plot_to_plot(
                    speed=speed,
                    angle=angle,
                    accel=acceleration,
                    height=start_height,
                    air_dens=air_density,
                    mat_dens=material_density,
                    mass=mass,
                    pen=self.airres_pen
                )
                self.plot.setTitle(title="Сравнение баллистической и параболической кривых")
            self.plot.addLine(y=0)
            m = max(max(x1), max(x2), max(y1), max(y2))
            self.plot.setRange(xRange=[0, m], yRange=[0, m])
            self.errorscreen.setPlainText(self.errorscreen.toPlainText() + "\nГрафик построен")
            self.tabWidget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
