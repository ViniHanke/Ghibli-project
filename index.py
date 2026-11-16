"""Flask application for the Ghibli Fans movie discussion forum."""

import os
import re
from datetime import datetime

import MySQLdb.cursors
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.update(
    MYSQL_HOST='127.0.0.1',
    MYSQL_USER='root',
    MYSQL_PASSWORD='',
    MYSQL_DB='ghibli',
)

# Development key for local coursework. Set FLASK_SECRET_KEY before deployment.
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'totoro')

mysql = MySQL(app)


def _logged_in():
    """Return whether a member has an active login session."""
    return 'loggedin' in session


def _discussion_url(movie_id):
    return redirect(url_for('discussion', movie_id=movie_id))


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if _logged_in():
        return redirect(url_for('movies'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Enter both your username and password.', 'error')
            return render_template('login.html')

        cursor = None
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT memberID, member_name, usrid, usrpwd '
                'FROM member WHERE usrid = %s',
                (username,),
            )
            member = cursor.fetchone()
        except Exception:
            app.logger.exception('Database error while checking login')
            flash('The login service could not reach the database. Try again.', 'error')
            return render_template('login.html')
        finally:
            if cursor is not None:
                cursor.close()

        if member is None or member['usrpwd'] != password:
            flash('Incorrect username or password.', 'error')
            return render_template('login.html')

        session.clear()
        session['loggedin'] = True
        session['memberID'] = member['memberID']
        session['member_name'] = member['member_name']
        session['username'] = member['usrid']
        return redirect(url_for('movies'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if _logged_in():
        flash('Log out before creating another account.', 'error')
        return redirect(url_for('movies'))

    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()

        error = None
        if not fullname or len(fullname) > 64:
            error = 'Enter a name of 1 to 64 characters.'
        elif not re.fullmatch(r'[A-Za-z0-9]{1,12}', username):
            error = 'Username must be 1 to 12 letters or numbers.'
        elif not 6 <= len(password) <= 12:
            error = 'Password must be between 6 and 12 characters.'
        elif len(email) > 64 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            error = 'Enter a valid email address of 64 characters or fewer.'

        if error:
            flash(error, 'error')
            return render_template('register.html')

        cursor = None
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT memberID FROM member WHERE usrid = %s OR email = %s',
                (username, email),
            )
            if cursor.fetchone() is not None:
                flash('That username or email is already registered.', 'error')
                return render_template('register.html')

            cursor.execute(
                'INSERT INTO member (member_name, email, usrid, usrpwd) '
                'VALUES (%s, %s, %s, %s)',
                (fullname, email, username, password),
            )
            mysql.connection.commit()
        except Exception:
            mysql.connection.rollback()
            app.logger.exception('Database error while registering member')
            flash('Registration could not be saved. Try again.', 'error')
            return render_template('register.html')
        finally:
            if cursor is not None:
                cursor.close()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/movies')
def movies():
    if not _logged_in():
        flash('Log in to view the movie list.', 'error')
        return redirect(url_for('login'))

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT movieID, title, releaseYear, director, length, rating '
            'FROM movie ORDER BY movieID'
        )
        movie_rows = cursor.fetchall()
    except Exception:
        app.logger.exception('Database error while loading movies')
        flash('The movie list could not be loaded. Try again.', 'error')
        return redirect(url_for('login'))
    finally:
        if cursor is not None:
            cursor.close()

    return render_template('movies.html', movies=movie_rows)


@app.route('/discussion/<int:movie_id>')
def discussion(movie_id):
    if not _logged_in():
        flash('Log in to view movie discussions.', 'error')
        return redirect(url_for('login'))

    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT movieID, title FROM movie WHERE movieID = %s',
            (movie_id,),
        )
        movie = cursor.fetchone()
        if movie is None:
            flash('That movie could not be found.', 'error')
            return redirect(url_for('movies'))

        cursor.execute(
            'SELECT d.discussionID, d.memberID, d.comments, d.commentDate, '
            'm.member_name, m.usrid '
            'FROM discussion AS d '
            'JOIN member AS m ON m.memberID = d.memberID '
            'WHERE d.movieID = %s ORDER BY d.discussionID',
            (movie_id,),
        )
        comments = cursor.fetchall()
    except Exception:
        app.logger.exception('Database error while loading discussion')
        flash('The discussion could not be loaded. Try again.', 'error')
        return redirect(url_for('movies'))
    finally:
        if cursor is not None:
            cursor.close()

    return render_template('discussion.html', movie=movie, comments=comments)


