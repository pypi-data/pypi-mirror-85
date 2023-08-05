from PythUnity import Variables
from PythUnity import Functions
from PythUnity.ProtectedList import ProtectedList
import copy
import pygame
import types
import inspect
class Object:
  def __init__(self, rect, image, onClick = None, onDrag = None, onClickOff = None, onScroll = None, onHover = None, onHoverOff = None, onHoverOn = None, enableDragOff = False, clickGroup = 0, fitImage=False, effect=None):
    self.__destroyed = False
    self.__parent = None
    self.__children = ProtectedList("children", "Object", False, False, False, False)
    self.__variables = {}
    self.__image = None
    self.__transformedImage = None
    self.__text = None
    self.__color = None
    self.__oldPos = (0, 0, 0, 0)
    self.__edited = True
    self.__components = ProtectedList("components", "Object", False, False, False, False)
    self.__clickGroup = None
    self.__velocity = (0, 0)
    self.__index = None
    self.__rect = None
    self.__transformed = False
    self.__transformedColor = False
    self.__updateLocal = False
    self.__updateGlobal = False
    self.renderOptions = RenderOptions(fitImage=fitImage, effect=effect)
    self.__globalRect = Rect(0, 0, 0, 0)
    self.__globalRect._Rect__owner = self
    self.__globalRect._Rect__global = True
    self.__enabled = True
    self.rect = rect
    self.clickGroup = clickGroup
    if(type(image) is tuple):
      self.color = image
    elif(type(image) is String):
      self.text = image.Copy()
    elif(type(image) is pygame.Surface):
      self.image = image
    if onClick != None or onDrag != None or onScroll != None:
      self.__button = Button(onClick, onDrag, onClickOff, onScroll, onHover, onHoverOff, onHoverOn, enableDragOff)
    else:
      self.__button = None
    Functions.AddObject(self)
  #####
  @property
  def rect(self):
      if(self.__updateLocal):
        self.__updateLocal = False
        offset = (0, 0)
        if(self.parent != None):
          offset = (self.parent.globalRect.left, self.parent.globalRect.top)
        self.__rect._Rect__left = self.globalRect.left - offset[0]
        self.__rect._Rect__top = self.globalRect.top - offset[1]
        self.__rect._Rect__width = self.globalRect.width
        self.__rect._Rect__height = self.globalRect.height
      return self.__rect
  @rect.setter
  def rect(self, value):
    self.__edited = True
    Functions.TypeCheck(value, Rect, "rect")
    self.__rect = value
    self.__rect._Rect__owner = self
    self.__rect._Rect__global = False
    UpdateRects(self.__rect)
    self.__transformed = True
    TransformText(self)
  @property
  def globalRect(self):
      if(self.__updateGlobal):
        self.__updateGlobal = False
        offset = (0, 0)
        if(self.parent != None):
          offset = (self.parent.globalRect.left, self.parent.globalRect.top)
        self.__globalRect._Rect__left = self.rect.left + offset[0]
        self.__globalRect._Rect__top = self.rect.top + offset[1]
        self.__globalRect._Rect__width = self.rect.width
        self.__globalRect._Rect__height = self.rect.height
      return self.__globalRect
  @globalRect.setter
  def globalRect(self, value):
    self.__edited = True
    Functions.TypeCheck(value, Rect, "globalRect")
    self.__globalRect = value
    self.__globalRect._Rect__owner = self
    self.__globalRect._Rect__global = True
    UpdateRects(self.__globalRect)
    self.__transformed = True
    TransformText(self)
  @property
  def renderOptions(self):
      return self.__renderOptions
  @renderOptions.setter
  def renderOptions(self, value):
    self.__edited = True
    Functions.TypeCheck(value, RenderOptions, "renderOptions")
    self.__renderOptions = value
    self._RenderOptions__owner = self
    TransformImage(self)
  @property
  def enabled(self):
      return self.__enabled
  @enabled.setter
  def enabled(self, value):
    self.__edited = True
    Functions.TypeCheck(value, bool, "enabled")
    self.__enabled = value
  @property
  def image(self):
    return self.__image
  @image.setter
  def image(self, value):
    self.__edited = True
    Functions.TypeCheck(value, pygame.Surface, "image")
    self.__image = value#.convert_alpha()
    self.__transformed = True
    self.__transformedColor = True
  @property
  def destroyed(self):
    return self.__destroyed
  @destroyed.setter
  def destroyed(self, value):
    Functions.Err("Cant set Object.destroyed")
  @property
  def index(self):
    return self.__index
  @index.setter
  def index(self, value):
    Functions.Err("Cant set Object.index")
  @property
  def parent(self):
    return self.__parent
  @parent.setter
  def parent(self, value):
    Functions.Err("Cant set Object.parent")
  @property
  def children(self):
    return self.__children
  @children.setter
  def children(self, value):
    Functions.Err("Cant set Object.children")
  @property
  def components(self):
    return self.__components
  @components.setter
  def components(self, value):
    Functions.Err("Cant set Object.components, use Object.AddComp or Object.DelComp")
  @property
  def variables(self):
    return self.__variables
  @variables.setter
  def variables(self, value):
    Functions.Err("Cant set Object.variables, add each variable individualy")
  @property
  def transformedImage(self):
    if(self.__transformed or self.__transformedColor):
      TransformImage(self, self.__transformedColor)
      self.__transformed = False
      self.__transformedColor = False
    if(self.text != None and self.image == None):
      if(self.text._String__imageChanged or self.text._String__rowChanged):
        self.text._String__imageChanged = False
        RenderText(self)
    return self.__transformedImage
  @transformedImage.setter
  def transformedImage(self, value):
    Functions.Err("Cant set Object.transformedImage")
  ##
  @property
  def text(self):
      return self.__text
  @text.setter
  def text(self, value):
    self.__edited = True
    Functions.TypeCheck(value, [String, type(None)], "text")
    self.__text = value
    self.text._String__owner = self
    self.text._String__imageChanged = True
    TransformText(self)
  @property
  def color(self):
      return self.__color
  @color.setter
  def color(self, value):
    self.__edited = True
    self.__color = SetColor(value, "color", "Object")
    self.__transformedColor = True
  @property
  def clickGroup(self):
      return self.__clickGroup
  @clickGroup.setter
  def clickGroup(self, value):
    Functions.TypeCheck(value, int, "clickGroup")
    self.__clickGroup = value
  @property
  def velocity(self):
      return self.__velocity
  @velocity.setter
  def velocity(self, value):
    Functions.TypeCheck(value, tuple, "velocity")
    self.__velocity = value
  @property
  def button(self):
      return self.__button
  @button.setter
  def button(self, value):
    Functions.TypeCheck(value, [Button, type(None)], "button")
    self.__button = value
  #####
  def __getitem__(self, i):
    self.__Throw("children.getitem")
    return self.__children[i]
  def __len__(self):
    self.__Throw("children.len")
    return len(self.__children)
  #####
  def Decendants(self):
    self.__Throw("Object.Decendants")
    indexes = []
    for i in self.__children:
      indexes.append(i)
      indexes.extend(i.Decendants())
    return indexes
  def Move(self, newIndex):#components can have their update function skipped on accident if ran in another comp.update
    self.__Throw("Object.Move")
    self.__edited = True
    children = self.GetParentChildren()
    if(newIndex < 0):
        Functions.Err("Object.Move failed, index less than 0")
    elif(newIndex > len(children)):
        Functions.Warn("Object.Move incorrect, index is greater than parent.children count")
    oldIndex = self.index
    self.__index = newIndex
    del children._ProtectedList__val[oldIndex]
    children._ProtectedList__val.insert(newIndex, self)
    i = oldIndex
    if(newIndex > oldIndex):
      while(i < newIndex):
        children[i]._Object__index = i
        i = i + 1
    elif(newIndex < oldIndex):
      while(i >= newIndex):
        children[i]._Object__index = i
        i = i - 1
  def SetParent(self, newParent):
    self.__Throw("Object.SetParent")
    self.__edited = True
    self.__updateGlobal = True
    children = self.GetParentChildren()
    self.Move(len(children))#make it so other children have their indexes fixed
    del children._ProtectedList__val[self.index]
    self.__parent = newParent
    self.__parent.children._ProtectedList__val.append(self)
    self.__index = len(self.__parent.children) - 1
  def GetParentChildren(self):
    self.__Throw("Object.GetParentChildren")
    children = None
    if(self.__parent != None):
      children = self.__parent.children
    else:
      children = Variables.var.parts
    return children
  def Copy(self):
    self.__Throw("Object.Copy")
    oldParent = self.parent
    parChildren = self.GetParentChildren()
    CopyHelp(self)
    tempVars = self.variables
    self.__variables = None
    copied = copy.deepcopy(self)
    self.__variables = tempVars
    copied._Object__variables = copy.copy(tempVars)
    copied._Object__index = len(parChildren)
    parChildren._ProtectedList__val.append(copied)
    copied._Object__parent = oldParent
    copied.Move(self.index + 1)
    CopyUnHelp(self, oldParent)
    CopyHelp2(copied, self, copied)
    CopyUnHelp(copied, oldParent)
    return copied
  def Destroy(self):
    self.__Throw("Object.Destroy")
    Variables.updates.append(self.globalRect.ToPygameRect())
    children = self.GetParentChildren()
    self.Move(len(children))
    del children._ProtectedList__val[self.index]
    self.__index = -1 #will cause Functions.Error if used incorrectly, did this on purpous
    self.__destroyed = True
    for i in self.__children:
      i.Destroy()
  def AddComp(self, comp):
    self.__Throw("Object.AddComp")
    self.__components._ProtectedList__val.append(comp)
    if(comp[0] != None):
        comp[0](self)
  def DelComp(self, index):
      self.__Throw("Object.DelComp")
      if(len(self.__components) > index):
          del self.__components._ProtectedList__val[index]
      else:
          Functions.Err("Object.DelComp failed, index greater than comp index")
  def SetClickGroup(self, number):
      self.__Throw("Object.SetClickGroup")
      self.clickGroup = number
      for i in self.children:
          i.SetClickGroup(number)
  def __Throw(self, action = ""):
    if(self.__destroyed):
      if(action == ""):
        Functions.Err("Object was destroyed")
      else:
        Functions.Err("Object was destroyed while " + action + "() was happening")
