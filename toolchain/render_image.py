from cv2 import cv2
import pathlib
import numpy
import os
import shutil
import typing
import dataclasses
import multiprocessing
import re
import time
import numba
subtitle_images = pathlib.Path("subtitle-images")
rendered_images = pathlib.Path("rendered-images")
raw_images = pathlib.Path("images")
FILENAME_EXPR = re.compile(
    r"subtitle-(?P<id>[0-9]+)-(?P<begin>[0-9]+)-(?P<end>[0-9]+).png")
BOTTOM_OFFSET = 40


@dataclasses.dataclass
class RenderData:
    flap: int
    subtitle_img: numpy.ndarray
    subtitle_id: int
    has_subtitle: bool = False


@numba.jit(nopython=True)
def process_image(src_img, subtitle_img):
    rowc = len(subtitle_img)
    colc = len(subtitle_img[0])
    img_rowc = len(src_img)
    img_colc = len(src_img[0])
    lurow = img_rowc-BOTTOM_OFFSET-rowc
    lucol = (img_colc-colc)//2
    # (lurow,lucol) 主字幕左上角坐标
    bg_area = src_img[lurow:lurow+rowc, lucol:lucol+colc]  # 截取背景
    for r in range(rowc):
        for c in range(colc):
            # 背景色(黑色)，半透明处理
            if subtitle_img[r, c][0] == 0 and subtitle_img[r, c][1] == 0 and subtitle_img[r, c][2] == 0:
                bg_area[r, c] = (bg_area[r, c]+subtitle_img[r, c])//2
            else:
                # 非背景色，不透明
                bg_area[r, c] = subtitle_img[r, c]
    src_img[lurow:lurow+rowc, lucol:lucol+colc] = bg_area


def render_to_image(data: RenderData):
    filename = f"{data.flap}.png"
    if not data.has_subtitle:
        if not os.path.exists(raw_images/filename):
            return
        shutil.copy(raw_images/filename, rendered_images/filename)
        return
    src_img = cv2.imread(str(raw_images/filename))
    process_image(src_img, data.subtitle_img)
    cv2.imwrite(str(rendered_images/filename), src_img)
    print(filename, "ok")


def main():
    begin_time = time.time()
    shutil.rmtree(rendered_images, True)
    os.mkdir(rendered_images)
    # to_render = [i for i in range(6253+1)]
    # renderdata = [RenderData(i, None, -1, False) for i in range(6253+1)]
    renderdata = [RenderData(i, None, -1, False) for i in range(0, 6253+2)]
    for item in os.listdir(subtitle_images):
        match_result = FILENAME_EXPR.match(item)
        groupdict = match_result.groupdict()
        # sub里的帧数从0开始
        begin = int(groupdict["begin"])+1
        end = int(groupdict["end"])+1

        subtitle_id = int(groupdict["id"])
        print(subtitle_images/item)
        image_data = cv2.imread(str(subtitle_images/item))

        for j in range(begin, end+1):
            renderdata[j] = RenderData(j, image_data, subtitle_id, True)
        # break
    print(f"{len(renderdata)} subtitles loaded")
    pool = multiprocessing.Pool()
    pool.map(render_to_image, renderdata)
    end_time = time.time()
    print(f"Task done, {end_time-begin_time}s")


if __name__ == "__main__":
    main()
