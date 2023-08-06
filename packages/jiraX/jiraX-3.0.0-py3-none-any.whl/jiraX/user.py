import logging
logging.basicConfig(level=logging.INFO)
from .base import Base


class User(Base):
	"""
	Class responsable for documentation sprints backlog in Jira
	"""
	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find(self,id_or_key): 
		try:
			logging.info("Start function: find")
	
			#TO DO
	
			logging.info("End function: find")
		except Exception as e: # NOSONAR
			logging.error("OS error: {0}".format(e))# NOSONAR
			logging.error(e.__dict__) # NOSONAR

	def find_by_project(self, project_key):
		"""
		Responsible for finding all users that have access to the project

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all Users with access to the project

		"""
		try:
			logging.info("Start function: find_by_project")
			return self.jira.search_assignable_users_for_projects("",project_key)
			logging.info("End function: find_by_project")
		except Exception as e: # NOSONAR
			logging.error("OS error: {0}".format(e))# NOSONAR
			logging.error(e.__dict__) # NOSONAR
	
