from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
# '''
# Red underlines? Install the required packages first: 
# Open the Terminal in PyCharm (bottom left). 

# On Windows type:
# python -m pip install -r requirements.txt

# On MacOS type:
# pip3 install -r requirements.txt

# This will install the packages from requirements.txt for this project.
# '''

# # class BookForm():
# #     book_name=

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///new-books-collections.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


with app.app_context():
    db.create_all()
# all_books = []


@app.route('/')
def home():
    result=db.session.execute(db.select(Book))
    all_books=result.scalars().all()
    return render_template('index.html',all=all_books)


@app.route("/add",methods=['GET','POST'])
def add():
    if request.method=="POST":
        # all_books.append({
        #     'title':request.form['title'],
        #     'author':request.form['author'],
        #     'rating':request.form['rating'],
        # })
        # CREATE RECORD
        
        new_book = Book( title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #UPDATE RECORD
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("editing.html", b=book_selected)


@app.route('/delete')
def delete():
    print("Triggerrs")
    book_id=request.args.get('id')
    book_delete= db.session.execute(db.select(Book).where(Book.id==book_id)).scalar()
    db.session.delete(book_delete)
    db.session.commit()
    print("Deleted")
    return redirect(url_for('home'))

    




if __name__ == "__main__":
    app.run(debug=True)







