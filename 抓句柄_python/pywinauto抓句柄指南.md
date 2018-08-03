#### pywinauto 使用：

1. 准备

   需要在win上装好py环境

   - 最好装与被抓句柄的程序相一致，比如抓32的句柄，就用32的python，其启动的时候，会有对应的提醒。
   - 下载&安装 ziyan的相关包、pywinauto。

2. 确定窗口所使用的后端。

   https://github.com/blackrosezy/gui-inspect-tool

   1. Spy++，如果spy++可以识别的，那么“win32”就是所需要的。

   2. inspect.exe，可以显示比spy++更多的控件及属性，那么使用“uia”，作为后端。

3. 新建app对象

4. ```
   app = pywinauto.Application()
   ```

   查找所需要的windows

   ```
   handle = pywinauto.findwindows.find_windows(class_name_re = "Note",title_re = "抓句柄*")
   # 返回值为
   # 实用参数：（参数来源于：pywinauto.findwindows.find_elements）
   parent			# 在这个父窗口下查找
   class_name_re	# 使用正则匹配类名
   title_re		# 使用正则匹配标题名
   handle			# 直接使用句柄查找
   control_id		# 控件ID（ControlID）
   control_type 	# 控件类型
   framework_id	# 框架id
   backend			# 搜索过程中，使用的后端
   top_level_only # 只搜索最上层的窗口(默认true)
   ```

5. 把app连接至查到的窗口（好像是为了操作这个窗口才需要。我们查找应该还不需要。）

   ```
   app = pywinauto.Application().connect(handle=hwnd)
   ```

6. 子窗口查找

   现在发现有两个方法。

   一是，复用`pywinauto.findwindows.find_windows` ，修改非top，指定parent为其handle。例如：

   ```
   childe_handle = pywinauto.findwindows.find_windows(
       title_re = "splitter",
       top_level_only = False,
       parent = handle)
       
   >> DEBUG: test: 方法一：匹配到子窗口的handle：['0x306e4', '0x306b2', '0x306e6']
   
   ```

   其二，使用`pywinauto.win32_element_info.HwndElementInfo(handle=handle)`查找handle下的所有子窗口。

   注意，这个会查找到很多层下的窗口。所以筛选起来会比较麻烦。

   ```
   tmp = pywinauto.win32_element_info.HwndElementInfo(handle=handle)
   childe_handle2 = tmp.children(title_re = "splitter")
   
   >> 方法二：匹配到子窗口的handle：['0x306e4', '0x306b2', '0x30704', ......, '0x306e6',............]
   ```

   当然，别以为使用`.children`的速度会快点，实际上是一样的，

   其`children`方法其实也是在所有HWND中筛选一遍。当然前面那个也是。0.0....遍历万岁？

   个人推荐方法一，看起来清爽，并且逻辑清晰点。

7. 窗口层次关系

   在spy++中，可以看到这些窗口的逐层关系。

   ![1533284205364](.\jpg\1533284205364.png)

8. 取文本

   ![1533285384751](.\jpg\1533285384751.png)

   假设经历千辛万苦获取到了所需要的子子子窗口的句柄。

   首先查看窗口的类型，比如，我这个窗口，类为 `SysListView32`，则在`...\pywinauto\controls\common_controls.py`中查找，支持分析此类新的方法。然后使用其分析，打印`.texts()`。支持分析的类，可以在其`windowclasses`中查看。

   ![1533286020303](.\jpg\1533286020303.png)

   ```
   text_handle = int(0x230792)
   msg_channel = pywinauto.controls.common_controls.ListViewWrapper(text_handle).texts()
   log.debug("{}的分析文本：{}".format(hex(text_handle),msg_channel))
   
   >> [2018-08-03 08:58:55.537169] DEBUG: test: 0x230792的分析文本：['', '运行时间:', '2:53:38', 'BitComet运行状态:', '总任务数:0 / 正在运行:0', '\n', '\n', ....]
   
   ```

   好了，剩下的就是你的骚操作时间。