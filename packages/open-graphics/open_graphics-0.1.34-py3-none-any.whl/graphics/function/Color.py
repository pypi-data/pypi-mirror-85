# !/usr/bin/env python
# coding=utf-8
# 功能包：颜色识别
# 作者：Cash
# https://github.com/pixelogik/ColorCube

import math
import cv2
import colour
import numpy as np
from PIL import Image

from .Graphics import resize
from ..common.logs import logs

__all__ = ["get_hist",
           "get_hsv",
           "get_temperature",
           "Color"]


def get_hist(image):
    """
    提取颜色直方图
    :param image:
    :return:
    """
    if not isinstance(image, np.ndarray):
        logs.error("Image is None!")
        return None
    if len(image.shape) == 3 and image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif len(image.shape) < 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    tmp, _ = resize(image, 320)
    tmp = cv2.calcHist([tmp], [0, 1, 2], None, [8, 8, 8],
                       [0, 256, 0, 256, 0, 256])
    # 变为512维的
    tmp = cv2.normalize(tmp, tmp).flatten()
    return tmp


def get_hsv(image):
    """
    Hue（色调、色相）
    Saturation（饱和度、色彩纯净度）
    Value（明度）
    :param image:
    :return:
    """
    if not isinstance(image, np.ndarray):
        logs.error("Image is None!")
        return None
    if len(image.shape) == 3 and image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif len(image.shape) < 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    tmp, _ = resize(image, 320)
    tmp = cv2.cvtColor(tmp, cv2.COLOR_RGB2HSV)
    return tmp[:, :, 0].mean(), tmp[:, :, 1].mean(), tmp[:, :, 2].mean()


def get_temperature(image):
    """
    图片色温
    <3000K 暖系
    3000-5000K 中性
    >5000K 冷系
    https://stackoverflow.com/questions/38876429/how-to-convert-from-rgb-values-to-color-temperature
    :param image: must be RGB
    :return:
    """
    if not isinstance(image, np.ndarray):
        logs.error("Image is None!")
        return None
    if len(image.shape) == 3 and image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif len(image.shape) < 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    tmp, _ = resize(image, 320)
    tmp = colour.sRGB_to_XYZ(tmp / 255)
    tmp = colour.XYZ_to_xy(tmp)
    # Conversion to correlated colour temperature in K.
    tmp = colour.xy_to_CCT_Hernandez1999(tmp)
    # 只保留 < 15000的结果
    return tmp[tmp < 7000].mean()


class CubeCell:
    def __init__(self):
        # Count of hits (dividing the accumulators by this value gives the average color)
        self.hit_count = 0
        # Accumulators for color components
        self.r_acc = 0.0
        self.g_acc = 0.0
        self.b_acc = 0.0


class LocalMaximum:
    # Local maxima as found during the image analysis.
    # We need this class for ordering by cell hit count.
    def __init__(self, hit_count, cell_index, r, g, b):
        # Hit count of the cell
        self.hit_count = hit_count
        # Linear index of the cell
        self.cell_index = cell_index
        # Average color of the cell
        self.r = r
        self.g = g
        self.b = b


