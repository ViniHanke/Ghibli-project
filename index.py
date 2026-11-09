#-------------------------------------------------------------------------------#
# Filename:   index.py
# Purpose:    Web app for the Ghibli Fans Website 
#             Requires a login to acces the forum pages or setting up a new user acount
#
#             1. creates the flask application
#             2. makes a database connection
#             3. Run SQL statemnts 
#             4. provides validations            
#             5. Provide web page content 
#
# Author:     Vinicius Hanke
# Created:    09//11/2026
# Version:    1.0
# Notes:      
#-------------------------------------------------------------------------------#
# IMPORT STATEMENTS
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from datetime import datetime
#-------------------------------------------------------------------------------#
# GLOBAL VARIABLES (accessible by all functions)
app = Flask (__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ghibli'
app.config['MYSQL-OPTIONS'] = {'ssl_ca' : 'C:/xampp/apache/conf/ca.pem'}

# secret key (can be any string value)
app.secret_key = 'totoro'

mysql = MySQL(app)

#-------------------------------------------------------------------------------#
# FUNCTIONS
#-------------------------------------------------------------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    # message for display if an error occurs
    msg = ''
    # show the login form with error message (if any)
    # ----------- Login TO DO ----------------- #

    # Show the login form with error message (if any)
    return render_template('login.html', msg=msg)
# end login() function

@app.route('/logout')
def logout():
    # ----------- Logout ----------- #
    try: 

        if ('loggedin' in session):
            # remove session data, this will log the user out
            session.pop('loggedin', None)
            session.pop('newreg', None)
            session.pop('username', None)
            session.pop('memberID', None)
            
            # redirect to login page
            return redirect(url_for('login'))
        else:
            # redirect to login page
            return redirect(url_for('login'))
    except:
            return redirect(url_for('login'))   
# end logout() function

@app.route('/register', methods=['GET', 'POST'])
def register():
    # register message 
    msg = ''
    # ----------- Register TO DO ----------------- #

    render_template('register.html', msg=msg)
    # end register() function

@app.route('/discussion', methods=['GET', 'POST'])
def discussion(MovieNbr):
    # discussion message 
    msg = ''
    # ----------- Discussion TO DO ----------------- #

    render_template('discussion.html', msg=msg)
    # end discussion() function

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    # movies message 
    msg = ''
    # ----------- Movies TO DO ----------------- #

    render_template('movies.html', msg=msg)
    # end movies() function

@app.route('/')
def home():
    # home message 
    msg = ''
    # ----------- Home TO DO ----------------- #

    render_template('login.html', msg=msg)
    # end home() function

# Function:    myFunction()
# Purpose:   
# Inputs:    
# Output:    
#-------------------------------------------------------------------------------#
def myFunction ():
    pass


#-------------------------------------------------------------------------------#
# Method:    main()
# Purpose:   entry point to the program
# Inputs:    void
# Output:    void
#-------------------------------------------------------------------------------#
def main():
    app.run(debug=True)
# end main() function

if __name__ == '__main__':
    main
    #---------------------------------------------------------------#
    # 1. DECLARE VARIABLES
    #---------------------------------------------------------------#
    
    
    
    #---------------------------------------------------------------#
    # 2. INPUTS
    #---------------------------------------------------------------#
    
    
    
    #---------------------------------------------------------------#
    # 3. PROCESS
    #---------------------------------------------------------------#
    
    
    
    #---------------------------------------------------------------#
    # 4. OUTPUTS
    #---------------------------------------------------------------#
       
# end main() function
#-------------------------------------------------------------------------------#
# call main() function if one exists
if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------#
