from PySide6.QtCore import QModelIndex
from PySide6.QtSql import QSqlTableModel
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont

class ProductsModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable("products_view")
        self.select()  # Загружаем все данные
        self.setHeaderData(0, 0, "ID")
        self.setHeaderData(1, 0, "Артикул")
        self.setHeaderData(2, 0, "Наименование")
        # ... и так далее для всех колонок, которые вы хотите показать

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        """Переопределяем метод для условного форматирования строк и ячеек"""
        if role == Qt.BackgroundRole:
            discount = self.data(self.index(index.row(), 7))  # Индекс колонки скидки
            quantity = self.data(self.index(index.row(), 8))  # Индекс колонки количества

            if discount > 15:
                return QColor("#2E8B57")  # Морская волна для скидки >15%
            if quantity == 0:
                return QColor("LightBlue")  # Голубой для нулевого остатка

        if role == Qt.FontRole:
            discount = self.data(self.index(index.row(), 7))
            if discount > 0:
                font = QFont()
                font.setStrikeOut(True)  # Зачеркиваем цену при скидке
                font.setBold(True)
                return font

        if role == Qt.ForegroundRole:
            discount = self.data(self.index(index.row(), 7))
            if discount > 0:
                return QColor("Red")  # Красный цвет для зачеркнутой цены

        return super().data(index, role)