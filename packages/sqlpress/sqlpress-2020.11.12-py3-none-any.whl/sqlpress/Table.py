from slytherin.collections import find_duplicates
from .Database import Schema


class Column:
	def __init__(self, name, table, alias=None):
		self._table = table
		self._name = name
		self._alias = alias

	@property
	def alias(self):
		return self._alias

	@alias.setter
	def alias(self, alias):
		self._alias = alias

	@property
	def table(self):
		"""
		:rtype: Table
		"""
		return self._table

	@property
	def name(self):
		return self._name

	def get_select_statement(self, prefix=None, suffix=None):
		if prefix is None and suffix is None:
			alias = self.alias
		elif prefix is not None and suffix is not None:
			alias = f'{prefix}{self.name}{suffix}'
		else:
			ValueError('either both prefix and suffix should be None or both should have value')

		if alias is None:
			return f'{self.table.alias_or_name}.{self.name}'
		else:
			return f'{self.table.alias_or_name}.{self.name} as {alias}'

class Table:
	def __init__(self, columns, name, schema=None, alias=None):
		"""
		:type columns: list[str]
		:type schema: str or Schema
		"""
		duplicates = find_duplicates(items=columns)
		if len(duplicates) > 0:
			raise ValueError(f'Duplicate columns: {", ".join(duplicates)}')
		self._columns = [Column(name=x, table=self) for x in columns]
		self._schema = schema
		self._name = name.strip()
		self._alias = alias

	def set_column_prefix_and_suffix(self, prefix, suffix):
		for column in self.columns:
			column.alias = f'{prefix}{column.name}{suffix}'

	@property
	def columns(self):
		"""
		:rtype: list[Column]
		"""
		return self._columns

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return self._name

	@property
	def schema(self):
		"""
		:rtype: Schema
		"""
		return self._schema

	def __str__(self):
		if self.schema is None:
			return str(self.name)
		else:
			return f'{str(self.schema)}.{self.name}'

	@property
	def alias(self):
		return self._alias

	@property
	def alias_or_name(self):
		return self.alias or self.name

	def get_from_statement(self):
		if self.alias is None:
			return f'from {str(self)}'
		else:
			return f'from {str(self)} as {self.alias}'

	def get_select_statement(self, indentation=''):
		lines = [indentation + 'select']
		for i, column in enumerate(self.columns):
			lines.append(f'{indentation}\t' + column.get_select_statement())
		lines.append(indentation + self.get_from_statement())
		return '\n'.join(lines)

	def print(self, **kwargs):
		print(self.get_select_statement(**kwargs))

	def join(self, other, type, prefixes, suffixes):
		"""
		:type other: Table
		:type prefixes: list[str] or tuple[str]
		:type suffixes: list[str] or tuple[str]
		:rtype: Join
		"""
		return Join(items=[self, other], prefixes=prefixes, suffixes=suffixes, join_type=type)

	def __eq__(self, other):
		return self.alias_or_name == other.alias_or_name

	def inner_join(self, **kwargs):
		return self.join(type='inner', **kwargs)

	def outer_join(self, **kwargs):
		return self.join(type='outer', **kwargs)

	def left_join(self, **kwargs):
		return self.join(type='left', **kwargs)

	def right_join(self, **kwargs):
		return self.join(type='right', **kwargs)

	def get_intersection(self, other, exclude=None):
		"""
		:type other: Table
		:rtype: list[str]
		"""
		if exclude is None:
			exclude = {}
		else:
			exclude = set(exclude)

		return [column for column in self.columns if column in other.columns and column not in exclude]


