from PythUnity import Variables
import PythUnity
import pygame
def AddObject(image):
  Variables.var.parts._ProtectedList__val.append(image)
  index = len(Variables.var.parts) - 1
  Variables.var.parts[index]._Object__index = index
  return index

#def AddObjects(images):
#  indexes = []
#  for i in images:
#    indexes.append(AddObject(i))
#  return indexes

def AddPrefab(name, obj):
  if(type(name) is not str):
      Err("Name value must be a " + str(str) + " not a " + str(type(name)))
  if(type(obj) is not PythUnity.Classes.Object):
      Err("Object value must be a " + str(PythUnity.Classes.Object) + " not a " + str(type(obj)))
  newObj = obj.Copy()
  newObj.Move(len(newObj.GetParentChildren()))
  del newObj.GetParentChildren()._ProtectedList__val[newObj.index]#need to remove prefab from child list
  newObj._Object__parent = None
  newObj._Object__index = -1
  Variables.var.prefabs[name] = newObj
def GetPrefab(name):
  if(type(name) is not str):
      Err("Name value must be a " + str(str) + " not a " + str(type(name)))
  if(name not in Variables.var.prefabs):
      Err("Prefab: \"" + name + "\" does not exist")
  newObj = Variables.var.prefabs[name].Copy()
  newObj.Move(len(newObj.GetParentChildren()))
  return newObj
def GetFonts():
  return pygame.font.get_fonts() 

def TypeCheck(value, typeInput, name, className = "Object"):
    correct = False
    outString = ""
    if(type(typeInput) == list):
      for i in typeInput:
          if(type(value) == i):
              correct = True
              break
          else:
              if(outString == ""):
                outString = TypeStringClean(str(i))
              else:
                outString = outString + " or " + TypeStringClean(str(i))
    else:
      correct = type(value) == typeInput
      outString = TypeStringClean(str(typeInput))
    if(not correct):
        Err("cant set PythUnity." + className + "." + name + " as a " + str(type(value)) + " it must be a " + outString)
def TypeStringClean(inputStr):
    inputStr = inputStr.replace("pygame", "PythUnity")
    return inputStr
def Err(text):
    raise Exception("PythUnity: " + text)
def Warn(text):
    raise RuntimeWarning("PythUnity: " + text)

