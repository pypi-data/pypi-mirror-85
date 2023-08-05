from PythUnity import Functions
class ProtectedList:
  def __init__(self, varName, className, canAppend, canInsert, canDelete, canSet, onAccess = None, allowedTypes = None):
    self.__varName = varName
    self.__className = className
    self.__canAppend = canAppend
    self.__canInsert = canInsert
    self.__canDelete = canDelete
    self.__onAccess = onAccess
    self.__allowedTypes = allowedTypes
    self.__val = []
  def __getitem__(self, i):
    if(self.__onAccess != None):
      self.__onAccess[0](self.__onAccess[1])
    if(type(i) is int):
      return self.__val[i]
    else:
      Functions.Err("in " + self.__className + "." + self.__varName + "[i] i must be a " + str(int) + " not " + str(type(i)))
  def __setitem__(self, i):
    if(self.__canSet and (len(self.__allowedTypes) == 0 or type(i) in self.__allowedTypes)):
      self.__val[i] = i
    elif(not self.__canSet):
      Functions.Err("you cannot set " + self.__className + "." + self.__varName + "[i] you can only get it")
    else:
      Functions.TypeCheck(i, self.__allowedTypes, self.__varName + "[i]", self.__className)
  def __len__(self):
    if(self.__onAccess != None):
      self.__onAccess[0](self.__onAccess[1])
    len(self.__val)
    return len(self.__val)
  def __delitem__(self, i):
    if(self.__canDelete):
      if(type(i) is int):
        del self.__val[i]
      else:
        Functions.Err("in " + self.__className + "." + self.__varName + "[i] i must be a " + str(int) + " not " + str(type(i)))
    else:
      Functions.Err(self.__className + "." + self.__varName + "[i] cannot be deleted")
  def append(self, val):
    if(len(self.__allowedTypes) == 0 or type(i) in self.__allowedTypes):
      self.__val.append(val)
    else:
      Functions.TypeCheck(i, self.__allowedTypes, self.__varName + "[i]", self.__className)