
from lib.workshop import *

from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, Blueprint, render_template_string
from flask_user import current_user, login_required, roles_required, UserManager


app = Blueprint('users', __name__, template_folder='templates')



# The Home page is accessible to anyone
@app.route('/user/all')
def home_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('users.home_page') }}>Home Page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('users.member_page') }}>Member Page</a> (login_required: member@example.com / Password1)</p>
                <p><a href={{ url_for('users.admin_page') }}>Admin Page</a> (role_required: admin@example.com / Password1')</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)

# The Members page is only accessible to authenticated users
@app.route('/user/members')
@login_required    # Use of @login_required decorator
def member_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('users.home_page') }}>Home Page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('users.member_page') }}>Member Page</a> (login_required: member@example.com / Password1)</p>
                <p><a href={{ url_for('users.admin_page') }}>Admin Page</a> (role_required: admin@example.com / Password1')</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)

# The Admin page requires an 'Admin' role.
@app.route('/user/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Admin Page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('users.home_page') }}>Home Page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('users.member_page') }}>Member Page</a> (login_required: member@example.com / Password1)</p>
                <p><a href={{ url_for('users.admin_page') }}>Admin Page</a> (role_required: admin@example.com / Password1')</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)


