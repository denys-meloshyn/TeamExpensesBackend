from datetime import datetime

from SharedModels import db
from constants import Constants
from PersonModel import PersonModel


class EventTeamMembers(db.Model):
    __tablename__ = 'event_team_members'

    k_team_member_id = 'teamMemberID'

    team_member_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event_model.event_id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person_model.person_id'))
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    @classmethod
    def find_rows_for_user(cls, user_id):
        """Find all events where current user is added as team member
        :param user_id: User ID
        :return:List of EventTeamMembers objects
        """
        if user_id is None or not isinstance(user_id, int):
            return []

        rows = EventTeamMembers.query.filter_by(user_id=user_id).all()

        return rows

    @classmethod
    def time_stamp_for_event(cls, event_id, time_stamp):
        """
        Search all rows with current event_id value which are greater than time_stamp value
        :param event_id:
        :param time_stamp:
        :return:
        """
        if time_stamp is None:
            items = EventTeamMembers.query.filter_by(event_id=event_id).all()
        else:
            items = EventTeamMembers.query.filter(EventTeamMembers.event_id == event_id,
                                                  EventTeamMembers.time_stamp > time_stamp).all()

        return items

    @classmethod
    def team_members(cls, event_id):
        """Find all team members with current event ID
        :param event_id: Event ID
        :return:List of EventTeamMembers objects
        """
        if event_id is None or not isinstance(event_id, int):
            return []

        team_member_rows = EventTeamMembers.query.filter_by(event_id=event_id).all()

        return team_member_rows

    @classmethod
    def find_team_member(cls, team_member_id):
        items = EventTeamMembers.query.filter_by(team_member_id=team_member_id).all()

        if len(items) > 0:
            return items[0]
        else:
            event_team_member = EventTeamMembers()

            event_team_member.is_removed = False
            event_team_member.time_stamp = datetime.utcnow()

            return event_team_member

    @classmethod
    def add_team_member(cls, event_model, person_model):
        if event_model is None:
            return

        if person_model is None:
            return

        items = EventTeamMembers.query.filter(event_id=event_model.event_id,
                                              person_id=person_model.person_id).all()
        if len(items) > 0:
            existed_model = items[0]
            existed_model.event_id = event_model.event_id
            existed_model.person_id = person_model.person_id

    @classmethod
    def remove_team_member(cls, event_model, person_items):
        if event_model is None:
            return

        if not isinstance(person_items, list):
            return

        for person_model in person_items:
            if isinstance(person_model, PersonModel):
                items = EventTeamMembers.query.filter(event_id=event_model.event_id,
                                                      person_id=person_model.person_id).all()
                if len(items) > 0:
                    existed_model = items[0]
                    existed_model.event_id = event_model.event_id
                    existed_model.person_id = person_model.person_id

    def configure_with_dict(self, dict_model):
        value = dict_model.get(Constants.k_event_id)
        if value is not None:
            self.event_id = value

        value = dict_model.get(PersonModel.k_person_id)
        if value is not None:
            self.person_id = value

        # Update time stamp each time we update model from user
        self.time_stamp = datetime.utcnow()

    def to_dict(self):
        json_object = dict()

        json_object[EventTeamMembers.k_team_member_id] = self.team_member_id
        json_object[Constants.k_event_id] = self.event_id
        json_object[PersonModel.k_person_id] = self.person_id
        json_object[Constants.k_is_removed] = self.is_removed

        return json_object
