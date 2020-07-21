# 3DImageProcessing
Tool that can transform a 2D image or video into 3D Meshes with Depth.<br>
Targeting all device include mobiles

## Auto Encoder Architecture<br>
Encoder<br>
Barebone MobileNetV2<br>
- In order to run smoothly on mobile device, I have decrease the learnable parameter into bare minimum requirement, half the parameters if compare with official MobileNetV2.<br>

Decoder<br>
Reverse of Encoder + Unet structure<br>
- Unet is the key for auto encoder to actually learn something, without it, nothing work

Architecture<br>


<br>
Data source<br>
1.DIML https://dimlrgbd.github.io/<br>
2.TAU http://www.cs.toronto.edu/~harel/TAUAgent/home.html<br>
3. Some other street, human pose depth images<br>

## Unity Barracuda
* Use tensorflow-onnx to export onnx file
* Implement Unity Barracuda to read onnx file, and asynchronous run it on corountine. (No available with threading)

## Unity Compute Shader / Geometry Shader
* Read generated depth texture and store the depth position, pixl value into ComputeBuffer
* Pass down the ComputeBuffer to Vert/Geometry/Frag Shader, and draw meshes there, or else it look just like point cloud.
