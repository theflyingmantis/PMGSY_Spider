import csv
import os
from config import OUTPUT_FILENAME

class PMGSYDataDumper:
	"""
	Dumps the data for all Gram Panchayats in csv file in data folder
	"""
	def __init__(self,data_dir_path):
		self.filepath = os.path.join(data_dir_path, OUTPUT_FILENAME)

	def createHeading(self):
		"""
		Creates heading for the csv file
		"""
		fieldNames = ['Year','Month','State','District']
		for i in range(1,43):
			fieldNames.append('col '+str(i))
		with open(self.filepath, 'w') as PMGSYFile:
			csvWriter = csv.writer(PMGSYFile)
			csvWriter.writerow(fieldNames)
		PMGSYFile.close()

	def dump(self,year,month,state,district,districtData):
		"""
		Dumps the data in csv file
		"""		
		with open(self.filepath, 'a') as PMGSYFile:
			csvWriter = csv.writer(PMGSYFile,delimiter=',')
			finalRow = [year,month,state,district]
			for column in districtData:
				finalRow.append(column)
			csvWriter.writerow(finalRow)
		PMGSYFile.close()
