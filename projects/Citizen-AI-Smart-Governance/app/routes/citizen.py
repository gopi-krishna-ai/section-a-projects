from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Application

bp = Blueprint('citizen', __name__)

@bp.before_request
@login_required
def require_login():
    pass

@bp.route('/dashboard')
def dashboard():
    return render_template('citizen/dashboard.html')

@bp.route('/workspace/<int:app_id>')
def workspace(app_id):
    # In a real app, query the Application model
    return render_template('citizen/workspace.html', app_id=app_id)

@bp.route('/new/<service_type>')
def new_application(service_type):
    # Mock creating a new app
    return redirect(url_for('citizen.workspace', app_id=1))

