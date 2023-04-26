from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import functools
from werkzeug.security import check_password_hash, generate_password_hash

# redirect for auth folder
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Redirect user to home page
    return render_template("auth/login.html")
  
@bp.route("/logout")
def logout():
    """Log user out"""
    redirect(url_for("index"))
  
@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    return render_template("auth/register.html")