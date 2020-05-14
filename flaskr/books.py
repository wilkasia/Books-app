from flask import (
    Blueprint, g, flash, redirect, render_template, request, url_for
)
from datetime import datetime
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('books', __name__)


@bp.route('/books', methods=('GET', 'POST'))
def all_books():
    books = get_all_books()
    return render_template('books/books.html', books=books)


@bp.route('/add_book', methods=('GET', 'POST'))
@login_required
def add_book():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        if not author:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "INSERT INTO books(author, title, description) VALUES (%s,  %s, %s)",
                (author, title, description)
            )
            db.commit()
            cursor.close()
            return redirect(url_for('books.all_books'))

    return render_template('books/add_book.html')


@bp.route('/<int:book_id>/borrow', methods=('GET', 'POST'))
@login_required
def borrow(book_id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "UPDATE books SET status=0 WHERE id=%s",
        (book_id,)
    )
    db.commit()

    cursor.execute(
        "INSERT INTO user_books (user_id, book_id, rent_date) VALUES (%s, %s, %s)",
        (g.user['id'], book_id, datetime.now())
    )
    db.commit()
    cursor.close()

    return redirect(url_for('books.all_books'))


@bp.route('/<int:user_book_id>/<int:book_id>/return', methods=('GET', 'POST'))
@login_required
def return_book(user_book_id, book_id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "UPDATE user_books SET return_date=%s WHERE id=%s",
        (datetime.now(), user_book_id)
    )
    db.commit()

    cursor.execute(
        "UPDATE books SET status=1 WHERE id=%s",
        (book_id,)
    )
    db.commit()
    cursor.close()

    return redirect(url_for('books.user_books'))


def get_all_books():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, author, title, description, status FROM books ORDER BY author"
    )

    books = cursor.fetchall()
    cursor.close()
    return books


def get_book(book_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM books WHERE id=%s",
        (book_id,)
    )
    book = cursor.fetchone()
    cursor.close()

    return book


@bp.route('/user_books', methods=('GET', 'POST'))
@login_required
def user_books():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT ub.id, ub.book_id, ub.rent_date, b.author, b.title FROM user_books ub "
        "LEFT JOIN books b ON ub.book_id = b.id WHERE user_id = %s AND return_date IS NULL "
        "ORDER BY rent_date DESC",
        (g.user['id'],)
    )

    books = cursor.fetchall()
    print(books)
    cursor.close()
    return render_template('books/user_books.html', books=books)


@bp.route('/history', methods=('GET', 'POST'))
@login_required
def history():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT ub.rent_date, ub.return_date, b.author, b.title FROM user_books ub "
        "LEFT JOIN books b ON ub.book_id = b.id WHERE user_id = %s AND return_date IS NOT NULL "
        "ORDER BY return_date DESC",
        (g.user['id'],)
    )

    books = cursor.fetchall()
    cursor.close()
    return render_template('books/history.html', books=books)


@bp.route('/<int:book_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(book_id):
    book = get_book(book_id)

    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        if not author:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                'UPDATE books SET author = %s, title = %s, description = %s'
                ' WHERE id = %s',
                (author, title, description, book_id)
            )
            cursor.close()
            db.commit()
            return redirect(url_for('books.all_books'))

    return render_template('books/edit.html', book=book)


@bp.route('/<int:book_id>/delete_book', methods=('GET', 'POST'))
@login_required
def delete_book(book_id):
    get_book(book_id)
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
    cursor.close()
    db.commit()
    return redirect(url_for('books.all_books'))