class Color:
    # Uses a 3d RGB histogram to find local maximas in the density distribution
    # in order to retrieve dominant colors of pixel images
    def __init__(self, resolution=20, avoid_color=None, distinct_threshold=0.14):
        # Keep resolution
        self.resolution = resolution
        # Threshold for distinct local maxima
        self.distinct_threshold = distinct_threshold
        # Color to avoid
        self.avoid_color = avoid_color
        # Helper variable to have cell count handy
        self.cell_count = resolution * resolution * resolution
        # Create cells
        self.cells = [CubeCell() for k in range(self.cell_count)]
        self.standard_color = [
            [232, 104, 48],
            [232, 58, 48],
            [232, 48, 140],
            [137, 48, 232],
            [64, 48, 232],

            [48, 128, 232],
            [48, 201, 232],
            [102, 238, 206],
            [48, 232, 73],
            [165, 232, 48],

            [232, 226, 48],
            [232, 183, 48],
            [232, 140, 48],
            [198, 125, 83],
            [0, 0, 0]
        ]
        self.standard_color_value = [
            '#e86830', '#e83a30', '#e8308c', '#8930e8', '#4030e8',
            '#3080e8', '#30c9e8', '#30e8bd', '#30e849', '#a5e830',
            '#e8e230', '#e8b730', '#e88c30', '#c67d53', '#000000']
        # Indices for neighbour cells in three dimensional grid
        self.neighbour_indices = [
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, -1],

            [0, 1, 0],
            [0, 1, 1],
            [0, 1, -1],

            [0, -1, 0],
            [0, -1, 1],
            [0, -1, -1],

            [1, 0, 0],
            [1, 0, 1],
            [1, 0, -1],

            [1, 1, 0],
            [1, 1, 1],
            [1, 1, -1],

            [1, -1, 0],
            [1, -1, 1],
            [1, -1, -1],

            [-1, 0, 0],
            [-1, 0, 1],
            [-1, 0, -1],

            [-1, 1, 0],
            [-1, 1, 1],
            [-1, 1, -1],

            [-1, -1, 0],
            [-1, -1, 1],
            [-1, -1, -1]
        ]

    def cell_index(self, r, g, b):
        # Returns linear index for cell with given 3d index
        index = r + g * self.resolution + b * self.resolution * self.resolution
        return index

    def clear_cells(self):
        for c in self.cells:
            c.hit_count = 0
            c.r_acc = 0.0
            c.g_acc = 0.0
            c.b_acc = 0.0

    def find_local_maxima(self, image):
        # Finds and returns local maxima in 3d histogram, sorted with respect to hit count
        # Reset all cells
        self.clear_cells()
        # Iterate over all pixels of the image
        for p in image.getdata():
            # Get color components
            r = float(p[0]) / 255.0
            g = float(p[1]) / 255.0
            b = float(p[2]) / 255.0
            # If image has alpha channel, weight colors by it
            if len(p) == 4:
                a = float(p[3]) / 255.0
                r *= a
                g *= a
                b *= a
            # Map color components to cell indices in each color dimension
            r_index = int(r * (float(self.resolution) - 1.0))
            g_index = int(g * (float(self.resolution) - 1.0))
            b_index = int(b * (float(self.resolution) - 1.0))
            # Compute linear cell index
            index = self.cell_index(r_index, g_index, b_index)
            # Increase hit count of cell
            self.cells[index].hit_count += 1
            # Add pixel colors to cell color accumulators
            self.cells[index].r_acc += r
            self.cells[index].g_acc += g
            self.cells[index].b_acc += b
        # We collect local maxima in here
        local_maxima = []
        # Find local maxima in the grid
        for r in range(self.resolution):
            for g in range(self.resolution):
                for b in range(self.resolution):
                    local_index = self.cell_index(r, g, b)
                    # Get hit count of this cell
                    local_hit_count = self.cells[local_index].hit_count
                    # If this cell has no hits, ignore it (we are not interested in zero hit cells)
                    if local_hit_count == 0:
                        continue
                    # It is a local maximum until we find a neighbour with a higher hit count
                    is_local_maximum = True
                    # Check if any neighbour has a higher hit count, if so, no local maxima
                    for n in range(27):
                        r_index = r + self.neighbour_indices[n][0]
                        g_index = g + self.neighbour_indices[n][1]
                        b_index = b + self.neighbour_indices[n][2]
                        # Only check valid cell indices (skip out of bounds indices)
                        if r_index >= 0 and g_index >= 0 and b_index >= 0:
                            if r_index < self.resolution and g_index < self.resolution and b_index < self.resolution:
                                if self.cells[self.cell_index(r_index, g_index, b_index)].hit_count > local_hit_count:
                                    # Neighbour hit count is higher, so this is NOT a local maximum.
                                    is_local_maximum = False
                                    # Break inner loop
                                    break
                    # If this is not a local maximum, continue with loop.
                    if is_local_maximum == False:
                        continue
                    # Otherwise add this cell as local maximum
                    avg_r = self.cells[local_index].r_acc / float(self.cells[local_index].hit_count)
                    avg_g = self.cells[local_index].g_acc / float(self.cells[local_index].hit_count)
                    avg_b = self.cells[local_index].b_acc / float(self.cells[local_index].hit_count)
                    local_maxima.append(LocalMaximum(local_hit_count, local_index, avg_r, avg_g, avg_b))
        # Return local maxima sorted with respect to hit count
        return sorted(local_maxima, key=lambda x: x.hit_count, reverse=True)

    def filter_distinct_maxima(self, maxima):
        # Returns a filtered version of the specified array of maxima,
        # in which all entries have a minimum distance of self.distinct_threshold
        result = []
        # Check for each maximum
        for m in maxima:
            # This color is distinct until a color from before is too close
            is_distinct = True
            for n in result:
                # Compute delta components
                r_delta = m.r - n.r
                g_delta = m.g - n.g
                b_delta = m.b - n.b
                # Compute delta in color space distance
                delta = math.sqrt(r_delta * r_delta + g_delta * g_delta + b_delta * b_delta)
                # If too close mark as non-distinct and break inner loop
                if delta < self.distinct_threshold:
                    is_distinct = False
                    break
            # Add to filtered array if is distinct
            if is_distinct == True:
                result.append(m)
        return result

    def filter_too_similar(self, maxima):
        # Returns a filtered version of the specified array of maxima,
        # in which all entries are far enough away from the specified avoid_color
        result = []
        ar = float(self.avoid_color[0]) / 255.0
        ag = float(self.avoid_color[1]) / 255.0
        ab = float(self.avoid_color[2]) / 255.0
        # Check for each maximum
        for m in maxima:
            # Compute delta components
            r_delta = m.r - ar
            g_delta = m.g - ag
            b_delta = m.b - ab
            # Compute delta in color space distance
            delta = math.sqrt(r_delta * r_delta + g_delta * g_delta + b_delta * b_delta)
            if delta >= 0.5:
                result.append(m)
        return result

    def get_main_color(self, image):
        tmp, _ = resize(image, 320)
        m = self.find_local_maxima(Image.fromarray(tmp))
        if not self.avoid_color is None:
            m = self.filter_too_similar(m)
        m = self.filter_distinct_maxima(m)
        colors = []
        for n in m:
            if len(colors) > 9:
                break
            r = round(n.r * 255.0)
            if r < 16:
                r = '0' + hex(r)[-1:]
            else:
                r = hex(r)[-2:]
            g = round(n.g * 255.0)
            if g < 16:
                g = '0' + hex(g)[-1:]
            else:
                g = hex(g)[-2:]
            b = round(n.b * 255.0)
            if b < 16:
                b = '0' + hex(b)[-1:]
            else:
                b = hex(b)[-2:]
            colors.append("#" + r + g + b)
            # colors.append([r, g, b])
        return colors

    def color_distance(self, color1, color2):
        r1, g1, b1 = color1[0], color1[1], color1[2]
        r2, g2, b2 = color2[0], color2[1], color2[2]
        r_mean = (r1 + r2) / 2
        r = r1 - r2
        g = g1 - g2
        b = b1 - b2
        return math.sqrt((2 + r_mean / 256) * (r ** 2) + 4 * (g ** 2) + (2 + (255 - r_mean) / 256) * (b ** 2))

    def get_similar_color(self, image, min_distance=180):
        tmp, _ = resize(image, 320)
        tmp = Image.fromarray(tmp)
        standard_color_count = [0 for i in range(len(self.standard_color))]
        # Iterate over all pixels of the image
        for p in tmp.getdata():
            for index in range(len(self.standard_color)):
                delta = self.color_distance(p, self.standard_color[index])
                if delta < min_distance:
                    standard_color_count[index] += 1
        color_percent = []
        w, h = tmp.size
        sum = w * h
        for i in range(len(standard_color_count)):
            color_percent.append(100 * standard_color_count[i] / sum)
        adjacentColorsList = []
        for i in range(0, len(color_percent)):
            adjacentColors = {}
            adjacentColors['color'] = self.standard_color_value[i]
            adjacentColors['percentage'] = color_percent[i]
            adjacentColorsList.append(adjacentColors)
        return adjacentColorsList


if __name__ == '__main__':
    import cv2
    import graphics as g

    image = cv2.imread("1.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = g.Color.get_temperature(image)
    print(result)
