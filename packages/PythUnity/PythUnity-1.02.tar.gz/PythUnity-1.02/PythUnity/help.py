import os

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def cls():os.system('cls' if os.name=='nt' else 'clear')
def border():
  print("///////////////////////////")
def smallBorder():
  print("//////////")
def option(number, text):
  print(str(number) + ". " + text)
def options(array):
    border()
    if(len(array) >= 2):
      print(array[0] + ": ")
      print(array[1])
    smallBorder()
    for i in range(len(array[2])):
        if(type(array[2][i]) == tuple):
            option(i, array[2][i][0])
        else:
            option(i, array[2][i])
    smallBorder()
    if(len(array[2]) != 0):
        user = input("Type the number choice or press {ENTER} to go back: ")
        while(user != "" and (not RepresentsInt(user) or int(user) >= len(array[2]))):
           if(not RepresentsInt(user)):
             print("incorrect format")
           else:
             print("option out of range")
           user = input("Type the number choice or press {ENTER} to go back: ")
        if(user != ""):
          cls()
          if(len(array[2][int(user)]) == 3):
            options(array[2][int(user)])
            cls()
            options(array)
          else:
            input("type {ENTER} to continue: ")
          border()
          return False
    else:
      input("type {ENTER} to continue: ")
    border()
    return True
