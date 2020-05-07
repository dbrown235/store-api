from db import db

class StoreModel(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic') #list of ItemModels
    # lazy makes it a query builder, without lazy it creates a complete list of items


    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]} #query for all to make list
    # until we call json method, SQLAlchemy does not look into items table

    @classmethod
    def find_by_name(cls, name):
        return cls.query.fliter_by(name=name).first()# SELECT * FROM items where name = name limit 1
        # returns ItemModel object

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