class Join:
	def __init__(self, items, prefixes, suffixes, join_type='inner', exclude_columns=None):
		"""
		:type items: list[Table or Join]
		:type prefixes: list[str] or str
		:type suffixes: list[str] or str
		"""
		if len(items) != 2:
			raise ValueError(f'there are {len(items)} items!')

		if not isinstance(items, (tuple, list)):
			raise TypeError(f'items should be either a list or a tuple!')

		if not isinstance(items[0], (Join, Table)):
			raise TypeError('the first item can only be a Join or a Table')
		if not isinstance(items[1], Table):
			raise TypeError('the second item can only be a Table')

		if isinstance(items[0], Join):
			if not isinstance(prefixes, (list, tuple)):
				prefixes = [None, prefixes]
			elif prefixes[0] is not None:
				raise TypeError('when joining a Join with a Table, the first prefix should be None')

			if not isinstance(suffixes, (list, tuple)):
				suffixes = [None, suffixes]
			elif suffixes[0] is not None:
				raise TypeError('when joining a Join with a Table, the first suffix should be None')

		if not isinstance(prefixes, (tuple, list)):
			raise TypeError(f'prefixes should be either a list or a tuple!')
		if not isinstance(suffixes, (tuple, list)):
			raise TypeError(f'suffixes should be either a list or a tuple!')

		if len(prefixes) != 2:
			raise ValueError(f'there are {len(prefixes)} prefixes!')
		if len(suffixes) != 2:
			raise ValueError(f'there are {len(suffixes)} suffixes!')

		self._items = list(items)
		self._prefixes = list(prefixes)
		self._suffixes = list(suffixes)

		if exclude_columns is None:
			self._exclude_columns = []
		elif isinstance(exclude_columns, str):
			self._exclude_columns = [exclude_columns]
		else:
			self._exclude_columns = list(exclude_columns)

		if isinstance(items[0], Table):
			if items[0] == items[1]:
				raise ValueError(f'the two tables have the same names/aliases')
		if isinstance(items[0], Join):
			for table in self.tables:
				if table == items[1]:
					raise ValueError(f'item 2 has the same name/alias as {table}')

		if join_type.lower() not in ['left', 'right', 'inner', 'outer']:
			raise ValueError(f'incorrect join type: {join_type}')
		self._join_type = join_type

	@property
	def join_type(self):
		"""
		:rtype:
		"""
		return self._join_type.lower()

	@property
	def tables(self):
		"""
		:rtype: list[Table]
		"""
		result = []
		for item in self.items:
			if isinstance(item, Table):
				result.append(item)
			else:
				result += item.tables
		return result

	@property
	def items(self):
		"""
		:rtype: list[Table or Join]
		"""
		return self._items

	@property
	def tables_and_prefixes_and_suffixes(self):
		"""
		:return: list[tuple[Table, str, str]]
		"""
		result = []
		for item, prefix, suffix in self.items:
			if isinstance(item, Table):
				if prefix is None or suffix is None:
					raise ValueError('prefix and suffix cannot be None for a Table')
				result.append((item, prefix, suffix))
			else:
				if prefix is not None or suffix is not None:
					raise ValueError('prefix and suffix should be None for a Join')
				result += item.tables_and_prefixes_and_suffixes
		return result

	def get_select_columns_statement(self, indentation=''):
		lines = [indentation + 'select']
		for table, prefix, suffix in self.tables_and_prefixes_and_suffixes:
			lines.append(f'{indentation}\t{table.alias_or_name} columns:')
			for column in table.columns:
				lines.append(f'{indentation}\t' + column.get_select_statement(prefix=prefix, suffix=suffix))
			lines.append(f'{indentation}\t ')
		lines.append(indentation + 'from')
		lines += self.get_from_statement_lines(indentation=indentation)
		return '\n'.join(lines)

	@property
	def left(self):
		"""
		:rtype: Join or Table
		"""
		return self.items[0]

	@property
	def columns(self):
		"""
		:rtype: list[Column]
		"""
		return self.left.columns + self.right.columns

	@property
	def right(self):
		"""
		:rtype: Table
		"""
		return self.items[1]

	def on_statement_lines(self, indentation=''):
		result = [indentation + 'on']
		if isinstance(self.left, Table):
			right_columns = {column.name: column for column in self.right.columns}
			for column in self.left.columns:
				if column.name in right_columns:
					right_column = right_columns[column.name]

					result.append(indentation + f'{}')

	def get_from_statement_lines(self, indentation=''):
		lines = []

		if isinstance(self.left, Join):
			lines += self.left.get_from_statement_lines(indentation=indentation)
		else:
			lines.append(indentation + self.left.get_from_statement())

		lines.append(f'{indentation}{self.join_type} join {self.right} as {self.right.alias_or_name}')

		lines.append(indentation + 'on')

		if isinstance(self.left, Join):




