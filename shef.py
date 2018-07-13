from settings import db


class Shef(db.Model):
    __tablename__ = 'shefs'

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

    def commit(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_group(cls, group_id):
        return Shef.query.filter(Shef.group==group_id).all()

    @classmethod
    def find_by_name(cls, group_id, name, func=None):
        Shef.query.filter(Shef.name==name, Shef.group==group_id).all()

        if shefs and len(shefs) == 1:
            shef = shefs[0]
        else:
            if func:
                func()
        return shef


    def __repr__(self):
        return f'<Shef {self.name}:{self.times}>'
    
def init_db():
    db.create_all()
