# BlenderSAM: Segment Anything Model Addon for Blender

This addon allows you to use the Segment Anything Model (SAM) from Meta AI to segment objects in images and 3D models using input prompts such as points or boxes. SAM is a promptable segmentation system with zero-shot generalization to unfamiliar objects and images, without the need for additional training. You can use this addon to generate masks and materials for all objects in an image, use them as references for 3D modeling, and segment different parts of a 3D model and apply different textures or materials to them.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Generating Masks and Materials](#generating-masks-and-materials)
  - [Creating Models from Masks](#creating-models-from-masks)
  - [Segmenting Models](#segmenting-models)
- [Tips and Suggestions](#tips-and-suggestions)
- [Suggested Use Cases](#suggested-use-cases)

## Installation

To install this addon, you need to have Blender 3.5 or higher, as well as Python 3.8 or higher. You also need to install the following dependencies:

- PyTorch 1.7 or higher
- TorchVision 0.8 or higher
- Segment Anything
- Numpy
- Mathutils
- OpenCV
- Pycocotools
- Matplotlib
- Onnxruntime
- Onnx

You can install these dependencies using pip or conda. For example using the command:
```
pip install torch torchvision segment_anything numpy mathutils opencv-python pycocotools matplotlib onnxruntime onnx
```

To install this addon in Blender, you need to download or clone this repository and copy the segment_anything_addon folder to your Blender addons directory (usually located at C:\Users\<username>\AppData\Roaming\Blender Foundation\Blender\<version>\scripts\addons on Windows or ~/.config/blender/<version>/scripts/addons on Linux). Alternatively, you can use Blender’s Install Add-on from File option in the Preferences menu and select the segment_anything_addon.zip file.

After installing the addon, you need to enable it in Blender’s Preferences menu under the Add-ons tab. You should see a new category called SAM with the Segment Anything Addon listed. Check the box next to it to enable it.

You also need to download a model checkpoint for the Segment Anything model from here and save it to a location of your choice. You will need to specify the path to this checkpoint when using the addon.

[Back to top](#table-of-contents)

## Usage

This addon provides a panel in the 3D Viewport’s UI region with buttons and labels for using the Segment Anything model. You can use this panel to load an image, generate masks and materials, create models from masks, and segment models using points or boxes.

### Generating Masks and Materials

To generate masks and materials for all objects in an image, follow these steps:

1. Click on the Open Image button in the SAM panel. This will open a file browser where you can select an image file of your choice.
2. After selecting an image file, click on the Generate Masks button in the SAM panel. This will load the image and use the Segment Anything model to generate masks and materials for all objects in it. You will see a message in the console informing you of the progress and results.
3. After generating masks and materials, you will see a list of images and materials in Blender’s data with names starting with “SAM_input”. Each image represents a mask for an object in the original image, and each material uses that mask as its alpha texture.



### Creating Models from Masks

To create models from masks and materials, follow these steps:

1. After generating masks and materials, click on the Create Models button in the SAM panel. This will use the masks and materials as references for 3D modeling by creating plane objects with extruded depth for each mask and material pair. You will see a message in the console informing you of the progress and results.
2. After creating models from masks, you will see a list of plane objects and materials in Blender’s data with names starting with “plane_” and “_material” respectively. Each plane object represents a model for an object in the original image, and each material uses its corresponding mask as its alpha texture.



### Segmenting Models

To segment different parts of a 3D model and apply different textures or materials to them, follow these steps:

1. After creating models from masks, select one of them in Blender’s viewport. You can use Blender’s object selection operator or click on the model name label in the SAM panel.
2. After selecting a model, click on the Segment Model button in the SAM panel. This will use the Segment Anything model to segment different parts of the model using input prompts such as points or boxes. You will see a message in the console informing you of the progress and results.
3. After segmenting the model, you will see a list of materials in Blender’s data with names starting with “_material”. Each material represents a texture or material for a part of the model based on its mask and label.

[Back to top](#table-of-contents)

## Tips and Suggestions

Here are some tips and suggestions for using this addon effectively:

- The quality and speed of segmentation depend on several factors such as image size, resolution, complexity, contrast, lighting, etc. You may need to adjust these factors or try different images to get better results.
- The Segment Anything model can segment objects based on different types of input prompts such as points or boxes. You can choose which type of input prompt you want to use by changing the <model_type> parameter when loading the model checkpoint. For example, if you want to use points as input prompts, you can use sam_model_registry["point"] instead of sam_model_registry["<model_type>"].
- The Segment Anything model can also segment objects based on text prompts such as object names or descriptions. However, this feature is not currently supported by this addon. If you want to use text prompts, you can refer to [this notebook](https://github.com/facebookresearch/segment-anything/blob/main/notebooks/SAM_Text_Prompts.ipynb) for an example of how to do it.
- The Segment Anything model can generate masks for all objects in an image automatically without any input prompts. However, this feature is not currently supported by this addon either. If you want to use automatic segmentation, you can refer to [this notebook](https://github.com/facebookresearch/segment-anything/blob/main/notebooks/SAM_Automatic_Segmentation.ipynb
) for an example of how to do it.
- The Segment Anything model can segment objects that are not visible or occluded by other objects using inpainting techniques. However, this feature is also not currently supported by this addon. If you want to use inpainting segmentation, you can refer to [this notebook](https://github.com/facebookresearch/segment-anything/blob/main/notebooks/SAM_Inpainting_Segmentation.ipynb) for an example of how to do it.

[Back to top](#table-of-contents)

## Suggested Use Cases

Here are some suggested use cases for this addon:

- You can use this addon to create realistic 3D models from images without having to manually trace or sculpt them.
- You can use this addon to edit or modify existing 3D models by changing their textures or materials based on different input prompts.
- You can use this addon to create custom assets or scenes for animation or game development by combining different models from images or other sources.
- You can use this addon to experiment with different segmentation tasks and challenges using your own images or models.

[Back to top](#table-of-contents)
