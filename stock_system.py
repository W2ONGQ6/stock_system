import sys
import sqlite3
import os
from datetime import date
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QDate
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
    border-radius: 18px;
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
    padding: 6px 10px;
    font-size: 13px;
    background: #fff;
    color: #333;
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
    padding: 8px 18px;
    font-size: 13px;
    font-weight: bold;
    color: #fff;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #7a5c3e, stop:1 #96754e);
}
QPushButton:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #6b4f33, stop:1 #866740);
}
QPushButton:pressed {
    background: #5a4028;
}
QPushButton#dangerBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #d96b6b, stop:1 #e88a8a);
    color: #fff;
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
QPushButton#returnBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #3d8455, stop:1 #5a9e6f);
    color: #fff;
    min-height: 22px;
    font-size: 14px;
}
QPushButton#returnBtn:hover {
    background: #347348;
}
QPushButton#compensateBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #b07820, stop:1 #c88a30);
    color: #fff;
    min-height: 22px;
    font-size: 14px;
}
QPushButton#compensateBtn:hover {
    background: #9a6818;
}
QPushButton#stockInBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #3d8455, stop:1 #5a9e6f);
    min-height: 22px;
    font-size: 14px;
    color: #fff;
}
QPushButton#stockInBtn:hover {
    background: #347348;
}
QPushButton#stockOutBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #c55050, stop:1 #d96b6b);
    min-height: 22px;
    font-size: 14px;
    color: #fff;
}
QPushButton#stockOutBtn:hover {
    background: #b04040;
}

/* ---- 左侧面板 ---- */
#stockLeftPanel {
    background: #fdfbf9;
    border-radius: 12px;
    border: 1px solid #e8e0d8;
}
#stockLeftPanel QLabel {
    border: none;
    background: transparent;
}
#stockLeftPanel QPushButton {
    border: none;
}
#clothingLeftPanel {
    background: #fdfbf9;
    border-radius: 12px;
    border: 1px solid #e8e0d8;
}
#clothingLeftPanel QLabel {
    border: none;
    background: transparent;
}
#clothingLeftPanel QPushButton {
    border: none;
}

/* ---- 日期选择器 ---- */
QDateEdit {
    border: 1px solid #d4ccc4;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
    background: #fff;
    color: #333;
}
QDateEdit:focus {
    border: 2px solid #b08968;
}
QDateEdit::drop-down {
    border: none;
    width: 24px;
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
    padding: 5px 8px;
    border-bottom: 1px solid #f0ebe6;
}
QHeaderView::section {
    background: #f9f5f1;
    color: #6b5b4e;
    font-weight: bold;
    font-size: 12px;
    padding: 7px 8px;
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
    font-size: 14px;
    font-weight: bold;
    padding: 10px 40px;
    margin-right: 4px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    min-width: 120px;
}
QTabBar::tab:selected {
    background: #fff;
    color: #b08968;
    border-bottom: 3px solid #b08968;
}
QTabBar::tab:hover:!selected {
    background: #f0e8e0;
}

