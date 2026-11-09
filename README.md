# Ghibli Fans

A Flask web app for Studio Ghibli fans. The project includes page templates for logging in, registering, viewing movies, and discussing films. Some route functionality is still in progress.

## Requirements

- Python 3.9 or later
- MySQL or MariaDB
- The MySQL client development tools needed by `mysqlclient`

On macOS with Homebrew, install the client tools and `pkg-config`:

```bash
brew install pkg-config mysql-client
```

If Homebrew reports that `mysql-client` is keg-only, make its package metadata available to `pkg-config` in the terminal you use for installation:

```bash
export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

## Setup

Create and activate a virtual environment from the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python packages:

```bash
python -m pip install Flask Flask-MySQLdb
```

Create the database and load the sample tables and data:

```bash
mysql -u root -p < dev/ghibli.sql
```

Enter your MySQL password when prompted. The app currently expects a database named `ghibli`, a local MySQL server, user `root`, and an empty password. If your MySQL settings differ, update the MySQL configuration in `index.py` before running the app.

## Run

With the virtual environment active and MySQL running, start the Flask app:

```bash
python index.py
```

The app runs in Flask debug mode. Open the local address shown in the terminal, usually `http://127.0.0.1:5000`.

## Project structure

- `index.py` — Flask app and route definitions
- `templates/` — HTML templates
- `static/` — CSS, images, and other static assets
- `dev/ghibli.sql` — database schema and sample data

## Development status

The login, registration, movie, and discussion routes are present, but several route handlers are marked as unfinished in `index.py`. The app may need additional implementation before those features work end to end.
