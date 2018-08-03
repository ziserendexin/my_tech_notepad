import pywinauto
import os.path
import sys
from pprint import pprint,pformat
from logbook import Logger, RotatingFileHandler, StreamHandler


# print("./{}.log".format(os.path.basename(__file__)))
# 将日志输出到轮换日志中（设定&应用）
RotatingFileHandler(
    "./{}.log".format(os.path.basename(__file__)),
    max_size=10000).push_application()
# 将日志输出到sys.stdout
StreamHandler(sys.stdout).push_application()
log = Logger('test')


# log.info("xaaa")
# 新建一个对象
app = pywinauto.Application()
# 通过 find_window来查找窗口
handles = pywinauto.findwindows.find_windows(title_re = ".+BitComet.+")
log.debug("匹配到主窗口的handle：{}".format(list(map(lambda x:hex(x),handles))))
handle = handles[0]
# 通过Application来新建对象，并连接这个句柄
# app = pywinauto.Application().connect(handle=handle)
# top_window = app.window()
childe_handle = pywinauto.findwindows.find_windows(
    title_re = "splitter",
    top_level_only = False,
    parent = handle)
log.debug("方法一：匹配到子窗口的handle：{}".format(list(map(lambda x:hex(x),childe_handle))))

# 方法二
tmp = pywinauto.win32_element_info.HwndElementInfo(handle=handle)
childe_handle2 = tmp.children(title_re = "splitter")
log.debug("方法二：匹配到子窗口的handle：{}".format(list(map(lambda x:hex(x.handle),childe_handle2[0:5]))))



# 把 窗口的句柄的来传入ListViewWrapper等控件，其中方法里面windowclasses表示这个所支持的类
text_handle = int(0x230792)
msg_channel = pywinauto.controls.common_controls.ListViewWrapper(text_handle).texts()
log.debug("{}的分析文本：{}".format(hex(text_handle),msg_channel))



