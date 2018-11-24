import bpy
from bpy.props import *
from bpy.types import Collection
from .. events import propertyChanged
from .. base_types import AnimationNodeSocket, PythonListSocket

class CollectionSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_CollectionSocket"
    bl_label = "Collection Socket"
    dataType = "Collection"
    drawColor = (0.3, 0.1, 0.1, 1.0)
    storable = False
    comparable = True

    collectionName: StringProperty(update = propertyChanged)

    def drawProperty(self, layout, text, node):
        layout.prop_search(self, "collectionName", bpy.data, "collections", text = text)

    def getValue(self):
        return bpy.data.collections.get(self.collectionName)

    def setProperty(self, data):
        self.collectionName = data

    def getProperty(self):
        return self.collectionName

    @classmethod
    def getDefaultValue(cls):
        return None

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, Collection) or value is None:
            return value, 0
        return cls.getDefaultValue(), 2


class CollectionListSocket(bpy.types.NodeSocket, PythonListSocket):
    bl_idname = "an_CollectionListSocket"
    bl_label = "Collection List Socket"
    dataType = "Collection List"
    baseType = CollectionSocket
    drawColor = (0.3, 0.1, 0.1, 0.5)
    storable = False
    comparable = False

    @classmethod
    def getCopyExpression(cls):
        return "value[:]"

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, list):
            if all(isinstance(element, Collection) or element is None for element in value):
                return value, 0
        return cls.getDefaultValue(), 2
