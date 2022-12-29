
bl_info = {
    "name": "All Project Timer",
    "author": "Genchan96",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "Info",
    "description": "Show time spent on all project",
    "warning": "This script a beta version. It may have bugs.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Interface"}



import bpy
import time
from bpy.app.handlers import persistent 
import getpass

class ProjectTimerReset(bpy.types.Operator):
    bl_idname = "poject_timer.reset"
    bl_label = "Reset Project Timer"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        bpy.projectTime = 0
        return {'FINISHED'}

class AllProjectTimerPreferences(bpy.types.AddonPreferences):

    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator("poject_timer.reset")
        
            
bpy.types.Scene.projectTime = bpy.props.IntProperty(
            name = "Project Time",
            description='All time spent on project',
            default = 0)

def draw_counter(self, context):
    projectTimerUpdate(context.scene)
        
    layout = self.layout
    region = context.region    

    if region.alignment == 'RIGHT':
        seconds = bpy.projectTime
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        layout.label(text=str(h)+':'+format(m, '02d')+':'+format(s, '02d'))

def projectTimerUpdate(scene):
    if not hasattr(bpy, 'projectTimestamp'): #first open

        bpy.projectTimestamp = int(time.time())
        print('Project Time: ', bpy.projectTime)
        print('Project Timestamp: ', bpy.projectTimestamp)
    delta = int(time.time()) - bpy.projectTimestamp
    if delta < 30:
        bpy.projectTime += delta
    bpy.projectTimestamp = int(time.time())

@persistent 
def projectTimerSave(scene):
    projectTimerUpdate(scene)
    username = getpass.getuser()
    txtpass3 = "C:/Users/" + username + "/AppData/Roaming/Blender Foundation/Blender/time.txt"
    with open(txtpass3,"w") as f:
            f.write(str(bpy.projectTime))    
    print('Project Time saved', bpy.projectTime)

@persistent    
def projectTimerLoad(scene):
    
    username = getpass.getuser()
    txtpass3 = "C:/Users/" + username + "/AppData/Roaming/Blender Foundation/Blender/time.txt"
    try:
        with open(txtpass3,"r") as f:
            t2 = f.read()
            t2_int = int(t2)
        bpy.projectTime = t2_int
    except FileNotFoundError:
        with open(txtpass3, "w") as f:
            f.write("0")
           
    bpy.projectTimestamp = int(time.time())
    print('Project Time loaded', bpy.projectTime)

def register():
    bpy.app.handlers.load_post.append(projectTimerLoad)
    bpy.app.handlers.save_pre.append(projectTimerSave)
    bpy.utils.register_class(ProjectTimerReset)
    bpy.utils.register_class(AllProjectTimerPreferences)
    bpy.types.TOPBAR_HT_upper_bar.append(draw_counter)


def unregister():
    bpy.app.handlers.load_post.remove(projectTimerLoad)
    bpy.app.handlers.save_pre.remove(projectTimerSave)
    bpy.utils.unregister_class(ProjectTimerReset)
    bpy.utils.unregister_class(AllProjectTimerPreferences)
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_counter)
    

if __name__ == "__main__":
    register()
