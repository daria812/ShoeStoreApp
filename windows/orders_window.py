from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QScrollArea, QLabel, QPushButton, QFrame,
                               QComboBox, QDateEdit, QLineEdit, QMessageBox, QDialog)
from PySide6.QtCore import Qt, QDate
from database.db import Database

class OrdersWindow(QMainWindow):
    def __init__(self, role, parent=None):
        super().__init__(parent)
        self.role = role
        self.db = Database.instance()
        self.selected_order_id = None   # для хранения выбранного заказа
        self.current_cards = []         # список карточек для сброса выделения

        self.setWindowTitle("Заказы")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Панель кнопок (только для администратора)
        if self.role == "admin":
            btn_layout = QHBoxLayout()
            self.btn_add = QPushButton("Добавить заказ")
            self.btn_add.setStyleSheet("background-color: #00FA9A; padding: 6px;")
            self.btn_add.clicked.connect(self.add_order)
            btn_layout.addWidget(self.btn_add)

            self.btn_edit = QPushButton("Редактировать заказ")
            self.btn_edit.setStyleSheet("background-color: #00FA9A; padding: 6px;")
            self.btn_edit.clicked.connect(self.edit_selected_order)
            btn_layout.addWidget(self.btn_edit)

            self.btn_delete = QPushButton("Удалить заказ")
            self.btn_delete.setStyleSheet("background-color: #FFA07A; padding: 6px;")
            self.btn_delete.clicked.connect(self.delete_selected_order)
            btn_layout.addWidget(self.btn_delete)

            btn_layout.addStretch()
            main_layout.addLayout(btn_layout)

        # Прокручиваемая область для карточек заказов
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_widget = QWidget()
        self.orders_layout = QVBoxLayout(scroll_widget)
        self.orders_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(self.scroll_area)

        self.load_orders()

    def load_orders(self):
        # Очищаем старые карточки
        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.current_cards.clear()
        self.selected_order_id = None

        query = """
            SELECT o.id, o.order_number, u.full_name, os.name AS status,
                   o.order_date, o.delivery_date, p.address
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN order_statuses os ON o.order_status_id = os.id
            LEFT JOIN pickup_points p ON o.pickup_point_id = p.id
            ORDER BY o.order_date DESC
        """
        rows = self.db.execute_query(query)

        for order in rows:
            card = self.create_order_card(order)
            self.orders_layout.addWidget(card)
            self.current_cards.append((card, order['id']))

    def create_order_card(self, order):
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("border: 1px solid #ccc; border-radius: 8px; padding: 8px; margin: 4px; background-color: #FFFFFF;")
        main_layout = QHBoxLayout(card)

        # Левая часть: информация о заказе (текст)
        info_html = f"""
        <b>Артикул заказа:</b> {order['order_number']}<br>
        <b>Клиент:</b> {order['full_name']}<br>
        <b>Статус:</b> {order['status']}<br>
        <b>Дата заказа:</b> {order['order_date'] or '—'}<br>
        <b>Адрес выдачи:</b> {order['address'] or '—'}
        """
        info_label = QLabel(info_html)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setStyleSheet("color: #000000;")
        main_layout.addWidget(info_label, stretch=1)

        # Правая часть: дата доставки (отдельный блок)
        delivery_layout = QVBoxLayout()
        delivery_label = QLabel(f"<b>Доставка<br>{order['delivery_date'] or '—'}</b>")
        delivery_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        delivery_label.setStyleSheet("background-color: #7FFF00; border-radius: 8px; padding: 5px; font-size: 12px;")
        delivery_layout.addWidget(delivery_label)
        delivery_layout.addStretch()
        main_layout.addWidget(delivery_label)

        # Сделаем карточку кликабельной для выбора
        card.mousePressEvent = lambda event, oid=order['id']: self.select_card(oid)

        return card

    def select_card(self, order_id):
        # Сброс выделения всех карточек
        for card, oid in self.current_cards:
            card.setStyleSheet("border: 1px solid #ccc; border-radius: 8px; padding: 8px; margin: 4px; background-color: #FFFFFF;")
        # Выделяем выбранную
        for card, oid in self.current_cards:
            if oid == order_id:
                card.setStyleSheet("border: 2px solid #00FA9A; border-radius: 8px; padding: 8px; margin: 4px; background-color: #E0FFE0;")
                break
        self.selected_order_id = order_id

    def add_order(self):
        dialog = OrderDialog(parent=self)
        if dialog.exec():
            self.load_orders()

    def edit_selected_order(self):
        if self.selected_order_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для редактирования")
            return
        dialog = OrderDialog(self.selected_order_id, self)
        if dialog.exec():
            self.load_orders()

    def delete_selected_order(self):
        if self.selected_order_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для удаления")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить заказ? Все его позиции также будут удалены.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.execute_non_query("DELETE FROM orders WHERE id = %s", (self.selected_order_id,))
            self.load_orders()


