from costarica.settings import db
import sqlalchemy


class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    alias_name = db.Column(db.String(80))
    group = db.Column(db.String(80), nullable=False)
    times = db.Column(db.Integer, nullable=False)

    def __init__(self, name, times, group, alias_name=''):
        self.name = str(name)
        self.alias_name = str(alias_name)
        self.times = int(times)
        self.group = str(group)

    def __repr__(self):
        return f'<Chef {self.name}:{self.times}>'

    def commit(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_group(cls, group_id):
        return Chef.query.filter(Chef.group==group_id).all()

    @classmethod
    def find_by_name(cls, group_id, name, func=None):
        chefs = Chef.query.filter(Chef.name==name, Chef.group==group_id).all()

        if chefs and len(chefs) == 1:
            chef = chefs[0]
            return chef
        else:
            if func:
                return func()


try:
    db.create_all()
    print("Created \"chef\" table.")
except sqlalchemy.exc.OperationalError:
    print("Cannot connect to db.")
