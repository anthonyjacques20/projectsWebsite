from hobbyProjectWebsite import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


# from hobbyProjectWebsite import create_app
# from sqlalchemy.dialects.postgresql import JSON
# import datetime 

# db =create_app().db

# class Result(db.Model):
#     __tablename__ = 'results'

#     id = db.Column(db.Integer, primary_key = True, sqllite_autoincrement = True)
#     # author_id = db.Column(db.Integer, nullable = False)
#     # created = db.Column(db.DateTime, nullable = False, default = datetime.datetime.utcnow)
#     title = db.Column(db.Text, nullable = False)
#     body = db.Column(db.Text, nullable = False)
#     # image = db.Column(db.Text, default = None)
#     # githubURL = db.Column(db.Text, default = None)
#     # moreInfoURL = db.Column(db.Text, default = None)

#     result_all = db.Column(JSON)
#     result_no_stop_words = db.Column(JSON)

#     def __init__(self, title, result_all, result_no_stop_words):
#         self.title = title
#         self.result_all = result_all
#         self.result_no_stop_words = result_no_stop_words

#     def __repr__(self):
#         return '<id {}>'.format(self.id)