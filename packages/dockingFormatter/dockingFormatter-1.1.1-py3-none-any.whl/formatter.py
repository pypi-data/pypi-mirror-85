import csv 
import openpyxl

class DockingFormatter:

    def findAffinityForCompound(self, fileName, **kwargs):
        #Creation of the intersting proccessedCompounds list
        affinity_list = []
        f = open(fileName)
        i = 0
        modeIterator = 0
        proccessedCompound = ""
        # affinitCount = ""
        #TODO: Correct appending proccessedCompound to the affinity_list
        for x in f:
            if "Processing compound" in x: #43 i in loop 
                proccessedCompound += x[-14:-8]
            if "mode |   affinity |" in x and i > 28:
                modeIterator = i
            if i == (modeIterator + 3):
                # affinitCount += x[13:17]
                affinity_list.append([proccessedCompound,x[3:4],x[13:17]])
                proccessedCompound = ""
            # if i == (modeIterator + 4) and x[13:17] == affinitCount:
            #     print(proccessedCompound)
            #     affinity_list.append([proccessedCompound,x[3:4], x[13:17]])
            # else:
            #     affinitCount = ""
            #     proccessedCompound = ""
            #     i += 1
            #     continue
            # if i == (modeIterator + 5) and x[13:17] == affinitCount:
            #     print(proccessedCompound)
            #     affinity_list.append([proccessedCompound,x[3:4], x[13:17]])
            # else:
            #     affinitCount = ""
            #     proccessedCompound = ""
            #     i += 1
            #     continue
            # if i == (modeIterator + 6) and x[13:17] == affinitCount:
            #     print(proccessedCompound)
            #     affinity_list.append([proccessedCompound,x[3:4], x[13:17]])
            #     affinitCount = ""
            #     proccessedCompound = ""
            i += 1
        affinity_list.pop(0)
        f.close()
        # with open(fileName + ".csv", 'w') as csv_file:
        #     writer = csv.writer(csv_file)
        #     writer.writerows(affinity_list)
        
        # Parsing data to excel workbook section
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet["A1"] = "Processing compound"
        sheet["B1"] = "Mode"
        sheet["C1"] = "Affinity"
        for row in affinity_list:
            sheet.append(row)
        if 'output' in kwargs:
            if '.xlsx' in kwargs.get("output"):
                workbook.save(f"{kwargs.get('output')}")
            else: 
                workbook.save(f"{kwargs.get('output')}.xlsx")
        else:
            workbook.save(f"{fileName[:-4]}.xlsx")
        



