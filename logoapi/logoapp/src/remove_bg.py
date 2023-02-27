import cv2
import numpy as np


def remove_background(input_path, output_path):
    print(f"input: {input_path}, output: {output_path}")
   
    # 이미지 불러오기
    img = cv2.imread(input_path)
    if input_path.endswith('png'): #convert to jpg
        print("Convert .png to .jpg")
        img=cv2.imread(input_path,cv2.IMREAD_UNCHANGED)
        trans_mask =img[:,:,3]==0 # 투명한 부분이 mask가 됨
        img[trans_mask]=[255,255,255,255]
        
        # jpg_path = input_path.split('/')[0]+'.jpg'
        # cv2.imwrite(jpg_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        # img = cv2.imread(jpg_path)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 임계값 조절
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    # mask
    mask = 255 - mask

    # morphology 적용
    # borderconstant 사용
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask
    # blur alpha channel
    #mask = cv2.GaussianBlur(mask, (0,0), sigmaX=1, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # 저장
    cv2.imwrite(output_path, result)



if __name__ == '__main__':
    import sys
    ori_path, new_path = sys.argv[1], sys.argv[2]
    images =remove_background(ori_path,new_path)