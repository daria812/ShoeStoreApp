from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QScrollArea, QLabel, QLineEdit,
                               QComboBox, QRadioButton, QPushButton, QFrame)
from PySide6.QtCore import Qt
from database.db import Database
from PySide6.QtWidgets import QMessageBox
import os
from PySide6.QtGui import QPixmap, QIcon
from dialogs.product_dialog import ProductDialog

class MainWindow(QMainWindow):
    def __init__(self, role, full_name):
        super().__init__()
        self.role = role
        self.full_name = full_name
        self.db = Database.instance()
        self.orders_win = None
        self.login_win = None
        self.setWindowTitle("Магазин обуви")
        self.resize(1000, 600)
        self.setStyleSheet("QMainWindow { background-color: #FFFFFF; }")

        icon_path = os.path.join(os.path.dirname(__file__), "..", "images", "Icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "images", "Icon.png")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        central.setStyleSheet("background-color: #FFFFFF;")

        # Верхняя панель
        top = QHBoxLayout()

        logo_path = os.path.join(os.path.dirname(__file__), "..", "images", "Icon.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(100, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            top.addWidget(logo_label)
        else:
            top.addWidget(QLabel("ЛОГО"))
        top.addStretch()
        top.addWidget(QLabel(f"Пользователь: {self.full_name}"))
        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.logout)
        top.addWidget(logout_btn)

        main_layout.addLayout(top)

        # Кнопка "Заказы" для менеджера и админа
        if self.role in ("manager", "admin"):
            btn_orders = QPushButton("Заказы")
            btn_orders.setStyleSheet("background-color: #00FA9A;")

            btn_orders.clicked.connect(self.open_orders)
            top.addWidget(btn_orders)

        # Прокручиваемая область для карточек товаров
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: #FFFFFF;")
        self.products_layout = QVBoxLayout(scroll_widget)
        self.products_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(self.scroll_area)

        # Панель фильтров (только для manager/admin)
        if self.role in ("manager", "admin"):
            filter_frame = QFrame()
            filter_frame.setStyleSheet("background-color: #7FFF00;")
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
            self.load_suppliers()
        else:
            # Для гостя и клиента фильтры не показываем, но атрибуты создаём пустыми
            self.search_edit = None
            self.supplier_combo = None
            self.sort_asc = None
            self.sort_desc = None


        self.load_products()
        if self.role == "admin":
            admin_buttons = QHBoxLayout()
            self.btn_add = QPushButton("Добавить товар")
            self.btn_add.clicked.connect(self.add_product)
            self.btn_edit = QPushButton("Редактировать товар")
            self.btn_edit.clicked.connect(self.edit_product)
            self.btn_delete = QPushButton("Удалить товар")
            self.btn_delete.clicked.connect(self.delete_product)
            self.btn_add.setStyleSheet("background-color: #00FA9A;")
            self.btn_edit.setStyleSheet("background-color: #00FA9A;")
            self.btn_delete.setStyleSheet("background-color: #FFA07A;")
            admin_buttons.addWidget(self.btn_add)
            admin_buttons.addWidget(self.btn_edit)
            admin_buttons.addWidget(self.btn_delete)
            main_layout.addLayout(admin_buttons)

    # noinspection PyMethodMayBeStatic
    def create_product_widget(self, product):
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("border: 1px solid #ccc; border-radius: 8px; padding: 8px; margin: 4px;")
        main_layout = QHBoxLayout(card)

        # Левая часть: фото (без изменений)
        photo_label = QLabel()
        photo_label.setFixedSize(120, 120)
        photo_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_path = product.get('image_path')
        if img_path and os.path.exists(img_path):
            pix = QPixmap(img_path)
            pix = pix.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            photo_label.setPixmap(pix)
        else:
            default_path = os.path.join(os.path.dirname(__file__), "..", "images", "picture.png")
            if os.path.exists(default_path):
                pix = QPixmap(default_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                photo_label.setPixmap(pix)
            else:
                photo_label.setText("Нет фото")
        main_layout.addWidget(photo_label)

        # Формируем цену с зачёркиванием (если есть скидка)
        price = product['price']
        discount = product['discount_percent']
        final_price = product['final_price']
        if discount > 0:
            price_html = f"<span style='text-decoration: line-through; color: red;'>{price:.2f}</span> <b>{final_price:.2f}</b>"
        else:
            price_html = f"{price:.2f}"

        # Текстовая информация БЕЗ строки о скидке
        html_text = f"""
        <b>{product.get('category', '')} | {product['name']}</b><br>
        <b>Описание товара:</b> {product.get('description', '')}<br>
        <b>Производитель:</b> {product.get('manufacturer', '')}<br>
        <b>Поставщик:</b> {product.get('supplier', '')}<br>
        <b>Цена:</b> {price_html}<br>
        <b>Единица измерения:</b> {product.get('unit', '')}<br>
        <b>Количество на складе:</b> {product['quantity_in_stock']}
        """
        info_label = QLabel(html_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)

        # Правая часть: информационный блок + отдельная ячейка для скидки
        right_layout = QHBoxLayout()
        right_layout.addWidget(info_label, stretch=1)  # текст занимает основное место

        # ---- ОТДЕЛЬНАЯ ЯЧЕЙКА ДЛЯ СКИДКИ ----

        discount_layout = QVBoxLayout()
        discount_label = QLabel(f"<b>Скидка<br>{discount}%</b>")
        discount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        discount_layout.addWidget(discount_label)
        discount_layout.addStretch()
        right_layout.addWidget(discount_label)

        main_layout.addLayout(right_layout, stretch=1)

        # Условный фон карточки (скидка >15% или остаток 0)
        if discount > 15:
            card.setStyleSheet(card.styleSheet() + "background-color: #2E8B57;")
        elif product['quantity_in_stock'] == 0:
            card.setStyleSheet(card.styleSheet() + "background-color: LightBlue;")

        return card

    def open_orders(self):
        from windows.orders_window import OrdersWindow
        self.orders_win = OrdersWindow(self.role)
        self.orders_win.show()

    def add_product(self):
        from dialogs.product_dialog import ProductDialog
        dlg = ProductDialog(parent=self)
        if dlg.exec():
            self.load_products()  # обновить таблицу

    def edit_product(self, product_id=None):
        if product_id is None:
            # Вызов из кнопки "Добавить товар" (без id)
            dlg = ProductDialog(parent=self)
        else:
            dlg = ProductDialog(product_id, self)
        if dlg.exec():
            self.load_products()

    def delete_product(self, product_id):
        # Проверка, есть ли товар в заказах
        check = self.db.execute_query("SELECT COUNT(*) as cnt FROM order_items WHERE product_id = %s", (product_id,))
        if check and check[0]['cnt'] > 0:
            QMessageBox.warning(self, "Ошибка", "Товар присутствует в заказах, удаление невозможно")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить товар?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Удалить фото, если есть
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
        # Очищаем старые карточки
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for product in rows:
            widget = self.create_product_widget(product)
            self.products_layout.addWidget(widget)

    def logout(self):
        self.close()
        from windows.login_window import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()