from flask import Flask, request
import json

class Employee :
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

database.add(1, Employee(1, "Jan", "Kowalski", "programistaooooooo"))

@app.route('/employee/<id>', methods=['GET','POST'])
def employee(id):
    if request.method == 'GET':
        return app.response_class(response=json.dumps(database[int(id)].__dict__),
                                  status=202,
                                  mimetype='application/json')

    if request.method == 'POST':
        if int(id) not in memory_database:
            name = request.json.get('name')
            surname = request.json.get('surname')
            position = request.json.get('position')
            database.add(Employee(id, name, surname, position))
            return app.response_class(response=json.dumps(Employee(id,name,surname,position).__dict__),
                                  status=201,
                                  mimetype='application/json')
        else:
            return app.response_class(response=f'Employee with id ={id} already exists',
                                  status=409,
                                  mimetype='application/text')



@app.route('/employees', methods=['GET'])
def employees():
    return app.response_class(response=json.dumps(database),
                                  status=202,
                                  mimetype='application/json')





if __name__ == '__main__':
    app.run()