from google.cloud import firestore
import datetime
from pytz import timezone

'''
# Add a new document
print("Open client")
db = firestore.Client()
print("Client open")
doc_ref = db.collection(u'test_data').document(u'10022019_1323')
print("doc ref")
doc_ref.set({
u'angle_data': {"0":10,
"1":11,
"2":15,
"3":1
},
u'measured_dist': u'1000',
u'sensor_id': 2019,
u'time_stamp': datetime.datetime.now(timezone('US/Eastern'))
})

# Then query for documents

users_ref = db.collection(u'test_data')
print("Get docs")
docs = users_ref.get()
print("done")

for doc in docs:
print(u'{} => {}'.format(doc.id, doc.to_dict()))
'''


def main():
	#Create a database connection
	db = firestore.Client()
	
	#Get name for new document
	'''
	doc = input("Enter the name of the document you'd like to create: ")
	
	#Create the reference to the document we want to create or modify
	doc_ref = db.collection(u'test_data').document(doc)
	#Get some angle data
	angle0 = int(input("Enter dummy data for angle 0: "))
	angle1 = int(input("Enter dummy data for angle 1: "))
	angle2 = int(input("Enter dummy data for angle 2: "))
	id = int(input("Enter the sensor id: "))
	
	#Set the data object
	doc_ref.set({
		u'angle_data': {"0":angle0,
				"1" : angle1,
				"2"  :angle2,
	},
		u'sensor_id': id,
		u'time_stamp': datetime.datetime.now()
	})
        #timezone('US/Eastern')
	#Add to data to database
	#users_ref = db.collection(u'test_data')

	'''
	dist = (386-200)/60
        
	doc_ref = db.collection(u'sensor_data').document("-1")
	tempData =dict()
	for i in range(61):
		tempData[str(30+i)] = 386-(dist*(i))
	dist = (276.86-200)/48
	for i in range(61,111):
		tempData[str(30+i)] = 200 + (dist*(i-60))
	dist = 23.5/12
	for i in range(111,121):
		tempData[str(30+i)] = 276.86 - (i-110)*dist
	print(tempData)
	
	#docs = users_ref.get()
	doc_ref.set({
                u'given_data': tempData,
                u'gps_location': "",
                u'mounted_height': 200,
		u'base_to_road_angle': 0,
		u'sensor_id': -1
        })
	

if __name__ == "__main__":
	main()

