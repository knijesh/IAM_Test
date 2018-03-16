
import os,random
import numpy as np    
import PIL  
import shutil
import cv2

def crop_image(image,dest,percent,pos):    
    import os,random
    img = cv2.imread(image)
    #cv2.imshow('image',img)
    #print(img.shape)
    rand_range = img.shape[1]
    percent = int(rand_range - img.shape[1]*percent/100)
    if pos:
        cropped = img[0:img.shape[0],percent:img.shape[1]]
    else:
        cropped = img[0:img.shape[0],0:percent]
        
    #cv2.imshow("cropped", cropped)
    cv2.imwrite(dest, cropped)
    cv2.waitKey(0)


def concatenate_images(image_list,output_path):
    import numpy as np    
    import PIL
    list_im = image_list
    imgs= [ PIL.Image.open(i) for i in list_im ]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    # save that beautiful picture
    imgs_comb = PIL.Image.fromarray(imgs_comb)
    imgs_comb.save(output_path) 


def delete_contents(path):
    folder = path
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)            
        except Exception as e:
            print(e)


def neg_sampcreate(image1,image2,dest):
    import numpy as np
    import shutil
    val = random.randint(20,50)
    #print(val)
    base_path = r"C:\Work\Barclays\PPI"
    try:
        temp_dest = os.path.join(base_path,'temp')
        if not os.path.exists(temp_dest):
            os.makedirs(temp_dest)
        dest1 =os.path.join(temp_dest,'dest.png')
        dest2 =os.path.join(temp_dest,'dest2.png')
        #print(dest1,dest2)
        #print(image1)
        crop_image(image1,dest1,val,True)
        #print(image2)
        crop_image(image2,dest2,val,False)
        d1 = cv2.imread(dest1)
        d2 = cv2.imread(dest2)
        concatenate_images(image_list=[dest1,dest2],output_path=dest)
        delete_contents(temp_dest)
    except Exception as e:
        shutil.rmtree(temp_dest)


def create_all_possible_pairs(lists):
    result = []
    for p1 in range(len(lists)):
            for p2 in range(p1+1,len(lists)):
                    result.append([lists[p1],lists[p2]])
    return result


if __name__ == '__main__':
    
    source = r"C:\Work\Barclays\PPI\IAM_Cleaned_DB_A2Z_to_be_shared"
    destination = os.path.abspath(r"C:\Work\Barclays\PPI\N_n_2")
    #print(destination)
    if not os.path.exists(destination):
        os.mkdir(destination)
    number_list = os.listdir(source)
    pairs = create_all_possible_pairs(number_list)
    # l =[]
    for each  in pairs:
        dir1,dir2 = os.path.join(source,each[0]),os.path.join(source,each[1])
        len_dir1,len_dir2 = len(os.listdir(dir1)),len(os.listdir(dir2))
        if len_dir1<=len_dir2:
            target = len_dir1
        else:
            target = len_dir2
        fil1,fil2 = zip(*random.sample(list(zip(os.listdir(dir1), os.listdir(dir2))),target))
        final_comp_list = list(zip(fil1,fil2))
        for img in final_comp_list:
            image1 = os.path.join(dir1,img[0])
            image2 = os.path.join(dir2,img[1])
            filename = str(image1.split(os.sep)[-1])+"_"+str(image2.split(os.sep)[-1])
            out_dest= os.path.join(destination,filename)
            #l.append(os.path.join(destination,filename))
            #print(image1,image2)
            #print(os.path.exists(os.path.join(dir1,image1)),os.path.exists(os.path.join(dir2,image2)))       
            neg_sampcreate(image1,image2,out_dest)
     
