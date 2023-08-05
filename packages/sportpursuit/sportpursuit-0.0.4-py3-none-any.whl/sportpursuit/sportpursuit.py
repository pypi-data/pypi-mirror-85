#the following class is for functions related to the retrieval of data - primarily sql
class GetData:
	def __init__(self,data):
		self.data = data

	def get_secret(secret_name): 
		import boto3

		region_name = "eu-west-1"

		# Create a Secrets Manager client
		session = boto3.session.Session()
		client = session.client(
		    service_name='secretsmanager',
		    region_name=region_name
		)

		# In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
		# See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
		# We rethrow the exception by default.

		try:
		    get_secret_value_response = client.get_secret_value(
		        SecretId=secret_name
		    )
		except ClientError as e:
		    if e.response['Error']['Code'] == 'DecryptionFailureException':
		        # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
		        # Deal with the exception here, and/or rethrow at your discretion.
		        raise e
		    elif e.response['Error']['Code'] == 'InternalServiceErrorException':
		        # An error occurred on the server side.
		        # Deal with the exception here, and/or rethrow at your discretion.
		        raise e
		    elif e.response['Error']['Code'] == 'InvalidParameterException':
		        # You provided an invalid value for a parameter.
		        # Deal with the exception here, and/or rethrow at your discretion.
		        raise e
		    elif e.response['Error']['Code'] == 'InvalidRequestException':
		        # You provided a parameter value that is not valid for the current state of the resource.
		        # Deal with the exception here, and/or rethrow at your discretion.
		        raise e
		    elif e.response['Error']['Code'] == 'ResourceNotFoundException':
		        # We can't find the resource that you asked for.
		        # Deal with the exception here, and/or rethrow at your discretion.
		        raise e
		else:
		    # Decrypts secret using the associated KMS CMK.
		    # Depending on whether the secret is a string or binary, one of these fields will be populated.
		    if 'SecretString' in get_secret_value_response:
		        json_secret = get_secret_value_response['SecretString']
		    else:
		        json_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
		    return json_secret



	def get_secret_jupyter(secret_name): 
		region_name = "eu-west-1"

		# Create a Secrets Manager client
		session = boto3.session.Session(profile_name='production')
		client = session.client(
			service_name='secretsmanager',
			region_name=region_name
		)

		# In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
		# See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
		# We rethrow the exception by default.

		try:
			get_secret_value_response = client.get_secret_value(
				SecretId=secret_name
			)
		except ClientError as e:
			if e.response['Error']['Code'] == 'DecryptionFailureException':
				# Secrets Manager can't decrypt the protected secret text using the provided KMS key.
				# Deal with the exception here, and/or rethrow at your discretion.
				raise e
			elif e.response['Error']['Code'] == 'InternalServiceErrorException':
				# An error occurred on the server side.
				# Deal with the exception here, and/or rethrow at your discretion.
				raise e
			elif e.response['Error']['Code'] == 'InvalidParameterException':
				# You provided an invalid value for a parameter.
				# Deal with the exception here, and/or rethrow at your discretion.
				raise e
			elif e.response['Error']['Code'] == 'InvalidRequestException':
				# You provided a parameter value that is not valid for the current state of the resource.
				# Deal with the exception here, and/or rethrow at your discretion.
				raise e
			elif e.response['Error']['Code'] == 'ResourceNotFoundException':
				# We can't find the resource that you asked for.
				# Deal with the exception here, and/or rethrow at your discretion.
				raise e
		else:
			# Decrypts secret using the associated KMS CMK.
			# Depending on whether the secret is a string or binary, one of these fields will be populated.
			if 'SecretString' in get_secret_value_response:
				json_secret = get_secret_value_response['SecretString']
			else:
				json_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
			return json_secret



	def get_redshift_credentials():
		import os
		# need to make sure credentials work either locally or in the cloud

		# reads the stored credentials on the system
		redshift_password = os.environ['redshift_password']
		redshift_username = os.environ['redshift_username']

		# if there are no local credentials then call the secrets function
		if redshift_password is None:
			redshift_password = get_secret("database/redshift/dataops")
			redshift_username = "dataops"

		if redshift_username is None:
			raise Exception('Redshift Username failed to read')

		if redshift_password is None:
			raise Exception('Redshift Password failed to read')

		return redshift_username, redshift_password


	def get_redshift_data(sql_string):
		import os
		import psycopg2
		import pandas as pd

		# reads the stored credentials on the system
		redshift_username, redshift_password = GetData.get_redshift_credentials()

		# puts everything together into a connection string
		redshift_connstring = "host='db-data-warehouse.sportpursuit.pro' dbname='sportpursuit' user='" + redshift_username + "' password='"+redshift_password+"' port='5439'"
		conn=psycopg2.connect(redshift_connstring)
		cur = conn.cursor()

		# runs the sql against the database
		cur.execute(sql_string)

		# gets the column names for the dataframe
		column_names = [desc[0] for desc in cur.description]
		data = cur.fetchall()
		cur.close()
		conn.close()

		# converts results into a dataframe and returns them
		data = pd.DataFrame(data)
		data.columns = column_names
		return data

	def execute_redshift_command(sql_string):
		import os
		import psycopg2

		# reads the stored credentials on the system
		redshift_username, redshift_password = GetData.get_redshift_credentials()

		# puts everything together into a connection string
		redshift_connstring = "host='db-data-warehouse.sportpursuit.pro' dbname='sportpursuit' user='" + redshift_username + "' password='"+redshift_password+"' port='5439'"
		conn = psycopg2.connect(redshift_connstring)
		cur = conn.cursor()

		# runs the sql against the database
		cur.execute(sql_string)

		# tells redshift to commit whatever command we submitted before
		conn.commit()

		cur.close()
		conn.close()

		# nothing to return
		# return the input so at least it's doing something we can check
		return sql_string