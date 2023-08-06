from PIL import Image, ImageSequence
import cv2
import numpy
from PIL import Image, ImageSequence

#checks whether a gif contains flashing or high saturation frames
def process_gif(gif_path):

    #exacts staturation and luminace from a frame
    def process_frame(frame):
        dst = frame.convert("RGB")
        avg_color_per_row = numpy.average(dst, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
        distance = (256-avg_color[0])**2 + avg_color[1]**2 + avg_color[2]**2
        
        #from http://en.wikipedia.org/wiki/Luminance_(relative)
        relLuminance = 0.2126*avg_color[0] + 0.7152*avg_color[1] + 0.0722*avg_color[2]
        
        return distance, relLuminance
    
    # determines if more than the 'theshold' of frames are saturated
    def check_saturation(saturated_count, unsaturated_count, threshold=0.25):
        return saturated_count/(saturated_count + unsaturated_count) >= threshold
    
    #checks is more than 'theshold' of frames contains flashing
    def check_flashing(luminance_list, total_frames, threshold=0.25):

        luminanceChanges = [luminance_list[i+1]-luminance_list[i] for i in range(len(luminance_list)-1)]
        avgLuminanceChange = sum(luminanceChanges) / len(luminanceChanges)
        numFlashes = 0
        for change in luminanceChanges:
            if change >= 2*avgLuminanceChange:
                numFlashes += 1
        
        return numFlashes >= threshold * total_frames
    
    # initialize variables
    numSaturated = 0
    numUnsaturated = 0
    luminances = []
    isSaturated = False
    isFlashing = False

    img = Image.open(gif_path)

    for i, frame in enumerate(ImageSequence.Iterator(img)):
        distance, relLuminance = process_frame(frame)

        # update numSaturated, numUnsaturated, and luminances
        if distance <= 20:
            numSaturated+=1
        else:
            numUnsaturated+=1
        luminances.append(relLuminance)

    isSaturated = check_saturation(numSaturated, numUnsaturated)

    numFrames = numSaturated + numUnsaturated #clean up later
    isFlashing = check_flashing(luminances, numFrames)

    return isFlashing, isSaturated
