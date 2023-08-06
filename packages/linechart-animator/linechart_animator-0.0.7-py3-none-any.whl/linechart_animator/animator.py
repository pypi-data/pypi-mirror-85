from typing import List, Optional
import os
import numpy as np

from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.interpolate import make_interp_spline

class Animator():
    def __init__(
        self,
        x_label_text: str,
        y_label_text: str,
        title_text: str,
        line_color: str='#fca311',
        line_width: float=5,
        outer_bg_color: str='#14213d', 
        inner_bg_color: str='#14213d',
        remove_chart_frames: bool=True,
        chart_frame_color: str='#000000',
        tick_params_length: float=0,
        tick_params_color: str='#e5e5e5',
        label_font_size: str=15,
        title_font_size: str=20,
        animation_interval: float=25,
        fps: int=24,
        dpi: int=192,
        width: int=1920,
        height: int=1080
    ):
        self.x_label_text = x_label_text
        self.y_label_text = y_label_text
        self.title_text = title_text
        self.line_color = line_color
        self.line_width = line_width
        self.outer_bg_color = outer_bg_color
        self.inner_bg_color = inner_bg_color
        self.remove_chart_frames = remove_chart_frames
        self.chart_frame_color = chart_frame_color
        self.tick_params_length = tick_params_length
        self.tick_params_color = tick_params_color
        self.label_font_size = label_font_size
        self.title_font_size = title_font_size
        self.animation_interval = animation_interval
        self.fps = fps
        self.dpi = dpi
        self.width = width,
        self.height = height

    def create_animated_chart(
        self, 
        x_values: List[float], 
        y_values: List[float], 
        output_path: str
    ) -> Optional[str]:
        x_values = np.array(x_values)
        y_values = np.array(y_values)

        #define x as 200 equally spaced values between the min and max of original x 
        xnew = np.linspace(x_values.min(), x_values.max(), 200) 
        #define spline
        spl = make_interp_spline(x_values, y_values, k=3)
        y_smooth = spl(xnew)
        x_values = xnew
        y_values = y_smooth

        fig = plt.figure(figsize=(self.width/self.dpi, self.heigth/self.dpi), dpi=self.dpi)
        ax = plt.axes(xlim=(np.amin(x_values)-1, np.amax(x_values)+1), ylim=(np.amin(y_values)-1, np.amax(y_values)+1))
        ax.tick_params(axis='both', which='both',length=self.tick_params_length)

        if self.remove_chart_frames:
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
        else:
            for spine in ax.spines.values():
                spine.set_edgecolor(self.chart_frame_color)

        ax.set_facecolor(self.outer_bg_color)
        fig.set_facecolor(self.inner_bg_color)
        ax.tick_params(axis='x', colors=self.tick_params_color)
        ax.tick_params(axis='y', colors=self.tick_params_color)
        plt.xlabel(self.x_label_text, fontsize=self.label_font_size, color=self.tick_params_color)
        plt.ylabel(self.y_label_text, fontsize=self.label_font_size, color=self.tick_params_color)
        plt.title(self.title_text, fontsize=self.title_font_size, color=self.tick_params_color)

        line, = ax.plot([], [], lw=self.line_width, color=self.line_color)

        def animate(i):
            line.set_data(x_values[:i],y_values[:i])

            return line,

        anim = animation.FuncAnimation(
            fig, 
            animate, 
            len(x_values),
            interval=self.animation_interval, 
            blit=True
        )
        
        anim.save(output_path, writer='ffmpeg', fps=self.fps)

        return os.path.exists(output_path)