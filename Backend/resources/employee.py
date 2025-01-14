
from flask_restful import Resource, reqparse
from db import *


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        # required=True,
                        # help="required"
                        )

    parser.add_argument('last_name',
                        type=str,
                        # required=True,
                        # help="required"
                        )

    parser.add_argument('phone',
                        type=str,
                        # required=True,
                        # help="required"
                        )

    parser.add_argument('email',
                        type=str,
                        # required=True,
                        # help="required"
                        )
    parser.add_argument('join_date',
                        type=str,
                        # required=True,
                        # help="required"
                        )
    parser.add_argument('quit_date',
                        type=str,
                        # required=False,
                        # help="optional"
                        )
    parser.add_argument('comment',
                        type=str,
                        # required=False,
                        # help="optional"
                        )
    parser.add_argument('employee_quit_id',
                        type=int,
                        # required=False,
                        # help="optional"
                        )
    parser.add_argument('job_title_id',
                        type=int,
                        # required=True,
                        # help="required"
                        )
    parser.add_argument('store_id',
                        type=int,
                        # required=True,
                        # help="required"
                        )
    # parser.add_argument('name', type=str, default='')
    # parser.add_argument('id', type=int, default='')

    def get(self, id):
        query = f"""SELECT 
        e.emp_id, e.e_first_name, e.e_last_name, e.e_phone, e.join_date, e.quit_date, e.e_comment,
        s.s_name, jt.jt_category, eq.eq_category
        FROM 
        employee as e
        JOIN store as s
        ON e.store_id = s.store_id
        JOIN job_title as jt
        ON e.job_title_id = jt.job_title_id
        LEFT JOIN employee_quit as eq
        ON e.employee_quit_id = eq.employee_quit_id
        WHERE e.emp_id = '{id}'"""
        res = execute_read_query_dict(db_conn, query)
        for i in res:
            if i['join_date'] != None:
                i['join_date'] = i['join_date'].strftime("%m/%d/%Y")
            if i['quit_date'] != None:
                i['quit_date'] = i['quit_date'].strftime("%m/%d/%Y")
        if res:
            return {"employee": res}, 200
        return {'message': 'type not found'}, 404

    def post(self):
        data = Employee.parser.parse_args()
        phone = (data['phone'])
        query = f"SELECT * FROM employee WHERE e_phone = '{phone}'"
        res = execute_read_query(db_conn, query)
        if res:
            return {'message': "employee already exists in the database"}, 400
        # get input data
        insert = f"INSERT INTO employee(e_first_name, e_last_name, e_phone, e_email, join_date, quit_date, e_comment, employee_quit_id, job_title_id, store_id) \
        VALUES('{data['first_name']}', '{data['last_name']}', '{data['phone']}', '{data['email']}', '{data['join_date']}', \
        '{data['quit_date']}', '{data['comment']}', {data['employee_quit_id']}, {data['job_title_id']}, \
        {data['store_id']})"
        execute_query(db_conn, insert)

        return {'message': 'record added'}, 200

    def delete(self, id):
        pass

    def put(self, id):
        pass


class EmployeeList(Resource):
    def get(self):
        query = """SELECT 
            e.emp_id, e.e_first_name, e.e_last_name, e.e_phone, e.join_date, e.quit_date, e.e_comment,
            s.s_name, jt.jt_category, eq.eq_category
            FROM 
            employee as e
            JOIN store as s
            ON e.store_id = s.store_id
            JOIN job_title as jt
            ON e.job_title_id = jt.job_title_id
            LEFT JOIN employee_quit as eq
            ON e.employee_quit_id = eq.employee_quit_id"""
        res = execute_read_query_dict(db_conn, query)
        for i in res:
            if i['join_date'] != None:
                i['join_date'] = i['join_date'].strftime("%m/%d/%Y")
            if i['quit_date'] != None:
                i['quit_date'] = i['quit_date'].strftime("%m/%d/%Y")
        return {"employees": res}
