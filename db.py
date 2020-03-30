import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, title text, artist text, label text, cat_number text, barcode text, supplier text, unit_price text, retail_price text, stock_level text, date_received text, sold_today text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM parts")
        rows = self.cur.fetchall()
        return rows

    def insert(self, title, artist, label, cat_number, barcode, supplier, unit_price, retail_price, stock_level, date_received, sold_today):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, artist, label, cat_number, barcode, supplier, unit_price, retail_price, stock_level, date_received, sold_today))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM parts WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, title, artist, label, cat_number, barcode, supplier, unit_price, retail_price, stock_level, date_received, sold_today):
        self.cur.execute("UPDATE parts SET title = ?, artist = ?, label = ?, cat_number = ?, barcode = ?, supplier = ?, unit_price = ?, retail_price = ?, stock_level = ?, date_received = ? , sold_today = ? WHERE id = ?", (title, artist, label, cat_number, barcode, supplier, unit_price, retail_price, stock_level, date_received, sold_today, id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# db = Database('store.db')
# db.insert("Dr Whatever","John Barry", "EMI", "ASD 2653", "None", "Cargo", "12.00", "18.00", 5, "24 Nov 19", 0)
# db.insert("Mr F","Gob", "Faceblock", "X33", "23845029834705", "Cargo", "12.00", "18.00", 4, "24 Nov 19", 0)
# db.insert("Pitch","Tony Bevan & Neil Davidson", "Foghorn Records", "Fog 2", "None", "SOR", "10.00", "15.00", 5, "10 Oct 19", 0)
