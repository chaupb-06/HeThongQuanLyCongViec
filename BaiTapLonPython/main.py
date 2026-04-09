import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QComboBox,
    QLabel,
    QHBoxLayout,
    QWidget
)
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
from database import Database


class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.db = Database()
        self.current_id = None
        self.sort_mode = "deadline"

        
        self.table_tasks.setColumnCount(8)
        self.table_tasks.setHorizontalHeaderLabels([
            "STT",
            "ID",
            "Tên Việc",
            "Danh Mục",
            "Người Làm",
            "Trạng Thái",
            "Ưu Tiên",
            "Hạn Chót"
        ])

        self.table_tasks.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_tasks.verticalHeader().setVisible(False)
        self.table_tasks.setSelectionBehavior(
            self.table_tasks.SelectRows
        )

        
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        lbl_sort = QLabel("Sắp xếp:")
        self.combo_sort = QComboBox()

        self.combo_sort.addItems([
        "Theo Hạn Chót",
        "Theo ID",
        "Theo Danh Mục"
        ])

        top_layout.addWidget(lbl_sort)
        top_layout.addWidget(self.combo_sort)

        self.tab_search.layout().insertWidget(0, top_widget)

       
        self.btn_add.clicked.connect(self.add_task)
        self.btn_edit.clicked.connect(self.update_task)
        self.btn_delete.clicked.connect(self.delete_task)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_refresh_all.clicked.connect(self.load_data)
        self.btn_export.clicked.connect(self.export_excel)

        self.txt_search.textChanged.connect(self.load_data)
        self.table_tasks.itemClicked.connect(self.fill_form)
        self.combo_sort.currentIndexChanged.connect(self.change_sort)

        
        self.init_combos()
        self.load_data()

    
    def format_text(self, text):
        return " ".join(word.capitalize() for word in text.strip().split())

    def change_sort(self):
    
        text = self.combo_sort.currentText()

        if "ID" in text:
            self.sort_mode = "id"
        elif "Danh Mục" in text:
            self.sort_mode = "category"
        elif "Tên" in text:
            self.sort_mode = "name"
        else:
            self.sort_mode = "deadline"

        self.load_data()

   
    def init_combos(self):
        self.combo_category.clear()
        for cid, name in self.db.get_lookup("categories"):
            self.combo_category.addItem(name, cid)

        self.combo_user.clear()
        for uid, name in self.db.get_lookup("users"):
            self.combo_user.addItem(name, uid)

        self.combo_status.clear()
        self.combo_status.addItems([
            "Mới",
            "Đang làm",
            "Xong",
            "Tạm dừng"
        ])

        self.combo_priority.clear()
        self.combo_priority.addItems([
            "Thấp",
            "Trung bình",
            "Cao",
            "Khẩn cấp"
        ])

    
    def load_data(self):
        search = self.txt_search.text()
        tasks = self.db.fetch_tasks(search, self.sort_mode)

        self.table_tasks.setRowCount(0)

        for row, task in enumerate(tasks):
            self.table_tasks.insertRow(row)

            row_data = [
                row + 1,  
                task["id"],
                task["task_name"],
                task["category_name"],
                task["user_name"],
                task["status"],
                task["priority"],
                str(task["deadline"])
            ]

            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table_tasks.setItem(row, col, item)

    
    def fill_form(self, item):
        row = item.row()

        self.current_id = self.table_tasks.item(row, 1).text()

        self.txt_task_name.setText(
            self.table_tasks.item(row, 2).text()
        )

        self.combo_category.setCurrentText(
            self.table_tasks.item(row, 3).text()
        )

        self.combo_user.setCurrentText(
            self.table_tasks.item(row, 4).text()
        )

        self.combo_status.setCurrentText(
            self.table_tasks.item(row, 5).text()
        )

        self.combo_priority.setCurrentText(
            self.table_tasks.item(row, 6).text()
        )

        date_text = self.table_tasks.item(row, 7).text()
        self.date_deadline.setDate(
            QDate.fromString(date_text, "yyyy-MM-dd")
        )

        self.main_tab.setCurrentIndex(0)

    
    def add_task(self):
        task_name = self.format_text(self.txt_task_name.text())

        if not task_name:
            QMessageBox.warning(self, "Lỗi", "Tên công việc không được để trống")
            return

        query = """
            INSERT INTO tasks
            (task_name, category_id, user_id, status, priority, deadline)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        params = (
            task_name,
            self.combo_category.currentData(),
            self.combo_user.currentData(),
            self.combo_status.currentText().lower(),
            self.combo_priority.currentText(),
            self.date_deadline.date().toPyDate()
        )

        if self.db.execute(query, params):
            self.load_data()
            self.clear_form()

    def update_task(self):
        if not self.current_id:
            return

        query = """
            UPDATE tasks
            SET task_name=%s,
                category_id=%s,
                user_id=%s,
                status=%s,
                priority=%s,
                deadline=%s
            WHERE id=%s
        """

        params = (
            self.format_text(self.txt_task_name.text()),
            self.combo_category.currentData(),
            self.combo_user.currentData(),
            self.combo_status.currentText().lower(),
            self.combo_priority.currentText(),
            self.date_deadline.date().toPyDate(),
            self.current_id
        )

        if self.db.execute(query, params):
            self.load_data()

    
    def delete_task(self):
        if self.current_id:
            if self.db.execute(
                "DELETE FROM tasks WHERE id=%s",
                (self.current_id,)
            ):
                self.load_data()
                self.clear_form()

    
    def clear_form(self):
        self.current_id = None
        self.txt_task_name.clear()
        self.date_deadline.setDate(QDate.currentDate())

    def export_excel(self):
        data = []

        for row in range(self.table_tasks.rowCount()):
            data.append({
                "STT": self.table_tasks.item(row, 0).text(),
                "ID": self.table_tasks.item(row, 1).text(),
                "Tên Việc": self.table_tasks.item(row, 2).text(),
                "Danh Mục": self.table_tasks.item(row, 3).text(),
                "Người Làm": self.table_tasks.item(row, 4).text(),
                "Trạng Thái": self.table_tasks.item(row, 5).text(),
                "Ưu Tiên": self.table_tasks.item(row, 6).text(),
                "Hạn Chót": self.table_tasks.item(row, 7).text()
            })

        df = pd.DataFrame(data)
        file_name = "Bao_Cao_Cong_Viec.xlsx"
        df.to_excel(file_name, index=False)
        os.startfile(file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec_())