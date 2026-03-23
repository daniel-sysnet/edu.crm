from flask import Blueprint, render_template

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="../../templates/dashboard",
    url_prefix="/dashboard",
)


@dashboard_bp.route("/")
def index():
    return render_template("dashboard/index.html")
