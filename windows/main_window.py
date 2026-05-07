from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                               QComboBox, QRadioButton, QPushButton, QFrame)
from PySide6.QtCore import Qt
from database.db import Database
from PySide6.QtWidgets import QMessageBox
import os
from PySide6.QtGui import QPixmap, QColor
class MainWindow(QMainWindow):
    def __init__(self, role, full_name):
        super().__init__()
        self.role = role
        self.full_name = full_name
        self.db = Database.instance()
        self.setWindowTitle("Магазин обуви")
        self.resize(1000, 600)

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Верхняя панель
        top = QHBoxLayout()
        top.addWidget(QLabel(f"Пользователь: {self.full_name}"))
        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.logout)
        top.addWidget(logout_btn)
        top.addStretch()
        main_layout.addLayout(top)

        # Кнопка "Заказы" для менеджера и админа
        if self.role in ("manager", "admin"):
            btn_orders = QPushButton("Заказы")
            btn_orders.clicked.connect(self.open_orders)
            top.addWidget(btn_orders)

        # Панель фильтров (только для manager/admin)
        if self.role in ("manager", "admin"):
            filter_frame = QFrame()
            filter_layout = QHBoxLayout(filter_frame)

            # Поиск
            filter_layout.addWidget(QLabel("Поиск:"))
            self.search_edit = QLineEdit()
            self.search_edit.textChanged.connect(self.load_products)
            filter_layout.addWidget(self.search_edit)

            # Фильтр по поставщику
            filter_layout.addWidget(QLabel("Поставщик:"))
            self.supplier_combo = QComboBox()
            self.supplier_combo.currentTextChanged.connect(self.load_products)
            filter_layout.addWidget(self.supplier_combo)

            # Сортировка
            self.sort_asc = QRadioButton("По возрастанию остатка")
            self.sort_desc = QRadioButton("По убыванию остатка")
            self.sort_asc.toggled.connect(self.load_products)
            self.sort_desc.toggled.connect(self.load_products)
            filter_layout.addWidget(self.sort_asc)
            filter_layout.addWidget(self.sort_desc)

            main_layout.addWidget(filter_frame)
        else:
            # Для гостя и клиента фильтры не показываем, но атрибуты создаём пустыми
            self.search_edit = None
            self.supplier_combo = None
            self.sort_asc = None
            self.sort_desc = None

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["ID", "Артикул", "Наименование", "Категория",
                                              "Производитель", "Поставщик", "Цена", "Скидка %",
                                              "Остаток", "Цена со скидкой"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.table)

        self.load_products()
        if self.role == "admin":
            admin_buttons = QHBoxLayout()
            self.btn_add = QPushButton("Добавить товар")
            self.btn_add.clicked.connect(self.add_product)
            self.btn_edit = QPushButton("Редактировать товар")
            self.btn_edit.clicked.connect(self.edit_product)
            self.btn_delete = QPushButton("Удалить товар")
            self.btn_delete.clicked.connect(self.delete_product)
            admin_buttons.addWidget(self.btn_add)
            admin_buttons.addWidget(self.btn_edit)
            admin_buttons.addWidget(self.btn_delete)
            main_layout.addLayout(admin_buttons)

            # Двойной клик по строке для редактирования
            self.table.doubleClicked.connect(self.edit_product)

    def open_orders(self):
        from windows.orders_window import OrdersWindow
        self.orders_win = OrdersWindow(self.role)
        self.orders_win.show()

    def add_product(self):
        from dialogs.product_dialog import ProductDialog
        dlg = ProductDialog(parent=self)
        if dlg.exec():
            self.load_products()  # обновить таблицу

    def edit_product(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для редактирования")
            return
        product_id = int(self.table.item(selected, 0).text())
        from dialogs.product_dialog import ProductDialog
        dlg = ProductDialog(product_id, self)
        if dlg.exec():
            self.load_products()

    def delete_product(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления")
            return
        product_id = int(self.table.item(selected, 0).text())
        # Проверка, есть ли товар в заказах
        check = self.db.execute_query("SELECT COUNT(*) as cnt FROM order_items WHERE product_id = %s", (product_id,))
        if check[0]['cnt'] > 0:
            QMessageBox.warning(self, "Ошибка", "Товар присутствует в заказах, удаление невозможно")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить товар?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Удаляем фото, если оно есть
            img = self.db.execute_query("SELECT image_path FROM products WHERE id=%s", (product_id,))
            if img and img[0]['image_path'] and os.path.exists(img[0]['image_path']):
                os.remove(img[0]['image_path'])
            self.db.execute_non_query("DELETE FROM products WHERE id=%s", (product_id,))
            self.load_products()


    def load_suppliers(self):
        suppliers = self.db.execute_query("SELECT DISTINCT supplier FROM products_view ORDER BY supplier")
        self.supplier_combo.clear()
        self.supplier_combo.addItem("Все поставщики")
        for row in suppliers:
            self.supplier_combo.addItem(row['supplier'])

    def load_products(self):
        conditions = []
        params = []
        if not hasattr(self, 'table'):
            print("Ошибка: self.table не создан!")
            return
        if self.role in ("manager", "admin"):
            search = self.search_edit.text().strip()
            if search:
                conditions.append("(name ILIKE %s OR description ILIKE %s OR article ILIKE %s OR manufacturer ILIKE %s OR supplier ILIKE %s)")
                search_param = f"%{search}%"
                params.extend([search_param]*5)
            supplier = self.supplier_combo.currentText()
            if supplier and supplier != "Все поставщики":
                conditions.append("supplier = %s")
                params.append(supplier)
        query = "SELECT * FROM products_view"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        # Сортировка
        if self.role in ("manager", "admin"):
            if self.sort_asc and self.sort_asc.isChecked():
                query += " ORDER BY quantity_in_stock ASC"
            elif self.sort_desc and self.sort_desc.isChecked():
                query += " ORDER BY quantity_in_stock DESC"
        rows = self.db.execute_query(query, params)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(row['article']))
            self.table.setItem(i, 2, QTableWidgetItem(row['name']))
            self.table.setItem(i, 3, QTableWidgetItem(row['category'] or ""))
            self.table.setItem(i, 4, QTableWidgetItem(row['manufacturer'] or ""))
            self.table.setItem(i, 5, QTableWidgetItem(row['supplier'] or ""))
            # Цена
            price_item = QTableWidgetItem(f"{row['price']:.2f}")
            # Скидка
            discount_item = QTableWidgetItem(f"{row['discount_percent']:.2f}")
            # Остаток
            qty_item = QTableWidgetItem(str(row['quantity_in_stock']))
            # Цена со скидкой
            final_item = QTableWidgetItem(f"{row['final_price']:.2f}")

            self.table.setItem(i, 6, price_item)
            self.table.setItem(i, 7, discount_item)
            self.table.setItem(i, 8, qty_item)
            self.table.setItem(i, 9, final_item)

            # Условное форматирование строки
            discount = row['discount_percent']
            qty = row['quantity_in_stock']
            if discount > 15:
                bg_color = QColor("#2E8B57")
                for col in range(self.table.columnCount()):
                    self.table.item(i, col).setBackground(bg_color)
            elif qty == 0:
                bg_color = QColor("LightBlue")
                for col in range(self.table.columnCount()):
                    self.table.item(i, col).setBackground(bg_color)

            # Зачёркивание цены, если есть скидка
            if discount > 0:
                font = price_item.font()
                font.setStrikeOut(True)
                font.setBold(True)
                price_item.setFont(font)
                price_item.setForeground(QColor("Red"))

        # Добавляем колонку фото, если её нет
        if self.table.columnCount() == 10:
            self.table.insertColumn(1)  # после ID
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Фото"))

        for i, row in enumerate(rows):
            # ... остальные ячейки сдвигаем на одну вправо
            # В i-й строке во второй колонке (индекс 1) размещаем QLabel с картинкой
            img_path = row['image_path']
            label = QLabel()
            if img_path and os.path.exists(img_path):
                pix = QPixmap(img_path)
                pix = pix.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(pix)
            else:
                label.setText("Нет фото")
                label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i, 1, label)

    def logout(self):
        self.close()
        from windows.login_window import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()