@app.route('/discussion/add', methods=['POST'])
def add_comment():
    if not _logged_in():
        flash('Log in before adding a comment.', 'error')
        return redirect(url_for('login'))

    movie_id = request.form.get('movie_id', type=int)
    comment_text = request.form.get('comment', '').strip()
    if movie_id is None:
        flash('The movie selection is invalid.', 'error')
        return redirect(url_for('movies'))
    if not comment_text or len(comment_text) > 256:
        flash('A comment must contain 1 to 256 characters.', 'error')
        return _discussion_url(movie_id)

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO discussion (memberID, movieID, commentDate, comments) '
            'VALUES (%s, %s, %s, %s)',
            (session['memberID'], movie_id, datetime.now().strftime('%d-%b-%Y'), comment_text),
        )
        mysql.connection.commit()
        flash('Your comment was added.', 'success')
    except Exception:
        mysql.connection.rollback()
        app.logger.exception('Database error while adding comment')
        flash('Your comment could not be saved.', 'error')
    finally:
        if cursor is not None:
            cursor.close()
    return _discussion_url(movie_id)


@app.route('/discussion/update', methods=['POST'])
def update_comment():
    if not _logged_in():
        flash('Log in before editing a comment.', 'error')
        return redirect(url_for('login'))

    movie_id = request.form.get('movie_id', type=int)
    discussion_id = request.form.get('discussion_id', type=int)
    comment_text = request.form.get('comment', '').strip()
    if movie_id is None:
        flash('The movie selection is invalid.', 'error')
        return redirect(url_for('movies'))
    if discussion_id is None or not comment_text or len(comment_text) > 256:
        flash('Choose a comment and enter 1 to 256 characters.', 'error')
        return _discussion_url(movie_id)

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE discussion SET comments = %s '
            'WHERE discussionID = %s AND memberID = %s AND movieID = %s',
            (comment_text, discussion_id, session['memberID'], movie_id),
        )
        mysql.connection.commit()
        flash('Your comment was updated.' if cursor.rowcount else 'That comment was not found or is not yours.',
              'success' if cursor.rowcount else 'error')
    except Exception:
        mysql.connection.rollback()
        app.logger.exception('Database error while updating comment')
        flash('Your comment could not be updated.', 'error')
    finally:
        if cursor is not None:
            cursor.close()
    return _discussion_url(movie_id)


@app.route('/discussion/delete', methods=['POST'])
def delete_comment():
    if not _logged_in():
        flash('Log in before deleting a comment.', 'error')
        return redirect(url_for('login'))

    movie_id = request.form.get('movie_id', type=int)
    discussion_id = request.form.get('discussion_id', type=int)
    if movie_id is None:
        flash('The movie selection is invalid.', 'error')
        return redirect(url_for('movies'))
    if discussion_id is None:
        flash('Choose a comment to delete.', 'error')
        return _discussion_url(movie_id)

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            'DELETE FROM discussion '
            'WHERE discussionID = %s AND memberID = %s AND movieID = %s',
            (discussion_id, session['memberID'], movie_id),
        )
        mysql.connection.commit()
        flash('Your comment was deleted.' if cursor.rowcount else 'That comment was not found or is not yours.',
              'success' if cursor.rowcount else 'error')
    except Exception:
        mysql.connection.rollback()
        app.logger.exception('Database error while deleting comment')
        flash('Your comment could not be deleted.', 'error')
    finally:
        if cursor is not None:
            cursor.close()
    return _discussion_url(movie_id)


if __name__ == '__main__':
    app.run(debug=True)
