class Database:
	def __init__(self, name):
		"""
		:type name: str
		"""
		self._name = name.strip()

	def __str__(self):
		return str(self.name)

	def __repr__(self):
		return f'<database: {self.name}>'

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return self._name


class Schema:
	def __init__(self, name, database=None):
		"""
		:type name: str
		:type database: Database
		"""
		self._name = name.strip()
		self._database = database

	def __str__(self):
		if self.database is None:
			return str(self.name)
		else:
			return f'{self.database.name}.{self.name}'

	def __repr__(self):
		return f'<schema: {self.name}'

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return self._name

	@property
	def database(self):
		"""
		:rtype: Database
		"""
		return self._database
