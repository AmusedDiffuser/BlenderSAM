# Import the Segment Anything model and the Blender API
import segment_anything
import bpy

# Import numpy for array manipulation
import numpy as np

# Import mathutils for matrix operations
import mathutils

# Define a function to load an image and generate masks for all objects in it
def generate_masks(image_path):
    """
    This function loads an image from a given path and generates masks for all objects in it using the Segment Anything model.
    Parameters:
        image_path (str): The path to the image file.
    Returns:
        masks (list): A list of dictionaries containing mask data, label, score, width, height, x, and y for each object in the image.
        materials (list): A list of Blender material objects corresponding to each mask.
    """

    # Try to load the image and create a new image object in Blender
    try:
        image = bpy.data.images.load(image_path)
        image.name = "SAM_input"
    except RuntimeError as e:
        # Handle the error if the image cannot be loaded
        print(f"Error: {e}")
        return None, None

    # Convert the image to RGB mode if it is not already
    if image.colorspace_settings.name != "sRGB":
        image.colorspace_settings.name = "sRGB"

    # Convert the Blender image object to a numpy array
    image_array = np.array(image.pixels).reshape(image.size[1], image.size[0], 4)[:, :, :3]

    # Reshape the numpy array to have a shape of (height, width, 3) and a dtype of np.uint8
    image_array = np.uint8(image_array * 255).transpose((1, 0, 2))

    # Rotate and resize the numpy array to match the original image orientation and aspect ratio
    # Get the rotation angle and scale factor from the image metadata
    rotation = math.radians(image.metadata.get("Orientation", 0))
    scale = image.metadata.get("Scale", 1)

    # Create a rotation matrix from the angle
    rotation_matrix = mathutils.Matrix.Rotation(rotation, 2)

    # Apply the rotation and scale to the numpy array
    image_array = np.array(
        [
            [rotation_matrix @ mathutils.Vector((x * scale, y * scale)) for x in row]
            for y, row in enumerate(image_array)
        ]
    )

    # Load the SAM model and create a mask generator object
    sam = segment_anything.sam_model_registry["<model_type>"](
        checkpoint="<path/to/checkpoint>"
    )
    mask_generator = segment_anything.SamAutomaticMaskGenerator(sam)

    # Generate masks for all objects in the image
    masks = mask_generator.generate(image_array)

    # Create an empty list to store the materials
    materials = []

    # For each mask, create a new image object in Blender and assign it to a new material
    for mask in masks:
        # Check if the mask score is above a threshold value (such as 0.5)
        if mask["score"] > 0.5:
            # Create a new image object from the mask data and name it with the object label
            mask_image = bpy.data.images.new(
                name=mask["label"], width=mask["width"], height=mask["height"]
            )
            mask_image.pixels = mask["data"]

            # Create a new material and assign the mask image as its alpha texture
            material = bpy.data.materials.new(name=mask["label"])
            material.use_nodes = True
            nodes = material.node_tree.nodes
            links = material.node_tree.links

            # Add an image texture node and set its image to the mask image
            texture_node = nodes.new(type="ShaderNodeTexImage")
            texture_node.image = mask_image

            # Add a principled BSDF node and set its base color to a random color
            bsdf_node = nodes.get("Principled BSDF")
            bsdf_node.inputs["Base Color"].default_value = [
                random.random() for _ in range(3)
            ] + [1.0]

            # Link the alpha output of the texture node to the alpha input of the bsdf node
            links.new(texture_node.outputs["Alpha"], bsdf_node.inputs["Alpha"])

            # Append the material to the list of materials
            materials.append(material)

    # Return the list of masks and materials
    return masks, materials


# Define a function to use the masks and materials as references for 3D modeling
def model_from_masks(masks, materials):
    """
    This function uses the masks and materials as references for 3D modeling by creating plane objects with extruded depth for each mask and material pair.
    Parameters:
        masks (list): A list of dictionaries containing mask data, label, score, width, height, x, and y for each object in the image.
        materials (list): A list of Blender material objects corresponding to each mask.
    Returns:
        None
    """

    # For each mask and material, create a new plane object in Blender and assign the material to it
    for mask, material in zip(masks, materials):
        # Create a new plane object and name it with the object label as a suffix
        bpy.ops.mesh.primitive_plane_add()
        plane = bpy.context.object
        plane.name = f"plane_{mask['label']}"

        # Scale and position the plane to match the mask bounding box
        plane.scale = (mask["width"] / 2, mask["height"] / 2, 1)

        # Subtract the x and y values from the plane location to align it with the original image
        plane.location = (
            plane.location.x - mask["x"],
            plane.location.y - mask["y"],
            plane.location.z,
        )

        # Assign the material to the plane using its label as a prefix
        plane.data.materials.append(material)
        plane.material_slots[0].name = f"{mask['label']}_material"

        # Extrude the plane along the normal axis to create some depth
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, random.uniform(0.1, 1))}
        )
        bpy.ops.object.mode_set(mode="OBJECT")


