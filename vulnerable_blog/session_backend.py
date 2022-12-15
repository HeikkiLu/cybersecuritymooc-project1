from django.contrib.sessions.backends.db import SessionStore as DBStore

class SessionStore(DBStore):
    def _get_new_session_key(self):
       session = "session0"
       counter = 0
       while self.exists(session):
           counter += 1
           session = "session" + str(counter)
       return session

