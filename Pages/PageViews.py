import ast
import json

from flask import Blueprint, flash, render_template, request

from OIDC_Module import oidc
from db_actions import PostgersqlDBManagement, SQLiteDBManagement

pages = Blueprint('pages', __name__, static_folder='static', static_url_path="/Pages/static",
                  template_folder='templates', )


@pages.route('/my/Page1')
@oidc.require_login
def page_1():
    flash('Authorized!', 'success')
    return render_template('Page1.html')


# user and Guest
@pages.route('/my/Page2')
@oidc.require_login
def page_2():
    flash('Authorized!', 'success')
    return render_template('Page2.html')


# Page3 user and admin
@pages.route('/my/Page3')
@oidc.require_login
def page_3():
    flash('Authorized!', 'success')
    return render_template('Page3.html')


# Page 4 only admin access where you can see the admin panel
@pages.route('/my/Page4')
@oidc.require_login
def page_4():
    flash('Authorized!', 'success')
    return render_template('Page4.html')


@pages.route('/my/Admin')
@oidc.require_login
def page_admin():
    flash('Authorized!', 'success')
    return render_template('PageAdmin.html')


@pages.route('/my/Postgres', methods=["GET", "POST"])
@oidc.require_login
def page_postgres():
    table_name = 'batch'
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    return render_template("table_view.html", table_name=table_name, db_name="Postgres",
                           column_names=database.get_table_columns(table_name),
                           table=database.get_table(table_name))


@pages.route("/my/Postgres/delete_batch_id_array", methods=["POST"])
@oidc.require_login
def delete_from_table_by_id_postgres():
    table_name = 'batch'
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    database.delete(tablename=table_name, column="batch_inspectionid",
                    condition=ast.literal_eval(request.form.get('data')))
    return "True"


@pages.route("/my/Postgres/delete_batch_name_array", methods=["POST"])
@oidc.require_login
def delete_from_table_by_name_postgres():
    table_name = 'batch'
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    database.delete(tablename=table_name, column="batchname",
                    condition=ast.literal_eval(request.form.get('data')))
    return "True"


@pages.route('/my/SQLite', methods=["GET", "POST"])
@oidc.require_login
def page_sqlite():
    table_name = 'batch'
    with open("parameters.json") as file:
        data = json.load(file)
        database = SQLiteDBManagement(path_to_sqlite_db=data["sqlite_path"])
    return render_template("table_view.html", table_name=table_name, db_name="SQLite",
                           column_names=database.get_table_columns(table_name),
                           table=database.get_table(table_name))


@pages.route("/my/SQLite/delete_batch_id_array", methods=["POST"])
@oidc.require_login
def delete_from_table_by_id_sqlite():
    table_name = 'batch'
    with open("parameters.json") as file:
        data = json.load(file)
        database = SQLiteDBManagement(path_to_sqlite_db=data["sqlite_path"])
    database.delete(tablename=table_name, column="batch_inspectionid",
                    condition=ast.literal_eval(request.form.get('data')))
    return "True"


@pages.route("/my/SQLite/delete_batch_name_array", methods=["POST"])
@oidc.require_login
def delete_from_table_by_name_sqlite():
    table_name = 'batch'
    with open("parameters.json") as file:
        data = json.load(file)
        database = SQLiteDBManagement(path_to_sqlite_db=data["sqlite_path"])
    database.delete(tablename=table_name, column="batchname",
                    condition=ast.literal_eval(request.form.get('data')))
    return "True"
