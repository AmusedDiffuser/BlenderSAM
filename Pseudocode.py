# BlenderSAM Segment Anything Addon for Blender (Pseudocode v2)

"""
This addon allows you to use the Segment Anything Model (SAM) from Meta AI to segment objects in images and 3D models using input prompts such as points, boxes, or text. SAM is a promptable segmentation system with zero-shot generalization to unfamiliar objects and images, without the need for additional training. You can use this addon to generate masks and materials for all objects in an image, use them as references for 3D modeling, and segment different parts of a 3D model and apply different textures or materials to them.
"""

# Import the required modules
import bpy
import bmesh
import mathutils
import segment_anything
import numpy as np
import cv2
import matplotlib.pyplot as plt
import onnxruntime as ort
import os

# Define some variables or arguments that can be customized by the user or detected automatically by the script
image_path = "path/to/image/file" # The path to the image file to be segmented
model_path = "path/to/model/checkpoint" # The path to the model checkpoint for the Segment Anything model
model_type = "point" # The type of input prompt to use for segmentation ("point", "box", or "text")
output_path = "path/to/output/folder" # The path to the output folder where the masks and materials will be saved

# Define some options or parameters that can improve or customize the segmentation results
threshold = 0.5 # The threshold value for binarizing the masks
confidence = 0.9 # The confidence value for filtering out low-confidence masks
num_classes = 10 # The number of classes to segment in an image or model
num_samples = 100 # The number of samples to use for text-based segmentation
num_iterations = 10 # The number of iterations to run the model for each input prompt
num_proposals = 5 # The number of proposals to generate for each input prompt
num_refinements = 3 # The number of refinements to apply for each proposal
num_samples_per_class = 10 # The number of samples to use for each class in automatic segmentation
num_classes_per_prompt = 5 # The number of classes to segment for each input prompt in manual segmentation
num_samples_per_prompt = 20 # The number of samples to use for each input prompt in manual segmentation
num_iterations_per_prompt = 5 # The number of iterations to run the model for each input prompt in manual segmentation
num_proposals_per_prompt = 3 # The number of proposals to generate for each input prompt in manual segmentation
num_refinements_per_prompt = 2 # The number of refinements to apply for each proposal in manual segmentation

# Load the image file using Blender's image module
try:
    # Check if the image path is valid and exists
    if os.path.isfile(image_path):
        # Use Blender's image open operator to load the image file
        bpy.ops.image.open(filepath=image_path)
        # Get the image object from Blender's data by its name
        image_name = os.path.basename(image_path)
        image = bpy.data.images[image_name]
    else:
        raise FileNotFoundError("Image file not found")
except RuntimeError:
    print("Error: Cannot load image file")

# Load the model checkpoint using ONNX Runtime
try:
    # Check if the model path is valid and exists
    if os.path.isfile(model_path):
        # Use ONNX Runtime to load the model checkpoint
        session = ort.InferenceSession(model_path)
    else:
        raise FileNotFoundError("Model checkpoint not found")
except RuntimeError:
    print("Error: Cannot load model checkpoint")

# Generate masks and materials for all objects in the image using the Segment Anything model
try:
    # Convert the image to a numpy array
    image_array = np.array(image.pixels).reshape(image.size[0], image.size[1], 4)
    
    # Use the Segment Anything model to segment all objects in the image automatically without any input prompts
    masks, labels = segment_anything.segment(image_array, session, model_type="auto", threshold=threshold, confidence=confidence, num_classes=num_classes, num_samples_per_class=num_samples_per_class)
    
    # Create a list of images and materials for each mask and label pair
    images = []
    materials = []
    for i in range(len(masks)):
        # Create an image object from the mask array and name it with the prefix "SAM_input"
        mask_image = bpy.data.images.new(f"SAM_input_{i}", width=image.size[0], height=image.size[1])
        mask_image.pixels = masks[i].flatten()
        images.append(mask_image)
        
        # Create a material object from the label and name it with the prefix "_material"
        material = bpy.data.materials.new(f"_material_{i}")
        material.use_nodes = True
        
        # Use the mask image as the alpha texture for the material
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Get the principled BSDF node and set its base color to the label color
        principled_node = nodes.get("Principled BSDF")
        principled_node.inputs["Base Color"].default_value = labels[i]
        
        # Add an image texture node and set its image to the mask image
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = mask_image
        
        # Add a mix shader node and set its factor to 0.5
        mix_node = nodes.new("ShaderNodeMixShader")
        mix_node.inputs["Fac"].default_value = 0.5
        
        # Link the nodes together
        links.new(principled_node.outputs["BSDF"], mix_node.inputs[1])
        links.new(texture_node.outputs["Alpha"], mix_node.inputs[2])
        
        # Set the material output node's input to the mix shader node's output
        output_node = nodes.get("Material Output")
        links.new(mix_node.outputs["Shader"], output_node.inputs["Surface"])
        
        materials.append(material)
        
    # Save the images and materials to the output folder using Blender's operators module
    for i in range(len(images)):
        # Check if the output folder is valid and exists
        if os.path.isdir(output_path):
            # Use Blender's image save as operator to save each image object as a png file in the output folder 
            bpy.ops.image.save_as(save_as_render=False, filepath=output_path + f"/SAM_input_{i}.png", relative_path=True)
            # Use Blender's libraries write operator to save each material object as a blend file in the output folder 
            bpy.data.libraries.write(output_path + f"/_material_{i}.blend", {materials[i]})
            
