class CalipsoExperiment(object):

        def __init__(self, id):
                self.proposal_id = id
                self.sessions = []
                self.subject = ''
                self.body = ''
                self.beam_line = []
                self.uid = None
                self.gid = None

        def to_json(self):
                return {'subject': self.subject,
                        'proposal_id': self.proposal_id,
                        'beam_line': self.beam_line,
                        'body': self.body,
                        'uid': self.uid,
                        'gid' : self.gid,
                        'sessions': self.sessions
                        }
