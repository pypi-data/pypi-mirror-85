import maglev
import persistence

from typing import Any, List

class Persistence:
	"""
	Provides a way of storing data for mindpowered packages.
	When mindpowered packages need to persist data, they will use Get and Mutate, which in turn will call the Mutators and Getters you have set up.
	You can set up the Mutators and Getters however you like whether to access a database such as MySQL or MongoDB, or simply write and read from text files.
	Note: when using a mapping (updateMapper, queryMapper, resultMapper), the data will be passed in as the first argument to the mapping function.
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("persistence")
		lib = persistence.persistence_Persistence(bus)

	def AddMutator(self, recordType: str, operationName: str, strategyMethod: Any, updateMapper: Any, useRecordDataAsParams: bool):
		"""		Set up a Mutator to change stored data
		Args:
			recordType (str):type of record being changed (eg. databsae table name)
			operationName (str):action being performed on the record (eg. insert, update)
			strategyMethod (Any):method to call to actually perform the mutation
			updateMapper (Any):method to call on recordData before calling strategyMethod with the results
			useRecordDataAsParams (bool):if set to true, the recordData will be passed as the arguments to strategyMethod, rather than as the first argument
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("persistence")
		args = [recordType, operationName, strategyMethod, updateMapper, useRecordDataAsParams]
		pybus.call('Persistence.AddMutator', args);

	def AddGetter(self, recordType: str, operationName: str, strategyMethod: Any, queryMapper: Any, resultMapper: Any, useQueryValuesAsParams: bool):
		"""		Set up a Getter to retrieve data
		Args:
			recordType (str):type of record being retrieved (eg. databsae table name)
			operationName (str):query being performed for the record type (eg. findById, findByName, findActive, getInsertedId)
			strategyMethod (Any):method to call to actually perform the data retrieval
			queryMapper (Any):method to call on queryValues before calling strategyMethod with the results
			resultMapper (Any):method to call on data returned from the strategyMethod before returning the results
			useQueryValuesAsParams (bool):if set to true, the queryValues will be passed as the arguments to strategyMethod, rather than as the first argument
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("persistence")
		args = [recordType, operationName, strategyMethod, queryMapper, resultMapper, useQueryValuesAsParams]
		pybus.call('Persistence.AddGetter', args);

	def Mutate(self, recordType: str, operationName: str, recordData: Any):
		"""		Use a Mutator to change stored data
		Args:
			recordType (str):type of record being changed (eg. databsae table name)
			operationName (str):action being performed on the record (eg. insert, update)
			recordData (Any):data being updated or saved by passing through updateMapper and then strategyMethod
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("persistence")
		args = [recordType, operationName, recordData]
		pybus.call('Persistence.Mutate', args);

	def Get(self, recordType: str, operationName: str, queryValues: Any) -> Any:
		"""		Use a Getter to retrieve data
		Args:
			recordType (str):type of record being retrieved (eg. databsae table name)
			operationName (str):query being performed for the record type (eg. findById, findByName, findActive, getInsertedId)
			queryValues (Any):values that will be passed through queryMapper and then strategyMethod to perform the query
		Returns:
			result from the getter after being passed through resultMapper
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("persistence")
		args = [recordType, operationName, queryValues]
		ret = pybus.call('Persistence.Get', args);
		return ret;