except RuntimeError:
    print("Error: Cannot generate masks and materials")

# Create models from masks and materials using Blender's mesh module
try:
    # Create a list of plane objects for each mask and material pair using Blender's mesh primitive plane add operator 
    planes = []
    for i in range(len(masks)):
        # Use Blender's mesh primitive plane add operator to create a plane object and name it with the prefix "plane_"
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1))
        plane_object = bpy.context.active_object
        plane_object.name = f"plane_{i}"
        
        # Scale the plane object to match the mask shape using Blender's transform resize operator
        bpy.ops.transform.resize(value=(masks[i].shape[1], masks[i].shape[0], 1))
        
        # Extrude the plane object along the z-axis based on the mask values using Blender's mesh extrude operator
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, masks[i] * 10)})
        bpy.ops.object.mode_set(mode="OBJECT")
        
        # Assign the material object to the plane object using Blender's object material slot operators
        bpy.ops.object.material_slot_add()
        plane_object.material_slots[0].material = materials[i]
        
        planes.append(plane_object)
        
    # Join all the plane objects into one model object using Blender's object join operator
    bpy.ops.object.select_all(action="DESELECT")
    for plane in planes:
        plane.select_set(True)
    bpy.ops.object.join()
    model_object = bpy.context.active_object
    model_object.name = "model"
    
    # Set the origin of the model object to its center of mass using Blender's object origin set operator
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS")
    
    # Shade the model object smoothly using Blender's object shade smooth operator
    bpy.ops.object.shade_smooth()
    
    # Save the model object to a file in the output folder using Blender's libraries write operator
    if os.path.isdir(output_path):
        bpy.data.libraries.write(output_path + "/model.blend", {model_object})
        
except RuntimeError:
    print("Error: Cannot create models from masks and materials")

# Segment models using points or boxes as input prompts using Blender's operators module
try:
    # Get the active object in Blender's viewport as the model to be segmented
    model_object = bpy.context.active_object
    
    # Use Blender's operators module to select points or draw boxes on the model as input prompts for segmentation
    if model_type == "point":
        bpy.ops.view3d.select_point()
    elif model_type == "box":
        bpy.ops.view3d.draw_box()
    
    # Get the selected points or drawn boxes as numpy arrays
    points_or_boxes = np.array(bpy.context.selected_points_or_boxes)
    
    # Convert the model object to a numpy array of vertices and faces
    vertices = np.array([v.co for v in model_object.data.vertices])
    faces = np.array([f.vertices for f in model_object.data.polygons])
    
    # Use the Segment Anything model to segment different parts of the model based on points or boxes as input prompts
    masks, labels = segment_anything.segment(vertices, faces, session, model_type=model_type, points_or_boxes=points_or_boxes, threshold=threshold, confidence=confidence, num_classes=num_classes_per_prompt, num_samples=num_samples_per_prompt, num_iterations=num_iterations_per_prompt, num_proposals=num_proposals_per_prompt, num_refinements=num_refinements_per_prompt)
    
    # Create a list of materials for each mask and label pair
    materials = []
    for i in range(len(masks)):
         # Create a material object from the label and name it with the prefix "_material"
         material = bpy.data.materials.new(f"_material_{i}")
         material.use_nodes = True
        
         # Use a vertex color layer as the mask texture for the material
         nodes = material.node_tree.nodes
         links = material.node_tree.links
        
         # Get the principled BSDF node and set its base color to the label color
         principled_node = nodes.get("Principled BSDF")
         principled_node.inputs["Base Color"].default_value = labels[i]
        
         # Add a vertex color node and set its layer name to "mask"
         vertex_color_node = nodes.new("ShaderNodeVertexColor")
         vertex_color_node.layer_name = "mask"
        
         # Add a mix shader node and set its factor to 0.5
         mix_node = nodes.new("ShaderNodeMixShader")
         mix_node.inputs["Fac"].default_value = 0.5
        
         # Link the nodes together
         links.new(principled_node.outputs["BSDF"], mix_node.inputs[1])
         links.new(vertex_color_node.outputs["Color"], mix_node.inputs[2])
        
         # Set the material output node's input to the mix shader node's output
         output_node = nodes.get("Material Output")
         links.new(mix_node.outputs["Shader"], output_node.inputs["Surface"])
         
         materials.append(material)
         
     # Assign each material object to a different part of the model based on its mask value using Blender's bmesh module     
     bm = bmesh.new()
     bm.from_mesh(model_object.data)
     
     for i in range(len(masks)):
         for f in bm.faces:
             if masks[i][f.index] == 1:
                 f.material_index = i
     
     bm.to_mesh(model_object.data)     
     
     # Save each material object to a separate file in the output folder using Blender's libraries write operator     
     for i in range(len(materials)):
         if os.path.isdir(output_path):
             bpy.data.libraries.write(output_path + f"/_material_{i}.blend", {materials[i]})
             
except RuntimeError:
    print("Error: Cannot segment models using points or boxes")
