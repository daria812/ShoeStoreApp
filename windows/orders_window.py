from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QComboBox, QDateEdit,
                               QDialog, QLabel, QLineEdit)
from PySide6.QtCore import Qt, QDate
from database.db import Database



class OrdersWindow(QMainWindow):
    def __init__(self, role, parent=None):
        super().__init__(parent)
        self.role = role
        self.db = Database.instance()
        self.setWindowTitle("Заказы")
        self.resize(900, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Кнопки управления (только для админа)
        if self.role == "admin":
            btn_layout = QHBoxLayout()
            self.btn_add = QPushButton("Добавить заказ")
            self.btn_add.clicked.connect(self.add_order)
            self.btn_edit = QPushButton("Редактировать заказ")
            self.btn_edit.clicked.connect(self.edit_order)
            self.btn_delete = QPushButton("Удалить заказ")
            self.btn_delete.clicked.connect(self.delete_order)
            btn_layout.addWidget(self.btn_add)
            btn_layout.addWidget(self.btn_edit)
            btn_layout.addWidget(self.btn_delete)
            layout.addLayout(btn_layout)

        # Таблица заказов
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Номер заказа", "Клиент", "Статус",
                                              "Дата заказа", "Дата выдачи", "Адрес выдачи", "Код получения"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        self.load_orders()

    def load_orders(self):
        query = """
            SELECT o.id, o.order_number, u.full_name, os.name AS status,
                   o.order_date, o.delivery_date, p.address, o.pickup_code
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN order_statuses os ON o.order_status_id = os.id
            LEFT JOIN pickup_points p ON o.pickup_point_id = p.id
            ORDER BY o.order_date DESC
        """
        rows = self.db.execute_query(query)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['order_number'])))
            self.table.setItem(i, 2, QTableWidgetItem(row['full_name']))
            self.table.setItem(i, 3, QTableWidgetItem(row['status']))
            self.table.setItem(i, 4, QTableWidgetItem(str(row['order_date']) if row['order_date'] else ''))
            self.table.setItem(i, 5, QTableWidgetItem(str(row['delivery_date']) if row['delivery_date'] else ''))
            self.table.setItem(i, 6, QTableWidgetItem(row['address'] or ''))
            self.table.setItem(i, 7, QTableWidgetItem(row['pickup_code'] or ''))

    def add_order(self):
        dialog = OrderDialog(parent=self)
        if dialog.exec():
            self.load_orders()

    def edit_order(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для редактирования")
            return
        order_id = int(self.table.item(selected, 0).text())
        dialog = OrderDialog(order_id, self)
        if dialog.exec():
            self.load_orders()

    def delete_order(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для удаления")
            return
        order_id = int(self.table.item(selected, 0).text())
        reply = QMessageBox.question(self, "Подтверждение", "Удалить заказ? Все позиции заказа также будут удалены.",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.execute_non_query("DELETE FROM orders WHERE id = %s", (order_id,))
            self.load_orders()


class OrderDialog(QDialog):
    def __init__(self, order_id=None, parent=None):
        super().__init__(parent)
        self.order_id = order_id
        self.db = Database.instance()
        self.setWindowTitle("Добавление заказа" if order_id is None else "Редактирование заказа")
        self.resize(400, 350)

        layout = QVBoxLayout(self)

        # Пользователь
        layout.addWidget(QLabel("Клиент:"))
        self.user_combo = QComboBox()
        self.load_users()
        layout.addWidget(self.user_combo)

        # Статус заказа
        layout.addWidget(QLabel("Статус:"))
        self.status_combo = QComboBox()
        self.load_statuses()
        layout.addWidget(self.status_combo)

        # Адрес пункта выдачи
        layout.addWidget(QLabel("Адрес пункта выдачи:"))
        self.pickup_combo = QComboBox()
        self.load_pickup_points()
        layout.addWidget(self.pickup_combo)

        # Дата заказа
        layout.addWidget(QLabel("Дата заказа:"))
        self.order_date_edit = QDateEdit()
        self.order_date_edit.setCalendarPopup(True)
        self.order_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.order_date_edit)

        # Дата выдачи
        layout.addWidget(QLabel("Дата выдачи:"))
        self.delivery_date_edit = QDateEdit()
        self.delivery_date_edit.setCalendarPopup(True)
        self.delivery_date_edit.setDate(QDate.currentDate().addDays(7))
        layout.addWidget(self.delivery_date_edit)

        # Код получения
        layout.addWidget(QLabel("Код получения:"))
        self.code_edit = QLineEdit()
        layout.addWidget(self.code_edit)

        # Кнопки
        buttons = QHBoxLayout()
        btn_ok = QPushButton("Сохранить")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)

        if order_id:
            self.load_order_data()

    def load_users(self):
        rows = self.db.execute_query("SELECT id, full_name FROM users WHERE role IN ('client', 'manager', 'admin') ORDER BY full_name")
        for row in rows:
            self.user_combo.addItem(row['full_name'], row['id'])

    def load_statuses(self):
        rows = self.db.execute_query("SELECT id, name FROM order_statuses ORDER BY id")
        for row in rows:
            self.status_combo.addItem(row['name'], row['id'])

    def load_pickup_points(self):
        rows = self.db.execute_query("SELECT id, address FROM pickup_points ORDER BY address")
        for row in rows:
            self.pickup_combo.addItem(row['address'], row['id'])

    def load_order_data(self):
        query = "SELECT * FROM orders WHERE id = %s"
        rows = self.db.execute_query(query, (self.order_id,))
        if not rows:
            return
        o = rows[0]
        # Устанавливаем выбранные значения
        idx = self.user_combo.findData(o['user_id'])
        if idx >= 0: self.user_combo.setCurrentIndex(idx)
        idx = self.status_combo.findData(o['order_status_id'])
        if idx >= 0: self.status_combo.setCurrentIndex(idx)
        idx = self.pickup_combo.findData(o['pickup_point_id'])
        if idx >= 0: self.pickup_combo.setCurrentIndex(idx)
        if o['order_date']:
            self.order_date_edit.setDate(QDate.fromString(str(o['order_date']), "yyyy-MM-dd"))
        if o['delivery_date']:
            self.delivery_date_edit.setDate(QDate.fromString(str(o['delivery_date']), "yyyy-MM-dd"))
        self.code_edit.setText(o['pickup_code'] or "")

    def accept(self):
        user_id = self.user_combo.currentData()
        status_id = self.status_combo.currentData()
        pickup_id = self.pickup_combo.currentData()
        order_date = self.order_date_edit.date().toString("yyyy-MM-dd")
        delivery_date = self.delivery_date_edit.date().toString("yyyy-MM-dd")
        pickup_code = self.code_edit.text().strip()

        if self.order_id is None:
            # Вставка – генерируем номер заказа (максимальный +1)
            max_num = self.db.execute_query("SELECT COALESCE(MAX(order_number), 0) as max FROM orders")[0]['max']
            order_number = max_num + 1
            query = """
                INSERT INTO orders (order_number, user_id, order_status_id, order_date, delivery_date, pickup_point_id, pickup_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (order_number, user_id, status_id, order_date, delivery_date, pickup_id, pickup_code)
            self.db.execute_non_query(query, params)
        else:
            query = """
                UPDATE orders SET user_id=%s, order_status_id=%s, order_date=%s, delivery_date=%s, pickup_point_id=%s, pickup_code=%s
                WHERE id=%s
            """
            params = (user_id, status_id, order_date, delivery_date, pickup_id, pickup_code, self.order_id)
            self.db.execute_non_query(query, params)
        super().accept()