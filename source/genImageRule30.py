import bpy

import random
#from random import seed
#from random import random

#https://en.m.wikipedia.org/wiki/Rule_30

class GenImageRule30Settings(bpy.types.PropertyGroup):
    image_name : bpy.props.StringProperty(
        name="Image Name", description="Name of image to generate", default = "rule30Image"
    )

    width : bpy.props.IntProperty(
        name="Width", description="Width of image", default = 512, min=1, soft_max = 1024
    )

    height : bpy.props.IntProperty(
        name="Height", description="Height of image", default = 512, min=1, soft_max = 1024
    )

    rand_seed : bpy.props.IntProperty(
        name="Randon Seed", description="Random Seed", default = 0
    )

    start_state : bpy.props.EnumProperty(
        items=(
            ('SINGLE', "Single Cell", "Start with a singe cell"),
            ('RANDOM', "Random", "First row has random data"),
        ),
        default='SINGLE'
    )
    

#-------------------------------------

class GenImageRule30Operator(bpy.types.Operator):
    """Generate a cellular automa image using Rule 30"""
    bl_idname = "kitfox.gen_image_rule30_operator"
    bl_label = "Generate a cellular automa image using Rule 30"
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self):
        self.dragging = False

    def execute(self, context):
        props = context.scene.rule30_props
    
        width = props.width
        height = props.width
        
        cells = [0] * width * height
        
        if props.start_state == 'SINGLE':
            cells[width // 2] = 1
        elif props.start_state == 'RANDOM':
            
            random.seed(props.rand_seed)
            
            for i in range(width):
                cells[i] = random.randint(0, 1)
        
        for j in range(1, height):
            for i in range(width):
                p0 = 0 if i == 0 else cells[(j - 1) * width + i - 1]
                p1 = cells[(j - 1) * width + i]
                p2 = 0 if i == width - 1 else cells[(j - 1) * width + i + 1]
                
                #apply rule 30
                code = p0 * 4 + p1 * 2 + p2
                value = 0
                if code >= 1 and code <= 4:
                    value = 1
                cells[j * width + i] = value

        #Generate image
        name = props.image_name
        image = bpy.data.images.new(name, width, height)
        pixels = [None] * width * height
        for i in range(width * height):
            pixels[i] = (1, 1, 1, 1) if cells[i] == 0 else (0, 0, 0, 1)
            
        pixels = [chan for px in pixels for chan in px]
        image.pixels = pixels

        return {'FINISHED'}
        
        
        
        
#---------------------------


class GenImageRule30Panel(bpy.types.Panel):
    """Generate Image using Wolfram's Rule 30 method"""
    bl_label = "Generate Image Rule 30"
    bl_idname = "OBJECT_PT_gen_image_rule30_props"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "Kitfox"


    def draw(self, context):
        layout = self.layout

        scene = context.scene
        props = scene.rule30_props
        
        col = layout.column();
        col.operator("kitfox.gen_image_rule30_operator", text="Generate Image")
        
        col.prop(props, "image_name")
        col.prop(props, "width")
        col.prop(props, "height")
        col.prop(props, "start_state")
        col.prop(props, "rand_seed")
        
        
        

#---------------------------


def register():
    bpy.utils.register_class(GenImageRule30Settings)
    bpy.utils.register_class(GenImageRule30Operator)
    bpy.utils.register_class(GenImageRule30Panel)

    bpy.types.Scene.rule30_props = bpy.props.PointerProperty(type=GenImageRule30Settings)

def unregister():
    del bpy.types.Scene.rule30_props

    bpy.utils.unregister_class(GenImageRule30Settings)
    bpy.utils.unregister_class(GenImageRule30Operator)
    bpy.utils.unregister_class(GenImageRule30Panel)


if __name__ == "__main__":
    register()