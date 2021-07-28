import cv2
import numpy as np
import os

def get_next_dir(paths,if_only_dir=True):
    # 传入一个当前的列表，获取下一级目录的所有文件夹列表
    # 默认只获得目录不获得文件
    path_list = []
    for path in paths:
        for next_dir_path in os.listdir(path):
            next_dir_path = path+'/'+next_dir_path
            if if_only_dir:
                if os.path.isdir(next_dir_path) == True:
                    path_list.append(next_dir_path)
            else:
                path_list.append(next_dir_path)
    return path_list


def get_aspect_ratio(img):  # 用于找到长宽比
    imgSize = img.shape
    aspect_ratio = imgSize[1]/imgSize[0]  # 6000/4000
    return aspect_ratio


def cut_img(img_list,output_path):
    for i, img_path in enumerate(img_list):
        print('{}   {}'.format(i,img_path))
        save_path = output_path + '/' + img_path.split('/')[-1]
        print('save to :{}'.format(save_path))
        # cv2.imwrite('save_path', img)

        img = cv2.imread(img_path)
        aspect_ratio = get_aspect_ratio(img)  # 长宽比
        height, width = img.shape[0:2]
        print(aspect_ratio)
        if aspect_ratio == 1.5:
            img_resize_out = cv2.resize(img, (0, 0), fx=864/width, fy=576/height, interpolation=cv2.INTER_NEAREST)
        elif aspect_ratio < 1.5:  # 也是就是这个图像更方，需要在左右填东西
            img_resize = cv2.resize(img, (0, 0), fx=576/height, fy=576/height, interpolation=cv2.INTER_NEAREST)
            img_size_new = img_resize.shape
            img_background = np.zeros((576, 864, 3), np.uint8)
            img_background[0:576, int((864-img_size_new[1])/2):int((864-img_size_new[1])/2)+img_size_new[1]] = img_resize
            img_resize_out = img_background
        else:  # 这玩意基本没有吧
            img_resize = cv2.resize(img, (0, 0), fx=864/width, fy=864/width, interpolation=cv2.INTER_NEAREST)
            img_size_new = img_resize.shape
            img_background = np.zeros((576, 864, 3), np.uint8)
            img_background[ int((576 - img_size_new[0]) / 2):int((576 - img_size_new[0]) / 2) + img_size_new[0], 0:864] = img_resize
            img_resize_out = img_background

        # cv2.imshow('resize0', img_resize_out)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        cv2.imwrite(save_path,img_resize_out)

if __name__ == '__main__':
        input_path = 'data/input'
        output_path = 'data/output'
        img_list = get_next_dir([input_path], False)   # 同样能获得长和宽
        print(img_list)
        cut_img(img_list, output_path)

