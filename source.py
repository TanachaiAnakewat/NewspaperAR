import cv2

method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
small_image = cv2.imread('newspaper_template.jpg')
large_image = cv2.imread('newspaper.jpg')
highlight = cv2.VideoCapture('highlight.mp4')
height = int(highlight.get(cv2.CAP_PROP_FRAME_HEIGHT)) #1280
width = int(highlight.get(cv2.CAP_PROP_FRAME_WIDTH)) #720


result = cv2.matchTemplate(small_image, large_image, method)

# We want the minimum squared difference
mn,_,mnLoc,_ = cv2.minMaxLoc(result)

# Draw the rectangle:
# Extract the coordinates of our best match
MPx,MPy = mnLoc

# Step 2: Get the size of the template. This is the same size as the match.
trows,tcols = small_image.shape[:2] #(262, 294)
ratio = tcols/trows

# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

# # Display the original image with the rectangle around the match.
#cv2.imshow('output',large_image)
# cv2.imwrite('result.png', img_rgb)
# # The image is only displayed if we call this
cv2.waitKey(0)

cv2.imshow('frame',large_image)

while(True):
    # Capture frame-by-frame
    ret, frame = highlight.read()
    #topleft = (height-trows)//2

    #crop video
    if width/height == ratio:
        if width != tcols:
            frame = cv2.resize(frame,(tcols,trows))
        else:
            frame = frame
    elif width/height > ratio:
        offset  = int(abs(width-ratio*height)/2)
        frame = frame[0:height,offset:width-offset]
        frame = cv2.resize(frame,(tcols,trows))
    else:
        offset  = int(abs((width/ratio)-height)/2)
        frame = frame[ offset:height-offset, 0:width]
        print(width/offset, ratio)
        frame = cv2.resize(frame,(tcols,trows))
        
    #frame = frame[int((height-trows)//2):int((height+trows)//2) , int((width-tcols)//2):int((width+tcols)//2)]
    # add image to frame
    large_image[MPy:MPy+trows , MPx:MPx+tcols ] = frame

    # Display the resulting frame
    cv2.imshow('frame',large_image)

    # Exit if ESC key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

# When everything done, release the capture
highlight.release()
cv2.destroyAllWindows()
