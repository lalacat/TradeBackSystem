from PyQt5 import QtGui

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GREY_COLOR = (100, 100, 100)

OPEN_COLOR = '#FFD700' # 黄色
CLOSE_COLOR = '#082E54' # 梅红色


UP_COLOR = '#FF0000' # (255, 0, 0)
DOWN_COLOR = '#32CD32' #酸橙绿 (61,89,171) # 深蓝色
CURSOR_COLOR = (255, 245, 230) # old lace

UP_LINE_COLOR = '#808069' # (255,215,0) 金黄色
MID_LINE_COLOR = '#FFFAF0' # (128,42,42) 棕色
DOWN_LINE_COLOR='#FF00FF' # (0,199,140) 土耳其玉色
FOUTH_COLOR= '#A020F0'  # (160,32,240) 紫色
FIVTH_COLOR = '#FF4500'  # 桔红


COLOR_GROUP = [UP_LINE_COLOR,MID_LINE_COLOR,DOWN_LINE_COLOR,FOUTH_COLOR]

# COLOR_GROUP = ['#5E2612','#03A89E','#228B22']

PEN_WIDTH = 1
BAR_WIDTH = 0.24
# BAR_WIDTH = 0.4



AXIS_WIDTH = 0.8
NORMAL_FONT = QtGui.QFont("Arial", 9)


def to_int(value: float) -> int:
    """"""
    return int(round(value, 0))