# Define a function to segment different parts of a 3D model and apply different textures or materials to them
def segment_model(model):
    """
    This function segments different parts of a 3D model and applies different textures or materials to them using the Segment Anything model.
    Parameters:
        model (Blender object): A Blender object representing a 3D model.
    Returns:
        None
    """

    # Convert the model to a mesh object if it is not already one
    if model.type != "MESH":
        bpy.ops.object.convert(target="MESH")

    # Load the SAM model and create a predictor object
    sam = segment_anything.sam_model_registry["<model_type>"](
        checkpoint="<path/to/checkpoint>"
    )
    predictor = segment_anything.SamPredictor(sam)

    # Set the model as the input image for the predictor
    predictor.set_image(model)

    # For each part of the model, create an input prompt (such as a point or a box) and get the corresponding mask from the predictor
    for part in model.parts:
        # Create an input prompt for the part using Blender's UI elements (this could be done by user interaction or some other method)
        input_prompt = create_input_prompt(part)

        # Get the mask, label, and score from the predictor
        mask, label, score = predictor.predict(input_prompt)

        # Check if the mask score is above a threshold value (such as 0.5)
        if mask["score"] > 0.5:
            # Create a new material and assign it to the part based on the mask and label (this could be done by user selection or some other method)
            material = create_material(mask, label)

            # Assign the material to the part using its label as a prefix 
            part.data.materials.append(material)
            part.material_slots[0].name = f"{label}_material"


# Define a helper function to create an input prompt for a given part of a 3D model using Blender's UI elements 
def create_input_prompt(part):
   """
   This function creates an input prompt for a given part of a 3D model using Blender's UI elements.
   Parameters:
       part (Blender object): A Blender object representing a part of a 3D model.
   Returns:
       input_prompt (dict): A dictionary containing type ("point" or "box") and coordinates of input prompt.
   """

   # The logic for creating an input prompt goes here 
   pass


# Define a helper function to create a new material based on given mask and label 
def create_material(mask,label):
   """
   This function creates a new material based on given mask and label.
   Parameters:
       mask (dict): A dictionary containing mask data.
       label (str): A string containing object label.
   Returns:
       material (Blender material): A Blender material object with given properties.
   """

   # The logic for creating a new material goes here 
   pass


# Example usage: load an image, generate masks and materials,
# use them as references for 3D modeling,
# and and segment one of the models
Create a panel to display the input image and allow the user to draw points or boxes on it
class SAM_PT_panel(bpy.types.Panel): “”" This class defines a panel to display the input image and allow the user to draw points or boxes on it. “”"

# Set the panel properties
bl_label = "Segment Anything"
bl_idname = "SAM_PT_panel"
bl_space_type = "VIEW_3D"
bl_region_type = "UI"
bl_category = "SAM"

# Define the panel layout
def draw(self, context):
    layout = self.layout

    # Add a file browser operator to select an image file
    layout.operator("image.open")

    # Add a label to show the selected image path
    layout.label(text=context.space_data.params.filename)

    # Add a button to generate masks and materials for the selected image
    layout.operator("sam.generate_masks")

    # Add a button to create models from the generated masks and materials
    layout.operator("sam.model_from_masks")

    # Add a label to show the selected model name
    layout.label(text=context.object.name)

    # Add a button to segment the selected model using points or boxes
    layout.operator("sam.segment_model")
Copy
Create an operator to generate masks and materials for the selected image
class SAM_OT_generate_masks(bpy.types.Operator): “”" This class defines an operator to generate masks and materials for the selected image using the Segment Anything model. “”"

# Set the operator properties
bl_idname = "sam.generate_masks"
bl_label = "Generate Masks"

# Define the operator execution
def execute(self, context):
    # Get the selected image path from Blender's context 
    image_path = context.space_data.params.filename

    # Check if an image path is selected or not 
    assert image_path != "", "No image path selected"

    # Print a message to inform the user that masks are being generated 
    print(f"Generating masks for {image_path}...")

    # Load an image and generate masks and materials
    masks, materials = generate_masks(image_path)

    # Check if masks and materials are not None (meaning no error occurred)
    assert masks is not None and materials is not None, "Failed to generate masks or materials"

    # Print a message to inform the user that masks are generated 
    print(f"Generated {len(masks)} masks.")

    return {"FINISHED"}
Copy
Create an operator to create models from the generated masks and materials
class SAM_OT_model_from_masks(bpy.types.Operator): “”" This class defines an operator to create models from the generated masks and materials using them as references for 3D modeling. “”"

# Set the operator properties
bl_idname = "sam.model_from_masks"
bl_label = "Create Models"

# Define the operator execution
def execute(self, context):
    # Get the generated masks and materials from Blender's data 
    masks = [image for image in bpy.data.images if image.name.startswith("SAM_input")]
    materials = [material for material in bpy.data.materials if material.name.startswith("SAM_input")]

    # Check if masks and materials are not empty or None 
    assert masks and materials, "No masks or materials found"

    # Print a message to inform the user that models are being created 
    print(f"Creating models from masks...")

    # Use the masks and materials as references for 3D modeling
    model_from_masks(masks, materials)

    # Print a message to inform the user that models are created 
    print(f"Created {len(masks)} models.")

    return {"FINISHED"}
Copy
Create an operator to segment the selected model using points or boxes
class SAM_OT_segment_model(bpy.types.Operator): “”" This class defines an operator to segment the selected model using points or boxes as input prompts for the Segment Anything model. “”"

# Set the operator properties
bl_idname = "sam.segment_model"
bl_label = "Segment Model"

# Define the operator execution
def execute(self, context):
     # Get the selected model from Blender's context 
     model = context.object

     # Check if a model is selected or not 
     assert model is not None, "No model selected"

     # Print a message to inform the user that parts are being segmented 
     print(f"Segmenting parts of {model.name}...")

     # Segment one of the models (for example, the first one) and apply different textures or materials to its parts
     segment_model(model)

     # Print a message to inform the user that process is done 
     print("Done!")

     return {"FINISHED"}
Copy
Register all classes defined above
classes = [SAM_PT_panel, SAM_OT_generate_masks, SAM_OT_model_from_masks, SAM_OT_segment_model]

def register(): for cls in classes: bpy.utils.register_class(cls)

def unregister(): for cls in classes: bpy.utils.unregister_class(cls)

if name == “main”: register()
