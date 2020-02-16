from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

class CategoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create')


class QuizForm(FlaskForm):
    question = TextAreaField('Question',
                             validators=[DataRequired()])
    marks = IntegerField('Marks',
                         validators=[DataRequired()])
    option1 = StringField('First Answers Option',
                          validators=[DataRequired()])
    option2 = StringField('Second Answers Option',
                          validators=[DataRequired()])
    option3 = StringField('Third Answers Option',
                          validators=[Optional()])
    option4 = StringField('Forth Answers Option',
                          validators=[Optional()])

    true_answer = SelectField('Answers',
                              choices=[('A', 'A'), ('B', 'B'),
                                       ('C', 'C'), ('D', 'D')],
                              validators=[DataRequired()]
                              )
    hint = FileField('Upload Content',   validators=[Optional()])
    submit = SubmitField('Add')
