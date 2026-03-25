import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette

# ===================== 全局样式 =====================
STYLE_SHEET = """
QMainWindow {
    background-color: #f5f0eb;
}
QWidget {
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", sans-serif;
}

/* ---- 登录页 ---- */
#loginCard {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #ffffff, stop:1 #faf7f4);
    border-radius: 16px;
    border: 1px solid #e8e0d8;
}
#loginTitle {
    font-size: 22px;
    font-weight: bold;
    color: #3a3a3a;
}
#loginSubtitle {
    font-size: 12px;
    color: #999;
}

/* ---- 通用输入框 ---- */
QLineEdit {
    border: 1px solid #d4ccc4;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    background: #fff;
    color: #333;
    min-height: 18px;
}
QLineEdit:focus {
    border: 2px solid #b08968;
}
QLineEdit:read-only {
    background: #f5f0eb;
    color: #888;
}

/* ---- 按钮 ---- */
QPushButton {
    border: none;
    border-radius: 8px;
    padding: 9px 22px;
    font-size: 13px;
    font-weight: bold;
    color: #fff;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #b08968, stop:1 #c9a887);
    min-height: 18px;
}
QPushButton:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #9c7555, stop:1 #b8956f);
}
QPushButton:pressed {
    background: #8a6644;
}
QPushButton#dangerBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #d96b6b, stop:1 #e88a8a);
}
QPushButton#dangerBtn:hover {
    background: #c55050;
}
QPushButton#secondaryBtn {
    background: #e8e0d8;
    color: #6b5b4e;
}
QPushButton#secondaryBtn:hover {
    background: #d9cfc5;
}
QPushButton#stockInBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #5a9e6f, stop:1 #7aba8e);
    min-height: 24px;
    font-size: 14px;
}
QPushButton#stockInBtn:hover {
    background: #4a8a5e;
}
QPushButton#stockOutBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #d96b6b, stop:1 #e88a8a);
    min-height: 24px;
    font-size: 14px;
}
QPushButton#stockOutBtn:hover {
    background: #c55050;
}

/* ---- 表格 ---- */
QTableWidget {
    background: #fff;
    border: 1px solid #e0d8d0;
    border-radius: 10px;
    gridline-color: #f0ebe6;
    font-size: 13px;
    selection-background-color: #f5ece3;
    selection-color: #3a3a3a;
}
QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #f0ebe6;
}
QHeaderView::section {
    background: #f9f5f1;
    color: #6b5b4e;
    font-weight: bold;
    font-size: 12px;
    padding: 8px 10px;
    border: none;
    border-bottom: 2px solid #e0d8d0;
}

/* ---- 选项卡 ---- */
QTabWidget::pane {
    border: 1px solid #e0d8d0;
    border-radius: 10px;
    background: #fff;
    top: -1px;
}
QTabBar::tab {
    background: #e8e0d8;
    color: #6b5b4e;
    font-size: 13px;
    font-weight: bold;
    padding: 10px 28px;
    margin-right: 4px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
QTabBar::tab:selected {
    background: #fff;
    color: #b08968;
    border-bottom: 2px solid #b08968;
}
QTabBar::tab:hover:!selected {
    background: #f0e8e0;
}

/* ---- 下拉框 ---- */
QComboBox {
    border: 1px solid #d4ccc4;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    background: #fff;
    color: #333;
    min-height: 18px;
}
QComboBox:focus {
    border: 2px solid #b08968;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
}
QComboBox QAbstractItemView {
    background: #fff;
    border: 1px solid #d4ccc4;
    border-radius: 6px;
    selection-background-color: #f5ece3;
    selection-color: #333;
}

/* ---- 分组框 ---- */
QGroupBox {
    font-size: 14px;
    font-weight: bold;
    color: #6b5b4e;
    border: 1px solid #e0d8d0;
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 18px;
    background: #fdfbf9;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
}

/* ---- 标签 ---- */
QLabel {
    color: #555;
    font-size: 13px;
}
QLabel#sectionTitle {
    font-size: 15px;
    font-weight: bold;
    color: #6b5b4e;
}
QLabel#statNumber {
    font-size: 28px;
    font-weight: bold;
    color: #b08968;
}
QLabel#statLabel {
    font-size: 11px;
    color: #999;
}

/* ---- 搜索框 ---- */
QLineEdit#searchInput {
    border: 1px solid #d4ccc4;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    background: #fff;
}

/* ---- 消息框 ---- */
QMessageBox {
    background: #fff;
}
QMessageBox QLabel {
    font-size: 13px;
    color: #333;
}
"""

