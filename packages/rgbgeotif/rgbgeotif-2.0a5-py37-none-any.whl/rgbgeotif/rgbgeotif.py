from matplotlib import pyplot as plt
import numpy as np
import rasterio

class RGBGeoTif(list):
    def __init__(self, file, return_img=True, range_scale=None):
        src = rasterio.open(file)
        arrays = src.read()
        if return_img:
            if range_scale is not None:
                arrays = np.uint8([255 * ((array - range_scale[0])/(range_scale[1] - range_scale[0]))
                                   for array in arrays])
                [self.append(v) for v in arrays]
            else:
                for array in arrays:
                    fig = plt.figure(figsize=array.shape, dpi=1)
                    plt.set_cmap("Greys")
                    plt.axis('off')
                    plt.imshow(array)
                    fig.tight_layout()
                    fig.canvas.draw()
                    w, h = fig.canvas.get_width_height()
                    image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8)
                    image.shape = (w, h, 3)
                    image = np.roll(image, 3, axis=2)
                    self.append(image)
                    plt.close(fig)
        else:
            [self.append(v) for v in arrays]


if __name__=="__main__":
    flood = "/mnt/DataHub/SYNS/FLOOD/data/sen11/S1Flood/Bolivia_23014_S1Flood.tif"
    sar = "Bolivia_23014_S1.tif"
    flood = RGBGeoTif(flood)
    sar = RGBGeoTif(sar)