class Button:
  def __init__(self, onClick = None, onDrag = None, onClickOff = None, onScroll = None, onHover = None, onHoverOff = None, onHoverOn = None, enableDragOff = None):
    self.__onClick = None
    self.__onClickOff = None
    self.__onDrag = None
    self.__onScroll = None
    self.__onHover = None
    self.__onHoverOff = None
    self.__onHoverOn = None
    self.__dragging = False
    self.__hovering = False
    self.__enableDragOff = None
    if(enableDragOff != None):
      self.enableDragOff = enableDragOff
    self.onClick = onClick
    self.onClickOff = onClickOff
    self.onDrag = onDrag
    self.onScroll = onScroll
    self.onHover = onHover
    self.onHoverOff = onHoverOff
    self.onHoverOn = onHoverOn
  @property
  def dragging(self):
      return self.__dragging
  @dragging.setter
  def dragging(self, value):
      Functions.Err("You cant set PythUnity.Button.dragging, you can only get it")
  @property
  def hovering(self):
      return self.__hovering
  @hovering.setter
  def hovering(self, value):
      Functions.Err("You cant set PythUnity.Button.hovering, you can only get it")
  ##
  @property
  def enableDragOff(self):
      return self.__enableDragOff
  @enableDragOff.setter
  def enableDragOff(self, value):
      Functions.TypeCheck(value, bool, "enableDragOff", "Button")
      self.__enableDragOff = value
  @property
  def onClick(self):
      return self.__onClick
  @onClick.setter
  def onClick(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onClick", "Button")
      TestFuncLen(value, "onClick", ["self", "string_mouseButton"])
      self.__onClick = value
  @property
  def onClickOff(self):
      return self.__onClickOff
  @onClickOff.setter
  def onClickOff(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onClickOff", "Button")
      TestFuncLen(value, "onClickOff", ["self", "string_mouseButton"])
      self.__onClickOff = value
  @property
  def onDrag(self):
      return self.__onDrag
  @onDrag.setter
  def onDrag(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onDrag", "Button")
      TestFuncLen(value, "onDrag")
      self.__onDrag = value
  @property
  def onScroll(self):
      return self.__onScroll
  @onScroll.setter
  def onScroll(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onScroll", "Button")
      TestFuncLen(value, "onScroll", ["self", "int_direction"])
      self.__onScroll = value
  @property
  def onHover(self):
      return self.__onHover
  @onHover.setter
  def onHover(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onHover", "Button")
      TestFuncLen(value, "onHover")
      self.__onHover = value
  @property
  def onHoverOff(self):
      return self.__onHoverOff
  @onHoverOff.setter
  def onHoverOff(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onHoverOff", "Button")
      TestFuncLen(value, "onHoverOff", ["self", "string_reason"])
      self.__onHoverOff = value
  @property
  def onHoverOn(self):
      return self.__onHoverOn
  @onHoverOn.setter
  def onHoverOn(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onHoverOn", "Button")
      TestFuncLen(value, "onHoverOn")
      self.__onHoverOn = value
class String:
  def __init__(self, text, fontSize, font, fontColor, backgroundColor, alignment = 0, maxRows = 0):
    self.__owner = None
    self.__fontSize = None
    self.__imageChanged = False
    self.__text = None
    self.__font = None
    self.__fontColor = None
    self.__backgroundColor = None
    self.__rows = ProtectedList("rows", "String", False, False, False, False, (StringFixRow, self))
    self.__maxRows = 0
    self.alignment = alignment
    self.fontSize = fontSize
    self.font = font
    self.fontColor = fontColor
    self.backgroundColor = backgroundColor
    self.text = text
    self.maxRows = maxRows
  @property
  def sizer(self):
    StringFixRow(self)
    return self.__sizer
  @sizer.setter
  def sizer(self, value):
    Functions.Err("can't set PythUnity.sizer, you can only get it")
  @property
  def maxRows(self):
    return self.__maxRows
  @maxRows.setter
  def maxRows(self, value):
    Functions.TypeCheck(value, int, "maxRows", "String")
    self.__maxRows = value
    self.__rowChanged = True
  @property
  def rows(self):
    StringFixRow(self)
    return self.__rows
  @rows.setter
  def rows(self, value):
    Functions.Err("can't set PythUnity.rows, you can only get it")
  @property
  def alignment(self):
    return self.__alignment
  @alignment.setter
  def alignment(self, value):
    Functions.TypeCheck(value, int, "alignment", "String")
    self.__alignment = value
    self.__imageChanged = True
    SetEdited(self)
  @property
  def fontSize(self):
    return self.__fontSize
  @fontSize.setter
  def fontSize(self, value):
    Functions.TypeCheck(value, [int, float], "fontSize", "String")
    self.__fontSize = value
    self.__rowChanged = True
    SetEdited(self)
  @property
  def text(self):
    return self.__text
  @text.setter
  def text(self, value):
    Functions.TypeCheck(value, str, "text", "String")
    self.__text = value
    self.__rowChanged = True
    SetEdited(self)
  @property
  def font(self):
    return self.__font
  @font.setter
  def font(self, value):
    Functions.TypeCheck(value, str, "font", "String")
    self.__font = value
    self.__rowChanged = True
    SetEdited(self)
  @property
  def fontColor(self):
    return self.__fontColor
  @fontColor.setter
  def fontColor(self, value):
    self.__fontColor = SetColor(value, "fontColor", "String")
    self.__imageChanged = True
    SetEdited(self)
  @property
  def backgroundColor(self):
    return self.__backgroundColor
  @backgroundColor.setter
  def backgroundColor(self, value):
    self.__backgroundColor = SetColor(value, "backgroundColor", "String")
    self.__imageChanged = True
    SetEdited(self)
  #######
  def Copy(self):
    self.rows#do this to clear the self.__rowChanged
    owner = self.__owner
    onAccess = self.__rows._ProtectedList__onAccess
    sizer = self.sizer
    self.__sizer = None
    self.__rows._ProtectedList__onAccess = None
    self.__owner = None
    new = copy.deepcopy(self)
    self.__sizer = sizer
    self.__rows._ProtectedList__onAccess = onAccess
    new._String__sizer = sizer
    new._String__rows._ProtectedList__onAccess = (onAccess[0], new)
    self.__owner = owner
    return new
  def GetSize(self):
    height = 0
    self.rows#do this to clear the self.__rowChanged
    sizer = self.sizer
    for row in self.rows:
      height = height + sizer.size(row)[1]
    width = 0
    for row in self.rows:
      size = sizer.size(row)[0]
      if(size > width):
        width = size
    return (width, height)
class Rect: #need to use @property so cant use pygame.Rect
    def __init__(self, left, top, width, height):
        self.__owner = None
        self.__left = None
        self.__top = None
        self.__width = None
        self.__height = None
        self.__global = False
        self.left = left
        self.top = top
        self.width = width
        self.height = height
    @property
    def left(self):
        return self.__left
    @left.setter
    def left(self, value):
      Functions.TypeCheck(value, [float, int], "left", "Rect")
      self.__left = float(value)
      UpdateRects(self)
      SetEdited(self)
    @property
    def top(self):
        return self.__top
    @top.setter
    def top(self, value):
      Functions.TypeCheck(value, [float, int], "top", "Rect")
      self.__top = float(value)
      UpdateRects(self)
      SetEdited(self)
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, value):
      Functions.TypeCheck(value, [float, int], "width", "Rect")
      self.__width = float(value)
      UpdateRects(self)
      if(self.__owner != None and not self.__global):
        self.__owner._Object__transformed = True
        TransformText(self.__owner)
      SetEdited(self)
    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, value):
      Functions.TypeCheck(value, [float, int], "height", "Rect")
      self.__height = float(value)
      UpdateRects(self)
      if(self.__owner != None and not self.__global):
        self.__owner._Object__transformed = True
        TransformText(self.__owner)
      SetEdited(self)
    ######
    def __getitem__(self, i):
      options = RectItemHelp(self, i)
      return getattr(self, options[i])
    def __setitem__(self, i, newvalue): 
      if(type(newvalue) is not int and type(newvalue) is not float):
        Functions.Err("in PythUnity.Rect[index] = newValue, newValue must be a " + str(int) + " or " + str(float) + " not " + str(type(newvalue)))
      options = RectItemHelp(self, i)
      attr = setattr(self, options[i], newvalue)
    ######
    def ToPygameRect(self):
        return pygame.Rect(self.left, self.top, self.width, self.height)
    def Copy(self):
        return Rect(self.left, self.top, self.width, self.height)
class RenderOptions:
  def __init__(self, fitImage=False, effect=None):#effect hasnt been implemented yet
    self.__owner = None
    self.fitImage = fitImage
    self.effect = effect
  @property
  def fitImage(self):
    return self.__fitImage
  @fitImage.setter
  def fitImage(self, value):
    Functions.TypeCheck(value, type(False), "fitImage", "RenderOptions")
    self.__fitImage = value
    if(self.__owner != None):
      self.__owner._Object__imageChanged = True
    SetEdited(self)
def TestFuncLen(func, name, neededArgs = ["self"], className="Button"):
    if(func != None):
        length = len(inspect.getargspec(func)[0])
        if(length != len(neededArgs)):
            Functions.Err("PythUnity." + className + "." + name + " must have an argument length of " + str(len(neededArgs)) + " not " + str(length) + "\nfunction: " + str(func)  + "\nneeded arguments: " + str(neededArgs) + "\nrecieved arguments: " + str(inspect.getargspec(func)[0]))
def RectItemHelp(self, i):
  options = ["left", "top", "width", "height"]
  if(type(i) is not int):
    Functions.Err("in PythUnity.Rect[index], index must be a " + str(int) + " not " + str(type(i)))
  if(i > 4 or i < 0):
    Functions.Err("in PythUnity.Rect[index], index must be between values 0 and " + str(len(options)))
  return options
def CopyHelp(self):
  if(self.transformedImage != None):
    self._Object__transformedImage = (pygame.image.tostring(self._Object__transformedImage, 'RGBA'), self._Object__transformedImage.get_size())
  if(self.image != None):
    self._Object__image = (pygame.image.tostring(self.image, 'RGBA'), self.image.get_size())
  self._Object__rect._Rect__owner = None
  self._Object__globalRect._Rect__owner = None
  self.renderOptions._RenderOptions__owner = None
  if(self.text != None):
    self.text._String__owner = None
    self.text._String__sizer = None
  self._Object__parent = None
  for i in self.children:
    CopyHelp(i)

def CopyUnHelp(self, parent):
  if(self._Object__image != None):
    self._Object__image = pygame.image.fromstring(self._Object__image[0], self._Object__image[1], 'RGBA')
  if(self._Object__transformedImage != None):
    self._Object__transformedImage = pygame.image.fromstring(self._Object__transformedImage[0], self._Object__transformedImage[1], 'RGBA')
  self._Object__rect._Rect__owner = self
  self._Object__globalRect._Rect__owner = self
  self.renderOptions._RenderOptions__owner = self
  if(self.text != None):
    self.text._String__owner = self
    self.text._String__sizer = pygame.font.Font(self.text.font + ".ttf", int(self.text._String__realFontSize))
  self._Object__parent = parent
  for i in self.children:
    CopyUnHelp(i, self)
def CopyHelp2(self, og, ogCopy):
  atts = dir(self)
  for att in atts:
    if(("_Object__" + att) not in atts):
      attObj = getattr(self, att)
      if(att[0] != "_" or att[1] == "O"):#if its a _Object__ atribute still copy
        attType = type(attObj)
        if(attType is not types.MethodType and attType is not list and attType is not type(None) and attType is not Object and attType is not type({})):
          setattr(self, att, copy.deepcopy(attObj))
  for i in self.variables.keys():
    attType = type(self.variables[i])
    if(attType is Object):
      if self.variables[i] in og.Decendants():
        index = og.Decendants().index(self.variables[i])
        self.variables[i] = ogCopy.Decendants()[index]
      elif(self.variables[i] == og):
        self.variables[i] = ogCopy
  for i in self.children:
    CopyHelp2(i, og, ogCopy)

def TransformImage(self, changeColor = False):
  if(self.image != None):
      ratio = self.image.get_size()
      if(type(self.color) is not type(None) and changeColor):
          color = self.color
          if(color == None):
              color = (255, 255, 255, 255)
          self._Object__transformedImage = self.image.copy()
          image2 = pygame.Surface(size=self._Object__transformedImage.get_size()).convert_alpha() 
          image2.fill(color)
          image2.blit(self._Object__transformedImage.convert_alpha(), (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
          self._Object__transformedImage = image2
      elif(type(self.color) is type(None)):
          self._Object__transformedImage = self.image
      ratio = self.image.get_size()
      if(not self.renderOptions.fitImage):
        max = ratio[0]
        if(max < ratio[1]):
          max = ratio[1]
        ratio = (float(ratio[0] / max), float(ratio[1] / max))
      else:
        ratio = (1, 1)
      ratio = (int(ratio[0] * self.rect.width), int(ratio[1] * self.rect.height))
      self._Object__transformedImage = pygame.transform.scale(self._Object__transformedImage, ratio)
  else:
    self._Object__transformedImage = None
def StringFixRow(self):
  if(self._String__rowChanged):
    self._String__rowChanged = False
    self._String__imageChanged = True
    StringResize(self)
    StringSetRow(self)
def StringResize(self, resetSize = True):
  if(resetSize):
    self._String__realFontSize = self.fontSize
  changeText = self.text
  rows = []
  while(True):
    enterIndex = changeText.find("\n")
    if(enterIndex == -1 or (self.maxRows > 0 and self.maxRows == len(rows)+1)):
      if(enterIndex != -1):
        rows.append(changeText[:enterIndex] + changeText[enterIndex+1:])
      else:
        rows.append(changeText)
      break
    rows.append(changeText[:enterIndex])
    changeText = changeText[enterIndex+1:]
  i = 0
  self._String__sizer = pygame.font.Font(self.font + ".ttf", int(self._String__realFontSize))
  if(self._String__owner != None and self._String__owner.rect.width > 0):
    sizer = self._String__sizer
    while(i < len(rows)):
      size = sizer.size(rows[i])[0]
      newRow = ""
      while(size > self._String__owner.rect.width):
        space = 0
        if (" " in rows[i]):
          space = rows[i].rindex(" ")+1
        chars = len(rows[i]) - space
        if(sizer.size(rows[i][space:])[0] <= self._String__owner.rect.width):
          newRow = rows[i][space-1:] + newRow
          rows[i] = rows[i][:space-1]
          if(sizer.size(rows[i])[0] <= self._String__owner.rect.width):
            newRow = newRow[1:]
        else:
          while(sizer.size(rows[i])[0] > self._String__owner.rect.width and rows[i][-1] != " "):
            newRow = rows[i][-1] + newRow
            rows[i] = rows[i][:-1]
          if(rows[i][-1] != " "):
            newRow = rows[i][-1] + newRow
            rows[i] = rows[i][:-1] + "-"
        size = sizer.size(rows[i])[0]
      i = i + 1
      if(newRow != ""):
        rows.insert(i, newRow)
  self._String__rows._ProtectedList__val = rows
def StringSetRow(self): 
  self._String__realFontSize = self.fontSize
  if(self.maxRows >= 1):
    while(len(self._String__rows._ProtectedList__val) > self.maxRows):
      self._String__realFontSize = self._String__realFontSize - 1
      StringResize(self, False)
  if(self._String__owner != None):
    if(self._String__owner.rect.height > 0):
      while(self._String__owner.rect.height < self.GetSize()[1] and self._String__realFontSize > 0):
        self._String__realFontSize = self._String__realFontSize - 1
        StringResize(self, False)
def TransformText(self):
  if(self.text != None):
    self.text._String__rowChanged = True

def RenderText(self):
  font = self.text.sizer
  size = self.text.GetSize()
  copRect = pygame.Rect(0, 0, size[0], size[1])
  transformImage = pygame.Surface(size, pygame.SRCALPHA)
  for row in range(len(self.text.rows)):
    tempRect = copy.deepcopy(copRect)
    tempOffset = 0
    if(self.text.alignment == 1):
      tempOffset = (size[0] - font.size(self.text.rows[row])[0])/2
    elif(self.text.alignment == 2):
      tempOffset = (size[0] - font.size(self.text.rows[row])[0])
    tempRect[0] = tempRect[0] + tempOffset
    transformImage.blit(font.render(self.text.rows[row], True, self.text.fontColor, self.text.backgroundColor), tempRect)
    copRect.top = copRect.top + font.size(self.text.rows[row])[1]
  self._Object__transformedImage = transformImage

def SetColor(value, varName, className):
  Functions.TypeCheck(value, [tuple, type(None)], varName, className)
  output = None
  if(value != None):
    temp = []
    max = -1
    for i in value:
      if(i < 0):
        Functions.Err("color cant have a negative value")
      if(i > max):
        max = i
      temp.append(i)
    value = temp
    if(max > 255):
      for i in range(len(value)):
        value[i] = value[i] / max * 255
    if(value == None or len(value) == 4):
      output = (float(value[0]), float(value[1]), float(value[2]), float(value[3]))
    elif(len(value) == 3):
      output = (float(value[0]), float(value[1]), float(value[2]), 255.0)
    else:
      Functions.Err(className + "." + varName + " must have a length of 3 or 4 in RGBA or RGB format")
  return output
def UpdateRects(self):
  if(self._Rect__owner != None):
    self._Rect__owner._Object__updateLocal = self._Rect__global
    self._Rect__owner._Object__updateGlobal = not self._Rect__global
    for i in self._Rect__owner.Decendants():
      i._Object__updateGlobal = True
def SetEdited(self):
  owner = None
  if(type(self) == Rect):
    owner = self._Rect__owner
  elif(type(self) == RenderOptions):
    owner = self._RenderOptions__owner
  else:
    owner = self._String__owner
  if(owner != None):
    owner._Object__edited = True