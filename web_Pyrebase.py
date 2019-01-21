import pyrebase

class Pyrebase:
    def __init__(self):
        config = {
            "apiKey": "lol",
            "authDomain": "lol",
            "databaseURL": "lol",
            "projectId": "lol",
            "storageBucket": "lol",
            "messagingSenderId": "lol",
            "serviceAccount": "lol"
        }
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()
        
        self.storeIndex = {
            "img_Static": 0,
            "img_PlotResults": 0,
            "img_DetectedPerson": 0
        }
    def storeFile(self, fileDir, folder):
        ref =  self.storage.child(folder + '/' + str(self.storeIndex[folder]) + '.png')
        upload = ref.put(fileDir)
        url = ref.get_url()
        self.storeIndex[folder] += 1
        print(self.storeIndex) 
        return url, self.storeIndex[folder]
    def delete(self, index, folder):
        ref = self.storage
        ref.delete(folder + '/' + str(index) + '.png')
        return "fuckoff"
    def clear(self, folder):
        if self.storeIndex[folder] == 0: 
            return "done clearing " + folder
        for i in range(self.storeIndex[folder]):
            print("deleting: ", folder + '/' + str(i) + '.png')
            self.storage.delete(folder + '/' + str(i) + '.png')
        self.storeIndex[folder] == 0
        return "done clearing " + folder
    def clearAll(self):
        for folder in  self.storeIndex:
            self.clear(folder)
#             if self.storeIndex[folder] == 0: pass
#             for i in range(self.storeIndex[folder]):
#                 print("deleting: ", folder + '/' + str(i) + '.png')
#                 self.storage.delete(folder + '/' + str(i) + '.png')
#             self.storeIndex[folderName] == 0
        return "done clearing all"