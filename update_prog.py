import pickle,xlrd,time
# to be imported only after selecting a location

class Teacher_obj(object) : # creating a class to handle the vast amount of data
    def __init__(self,n,sheet) :# basically each teacher is converted into an object and the 9 periods are stored in following variables
        self.name = sheet.cell_value(n,0)
        self.cl = 0 # [ 0 = "6 to 8", 1 ="9&10",2 ="11 & 12"]
        self.pos = n

def runit() :

    update = open("Support/update.bat","w")


    def  select_most_occurance(n) :
        l = []
        for sheet_no in range (0,5) :
            sheet = book.sheet_by_index(sheet_no)
            for i in range(1,10) :
                temp =  ""
                for j in str(sheet.cell_value(n,i)) :
                    if str(j).isdigit() and ( (len(temp) == 1 and temp[0] == "1" ) or (len(temp) == 0)) :
                        temp+=j
                else :
                    l.append(temp)

        to_return = ""
        cl_list = [0,0,0] # ["6 to 8","9&10","11 & 12"]
        for i in l :
            if  i != "":
               if int(i) in [6,7,8] :
                   cl_list[0]+=1
               elif int(i) in [9,10] :
                   cl_list[1]+=1
               elif int(i) in [11,12] :
                   cl_list[2]+=1
        maxi = [0,0]
        for i in range(len(cl_list)) :
            if cl_list[i] > maxi[1] :
                maxi = [i,cl_list[i]]
        else :
            if maxi[0] not in [0,1,2] :
                print 'Error parsing. Contact support immidiately !'
                time.sleep(5)
        return maxi[0]








    l = []
    with open("Support/path.txt", "r") as textfile:
        a = textfile.readline()
        book = xlrd.open_workbook(a)

    sheet = book.sheet_by_index(0)
    for n in range(sheet.nrows) :
        l.append(Teacher_obj(n,sheet))


    for i in l :
        i.cl = select_most_occurance(i.pos)
    pickle.dump(l,update)
    update.close()
    print 'Done'

if __name__ == '__main__' :
    runit()
