import os
import shutil
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QComboBox, QTextEdit, QPushButton,
                               QFileDialog, QMessageBox, QSpinBox, QDoubleSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from database.db import Database
from customtkinter import set_appearance_mode

class ProductDialog(QDialog):
    def __init__(self, product_id=None, parent=None):
        super().__init__(parent)
        set_appearance_mode("light")
        self.product_id = product_id  # None для добавления, иначе редактирование
        self.db = Database.instance()
        self.setWindowTitle("Добавление товара" if product_id is None else "Редактирование товара")
        self.resize(500, 600)

        layout = QVBoxLayout(self)

        # Поля формы
        # Артикул
        layout.addWidget(QLabel("Артикул:"))
        self.article_edit = QLineEdit()
        layout.addWidget(self.article_edit)

        # Наименование
        layout.addWidget(QLabel("Наименование:"))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        # Категория (выпадающий список)
        layout.addWidget(QLabel("Категория:"))
        self.category_combo = QComboBox()
        self.load_categories()
        layout.addWidget(self.category_combo)

        # Производитель (выпадающий список)
        layout.addWidget(QLabel("Производитель:"))
        self.manufacturer_combo = QComboBox()
        self.load_manufacturers()
        layout.addWidget(self.manufacturer_combo)

        # Поставщик (выпадающий список)
        layout.addWidget(QLabel("Поставщик:"))
        self.supplier_combo = QComboBox()
        self.load_suppliers()
        layout.addWidget(self.supplier_combo)

        # Единица измерения (выпадающий список)
        layout.addWidget(QLabel("Единица измерения:"))
        self.unit_combo = QComboBox()
        self.load_units()
        layout.addWidget(self.unit_combo)

        # Цена
        layout.addWidget(QLabel("Цена:"))
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0, 1000000)
        self.price_spin.setDecimals(2)
        layout.addWidget(self.price_spin)

        # Количество на складе
        layout.addWidget(QLabel("Количество на складе:"))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 1000000)
        layout.addWidget(self.quantity_spin)

        # Скидка (%)
        layout.addWidget(QLabel("Скидка (%):"))
        self.discount_spin = QSpinBox()
        self.discount_spin.setRange(0, 100)
        layout.addWidget(self.discount_spin)

        # Описание
        layout.addWidget(QLabel("Описание:"))
        self.description_edit = QTextEdit()
        layout.addWidget(self.description_edit)

        # Фото
        layout.addWidget(QLabel("Фото товара:"))
        photo_layout = QHBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setText("Нет фото")
        self.photo_path = None  # храним путь к файлу (относительный)
        self.photo_file_name = None  # имя файла
        photo_layout.addWidget(self.photo_label)
        btn_load = QPushButton("Загрузить фото")
        btn_load.clicked.connect(self.load_photo)
        photo_layout.addWidget(btn_load)
        layout.addLayout(photo_layout)

        # Кнопки OK/Cancel
        buttons = QHBoxLayout()
        btn_ok = QPushButton("Сохранить")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)

        if product_id is not None:
            self.load_product_data()

    def load_categories(self):
        rows = self.db.execute_query("SELECT id, name FROM categories ORDER BY name")
        for row in rows:
            self.category_combo.addItem(row['name'], row['id'])

    def load_manufacturers(self):
        rows = self.db.execute_query("SELECT id, name FROM manufacturers ORDER BY name")
        for row in rows:
            self.manufacturer_combo.addItem(row['name'], row['id'])

    def load_suppliers(self):
        rows = self.db.execute_query("SELECT id, name FROM suppliers ORDER BY name")
        for row in rows:
            self.supplier_combo.addItem(row['name'], row['id'])

    def load_units(self):
        rows = self.db.execute_query("SELECT id, name FROM units ORDER BY name")
        for row in rows:
            self.unit_combo.addItem(row['name'], row['id'])

    def load_product_data(self):
        query = "SELECT * FROM products WHERE id = %s"
        rows = self.db.execute_query(query, (self.product_id,))
        if not rows:
            return
        p = rows[0]
        self.article_edit.setText(p['article'])
        self.name_edit.setText(p['name'])
        self.description_edit.setText(p['description'] or "")
        self.price_spin.setValue(float(p['price']))
        self.quantity_spin.setValue(p['quantity_in_stock'])
        self.discount_spin.setValue(p['discount_percent'])

        # Установить выбранные элементы в комбобоксах
        idx = self.category_combo.findData(p['category_id'])
        if idx >= 0: self.category_combo.setCurrentIndex(idx)
        idx = self.manufacturer_combo.findData(p['manufacturer_id'])
        if idx >= 0: self.manufacturer_combo.setCurrentIndex(idx)
        idx = self.supplier_combo.findData(p['supplier_id'])
        if idx >= 0: self.supplier_combo.setCurrentIndex(idx)
        idx = self.unit_combo.findData(p['unit_id'])
        if idx >= 0: self.unit_combo.setCurrentIndex(idx)

        # Фото
        if p['image_path'] and os.path.exists(p['image_path']):
            pixmap = QPixmap(p['image_path'])
            pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)
            self.photo_path = p['image_path']
            self.photo_file_name = os.path.basename(p['image_path'])

    def load_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            # Проверяем размеры (300x200)
            pixmap = QPixmap(file_path)
            if pixmap.width() > 300 or pixmap.height() > 200:
                pixmap = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
            # Сохраняем в папку images (создаём если нет)
            images_dir = "images"
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            # Генерируем уникальное имя файла (можно использовать артикул или id, но проще по времени)
            ext = os.path.splitext(file_path)[1]
            new_name = f"product_{self.product_id or 'new'}_{os.path.basename(file_path)}"
            new_path = os.path.join(images_dir, new_name)
            shutil.copyfile(file_path, new_path)
            # Отображаем миниатюру
            thumb = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(thumb)
            self.photo_path = new_path
            self.photo_file_name = new_name


    def accept(self):
        # Проверка обязательных полей
        if not self.article_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Артикул обязателен")
            return
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Наименование обязательно")
            return

        # Собираем данные
        article = self.article_edit.text().strip()
        name = self.name_edit.text().strip()
        category_id = self.category_combo.currentData()
        manufacturer_id = self.manufacturer_combo.currentData()
        supplier_id = self.supplier_combo.currentData()
        unit_id = self.unit_combo.currentData()
        price = self.price_spin.value()
        quantity = self.quantity_spin.value()
        discount = self.discount_spin.value()
        description = self.description_edit.toPlainText().strip()
        image_path = self.photo_path if self.photo_path else None

        if self.product_id is None:
            # Вставка
            query = """
                INSERT INTO products (article, name, description, category_id, manufacturer_id, supplier_id, unit_id,
                                      price, discount_percent, quantity_in_stock, image_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (article, name, description, category_id, manufacturer_id, supplier_id, unit_id,
                      price, discount, quantity, image_path)
            self.db.execute_non_query(query, params)
        else:
            # Обновление
            query = """
                UPDATE products SET article=%s, name=%s, description=%s, category_id=%s, manufacturer_id=%s,
                       supplier_id=%s, unit_id=%s, price=%s, discount_percent=%s, quantity_in_stock=%s, image_path=%s
                WHERE id=%s
            """
            params = (article, name, description, category_id, manufacturer_id, supplier_id, unit_id,
                      price, discount, quantity, image_path, self.product_id)
            self.db.execute_non_query(query, params)

        super().accept()

    def reject(self):
        super().reject()