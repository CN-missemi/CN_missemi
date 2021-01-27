# Farmer's Embedding Method - Toolchain

农民压制法工具链。

使用```Chromium``` + ```Pyppeteer```渲染字幕图像，然后使用```numba```JIT优化过的```OpenCV```操作来将字幕逐帧附加到视频图片上，最后将视频图片拼接起来。

## 准备
```plain
- images/ (以X.png为格式逐帧存储原视频图像)
- myaudio.m4a (原视频的音频文件)
```

## 运行
在```render_subtitle.py```内，修改```FILENAME```为使用的字幕文件后运行```render_subtitle.py```。

在```render_image.py```内，根据提示修改第```68```行。

等待完成后运行```render_image.py```，最后运行```generate_final_video.py```生成最终视频。