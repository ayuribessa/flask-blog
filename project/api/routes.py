from flask import jsonify, make_response
from flask_restful import Resource
from . import api
from project import db
from project.models import Task
################
#### routes ####
################

class TodoTasks(Resource):
	def get(self):
		results = db.session.query(Task).limit(10).offset(0).all()
		json_results = []
		for result in results:
			data = {
			'task_id': result.task_id,
			'task name': result.name,
			'due date': str(result.due_date),
			'priority': result.priority,
			'posted date': str(result.posted_date),
			'status': result.status,
			'user id': result.user_id
			}	
			json_results.append(data)
		return jsonify(items=json_results)

	def put(self):
		return {'error' : 'operação não permitida'}
		
	def delete(self):
		return {'error' : 'operação não permitida'}
    
	def post(self):
		return {'error' : 'operação não permitida'}

class TodoTask(Resource):
	def get(self,task_id):
		result = db.session.query(Task).filter_by(task_id=task_id).first()
		if result:
			result = {
				'task_id': result.task_id,
				'task name': result.name,
				'due date': str(result.due_date),
				'priority': result.priority,
				'posted date': str(result.posted_date),
				'status': result.status,
				'user id': result.user_id
			}	
			code = 200
		else:
			code = 404
			result = {"error": "Element does not exist"}
		return make_response(jsonify(result),code)

api.add_resource(TodoTasks,'/tasks/')
api.add_resource(TodoTask,'/task/<int:task_id>')
