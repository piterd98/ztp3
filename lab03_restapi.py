from flask import Flask, request
import json


class Employee:
    def __init__(self, id, name, surname, position):
            self.id = id
            self.name = name
            self.surname = surname
            self.position = position

    @property
    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'position': self.position
        }


class memory_database(dict):

    def add(self, key, value):
        self[key] = value


app = Flask(__name__)

database = memory_database()

database.add(1, Employee(1, "Jan", "Kowalski", "programista"))


@app.route('/employee/<id>', methods=['GET','POST','PUT'])
def employee(id):
    id = int(id)
    if request.method == 'GET':
        return app.response_class(response=json.dumps(database[id].__dict__),
                                  status=202,
                                  mimetype='application/json')

    if request.method == 'POST':
        if id not in database.keys():
            name = request.json.get('name')
            surname = request.json.get('surname')
            position = request.json.get('position')
            database.add(id, Employee(id, name, surname, position))
            return app.response_class(response=json.dumps(Employee(id, name, surname, position).__dict__),
                                  status=202,
                                  mimetype='application/json')
        else:
            return app.response_class(response=f'Employee with {id = } already exists',
                                  status=409,
                                  mimetype='application/text')

    if request.method == 'PUT':
        if id in database.keys():
            name = request.json.get('name')
            surname = request.json.get('surname')
            position = request.json.get('position')
            database.add(id, Employee(id, name, surname, position))
            return app.response_class(response=json.dumps(Employee(id, name, surname, position).__dict__),
                                  status=202,
                                  mimetype='application/json')
        else:
            return app.response_class(response=f'Employee with {id = } could not be found',
                                  status=404,
                                  mimetype='application/text')




@app.route('/employees', methods=['GET'])
def employees():
    return app.response_class(response=json.dumps({emp.id: emp.__dict__ for emp in database.values()}),
                                  status=202,
                                  mimetype='application/json')


if __name__ == '__main__':
    app.run()