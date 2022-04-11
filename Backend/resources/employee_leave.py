from flask_restful import Resource, reqparse
from db import *

class EmployeeLeave(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('category',
                        type=str,
                        required=False,
                        help="optional"
                        )

    def get(self, category):
        query = f"SELECT * FROM employee_leave WHERE LOWER(el_category) = '{category.lower()}'"
        res = execute_read_query_dict(db_conn, query)
        if res:
            return {"employee leave type": res}, 200
        return {'message': 'title not found'}, 404

    def post(self, category):
        query = f"SELECT * FROM employee_leave WHERE el_category='{category.lower()}'"
        res = execute_read_query(db_conn, query)
        if res:
            return {'message': "A Cateogry with name '{}' already exists.".format(category)}, 400

        # get input data
        insert = f"INSERT INTO employee_leave(el_category) VALUES('{category.lower()}')"
        execute_query(db_conn, insert)

        return {'message': 'record added'}, 200

    def delete(self, category):
        query = f"SELECT * FROM employee_leave WHERE el_category='{category.lower()}'"
        res = execute_read_query(db_conn, query)
        if res:
            delete_query = f"DELETE FROM employee_leave WHERE LOWER(el_category) = '{category.lower()}'"
            execute_query(db_conn, delete_query)
        else:
            return {'message': 'title not found'}, 404
        return {'message': 'record deleted'}

    def put(self, category):
        pass


class EmployeeLeaveList(Resource):
    def get(self):
        query = 'SELECT * FROM employee_leave'
        res = execute_read_query_dict(db_conn, query)
        return {'employee quit type': res}, 200