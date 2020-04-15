class Loader():
    
    def loadArray(id_num):
        filename = "vals" + str(id_num) + ".txt"
        outArray = []
        try:
            file = open(filename, mode='r')
            for val in file:
                outArray.append(float(val))
        except:
            print("Could not load. Creating new file: vals" + str(id_num))
            file = open(filename, mode='w')
            file.close()

        return outArray
        
    def saveArray(id_num, array):
        filename = "vals" + str(id_num) + ".txt"
        file = open(filename, mode='w')
        for val in array:
            file.write(str(val)+'\n')
        file.close()
