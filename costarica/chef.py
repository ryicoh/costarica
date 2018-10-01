from sqlalchemy.exc import OperationalError

from costarica.db import db


class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    times = db.Column(db.Integer, nullable=False)

    alias_name = db.Column(db.String(80))
    group_id = db.Column(db.String(80))

    def __init__(self, user_id, display_name, times, alias_name='', group_id=''):
        self.user_id = str(user_id)
        self.display_name = str(display_name)
        self.times = int(times)

        self.alias_name = str(alias_name)
        self.group_id = str(group_id)

    def __repr__(self):
        return f'<Chef {self.display_name}:{self.times}>'

    def commit(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id):
        return Chef.query.filter(Chef.user_id == user_id).all()

    @classmethod
    def find_by_group(cls, group_id):
        return Chef.query.filter(Chef.group_id == group_id).all()

    @classmethod
    def find_by_user_id_and_group_id(cls, user_id, group_id, func=None):
        chefs = Chef.query.filter(Chef.user_id == user_id, Chef.group_id == group_id).all()

        if chefs and len(chefs) == 1:
            return chefs[0]

        if func:
            return func()


try:
    db.create_all()
    print('Created "chef" table.')
except OperationalError:
    print('Cannot connect to db.')
