class CalipsoInvestigationUser(object):

    def __init__(self):
        self.name = ''
        self.full_name = ''
        self.role = ''
        self.investigation_name = ''
        self.investigation_id = ''

    def to_json(self):
        return {
            'name': self.name,
            'fullName': self.full_name,
            'role': self.role,
            'investigationName': self.investigation_name,
            'investigationId': self.investigation_id
            }
