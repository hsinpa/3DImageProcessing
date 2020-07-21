# 3DImageProcessing
Tool that can transform a 2D image or video into 3D Meshes with Depth.<br>
Targeting all device include mobiles

## Auto Encoder Architecture<br>
Encoder<br>
Barebone MobileNetV2<br>
- In order to run smoothly on mobile device, I have decrease the learnable parameter into bare minimum requirement, half the parameters if compare with official MobileNetV2.
- 

Decoder
Reverse of Encoder + Unet structure<br>
- Unet is the key for auto encoder to actually learn something, without it, nothing work
<br>
Data source<br>
1.DIML https://dimlrgbd.github.io/<br>
2.

## Unity Barracuda
Use tensorflow-onnx to export onnx file


## Unity Compute Shader / Geometry Shader