cls()
print("Run PythUnity.help() for help")
border()
def help():
    array = ("Help Options", "This is the help menu!\ntype the number of one of the options below for more information\nnote: going in order is recommended\n\nif you use features not talked about here you will most likely crash the application", [
        ("Startup", "to start up its very simple\nheres an example of a startup:\n\nimport PythUnity\n#PythUnity.help()\ndef Start():\n   print(\"started\")\nPythUnity.v.starts.append(Start)\nPythUnity.init()\n\nAnd thats all you have to do, \nyou can put whatever you want before PythUnity.init() runs but after you run PythUnity.init() the rest of your code wont run,\nso you'll have to use buttons and components to get what you need done, \nas you go throught this help section you'll learn how to do so", []),
        ("Creating Objects", "You can create GameObjects just like in Unity! by using PythUnity.Object(), choose one of the options too learn more", [
            ("Creating Rectangles", "to create a rectange you must do PythUnity.Object(transform, color) \nthe transform parameter is an instance of the PythUnity.Rect() value,\nThe color parameter is a tuple ie. (255, 255, 255) or (255, 255, 255, 50) for semi transparency\nthe two formats you can use are RGB and RGBA", [
                ("PythUnity.Rect", "instantiating the PythUnity.Rect looks like this PythUnity.Rect(dist_from_left, dist_from_top, width, height)", [
                    ("Methods", "", [
                        ("Copy()", "returns a copy of the Rect", [])]),
                    ("Variables", "all the variables", [
                        ("left", "distance from the left side from screen", []),
                        ("top", "distance from the top side from screen", []),
                        ("width", "width in pixels", []),
                        ("height", "height in pixels", [])])])]), 
            ("Creating Images", "if you dont know how to make a rectange I would recommend going back\nmaking an image is alot like making a rectange\nthe difference is instead of using a color you do a PythUnity.Surface\nan example is PythUnity.Object(transform, PythUnity.image(image_path_string))\nthe code above will make an object with an image from that filepath", [
                ("Image Coloring", "you can change the color of images\nfor example take the example we just saw and add \n.color = (50, 255, 50)\nto turn the image green\n\nimage = PythUnity.Object(PythUnity.Rect(0, 0, 500, 500), PythUnity.image(\"image.jpg\"))\nimage.color = (50, 255, 50)", []),
                ("PythUnity.Surface & PythUnity.image", "PythUnity.Surface and PythUnity.image are the same as pygame.Surface and pygame.image, \nso for documentation go to https://www.pygame.org/docs/\nNote: PythUnity.imag.load is different from pygame.image.load because PythUnity.image.load supports transparency", [
                    ("PythUnity.image.load", "its the same as pygame.image.load except that it sets the colorKey to support PNG transparency it also converts it to a Surface to speed up rendering\nfor example: \nPythunity.image.load(\"Image.png\", colorKey=(255, 0, 0))\n\nthis will make the color red transparent, by default the colorKey is set to None\nif the colorKey is set to None it will make a image without a alpha channel\nremoving the alpha channel speeds up rendering alot", [])]),]), 
            ("Creating Text", "Creating text takes more space but is just as easy as the others, select one of the options to learn more", [
                ("Format", "the format for creating text looks like this:\nPythUnity.Object(transform, PythUnity.String(message, font_size, font, font_color, background_color, alignment = 0, maxRows=0))", []),
                ("PythUnity.String", "this is the type that stores data on how the text is displayed on the screen\nif you set the PythUnity.Object.rect.width then it will\nkeep the text from going past the width and will instead make new lines\nbut if the width is set to 0 or less, it will keep going as one line\nif the height is greater than 0 than it will scale the font size down to fit the height", [
                    ("Methods", "", [
                        ("GetSize()", "gets the amount of pixels it takes up", []),
                        ("Copy()", "returns a copy of the object", [])]),
                    ("Variables", "all the variables", [
                        ("rows", "a string array of every line", []),
                        ("alignment", "the alignment of the object\n0->left\n1->middle\n2->right", []),
                        ("fontSize", "a integer of the font size", []),
                        ("text", "a string of the plain text before its made into rows", []),
                        ("font", "a string type of the font\nto get all available fonts on the system run PythUnity.GetFonts()", []),
                        ("fontColor", "a tuple of RGB or RGBA format of the color of the text", []),
                        ("backgroundColor", "a tuple of RGB or RGBA format of the color of the highlight of the text,\ncan be None to not have a highlight", []),
                        ("maxRows", "a integer saying the max amount of rows the String can have before scaling fontSize down\nif its less than 1 then it will be ignored\nnote: it wont change the fontSize variable, just how big the text displays on the screen", []),
                        ("sizer", "creates a pygame.font.Font() from the String\nyou can use it to get the size of rows in pixels, for example:\n\ndef Test():\n\ttextObj = PythUnity.Object(PythUnity.Rect(0, 0, 0, 0), PythUnity.String(\"line1\\nline2\", 40, \"freesansbold\", (0, 0, 0), None))\n\tprint(textObj.text.sizer.size(textObj.text.rows[1]))\nPythUnity.v.starts.append(Test)\nPythUnity.init()", [])])]),
            ("Example", "this will create a highlighted text saying hi: \ntext = PythUnity.String(\"hi\", 24, \"freesansbold\", (255, 255, 0), (0, 255, 255))\nPythUnity.Object(PythUnity.Rect(280, 150, 100, 200), text)", [])]),
            ("Creating Buttons", "when instantiating the Object class there are additional parameters that allow you to make buttons\n these additional parameters are: \nObject(onClick, onDrag, onClickOff, onScroll, onHover, onHoverOff, onHoverOn, enableDragOff, clickGroup)",[
                ("Button Type, PythUnity.Button", "this is the class type of Object.button\nto instatiate this type do:\nPythUnity.Button(onClick, onDrag, onClickOff, onScroll, onHover, onHoverOff, onHoverOn, enableDragOff)\nheres an example:\ndef Click(self, button):\n    print(\"clicked with button \" + button)\nbutton = PythUnity.Button(Click)", [
                    ("Variables", "all the variables", [
                        ("hovering", "returns true if mouse is hovering over object, good for knowing if the onHover() function is running", []),
                        ("dragging", "returns true if object is being dragged, good for knowing if the onDrag() function is running", []),
                        ("enableDragOff", "is a boolean, if enabled if your mouse stops hovering over the object while your dragging \nit will still run the onDrag() function till you let go", [])]),
                    ("Methods", "A list of methods that you can set, more method info in the \"Creating Buttons\" section", [
                        ("onClick", "takes arguments (object_ran_on, string_button_name)\nnote: if button was blocked this will run with string_button_name as \"Blocked\" and if the mouse stops hovering over the button it will run with string_button_name as \"Off\"", []),
                        ("onDrag", "takes arguments (object_ran_on)", []),
                        ("onClickOff", "takes arguments (object_ran_on, string_button_name)\nif blocked, string_button_name=\"Blocked\"\nif fell off, string_button_name=\"Off\"\nif let go, string_button_name=MOUSE_BUTTON_NAME", []),
                        ("onScroll", "takes arguments (object_ran_on, int_direction)\nup: int_direction = 1\ndown: int_direction = -1", []),
                        ("onHover", "takes arguments (object_ran_on)", []),
                        ("onHoverOn", "takes arguments (object_ran_on)", []),
                        ("onHoverOff", "takes arguments (object_ran_on, reason)\nif blocked, reason=\"Blocked\"\nif fell off, reason=\"Off\"", [])])]),
                ("Object.button.onClick", "is a method, whenever you click the object this function will run", []),
                ("Object.button.onDrag", "is a method, whenever you hold the mouse button on the object this function will run", []),
                ("Object.button.onClickOff", "is a method, whenever you click off the object this function will run", []),
                ("Object.button.onScroll", "is a method, whenever you use the scroll button while hovering over the Object this will run", []),
                ("Object.button.onHover", "is a method, whenever your mouse is over the button it will run", []),
                ("Object.button.onHoverOff", "is a method, whenever your mouse stops hovering it will run", []),
                ("Object.button.onHoverOn", "is a method, whenever your mouse starts hovering over an object it will run", []),
                ("Object.button.enableDragOff", "is a boolean, if enabled if your mouse stops hovering over the object while your dragging \nit will still run the drag funciton till you let go", []),
                ("Object.clickGroup", "talked about in \"Object Variables\" section", [])])]),
        ("Object Methods", "Objects come with many built in tools, some you will need to know, some will be useful to know\nHeres a list of all the functions, its recommended to go in order", [
            ("Move(index)", "this function moves the object around the layer\nimagine you have a stack of papers and you move the 56th page down to the 30th page, thats what .Move does, it moves the page to the index'th page", []),
            ("SetParent(target)", "this function sets the parent of an object to another\nimagine you have a russian doll and you put another doll into it, thats what .SetParent does, \nit takes the doll out of one doll and then puts it into another, and in this case the other doll is the target variable", []),
            ("GetParentChildren()", "this function get the children of the parent, remember the russian doll example? the children are the smaller dolls", []),
            ("Copy()", "this makes a copy of the Object and returns the copy, the copy will have all the same attriutes of the old one, including position so make sure to move it", []),
            ("Destroy()", "this will destroy the object its run on, \nthis will cause it to no longer be rendered or in the child list of the parent, \nrunning functions on destroyed objects will cause the program to crash", []),
            ("AddComp(comp)", "this will add a component,\na component is like a script, just like Unity it has a Start(), and Update() function\nan example you can run is:\nrandObj = PythUnity.Object(PythUnity.Rect(500, 500, 750, 300), (255, 0, 0))\ndef Banana(self):\n   print(\"banana start\")\ndef Apple(self):\n   print(\"apple update\")\nrandObj.AddComp((Banana, Apple))", []),
            ("DelComp(index)", "this will remove a component from the component list at an index,\nfor example if we took the example from AddComp and then ran: \nrandObj.DelComp(0)\nit wouldve removed the component we just added", []),
            ("Decendants()", "this will get all the children of the object your running it on, \naswell as the children of those children and so on and so on", []), 
            ("SetClickGroup(new_click_group)", "this will set the clickGroup variable of all the objects that are a decendant of the object it was run on", []),
            ("SetEnabled(value)", "this will set the enabled variable of all the objects that are a decendant of the object it was run on", [])]),
       ("Object Variables", "the Object class also comes with variables", [
            ("rect", "a PythUnity.Rect describing the objects position relative to its parent", []),
            ("globalRect", "a PythUnity.Rect describing the objects real position", []),
            ("children", "an array of all the children an Object has\nas a shortcut you can do PythUnity.Object[i] instead of PythUnity.Object.children[i]", []),
            ("destroyed", "says whether an Object is destroyed or not", []),
            ("parent", "returns the parent of the object, if the object doesnt have a parent it will return None", []),
            ("variables", "a dictionary where components store their variables", []),
            ("image", "if you created an Object with an image it will show here", []),
            ("transformedImage", "if the object is a image it will return the image variable after scale and color are applied to it\nif the object is a text it wil lreturned the rendered form of the text", []),
            ("text", "if you created an Object with text it will show here", []),
            ("color", "if you created an Object with a color it will show here", []),
            ("components", "shows a list of all of your Objects components", []),
            ("clickGroup", "an int that allows you to set the clickGroup of the Object, \nobjects in the same clickGroup wont block eachoher from being clicked\nuseful if you have an image over a button and you dont want the button to get blocked by the image", []),
            ("velocity", "a tuple for the x and y speed of an object, represented as (x, y)", []),
            ("button", "hold information on the onClick and OnDrag etc of the Object, it is a PythUnity.Button type, \nif you didnt add any button functions this value will be set to None", [
                ("Methods", "", [
                    ("onClick", "its the same as the onClick in the Object parameters", []),
                    ("onClickOff", "its the same as the onClickOff in the Object parameters", []),
                    ("onDrag", "its the same as the onDrag in the Object parameters", []),
                    ("onScroll", "its the same as the onScroll in the Object parameters", []),
                    ("onHoverOff", "its the same as the onHoverOff in the Object parameters", []),
                    ("onHoverOn", "its the same as the onHoverOn in the Object parameters", []),
                    ("onHover", "its the same as the onHover in the Object parameters", [])]),
                ("Variables", "", [
                    ("enableDragOff", "its the same as the enableDragOff in the Object parameters", []),
                    ("dragging", "says if the Object is currently being dragged", [])])]),
            ("renderOptions", "the renderOptions of the Object", [
                ("RenderOptions Type, PythUnity.RenderOptions", "this is the class type of renderOptions", [
                    ("Variables", "all the variables", [
                        ("fitImage", "if True and the Object is a image it will fill the rect.width and rect.height of the object\nfor example:\n\n#This image will take up 500 by 500 pixels\nimgObj = PythUnity.Object(PythUnity.Rect(0, 0, 500, 500), PythUnity.image.load(\"image.jpg\"), fitImage=True)\n\n#In this image either the width or height of the image will be 500 pixels depending on which is bigger\nimgObj = PythUnity.Object(PythUnity.Rect(0, 0, 500, 500), PythUnity.image.load(\"image.jpg\"))\n", [])]),
                        ("effect", "not implemented yet", [])])]),
            ("enabled", "by default is set to True,\nif False object will not render or recieve button presses\nif True object will render and recieve button presses", []),]),
        ("Prefabs", "A prefab is a blueprint to create an object", [
            ("AddPrefab", "you can use PythUnity.AddPrefab(\"name\", part) \nto create a prefab from a part and store it at the name string\nheres an example: \npart = PythUnity.Object(PythUnity.Rect(0, 0, 100, 100), (255, 0, 0))\nPythUnity.AddPrefab(\"Square\", part)", []),
            ("GetPrefab", "you can use PythUnity.GetPrefab(\"name\") \nto create a part from a prefab that is stored at the name string\nheres an example: \npart = PythUnity.GetPrefab(\"Square\")", [])]),
        ("Global Variables", "Global Variables are variables that PythUnity uses\nYou can access global variables with \"PythUnity.v\" for example \"PythUnity.v.deltaTime\"\nbelow are all the variables", [
            ("deltaTime", "a float value of the amount of seconds between each render", []),
            ("parts", "an array of all the Objects that are not parented", []),
            ("prefabs", "a dictionary of all the Prefabs that have been made", []),
            ("starts", "an array used to define which functions you want PythUnity to run at the beggining", []),
            ("backgroundColor", "a 3 length tuple that represents a RGB format color for the background of the window", []),
            ("mousePosition", "a 2 length tuple representing the xy coordiantes of the mouse in the window", []),
            ("oldMousePosition", "a 2 length tuple representing the last xy coordiantes of the mouse in the window", []),
            ("screenRect", "a 2 length tuple representing (width, height) of the window\nnote: you have to set this before calling PythUnity.init()", []),
            ("mouseDragging", "a bool saying whether or not the mouse is being held down", []),
            ("icon", "a PythUnity.Surface that represents the icon on the top left of the window\nsetting it will change the window icon", []),
            ("appName", "a string that represents the text on the top left of the window\nsetting it will change the text", []),
            ("keys", "a dictionary with they keyboard button names as the keys,\neach item in the dictionary has 3 values:\n\"Clicked\": was just pressed\n\"Held\": is being held\n\"Off\": was just released", []),
            ("PreRender", "a settable function that is run right before pygame.update()", []),
            ("PythUnity.Variables.updates", "an array of pyame.rect \nused in pygame.update()\nUseful for using in the PreRender function", [])]),
        ("ProtectedList", "the type used in Object.children, Object.components, and String.rows\n\nits like a normal array but it will throw an error if you append, insert, or delete an item from a list \nif the list prohibits it\n\nNote: indexing, looping, and getting the length is the same as a normal array", [
            ("Methods", "", [
                ("append", "same as array.append but will throw error if your not allowed to append", []),
                ("insert", "same as array.insert but will throw error if your not allowed to append", [])]),
            ("Hidden Variables", "only use/change if you know what your doing\nyou will most likely cause errors in random parts of your code if you edit these", [
                ("_ProtectedList__canAppend", "says if appending is allowed", []),
                ("_ProtectedList__canInsert", "says if inserting is allowed", []),
                ("_ProtectedList__canDelete", "says if deleting items is allowed", []),
                ("_ProtectedList__allowedTypes", "either a type variable or a list of type variables describing which types can be added to the list\nif its an empty array then all types are allowed", []),
                ("_ProtectedList__val", "the base array of the ProtectedList\nediting this will bypass all the protection", [])])])])
    while(True):
      cls()
      if(options(array)):
        if(input("Do you want to Exit? Y/N: ") == "Y"):
          break
      else:
        break
    cls()