/* ---- 下拉框 ---- */
QComboBox {
    border: 1px solid #d4ccc4;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
    background: #fff;
    color: #333;
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
    border: none;
}
QLabel#statNumber {
    font-size: 28px;
    font-weight: bold;
    color: #b08968;
    border: none;
}
QLabel#statLabel {
    font-size: 11px;
    color: #999;
    border: none;
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
                code TEXT DEFAULT '',
                name TEXT NOT NULL,
                category TEXT,
                brand TEXT,
                size TEXT,
                color TEXT,
                season TEXT,
                stock INTEGER DEFAULT 0,
                cost_price REAL DEFAULT 0
            )
        ''')
        # 兼容旧数据库：如果 clothing 表没有 code 列则添加
        try:
            self.cursor.execute("SELECT code FROM clothing LIMIT 1")
        except sqlite3.OperationalError:
            self.cursor.execute("ALTER TABLE clothing ADD COLUMN code TEXT DEFAULT ''")
        # 出入库记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clothing_id INTEGER NOT NULL,
                clothing_name TEXT,
                department TEXT DEFAULT '',
                team_name TEXT DEFAULT '',
                host_operator TEXT DEFAULT '',
                anchor_name TEXT DEFAULT '',
                contact TEXT DEFAULT '',
                record_date TEXT,
                quantity INTEGER DEFAULT 0,
                direction INTEGER DEFAULT -1,
                status TEXT DEFAULT '借出',
                compensate_amount REAL DEFAULT 0,
                remark TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now','localtime')),
                return_date TEXT DEFAULT '',
                FOREIGN KEY (clothing_id) REFERENCES clothing(id)
            )
        ''')
        # 兼容旧数据库：如果 stock_records 表没有 return_date 列则添加
        try:
            self.cursor.execute("SELECT return_date FROM stock_records LIMIT 1")
        except sqlite3.OperationalError:
            self.cursor.execute("ALTER TABLE stock_records ADD COLUMN return_date TEXT DEFAULT ''")
        # 默认管理员
        self.cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users (username,password) VALUES (?,?)", ("admin", "123456"))
        self.conn.commit()

    def check_login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def add_clothing(self, code, name, category, brand, size, color, season, stock, cost_price):
        self.cursor.execute(
            "INSERT INTO clothing (code,name,category,brand,size,color,season,stock,cost_price) VALUES (?,?,?,?,?,?,?,?,?)",
            (code, name, category, brand, size, color, season, stock, cost_price))
        self.conn.commit()

    def update_clothing(self, id_, code, name, category, brand, size, color, season, stock, cost_price):
        self.cursor.execute(
            "UPDATE clothing SET code=?,name=?,category=?,brand=?,size=?,color=?,season=?,stock=?,cost_price=? WHERE id=?",
            (code, name, category, brand, size, color, season, stock, cost_price, id_))
        self.conn.commit()

    def delete_clothing(self, id_):
        self.cursor.execute("DELETE FROM clothing WHERE id=?", (id_,))
        self.conn.commit()

    def get_all_clothing(self):
        self.cursor.execute("SELECT id,code,name,category,brand,size,color,season,stock,cost_price FROM clothing")
        return self.cursor.fetchall()

    def search_clothing(self, keyword):
        query = "SELECT id,code,name,category,brand,size,color,season,stock,cost_price FROM clothing WHERE name LIKE ? OR code LIKE ? OR category LIKE ? OR brand LIKE ? OR color LIKE ?"
        pattern = f"%{keyword}%"
        self.cursor.execute(query, (pattern, pattern, pattern, pattern, pattern))
        return self.cursor.fetchall()

    def find_clothing_by_code(self, code):
        self.cursor.execute("SELECT id, name, stock FROM clothing WHERE code=?", (code,))
        return self.cursor.fetchone()

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

    # ---- 出入库记录 ----
    def add_stock_record(self, clothing_id, clothing_name, department, team_name,
                         host_operator, anchor_name, contact, record_date,
                         quantity, direction, status, remark):
        self.cursor.execute('''
            INSERT INTO stock_records
            (clothing_id, clothing_name, department, team_name, host_operator,
             anchor_name, contact, record_date, quantity, direction, status, remark)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (clothing_id, clothing_name, department, team_name, host_operator,
              anchor_name, contact, record_date, quantity, direction, status, remark))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_stock_records(self):
        self.cursor.execute('''
            SELECT sr.id, COALESCE(c.code,''), sr.clothing_name, sr.department, sr.team_name,
                   sr.host_operator, sr.anchor_name, sr.contact, sr.record_date,
                   sr.quantity, sr.direction, sr.status, sr.compensate_amount, sr.remark,
                   sr.created_at, COALESCE(sr.return_date,'')
            FROM stock_records sr LEFT JOIN clothing c ON sr.clothing_id = c.id
            ORDER BY sr.id DESC
        ''')
        return self.cursor.fetchall()

    def search_stock_records(self, keyword):
        pattern = f"%{keyword}%"
        self.cursor.execute('''
            SELECT sr.id, COALESCE(c.code,''), sr.clothing_name, sr.department, sr.team_name,
                   sr.host_operator, sr.anchor_name, sr.contact, sr.record_date,
                   sr.quantity, sr.direction, sr.status, sr.compensate_amount, sr.remark,
                   sr.created_at, COALESCE(sr.return_date,'')
            FROM stock_records sr LEFT JOIN clothing c ON sr.clothing_id = c.id
            WHERE sr.clothing_name LIKE ? OR c.code LIKE ? OR sr.department LIKE ? OR sr.team_name LIKE ?
               OR sr.host_operator LIKE ? OR sr.anchor_name LIKE ? OR sr.contact LIKE ? OR sr.remark LIKE ?
            ORDER BY sr.id DESC
        ''', (pattern, pattern, pattern, pattern, pattern, pattern, pattern, pattern))
        return self.cursor.fetchall()

    def update_record_status(self, record_id, new_status, compensate_amount=0):
        from datetime import datetime
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.cursor.execute(
            "UPDATE stock_records SET status=?, compensate_amount=?, return_date=? WHERE id=?",
            (new_status, compensate_amount, now, record_id))
        self.conn.commit()

    def update_record_quantity(self, record_id, new_quantity):
        self.cursor.execute(
            "UPDATE stock_records SET quantity=? WHERE id=?",
            (new_quantity, record_id))
        self.conn.commit()

    def split_record_for_return(self, record_id, return_qty):
        """将借出记录拆分：return_qty 件标记为已归还，剩余保持借出"""
        from datetime import datetime
        record = self.get_record_by_id(record_id)
        if not record:
            return False
        total_qty = record[9]
        if return_qty > total_qty or return_qty <= 0:
            return False
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        if return_qty == total_qty:
            # 全部归还
            self.cursor.execute(
                "UPDATE stock_records SET status='已归还', return_date=? WHERE id=?",
                (now, record_id))
        else:
            # 减少原记录数量
            self.cursor.execute(
                "UPDATE stock_records SET quantity=? WHERE id=?",
                (total_qty - return_qty, record_id))
            # 新建一条已归还记录
            self.cursor.execute('''
                INSERT INTO stock_records
                (clothing_id, clothing_name, department, team_name, host_operator,
                 anchor_name, contact, record_date, quantity, direction, status, remark,
                 created_at, return_date)
                SELECT clothing_id, clothing_name, department, team_name, host_operator,
                       anchor_name, contact, record_date, ?, direction, '已归还', remark,
                       created_at, ?
                FROM stock_records WHERE id=?
            ''', (return_qty, now, record_id))
        self.conn.commit()
        return True

    def split_record_for_compensate(self, record_id, comp_qty, comp_amount):
        """将借出记录拆分：comp_qty 件标记为已赔付，剩余保持借出"""
        from datetime import datetime
        record = self.get_record_by_id(record_id)
        if not record:
            return False
        total_qty = record[9]
        if comp_qty > total_qty or comp_qty <= 0:
            return False
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        if comp_qty == total_qty:
            # 全部赔付
            self.cursor.execute(
                "UPDATE stock_records SET status='已赔付', compensate_amount=?, return_date=? WHERE id=?",
                (comp_amount, now, record_id))
        else:
            # 减少原记录数量
            self.cursor.execute(
                "UPDATE stock_records SET quantity=? WHERE id=?",
                (total_qty - comp_qty, record_id))
            # 新建一条已赔付记录
            self.cursor.execute('''
                INSERT INTO stock_records
                (clothing_id, clothing_name, department, team_name, host_operator,
                 anchor_name, contact, record_date, quantity, direction, status,
                 compensate_amount, remark, created_at, return_date)
                SELECT clothing_id, clothing_name, department, team_name, host_operator,
                       anchor_name, contact, record_date, ?, direction, '已赔付',
                       ?, remark, created_at, ?
                FROM stock_records WHERE id=?
            ''', (comp_qty, comp_amount, now, record_id))
        self.conn.commit()
        return True

    def get_record_by_id(self, record_id):
        self.cursor.execute('''
            SELECT id, clothing_id, clothing_name, department, team_name,
                   host_operator, anchor_name, contact, record_date,
                   quantity, direction, status, compensate_amount, remark
            FROM stock_records WHERE id=?
        ''', (record_id,))
        return self.cursor.fetchone()

    def delete_stock_record(self, record_id):
        self.cursor.execute('DELETE FROM stock_records WHERE id=?', (record_id,))
        self.conn.commit()

    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*), COALESCE(SUM(stock),0) FROM clothing")
        count, total_stock = self.cursor.fetchone()
        self.cursor.execute("SELECT COUNT(*) FROM clothing WHERE stock <= 5")
        low_stock = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COALESCE(SUM(quantity),0) FROM stock_records WHERE status='借出'")
        borrowed_qty = self.cursor.fetchone()[0]
        return count, total_stock, low_stock, borrowed_qty


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
                border-radius: 10px; color: #888;
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
    COLUMNS = ['ID', '编号', '名称', '分类', '品牌', '尺码', '颜色', '季节', '库存', '进价(¥)']

    def __init__(self, username='admin'):
        super().__init__()
        self.db = Database()
        self.username = username
        self.init_ui()
        self.load_clothing()
        self.load_stock_records()

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
        self.stat_cats = self._make_stat_card('待归还', '0', '#c88a30')
        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_stock)
        stats_layout.addWidget(self.stat_low)
        stats_layout.addWidget(self.stat_cats)
        main_layout.addLayout(stats_layout)

        # ---- 选项卡 ----
        self.tab = QTabWidget()
        self.tab.addTab(self._create_stock_tab(), '🔄  出入库管理')
        self.tab.addTab(self._create_clothing_tab(), '📦  商品管理')
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
        count, total_stock, low, borrowed = self.db.get_stats()
        self.stat_total._num_label.setText(str(count))
        self.stat_stock._num_label.setText(str(total_stock))
        self.stat_low._num_label.setText(str(low))
        self.stat_cats._num_label.setText(str(borrowed))

    # ---------- 商品管理标签 ----------
    def _create_clothing_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(16)

        # ── 左侧表单 ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(320)
        scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')
        left_panel = QWidget()
        left_panel.setObjectName('clothingLeftPanel')
        form_outer = QVBoxLayout(left_panel)
        form_outer.setContentsMargins(18, 14, 18, 14)
        form_outer.setSpacing(8)

        form_title = QLabel('商品信息')
        form_title.setObjectName('sectionTitle')
        form_outer.addWidget(form_title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.c_id = QLineEdit()
        self.c_id.setReadOnly(True)
        self.c_id.setPlaceholderText('自动生成')
        self.c_code = QLineEdit()
        self.c_code.setPlaceholderText('输入编号')
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

        form.addRow('ID：', self.c_id)
        form.addRow('编号：', self.c_code)
        form.addRow('名称：', self.c_name)
        form.addRow('分类：', self.c_category)
        form.addRow('品牌：', self.c_brand)
        form.addRow('尺码：', self.c_size)
        form.addRow('颜色：', self.c_color)
        form.addRow('季节：', self.c_season)
        form.addRow('库存：', self.c_stock)
        form.addRow('进价(¥)：', self.c_cost)
        form_outer.addLayout(form)

        form_outer.addSpacing(8)

        # 按钮
        btn_row1 = QHBoxLayout()
        self.add_btn = QPushButton('✚ 新增')
        self.add_btn.setObjectName('secondaryBtn')
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

        # Excel 导入/导出按钮
        btn_row3 = QHBoxLayout()
        self.import_btn = QPushButton('📥 Excel导入')
        self.import_btn.setObjectName('secondaryBtn')
        self.export_btn = QPushButton('📤 导出模板')
        self.export_btn.setObjectName('secondaryBtn')
        btn_row3.addWidget(self.import_btn)
        btn_row3.addWidget(self.export_btn)
        form_outer.addLayout(btn_row3)

        self.import_btn.clicked.connect(self.import_excel)
        self.export_btn.clicked.connect(self.export_template)

        form_outer.addStretch()

        scroll.setWidget(left_panel)

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
        self.clothing_table.setSortingEnabled(True)
        self.clothing_table.cellClicked.connect(self.select_clothing)
        right_panel.addWidget(self.clothing_table, 1)

        layout.addWidget(scroll)
        layout.addLayout(right_panel, 1)
        return widget

    # ---------- 出入库标签 ----------
    STOCK_RECORD_COLS = ['记录ID', '商品编号', '商品名称', '部门', '团名',
                         '主持/运营', '主播艺名', '联系方式', '操作日期',
                         '数量', '类型', '状态', '赔付金额(¥)', '备注',
                         '借出时间', '归还时间']

    def _create_stock_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(16)

        # ── 左侧表单 ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(340)
        scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')
        left_panel = QWidget()
        left_panel.setObjectName('stockLeftPanel')
        form_outer = QVBoxLayout(left_panel)
        form_outer.setContentsMargins(18, 14, 18, 14)
        form_outer.setSpacing(8)

        form_title = QLabel('出入库操作')
        form_title.setObjectName('sectionTitle')
        form_outer.addWidget(form_title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.stock_id = QLineEdit()
        self.stock_id.setPlaceholderText('输入商品编号（如 BH001）')
        self.stock_department = QLineEdit()
        self.stock_department.setPlaceholderText('输入部门')
        self.stock_team = QLineEdit()
        self.stock_team.setPlaceholderText('输入团名')
        self.stock_host = QLineEdit()
        self.stock_host.setPlaceholderText('主持/运营')
        self.stock_anchor = QLineEdit()
        self.stock_anchor.setPlaceholderText('主播艺名')
        self.stock_contact = QLineEdit()
        self.stock_contact.setPlaceholderText('联系方式')
        self.stock_date = QDateEdit()
        self.stock_date.setCalendarPopup(True)
        self.stock_date.setDate(QDate.currentDate())
        self.stock_date.setDisplayFormat('yyyy-MM-dd')
        self.stock_num = QLineEdit()
        self.stock_num.setPlaceholderText('输入数量')
        self.stock_remark = QLineEdit()
        self.stock_remark.setPlaceholderText('备注信息')

        form.addRow('编号：', self.stock_id)
        form.addRow('部门：', self.stock_department)
        form.addRow('团名：', self.stock_team)
        form.addRow('主持/运营：', self.stock_host)
        form.addRow('主播艺名：', self.stock_anchor)
        form.addRow('联系方式：', self.stock_contact)
        form.addRow('操作日期：', self.stock_date)
        form.addRow('数量：', self.stock_num)
        form.addRow('备注：', self.stock_remark)
        form_outer.addLayout(form)

        form_outer.addSpacing(6)

        hint = QLabel('💡 借出会自动减库存，入库会自动加库存')
        hint.setStyleSheet('color: #b08968; font-size: 11px;')
        hint.setWordWrap(True)
        form_outer.addWidget(hint)

        # 借出/归还按钮（一组）
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        self.out_btn = QPushButton('📤  借出')
        self.out_btn.setObjectName('stockOutBtn')
        self.return_btn = QPushButton('↩ 归还')
        self.return_btn.setObjectName('returnBtn')
        self.out_btn.clicked.connect(lambda: self.operate_stock(-1))
        self.return_btn.clicked.connect(self.return_stock)
        btn_row.addWidget(self.out_btn)
        btn_row.addWidget(self.return_btn)
        form_outer.addLayout(btn_row)

        form_outer.addSpacing(4)

        # 入库/赔付按钮（一组）
        btn_row2 = QHBoxLayout()
        btn_row2.setSpacing(12)
        self.in_btn = QPushButton('📥  入库')
        self.in_btn.setObjectName('stockInBtn')
        self.compensate_btn = QPushButton('💰 赔付')
        self.compensate_btn.setObjectName('compensateBtn')
        self.in_btn.clicked.connect(lambda: self.operate_stock(1))
        self.compensate_btn.clicked.connect(self.compensate_stock)
        btn_row2.addWidget(self.in_btn)
        btn_row2.addWidget(self.compensate_btn)
        form_outer.addLayout(btn_row2)

        # 清空按钮
        self.stock_clear_btn = QPushButton('↺ 清空表单')
        self.stock_clear_btn.setObjectName('secondaryBtn')
        self.stock_clear_btn.clicked.connect(self.clear_stock_form)
        form_outer.addWidget(self.stock_clear_btn)

        # 删除记录按钮
        self.stock_del_btn = QPushButton('✕ 删除记录')
        self.stock_del_btn.setObjectName('dangerBtn')
        self.stock_del_btn.clicked.connect(self.delete_stock_record)
        form_outer.addWidget(self.stock_del_btn)

        form_outer.addStretch()

        scroll.setWidget(left_panel)

        # ── 右侧记录表 ──
        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)

        # 搜索栏
        search_row = QHBoxLayout()
        self.stock_search_input = QLineEdit()
        self.stock_search_input.setObjectName('searchInput')
        self.stock_search_input.setPlaceholderText('🔍  搜索商品名 / 部门 / 团名 / 主播 ...')
        self.stock_search_input.textChanged.connect(self.search_stock_records)
        search_row.addWidget(self.stock_search_input)
        right_panel.addLayout(search_row)

        # 记录表格
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(len(self.STOCK_RECORD_COLS))
        self.stock_table.setHorizontalHeaderLabels(self.STOCK_RECORD_COLS)
        self.stock_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.stock_table.setSelectionMode(QTableWidget.SingleSelection)
        self.stock_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.stock_table.setAlternatingRowColors(True)
        self.stock_table.setStyleSheet('QTableWidget { alternate-background-color: #faf7f4; }')
        self.stock_table.horizontalHeader().setStretchLastSection(True)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.stock_table.verticalHeader().setVisible(False)
        self.stock_table.setSortingEnabled(True)
        self.stock_table.cellClicked.connect(self.select_stock_record)
        right_panel.addWidget(self.stock_table, 1)

        layout.addWidget(scroll)
        layout.addLayout(right_panel, 1)
        return widget

    # ---------- 数据操作 ----------
    def load_clothing(self):
        data = self.db.get_all_clothing()
        self._fill_table(data)
        self._update_stats()

    def _fill_table(self, data):
        self.clothing_table.setSortingEnabled(False)
        self.clothing_table.setRowCount(len(data))
        # 数值列：0=ID, 8=库存, 9=进价
        numeric_cols = {0, 8, 9}
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                cell = QTableWidgetItem(str(value))
                cell.setTextAlignment(Qt.AlignCenter)
                if col in numeric_cols:
                    try:
                        cell.setData(Qt.UserRole, float(value) if value else 0)
                    except (ValueError, TypeError):
                        cell.setData(Qt.UserRole, 0)
                # 低库存高亮 (库存列索引=8)
                if col == 8 and isinstance(value, int) and value <= 5:
                    cell.setForeground(QColor('#d96b6b'))
                    cell.setFont(QFont("", -1, QFont.Bold))
                self.clothing_table.setItem(row, col, cell)
        self.clothing_table.resizeColumnsToContents()
        self.clothing_table.setSortingEnabled(True)

    def search_clothing(self, text):
        keyword = text.strip()
        data = self.db.search_clothing(keyword) if keyword else self.db.get_all_clothing()
        self._fill_table(data)

    def select_clothing(self, row):
        table = self.clothing_table
        self.c_id.setText(table.item(row, 0).text())
        self.c_code.setText(table.item(row, 1).text())
        self.c_name.setText(table.item(row, 2).text())
        # 设置下拉框
        cat = table.item(row, 3).text()
        idx = self.c_category.findText(cat)
        self.c_category.setCurrentIndex(idx if idx >= 0 else 0)
        self.c_brand.setText(table.item(row, 4).text())
        sz = table.item(row, 5).text()
        idx = self.c_size.findText(sz)
        self.c_size.setCurrentIndex(idx if idx >= 0 else 0)
        self.c_color.setText(table.item(row, 6).text())
        se = table.item(row, 7).text()
        idx = self.c_season.findText(se)
        self.c_season.setCurrentIndex(idx if idx >= 0 else 0)
        self.c_stock.setText(table.item(row, 8).text())
        self.c_cost.setText(table.item(row, 9).text())

    def clear_form(self):
        for w in [self.c_id, self.c_code, self.c_name, self.c_brand, self.c_color, self.c_stock, self.c_cost]:
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
            self.c_code.text().strip(),
            name, self.c_category.currentText(), self.c_brand.text().strip(),
            self.c_size.currentText(), self.c_color.text().strip(),
            self.c_season.currentText(),
            int(self.c_stock.text() or 0),
            float(self.c_cost.text() or 0))
        self.load_clothing()
        self.clear_form()
        QMessageBox.information(self, '成功', '服装商品已添加！')

    def update_clothing(self):
        if not self.c_id.text():
            QMessageBox.warning(self, '提示', '请先选择要修改的商品')
            return
        self.db.update_clothing(
            int(self.c_id.text()),
            self.c_code.text().strip(),
            self.c_name.text().strip(), self.c_category.currentText(),
            self.c_brand.text().strip(), self.c_size.currentText(),
            self.c_color.text().strip(), self.c_season.currentText(),
            int(self.c_stock.text() or 0),
            float(self.c_cost.text() or 0))
        self.load_clothing()
        QMessageBox.information(self, '成功', '商品信息已更新！')

    def delete_clothing(self):
        if not self.c_id.text():
            QMessageBox.warning(self, '提示', '请先选择要删除的商品')
            return
        reply = QMessageBox.question(self, '确认删除',
            f'确定要删除编号={self.c_id.text()} 吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_clothing(int(self.c_id.text()))
            self.load_clothing()
            self.clear_form()
            QMessageBox.information(self, '成功', '商品已删除！')

    # ---------- Excel 导入导出 ----------
    def import_excel(self):
        """从 Excel 文件批量导入商品"""
        try:
            import openpyxl
        except ImportError:
            QMessageBox.warning(self, '缺少依赖', '请先安装 openpyxl：\npip install openpyxl')
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择 Excel 文件', '',
            'Excel 文件 (*.xlsx *.xls);;所有文件 (*)')
        if not file_path:
            return

        try:
            wb = openpyxl.load_workbook(file_path, read_only=True)
            ws = wb.active

            # 读取表头，建立列名到索引的映射
            headers = [str(cell.value).strip() if cell.value else '' for cell in next(ws.iter_rows(min_row=1, max_row=1))]
            col_map = {}
            header_aliases = {
                '编号': 'code', '服装编号': 'code', '商品编号': 'code', 'code': 'code',
                '名称': 'name', '服装名称': 'name', '商品名称': 'name', 'name': 'name',
                '分类': 'category', '品牌': 'brand', '尺码': 'size',
                '颜色': 'color', '季节': 'season', '库存': 'stock',
                '进价': 'cost_price', '进价(¥)': 'cost_price',
            }
            for i, h in enumerate(headers):
                key = header_aliases.get(h)
                if key:
                    col_map[key] = i

            if 'name' not in col_map:
                QMessageBox.warning(self, '格式错误',
                    '未找到"名称"或"服装名称"列。\n\n'
                    '请确保 Excel 表头包含：编号、服装名称\n'
                    '可选列：分类、品牌、尺码、颜色、季节、库存、进价')
                wb.close()
                return

            success = 0
            errors = []
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                if not row or all(v is None for v in row):
                    continue
                try:
                    def get_val(key, default=''):
                        idx = col_map.get(key)
                        if idx is not None and idx < len(row) and row[idx] is not None:
                            return row[idx]
                        return default

                    name = str(get_val('name', '')).strip()
                    if not name:
                        continue

                    code = str(get_val('code', '')).strip()
                    category = str(get_val('category', '其他')).strip()
                    brand = str(get_val('brand', '')).strip()
                    size = str(get_val('size', '均码')).strip()
                    color = str(get_val('color', '')).strip()
                    season = str(get_val('season', '四季通用')).strip()
                    stock = int(float(get_val('stock', 0)))
                    cost_price = float(get_val('cost_price', 0))

                    self.db.add_clothing(code, name, category, brand, size, color, season, stock, cost_price)
                    success += 1
                except Exception as e:
                    errors.append(f'第{row_idx}行: {e}')

            wb.close()
            self.load_clothing()

            msg = f'成功导入 {success} 条商品记录！'
            if errors:
                msg += f'\n\n{len(errors)} 条失败：\n' + '\n'.join(errors[:10])
                if len(errors) > 10:
                    msg += f'\n... 还有 {len(errors)-10} 条错误'
            QMessageBox.information(self, '导入完成', msg)

        except Exception as e:
            QMessageBox.critical(self, '导入失败', f'读取 Excel 文件时出错：\n{e}')

    def export_template(self):
        """导出 Excel 导入模板"""
        try:
            import openpyxl
        except ImportError:
            QMessageBox.warning(self, '缺少依赖', '请先安装 openpyxl：\npip install openpyxl')
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存导入模板', '商品导入模板.xlsx',
            'Excel 文件 (*.xlsx);;所有文件 (*)')
        if not file_path:
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = '商品导入'

            # 表头
            headers = ['编号', '服装名称', '分类', '品牌', '尺码', '颜色', '季节', '库存', '进价']
            for col, h in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=h)
                cell.font = openpyxl.styles.Font(bold=True)
                cell.alignment = openpyxl.styles.Alignment(horizontal='center')

            # 示例数据
            sample = ['BH001', '春季新款T恤', '上衣', '优衣库', 'L', '白色', '春季', 100, 49.9]
            for col, v in enumerate(sample, 1):
                ws.cell(row=2, column=col, value=v)

            # 调整列宽
            for col in range(1, len(headers) + 1):
                ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 14

            wb.save(file_path)
            wb.close()
            QMessageBox.information(self, '成功', f'导入模板已保存到：\n{file_path}')
        except Exception as e:
            QMessageBox.critical(self, '导出失败', f'保存模板时出错：\n{e}')

    def operate_stock(self, direction):
        code_text = self.stock_id.text().strip()
        num_text = self.stock_num.text().strip()
        if not code_text or not num_text:
            QMessageBox.warning(self, '提示', '请输入商品编号和数量')
            return
        try:
            quantity = abs(int(num_text))
        except ValueError:
            QMessageBox.warning(self, '提示', '数量必须为数字')
            return
        if quantity <= 0:
            QMessageBox.warning(self, '提示', '数量必须大于 0')
            return

        # 按编号查找商品
        result = self.db.find_clothing_by_code(code_text)
        if result is None:
            QMessageBox.warning(self, '提示', f'未找到编号为「{code_text}」的商品')
            return
        clothing_id, clothing_name, current_stock = result

        num = quantity * direction
        if not self.db.update_stock(clothing_id, num):
            QMessageBox.warning(self, '失败', '库存不足，操作失败！')
            return

        op_type = '入库' if direction > 0 else '借出'
        status = '入库' if direction > 0 else '借出'
        record_date = self.stock_date.date().toString('yyyy-MM-dd')

        self.db.add_stock_record(
            clothing_id, clothing_name,
            self.stock_department.text().strip(),
            self.stock_team.text().strip(),
            self.stock_host.text().strip(),
            self.stock_anchor.text().strip(),
            self.stock_contact.text().strip(),
            record_date, quantity, direction, status,
            self.stock_remark.text().strip())

        self.load_clothing()
        self.load_stock_records()
        self.clear_stock_form()
        self._update_stats()
        QMessageBox.information(self, '成功', f'{op_type} {quantity} 件完成！')

    def return_stock(self):
        """归还：选中一条借出记录，支持任意数量归还"""
        selected = self.stock_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请先在右侧表格中选择一条借出记录')
            return
        record_id = int(self.stock_table.item(selected, 0).text())
        record = self.db.get_record_by_id(record_id)
        if not record:
            QMessageBox.warning(self, '提示', '未找到该记录')
            return

        current_status = record[11]
        if current_status != '借出':
            QMessageBox.warning(self, '提示', f'该记录状态为"{current_status}"，只能对"借出"状态的记录进行归还')
            return

        clothing_id = record[1]
        total_qty = record[9]

        return_qty, ok = QInputDialog.getInt(
            self, '归还数量',
            f'商品：{record[2]}\n'
            f'借出数量：{total_qty} 件\n'
            f'借用人：{record[6]}（{record[5]}）\n\n'
            f'请输入归还数量：',
            total_qty, 1, total_qty)
        if not ok:
            return

        reply = QMessageBox.question(self, '确认归还',
            f'确认归还商品：{record[2]}\n'
            f'归还数量：{return_qty} / {total_qty} 件\n'
            f'借用人：{record[6]}（{record[5]}）',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 库存回加
        self.db.update_stock(clothing_id, return_qty)
        self.db.split_record_for_return(record_id, return_qty)
        self.load_clothing()
        self.load_stock_records()
        self._update_stats()
        msg = f'已归还 {return_qty} 件！'
        if return_qty < total_qty:
            msg += f'\n剩余 {total_qty - return_qty} 件仍为借出状态'
        QMessageBox.information(self, '成功', msg)

    def compensate_stock(self):
        """赔付：选中借出记录，支持任意数量赔付"""
        selected = self.stock_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请先在右侧表格中选择一条借出记录')
            return
        record_id = int(self.stock_table.item(selected, 0).text())
        record = self.db.get_record_by_id(record_id)
        if not record:
            QMessageBox.warning(self, '提示', '未找到该记录')
            return

        current_status = record[11]
        if current_status != '借出':
            QMessageBox.warning(self, '提示', f'该记录状态为"{current_status}"，只能对"借出"状态的记录进行赔付')
            return

        total_qty = record[9]

        comp_qty, ok = QInputDialog.getInt(
            self, '赔付数量',
            f'商品：{record[2]}\n'
            f'借出数量：{total_qty} 件\n'
            f'借用人：{record[6]}（{record[5]}）\n\n'
            f'请输入赔付数量：',
            total_qty, 1, total_qty)
        if not ok:
            return

        amount, ok = QInputDialog.getDouble(
            self, '赔付金额',
            f'商品：{record[2]}（赔付 {comp_qty} 件）\n请输入赔付金额（¥）：',
            0, 0, 999999, 2)
        if not ok:
            return

        reply = QMessageBox.question(self, '确认赔付',
            f'确认对以下记录进行赔付：\n'
            f'商品：{record[2]}\n'
            f'赔付数量：{comp_qty} / {total_qty} 件\n'
            f'借用人：{record[6]}（{record[5]}）\n'
            f'赔付金额：¥{amount:.2f}',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        self.db.split_record_for_compensate(record_id, comp_qty, amount)
        self.load_stock_records()
        self._update_stats()
        msg = f'赔付 {comp_qty} 件，¥{amount:.2f} 已记录！'
        if comp_qty < total_qty:
            msg += f'\n剩余 {total_qty - comp_qty} 件仍为借出状态'
        QMessageBox.information(self, '成功', msg)

    def delete_stock_record(self):
        """删除选中的出入库记录"""
        selected = self.stock_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请先在右侧表格中选择一条记录')
            return
        record_id = int(self.stock_table.item(selected, 0).text())
        record = self.db.get_record_by_id(record_id)
        if not record:
            QMessageBox.warning(self, '提示', '未找到该记录')
            return

        status = record[11]
        clothing_id = record[1]
        quantity = record[9]
        direction = record[10]

        reply = QMessageBox.question(self, '确认删除',
            f'确认删除以下记录？\n\n'
            f'商品：{record[2]}\n'
            f'数量：{quantity} 件\n'
            f'状态：{status}\n'
            f'借用人：{record[6]}（{record[5]}）\n\n'
            f'❗ 删除后库存将自动还原',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 还原库存：入库记录删除后减库存，借出记录删除后加库存
        if direction == 1:
            # 入库记录 -> 删除后减库存
            self.db.update_stock(clothing_id, -quantity)
        elif status == '借出':
            # 借出未归还 -> 删除后加回库存
            self.db.update_stock(clothing_id, quantity)
        # 已归还/已赔付的记录删除不影响库存（已经还原过了）

        self.db.delete_stock_record(record_id)
        self.load_clothing()
        self.load_stock_records()
        self._update_stats()
        QMessageBox.information(self, '成功', '记录已删除')

    # ---------- 出入库记录查询 ----------
    def load_stock_records(self):
        data = self.db.get_all_stock_records()
        self._fill_stock_table(data)

    def _fill_stock_table(self, data):
        self.stock_table.setSortingEnabled(False)
        self.stock_table.setRowCount(len(data))
        # 数值列索引：0=记录ID, 9=数量, 12=赔付金额
        numeric_cols = {0, 9, 12}
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                # direction 列(10)显示为文字
                if col == 10:
                    display = '入库' if value == 1 else '借出'
                elif col == 12:
                    display = f'{value:.2f}' if value else '0.00'
                else:
                    display = str(value) if value is not None else ''
                cell = QTableWidgetItem(display)
                cell.setTextAlignment(Qt.AlignCenter)
                # 数值列设置 sortData 保证数字排序
                if col in numeric_cols:
                    try:
                        cell.setData(Qt.UserRole, float(value) if value else 0)
                    except (ValueError, TypeError):
                        cell.setData(Qt.UserRole, 0)
                # 状态列(11)着色
                if col == 11:
                    if value == '借出':
                        cell.setForeground(QColor('#d96b6b'))
                        cell.setFont(QFont("", -1, QFont.Bold))
                    elif value == '已归还':
                        cell.setForeground(QColor('#5a9e6f'))
                    elif value == '已赔付':
                        cell.setForeground(QColor('#c88a30'))
                        cell.setFont(QFont("", -1, QFont.Bold))
                self.stock_table.setItem(row, col, cell)
        self.stock_table.resizeColumnsToContents()
        self.stock_table.setSortingEnabled(True)

    def search_stock_records(self, text):
        keyword = text.strip()
        data = self.db.search_stock_records(keyword) if keyword else self.db.get_all_stock_records()
        self._fill_stock_table(data)

    def select_stock_record(self, row):
        """点击记录行时，将信息填充到左侧表单（用于归还/赔付操作参考）"""
        table = self.stock_table
        if table.item(row, 1):
            self.stock_id.setText(table.item(row, 1).text())
        if table.item(row, 3):
            self.stock_department.setText(table.item(row, 3).text())
        if table.item(row, 4):
            self.stock_team.setText(table.item(row, 4).text())
        if table.item(row, 5):
            self.stock_host.setText(table.item(row, 5).text())
        if table.item(row, 6):
            self.stock_anchor.setText(table.item(row, 6).text())
        if table.item(row, 7):
            self.stock_contact.setText(table.item(row, 7).text())
        if table.item(row, 9):
            self.stock_num.setText(table.item(row, 9).text())
        if table.item(row, 13):
            self.stock_remark.setText(table.item(row, 13).text())

    def clear_stock_form(self):
        for w in [self.stock_id, self.stock_department, self.stock_team,
                  self.stock_host, self.stock_anchor, self.stock_contact,
                  self.stock_num, self.stock_remark]:
            w.clear()
        self.stock_date.setDate(QDate.currentDate())


# ===================== 程序入口 =====================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())