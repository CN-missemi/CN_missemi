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
from numba import cuda
subtitle_images = pathlib.Path("subtitle-images")
rendered_images = pathlib.Path("rendered-images")
raw_images = pathlib.Path("images")
FILENAME_EXPR = re.compile(
    r"(?P<type>(major)|(minor))-subtitle-(?P<id>[0-9]+)-(?P<begin>[0-9]+)-(?P<end>[0-9]+)\.png")
BOTTOM_OFFSET = 40  # 主字幕底边距离视频底部的距离
TOP_OFFSET = 40  # 副字幕顶边距离视频顶部的距离


@dataclasses.dataclass
class RenderData:
    flap: int
    subtitle_img: numpy.ndarray = None
    subtitle_id: int = -1
    minor_subtitle_img: numpy.ndarray = None
    minor_subtitle_id: int = -1
    has_subtitle: bool = False
    force_render: bool = False  # 为true时，即使目标文件已经存在也要重新渲染


@numba.jit(nopython=True)
# @cuda.jit()
def render_subtitle(src_img: numpy.ndarray, subtitle_img: numpy.ndarray, major: bool):
    rowc = len(subtitle_img)
    colc = len(subtitle_img[0])
    img_rowc = len(src_img)
    img_colc = len(src_img[0])
    if major:
        lurow = img_rowc-BOTTOM_OFFSET-rowc
    else:
        lurow = TOP_OFFSET
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
    if os.path.exists(rendered_images/filename):
        if data.force_render:
            os.remove(rendered_images/filename)
        else:
            return
    if not data.has_subtitle:
        if not os.path.exists(raw_images/filename):
            return
        shutil.copy(raw_images/filename, rendered_images/filename)
        return
    src_img = cv2.imread(str(raw_images/filename))
    if data.subtitle_img is not None:
        render_subtitle(src_img, data.subtitle_img, True)
    if data.minor_subtitle_img is not None:
        render_subtitle(src_img, data.minor_subtitle_img, False)
    cv2.imwrite(str(rendered_images/filename), src_img)
    print(filename, "ok")


def main():
    begin_time = time.time()
    if not os.path.exists(rendered_images):
        os.mkdir(rendered_images)
    renderdata = [RenderData(flap=i, subtitle_img=None, subtitle_id=-1, minor_subtitle_id=-1, minor_subtitle_img=None,
                             has_subtitle=False) for i in range(0, 86880+2)]  # full:67071
    for item in os.listdir(subtitle_images):
        match_result = FILENAME_EXPR.match(item)
        groupdict = match_result.groupdict()
        # sub里的帧数从0开始
        begin = int(groupdict["begin"])+1
        end = int(groupdict["end"])+1
        subtitle_type = groupdict["type"]
        subtitle_id = int(groupdict["id"])
        print(subtitle_images/item)
        image_data = cv2.imread(str(subtitle_images/item))
        if subtitle_type == "major":
            for j in range(begin, end+1):
                if j >= len(renderdata):
                    break
                renderdata[j] = RenderData(
                    flap=j,
                    subtitle_img=image_data,
                    subtitle_id=subtitle_id,
                    minor_subtitle_id=renderdata[j].minor_subtitle_id,
                    minor_subtitle_img=renderdata[j].minor_subtitle_img,
                    has_subtitle=True)

        else:
            for j in range(begin, end+1):
                if j >= len(renderdata):
                    break
                renderdata[j] = RenderData(
                    flap=j,
                    subtitle_img=renderdata[j].subtitle_img,
                    subtitle_id=renderdata[j].subtitle_id,
                    minor_subtitle_img=image_data,
                    minor_subtitle_id=subtitle_id,
                    has_subtitle=True 
                )
                # renderdata[j] = RenderData(
                #     flap=j,
                #     subtitle_img=renderdata[j].subtitle_img,
                #     subtitle_id=renderdata[j].subtitle_id,
                #     minor_subtitle_img=None,
                #     minor_subtitle_id=-1,
                #     has_subtitle=True,
                #     force_render=True
                # )  # 只渲染副字幕

        # break
    print(f"{len(renderdata)} flaps loaded")
    pool = multiprocessing.Pool()
    pool.map(render_to_image, renderdata)
    end_time = time.time()
    print(f"Task done, {end_time-begin_time}s")


if __name__ == "__main__":
    main()
