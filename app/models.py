from app import db

class Attribute(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Attribute {}>'.format(self.text)


class AttributeMapper(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attribute.id'))
    text = db.Column(db.String(64), index=True)
    attribute_value_id = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<AttributeMapper {}-{}>'.format(self.text, self.attribute_value_id)

