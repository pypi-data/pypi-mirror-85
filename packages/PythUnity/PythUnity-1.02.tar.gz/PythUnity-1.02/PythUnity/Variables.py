from PythUnity.Functions import Err
from PythUnity.Functions import TypeCheck
from PythUnity.ProtectedList import ProtectedList
from PythUnity import __file__
import pygame
import os
class Var:
    def  __init__(self):
        self.__parts = ProtectedList("parts", "v", False, False, False, False)
        self.__deltaTime = 0
        self.__prefabs = {}
        self.__starts = []
        self.__backgroundColor = (255, 255, 255)
        self.__mousePosition = (0, 0)
        self.__oldMousePosition = (0, 0)
        self.__screenRect = (800, 600)
        self.__mouseDragging = False
        self.__PreRender = None
        self.icon = pygame.transform.scale(pygame.image.load(os.path.dirname(__file__) + "/Assets/Icon.jpg"), (32, 32))
        self.appName = "PythUnity window"
        self.keys = {}
    ######
    @property
    def icon(self):
      return self.__icon
    @icon.setter
    def icon(self, value):
      TypeCheck(value, pygame.Surface, "icon", "v.")
      pygame.display.set_icon(value)
      self.__icon = value
    @property
    def appName(self):
      return self.__appName
    @appName.setter
    def appName(self, value):
      TypeCheck(value, str, "appName", "v.")
      pygame.display.set_caption(value)
      self.__appName = value
    @property
    def parts(self):
      return self.__parts
    @parts.setter
    def parts(self, value):
      Err("cant set PythUnity.v.parts, use PythUnity.Object() to create and Object.Destroy() to remove, this is only for getting objects at index, run PythUnity.help() for help")
    @property
    def deltaTime(self):
      return self.__deltaTime
    @deltaTime.setter
    def deltaTime(self, value):
      Err("cant set PythUnity.v.deltaTime, use this to see how much time passed since the last Update call")
    @property
    def prefabs(self):
      return self.__prefabs
    @prefabs.setter
    def prefabs(self, value):
      Err("cant set PythUnity.v.prefabs, use PythUnity.AddPrefab() and PythUnity.GetPrefab(), for more information on this run PythUnity.help()")
    @property
    def starts(self):
      return self.__starts
    @starts.setter
    def starts(self, value):
      Err("cant set PythUnity.v.starts, add each start function individually")
    @property
    def mousePosition(self):
      return self.__mousePosition
    @mousePosition.setter
    def mousePosition(self, value):
      Err("cant set PythUnity.v.mousePosition, use this to get the position of the mouse")
    @property
    def oldMousePosition(self):
      return self.__oldMousePosition
    @oldMousePosition.setter
    def oldMousePosition(self, value):
      Err("cant set PythUnity.v.oldMousePosition, use this to get the last position of the mouse")
    @property
    def mouseDragging(self):
      return self.__mouseDragging
    @mouseDragging.setter
    def mouseDragging(self, value):
      Err("cant set PythUnity.v.mouseDragging, use this to see if the mouse is calling Button.Drag functions")
    ###
    @property
    def backgroundColor(self):
      return self.__backgroundColor
    @backgroundColor.setter
    def backgroundColor(self, value):
      TypeCheck(value, tuple, "backgroundColor", "v.")
      self.__backgroundColor = value
    @property
    def screenRect(self):
      return self.__screenRect
    @screenRect.setter
    def screenRect(self, value):
      TypeCheck(value, tuple, "", "screenRect")
      self.__screenRect = value
    @property
    def PreRender(self):
      return self.__PreRender
    @PreRender.setter
    def PreRender(self, value):
      TypeCheck(value, [type(self.__init__), type(TypeCheck), type(None)], "PreRender", "v.")
      self.__PreRender = value
###
global var
var = Var()

global updates
updates = []