from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from multiprocessing import Queue
import os
import time
import multiprocessing as mp

cur_dir = "C:\\Work\Barclays\\Deploymnet_Multiprocessing\\val2017"

# load the model
model = VGG16()

def  func(cur_dir,queue):
	pred = []
	for root,dirs, files in os.walk(cur_dir):
		files = files[:20]
		for fil in files:
			#print(os.path.join(root,fil))
			#print(files)
			#load an image from file
			image = load_img(os.path.join(root,fil), target_size=(224, 224))
			# convert the image pixels to a numpy array
			image = img_to_array(image)
			# reshape data for the model
			image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
			# prepare the image for the VGG model
			image = preprocess_input(image)
			# predict the probability across all output classes
			yhat = model.predict(image)
			# convert the probabilities to class labels
			label = decode_predictions(yhat)
			# retrieve the most likely result, e.g. highest probability
			label = label[0][0]
			# print the classification
			#print('%s (%.2f%%)' % (label[1], label[2]*100))
			queue.put(label[1],label[2]*100)
			#pred.append([label[1],label[2]*100])

	#return pred


if __name__ == '__main__':
	#pool = mp.Pool(processes=4)
	q = Queue()
	#cur_dir = "C:\\Work\Barclays\\Deploymnet_Multiprocessing\\val2017"
	file_list = []
	cur_dir = "C:\\Work\Barclays\\Deploymnet_Multiprocessing\\val2017"
	for root, dirs, files in os.walk(cur_dir):
	    files = files[:3]
	    for f in files:
	        file_list.append(os.path.join(root,f))
	processes = [mp.Process(target=func,args=(os.path.join(cur_dir, f),q)) for f in file_list]

	for p in processes:
	    print(p)
	    p.start()

	# Exit the completed processes
	for p in processes:
	    p.join()

	# Get process results from the output queue
	results = [q.get() for p in processes]
	print(results)