class OrderDialog(QDialog):
    def __init__(self, order_id=None, parent=None):
        super().__init__(parent)
        self.order_id = order_id
        self.db = Database.instance()
        self.setWindowTitle("Добавление заказа" if order_id is None else "Редактирование заказа")
        self.resize(400, 350)

        layout = QVBoxLayout(self)

        # Артикул заказа (номер)
        layout.addWidget(QLabel("Артикул заказа:"))
        self.article_edit = QLineEdit()
        layout.addWidget(self.article_edit)

        # Статус заказа
        layout.addWidget(QLabel("Статус заказа:"))
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

        # Дата доставки
        layout.addWidget(QLabel("Дата доставки:"))
        self.delivery_date_edit = QDateEdit()
        self.delivery_date_edit.setCalendarPopup(True)
        self.delivery_date_edit.setDate(QDate.currentDate().addDays(7))
        layout.addWidget(self.delivery_date_edit)

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
        self.article_edit.setText(str(o['order_number']))
        idx = self.status_combo.findData(o['order_status_id'])
        if idx >= 0: self.status_combo.setCurrentIndex(idx)
        idx = self.pickup_combo.findData(o['pickup_point_id'])
        if idx >= 0: self.pickup_combo.setCurrentIndex(idx)
        if o['order_date']:
            self.order_date_edit.setDate(QDate.fromString(str(o['order_date']), "yyyy-MM-dd"))
        if o['delivery_date']:
            self.delivery_date_edit.setDate(QDate.fromString(str(o['delivery_date']), "yyyy-MM-dd"))

    def accept(self):
        article = self.article_edit.text().strip()
        if not article:
            QMessageBox.warning(self, "Ошибка", "Артикул заказа обязателен")
            return
        try:
            order_number = int(article)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Артикул должен быть числом")
            return

        status_id = self.status_combo.currentData()
        pickup_id = self.pickup_combo.currentData()
        order_date = self.order_date_edit.date().toString("yyyy-MM-dd")
        delivery_date = self.delivery_date_edit.date().toString("yyyy-MM-dd")

        if self.order_id is None:
            # При добавлении берём пользователя с ролью admin (id=1) или первого попавшегося
            users = self.db.execute_query("SELECT id FROM users LIMIT 1")
            user_id = users[0]['id'] if users else 1
            max_num = self.db.execute_query("SELECT COALESCE(MAX(order_number), 0) as max FROM orders")[0]['max']
            if order_number <= max_num:
                QMessageBox.warning(self, "Ошибка", "Такой артикул заказа уже существует")
                return
            query = """
                INSERT INTO orders (order_number, user_id, order_status_id, order_date, delivery_date, pickup_point_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (order_number, user_id, status_id, order_date, delivery_date, pickup_id)
            self.db.execute_non_query(query, params)
        else:
            query = """
                UPDATE orders SET order_number=%s, order_status_id=%s, order_date=%s, delivery_date=%s, pickup_point_id=%s
                WHERE id=%s
            """
            params = (order_number, status_id, order_date, delivery_date, pickup_id, self.order_id)
            self.db.execute_non_query(query, params)

        super().accept()