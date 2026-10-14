from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

bp = Blueprint('admin', __name__)

@bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin():
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.index'))

@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

