# DnnLab
Dnnlab is a small framework for deep learning models based on TensorFlow.



It provides custom training loops for:
* Generative Models (GAN, cGan, cycleGAN)
* Image Detection (custom YOLO)


Additonaly custom Keras Layer:
* Non-Local-Blocks (Self-Attention)
* Squeeze and Excitation Blocks (SEBlocks)
* YOLO-Decoding Layer

Input pipeline functionality:
* YOLO (Tfrecords to Datasets)
* YOLO data augmentation
* Generative Models (Tfrecords to Datasets)

TensorBoard output:
* YOLO coco metrics (Precision (mAP) & Recall)
* YOLO loss (loss_class, loss_conf, loss_xywh, total_loss)
* YOLO bounding boxes
* Generative Models (Loss & Images)


## Requirements
TensorFlow 2.3.0

## Installation
Run the following to install:
```python
pip install dnnlab
```







