from mailer import db


class ProviderModel(db.Model):
  __tablename__ = 'providers'

  id        = db.Column(db.Integer, primary_key=True)
  name      = db.Column(db.String(50))
  key       = db.Column(db.String(100))
  errors    = db.Column(db.Integer)
  successes = db.Column(db.Integer)
  rank      = db.Column(db.Integer)

  def __init__(self, name, key, errors=0, successes=0, rank=0):
    self.name      = name
    self.key       = key
    self.errors    = errors
    self.successes = successes
    self.rank      = rank


  @classmethod
  def getAllByRank(cls):
    return cls.query.order_by('rank').all()


  def __repr__(self):
      return '<Provider: id {}>'.format(self.id)