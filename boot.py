import os
import simplejson as json
from flask import Flask, abort, make_response, url_for, request
# from models import db

basedir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(basedir, '/data/api.db')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DB_URI'] = 'sqlite:///' + db_file

data = [
    {'id': 1, 'company': 'my beautiful laundrette', 'active': True},
    {'id': 2, 'company': 'acme limited', 'active': False}
]


def Py2j(content, status=200, charset='utf-8', prefix=None):
    c_type = {'Content-type': 'application/json; charset={}'.format(charset)}

    if prefix:
        out = {}
        out[prefix] = content
        return json.dumps(out), status, c_type

    return json.dumps({'data': content}), status, c_type


def j2Py(content):
    return json.loads(content)


def data_link(it):
    nu_data = {}
    for field in it:
        if field == 'id':
            nu_data['uri'] = url_for('getOneData', res_id=it['id'], _external=True)
        else:
            nu_data[field] = it[field]
    return nu_data

"""
Get ALL (index)
"""


@app.route('/')
def index():
    # c = data
    return Py2j({'companies': [data_link(elem) for elem in data]})

"""
get ONE element from collection (/:id)
"""


@app.route('/<int:res_id>', methods=['GET'])
def getOneData(res_id):
    """
    try:
        result = data[res_id - 1]
    except:
        abort(404)
    """
    company = [company for company in data if company['id'] == int(res_id)]
    if len(company) == 0:
        abort(404)
    return Py2j(company[0], prefix='find_company')


@app.route('/create', methods=['POST'])
def create():
    if not request.json or not 'company' in request.json:
        abort(400)
    req = {
        'id': data[-1]['id'] + 1,
        'company': request.json['company'],
        'active': request.json.get('active', '') or False
    }
    data.append(req)
    return Py2j(req, prefix='created_successfully', status=201)


@app.route('/<int:data_id>/update', methods=['PUT'])
def update(data_id):
    target = [company for company in data if company['id'] == data_id]
    if len(target) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'company' in request.json and type(request.json['company']) is not str:
        abort(400)
    if 'active' in request.json and type(request.json['active']) is not bool:
        abort(400)
    target[0]['company'] = request.json.get('company', target[0]['company'])
    target[0]['active'] = request.json.get('active', target[0]['active'])
    return Py2j(target[0], prefix='updated_successfully', status=202)


@app.route('/<int:target>/delete', methods=['DELETE'])
def delete(target):
    casualty = [casualty for casualty in data if casualty['id'] == target]
    if len(casualty) == 0:
        abort(404)
    removed = casualty[0]
    data.remove(casualty[0])
    print(removed)
    return Py2j(removed, prefix='deleted_successfully', status=204)

"""
Thank you, Wikipedia: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
"""


@app.errorhandler(404)
def not_found(error):
    resp = make_response(json.dumps(
        {'error_code': 404, 'error_msg': 'Not found'}
        ), 404)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


@app.errorhandler(400)
def not_found(error):
    resp = make_response(json.dumps(
        {'error_code': 400, 'error_msg': 'Bad request.'}
        ), 400)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


@app.errorhandler(401)
def not_found(error):
    resp = make_response(json.dumps(
        {'error_code': 401, 'error_msg': 'Unauthorized.'}
        ), 401)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


@app.errorhandler(403)
def not_found(error):
    resp = make_response(json.dumps(
        {'error_code': 403, 'error_msg': 'Forbidden.'}
        ), 403)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


@app.errorhandler(405)
def not_found(error):
    resp = make_response(json.dumps(
        {'error_code': 405, 'error_msg': 'Method Not Allowed.'}
        ), 405)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


@app.errorhandler(406)
def not_found(error):
    resp = make_response(json.dumps(
        {'error_code': 406, 'error_msg': 'Not acceptable.'}
        ), 406)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
