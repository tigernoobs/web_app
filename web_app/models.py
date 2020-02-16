from datetime import datetime
from web_app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean)
    user = db.Column(db.Boolean) 
    results = db.relationship(
        'Result', 
        backref='author', 
        lazy=True
    )

    categories = db.relationship(
        'Category',
        backref='staff',
        lazy=True
    )
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"('{self.username}','{self.email}', '{self.image_file}')"







class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quizes = db.relationship(
        'Quiz',
        backref='category',
        lazy=True 
        
        )
    def __repr__(self):
        return f"('{self.name}','{self.description}' '{self.pub_date}')"




class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text)
    option4 = db.Column(db.Text)
    true_answer = db.Column(db.Text, nullable=False)
    hint = db.Column(db.LargeBinary)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    results = db.relationship(
        'Result',
        backref='quiz',
        lazy=True
    )
   

    def __repr__(self):
        return f"('{self.question}', '{self.option1}', '{self.option2}', '{self.option3}', '{self.option4}', '{self.marks}')"


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    selection = db.Column(db.Boolean, default=False)
    response = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"('{self.selection}', '{self.response}', '{self.score}')"








