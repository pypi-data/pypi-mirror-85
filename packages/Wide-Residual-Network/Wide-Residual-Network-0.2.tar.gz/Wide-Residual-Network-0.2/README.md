This package is for creating a wide residual convolutional neural network with keras and tensorflow as backend.

This architecture was first introduced in the paper on https://arxiv.org/abs/1605.07146 .

For istallation: TODO

Please first install tensorflow in order to be able to use this package.

When you've installed the package, you can import it with:

	1: from wideresnet import WideResNet

Example code for creating a model:
	
	1: wideresnet_obj = WideResNet(input_shape = (224, 224, 3), k = 2, num_layers = 22, num_classes = 4)
	2: model = wideresnet_obj.create_model()