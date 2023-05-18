#BlenderSAM: Segment Anything Addon for Blender

This addon allows you to use the Segment Anything Model (SAM) from Meta AI to segment objects in images and 3D models using input prompts such as points, boxes, or text. SAM is a promptable segmentation system with zero-shot generalization to unfamiliar objects and images, without the need for additional training. You can use this addon to generate masks and materials for all objects in an image, use them as references for 3D modeling, and segment different parts of a 3D model and apply different textures or materials to them.

## Table of Contents
- [Overview](#overview)
- [Update Log](#update-log)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Tips and Suggestions](#tips-and-suggestions)
- [Suggested Use Cases](#suggested-use-cases)

## Overview
BlenderSAM is an addon for Blender that integrates the Segment Anything Model (SAM) from Meta AI. SAM is a powerful and versatile open source segmentation model that can segment any object in an image or a 3D model using input prompts such as points, boxes, or text. SAM has been trained on a large dataset of 11 million images and 1.1 billion masks, and can segment objects that it has never seen before without any additional training. BlenderSAM allows you to use SAM within Blender to create masks and materials for all objects in an image, use them as references for 3D modeling, and segment different parts of a 3D model and apply different textures or materials to them.

[Back to top](#table-of-contents)

## Update Log
- Version 0.1 (May 2023): Initial release of BlenderSAM addon
- Version 1.0 (May 2023): Added Blender Python operators, utilities, and modules to simplify and optimize the pseudocode. Added options and parameters for fine-tuning and controlling the segmentation output. Added support for text-based segmentation

[Back to top](#table-of-contents)

## Features
- Segment all objects in an image automatically without any input prompts
- Segment specific objects in an image or a 3D model using points or boxes as input prompts
- Segment objects in an image or a 3D model using text as input prompts
- Generate masks and materials for each segmented object
- Save the masks and materials to the output folder
- Create models from masks and materials using Blender's mesh module
- Assign different materials to different parts of a model based on the segmentation masks
- Use options and parameters to fine-tune and control the segmentation output

[Back to top](#table-of-contents)

## Installation
To install BlenderSAM addon, follow these steps:

1. Download the latest version of BlenderSAM from this github repo.
2. Open Blender and go to Edit > Preferences > Add-ons.
3. Click on Install... and browse to the downloaded zip file.
4. Enable the addon by checking the box next to it.
5. Download the Segment Anything model checkpoint from this link: https://github.com/facebookresearch/segment-anything/releases/download/v1.0/sam.onnx
6. Save the model checkpoint to a folder of your choice.

[Back to top](#table-of-contents)

## Usage
To use BlenderSAM addon, follow these steps:

1. Load an image or a 3D model that you want to segment in Blender.
2. Go to the Properties panel > Object Data Properties > Custom Properties.
3. Set the image path, model path, model type, output path, threshold, confidence, num_classes, num_samples, num_iterations, num_proposals, num_refinements, num_samples_per_class, num_classes_per_prompt, num_samples_per_prompt, num_iterations_per_prompt, num_proposals_per_prompt, num_refinements_per_prompt according to your preferences.
4. Click on the Generate Masks button to generate masks and materials for all objects in the image automatically without any input prompts.
5. Click on the Create Models button to create models from masks and materials using Blender's mesh module.
6. Click on the Segment Models button to segment models using points or boxes as input prompts using Blender's operators module.

[Back to top](#table-of-contents)

## Tips and Suggestions
Here are some tips and suggestions for using BlenderSAM addon:

- Use high-resolution images or models for better segmentation results.
- Adjust the threshold and confidence values according to your needs. Higher values will result in fewer but more confident masks, while lower values will result in more but less confident masks.
- Adjust the num_classes value according to your needs. Higher values will result in more diverse classes of objects being segmented, while lower values will result in fewer but more general classes of objects being segmented.
- Adjust the num_samples value according to your needs. Higher values will result in more samples being used for text-based segmentation, while lower values will result in fewer but faster samples being used for text-based segmentation.
- Adjust the num_iterations value according to your needs. Higher values will result in more iterations being run for each input prompt, while lower values will result in fewer but faster iterations being run for each input prompt.
- Adjust the num_proposals value according to your needs. Higher values will result in more proposals being generated for each input prompt, while lower values will result in fewer but faster proposals being generated for each input prompt.
- Adjust the num_refinements value according to your needs. Higher values will result in more refinements being applied for each proposal, while lower values will result in fewer but faster refinements being applied for each proposal.
- Adjust the num_samples_per_class value according to your needs. Higher values will result in more samples being used for each class in automatic segmentation, while lower values will result in fewer but faster samples being used for each class in automatic segmentation.
- Adjust the num_classes_per_prompt value according to your needs. Higher values will result in more classes being segmented for each input prompt in manual segmentation, while lower values will result in fewer but more specific classes being segmented for each input prompt in manual segmentation.
- Adjust the num_samples_per_prompt value according to your needs. Higher values will result in more samples being used for each input prompt in manual segmentation, while lower values will result in fewer but faster samples being used for each input prompt in manual segmentation.
- Adjust the num_iterations_per_prompt value according to your needs. Higher values will result in more iterations being run for each input prompt in manual segmentation, while lower values will result in fewer but faster iterations being run for each input prompt in manual segmentation.
- Adjust the num_proposals_per_prompt value according to your needs. Higher values will result in more proposals being generated for each input prompt in manual segmentation, while lower values will result in fewer but faster proposals being generated for each input prompt in manual segmentation.
- Adjust the num_refinements_per_prompt value according to your needs. Higher values will result in more refinements being applied for each proposal in manual segmentation, while lower values will result in fewer but faster refinements being applied for each proposal in manual segmentation.

[Back to top](#table-of-contents)

## Suggested Use Cases
Here are some suggested use cases for using BlenderSAM addon:

- Use it as a reference tool for creating realistic 3D models from images by generating masks and materials for all objects in an image and creating models from them using Blender's mesh module.
- Use it as a creative tool for modifying existing 3D models by segmenting different parts of them using points or boxes as input prompts and applying different textures or materials to them using Blender's bmesh module.
- Use it as a learning tool for exploring different objects and classes by segmenting them using text as input prompts and seeing how they are represented by masks and materials.

[Back to top](#table-of-contents)
