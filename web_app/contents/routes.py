from flask import render_template, request, redirect, flash, abort, url_for, send_file, Blueprint
from flask_login import current_user, login_required
from web_app import db
from web_app.models import User, Quiz, Category, Result
from web_app.contents.forms import CategoryForm, QuizForm
from io import BytesIO


contents = Blueprint('contents',  __name__)


@contents.route("/category/new", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            title=form.title.data, description=form.description.data, staff=current_user)
        db.session.add(category)
        db.session.commit()
        flash('Your category has been created!', 'success')
        return redirect(url_for('contents.category'))
    return render_template('new_category.html', title='New categories',
                           form=form, legend='New category')

@contents.route("/category/<int:category_id>")
@login_required
def display_category(category_id):
    category = Category.query.get_or_404(category_id)
    quizes = Quiz.query.filter_by(category_id=category_id)
    return render_template('category.html', category=category, category_id=category_id, quizes=quizes)



@contents.route("/category/<int:category_id>/update", methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.staff != current_user:
        abort(403)
    form = CategoryForm()
    if form.validate_on_submit():
        category.title = form.title.data
        category.description = form.description.data
        db.session.commit()
        flash('Your Category has been updated!', 'success')
        return redirect(url_for('contents.category'))
    elif request.method == 'GET':
        form.title.data = category.title
        form.description.data = category.description
    return render_template('new_category.html', title='Update Category',
                           form=form, legend='Update Category')


@contents.route("/category/<int:category_id>/delete", methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.staff != current_user:
        abort(403)
    db.session.delete(category)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('contents.category'))

@contents.route("/quiz/<int:category_id>/new", methods=['GET','POST'])
@login_required
def new_question(category_id):
    chapter = Category.query.get_or_404(category_id)
    form = QuizForm()
    if form.validate_on_submit():
        file = form.hint.data
        quiz = Quiz(
            question=form.question.data, marks=form.marks.data, 
            option1=form.option1.data, option2=form.option2.data,
            option3=form.option3.data, option4=form.option4.data, 
            true_answer=form.true_answer.data, hint = file.read(),
            category=chapter 
            )
        db.session.add(quiz)
        db.session.commit()
        if request.form['promp'] == 'NO':
            flash('Your question has been created!', 'success')
            return redirect(url_for('contents.display_category', category_id=category_id))
            
        if request.form['promp'] == 'YES':
            return redirect(url_for('contents.new_question', category_id=category_id))
        
    return render_template('new_question.html', title='Add Questions',
                           form=form, legend='Add Question', chapter=chapter)



@contents.route("/quiz/<int:quiz_id>/delete", methods=['POST','GET'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Your Question has been deleted!', 'success')
    return redirect(url_for('contents.category'))



@contents.route("/info/<int:category_id>", methods=['POST','GET'])
@login_required
def info(category_id):

    category = Category.query.get_or_404(category_id)
    quiz = Quiz.query.\
        filter_by(category_id=category_id).\
        first()


    total = Quiz.query.\
            filter_by(category_id=category_id).\
            count()
           
    contex={
        'category':category
         
         }

    return render_template('info.html',**contex, total=total, quiz=quiz )
    

@contents.route ("/test/<int:category_id>/<int:quiz_id>/", methods=['GET','POST'])
@login_required
def test(category_id,quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    category = Category.query.get_or_404(category_id)

    status = Quiz.query.\
        filter_by(category_id=category_id).\
        count()
    
         
    context ={
        'quiz': quiz,
        'category' : category
    }
    return render_template('question.html', **context, category_id=category_id, quiz_id=quiz_id, status=status) 


@contents.route ("/download/<int:quiz_id>", methods=['GET', 'POST'])
@login_required
def download(quiz_id):
    notes = Quiz.query.get_or_404(quiz_id)
    return send_file(BytesIO(notes.hint), attachment_filename='flask.png', as_attachment=True)



@contents.route ("/test/<int:category_id>/<int:quiz_id>/check", methods=['POST', 'GET'])
@login_required
def check(category_id,quiz_id): 
    score=0
    current_selection = request.form['selection']
    marks = request.form['marks']
    response = request.form['response']
    chapter = request.form['title']
    status = request.form['status']

    if int (quiz_id) < int (status):
        if request.method == 'POST' and current_selection == request.form['answer']:
            keputusan = Result(name=chapter,selection=True, score=marks, response=response, quiz_id=quiz_id, author=current_user)
            db.session.add(keputusan)
            db.session.commit()
            num = 1
            quiz_id = num + int(quiz_id)
            return redirect(url_for('contents.test', category_id=category_id, quiz_id=quiz_id))
        else:
            Keputusan = Result(name=chapter,selection=False, score=score, response=response, quiz_id=quiz_id, author=current_user)
            db.session.add(Keputusan)
            db.session.commit()
            num = 1
            quiz_id = num + int(quiz_id)
            return redirect(url_for('contents.test', category_id=category_id, quiz_id=quiz_id))


    if int (quiz_id) == int (status):
        if request.method == 'POST' and current_selection == request.form['answer']:
            keputusan = Result(name=chapter, selection=True, score=marks,
                               response=response, quiz_id=quiz_id, author=current_user)
            db.session.add(keputusan)
            db.session.commit()
            num = 1
            quiz_id = num + int(quiz_id)
            return redirect(url_for('main.home'))
        else:
            Keputusan = Result(name=chapter,selection=False, score=score, response=response, quiz_id=quiz_id, author=current_user)
            db.session.add(Keputusan)
            db.session.commit()
            num = 1
            quiz_id = num + int(quiz_id)
            return redirect(url_for('main.home'))

