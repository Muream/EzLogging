from __future__ import absolute_import
from core.clipLogger import clipLogger

# clipLogger()


myList = range(0, 100)
print myList
for index, element in enumerate(myList):
    try:
        myList.remove(myList[index+1])
    except:
        pass
print myList
