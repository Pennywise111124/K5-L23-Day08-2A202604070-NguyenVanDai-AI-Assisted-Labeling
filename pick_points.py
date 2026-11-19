import sys
import matplotlib.pyplot as plt
from PIL import Image
im = Image.open(f"data/images/{sys.argv[1]}")
fig, ax = plt.subplots(figsize=(12, 8)); ax.imshow(im)
def on_click(e):
    if e.xdata is None: return
    print(f"{round(e.xdata)},{round(e.ydata)}")
    ax.plot(e.xdata, e.ydata, "r+"); fig.canvas.draw()
fig.canvas.mpl_connect("button_press_event", on_click)
plt.show()