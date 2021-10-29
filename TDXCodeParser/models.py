from app import db

class Func(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer)

    def __repr__(self) -> str:
        return '<{} {}>'.format(self.__class__.__name__,self.body)