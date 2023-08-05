
# this currently only includes a single meaningful function for testing

#the following class is for functions related to the retrieval of data - primarily sql
class get_data:
	def __init__(self,data):
		self.data = data

	def get_redshift_data(sql_string):
		import psycopg2
		import pandas as pd

		redshift_password = os.environ['redshift_pass']
		redshift_username = os.environ['redshift_user']

		redshift_connstring = "host='db-data-warehouse.sportpursuit.pro' dbname='sportpursuit' user='" + redshift_username + "' password='"+redshift_password+"' port='5439'"
		conn=psycopg2.connect(redshift_connstring)
		cur = conn.cursor()
		cur.execute(sql_string)
		column_names = [desc[0] for desc in cur.description]
		data = cur.fetchall()
		cur.close()
		conn.close()
		data = pd.DataFrame(data)
		data.columns = column_names
		return data