import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SinglePageTable(db.Model):
    __tablename__ = 'single_page_table'

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'ID', 'filtered': False, 'sortered': False})
    date = db.Column(db.Date, info={'verbose_name': 'Дата', 'filtered': True, 'sortered': False})
    name = db.Column(db.String(255), info={'verbose_name': 'Название', 'filtered': True, 'sortered': True})
    count = db.Column(db.Integer, info={'verbose_name': 'Количество', 'filtered': True, 'sortered': True})
    length = db.Column(db.Float, info={'verbose_name': 'Расстояние', 'filtered': True, 'sortered': True})

    def __init__(self, date, name, count, length):
        self.date = date
        self.name = name
        self.count = count
        self.length = length

    def to_json(self):
        return {'id': self.id, 'date': self.date, 'name': self.name, 'count': self.count, 'length': self.length}
