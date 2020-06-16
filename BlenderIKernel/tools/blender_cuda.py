# blender -b -P available_device.py
# /f/bin4/blender-2.82-windows64/blender.exe  -P A_RENDER/blender_cuda.py -b "C:\Users\diego2\Desktop/Caja Plastica 1.blend"

# blender -b Nave.blend  -o //nave_###.png -P ~/cuda_setup.py -f 1

# blender -b file.blend -P cuda1.py -s 1 -e 10 -a &
# blender -b file.blend -P cuda2.py -s 11 -e 20 -a &

import sys,os,time
import bpy,  _cycles
import math

LEGACY_MODE = bpy.app.version < (2, 80, 0) #Switch based on version for Blender 2.8+ or legacy support.

#o = byp.data.object[0]
#if LEGACY_MODE:
#    o.hide = False #unhide object using legacy commands
#else:
#    o.hide_viewport = 0 #unhide object using modern commands

current_dir = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(current_dir, "output.jpg")

bpy.context.scene.cycles.device = 'CPU'
bpy.context.scene.render.engine='BLENDER_WORKBENCH'
bpy.ops.wm.read_homefile()

scene = bpy.context.scene
scene.render.resolution_x = 800
scene.render.resolution_y = 600

bpy.ops.object.select_pattern(pattern="Plane*")

target = bpy.context.selected_objects[0]

#activeObject = bpy.context.active_object #Set active object to variable
mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
target.data.materials.append(mat) #add the material to the object
#bpy.context.object.active_material.diffuse_color = (1, 0, 0) #change color
mat.diffuse_color = (1,0,0,1)
# (or bpy.data.materials['Materialname'].diffuse_color) i
#scene.objects.active = target

cam_x_pos = max([v[0] for v in target.bound_box]) * 0.3
cam_y_pos = max([v[1] for v in target.bound_box]) * 0.3
cam_z_pos = max([v[2] for v in target.bound_box]) * 4.2

rot_centre = bpy.data.objects.new('rot_centre', None)
#scene.objects.link(rot_centre)
bpy.context.collection.objects.link(rot_centre)

rot_centre.location = target.location

ca = bpy.data.objects.new('newcam', bpy.data.cameras.new('newcam'))
ca.location = (cam_x_pos, cam_y_pos, cam_z_pos)
ca.parent = rot_centre
m = ca.constraints.new('TRACK_TO')
m.target = target
m.track_axis = 'TRACK_NEGATIVE_Z'
m.up_axis = 'UP_Y'

#ca.rotation= (-0.7853, 0, 0)
bpy.context.collection.objects.link(ca)
#ca = bpy.data.cameras.new('newcam')
# ca.angle = math.radians(84.5661)
# ca.lens_unit = 'FOV'
# ca.display_size = 0.5
lamp = bpy.data.objects.new('lamp', bpy.data.lights.new('lamp', type='SUN'))
lamp.location=(0, 5, 0)
bpy.context.collection.objects.link(lamp)

rot_centre.rotation_euler.z = 0.0
rot_centre.keyframe_insert('rotation_euler', index=2, frame=1)
rot_centre.rotation_euler.z = math.radians(360.0)
rot_centre.keyframe_insert('rotation_euler', index=2, frame=101)
# set linear interpolation for constant rotation speed
for c in rot_centre.animation_data.action.fcurves:
    for k in c.keyframe_points:
        k.interpolation = 'LINEAR'
scene.frame_end = 100

# bpy.context.scene.update()
bpy.context.view_layer.update()

sceneKey = bpy.data.scenes.keys()[0]

for obj in bpy.data.objects:
	if ( obj.type =='CAMERA') and ( obj.name == 'cam1' or obj.name == 'cam2') and type=="0":
		pass

bpy.context.scene.camera = bpy.data.objects['newcam']
#bpy.context.scene.camera = bpy.data.objects['Camera']
scene.camera = ca

#bpy.data.scenes[sceneKey].camera = obj
bpy.data.scenes[sceneKey].render.filepath = out
bpy.ops.render.render('INVOKE_DEFAULT', write_still=True )
bpy.ops.wm.quit_blender()
