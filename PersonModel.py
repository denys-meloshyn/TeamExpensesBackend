__author__ = 'Denys.Meloshyn'

import uuid
import time
from SharedModels import db

class PersonModel(db.Model):
    def __init__(self):
        token = str(uuid.uuid4()) + '|' + str(time.time() * 1000 )
        self.token = token

    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    facebook_id = db.Column(db.Text)
    token = db.Column(db.Text)

    def to_dict(self):
        print self.first_name
        json_object = {'person_id': self.person_id,
                       'firstName': self.first_name,
                       'lastName': self.last_name,
                       'email': self.email,
                       'facebook_id': self.facebook_id,
                       'token': self.token}

        return json_object
