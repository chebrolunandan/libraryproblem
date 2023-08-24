from pymongo import MongoClient
class HospitalDB:
    def init(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['Hospital']
        self.doctors = self.db['Doctor']
        self.patients = self.db['Patient']
        self.medicines = self.db['Medicine']

    def create_doctor(self, doctor):
        result = self.doctors.insert_one(doctor)
        return result.inserted_id

    def create_patient(self, patient):
        result = self.patients.insert_one(patient)
        return result.inserted_id

    def create_medicine(self, medicine):
        result = self.medicines.insert_one(medicine)
        return result.inserted_id

    def read_doctor(self, query={}):
        result = self.doctors.find(query)
        return [doctor for doctor in result]

    def read_patient(self, query={}):
        result = self.patients.find(query)
        return [patient for patient in result]

    def read_medicine(self, query={}):
        result = self.medicines.find(query)
        return [medicine for medicine in result]

    def update_doctor(self, query, update):
        result = self.doctors.update_one(query, update)
        return result.modified_count

    def update_patient(self, query, update):
        result = self.patients.update_one(query, update)
        return result.modified_count

    def update_medicine(self, query, update):
        result = self.medicines.update_one(query, update)
        return result.modified_count

    def delete_doctor(self, query):
        result = self.doctors.delete_one(query)
        return result.deleted_count

    def delete_patient(self, query):
        result = self.patients.delete_one(query)
        return result.deleted_count

    def delete_medicine(self, query):
        result = self.medicines.delete_one(query)
        return result.deleted_count