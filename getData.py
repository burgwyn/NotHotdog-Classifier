import urllib
import urllib.request
from cv2 import imread, imwrite
import os
from numpy import bitwise_xor
from multiprocessing.dummy import Pool as ThreadPool 
import itertools

pic_num = 1

def store_raw_images(paths, links):
    global pic_num
    for link, path in zip(links, paths):
        if not os.path.exists(path):
            os.makedirs(path)
        image_urls = str(urllib.request.urlopen(link).read())
        
        pool = ThreadPool(32)
        pool.starmap(load_image, zip(itertools.repeat(path),image_urls.split('\\n'),itertools.count(pic_num))) 
        pool.close() 
        pool.join()
                    
def load_image(path,link, counter):
    global pic_num
    if pic_num < counter:
        pic_num = counter+1
    try:                
        urllib.request.urlretrieve(link, path+"/"+str(counter)+".jpg")
        img = imread(path+"/"+str(counter)+".jpg")             
        if img is not None:
            imwrite(path+"/"+str(counter)+".jpg",img)
            print(counter)

    except Exception as e:
        print(str(e))  
    
def remove_invalid(dir_paths):
    for dir_path in dir_paths:
        for img in os.listdir(dir_path):
            for invalid in os.listdir('invalid'):
                try:
                    current_image_path = str(dir_path)+'/'+str(img)
                    invalid = imread('invalid/'+str(invalid))
                    question = imread(current_image_path)
                    if invalid.shape == question.shape and not(bitwise_xor(invalid,question).any()):
                        os.remove(current_image_path)
                        break

                except Exception as e:
                    print(str(e))
  
def main():
    links = [ 
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n01318894', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03405725', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00021265', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07690019', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07865105', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07697537' ]
    
    paths = ['pets', 'furniture', 'people', 'food', 'frankfurter', 'chili-dog', 'hotdog']
    
    
    store_raw_images(paths, links)
    remove_invalid(paths)


if __name__ == "__main__":

    main()
