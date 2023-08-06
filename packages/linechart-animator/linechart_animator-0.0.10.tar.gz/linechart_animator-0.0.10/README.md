# linechart_animator

![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/linechart_animator?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/linechart_animator)

<img src="https://j.gifs.com/914qNZ.gif" width="550" height="400"/>

## Installation
````bash
pip3 install linechart_animator
````
## Usage

````python
from linechart_animator import Animator

animator = Animator(
    x_label_text='x label',
    y_label_text='y label',
    title_text='Animated linechart'
)

animator.create_animated_chart(
    x_values = [1,10,16,43,52], # SORTED ARRAY
    y_values = [35,42,53,2,90],
    output_path='/Users/macbook/Desktop/animated_chart.mp4'
)
````

## Notes

* x axis values must be a sorted array.
* Matplotlib doesn't work with pixels directly, but rather physical sizes and DPI. If you want to display a figure with a certain pixel size, you need to know the DPI of your monitor. For example this link will detect that for you: https://www.infobyip.com/detectmonitordpi.php

### Optional parameters with their default values

````python
line_color: str='#fca311'
line_width: float=5
outer_bg_color: str='#14213d'
inner_bg_color: str='#14213d'
remove_chart_frames: bool=True
chart_frame_color: str='#000000'
tick_params_length: float=0
tick_params_color: str='#e5e5e5'
label_font_size: str=15
title_font_size: str=20
animation_interval: float=25
fps: int=24
dpi: int=192
width: int=1920
height: int=1080
````
