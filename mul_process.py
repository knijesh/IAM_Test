import multiprocessing as mp
import os
#import multiprocessing
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from multiprocessing import Queue

# load the model
model = VGG16()
  

def image_class_pred(cur_dir):	
	pred ={}
	for root,dirs, files in os.walk(cur_dir):
		files = files[:2]
		for fil in files:
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
		    #queue.put(label[1],label[2]*100)
		    #print(label[1],label[2]*100)
		    pred[label[1]]=label[2]*100
		    #print('%s (%.2f%%)' % (label[1], label[2]*100))
	return pred

if __name__ == '__main__':
	import time
	start = time.time()
	pool = mp.Pool(processes=4)
	cur_dir = "C:\\Work\Barclays\\Deploymnet_Multiprocessing\\val2017"
	#results = [pool.apply(cube, args=(x,)) for x in range(1,7)]
	results = pool.map_async(image_class_pred,cur_dir)
	pool.close()
	pool.join()
	print(results)
	print(time.time()-start)



#9394952207