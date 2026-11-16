# Ghibli Fans

A Flask and MySQL forum for browsing Studio Ghibli films and discussing each movie. Members can register, log in, view comments, and create, update, or delete their own comments.

## Requirements

- Python 3.9 or later
- XAMPP with its MySQL/MariaDB server, or another local MySQL-compatible server
- The MySQL client development tools required by `mysqlclient`

On macOS with Homebrew, install the client tools and `pkg-config` if needed:

```bash
brew install pkg-config mysql-client
```

If Homebrew reports that `mysql-client` is keg-only, make its package metadata available in the terminal used to install Python packages:

```bash
export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

## Set up the database

1. Start MySQL in XAMPP.
2. In phpMyAdmin, import `dev/ghibli.sql`. This creates the `ghibli` database, its `member`, `movie`, and `discussion` tables, and the supplied sample data.
3. The default local settings in `index.py` use host `127.0.0.1`, user `root`, an empty password, and database `ghibli`. If your XAMPP MySQL settings differ, update those values in `index.py`.

The SQL file creates a fresh database. Do not import it over a database containing records you need to keep unless you have backed up that database first.

## Set up and run the app

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Flask Flask-MySQLdb
python index.py
```

Open <http://127.0.0.1:5000/>. Set `FLASK_SECRET_KEY` to a private value in your terminal before running the app outside local coursework use.

## Sample accounts

The supplied SQL data includes these accounts:

| Username | Password | Member |
| --- | --- | --- |
| `jimmy123` | `jimmy123` | Jimmy Page |
| `will123` | `will123` | Will Stanford |

These are coursework sample credentials and should not be used in a public deployment.

## Features

- Register a member with server-side validation and duplicate username/email checks.
- Log in against the `member` table and keep the member ID and display name in a Flask session.
- Restrict movie and discussion pages to logged-in members.
- Display the movie catalogue from MySQL with clickable poster images and title search links.
- Display all comments for a selected movie. Members can add comments and edit or delete only comments they own.
- Use parameterized SQL for database values and Jinja's automatic HTML escaping for displayed content.

## Project structure

- `index.py` — Flask routes, validation, session handling, and SQL operations
- `templates/` — login, registration, movie, discussion, and logout page templates
- `static/css/style.css` — site styling
- `static/movie_img/` — movie posters named by `movieID`
- `static/img/` — site logo and favicon
- `dev/ghibli.sql` — database schema and sample data

## Data and security notes

The supplied database schema stores passwords in a 12-character text field. To remain compatible with the provided sample accounts and schema, this coursework version compares those stored passwords directly. A public deployment should migrate to a password-hash column and use a production secret key, HTTPS, CSRF protection, and a restricted database account.
