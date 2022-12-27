import numpy as np
from pathlib import Path
import SimpleITK as itk
from typing import Optional, Union

DIRECTION_COSINES = [1, 0, 0, 0, 1, 0, 0, 0, 1]
# T011A0HQ135, T017A0\T017A0HQ002.nrrd

#-------------------------------------------------------------------------

def _check_orientation(img: itk.Image, id_) -> Union[itk.Image, bool]:
    """ Check image is orientated correctly
        and flip/rotate if necessary
    """

    image_dir = np.around(img.GetDirection()).astype(np.int32)
    if (image_dir == DIRECTION_COSINES).all():
        return img, False

    if image_dir[0] == 0 and image_dir[4] == 0:
        img = itk.PermuteAxes(img, [1, 0, 2])
        image_dir = np.around(img.GetDirection()).astype(np.int32)
        print(id_)

    img = img[::image_dir[0], ::image_dir[4], :]

    return img, True


#-------------------------------------------------------------------------

def check_coordinates(curr_dir: Optional[Path] = None) -> None:
    """ Check that all images are oriented correctly in LPS system with
        direction cosines (1, 0, 0, 0, 1, 0, 0, 0, 1) - if e.g.
        (1, 0, 0, 0, -1, 0, 0, 0, 1) then flip as appropriate
    """

    if curr_dir is None:
        curr_dir = Path()

    for img_id in curr_dir.glob('*'):
        img = itk.ReadImage(img_id)
        img, transformed = _check_orientation(img, img_id)

        if transformed:
            itk.WriteImage(img, img_id, dtype=np.int16)

        elif "T002A1" not in str(img_id):
            itk.WriteImage(img, img_id, dtype=np.int16)