import cv2 
import numpy as np 
from astropy.io import fits 
import matplotlib.pyplot as plt 


def shape_increase(data, factor, fac=1):
    """
    Increases the boundary of the mask by one pixel. i.e., adds one layer of pixels around the mask present in the data
    passed in.

    Parameters
    --------------
    data:
        Array with the original shape that we wish to expand
    factor:
        number of pixels that we wish to increase
    fac:
        Used internally

    Returns
    -------
        numpy array:
            Increased image
    Notes
    -----

        This is a recursive function to expand by a number of pixels (factor) our image inside the data array.
        This function muss be refactored since it's inefficient. However, for the time being, the overhead that it introduces
        is not enough to justify optimizing it.
    """
    # ToDO: refactor this. IN other words: prettify this
    if factor < 1:
        return data

    positions = np.where(data != 0)  # array positions that we wish to increase

    new = np.zeros(data.shape)

    cases = [[0, 0], [0, 1], [1, 0], [1, 1], [0, -1], [-1, 0], [-1, -1], [1, -1], [-1, 1]]

    max_pos = data.shape[0]
    for pos in zip(positions[0], positions[1]):

        for j in cases:

            val_x = j[0]
            val_y = j[1]

            if pos[0] + val_x < 0:
                val_x = -pos[0]
            elif pos[0] + val_x >= max_pos:
                val_x = max_pos - pos[0] - 1

            if pos[1] + val_y < 0:
                val_y = -pos[1]

            elif pos[1] + val_y >= max_pos:
                val_y = max_pos - pos[1] - 1

            new[pos[0] + val_x, pos[1] + val_y] = 1

    if fac >= factor:
        return new
    elif fac > 1000:
        # Cap of 1000 iterations
        logger.fatal("Iteration cap was reached. Problems increasing the mask")
        return -1
    else:
        return shape_increase(new, factor, fac + 1)


def get_contours(image):

    im = image.copy()
    im /= np.nanmax(image)
    im *= 255
    im[np.where(im > 255)] = 255
    im[np.where(im <0)] = 0
    im = np.uint8(im)

    # TODO: change this threshold
    _, thresh = cv2.threshold(im, 10, 255, 0)
    contours, _ = cv2.findContours(thresh, 1, 2)

    to_remove = []
    for j in range(len(contours)):  # removes small contours (under 5 points)
        #print(cv2.contourArea(cont))

        if cv2.contourArea(contours[j]) <= 50:
            to_remove.append(j)
    for rm in reversed(to_remove):
        contours.pop(rm)

    found_masks = []
    brightness = [] 

    for cont in contours:
        mask = np.zeros(im.shape)
        cv2.drawContours(
            mask, [cont], -1, (255, 255, 255), -1
        )  # fills the contour with data

        mask[np.where(mask != 0)] = 1  # makes sure that we have binary mask
        found_masks.append(mask)
        brightness.append(np.nanmax(mask*image))

    return found_masks, brightness

def calc_mom(contour):
    M = cv2.moments(contour)

    cY = M["m10"] / M["m00"]
    cX = M["m01"] / M["m00"]
    return [cX, cY]


def shape_analysis(image, repeat_removal = 0):

    masks_to_keep = []
    masks_locs = []

    all_masks, brightness = get_contours(image)

    print(np.sort(brightness)[::-1])
    
    sorted_vals = np.argsort(brightness)[::-1]
    print(sorted_vals)
    all_masks = np.asarray(all_masks)[sorted_vals]
    
    for k in range(repeat_removal):
        if k ==0:
            im = image.copy()

        maximum_mask = all_masks[k]
        masks_to_keep.append(maximum_mask.copy())
        masks_locs.append(calc_mom(maximum_mask))
        maximum_mask = shape_increase(maximum_mask, 7)

        im[np.where( maximum_mask == 1 )] = np.nan 
    plt.imshow(im)
    plt.show()
    all_masks, brightness = get_contours(im)

    scaling_factor = 1
    for mask in all_masks:
        locs = calc_mom(mask)
        use = True
        for previous_locs in masks_locs:
            if np.isclose(previous_locs[0], locs[0], atol=15 * scaling_factor) and np.isclose(previous_locs[1], locs[1], atol=15 * scaling_factor):
                use = False 
        
        if use:
            masks_to_keep.append(mask)
            masks_locs.append(locs)
            
    return masks_to_keep, masks_locs




    

if __name__ == '__main__':
    path = '/home/amiguel/archi/data_files/CHEOPSim_job7794/data_reduction/COR/CH_PR900018_TG003901_TU2019-10-11T07-51-45_SCI_COR_SubArray_V0000.fits'
    path = '/home/amiguel/archi/data_files/55Cnc/data_reduction/COR/CH_PR300024_TG000301_TU2020-03-09T04-59-05_SCI_COR_SubArray_V0100.fits'
    #path = '/home/amiguel/archi/data_files/CHEOPSim_job7792/data_reduction/COR/CH_PR900018_TG003901_TU2019-10-11T07-50-39_SCI_COR_SubArray_V0000.fits'
    #path = '/home/amiguel/archi/data_files/CHEOPSim_job7793/data_reduction/COR/CH_PR900018_TG003901_TU2019-10-11T07-50-27_SCI_COR_SubArray_V0000.fits'
    with fits.open(path) as hdulist:
        images = hdulist[1].data 
    
    print(np.asarray(images[0]))
    masks_to_keep, masks_locs = shape_analysis(np.asarray(images[0]), 1)


    [plt.contour(i) for i in masks_to_keep]
    # Normalization to use with OpenCv
    plt.figure()
    plt.imshow(np.log10(images[0]))

    plt.show()
