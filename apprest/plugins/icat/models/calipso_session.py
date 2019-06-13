class CalipsoSession(object):
    def __init__(self, session_number):
        self.session_number = session_number
        self.start_date = ''
        self.end_date = ''
        self.subject = ''
        self.body = ''

    def to_json(self):
        return {'session_number': self.session_number,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'subject': self.subject,
                'body': self.body,
                'data_set_path': ''
                }
