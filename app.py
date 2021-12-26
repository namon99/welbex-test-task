import operator
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, json
from flask_migrate import Migrate

import settings
from models import db, SinglePageTable

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
app.config['SERVER_NAME'] = None

db.init_app(app)
migrate = Migrate(app, db)


def filter_table(column, condition, value):
    conditions = {
        'equals': operator.eq,
        'include': operator.contains,
        'greater': operator.gt,
        'less': operator.lt,
    }
    value = float(value) if value.isnumeric() else value
    try:
        value = datetime.strptime(value, "%d.%m.%Y").date()
    except:
        pass
    if not isinstance(value, str) and condition == 'include':
        return []
    data = [d for d in SinglePageTable.query.all() if conditions[condition](getattr(d, column), value)]
    return data


@app.route('/')
def index():
    data = SinglePageTable.query.all()
    columns = SinglePageTable.__table__.columns
    sorted_columns = [c for c in columns if c.info.get('sortered', False)]
    filtered_columns = [c for c in columns if c.info.get('filtered', False)]
    return render_template(
        'index.html',
        data=data, columns=columns, filtered_columns=filtered_columns,
        columns_name=[c.name for c in columns], sorted_columns=sorted_columns,
    )


@app.route('/filter/', methods=['POST'])
def filter_table_request():
    column = request.form['column']
    condition = request.form['condition']
    value = request.form['filter_value']
    data = filter_table(column, condition, value)
    data = [d.to_json() for d in data]
    return jsonify(data)


@app.route('/sort/', methods=['POST'])
def sort_table():
    sort_column = request.form['sort_column']
    column = request.form.get('column', None)
    condition = request.form.get('condition', None)
    value = request.form.get('filter_value', None)
    try:
        data = filter_table(column, condition, value)
    except:
        data = SinglePageTable.query.all()
    print(data)
    data.sort(key=lambda t: getattr(t, sort_column))
    data = [d.to_json() for d in data]
    return jsonify(data)


@app.route('/table/', methods=['POST'])
def get_table():
    data = SinglePageTable.query.all()
    data = [d.to_json() for d in data]
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