# ===================== 数据库操作类 =====================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('clothing_db.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # 用户表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # 服装商品表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clothing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                brand TEXT,
                size TEXT,
                color TEXT,
                season TEXT,
                stock INTEGER DEFAULT 0,
                cost_price REAL DEFAULT 0,
                sell_price REAL DEFAULT 0
            )
        ''')
        # 默认管理员
        self.cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users (username,password) VALUES (?,?)", ("admin", "123456"))
        self.conn.commit()

    def check_login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def add_clothing(self, name, category, brand, size, color, season, stock, cost_price, sell_price):
        self.cursor.execute(
            "INSERT INTO clothing (name,category,brand,size,color,season,stock,cost_price,sell_price) VALUES (?,?,?,?,?,?,?,?,?)",
            (name, category, brand, size, color, season, stock, cost_price, sell_price))
        self.conn.commit()

    def update_clothing(self, id_, name, category, brand, size, color, season, stock, cost_price, sell_price):
        self.cursor.execute(
            "UPDATE clothing SET name=?,category=?,brand=?,size=?,color=?,season=?,stock=?,cost_price=?,sell_price=? WHERE id=?",
            (name, category, brand, size, color, season, stock, cost_price, sell_price, id_))
        self.conn.commit()

    def delete_clothing(self, id_):
        self.cursor.execute("DELETE FROM clothing WHERE id=?", (id_,))
        self.conn.commit()

    def get_all_clothing(self):
        self.cursor.execute("SELECT * FROM clothing")
        return self.cursor.fetchall()

    def search_clothing(self, keyword):
        query = "SELECT * FROM clothing WHERE name LIKE ? OR category LIKE ? OR brand LIKE ? OR color LIKE ?"
        pattern = f"%{keyword}%"
        self.cursor.execute(query, (pattern, pattern, pattern, pattern))
        return self.cursor.fetchall()

    def update_stock(self, id_, num):
        self.cursor.execute("SELECT stock FROM clothing WHERE id=?", (id_,))
        row = self.cursor.fetchone()
        if row is None:
            return False
        new_stock = row[0] + num
        if new_stock < 0:
            return False
        self.cursor.execute("UPDATE clothing SET stock=? WHERE id=?", (new_stock, id_))
        self.conn.commit()
        return True

    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*), COALESCE(SUM(stock),0) FROM clothing")
        count, total_stock = self.cursor.fetchone()
        self.cursor.execute("SELECT COUNT(*) FROM clothing WHERE stock <= 5")
        low_stock = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(DISTINCT category) FROM clothing")
        categories = self.cursor.fetchone()[0]
        return count, total_stock, low_stock, categories


# ===================== 登录窗口 =====================
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('服装库存管理系统')
        self.setFixedSize(420, 480)
        self.setStyleSheet("background-color: #f5f0eb;")

        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setAlignment(Qt.AlignCenter)

        # 登录卡片
        card = QWidget()
        card.setObjectName('loginCard')
        card.setFixedSize(340, 380)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(36, 36, 36, 36)

        # Logo 区域
        logo_label = QLabel('👗')
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet('font-size: 48px; border: none;')
        card_layout.addWidget(logo_label)

        title = QLabel('服装库存管理系统')
        title.setObjectName('loginTitle')
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel('Clothing Inventory Management')
        subtitle.setObjectName('loginSubtitle')
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(10)

        # 账号
        user_label = QLabel('👤  账号')
        user_label.setStyleSheet('font-size: 12px; color: #888;')
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText('请输入账号')
        self.user_input.setText('admin')
        card_layout.addWidget(user_label)
        card_layout.addWidget(self.user_input)

        # 密码
        pwd_label = QLabel('🔒  密码')
        pwd_label.setStyleSheet('font-size: 12px; color: #888;')
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText('请输入密码')
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setText('123456')
        card_layout.addWidget(pwd_label)
        card_layout.addWidget(self.pwd_input)

        card_layout.addSpacing(8)

        # 登录按钮
        self.login_btn = QPushButton('登  录')
        self.login_btn.setStyleSheet('''
            QPushButton {
                min-height: 24px; font-size: 15px; font-weight: bold;
                border-radius: 10px;
            }
        ''')
        self.login_btn.clicked.connect(self.login)
        self.pwd_input.returnPressed.connect(self.login)
        card_layout.addWidget(self.login_btn)

        card_layout.addStretch()
        outer.addWidget(card)

    def login(self):
        username = self.user_input.text().strip()
        password = self.pwd_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, '提示', '请输入账号和密码')
            return
        if self.db.check_login(username, password):
            self.main_win = MainWindow(username)
            self.main_win.show()
            self.close()
        else:
            QMessageBox.warning(self, '登录失败', '账号或密码错误，请重试')


# ===================== 主功能窗口 =====================
class MainWindow(QMainWindow):
    CATEGORIES = ['上衣', '裤装', '裙装', '外套', '内衣', '鞋履', '配饰', '其他']
    SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', '均码']
    SEASONS = ['春季', '夏季', '秋季', '冬季', '四季通用']
    COLUMNS = ['ID', '名称', '分类', '品牌', '尺码', '颜色', '季节', '库存', '进价(¥)', '售价(¥)']

    def __init__(self, username='admin'):
        super().__init__()
        self.db = Database()
        self.username = username
        self.init_ui()
        self.load_clothing()

    def init_ui(self):
        self.setWindowTitle('服装库存管理系统')
        self.setMinimumSize(1080, 680)
        self.resize(1160, 720)

        # 主布局
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 12, 20, 12)
        main_layout.setSpacing(10)

        # ---- 顶部栏 ----
        header = QHBoxLayout()
        app_title = QLabel('👗 服装库存管理系统')
        app_title.setStyleSheet('font-size: 20px; font-weight: bold; color: #3a3a3a;')
        header.addWidget(app_title)
        header.addStretch()
        user_label = QLabel(f'👤 {self.username}')
        user_label.setStyleSheet('font-size: 13px; color: #888; margin-right: 8px;')
        header.addWidget(user_label)
        main_layout.addLayout(header)

        # ---- 统计卡片 ----
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(14)
        self.stat_total = self._make_stat_card('商品总数', '0', '#b08968')
        self.stat_stock = self._make_stat_card('总库存量', '0', '#5a9e6f')
        self.stat_low = self._make_stat_card('低库存预警', '0', '#d96b6b')
        self.stat_cats = self._make_stat_card('分类数', '0', '#6b8fb0')
        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_stock)
        stats_layout.addWidget(self.stat_low)
        stats_layout.addWidget(self.stat_cats)
        main_layout.addLayout(stats_layout)

        # ---- 选项卡 ----
        self.tab = QTabWidget()
        self.tab.addTab(self._create_clothing_tab(), '📦  商品管理')
        self.tab.addTab(self._create_stock_tab(), '🔄  出入库管理')
        main_layout.addWidget(self.tab, 1)

    # ---------- 统计卡片 ----------
    def _make_stat_card(self, label_text, number, color):
        card = QWidget()
        card.setStyleSheet(f'''
            QWidget {{
                background: #fff;
                border-radius: 12px;
                border: 1px solid #eee;
            }}
        ''')
        card.setFixedHeight(88)
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(2)
        num = QLabel(number)
        num.setObjectName('statNumber')
        num.setAlignment(Qt.AlignCenter)
        num.setStyleSheet(f'font-size: 28px; font-weight: bold; color: {color}; border: none;')
        lbl = QLabel(label_text)
        lbl.setObjectName('statLabel')
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet('font-size: 11px; color: #999; border: none;')
        layout.addWidget(num)
        layout.addWidget(lbl)
        card._num_label = num
        return card

    def _update_stats(self):
        count, total_stock, low, cats = self.db.get_stats()
        self.stat_total._num_label.setText(str(count))
        self.stat_stock._num_label.setText(str(total_stock))
        self.stat_low._num_label.setText(str(low))
        self.stat_cats._num_label.setText(str(cats))

    # ---------- 商品管理标签 ----------
    def _create_clothing_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(16)

        # ── 左侧表单 ──
        left_panel = QWidget()
        left_panel.setStyleSheet('background: #fdfbf9; border-radius: 12px; border: 1px solid #eee;')
        left_panel.setFixedWidth(300)
        form_outer = QVBoxLayout(left_panel)
        form_outer.setContentsMargins(20, 16, 20, 16)
        form_outer.setSpacing(10)

        form_title = QLabel('商品信息')
        form_title.setObjectName('sectionTitle')
        form_title.setStyleSheet('font-size: 15px; font-weight: bold; color: #6b5b4e; border: none;')
        form_outer.addWidget(form_title)

        form = QFormLayout()
        form.setSpacing(8)
        form.setLabelAlignment(Qt.AlignRight)

        self.c_id = QLineEdit()
        self.c_id.setReadOnly(True)
        self.c_id.setPlaceholderText('自动生成')
        self.c_name = QLineEdit()
        self.c_name.setPlaceholderText('输入服装名称')
        self.c_category = QComboBox()
        self.c_category.addItems(self.CATEGORIES)
        self.c_brand = QLineEdit()
        self.c_brand.setPlaceholderText('输入品牌')
        self.c_size = QComboBox()
        self.c_size.addItems(self.SIZES)
        self.c_color = QLineEdit()
        self.c_color.setPlaceholderText('输入颜色')
        self.c_season = QComboBox()
        self.c_season.addItems(self.SEASONS)
        self.c_stock = QLineEdit()
        self.c_stock.setPlaceholderText('0')
        self.c_cost = QLineEdit()
        self.c_cost.setPlaceholderText('0.00')
        self.c_price = QLineEdit()
        self.c_price.setPlaceholderText('0.00')

        form.addRow('ID：', self.c_id)
        form.addRow('名称：', self.c_name)
        form.addRow('分类：', self.c_category)
        form.addRow('品牌：', self.c_brand)
        form.addRow('尺码：', self.c_size)
        form.addRow('颜色：', self.c_color)
        form.addRow('季节：', self.c_season)
        form.addRow('库存：', self.c_stock)
        form.addRow('进价(¥)：', self.c_cost)
        form.addRow('售价(¥)：', self.c_price)
        form_outer.addLayout(form)

        form_outer.addSpacing(8)

        # 按钮
        btn_row1 = QHBoxLayout()
        self.add_btn = QPushButton('✚ 新增')
        self.update_btn = QPushButton('✎ 修改')
        self.update_btn.setObjectName('secondaryBtn')
        btn_row1.addWidget(self.add_btn)
        btn_row1.addWidget(self.update_btn)
        form_outer.addLayout(btn_row1)

        btn_row2 = QHBoxLayout()
        self.del_btn = QPushButton('✕ 删除')
        self.del_btn.setObjectName('dangerBtn')
        self.clear_btn = QPushButton('↺ 清空')
        self.clear_btn.setObjectName('secondaryBtn')
        btn_row2.addWidget(self.del_btn)
        btn_row2.addWidget(self.clear_btn)
        form_outer.addLayout(btn_row2)

        self.add_btn.clicked.connect(self.add_clothing)
        self.update_btn.clicked.connect(self.update_clothing)
        self.del_btn.clicked.connect(self.delete_clothing)
        self.clear_btn.clicked.connect(self.clear_form)

        form_outer.addStretch()

        # ── 右侧表格 ──
        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)

        # 搜索栏
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setObjectName('searchInput')
        self.search_input.setPlaceholderText('🔍  搜索名称 / 分类 / 品牌 / 颜色 ...')
        self.search_input.textChanged.connect(self.search_clothing)
        search_row.addWidget(self.search_input)
        right_panel.addLayout(search_row)

        # 表格
        self.clothing_table = QTableWidget()
        self.clothing_table.setColumnCount(10)
        self.clothing_table.setHorizontalHeaderLabels(self.COLUMNS)
        self.clothing_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.clothing_table.setSelectionMode(QTableWidget.SingleSelection)
        self.clothing_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.clothing_table.setAlternatingRowColors(True)
        self.clothing_table.setStyleSheet('''
            QTableWidget { alternate-background-color: #faf7f4; }
        ''')
        self.clothing_table.horizontalHeader().setStretchLastSection(True)
        self.clothing_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.clothing_table.verticalHeader().setVisible(False)
        self.clothing_table.cellClicked.connect(self.select_clothing)
        right_panel.addWidget(self.clothing_table, 1)

        layout.addWidget(left_panel)
        layout.addLayout(right_panel, 1)
        return widget

    # ---------- 出入库标签 ----------
    def _create_stock_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        title = QLabel('出入库操作')
        title.setObjectName('sectionTitle')
        title.setStyleSheet('font-size: 16px; font-weight: bold; color: #6b5b4e;')
        layout.addWidget(title)

        # 操作卡片
        card = QWidget()
        card.setStyleSheet('background: #fdfbf9; border-radius: 12px; border: 1px solid #eee;')
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 24, 32, 24)
        card_layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)
        self.stock_id = QLineEdit()
        self.stock_id.setPlaceholderText('输入商品 ID')
        self.stock_num = QLineEdit()
        self.stock_num.setPlaceholderText('输入数量')
        form.addRow('商品 ID：', self.stock_id)
        form.addRow('操作数量：', self.stock_num)
        card_layout.addLayout(form)

        hint = QLabel('💡 入库填正数，出库填正数后点"出库"按钮')
        hint.setStyleSheet('color: #b08968; font-size: 12px; border: none;')
        card_layout.addWidget(hint)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)
        self.in_btn = QPushButton('📥  入库')
        self.in_btn.setObjectName('stockInBtn')
        self.out_btn = QPushButton('📤  出库')
        self.out_btn.setObjectName('stockOutBtn')
        self.in_btn.clicked.connect(lambda: self.operate_stock(1))
        self.out_btn.clicked.connect(lambda: self.operate_stock(-1))
        btn_row.addWidget(self.in_btn)
        btn_row.addWidget(self.out_btn)
        card_layout.addLayout(btn_row)

        layout.addWidget(card)
        layout.addStretch()
        return widget

    # ---------- 数据操作 ----------
    def load_clothing(self):
        data = self.db.get_all_clothing()
        self._fill_table(data)
        self._update_stats()

    def _fill_table(self, data):
        self.clothing_table.setRowCount(len(data))
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                cell = QTableWidgetItem(str(value))
                cell.setTextAlignment(Qt.AlignCenter)
                # 低库存高亮
                if col == 7 and isinstance(value, int) and value <= 5:
                    cell.setForeground(QColor('#d96b6b'))
                    cell.setFont(QFont("", -1, QFont.Bold))
                self.clothing_table.setItem(row, col, cell)
        self.clothing_table.resizeColumnsToContents()

    def search_clothing(self, text):
        keyword = text.strip()
        data = self.db.search_clothing(keyword) if keyword else self.db.get_all_clothing()
        self._fill_table(data)

    def select_clothing(self, row):
        table = self.clothing_table
        self.c_id.setText(table.item(row, 0).text())
        self.c_name.setText(table.item(row, 1).text())
        # 设置下拉框
        cat = table.item(row, 2).text()
        idx = self.c_category.findText(cat)
        self.c_category.setCurrentIndex(idx if idx >= 0 else 0)
        self.c_brand.setText(table.item(row, 3).text())
        sz = table.item(row, 4).text()
        idx = self.c_size.findText(sz)
        self.c_size.setCurrentIndex(idx if idx >= 0 else 0)
        self.c_color.setText(table.item(row, 5).text())
        se = table.item(row, 6).text()
        idx = self.c_season.findText(se)
        self.c_season.setCurrentIndex(idx if idx >= 0 else 0)
        self.c_stock.setText(table.item(row, 7).text())
        self.c_cost.setText(table.item(row, 8).text())
        self.c_price.setText(table.item(row, 9).text())

    def clear_form(self):
        for w in [self.c_id, self.c_name, self.c_brand, self.c_color, self.c_stock, self.c_cost, self.c_price]:
            w.clear()
        self.c_category.setCurrentIndex(0)
        self.c_size.setCurrentIndex(0)
        self.c_season.setCurrentIndex(0)

    def add_clothing(self):
        name = self.c_name.text().strip()
        if not name:
            QMessageBox.warning(self, '提示', '请输入服装名称')
            return
        self.db.add_clothing(
            name, self.c_category.currentText(), self.c_brand.text().strip(),
            self.c_size.currentText(), self.c_color.text().strip(),
            self.c_season.currentText(),
            int(self.c_stock.text() or 0),
            float(self.c_cost.text() or 0),
            float(self.c_price.text() or 0))
        self.load_clothing()
        self.clear_form()
        QMessageBox.information(self, '成功', '服装商品已添加！')

    def update_clothing(self):
        if not self.c_id.text():
            QMessageBox.warning(self, '提示', '请先选择要修改的商品')
            return
        self.db.update_clothing(
            int(self.c_id.text()),
            self.c_name.text().strip(), self.c_category.currentText(),
            self.c_brand.text().strip(), self.c_size.currentText(),
            self.c_color.text().strip(), self.c_season.currentText(),
            int(self.c_stock.text() or 0),
            float(self.c_cost.text() or 0),
            float(self.c_price.text() or 0))
        self.load_clothing()
        QMessageBox.information(self, '成功', '商品信息已更新！')

    def delete_clothing(self):
        if not self.c_id.text():
            QMessageBox.warning(self, '提示', '请先选择要删除的商品')
            return
        reply = QMessageBox.question(self, '确认删除',
            f'确定要删除商品 ID={self.c_id.text()} 吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_clothing(int(self.c_id.text()))
            self.load_clothing()
            self.clear_form()
            QMessageBox.information(self, '成功', '商品已删除！')

    def operate_stock(self, direction):
        id_text = self.stock_id.text().strip()
        num_text = self.stock_num.text().strip()
        if not id_text or not num_text:
            QMessageBox.warning(self, '提示', '请输入商品 ID 和操作数量')
            return
        num = abs(int(num_text)) * direction
        if self.db.update_stock(int(id_text), num):
            self.load_clothing()
            op = '入库' if direction > 0 else '出库'
            QMessageBox.information(self, '成功', f'{op} {abs(num)} 件完成！')
            self.stock_id.clear()
            self.stock_num.clear()
        else:
            QMessageBox.warning(self, '失败', '库存不足，出库失败！')


# ===================== 程序入口 =====================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())