<body class="typora-export">
# matplotlib笔记（基于 matplotlib 1.5.1 ）

## 一、matplotlib配置

1. matplotlib配置信息是从配置文件中读取的。在配置文件中可以为matplotlib几乎所有的属性指定永久有效的默认值。

2. 查看配置：你可以通过 `matplotlib.rcParams`字典访问所有已经加载的配置项

![查看matplotlib配置](./../imgs/settings_from_rcParams.JPG)

3. 修改配置：

    * 你可以通过 `matplotlib.rcParams`字典修改所有已经加载的配置项

    ![通过rcParams修改配置](./../imgs/modify_settings_with_rcParams.JPG)

    * 你可以通过`matplotlib.rc(*args,**kwargs)`来修改配置项，其中`args`是你要修改的属性，`kwargs`是属性的关键字属性

    ![通过rc函数修改配置](./../imgs/modify_settings_with_rc.JPG)

    * 你可以调用`matplotlib.rcdefaults()`将所有配置重置为标准设置。

    ![恢复默认配置](./../imgs/reset_settings.JPG)


4. 配置文件：如果不希望在每次代码开始时进行参数配置，则可以在项目中给出配置文件。配置文件有三个位置：

    * 系统级配置文件。通常在python的`site-packages`目录下。每次重装`matplotlib`之后该配置文件就会被覆盖。

    * 用户级配置文件。通常在`$HOME`目录下。可以用`matplotlib.get_configdir()`函数来查找当前用户的配置文件目录。可以通过`MATPLOTLIBRC`修改它的位置。

    ![恢复默认配置](./../imgs/setting_files.JPG)

    * 当前工作目录。即项目的目录。在当前目录下，可以为目录所包含的当前项目给出配置文件，文件名为`matplotlibrc`。


优先级顺序是： 当前工作目录 > 用户级配置文件 > 系统级配置文件。查看当前使用的配置文件的路径为： `matplotlib.matplotlib_fname()`函数。

配置文件的内容常见的有以下几种：

    * axes:设置坐标轴边界和表面的颜色、坐标刻度值大小和网格的显示
    * backend：设置目标输出TkAgg和GTKAgg
    * figure:控制dpi、边界颜色、图像大小和子区(`subplot`)设置
    * font：字体(`font family`)、字体大小和样式设置
    * grid:设置网格颜色和线型
    * legend：设置图例以及其中的文本显示
    * line：设置线条（颜色、线型、宽度等）和标记
    * patch: 填充2D空间的图形图像，如多边形和圆。控制线宽、颜色和抗锯齿设置等。
    * savefig:对保存的图形进行单独设置。如渲染的文件背景为白色。
    * text：设置字体颜色、文本解析（纯文本和latex标记）等。
    * verbose:设置matplotlib执行期间的信息输出，如silent、helpful、debug和debug--annoying
    * xticks和yticks：为x、y轴的主刻度和次刻度设置颜色、大小、方向以及标签大小


## 二、 matplotlib Artist

1. `matplotlib`有三个层次的API：

    * `matplotlib.backend_bases.FigureCanvas`：代表了一个绘图区，在这个绘图区上图表被绘制
    * `matplotlib.backend_bases.Renderer`：代表了渲染器，它知道如何在绘图区上绘图。
    * `matplotlib.artist.Artist`：代表了图表组件，它知道如何利用渲染器在绘图区上绘图。

通常用于有95%以上的时机都是与`matplotlib.artist.Artist`类打交道，它是高层次的绘图控制。

2. `matplotlib`中有两种`Artist`：

    * `primitive`：代表了我们在绘图区域上绘制的基础的绘图组件，比如`Line2D`，`Rectangle`，`Text` 以及`AxesImage`等等。

    * `container`：代表了放置`primitive`的那些绘图组件。比如`Axis`、`Axes`以及`Figure`，如图所示

    ![Artist](./../imgs/Artist.JPG)


3. `matplotlib`的标准使用流程为：

    * 创建一个`Figure`实例对象`fig`
    * 使用`fig`实例创建一个或者多个`Axes`实例，或者创建一个或者多个`Subplot`实例
    * 使用`Axes`实例的方法来创建`primitive`

4. 每个在图形中出现的元素都是`Artist`。其属性有：

    * `Figure.patch`属性：是一个`Rectangle`，代表了图表的矩形框，它的大小就是图表的大小， 并且可以通过它设置图表的背景色和透明度。

    * `Axes.patch`属性：也是一个`Rectangle`，代表了绘图坐标轴内部的矩形框（白底黑边）， 通过它可以设置`Axes`的颜色、透明度等。

    * 所有的`Artist`有下列属性。：

        * `.alpha`属性：透明度。值为0--1之间的浮点数
        * `.animated`属性：一个布尔值，表示是否用于加速动画绘制
        * `.axes`属性：返回这个`Artist`所属的`axes`，可能为`None`
        * `.clip_box`属性：用于剪切`Artist`的`bounding box`
        * `.clip_on`属性：是否开启`clip`
        * `.clip_path`属性：`Artist`沿着该`path`执行`clip`
        * `.contains`属性：一个`picking function`用于测试`Artist`是否包含`pick point`
        * `.figure`属性：该`Artist`所属的`Figure`，可能为`None`
        * `.gid`属性：该`Artist`的`id`字符串
        * `.label`：一个`text label`
        * `.picker`:一个`python object`用于控制`object picking`
        * `.transform`：转换矩阵
        * `.url`属性：一个`url string`，代表本`Artist`
        * `.visible`：布尔值，控制`Artist`是否绘制
        * `.zorder`：决定了`Artist`的绘制顺序。`zorder`越小就越底层，则越优先绘制。


这些属性可以通过旧式的`setter`和`getter`函数访问和设置。如：`o.get_alpha()`、`o.set_alpha(0.5)`。如果你想一次设置多个属性，也可以用：`o.set(alpha=0.5,zorder=2)`这种方式。你可以使用`matplotlib.artist.getp(o)`来一次获取`o`的所有属性。

当然你可以使用`pyplot.getp(o,"alpha")`来获取属性（一次只能返回一个属性），如果指定属性名，则返回对象的该属性值；如果不指定属性名，则返回对象的所有的属性和值。用`pyplot.setp(o,alpha=0.5,zorder=2)`来设置属性（一次可以设置多个属性）

![Artist所有属性](./../imgs/Artist_attribute.JPG)


### 1. container Artist:

#### a. Figure

1. `matplotlib.figure.Figure`是最顶层的`container Artist`，它包含了图表中的所有元素。

    * `Figure.patch`属性：`Figure`的背景矩形
    * `Figure.axes`属性：持有的一个`Axes`实例的列表（包括`Subplot`)
    * `Figure.images`属性：持有的一个`FigureImages patch`列表
    * `Figure.lines`属性：持有一个`Line2D`实例的列表（很少使用）
    * `Figure.legends`属性：持有的一个`Figure Legend`实例列表（不同于`Axes.legends`)
    * `Figure.patches`属性：持有的一个`Figure pathes`实例列表（很少使用)
    * `Figure.texts`属性：持有的`Figure Text`实例列表

其他的属性：

    * `Figure.figsize`属性：图像的尺寸，`(w,h)`，以英寸为单位
    * `Figure.dpi`属性：图像分辨率
    * `Figure.facecolor`属性：背景色
    * `Figure.edgecolor`属性：`edge color`
    * `Figure.linewidth`：`edge linewidth`
    * `Figure.frameon`：如果为`False`，则不绘制图像
    * `Figure.subplotpars`：一个`SubplotParams`实例
    * `Figure.tight_layout`：如果为`False`，则使用`subplotpars`；否则使用`tight_layout()`调整`subplot parameters`

2. 当你执行`Figure.add_subplot()`或者`Figure.add_axes()`时，这些新建的`Axes`都被添加到`Figure.axes`列表中。

3. 由于`Figure`维持了`current axes`，因此你不应该手动的从`Figure.axes`列表中添加删除元素，而是要通过`Figure.add_subplot()`、`Figure.add_axes()`来添加元素，通过`Figure.delaxes()`来删除元素。但是你可以迭代或者访问`Figure.axes`中的`Axes`，然后修改这个`Axes`的属性。

4. 可以通过`Figure.gca()`获取`current axes`，通过`Figure.sca()`设置`current axes`。

5. `Figure`也有它自己的`text`、`line`、`patch`、`image`。你可以直接通过`add primitive`语句直接添加。但是注意`Figure`默认的坐标系是以像素为单位，你可能需要转换成`figure`坐标系：(0,0)表示左下点，(1,1)表示右上点。

![Figure](./../imgs/Figure_attribute.JPG)

6. 创建`Figure`的方法：

```
matplotlib.pyplot.figure(num=None, figsize=None, dpi=None, facecolor=None,  edgecolor=None, frameon=True, FigureClass=<class 'matplotlib.figure.Figure'>,   **kwargs)
```

    * `num`：一个整数或者字符串。

        * 若未提供，则创建一个新的`figure`。<br></br>
        * 如果给出了一个整数，而且某个现有的`figure`对象的`number`属性刚好等于这个整数，则激活该`figure`并且返回该`figure`；否则创建一个新的`figure`
        * 如果是个字符串，则创建一个新的`figure`，并且将`window title`设置为该字符串。

    * `figsize`：一对整数的元组。给出了英寸为单位的高度和宽度。默认由`rc`的 `figure.figsize`给出

    * `dpi`：一个整数，给出`figure`的分辨率。默认由`rc`的 `figure.dpi`给出

    * `facecolor`：背景色。若未提供，则由`rc`的 `figure.facecolor`给出

    * `edgecolor`：`border color`。若未提供，则由`rc`的 `figure.edgecolor`给出


返回一个`figure`


##### 1>. Figure 的一些方法

1. `add_axes(*args, **kwargs)`：创建一个`Axes`对象。如果已经存在同样位置同样参数的一个`Axes`，则返回该`Axes`，并将其设为`current Axes`。其参数有：<br></br>

    * `rect`:一个元组，代表了`(left,bottom,width,height)`，它是第一个位置参数
    * `axisbg`：一个`color`，背景色
    * `frameon`：布尔值，是否`display frame`
    * `sharex`：另一个`Axes`对象，与该`Axes`共享 `xaxis`
    * `sharey`：另一个`Axes`对象，与该`Axes`共享 `yaxis`
    * `projection`：坐标系类型。`projection='polar'`也等价于`polar=True`
    * `aspect`：一个数值，指定`x`和`y`轴每个单位的尺寸比例。也可以设定为字符串`'equal'/'auto'`
    * 关键字参数为`projection`+`Axes`的合法关键字

如果你想在同样的一个`rect`创建两个`Axes`，那么你需要设置`label`参数。不同的`Axes`通过不同的`label`鉴别。

如果你使用了`fig.delaxes()`从`Figure`中移除了`ax`，那么你可以通过`fig.add_exes(ax)`来将其放回。

2. `add_subplot(*args,**kwargs)`：创建一个`subplot`。如果已经存在同样位置同样参数的一个`subplot`，则返回该`subplot`，并将其设为`current Axes`。

    * 关键字参数为`projection`+`Axes`的合法关键字。`projection`：坐标系类型。`projection='polar'`也等价于`polar=True`
    * 位置参数为：`add_subplot(nrows, ncols, plot_number)`。表示`nrows`行， `nclos`列每个单元格是一个`sub-axes`。`plot_number`给出了指定的`sub-axes`，从 1开始。最大为`nrows*ncols`。当这三个数字都是个位数时，可以使用一个三位数代替，每位代表一个数。
    * `axisbg`：一个`color`，背景色
    * `frameon`：布尔值，是否`display frame`
    * `sharex`：另一个`Axes`对象，与该`Axes`共享 `xaxis`
    * `sharey`：另一个`Axes`对象，与该`Axes`共享 `yaxis`
    * `projection`：坐标系类型。`projection='polar'`也等价于`polar=True`
    * `aspect`：一个数值，指定`x`和`y`轴每个单位的尺寸比例。也可以设定为字符串`'equal'/'auto'`

3. `autofmt_xdate(bottom=0.2, rotation=30, ha='right')`：用于设置`Date ticklabel`的位置。`bottom`设置距离`subplot`底部的位置。`rotation`设置了`xtick label`的旋转角度。`ha`设置`xtick label`的对其方式。该函数主要用于当`xtick`为日期，可能会重叠，因此可以旋转一个角度

4. `clear()`：清除一个`figure`

5. `clf(keep_observers=False)`：清除一个`figure`。如果`keep_observers=True`，则`gui`仍然会跟踪`figure`中的`axes`

6. `colorbar(mappable, cax=None, ax=None, use_gridspec=True, **kw)`：为`mappable`创建一个`colorbar`。其中：

    * `mapple`：一个`ScalarMapple`实例。它可以是`Image/ContourSet...`。
    * `cax`：指定在哪个`axes`中绘制`colorbar`。也可以是`None`
    * `ax`：None | parent axes object(s) from which space for a new colorbar axes will be stolen.
    * `use_gridspec`：False | If cax is None, a new cax is created as an instance of Axes. If ax is an instance of Subplot and use_gridspec is True, cax is created as an instance of Subplot using the grid_spec module

7. `delaxes(a)`：从`figure`中移除`axes`

8. `gca(**kwargs)`：返回`current axes`。如果不存在则创建一个

9. `get_children()`：获取`figure`中包含的`artists`

10. `get_dpi/get_edgecolor/get_facecolor/get_figheight/get_figwidth/` `get_frameon/get_tight_layout...`：获取对应的属性值

11. `get_size_inches()`：返回`fig`的当前尺寸（单位为英寸。`1in=2.54cm`）

12. `legend(handles, labels, *args, **kwargs)`：创建图例。

    * `handles`：是一个`Lin2D/Patch`等实例的一个序列
    * `labels`：是个字符串序列，用于给上述实例添加图例说明
    * `loc`：指定图例的位置。可以是字符串`'best'`/`'upper right'`/`'upper left'` /`'lower left'`/`'lower right'`/`'right'`/`'center left'`/`'center right'` /`'lower center'`/`'upper center'`/`'center'`。你也可以指定坐标`(x,y)`，其中`(0,0)`是左下角，`(1,1)`是右上角
    * `numpoint`/`scatterpoints`：图例上每个图例线的点数
    * `fancybox`：如果为`True`，图例的边框采用圆角矩形
    * `shadow`：如果为`True`，图例添加背影
    * `ncol`：列数
    * `title`：图例的标题
    * `framealpha`：一个浮点数，从0到 1，图例的透明度
    * `frameon`：一个布尔值，如果为`True`，则绘制图例的背景框。否则不绘制。

13. `savefig(fname, dpi=None, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None, transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)`：保存图像。

    * `fname`：带路径的文件名。
    * `dpi`：保存的分辨率。
    * `facecolor/edgecolor`：`figure rectangle`的背景色和边线颜色
    * `orientation`：可以为`'landscape' | 'portrait'`
    * `format`：图片格式。可以为`'png'/'pdf'/'svg'/'eps'...`
    * `transparent`：如果为`True`，设置`figure`和`axes`背景透明（除非你设置了`facecolor/edgecolor`）
    * `frameon`：如果为`False`，则图形背景透明

14. `sca(a)`：设置`a`为`current axes`并返回它

15. `set_dpi/set_edgecolor...`：设置相关属性

16. `show(warn=True)`：显示图像。如果`warn=True`，则开启警报

17. `subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=None, hspace=None)`：调整`subplot`的位置。

18. `suptitle(t, **kwargs)`:设置图像标题。`t`为标题字符串。关键字参数就是`Text`对象的参数：

    * `x`：在图形坐标系中，标题的横坐标（范围 0～1）
    * `y`：在图形坐标系中，标题的纵坐标（范围 0～1）
    * `horizontalalignment`：标题水平对齐方式，默认为`'center'`
    * `verticalalignment`：标题垂直对齐方式，默认为`'top'`
    * `fontsize`：字体大小

19. `text(x, y, s, *args, **kwargs)`：添加文本。

    * `x`：在图形坐标系中，标题的横坐标（范围 0～1）
    * `y`：在图形坐标系中，标题的纵坐标（范围 0～1）
    * `s`：文本字符串

20. `tight_layout(renderer=None, pad=1.08, h_pad=None, w_pad=None, rect=None)`：调整`subplot`的间距。

    * `pad`：设定`subplot`和`figure edge`之间的距离。单位为`font-size`
    * `h_pad/w_pad`：`subplot`之间的高距/宽距。


#### b. Axes类

1. `Axes`类是`matplotlib`的核心，你在大多数时间都是在与它打交道。`Axes`代表了`plotting area`。大量的用于绘图的`Artist`存放在它内部，并且它有许多辅助方法来创建和添加`Artist`给它自己，而且它也有许多赋值方法来访问和修改这些`Artist`。

它有许多方法用于绘图，如`.plot()`、`.text()`、`.hist()`、`.imshow()`等方法用于创建大多数常见的`primitive`(如`Line2D`，`Rectangle`，`Text`，`Image`等等）。这些方法会创建`primitive Artist`实例，并且添加这些实例到对应的`container`上去，然后必要的时候会绘制这些图形。

2. `Subplot`就是一个特殊的`Axes`，其实例是位于网格中某个区域的`Subplot`实例。其实你也可以在任意区域创建`Axes`，通过`Figure.add_axes([left,bottom,width,height])`来创建一个任意区域的`Axes`，其中`left,bottom,width,height`都是[0--1]之间的浮点数，他们代表了相对于`Figure`的坐标。

![Axes类](./../imgs/Axes.JPG)

3. `Axes`包含了一个`.patch`属性，对于笛卡尔坐标系而言，它是一个`Rectangle`；对于极坐标而言，它是一个`Circle`。这个`.patch`属性决定了`plotting region`的形状、背景和边框。

![Axes背景](./../imgs/Axes_patch.JPG)

4. 当调用`Axes.plot()`方法时，该方法会创建一个`matplotlib.lines.Line2D`实例，然后会利用传给`.plot()`的关键字参数来更新该`Line2D`的属性，然后将这个`Line2D`添加到`Axes.lines`列表中。该方法返回的刚创建的`Line2D`列表，因为你可以传递多个`(x,y)`值从而创建多个`Line2D`。

当调用`Axes.hist()`方法时，类似于`.plot()`方法，不过它会添加`patches`到`Axes.patches`列表。

![Axe绘图方法](./../imgs/Axes_plot_method.JPG)

5. 你不应该直接通过`Axes.lines`和`Axes.patches`列表来添加图表。因为当你通过`.plot()`和`.hist()`等方法添加图表时，`matplotlib`会做许多工作而不仅仅是添加绘图组件到`Axes.lines`或者`Axes.patches`列表中。

但是你可以使用`Axes`的辅助方法`.add_line()`和`.add_patch()`方法来添加。

![Axe手动添加绘图组件](./../imgs/Axes_add_plots.JPG)

6. 下面是`Axes`用于创建`primitive Artist`以及添加他们到相应的`container`中的方法：

    * `ax.annotate()`：创建`text annotation`（`Annotate`对象），然后添加到`ax.texts`列表中。
    * `ax.bar()`：创建`bar chart`（`Rectangle`对象），然后添加到`ax.patches`列表中。
    * `ax.errorbar()`：创建`error bar plot`（`Line2D`对象和`Rectangle`对象），然后添加到`ax.lines` 列表中和`ax.patches`列表中。
    * `ax.fill()`：创建`shared area`（`Polygon`对象），然后添加到`ax.patches`列表中
    * `ax.hist()`：创建`histogram`（`Rectangle`对象），然后添加到`ax.patches`列表中。
    * `ax.imshow()`：创建`image data`（`AxesImage`对象），然后添加到`ax.images`列表中。
    * `ax.legend()`：创建`axes legends`（`Legend`对象），然后添加到`ax.legends`列表中。
    * `ax.plot()`：创建`xy plot`（`Line2D`对象），然后添加到`ax.lines`列表中。
    * `ax.scatter()`：创建`scatter charts`（`PolygonCollection`对象），然后添加到 `ax.collections`列表中。
    * `ax.text()`：创建`text`（`Text`对象），然后添加到`ax.texts`列表中。

7. 另外`Axes`还包含两个最重要的`Artist container`：

    * `ax.xaxis`：`XAxis`对象的实例，用于处理`x`轴`tick`以及`label`的绘制
    * `ax.yaxis`：`YAxis`对象的实例，用于处理`y`轴`tick`以及`label`的绘制

`Axes`包含了许多辅助方法来访问和修改`XAxis`和`YAxis`，这些辅助方法其实内部调用的是`XAxis`和`YAxis`的方法。因此通常情况下你不需要直接调用`XAxis`和`YAxis`的方法。

![Axe坐标轴](./../imgs/Axes_axis.JPG)


##### 1>. Axes 的一些方法

1. `acorr(x, **kwargs)`：绘制序列`x`的自相关。

    * `x`：一个标量序列。对`x`执行自相关
    * `normed`：一个布尔值，如果为`True`，则对数据正则化处理
    * `maxlags`：一个整数，默认为10.它给出了要展示多少个`lag`。如果为`None`，则使用所有的`2*len(x)-1`个
    * 其他`kwargs`：控制了`Line2D`的属性

返回： `(lags,c,lin,b)`

    * `lags`：是一个长度为`2*maxlags+`的`lag vector`
    * `c`：是长度为`2*maxlags+`的自相关向量
    * `line`：是一个`Line2D`实例
    * `b`：是`x-axis` ![acorr](./../imgs/acorr.JPG)

2. `add_artist(a)`：添加`a`（一个`Artist`对象）到`axes`上

3. `add_collection(collection, autolim=True)`：添加`Collection`实例到`axes`上

4. `add_container(container)`：添加`Container`实例到`axes`上

5. `add_image(image)`：添加`Image`实例到`axes`上

6. `add_line(line)`：添加`Line2D`实例到`axes`上

7. `add_patch(p)`：添加`Patch`实例到`axes`上

8. `add_table(tab)`：添加`Table`实例到`axes`上

9. `annotate(*args, **kwargs)`：对坐标点`(x,y)`绘制注解。

    * `s`：注解字符串

    * `xy`：一个长度为2的序列，给出了坐标点的`(x,y)`坐标

    * `xytext`：一个长度为2的序列，给出了注解字符串的`(x,y)`坐标

    * `xycoords`：给出了坐标点的`(x,y)`所对应的坐标系。可以为`'figure points'`、 `'figure pixels'`、`'figure fraction'`、`'axes points'`、 `'axes pixels'`、`'axes fraction'`、`'data'`。其中`figure`表示`Figure`坐标系，`axes`表示`Axes`坐标系，`data`表示被注解的点所在的数据坐标系。`points`表示单位为点（分辨率的点）；`pixels`表示单位为像素，`fraction`表示：(0,0) 为左下角，(1,1) 为右上角

    * `textcoords`：给出了注解字符串的`(x,y)`所对应的坐标系。可以为`xycoords`允许的值之外，还可以为：

        * `'offset points'`：偏移被注解的坐标点的距离为 `(x,y)`个点（分辨率的点）
        * `'offset pixels'`：偏移被注解的坐标点的距离为 `(x,y)`个像素

    * `arrowprops`：一个字典，给出了箭头的类型。

        * 若字典不包含`arrowstyle`，则可以使用下面的键： `width/headwidth/headlength/shrink`以及其他的`FancyArrowPatch`的属性。
        * 如果字典包含了`arrowstyle`，则上面的这些键将被屏蔽。`arrowstyle`的值可以为： `'-'`、`'->'`、`'-['`、`'|-|'`、`'-|>'`、`'<-'`、`'<->'`、 `'<|-'`、`'<|-|>'`、`'fancy'`、`'simple'`、`'wedge'`

    * `annotation_clip`：一个布尔值。如果为`True`，则超出`axes`的部分将会不可见


![annotate](./../imgs/annotate.JPG)

10. `autoscale_view(tight=None, scalex=True, scaley=True)`：自动调整坐标轴的范围。如果你不想自动调整`x`轴，则`scalex=False`即可。`y`轴类似。

11. `arrow(x, y, dx, dy, **kwargs)`：绘制箭头。箭头起点为 `(x,y)`，终点为 `(x+dx,y+dy)`。你也可以使用`annotate()`来模拟本方法。

    * `x,y`：箭头起点坐标（`data`坐标系）
    * `dxx,dy`：箭头终点坐标为 `(x+dx,y+dy)`（`data`坐标系）
    * `width`：箭头宽度
    * `length_includes_head:`：如果为`True`，则箭头的头部也算在箭头长度内
    * `head_width`：箭头的头部宽度
    * `head_length`：箭头的头部长度
    * `shape`：可以为`'full'/'left'/'right'`。确定是绘制左半边/右半边还是全部画出
    * 其他参数控制了`Patch`的属性

![arrow](./../imgs/arrow.JPG)

12. `axhline(y=0, xmin=0, xmax=1, **kwargs)`：绘制水平线。

    * `y`：一个标量，默认为 0.给出了水平的 `y`坐标（采用`data`坐标系）
    * `xmin`：一个标量，默认为 0。给出了水平线的起始横坐标。最大为 1（表示最右侧）（使用`Axes`坐标系）
    * `xmax`：一个标量，默认为 1。 给出了水平线的终点横坐标。最小为 0 （表示最左侧）（使用`Axes`坐标系）
    * 其他关键字参数控制`Line2D`的属性

![axhline](./../imgs/axhline.JPG)

13. `axhspan(ymin, ymax, xmin=0, xmax=1, **kwargs)`：绘制水平区域。

    * `ymin/ymax`：给出了水平区域的`y`坐标的下界和上界，采用`data`坐标系
    * `xmin/xmax`：给出了水平区域的左侧和右侧的位置。采用`Axes`坐标系，最小为0，最大为 1
    * 其他关键字参数控制`Line2D`的属性

![axhspan](./../imgs/axhspan.JPG)

14. `axis(*v, **kwargs)`：设置`axis`属性，它返回的是`(xmin,xmax,ymin,ymax)`。`data`坐标系下每个轴的最小值、最大值。

    * `v`： Axis data limits set from a float list。也可以是字符串：

        * `'on'`：Toggle axis lines and labels on
        * `'off'`：Toggle axis lines and labels off
        * `'equal'`:Equal scaling by changing limits
        * `''tight`：Limits set such that all data is shown
        * `'auto'`:Automatic scaling, fill rectangle with data

    * `xmin/ymin/ymax/ymax`：待设置的轴的最小/最大值


15. `axvline(x=0, ymin=0, ymax=1, **kwargs)`：绘制垂直线。

    * `x`：一个标量，默认为 0.给出了垂直线的 `x`坐标（采用`data`坐标系）
    * `ymin`：一个标量，默认为 0。给出了垂直线的起始纵坐标。最大为 1（表示最上侧）（使用`Axes`坐标系）
    * `ymax`：一个标量，默认为 1。 给出了垂直线的终点纵坐标。最小为 0 （表示最下侧）（使用`Axes`坐标系）
    * 其他关键字参数控制`Line2D`的属性

![axvline](./../imgs/axvline.JPG)

16. `axvspan(xmin, xmax, ymin=0, ymax=1, **kwargs)`：绘制垂直区域。

    * `xmin/xmax`：给出了垂直区域的`x`坐标的左侧和右侧，采用`data`坐标系
    * `ymin/ymax`：给出了垂直区域的上侧和下侧的位置。采用`Axes`坐标系，最小为0，最大为 1
    * 其他关键字参数控制`Line2D`的属性

![axvspan](./../imgs/axvspan.JPG)

17. `bar(left, height, width=0.8, bottom=None, **kwargs)`：绘制一个`bar`。

    * `left`：一个标量或者标量的序列，`bar`的左侧的`x`坐标，采用`data`坐标系
    * `height`：一个标量或者标量的序列，`bar`的高度，采用`data`坐标系
    * `width`：一个标量或者标量的序列，`bar`的宽度，默认为 0.8，采用`data`坐标系
    * `bottom`：一个标量或者标量的序列，`bar`的底部的`y`坐标，默认为 0，采用`data`坐标系
    * `color`：一个标量或者标量的序列，`bar`的背景色
    * `edgecolor`：一个标量或者标量的序列，`bar`的边色颜色
    * `linewidth`：一个标量或者标量的序列，`bar`的边的线宽
    * `tick_label`：一个字符串或者字符串的序列，给出了`bar`的`label`
    * `xerr`：一个标量或者标量的序列，用于设置`bar`的`errorbar`。（水平方向的小横线）
    * `yerr`：一个标量或者标量的序列，用于设置`bar`的`errorbar`（垂直方向的小横线）
    * `ecolor`：一个标量或者标量的序列，用于设置`errorbar`。
    * `capsize`：一个标量，用于设置`errorbar`。小横线头部的一个小短线
    * `error_kw`：一个字典，用于设置`errorbar`。如`ecolor/capsize`关键字
    * `align`：一个字符串，设定`bar`的对齐方式。可以为`'edge'`或者`'center'`。柱子的左边跟`x=left`线对齐，还是柱子的中线跟`x=left`线对齐。
    * `orientation`：一个字符串，指定`bar`的方向。可以为`'vertical'`或者`'horizontal'`。它决定了`errbar`和`label`放置的位置。
    * `log`：一个布尔值，如果为`True`，则设置`axis`为对数坐标

返回`matplotlib.container.BarContainer`.

你可以一次添加多个`bar`，此时就是上述的“标量的序列”。 ![bar](./../imgs/bar.JPG)

18. `barh(bottom, width, height=0.8, left=None, **kwargs)`：绘制水平的`bar`

    * `bottom`：一个标量或者标量的序列，`bar`的底部的`y`坐标，默认为 0，采用`data`坐标系
    * `width`：一个标量或者标量的序列，`bar`的宽度，默认为 0.8，采用`data`坐标系<br></br>
    * `height`：一个标量或者标量的序列，`bar`的高度，采用`data`坐标系
    * `left`：一个标量或者标量的序列，`bar`的左侧的`x`坐标，采用`data`坐标系
    * 其他参数参考 `bar`方法

它就是`bar(orientation='horizontal')`。

![barh](./../imgs/barh.JPG)

19. `cla()/clear()`：清除`Axes`

20. `clabel(CS, *args, **kwargs)`：为等高线添加`label`。

    * `CS`：由`contour`函数返回的`ContourSet`，代表一组等高线
    * `fontsize`：`label`的字体大小，或者给出字符串`'smaller'/'x-large'`
    * `colors`：如果为`None`，则使用对应的等高线的颜色。如果为一个字符串指定的颜色，则所有的等高线`label`使用该颜色。如果为一组颜色，则不同的等高线的`label`按顺序使用其中的不同的颜色。
    * `inline`：一个布尔值。如果为`True`，则移除`label`覆盖的底层的等高线（嵌入式）；否则就全部绘制（重叠式）
    * `inline_spacing`:一个浮点数，单位为像素点。它控制了`label`距离等高线的距离

![clabel](./../imgs/clabel.JPG)

21. `contour(*args, **kwargs)`：绘制等高线。它返回一个`QuadContourSet`对象 最常用的四种方式：

    * `contour(Z)`：其中 `Z`为二维数组。数据坐标系下的坐标点 `(i,j)`对应了`Z[j,i]`（`x`轴对应列，`y`轴对应行）。该方法随机挑选一些等高线绘制。

    * `contour(X,Y,Z)`：其中 `X/Y/Z`均为二维数组，且形状相同。对应位置的横坐标由 `X`提供，纵坐标由 `Y`提供，值由 `Z` 提供。该方法随机挑选一些等高线绘制。

    >     > 

    > `X`和`Y`也可以同时是一维数组，且`len(X)`是`Z`的列数，`len(Y)`是`Z`的行数。



    * `contour(Z,N)/contour(X,Y,Z,N)`：`N`为一个整数，表示绘制`N`条等高线。该方法随机挑选`N`条等高线绘制。

    * `contour(Z,V)/contour(X,Y,Z,V)`：`V`为一个递增的序列，表示绘制那些值位于`V`中的等高线


![contour](./../imgs/contour.JPG) ![contour](./../imgs/contour.png)

其他关键字参数：

    * `colors`：如果为`None`，则由`cmap`给出。如果是一个字符串，这所有的等高线由字符串指定的颜色给出。如果是一个序列，该序列中每个都代表了一个颜色，则等高线的颜色依次由该序列给出。

    * `cmap`：一个`Colormap`对象。如果为`None`，则默认的`Colormap`将被使用

    * `levels`：一个序列（升序排列）。指定了要绘制等高线值位于`levels`的等高线。

    * `origin`：参考`Axes.imshow`中的该参数设置。

    * `extent`：它是一个元组`(x0,x1,y0,y1)`。如果给出了`(X,Y)`，则该参数无效。如果未给出`(X,Y)`：

        * 如果`origin`非`None`，则它给出了外边界， `Z[0,0]`位于图形中间
        * 如果`origin`为`None`，则`(x0,y0)`对应`Z[0,0]`；`(x1,y1)`对应`Z[-1.-1]`，等价于同时使用了`set_xlim(left,right)+set_ylim(bottom,top)`

    * `antialiased`：一个布尔值，用于开启/关闭反走样

    * `linewidths`：如果为`None`，则使用默认值。如果为一个整数，则所有的等高线都是用该线宽。如果为一个整数序列，则等高线依次使用它指定的线宽。只有`contour`适用

    * `linestyles`：如果为`None`，则使用默认的实线。你也可以指定为`'solid'/'dashed'/'dashdot'/'dotted'`。你可以指定搜有的等高线使用一种线型，也可以使用一个线型序列。只有`contour`适用


22. `contourf(*args, **kwargs)`：它绘制的是带填充的等高线。其参数和用法基本和`contour`相同。它返回一个`QuadContourSet`对象

    * `contourf(Z,V)/contourf(X,Y,Z,V)`：`V`是递增的序列，指定了等高线的值。该方法会填充`V`中相邻两个等高线之间的区域
    * `contourf`不同与`contour`的关键字参数为`hatches`：它指定了填充区域的填充类型（如以小斜线填充）。如果为`None`，则无任何`hatch`。它典型值为`hatches=['.', '/', '\', None, '\\', '*','-',]`
    * `contourf`填充的是半开半闭区间`(z1,z2]`

![contourf](./../imgs/contourf.png)

23. `errorbar(x, y, yerr=None, xerr=None, fmt='', ecolor=None, elinewidth=None,` `capsize=None, barsabove=False, lolims=False, uplims=False, xlolims=False,` `xuplims=False, errorevery=1, capthick=None, **kwargs)`：绘制`errorbar`，返回`(plotline, caplines, barlinecols)`

    * `x`：一个序列，指定`x`坐标
    * `y`:一个序列，指定`y`坐标。即： `y=f(x)`
    * `yerr`：指定`y`的`error`。如果为标量，则每个点都是相同的`error`；如果为一维向量，则依次给出了每个点的`error`。如果是个二维向量，则依次给出了每个点的上`error`和下`error`
    * `xerr`：指定`x`的`error`。如果为标量，则每个点都是相同的`error`；如果为一维向量，则依次给出了每个点的`error`。如果是个二维向量，则依次给出了每个点的左`error`和右`error`
    * `fmt`：可以为空字符串，或者`'none'`或者其他的`plot format string`。如果是`'none'`则只有`errorbars`能够被绘制
    * `ecolor`：指定了`errorbar`的颜色
    * `elinewidth`：指定了`errorbar`的线宽<br></br>
    * `capsize`：指定了`errorbar`头部的小横线的宽度
    * `errorevery`：一个整数。如果为 4， 则每隔 4个点才绘制一个`errorbar`
    * 其他的关键字参数都是用于指定`marker`的类型。如： `marker='s', mfc='red', mec='green', ms=20, mew=4`。他们是`markderfacecolor,markeredgecolor,markdersize,markderedgewidth`的缩写。

![errorbar](./../imgs/errorbar.JPG)

24. `eventplot(positions, orientation='horizontal', lineoffsets=1, linelengths=1,` `linewidths=None, colors=None, linestyles='solid', **kwargs)` ：绘制时间线。时间线就是在指定位置上并排的一系列线段。返回 `matplotlib.collections.EventCollection`的一个列表

    * `positions`：一个一维或者二维的数组。每一行代表了一组直线
    * `orientation`：可以为`'horizonal'|'vertical'`，代表了摆放时间线的方式。如果是水平走向的，则垂直摆放直线；如果是垂直走向的，则水平放置直线
    * `lineoffsets`：一个浮点数或者浮点数的序列，指定了时间线中轴距离`y=0`的偏离值
    * `linelengths`：一个浮点数或者浮点数的序列，指定了线的长度
    * `linewidths`：一个浮点数或者浮点数的序列，指定了线的宽度
    * `colors`：一个颜色或者一组颜色，指定了线的颜色。颜色可以为颜色字符串，或者一个`RGB`元组。
    * `linestyles`：一个线型或者一组线型，指定了线型。线型在`'solid' | 'dashed' | 'dashdot' | 'dotted'`四者之一

如果`positions`是一个一维数组，表示绘制一组时间线。那么`lineoffsets/linelengths/linewidths/colors/linestyles`都是标量值，指定该组时间线的格式。如果`positions`是一个二维数组则，有多少行，就有多少组时间线。制定时间线格式的这些参数都是序列，序列长度就是`positions`的行数。

![eventplot](./../imgs/eventplot.JPG)

25. `fill(*args, **kwargs)`：绘制多边形。返回一个`Patch`列表。其常用的方式为：

    * 绘制一个多边形： `fill(x,y,'b')`，其中`x`为多边形的边上的点的`x`坐标；`y`为多边形的边上的点的`y`坐标。`'b'`为多边形的填充颜色。

    * 绘制多个多边形： `fill(x1,y1,'b',x2,y2,'r')`。这里指定多个`x,y,color`就可以。

    * `closed`关键字参数：一个布尔值，确定是否封闭多边形（即多一条从起点到终点的边）。默认为`True`

    * `plot()`支持的`color string`在这里也被支持

    * 剩下的关键字参数用于控制`Polygon`的属性。如

        * `hatch`：一个字符串，指定填充方式，如`['/' | '\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*']`
        * `label`：一个字符串，指定标签
        * `fill`：一个布尔值，决定是否填充
        * `facecolor/edgecolor/color`：颜色


![fill](./../imgs/fill.JPG)

26. `fill_between(x, y1, y2=0, where=None, interpolate=False, step=None, **kwargs)`：绘制填充区域。它填充两个曲线之间的部分。它返回一个`PolyCollection`对象。

    * `x`：一个序列，指定`x`坐标
    * `y1`：第一条曲线的纵坐标。如果为标量，说明该曲线为水平线。
    * `y2`：第二条曲线的纵坐标。如果为标量，说明该曲线为水平线。
    * `where`：指定填充哪里。如果为`None`，则填充两条曲线之间的所有区域，这是默认值。如果非`None`，则他是一个一维布尔数组，长度与`x`相同。只有为`True`对应的`x`处才被填充。
    * `interpolate`：一个布尔值。如果`True`，则进行插值计算来寻找两个曲线的交点。如果为`False`，则不进行插值。
    * `step`：可以为`'pre'/'post'/'mid'`或者`None`，设定填充区域的边界的形状。 ![fill_between](./../imgs/fill_between.JPG)

27. `fill_betweenx(y, x1, x2=0, where=None, step=None, **kwargs)`：绘制填充区域。该区域是以`y`为自变量，`x`为函数的两条曲线合围而成。它返回一个`PolyCollection`对象。

    * `y`：一个序列，为纵坐标
    * `x1`：第一个曲线的`x`坐标。它是一个反函数，即以`y`为自变量
    * `x2`：第二个曲线的`y`坐标。它也是一个反函数
    * `where`：指定填充哪里。如果为`None`，则填充两条曲线之间的所有区域，这是默认值。如果非`None`，则他是一个一维布尔数组，长度与`y`相同。只有为`True`对应的`y`处才被填充。
    * `step`：可以为`'pre'/'post'/'mid'`或者`None`，设定填充区域的边界的形状。

通常建议提供一个`alpha`参数，用于设定填充的透明度。如果同一个区域被多个`fill_between()`填充，那么设定`alpha`之后会让每一层都能显示出来。<br></br>

> > 

> `fill_between`沿着`x`轴填充；`fill_betweenx`沿着`y`轴填充



![fillbetweenx](./../imgs/fillbetweenx.JPG)

28. `findobj(match=None, include_self=True)`：筛选出合适的`artist`对象，返回一个列表。他会递归的向下搜寻

    * `match`指定过滤器。

        * 如果为`None`，则它选出`axes`包含的所有`artist`
        * 如果为一个函数，则函数接受一个`artist`参数，返回布尔值。所有返回`True`的`artist`被选中
        * 如果是一个类，则返回属于该类的`artist`

    * `include_self`：如果为`True`，则也检查自己


29. `get_xx`函数：返回对应的属性值。有： `get_alpha/get_anchor/get_animated/get_aspect/get_axis_bgcolor/` `get_axisbelow/get_clip_box/get_clip_path/get_frame_on/get_gid` `get_label/get_legend/get_lines/get_title/get_transform/get_visible` `get_xaxis/get_xlabel/get_xlim/get_xscale/get_xticklabels/get_yaxis...`

30. `grid(b=None, which='major', axis='both', **kwargs)`：开启关闭网格。

    * `b`为布尔值，指定你想开启(`True`)还是关闭网格
    * `which`：可以为`'major'/'minor'/'both'`，指定你想开启哪个级别的网格
    * `axis`：可以为`'x'/'y'/'both'`，指定你想在那个轴上开启网格
    * 其他的关键字参数设定了网格的线条类型。如`color/linestype/linewidth`

还有一种简单用法，就是`axes.grid()`，此时表示：如果网格开启，则关闭。如果网格关闭，则开启。

31. `hexbin(x, y, C=None, gridsize=100, bins=None, xscale='linear', yscale='linear',` `extent=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None,` `edgecolors='none', reduce_C_function=<function mean>, mincnt=None,` `marginals=False, **kwargs)`：绘制`hexbin`。它用于同一个地方有很多点的情况，是六边形面元划分，是一种二元直方图。返回一个`PolyCollection`对象。

    * `x/y`：一维数组，它们形状相同。它们给出了绘制六边形面元的点。

    * `C`：如果非`None`，则它给出了坐标`(x[i],y[i])`的`count value`。它和`x`长度相同，也是一维数组

    >     > 

    > `x/y/C`也可能是`masked array`，此时只有`unmasked`的点才被绘制<br></br>



    * `reduce_C_function`：将坐标`(x[i],y[i])`的`count value`进行归并。因为同一个坐标可能被设定了多个`count value`。而每个点根据其`count value`来染色

    * `gridsize`：一个整数。它调整了六边形面元`x`方向的尺寸，`y`方向的尺寸自动选取。你也可以设定它为一个元组，同时调整`x/y`方向的尺寸。它实际上给出的是`x`轴可以放置的面元数量，因此该数值越大，六边形面元尺寸越小。

    * `bins`：

        * 如果为`None`，则每个六边形面元的颜色值直接对应了它的`count value`
        * 如果为`'log'`，则每个六边形面元的颜色值对应了它的`count value+1`的对数值
        * 如果为一个整数， divide the counts in the specified number of bins, and color the hexagons accordingly
        * 如果为一个整数序列，则the values of the lower bound of the bins to be used

    * `xscale`：可以为`'linear'/'log'`，设置了`x`轴是线性还是对数

    * `scale`：可以为`'linear'/'log'`，设置了`y`轴是线性还是对数

    * `mincnt`：一个整数或者`None`。它指定显示这一类的面元：面元包含的坐标点的数量超过`mincnt`。对于面元包含坐标点数量少于`mincnt`的，不显示。

    * `marginals`：一个布尔值。如果为`True`，则沿着坐标轴绘制密度条。

    * `extent`：一个元组`(left, right, bottom, top)`，等价于同时使用了`set_xlim(left,right)+set_ylim(bottom,top)`。

    * 剩下的参数设定颜色和面元的属性。


![hexbin](./../imgs/hexbin.JPG) ![hexbin](./../imgs/hexbin.png)

32. `hist(x, bins=10, range=None, normed=False, weights=None, cumulative=False,` `bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None,` `log=False, color=None, label=None, stacked=False, **kwargs)` ：绘制直方图。 其返回值为：

    * 如果绘制一个直方图，那么就是元组 `(n, bins, patches)`，`n`为频数/频率；`bins`为直方图的各个分界点；`patches`为每个直方图。
    * 如果绘制多个直方图，那么就是元组 `([n0, n1, ...], bins, [patches0, patches1,...])`

参数为：

    * `x`:一个序列或者一维数组，给定了直方图的数据
    * `bins`：一个整数。返回了`bins+1`个分界点，将竖着划分成等分的`bins`份。你可以传递一个序列，指定分界点，此时可以实现非等分的划分。
    * `range`：一个元组，给出了数据的上界和下界，在这之外的数据不被考虑。默认就是`(x.min(),x.max())`
    * `normed`：布尔值，如果为`True`，则返回的是数据出现的频率；否则返回的是数据出现的频数
    * `weights`：长度与`x`相同的序列，给出了每个数据的权重
    * `cumulative` ：布尔值。如果为`True`，则计算的是累积频率/频数
    * `bottom`：一个整数或者整数序列或者`None`，指定了直方图底部的纵坐标。默认为 0
    * `histtype`：直方图的类型。可以为`'bar'/'barstacked'/'step'/'stepfilled'`
    * `align`：直方图每个小矩形的对齐方式。可以为`'left'/'mid'/right'`
    * `orientation`：调整方向。可以为`'horizontal'/'vertical'`。如果为水平则，使用`barh`，同时`bottom`参数设定的是左侧的横坐标值
    * `rwidth`：一个标量值，设定了直方图每个矩形的相对于默认值的宽度。如果直方图类型为 `step/stepfilled`，则忽略该参数。
    * `log`：布尔值。如果为`True`：则`x`轴使用对数坐标
    * `color`：颜色或者颜色序列，用于给直方图指定颜色
    * `label`：字符串或者字符串序列。给直方图指定标签
    * `stacked`：一个布尔值。如果为`True`，则多个直方图会叠加在一起。
    * 其他参数设置了`Patch`的属性

![hist](./../imgs/hist.JPG) ![hist](./../imgs/hist.png)

33. `hist2d(x, y, bins=10, range=None, normed=False, weights=None, cmin=None,` `cmax=None, **kwargs)`：绘制二维直方图。其返回值为元组 `(counts, xedges, yedges, Image)`

参数为：

    * `x`:一个序列或者一维数组，给定了`x`坐标序列

    * `y`:一个序列或者一维数组，给定了`y`坐标序列

    * `bins`：

        * 如果为整数，则给出了两个维度上的区间数量
        * 如果为`int,int`序列，则分别给出了`x`区间数量和`y`区间数量
        * 如果给定了一个一维数组，则给出了 `x_edges=y_edges=bins`
        * 如果为定了`array,array`，则分别给出了`x_edges,y_edges`

    * `range`：一个`(2,2)`的数组，给出了数据的上界和下界，在这之外的数据不被考虑。默认就是`(x.min(),x.max())`

    * `normed`：布尔值，如果为`True`，则返回的是数据出现的频率；否则返回的是数据出现的频数

    * `weights`：长度与`x`相同的序列，给出了每个数据的权重

    * `cmin`：一个标量值。那些`count`值小于`cmin`的单元不被显示。同时返回的结果中，这些单元返回`nan`

    * `cmax`：一个标量值。那些`count`值大于`cmax`的单元不被显示。同时返回的结果中，这些单元返回`nan`

    * 其他参数设置了`pcolorfast()`属性


![hist2d](./../imgs/hist2d.JPG)

34. `hlines(y, xmin, xmax, colors='k', linestyles='solid', label='', **kwargs)`：从`xmin`到`xmax`绘制一系列的水平线。这些水平线的纵坐标由`y`提供。

    * `y`：水平线的纵坐标。如果为标量，则为一条水平；如果为序列，则为一系列水平线。数据坐标系
    * `xmin/xmax`：水平线的起点和终点的横坐标。如果是个标量，则所有的水平线公用。如果是序列，则每个水平线设置一个。数据坐标系
    * `linestyles`：指定线型。可以为一个字符串（所有水平线公用），或者字符串序列（每个水平线一个）。线型在`'solid' | 'dashed' | 'dashdot' | 'dotted'`四者之一
    * `colors`：指定颜色。可以为一个颜色（所有水平线公用），或者颜色序列（每个水平线一个）。
    * `label`：一个字符串，指定标签。
    * 其他关键字参数设置`LineCollection`属性。

![hlines](./../imgs/hlines.JPG)

35. `imshow(X, cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, vmin=None,` `vmax=None, origin=None, extent=None, shape=None, filternorm=1, filterrad=4.0, imlim=None,` `resample=None, url=None, **kwargs)`：绘制图片。返回一个`AxesImage`对象

    * `X`：包含了图片的数据。其形状可以为：

        * `(n,m)`（灰度图），类型为`float`
        * `(n,m,3)`（`RGB`图），类型为`float`（此时每个元素的值都在 0 和 1.0 之间），或者`unit8`
        * `(n,m,4)`（`RGBA`图），类型为`float`（此时每个元素的值都在 0 和 1.0 之间），或者`unit8`

    * `cmap`：一个`Colormap`实例。默认由`rc`的`image.cmap`指定。如果`X`是`RGB/RGBA`，则忽略该参数

    * `aspect`：一个字符串，指定图片的缩放。可以为：

        * `'auto'`：缩放图片的宽高比，是的它匹配`axes`
        * `'equal'`：当`extent`参数为`None`时，修改`axes`的宽高比，使得它匹配图片；如果`extent`参数不是`None`，则修改`axes`的宽高比来匹配`extent`
        * `None`：默认由`rc`的`image.aspect`指定

    * `interpolation`：一个字符串，指定插值方式。可以为`'none', 'nearest', 'bilinear', 'bicubic',` `'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom',` `'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos'`

    * `norm`：一个`Normalize`实例，用于将图片亮度正则化到 `0~1`。如果为`None`，则采用`normalize.norm`

    * `vmin/vmax`：用于辅助`norm`进行正则化。如果你传入了一个`norm`实例，则该参数忽略

    * `alpha`：浮点数，指定透明度

    * `origin`：可以为`'upper'/'lower'`。图片的第一个像素`X[0,0]`放置在坐标原点。

        * `'upper'`：横坐标向右，纵坐标向下
        * `'lower'`：横坐标向右，纵坐标向上

    * `extent`：一个元组`(left, right, bottom, top)`，等价于同时使用了`set_xlim(left,right)+set_ylim(bottom,top)`

    * `shape`：一个元组`(column,rows)`，用于`rar buffer image`

    * `filternorm/filterrad`：用于过滤

    * 其他参数用于调整 `Artist`属性


![imshow](./../imgs/imshow.JPG) ![imshow](./../imgs/imshow.png)

36. `legend(*args, **kwargs)`：创建一个图例。

    * 最简单的方式：你首先创建一个`Axes`，然后在其中添加`lines`，然后直接调用`ax.legend()`即可。此时那些`label`非空的线将被图例注释

    * 你也可以采用下面面向对象的方案：线创建`line`，然后调用`line.set_label()`，然后调用`ax.legend()`。此时的逻辑更清晰

    * 如果你不想让某个`line`被图例注释，则它的`label`要么为空字符串，要么为以下划线开始。

    * 还有一种直接控制图例的方式：它直接显式指定了被注释的`line`和对应的`label`

    ```
xxxxxxxxxxax.legend((line1,line2,line3),('label1','label2','label3'))
    ```

    关键字参数：

    * `loc`：指定了图例的位置。可以为整数或者字符串。可以是字符串`'best'`/`'upper right'`/`'upper left'` /`'lower left'`/`'lower right'`/`'right'`/`'center left'`/`'center right'` /`'lower center'`/`'upper center'`/`'center'`，对应于整数的 `0~10`。你也可以指定坐标`(x,y)`，其中`(0,0)`是左下角，`(1,1)`是右上角

    * `ncol`：一个整数，指定图例中有几列，默认为 1列

    * `prop`：一个字典，或者`FontProperties`实例，可以指定图例中的字体属性。

    * `fontsize`：控制字体大小，可以为整数、浮点数（指定字体绝对大小），或者字符串 `'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'`

    * `numpoint`/`scatterpoints`：图例上每个图例线的点数

    * `fancybox`：如果为`True`，图例的边框采用圆角矩形

    * `framealpha`：一个浮点数，从0到 1，图例的透明度

    * `frameon`：一个布尔值，如果为`True`，则绘制图例的背景框。否则不绘制。

    * `shadow`：如果为`True`，图例添加背影

    * `ncol`：列数

    * `title`：图例的标题


![legend](./../imgs/legend.JPG) ![legend](./../imgs/legend.png)

37. `locator_params(axis='both', tight=None, **kwargs)`：控制`tick locator`

    * `axis`：一个字符串，指定控制那个轴。可以为`'x'/'y'/'both'`。
    * `tight`：一个布尔值。它传递给`autoscale_view()`
    * 其他关键字参数传递给`set_params()`方法

如果你想调整主轴上的刻度线的数量，可以使用`ax.locator_params(tight=True,nbins=4)`

![locator_params](./../imgs/locator_params.JPG)

38. `loglog(*args, **kwargs)`：绘制`line`，但是将`x`轴和`y`轴都调整为对数坐标

    * `x`：数据的`x`坐标
    * `y`：数据的`y`坐标
    * `basex/basey`：一个大于 1 的标量，控制对数的底数
    * `subsx/subsy`：一个序列，给出了`x/y`轴的子刻度的位置（数据坐标系）。默认为`None`，此时子刻度是自动划分的
    * `nonposx/nonposy`：如果为`'mask'`，则`x/y`的负数或者零将被视作无效的数；如果为`'clip'`，则`x/y`的负数或者零将被视作一个非常小的正数（因为对数的自变量要大于零）
    * 剩下的参数将被作为`Line2D`的属性

39. `margins(*args, **kw)`：设置`Axes`的`margin`。你可以通过`ax.margins()`获取当前的`margin`。 你也可以通过`ax.margins(x=xmargin,y=ymargin)`来设置`margin`。这两个参数的值是 `0～1` ![margins](./../imgs/margins.JPG)

40. `matshow(Z, **kwargs)`：将一个矩阵绘制成图片。

    * `Z`：一个形状为`(n,m)`的数组
    * 其他参数见`imshow`

![matshow](./../imgs/matshow.JPG)

41. `minorticks_off()`：关闭次刻度线。`minorticks_on()`：打开次刻度线。

42. `pcolor(*args, **kwargs)`：绘制一个`pseudocolor plot`，返回一个`Collection`实例。对于大型数组，它很慢，此时推荐使用`pcolormesh()`。

常用的方式为： `pcolor(C,*kwargs)`，此时`C`为一个二维数组。也可以指定`pcolor(X,Y,C,*kwargs)`。`X/Y/C`都是二维数组，并且`X`和`Y`的尺寸比`C`大。它将在四个点决定的矩形中填充颜色`C[i,j]`： `(X[i, j], Y[i, j])`，`(X[i, j+1], Y[i, j+1])`， `(X[i+1, j], Y[i+1, j])`，`(X[i+1, j+1], Y[i+1, j+1])`。`X/Y`也可以是一维的，但是首先会进行广播法则。

关键字参数为：

    * `cmap`：一个`Colormap`实例。如果为`None`，则使用`rc`的设置
    * `edgecolors`：`None`或者`'none'`或者一个颜色或者一个颜色序列。用于设定边的颜色
    * 其他参数设置`PopyCollection`属性<br></br>

![pcolor](./../imgs/pcolor.JPG)

43. `pcolorfast(*args, **kwargs)`：用法和`pcolor`相同，它是一个实验性质的，提供了一个更快的实现。

44. `pcolormesh(*args, **kwargs)`：作用和`pcolor`相同。但是它是另一个实现方式，并且返回不同的对象，它返回的是`QuadMesh`对象。它的速度更快。其参数和用法与`pcolor`相同。

    * `edgecolors`：除了`pcolor`的`edgecolors`之外，还多了一个`'face'`，表示使用与四边形背景色相同的颜色。

![pcolormesh](./../imgs/pcolormesh.JPG)

45. `pie(x, explode=None, labels=None, colors=None, autopct=None, pctdistance=0.6,` `shadow=False, labeldistance=1.1, startangle=None, radius=None, counterclock=True,` `wedgeprops=None, textprops=None, center=(0, 0), frame=False)`：绘制饼状图。

    * `x`：数据序列。每一块饼的权重为`x/sum(x)`；如果`sum(x)<=1`，则`x`已经代表了每一块饼的权重，此时并不会除以`sum(x)`。饼状图从`x`轴开始，逆时针绘制。
    * `explode`：如果不是`None`，则它给出了每个饼的径向偏移量。该偏移量表示：径向偏移除以半径。
    * `colors`：给出了每一块饼的颜色。可以为`None`或者颜色序列
    * `labels`：给出了每个饼的字符串标签。可以为`None`或者字符串序列
    * `autopct`：它可以为一个字符串，可以指定每个饼的数值标签，但是该字符串是 `fmt%pct`，通过`pct`参数格式化，`pct`为饼的比重（自动提供）。也可以是一个可调用对象。
    * `pctdistance`：若`autopct`为`None`，则忽略之。否则就是数值标签的径向距离，它是个相对距离，相对于半径。
    * `labeldistance`：控制了饼的字符串标签的径向距离，它是个相对距离，相对于半径。
    * `shadow`：一个布尔值，如果为`True`，则绘制带阴影的饼状图
    * `startangle`：如果不是`None`，则它可控制了第一块饼与`x`轴的夹角
    * `radius`：一个标量，控制了饼状图的半径。如果为`None`，则默认为 1
    * `counterclock`：一个布尔值。如果为`True`，则为逆时针方向；否则为顺时针排列
    * `wedgeprops`：一个字典，控制了每一块饼的某些属性，如线型
    * `textprops`：一个字典，控制了饼的文字的一些属性
    * `center`：一个二元的元组，指定了饼状图的中心
    * `frame`：一个布尔值，控制是否绘制`axes frame`（也就是背后的数轴）。发现版本`1.5.3`中，开启它是个`Bug`，图形混乱。

为了显示好看，建议使用`ax.set_aspect(1)`将`Axes`的长宽比设置为 1， 此时的饼状图是个圆形（否则为椭圆）。

![pie](./../imgs/pie.JPG) ![pie](./../imgs/pie.png)

46. `plot(*args, **kwargs)`：绘制`line`或者`marker`。他返回`line`的列表。

最简单的用法是：`plot(x,y)`，其中`x`为数据点的横坐标，`y`为数据点的纵坐标。此时采用默认的线型和颜色。

    * 你也可以设置线型和颜色为 `plot(x,y,'bo')`：`'b'`代表颜色为蓝色，`'o'`代表使用小圆圈标记数据点。`'bo'`称作`plot format string`
    * 你也可以省略`x`：`plot(y)`。此时隐含着`x`等于`[0,1,...len(y-1)]`
    * 如果`x/y`为二维数组，那么每一行作为一组`line`来绘制
    * 如果你想一次绘制多条线，可以用`plot(x1,y1,'b+',x2,y2,'b-',x3,y3,'bo')`

控制`marker`的字符串可以为：`'-'/'--'/'-.'/':'/'.'/','/'o'/'v'/'^'/'<'/'>'/'1'/'2'/'3'/'4'/` `'s'/'p'/'*'/'h'/'H'/'+'/'x'/'D'/'d'/'|'/'_'`

控制颜色的字符串可以为： `'b'/'g'/'r'/'c'/'m'/'y'/'k'/'w'`；你也可以指定它们的全名，如`'red'`；或者指定十六进制字符串`'#00ff00`；或者指定一个`RGB/RGBA`元组： `(0,1,0)/(0,1,0,1)`。

默认情况下，不同的线采用不同的线型，它由`rc`的`axes.prop_cycle`参数控制，并且是循环使用。这些参数都可以单独地作为关键字参数来设置。如果一个`plot`绘制了多条线，则其参数对所有的线起作用。这些关键字全部用于设定`Line2D`的属性。

![plot](./../imgs/plot.JPG) ![plot](./../imgs/plot.png)

47. `plot_date(x, y, fmt='o', tz=None, xdate=True, ydate=False, **kwargs)`：绘制日期相关的数据。它类似于`plot()`方法，但是`plot_data`的`x`轴或者`y`轴可能是日期相关的数据。

    * `x/y`：待绘制的点的坐标序列。如果是日期序列，则代表了从 `0001-01-01 UTC`以来的天数（浮点数）（它映射到整数 1）。日期必须大于等于 0（1代表第一天），且日期跨度大于一个月（31天）
    * `fmt`：`plot format string`，如`bo`
    * `tz`：指定时区。可以为时区字符串，也可以为`tzinfo`实例或者`None`
    * `xdate`：一个布尔值。如果为`True`，则`x`轴为时间序列
    * `ydate`：一个布尔值。如果为`True`，则`y`轴为时间序列
    * 其他参数用于设定`Line2D`的属性

注意：`plot_date()`使用默认的`dates.AutoDateLocator/dates.AutoDateFormatter`。如果你希望使用自定义的，则你需要在调用`plot_date()`之后调用方法来设置`date ticker/date formatter`

设置时区：

```
xxxxxxxxxx  from datetime import timezone,timedelta  ax.plot_date(X,Y,tz=timezone(+timedelta(hours=23)))
```

设置日期格式化和位置：

```
xxxxxxxxxx  from matplotlib.dates import AutoDateLocator,AutoDateFormatter,DateFormatter  autoloc = AutoDateLocator() #默认的 formatter  autofmt = AutoDateFormatter() #默认的 locator  myfmt = DateFormatter('%Y-%m-%d %H:%M:%S')#自定义的formatter,使用`strftime()`的格式化方式  ax.xaxis.set_major_locator(autodates)       #设置时间间隔  ax.xaxis.set_major_formatter(myfmt)      #设置时间显示格式
```

    * `ax.xaxis.set_major_locator()`设置`x`轴的主刻度的`locator`
    * `ax.xaxis.set_major_formatter()`设置`x`轴的主刻度的`formatter`
    * `DateFormatter`：初始化字符串的解释与`strftime()`相同
    * 常见的一些`DateLocator`有：`MinuteLocator`、`HourLocator` 、`DayLocator`、`WeekdayLocator`、`MonthLocator`、`YearLocator`、`AutoDateLocator`

![plot_date](./../imgs/plot_date.JPG)

48. `properties()`：返回一个字典，该字典中包含了`axes`中的所有属性的键值对。

49. `quiver(*args, **kw)`：创建一个二维的场向量。

常见的调用方式有： `quiver(U,V,**kw)`、 `quiver(U,V,C,**kw)`、`quiver(X,Y,U,V,C,**kw)`、`quiver(X,Y,U,V,C,**kw)`。其中 `U/V`为向量的`x`轴分量和`y`轴分量。`X/Y`为绘制向量的起点坐标。`C`用于指定每个箭头的颜色。

    * 如果为指定`X/Y`，则默认每个向量的起点从每个单元格生成。

关键字参数有：

    * `units`：一个字符串，指定箭头的单位。除了箭头的长度以外，其他的度量都是以该单位为准。可以为：

        * `'width'/'height'`：以`axes`的宽度/高度为单位
        * `'dots'/'inches'`：以像素点/英寸为单位
        * `'x'/'y'/'xy'`：以数据坐标系下的`X/Y`为单位，而`xy'`表示数据坐标系下的单位矩形的对角线为单位。

    * `angles`：指定向量的角度。正方形可能因为`X/Y`轴缩放尺度不同而显示为长方形。可以为`'uv'`，表示只采用`U,V`的值计算；可以为`'xy'`，表示角度计算时考虑`X`轴与`Y`轴的缩放尺度。

    * `scale`：一个浮点数，决定缩放比例。它和`scale_units`决定了箭头的全长。假如向量的长度计算得到为 10，那么假如`scale`为 2， 而`scale_units`为`dots`，那么该向量的长度为`5`像素点。

    * `scale_units`：一个字符串，指定缩放比例的单位。可以为`'width'/'height'/'dots'/'inches'/'x'/'y'/'xy'`

    * `width`:一个标量，指定箭头的宽度，单位由`units`参数指定

    * `headwitdh`:一个标量，指定箭头的头部的宽度，单位由`units`参数指定

    * `headlength`:一个标量，指定箭头的头部的长度，单位由`units`参数指定

    * `headaxislength`:一个标量，指定的是箭头的头部的左半边小三角与箭杆的相交的长度。单位由`units`参数指定

    * `minshaft`:一个标量，Length below which arrow scales, in units of head length. 。不要设置成小于 1，否则图形很难看

    * `minlength`:一个标量，指定所有箭头的最短长度（单位由`units`参数指定）。如果有的箭头长度小于它，则绘制成一个点。

    * `pivot`:一个字符串，控制了箭头旋转的中心。可以为`'tail'/'mid'/'middle'/'tip'`。`tip`表示箭头的尖尖。

    * `color`:给出了箭头的颜色。如果给出了`C`参数，则该参数被忽略。

    * 其他参数控制了`PolyCollection`的属性


![quiver](./../imgs/quiver.JPG)

50. `quiverkey(*args, **kw)`：给`quiver`设置`key`。常用的调用方式为：`quiverkey(Q,X,Y,U,label,**kw)`。

    * `Q`：一个`Quiver`实例，由`quiver()`返回

    * `X/Y`：`key`放置的位置，都是标量

    * `U`：`key`的长度，都是标量

    * `label`：一个字符串，指定了标记。

    * `coordinates`：一个字符串，指定了`X/Y`的坐标系。

        * `'axes'`：`axes`坐标系，`(0，0)`为`axes`的左下角，`(1,1)`为`axes`的右上角。
        * `'figure'`：`figure`坐标系，`(0，0)`为`figure`的左下角，`(1,1)`为`figure`的右上角。
        * `'data'`：`data`坐标系
        * `'inches'`：为`figure`坐标系，但是以像素点为基准。`(0,0)`为左下角

    * `color`：重写了`Q`的`color`

    * `labelpos`：放置标记的位置，可以为`'N'/'S'/'E'/'W'`

    * `labelsep`：给出了标记和箭头的距离，单位为英寸

    * `labelcolor`：给出了标记的颜色

    * `fontproperties`：一个字典或者`FontProperties`实例，设置了标记的字体。

    * 其他的关键字参数用于重写`quiver`的一些属性。


![quiverkey](./../imgs/quiver_key.JPG)

51. `remove()`：从`figure`中移除本`axes`。除非重绘`figure`，否则看不出来效果。

52. `scatter(x, y, s=20, c=None, marker='o', cmap=None, norm=None, vmin=None, vmax=None,` `alpha=None, linewidths=None, verts=None, edgecolors=None, **kwargs)`：绘制散点图。返回一个`PathCollection`实例。

    * `x/y`：数据的`x`坐标和`y`坐标，要求它们形状为`(n,)`

    * `s`:指定散点的尺寸，可以为标量，也可以为一个长度为`n`的序列

    * `c`：指定散点的颜色。可以为一个颜色，或者颜色序列

    * `marker`：指定散点的类型，默认为`'o'`。可以为`'.',',','o','v','^','<','>','1','2','3','4','s','p',` `'*','h','H','+','x','D','d','|','_','None',None,' ','','$...$'`之一。也可以为一个`Path`实例。也可以是一个元组`(numsided,style,angle)`：

        * `numsided`指定了边的数量
        * `style`：可以为`0`(正多边形）；`1`（星星状的符号）；`2`（一个`*`）;`3`（一个圆，此时`numsided,angle`被忽略）
        * `angle`：指定了散点旋转的角度（按照角度制而不是弧度制）

    * `cmap`：设定一个`colormap`。可以是`Colormap`实例，或者它的名字。只有当`c`参数为一列浮点数时，有效

    * `norm`：一个`Normalize`实例，用于将亮度调整到`0~1`

    * `vmin,vmax`：一个标量，用于辅助默认的`norm`调整亮度（如果你传入了一个`Normalize`实例给`norm`，则该参数忽略）

    * `alpha`：一个标量，设置透明度

    * `linewidths`：一个标量或者序列，设置线宽

    * `edgecolors`：设定边线的颜色，可以为一个颜色，或者颜色序列

    * 其他参数用于设定`Collection`参数


![scatter](./../imgs/scatter.JPG)

53. `semilogx(*args, **kwargs)`：它类似`plot()`，只是将`x`轴设置为对数坐标。除了多了下面的参数外，其他设置与`plot()`一样。

    * `basex`：一个大于 1 的标量，用于设置对数的底数
    * `subx`：一个序列或者`None`。用于设置`x`轴的主要刻度值。默认采用自动设定
    * `nonposx`：如果为`'mask'`，则`x`的负数或者零将被视作无效的数；如果为`'clip'`，则`x`的负数或者零将被视作一个非常小的正数（因为对数的自变量要大于零）

54. `semilogy(*args, **kwargs)`：它类似`plot()`，只是将`y`轴设置为对数坐标。除了多了下面的参数外，其他设置与`plot()`一样。

    * `basey`：一个大于 1 的标量，用于设置对数的底数
    * `suby`：一个序列或者`None`。用于设置`y`轴的主要刻度值。默认采用自动设定
    * `nonposy`：如果为`'mask'`，则`y`的负数或者零将被视作无效的数；如果为`'clip'`，则`y`的负数或者零将被视作一个非常小的正数（因为对数的自变量要大于零）<br></br>![loglog](./../imgs/loglog.JPG)

55. `spy(Z, precision=0, marker=None, markersize=None, aspect='equal',` `origin='upper', **kwargs)`：绘制矩阵中的非零值。

    * `Z`：待绘制的二维矩阵，它和`precision`决定了绘制区域。坐标点`(i,j)`对应于`Z[j,i]`，即列对应于`x`轴。
    * `precision`：只有`Z`中的那些大于`precision`的值才被绘制
    * `marker`：用它来表示`Z`中的非零值
    * `markersize`：`marker`的大小。
    * `aspect`：高宽比
    * `origin`：参考`imshow`的`origin` ![spy](./../imgs/spy.JPG)

56. `stem(*args, **kwargs)`：绘制`stem`图。其调用方式为：

```
xxxxxxxxxx  stem(y, linefmt='b-', markerfmt='bo', basefmt='r-')  stem(x, y, linefmt='b-', markerfmt='bo', basefmt='r-')
```

```
xxxxxxxxxx其中：`linefmt`决定了垂线的格式。`markerfmt`决定了每个`fmt`的格式。`x`决定了每条垂线的位置（如果未提供，则为`[0,1,...len(y)-1]`）。`y`序列决定了每条垂线的高度。 `basefmt`决定了位于`y=0`这条基准直线的格式。
```

![stem](./../imgs/stem.JPG)

57. `step(x, y, *args, **kwargs)`：绘制阶梯图。调用方式为`step(x, y, *args, **kwargs)`

    * `x/y`：都是一维序列，并且假设`x`为单调递增的（如果不满足，也不报错）
    * `where`：指定分步类型。可以为`'pre'/'post'/'mid'`
    * 其他参数与`plot()`相同

![step](./../imgs/step.JPG)

58. `streamplot(x, y, u, v, density=1, linewidth=None, color=None, cmap=None, norm=None,` `arrowsize=1, arrowstyle='-|>', minlength=0.1,` `transform=None, zorder=1, start_points=None)`：绘制向量场流线。

    * `x/y`：一维数组，给出了网格的坐标
    * `u/v`：二维数组，给出了每个网格的向量。其行数等于`y`的长度，列数等于`x`的长度
    * `density`：一个浮点数或者浮点数的二元元组。控制了绘制向量场的密度。
    * `linewidth`：标量或者二维数组，给出了每个向量箭头的线宽
    * `color`：标量或者二维数组，给出了每个向量箭头的颜色
    * `cmap`：一个`Colormap`实例。当`color`是一个二维数组时，它配合使用，给出了每个向量箭头的颜色
    * `norm`：一个`Normalize`实例。当`color`是一个二维数组时，它配合使用，将颜色亮度调整为`0~1`
    * `arrowsize`：一个浮点数，给出了箭头缩放比例
    * `arrowstyle`：一个字符串，给出了箭头的类型。
    * `minlength`：一个浮点数，限定了最小的向量长度
    * `start_points`：它是一个`N*2`的数组，`N`流线起点的个数，给出了流线起始点的位置

![streamplot](./../imgs/streamplot.JPG)

59. `table(**kwargs)`：添加一个表格，返回一个`table.Table`实例。调用方式为：

```
xxxxxxxxxx  table(cellText=None, cellColours=None,  cellLoc='right', colWidths=None,  rowLabels=None, rowColours=None, rowLoc='left',  colLabels=None, colColours=None, colLoc='center',  loc='bottom', bbox=None)
```

60. `text(x, y, s, fontdict=None, withdash=False, **kwargs)`：添加文本，返回一个`Text`实例。

    * `s`：一个字符串，被添加的文本
    * `x/y`：一个标量，文本被添加的坐标
    * `fontdict`：一个字典，给出了字体属性。
    * `withdash`：一个布尔值。如果为`True`，则创建一个`TextWithDash`实例而不是`Text`实例。
    * 其他参数用于控制`Text`属性

61. `tick_params(axis='both', **kwargs)`：控制`tick`和`tick label`。

    * `axis`：一个字符串，指定要控制那个轴。可以为`'x'/'y'/'both'`
    * `reset`：一个布尔值。如果为`True`，那么在进行处理其他关键字参数之前，先恢复默认值。默认为`False`
    * `which`：一个字符串，指定控制主刻度还是次刻度。可以为`'major'/'minor'/'both'`
    * `direction`：一个字符串，控制将刻度放置在`axes`里面还是外面。可以为`'in'/'out'/'inout'`
    * `length`：一个标量值。给出了每个刻度线的长度（就是那个小竖线），单位为像素点
    * `width`：一个标量值。给出了每个刻度线的宽度（就是那个小竖线），单位为像素点
    * `color`：给出刻度线的颜色
    * `pad`：一个标量值，给出了刻度线和刻度`label`之间的距离，单位为像素点
    * `labelsize`：一个标量值，给出了刻度`label`的字体大小。可以为数值，单位为像素点。也可以为字符串，如`large'`
    * `labelcolor`：给出了刻度`label`的颜色
    * `colors`：同时调整刻度线的颜色和刻度`label`的颜色
    * `bottom/top/left/right`：一个布尔值或者字符串`'on'/'off'`。控制是否绘制对应位置的刻度线
    * `labelbottom/labeltop/labelleft/labelright`：一个布尔值或者字符串`'on'/'off'`。控制是否绘制对应位置的刻度`label`

62. `vlines(x, ymin, ymax, colors='k', linestyles='solid', label='', **kwargs)`：绘制一群垂直线。

    * `x`：标量或者一维数组，给出了垂线的位置
    * `ymin/ymax`：给出了垂线的起始和终止位置。如果是个标量，则所有垂线共享该值
    * `colors`：给出垂线的颜色
    * `linestyles`：给出了垂线的线型
    * `label`：一个字符串
    * 其他关键字参数设置`LineCollection`参数

63. `xcorr(x, y, normed=True, detrend=<function detrend_none>, usevlines=True,` `maxlags=10, **kwargs)`：绘制互相关图。参数解释参考`acorr()`自相关函数。


#### c. Axis类

1. `matplotlib.axis.Axis`实例处理`tick line`、`grid line`、`tick label`以及`axis label`的绘制，它包括坐标轴上的刻度线、刻度`label`、坐标网格、坐标轴标题。通常你可以独立的配置`y`轴的左边刻度以及右边的刻度，也可以独立地配置`x`轴的上边刻度以及下边的刻度。

    * 刻度包括主刻度和次刻度，它们都是`Tick`刻度对象。

2. `Axis`也存储了数据用于内部的缩放以及自适应处理。它还有`Locator`实例和`Formatter`实例用于控制刻度线的位置以及刻度`label`。

3. 每个`Axis`都有一个`.label`属性，也有主刻度列表和次刻度列表。这些`tick`是`XTick`和`YTick`的实例，他们存放着实际的`line primitive`以及`text primitive`来渲染刻度线以及刻度文本。

4. 刻度是动态创建的，只有在需要创建的时候才创建（比如缩放的时候）。`Axis`也提供了一些辅助方法来获取刻度文本、刻度线位置等等：

    * `Axis.get_major_ticks()`：获取主刻度列表（一个`Tick`对象的列表）

    * `Axis.get_minor_ticks()`：获取次刻度列表（一个`Tick`对象的列表）

    * `Axis.get_majorticklabels()`：获取主刻度`label`列表（一个`Text`对象的列表）

    * `Axis.get_majorticklines()`:获取主刻度线（一个`Line2D`对象的列表）

    * `Axis.get_ticklocs()`：获取刻度线位置的列表。 可以通过`minor=True|False`关键字参数控制输出`minor`还是`major`的`tick location`。

    * `Axis.get_ticklabels()`：获取刻度`label`列表(一个`Text`实例的列表）。 可以通过`minor=True|False`关键字参数控制输出`minor`还是`major`的`tick label`。

    * `Axis.get_ticklines()`：获取刻度线列表(一个`Line2D`实例的列表）。 可以通过`minor=True|False`关键字参数控制输出`minor`还是`major`的`tick line`。

    * `Axis.get_scale()`：获取坐标轴的缩放属性，如`'log'`或者`'linear'`

    * `Axis.get_view_interval()`:获取内部的`axis view limits`实例

    * `Axis.get_data_interval()`:获取内部的`axis data limits`实例

    * `Axis.get_gridlines()`:获取`grid line`的列表

    * `Axis.get_label()`:获取`axis label`(一个`Text`实例)

    * `Axis.get_label_text()`:获取`axis label`的字符串

    * `Axis.get_major_locator()`:获取`major tick locator`(一个`matplotlib.ticker.Locator`实例)

    * `Axis.get_minor_locator()`:获取`minor tick locator`(一个`matplotlib.ticker.Locator`实例)

    * `Axis.get_major_formatter()`:获取`major tick formatter`(一个`matplotlib.ticker.Formatter`实例)

    * `Axis.get_minor_formatter()`:获取`minor tick formatter`(一个`matplotlib.ticker.Formatter`实例)

    * `Axis.grid(b=None,which='major',**kwargs)`:一个开关，用于控制`major`或者`minor`的`tick`的`on|off`

    ![Axis tick](./../imgs/Axis.JPG)


5. Axis 方法

    * `axis_date(tz=None)`：将`x`轴视作时间轴
    * `cla()`：清除`axis`
    * `get_xxx()`方法：参考前面叙述的内容
    * `set_xxx()`方法：对应的设置方法。

6. 获取刻度线或者刻度`label`之后，可以设置其各种属性，如可以对刻度`label`旋转 30度：

```
xxxxxxxxxx  for line in axis.get_majorticklabels():    line.set_rotation(30)
```


#### d. Tick类

1. `matplotlib.axis.Tick`类是从`Figure`-->`Axes`-->`Tick`这个`container`体系中最末端的`container`。`Tick`容纳了`tick`、`grid line`以及`tick`对应的`label`。所有的这些都可以通过`Tick`的属性获取:

    * `Tick.tick1line`：一个`Line2D`实例
    * `Tick.tick2line`：一个`Line2D`实例
    * `Tick.gridline`：一个`Line2D`实例
    * `Tick.label1`：一个`Text`实例
    * `Tick.label2`：一个`Text`实例
    * `Tick.gridOn`：一个布尔值，决定了是否绘制`tickline`
    * `Tick.tick1On`：一个布尔值，决定了是否绘制`1st tickline`
    * `Tick.tick2On`：一个布尔值，决定了是否绘制`2nd tickline`
    * `Tick.label1On`：一个布尔值，决定了是否绘制`1st tick label`
    * `Tick.label2On`：一个布尔值，决定了是否绘制`2nd tick label`

> > 

> `y`轴分为左右两个，因此`tick1*`对应左侧的轴；`tick2*`对应右侧的轴。 `x`轴分为上下两个，因此`tick1*`对应下侧的轴；`tick2*`对应上侧的轴。



![Tick](./../imgs/Tick.JPG)

2. 方法有：

    * `get_loc()`：以标量的形式返回`Tick`的坐标
    * `get_pad()`：返回`Tick`的`label`和刻度线之间的距离（单位为像素点）
    * `set_label(s)/set_label1(s)/set_label2(s)`：设置`label`
    * `set_pad(val)`：设置`Tick`的`label`和刻度线之间的距离（单位为像素点）


### 2. primitive

#### a. Line2D类

1. `matplotlib.lines.Line2D`类是`matplotlib`中的曲线类（基类是`matplotlib.artist.Artist`），它可以有各种各样的颜色、类型、以及标注等等。它的构造函数为：

```
xxxxxxxxxx  Line2D(xdata, ydata, linewidth=None, linestyle=None,  color=None, marker=None, markersize=None, markeredgewidth  =None, markeredgecolor=None, markerfacecolor  =None, markerfacecoloralt=’none’, fillstyle=None,  antialiased=None, dash_capstyle=None, solid_capstyle=None,  dash_joinstyle=None, solid_joinstyle=None, pickradius=5,  drawstyle=None, markevery=None, **kwargs)
```

这些关键字参数都是`Line2D`的属性。其属性有：


* 继承自`Artist`基类的属性： `.alpha`、`.animated`、`.axes`、`.clip_box`、.`.clip_on`、`.clip_path`、`.contains`、 `.figure`、`.gid`、`.label`、`.picker`、`.transform`、`.url`、`.visible`、`.zorder`

* `.antialiased`或者`.aa`属性：一个布尔值。如果为`True`则表示线条是抗锯齿处理的

* `.color`或者`.c`属性：一个`matplotlib color`值，表示线条的颜色，

* `.dash_capstyle`属性：为`'butt' or 'round' or 'projecting'`，表示虚线头端类型

* `.dash_joinstyle`属性：为`'miter' or 'round' or 'bevel'`，表示虚线连接处类型

* `.dashes`属性：一个数值序列，表示虚线的实部、虚部的尺寸。如果为`(None,None)`则虚线成为实线

* `.drawstyle`属性：为`'default'or'steps'or'step-pre'or'step-mid'or'step-post'`，表示曲线类型。

    * `'default'`：点之间以直线连接
    * `'steps*'`：绘制阶梯图。其中`steps`等价于`steps-pre`，是为了保持兼容旧代码

* `.fillstyle`属性：为`'full'or'left'or'right'or'bottom'or'top'or'none'`表示`marker`的填充类型。

    * `'full'`：填充整个`marker`
    * `none`：不填充`marker`
    * 其他值：表示填充一半`marker`<br></br>

* `.linestyle`或者`ls`属性：指定线型，可以为以下值：

    * `'-'`或者`'solid'`：表示实线
    * `'--'`或者`dashed`：表示虚线
    * `'-.'`或者`dash_dot`：表示点划线
    * `':'`或者`'dotted'`：表示点线
    * `'None'`或者`' '`或者`''`：表示没有线条（不画线）

* `.linewidth`或者`lw`属性：为浮点值，表示线条宽度

* `.marker`属性：可以为一系列的字符串，如`'.'、','、'o'....`,表示线条的`marker`

* `.markeredgecolor`或者`.mec`属性:可以为`matplotlib color`，表示`marker`的边的颜色

* `.markeredgewidth`或者`.mew`属性:可以为浮点数，表示`marker`边的宽度

* `.markerfacecolor`或者`.mfc`属性：可以为`matplotlib color`，表示`marker`的前景色

* `.markerfacecoloralt`或者`.mfcalt`属性：可以为`matplotlib color`，表示`marker`的可选前景色

* `.markersize`或者`.ms`属性：可以为浮点数，表示`marker`的大小

* `.markevery`属性：指定每隔多少个点绘制一个`marker`，可以为以下值：

    * `None`：表示每个点都绘制`marker`
    * `N`：表示每隔`N`个点绘制`marker`，从0开始
    * `(start,N)`：表示每隔`N`个点绘制`marker`，从`start`开始
    * `[i,j,m,n]`：只有点`i,j,m,n`的`marker`绘制
    * ...其他值参考文档

* `.pickradius`属性：浮点值，表示`pick radius`

* `.solid_capstyle`属性：可以为`'butt'、'round'、'projecting'`，表示实线的头端类型

* `.sold_joinstyle`属性：可以为`'miter'、'round'、'bevel'`，表示实线连接处的类型

* `.xdata`属性：可以为一维的`numpy.array`，表示`x`轴数据

* `.ydata`属性：可以为一维的`numpy.array`，表示`y`轴数据


#### b. Text类

1. `matplotlib.text.Text`类是绘制文字的类（基类是`matplotlib.artist.Artist`）。它的构造函数为：

```
xxxxxxxxxx  Text(x=0, y=0, text='', color=None, verticalalignment='baseline',  horizontalalignment=’left’, multialignment=None, fontproperties  =None, rotation=None, linespacing=None, rotation_  mode=None, usetex=None, wrap=False, **kwargs)
```

这些关键字参数也是属性。其属性有：


* 继承自`Artist`基类的属性： `.alpha`、`.animated`、`.axes`、`.clip_box`、.`.clip_on`、`.clip_path`、`.contains`、 `.figure`、`.gid`、`.label`、`.picker`、`.transform`、`.url`、`.visible`、`.zorder`

* `.backgroundcolor`属性：背景色，可以为任何`matplotlib color`

* `.bbox`属性：文本框的边框。其值是`FancyBboxPatch`类的属性字典。

* `.color`属性：字体颜色，可以为任何`matplotlib color`

* `.family`或者`.name`或者`.fontfamily`或者`.fontname`属性：字体的名字。可以是`string`或者`string list`（表示可以为若干个名字，优先级依次递减）。`string`必须是一个真实字体的名字，或者一个字体的`class name`。

* `.fontproperties`或者`.font_properties`属性：字体的属性，值是一个`matplotlib.font_manager.FontProperties`实例（该实例一次性设置字体的很多属性，比如字体类型、字体名字、字体大小、宽度、...）

* `.horizontalalignment`或者`.ha`属性：水平对齐方式，可以为`'center'、'right'、'left'`

* `.linespacing`属性：为浮点数，单位为`font size`，表示行间距

* `.multialignment`属性：`multiline text`对齐方式，可以为`'left'、'right'、'center'`

* `.position`属性：为一个元组`(x,y)`，表示文本框的位置

* `.rotation`属性：字体旋转角度。可以为下列值：

    * 浮点数，表示角度
    * `'vertical'、'horizontal'`

* `.rotation_mode`属性：旋转模式。可以为下列值：

    * `'anchor'`：文本首先对齐，然后根据对齐点来旋转
    * `None`：文本先旋转，再对齐

* `.size`或者`.fontsize`属性：字体大小。可以为下列值：

    * 浮点值，表示字体大小
    * `'xx-small'、'x-small'、'small'、'medium'、'large'、'x-large'、'xx-large'`

* `.stretch`或者`.fontstretch`属性：字体沿水平方向的拉伸。可以为下列值：

    * 整数，在[0---1000]之间
    * `'ultra-condensed'`、`'extra-condensed'`、`'condensed'`、`'semi-condensed'` 、`'normal'`、`'semi-expanded'`、`'expanded'`、`'extra-expanded'`、`'ultra-expanded'`

* `.style`或者`.fontstyle`属性：字体样式，可以为`'normal'、'italic'、'oblique'`

* `.text`属性:文本字符串，可以为任意字符串（他可以包含`'\n'`换行符或者`LATEX`语法）

* `.variant`或者`.fontvariant`属性：表示字体形变，可以为下列值：`'normal'、'small-caps'`

* `.verticalalignment`或者`.ma`或者`.va`属性：表示文本的垂直对齐，可以为下列值：

    * `'center'、'top'、'bottom'、'baseline'`

* `.weight`或者`.fontweight`属性：设置字体的`weight`，可以为下列值：

    * 一个整数值，在[0---1000]之间
    * `'ultralight'`、`'light'`、`'normal'`、`'regular'`、`'book`'、`'medium'`、 `'roman'`、`'semibold'`、`'demibold'`、`'demi'`、`'bold'`、`'heavy'`、 `'extrabold'`、`'black'`

* `.x`属性：一个浮点值，表示文本框位置的`x`值

* `.y`属性：一个浮点值，表示文本框位置的`y`值


#### c. Annotation类

1. `matplotlib.text.Annotation`类是图表中的图式，它是一个带箭头的文本框，用于解说图表中的图形。它的基类是`matplotlib.text.Text`和`matplotlib.text._AnnotationBase`。其构造函数为：

```
xxxxxxxxxxAnnotation(s, xy, xytext=None, xycoords=’data’, textcoords=None, arrowprops  =None, annotation_clip=None, **kwargs)
```

在位置`xytext`处放置一个文本框，该文本框用于解释点`xy`，文本框的文本为`s`。


* `s`：文本框的文本字符串

* `xy`：被解释的点的坐标

* `xytext`：文本框放置的位置。如果为`None`，则默认取`xy`

* `xycoords`：`xy`坐标系，默认取`'data'`坐标系（即`xy`是数据坐标系中的点）。可以为以下值：

    * `'figure points'`：从`figure`左下角开始的点
    * `'figure pixesl'`：从`figure`左下角开始的像素值
    * `'figure fraction'`：`(0,0)`代表`figure`的左下角，`(1,1)`代表`figure`的右上角
    * `'axes points'`：从`axes`左下角开始的点
    * `'axes pixels'`：从`axes`左下角开始的像素
    * `'axes fraction'`：`(0,0)`代表`axes`的左下角，`(1,1)`代表`axes`的右上角
    * `'data'`：使用被标注对象的坐标系
    * `'offset points'`：指定从`xy`的偏移点
    * `'polar'`：极坐标系

* `textcoords`：文本框坐标系（即`xytext`是文本坐标系中的点），默认等于`xycoords`

* `arrowprops`：指定文本框和被解释的点之间的箭头。如果不是`None`，则是一个字典，该字典设定了`matplotlib.lines.Line2D`的属性。

    * 如果该字典有一个`arrowstyle`属性，则该键对应的值也是一个字典，创建一个`FancyArrowsPatch`实例，实例属性由该字典指定。
    * 如果该字典没有`arrowstyle`属性，则创建一个`YAArrow`实例，

* `annotation_clip`：控制超出`axes`区域的`annotation`的显示。如果为`True`则`annotation` 只显示位于`axes`区域内的内容。

* 额外的关键字参数全部是设置`Text`的属性


#### d. Legend

1. `matplotlib.legend.Legend`是图例类，它的基类是`matplotlib.artist.Artist`。其构造函数为：

```
xxxxxxxxxx  Legend(parent, handles, labels, loc=None, numpoints=None, markerscale  =None, markerfirst=True, scatterpoints=None,  scatteryoffsets=None, prop=None, fontsize=None, borderpad  =None, labelspacing=None, handlelength=None,  handleheight=None, handletextpad=None, borderaxespad  =None, columnspacing=None, ncol=1, mode=None,  fancybox=None, shadow=None, title=None, framealpha  =None, bbox_to_anchor=None, bbox_transform=None,  frameon=None, handler_map=None)
```

其关键字参数为：


* `parent`：持有该`legend`的`artist`

* `loc`:图例的位置。其值可以为字符串或者数字：

    * `best`或0：自动计算
    * `upper right`或1： 右上角
    * `upper left`或2：上角
    * `lower left`或3：下角
    * `lower right`或4：右下角
    * `right`或5：右边
    * `center left`或6：中间偏左
    * `center right`或7：中间偏右
    * `lower center`或8：中间底部
    * `upper center`或9：中间顶部
    * `center`或10：正中央

* `handle`：一个`artist`列表，添加这些`artist`到`legend`中

* `lebels`：一个字符串列表添加到`legend`中

* `prop`:字体属性

* `fontsize`: 字体大小（只有`prop`未设置时有效）

* `markerscale`: `marker`的缩放比例（相对于原始大小）

* `markerfirst`: 如果为`True`，则`marker`放在`label`左侧；否则`marker`放在`label`右侧

* `numpoints`: the number of points in the legend for line

* `scatterpoints`: the number of points in the legend for scatter plot

* `scatteryoffsets`: a list of offsets for scatter symbols in legend

* `frameon`: if True, draw a frame around the legend. If None, use rc

* `fancybox`: if True, draw a frame with a round fancybox. If None, use rc

* `shadow`: if True, draw a shadow behind legend

* `framealpha`: If not None, alpha channel for the frame.

* `ncol`: number of columns

* `borderpad`: the fractional whitespace inside the legend border

* `labelspacing`: the vertical space between the legend entries

* `handlelength`: the length of the legend handles

* `handleheight`: the height of the legend handles

* `handletextpad`: the pad between the legend handle and text

* `borderaxespad`: the pad between the axes and legend border

* `columnspacing`:the spacing between columns

* `title`: 图例的标题

* `bbox_to_anchor`: the bbox that the legend will be anchored.

* `bbox_transform`: the transform for the bbox. transAxes if Noneloc a location code

* 其他关键字参数用于设置属性


属性为：

* 继承自`Artist`基类的属性： `.alpha`、`.animated`、`.axes`、`.clip_box`、.`.clip_on`、`.clip_path`、`.contains`、 `.figure`、`.gid`、`.label`、`.picker`、`.transform`、`.url`、`.visible`、`.zorder`

#### e. Patch类

1. `matplotlib.patches.Patch`类是二维图形类。它的基类是`matplotlib.artist.Artist`。其构造函数为：

```
xxxxxxxxxx  Patch(edgecolor=None, facecolor=None, color=None,  linewidth=None, linestyle=None, antialiased=None,  hatch=None, fill=True, capstyle=None, joinstyle=None,  **kwargs)
```

参数为：


* `edgecolor`：可以为`matplotlib color`，表示边线条的颜色，若为`none`则表示无颜色

* `facecolor`：可以为`matplotlib color`，表示前景色，若为`none`则表示无颜色

* `color`可以为`matplotlib color`，表示边线条和前景色的颜色。

* `linewidth`：为浮点数，表示线条宽度

* `linestyle`：指定线型，可以为以下值：

    * `'-'`或者`'solid'`：表示实线
    * `'--'`或者`dashed`：表示虚线
    * `'-.'`或者`dash_dot`：表示点划线
    * `':'`或者`'dotted'`：表示点线
    * `'None'`或者`' '`或者`''`：表示没有线条（不画线）

* `antialiased`：一个布尔值。如果为`True`则表示线条是抗锯齿处理的

* `hatch`：设置`hatching pattern`，可以为下列的值：

    * `'\'`、`'|'`、`'-'`、`'+'`、`'x'`、`'o'`、`'0'`、`'.'`、`'*'`

* `fill`：为布尔值。如果为`True`则填充图形，否则不填充

* `capstyle`：为`'butt' or 'round' or 'projecting'`，表示线条头端类型

* `joinstyle`：可以为`'miter'、'round'、'bevel'`，表示矩形线条接头类型

* 其他关键字参数用于设置属性


> > 

> 如果 `edgecolor, facecolor, linewidth, or antialiased` 为`None`则这些值从`rc params`中读取



属性如下：

* 继承自`Artist`基类的属性： `.alpha`、`.animated`、`.axes`、`.clip_box`、.`.clip_on`、`.clip_path`、`.contains`、 `.figure`、`.gid`、`.label`、`path_effects`、`.picker`、`.transform`、`.url`、`.visible`、 `.zorder`

* `.antialiased`或者`.aa`属性：一个布尔值。如果为`True`则表示线条是抗锯齿处理的

* `.capstyle`属性：为`'butt' or 'round' or 'projecting'`，表示线条头端类型

* `.color`属性：可以为`matplotlib color`，表示边线条和前景色的颜色。

* `.edgecolor`或者`.ec`属性：可以为`matplotlib color`，表示边线条的颜色，若为`none`则表示无颜色

* `.facecolor`或者`.fc`属性：可以为`matplotlib color`，表示前景色，若为`none`则表示无颜色

* `.fill`属性：为布尔值。如果为`True`则填充图形，否则不填充

* `.hatch`属性：设置`hatching pattern`，可以为下列的值：

    * `'\'`、`'|'`、`'-'`、`'+'`、`'x'`、`'o'`、`'0'`、`'.'`、`'*'`

* `.joinstyle`属性：可以为`'miter'、'round'、'bevel'`，表示矩形线条接头类型

* `.linestyle`或者`.ls`属性：指定线型，可以为以下值：

    * `'-'`或者`'solid'`：表示实线
    * `'--'`或者`dashed`：表示虚线
    * `'-.'`或者`dash_dot`：表示点划线
    * `':'`或者`'dotted'`：表示点线
    * `'None'`或者`' '`或者`''`：表示没有线条（不画线）

* `.linewidth`或者`.lw`属性：为浮点数，表示线条宽度


#### f. Rectangle 类

1. `matplotlib.patches.Rectangle`类是矩形类（基类是`matplotlib.patches.Patch`），其构造函数为：`Rectangle(xy,width,height,angle=0.0,**kwargs)`。 参数为：

    * `xy`：矩形左下角坐标
    * `width`：矩形宽度
    * `height`：矩形高度
    * 其他关键字参数用于设置属性

其属性有：

    * 继承自`Artist`基类的属性： `.alpha`、`.animated`、`.axes`、`.clip_box`、.`.clip_on`、`.clip_path`、`.contains`、 `.figure`、`.gid`、`.label`、`.picker`、`.transform`、`.url`、`.visible`、`.zorder`
    * 继承自`Patch`基类的属性： `.antialiased`或者`.aa`、`.capstyle`、`.color`、`.edgecolor`或者`.ec`、`.facecolor`或者`.fc`、`.fill`、`.hatch`、`.joinstyle`、`.linestyle`或者`.ls`、`.linewidth`或者`.lw`属性


#### g. Polygon类

1. `matplotlib.patches.Polygon`类是多边形类。其基类是`matplotlib.patches.Patch`。其构造函数为： `Polygon(xy, closed=True, **kwargs)`。参数为：

    * `xy`是一个`N×2`的`numpy array`，为多边形的顶点。
    * `closed`为`True`则指定多边形将起点和终点重合从而显式关闭多边形。
    * 其他关键字参数用于设置属性

`Polygon`的属性有：

    * 继承自`Artist`基类的属性： `.alpha`、`.animated`、`.axes`、`.clip_box`、.`.clip_on`、`.clip_path`、`.contains`、 `.figure`、`.gid`、`.label`、`.picker`、`.transform`、`.url`、`.visible`、`.zorder`
    * 继承自`Patch`基类的属性： `.antialiased`或者`.aa`、`.capstyle`、`.color`、`.edgecolor`或者`.ec`、`.facecolor`或者`.fc`、`.fill`、`.hatch`、`.joinstyle`、`.linestyle`或者`.ls`、`.linewidth`或者`.lw`属性


#### h. PolyCollection类

1. `matplotlib.collections.PolyCollection`是多边形集合类，其基类是`matplotlib.collections._CollectionWithSizes`。它的构造函数为： `PolyCollection(verts, sizes=None, closed=True, **kwargs)`。

其关键字参数为：

    * `verts`：一个顶点序列。每个顶点都由`xy元组`或者`xy数组`组成
    * `sizes`：一个浮点数序列，依次指定每个顶点正方形的边长。如果序列长度小于顶点长度，则循环从序列头部再开始 挑选
    * `closed`：如果为`True`，则显式封闭多边形
    * `edgecolors`: `collection`的边的颜色
    * 其他关键字参数用于设置属性

下面为属性：

    * 继承自`Artist`基类的属性： `.alpha`、`.animated`、`.axes`、`.clip_box`、.`.clip_on`、`.clip_path`、`.contains`、 `.figure`、`.gid`、`.label`、`.picker`、`.transform`、`.url`、`.visible`、`.zorder`
    * `.facecolors`: `collection`的前景色
    * `.linewidths`: `collection`的边线宽
    * `.antialiaseds`:抗锯齿属性，可以为`True`或者`False`
    * `.offsets`: 设置`collection`的偏移
    * `.norm`: 归一化对象
    * `.cmap`:`color map`


## 三、基本概念

1. `matplotlib`被划分为不同的层次：

    * `matplotlib.pyplot`模块：位于`matplotlib`的顶层，它是一个`state-machine environment`。该模块中的很多函数是用于给当前`Figure`的当前`Axes`添加`plot element`，比如`line`、`text`、`image`等。它非常类似于`Matlab`的用法。
    * 下一层是面向对象的接口：在这一层`pyplot`只是用部分函数来创建`Figure`，然后通过该`Figure`显式的创建`Axes`，然后通过面向对象的接口在该`Axes`上添加图形。极端情况下用户可以完全抛弃`pyplot`而完全使用面向对象的接口。

> > 

> 对于非交互式绘图，官方文档推荐用`pyplot`创建`Figure`，然后使用面向对象接口来绘图。



2. `matplotlib`的所有`plotting function`期待输入`numpy.array`或者`numpy.ma.masked_array`类型的数据作为输入。某些长得像`numpy.array`的数据比如`numpy.matrix`类型的输入数据可能会导致`matplotlib`工作异常。如果确实需要使用`numpy.matrix`，你应该首先将它转换为`numpy.array`

3. matplotlib 、 pyplot 、 pylab 的关系:

    * `matplotlib`：它是整个`package`
    * `matplotlib.pyplot`：是`matplotlib`的一个`module`。它为底层的面向对象接口提供了一个`state-machine interface`。这个`state-machine`必要的时候隐式创建`Figure`和`Axes`，并维护`current Figure`和`current Axes`
    * `pylab`是一个便利的`module`，它导入了`matplotlib.pyplot`以及`numpy`，它只是为了`plot`以及`math`方便而用。官方文档不推荐使用它。

`pyplot.gcf()`：获取当前的`figure`对象。`pyplot.gca()`：获取当前的`Axes`对象

4. 代码风格:官方文档不推荐 `MATLAB`风格的代码。因为`MATLAB`风格代码维护了全局状态，你执行同一个`plot`多次可能会发现结果是不同的。官方文档推荐使用如下风格：

```
xxxxxxxxxx  import matplotlib.pyplot as plt  import numpy as np  fig=plt.figure()  ax=fig.add_subplot(111)  ax.plot(...)  ax.show()
```

这样的风格使得在绘图事件中，每个角色都很清楚，数据的流动也很清楚。


### 1. backend

1. `matplotlib`可以适用于非常广泛的场景：

    * `matplotlib`可以交互式地用于`python shell`
    * `matplotlib`可以嵌入到`wxpython`或者`pygtk`等`GUI`程序中
    * `matplotlib`可以在脚本中使用从而生成`postscript image`

为了适应于这些场景，`matplotlib`针对这些`target`生成不同的输出格式。这种能力称之为`backend`。

> > 

> 与之相对的`frontend`指的是用户使用`matplotlib`而编写的代码



2. 有两种类型的`backend`：

    * 交互式的`backend`：应用于`pygtk`、`wxpython`、`tkinter`、`qt4`、`macosx`等中
    * 非交互式的`backend`：用于生成`image file`（如`PNG、SVG、PDF、PS`等格式文件，这些`backend`的名字暗示了要存储的文件的格式）

3. 有多种方法来设置`backend`，其中后面提到的方法会覆盖前面的方法设置的`backend`：

    * 在`matplotlibrc`配置文件中设置的`backend`参数，如`backend: WXAgg #使use wxpython with antigrain(agg) rendering`
    * 设置`MPLBACKEND`环境变量，无论是在`shell`中设置还是在脚本中设置。
    * 对单个脚本设置`backend`时，可以直接在`python`命令后添加`-d`命令（这种方法不推荐，`deprecated`）
    * 在脚本中使用特定的`backend`时，可以用`matplotlib.use('PDF')`命令。这条语句必须在`import matplotlib.pyplot`语句之前执行。如果在`import matplotlib.pyplot`之后执行`use`语句，则没有任何效果。通常建议避免使用`use()`方法，因为使用该脚本的人无法修改`backend`了。

> 
    * 设定`backend`时，是忽略大小写的。因此`GTKAgg`也等价于`gtkagg`
    * 查看当前的`backend`可以用：`matplotlib.get_backend()`


4. rendering engine ：`matplotlib`提供的常用的`rendering engine`是`Agg`，它采用的是`Anti-Grain Geometry C++ library`。除了`macosx`之外的所有`user interface`都可以用`agg rendering`，如`WXAgg,GTKAgg,QT4Agg,TkAgg`这些`backend`。

某些`user interface`还支持其他引擎，如`GTK`支持`Cario`引擎，如`GTKCariro backend`。

下面是所有的`Rendering engine`：

    * `AGG`：输出`png`格式文件。它可以输出高质量的图形
    * `PS`：输出`ps\eps`格式文件。它是`Postscript output`
    * `PDF`：输出`pdf`格式文件。
    * `SVG`：输出`svg`格式文件
    * `Cairo`：可以输出`png、ps、pdf、svg...`等格式文件
    * `GDK`：可以输出`png、jpg、tiff...`等格式文件，它使用`Gimp Drawing Kit`

> > 

> 要想保存成指定类型文件，如`PDF`，那么首先要设置合适的`backend`，




### 2. 交互式模式

1. 使用交互式`backend`可以`plotting to the screen`，但是前提是`matplotlib`必须是`interactive mode`。

你可以在`matplotlibrc`配置文件中设置`matplotlib`是否位于交互模式，也可以通过代码`matplotlib.interacite()`来设置`matplotlib`位于交互模式。你可以通过代码`matplotlib.is_interactive()`来判断代码是否交互模式。通常并不建议在绘图过程中修改交互模式，因此要提前修改交互模式再绘图。

> > 

> 交互模式也可以通过`matplotlib.pyplot.ion()`开启交互模式，由`matplotlib.pyplot.ioff()`关闭交互模式。另外交互模式支持`ipython`和`python shell`，但是不支持`IDLE IDE`。



![交互模式](./../imgs/interactive_mode.JPG)

2. 在交互模式下：

    * `pyplot.plot()`绘图之后图表马上显示，`pyplot`自动绘制到屏幕，不需要调用`pyplot.show()`
    * 图表显式之后你可以继续输入命令。任何对图形的修改会实时的反应到图表中去。
    * 使用面向对象的方法，如`Axes`的方法并不会自动调用`draw_if_interactive()`。如果你通过`Axes`来修改图表，想更新图表的话那么你需要手动调用`.draw()`方法。而`pyplot`模块中的函数会主动调用`draw_if_interactive()`,因此如果你是通过`pyplot`模块修改图表那么不需要手动调用`.draw()`方法就是实时绘制。

3. 在非交互模式下：

    * 在绘图之后必须手动调用`pyplot.show()`才能显示图表。该函数会阻塞执行直到你关闭了图表窗口。
    * 所有的绘制工作会延迟到`pyplot.show()`函数调用
    * 在1.0版本以前，单个脚本文件中只能调用一次`pyplot.show()`，在1.01版本之后该限制被放松。


### 3. matplotlib的颜色

1. 可以通过`matplotlib.pyplot.colors()`方法获取`matplotlib`支持的所有颜色。该方法不做任何事情，就是提供一个帮助文档。

2. `matplotlib`提供了下面颜色的别名：`'b'`：蓝色；`'g'`：绿色；`'r'`：红色；`'y'`：黄色；`'c'`：青色；`'k'`：黑色；`'m'`：洋红色；`'w'`：白色。

3. 你也可以定制自己的颜色。有两种方法：

    * 使用HTML十六进制字符串：如`'#eeefff'`
    * 使用HTML颜色名字：如`'red'`
    * 使用一个归一化到闭区间[0-1]的RGB元组：如`color=(0.3,0.3,0.4)`


### 4. matplotlib.cm

1. `matplotlib.cm`模块包含了一系列的`colormap`，以及相关的函数。它主要有两个函数：

    * `matplotlib.cm.get_cmap(name=None, lut=None)`：获取一个`colormap`实例。其中：

        * `name`：指定了`colormap`的名字。如果为`None`，则使用`rc`配置。如果它已经是`colormap`实例，则直接返回该实例。注意：`register_cmap`注册的`colormap`优先查询
        * `lut`：一个整数。如果非`None`，则指定了查询表的`number of entries`

    * `matplotlib.cm.register_cmap(name=None, cmap=None, data=None, lut=None)`：注册一个`colormap`。有两种使用方式：

        * `register_cmap(name='swirly', cmap=swirly_cmap)`：此时`cmap`参数必须是`matplotlib.colors.Colormap`实例。`name`默认为该`Colormap`实例的`.name`属性。
        * `register_cmap(name='choppy', data=choppydata, lut=128)`：此时这三个参数传递给`matplotlib.colors.LinearSegementedColormap`初始化函数。


所有的内置的`name`如下：

```
xxxxxxxxxx  'Perceptually Uniform Sequential':['viridis', 'inferno', 'plasma', 'magma']  'Sequential':['Blues', 'BuGn', 'BuPu','GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',  'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu','Reds', 'YlGn', 'YlGnBu',   'YlOrBr', 'YlOrRd']  'Sequential (2)':['afmhot', 'autumn', 'bone', 'cool','copper', 'gist_heat', 'gray',   'hot','pink', 'spring', 'summer', 'winter']   'Diverging':['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',  'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral','seismic']   'Qualitative':['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2',  'Set1', 'Set2', 'Set3']   'Miscellaneous':['gist_earth', 'terrain', 'ocean', 'gist_stern','brg',  'CMRmap', 'cubehelix','gnuplot', 'gnuplot2',     'gist_ncar','nipy_spectral', 'jet', 'rainbow',  'gist_rainbow', 'hsv', 'flag', 'prism']
```

你可以使用`cm.get_cmap('winter')`来使用，也可以直接用`cm.winter`来使用。

![cm0](../imgs/cm0.JPG) ![cm1](../imgs/cm1.JPG) ![cm2](../imgs/cm2.JPG) ![cm3](../imgs/cm3.JPG) ![cm4](../imgs/cm4.JPG) ![cm5](../imgs/cm5.JPG) ![cm6](../imgs/cm6.JPG)


### 5. matplotlib.colors

1. `matplotlib.colors`是一个模块，用于转换数字或者颜色参数到 `RGB` 或者`RGBA`

    * `RGB`：一个浮点数元组，有3个浮点数。每个数都是 0-1之间
    * `RGBA`：一个浮点数元组，有4个浮点数。每个数都是 0-1之间

2. `colors.cnames`是个字典，它给出了常用颜色的字符串和对应的`#FFFFFF`形式。 ![cnames](../imgs/colors_cnames.JPG)

3. `colors.rgb2hex(rgb)`函数：给出了`rgb`元组到`#FFFFFF`形式。 而`hex2color(s)`给出了`#FFFFFF`到`rgb`形式。 ![rgb_hex](../imgs/colors_rgb_hex.JPG)

4. `colors.ColorConverter`类是个颜色转换器类。它提供了下面方法用于转换颜色：

    * `.to_rgb(arg)`：转换其他类型的颜色到标准的`rgb`三元组。其中`arg`可以为一个`rgb/rgba`序列，或者一个字符串，字符串格式为：

        * 一个代表颜色的字符，如`'rgbcmykw'`
        * 一个十六进制的颜色字符串，如`'#0FFFFFF'`
        * 一个标准的颜色的名字，如`'red'`
        * 一个代表浮点数的字符串，如`'0.5'`

    * `.to_rgba(arg, alpha=None)`：转换其他类型的颜色到标准的`rgba`四元组

    * `to_rgba_array(c, alpha=None)`：它返回一个`ndarray`，而不是一个元组


`colors.colorConverter`是模块提供的一个默认的实例。 ![colorConverter](../imgs/colors_colorConverter.JPG)

5. `colors.Colormap`是所有`colormap`的基类。`colormap`用于将`[0,1]`之间的浮点数转换为`RGBA`颜色。

> > 

> 它是一个颜色条，浮点数对应了颜色条的位置（归一化为0.0~1.0），`RGBA`颜色对应了指定颜色条某个位置处的颜色。



其属性有：

    * `name`：`colormap`名字
    * `N`：一个整数，表示`rgb`颜色层级，默认为256级

常用方法有：

    * `__call__(self, X, alpha=None, bytes=False)`：颜色转换。

        * `X`为一个标量或者`ndarray`，给出了待转换的数据。如果是浮点数，则必须是`[0.0,1.0]`之间。如果是整数，则必须是`[0,self.N)`之间。如果是标量，则返回`rgba`四元组。如果是`ndarray`，则返回一个`ndarray`，相当于对每个元素进行标量转换，然后组装成`ndarray`
        * `alpha`：一个浮点数，给出了透明度。必须是0到1之间
        * `bytes`：一个布尔值。如果为`True`，则返回的结果是`[0,255]`之间。否则是`[0.0,1.0]`之间


6. `colors.LinearSegmentColormap(Colormap)`：是`Colormap`的子类。

额外的属性： `._gamma`/`._segmentdata`

    * 它的构造函数为：`__init__(self, name, segmentdata, N=256, gamma=1.0)`。其中`segmentdata`是一个字典，字典的键分别为`'red'/'green'/'blue'`，字典的值为一个列表，列表元素为三元组(`alpha`被忽略）。如：

    ```
xxxxxxxxxx  {'red':[(0.0,  0.0, 0.0),  (0.5,  1.0, 1.0),  (1.0,  1.0, 1.0)],  'green': [(0.0,  0.0, 0.0),  (0.25, 0.0, 0.0),  (0.75, 1.0, 1.0),  (1.0,  1.0, 1.0)],  'blue':  [(0.0,  0.0, 0.0),  (0.5,  0.0, 0.0),  (1.0,  1.0, 1.0)]}
    ```

    每一行代表了元组`(x,y0,y1)`。其中`red/green/blue`中，每一列`x`必须从0递增到1；`y0/y1`也是如此。对于任何落到`x[i]~x[i+1]`之间的值`z`，其映射的颜色由`y1[i]`和`y0[i+1]`插值决定。

    * 类方法 `from_list(name, colors, N=256, gamma=1.0)`:从一个颜色序列中构造`LinearSegmentColormap`。其中`colors`是一个颜色序列，`matplotlib`会将颜色均匀分布，`val=0`处对应`colors[0]`，`val=1`处对应`colors[-1]`。你也可以传递一个`(value,color)`元组的序列，其中`value`指定了对应位置处的`color`，其中`value`位于`[0.0,1.0]`


![LinearSegmentColormap0](../imgs/colors_LinearSegmentColormap0.JPG) ![LinearSegmentColormap1](../imgs/colors_LinearSegmentColormap1.JPG)

7. `colors.ListedColormap(Colormap)`是`Colormap`的子类。它用于从一个`list of colors`中创建`colormap`。

    * 构造方法为：`__init__(self, colors, name=’from_list’, N=None)`。其中`color`是一个颜色列表。或者为一个浮点数`ndarray`，其形状为`Nx3`或者`Nx4`。`N`为`colormap`的条目数，如果`N <len(colors)`，则截断`colors`。如果`N > len(colors)`，则重复`colors`到指定长度。

![ListedColormap](../imgs/colors_ListedColormap.JPG)

8. `colors.Normalize`：是归一化类。它用于将数据归一化到`[0.0,1.0]`

    * 构造方法为： `__init__(self, vmin=None, vmax=None, clip=False)`。如果未提供`vmin/vmax`，则使用数据的最小值和最大值。如果`clip=True`，则落在`vmin~vmax`之外的数据被截断为0或者1。如果`vmin==vmax`，则始终返回 0
    * 属性有： `.vmin/.vmax/.clip`
    * 类方法为： `process_value(value)`：调整`value`的格式，从而方便后续的操作
    * 实例方法： `__call__(self, value, clip=None)`：归一化处理
    * 实例方法： `inverse(self, value)`：逆归一化处理

![Normalize](../imgs/colors_Normalize.JPG)

9. `colors.LogNorm`类是`Normalize`的子类，它使用对数来归一化

10. `colors.rgb_to_hsv(arr)`：将`rgb`形式的浮点数数组转换为`hsv`格式的浮点数组。而`hsv_to_rgb(hsv)`执行的是逆向操作。


### 6. matplotlib.colorbar

1. `matplotlib.colorbar`模块包含了创建`colorbar`的一些方法和类。

    * `ColorbarBase`：绘制`colorbar`的基类
    * `Colorbar`：用于`imges/contour`等的`colorbar`类
    * `make_axes()`：用于调整`Axes`并向其中添加一个`colorbar`

2. `matplotlib.colorbar.Colorbar(ax, mappable, **kw)`：`Colorbar`类。通常没必要显式调用构造函数，而应该调用下面两个方式：

    * `Figure.colorbar(mappable, cax=None, ax=None, use_gridspec=True, **kw)`
    * `pyplot.colorbar(mappable=None, cax=None, ax=None, **kw)`

参数为：

    * `mappable`：为`Image/ContourSet`对象。它是你将要应用`colorbar`的对象
    * `cax`：它指定了你将在哪个`Axes`内绘制`colorbar`
    * `ax`：你的新的`colorbar Axes`从该`ax`中拿到绘制空间。
    * `use_gridspec`：一个布尔值。如果`cax=None`，则如果`use_gridspec=True`，则创建一个`Subplot`对象。如果为`False`，则创建一个`Axes`对象。

额外的参数参与设置两个对象：

    * `axes`对象：

        * `orientation` ：设置为垂直`'vertical'`还是水平`'horizontal'`
        * `fraction` ：一个浮点数，指定从原始的`Axes`中窃取多少倍的空间来绘制`colorbar` 。默认为 0.15
        * `pad` ：0.05 if vertical, 0.15 if horizontal; 一个浮点数，指定两个`Axes`的间距
        * `shrink` ： 指定`colorbar`的伸缩比。默认为 1.0
        * `aspect` ：指定`colorbar`的长宽比。默认为 20

    * `colorbar`对象：

        * `extend`：一个字符串。可以为`'neither'/'both'/'min'/'max'`。如果不是`'neither'`，则它会在`colorbar`对应端添加箭头（如果`extendrect=False`）
        * `extendfrac`：`colorbar`指示超出部分的箭头的长度。
        * `extendrect`：一个布尔值。如果为`True`，则超出部分不用箭头。
        * `drawedges`：一个布尔值，如果为`True`，则绘制`colorbar`的边。
        * `ticks`：给出你要显示哪些`tick`
        * `format`：指定格式化方式。可以为格式化字符串如`%.3f`，或者`Formatter`对象。


![colorbar](../imgs/colorbar.JPG) ![colorbar](../imgs/colorbar.png)


## 四、布局

### 1. 简单布局

1. 简单布局通过`Figure.add_subplot(*args,**kwargs)`方法来完成，它返回的是`Axes`实例。当然你也可以通过`pyplot.subplot(*args,**kwargs)`函数来完成，他返回的也是`Axes`实例，该函数只是一个便利函数。

> > 

> `SubPlot`类是`Axes`类的子类。因此`SubPlot`对象也是`Axes`对象。



1. 最典型用法是`matplotlib.pyplot.subplot(nrows,ncols,plot_number)`。`nrows`和`ncols`将图表划分成`nrows*ncols`大小的网格区域，每一个区域都能存放一个`SubPlot`；该函数创建`plot_number`位置处的`SubPlot-axes`。其中`plot_number`起始于1，最大值为`nrows*ncols`。

如果`nrows`、`ncols`、`plot_number`都是个位数，则你可以指定一个三位数来简化函数调用`matplotlib.pyplot.subplot(integer)`，其中百分位代表`nrows`，十分位代表`ncols`，各位代表`plot_number`。

2. `add_subplot`其他的参数：

    * `axisbg`关键字参数：指定`subplot`的背景色
    * `polar`关键字参数：指定`subplot`是否是极坐标。默认为`False`
    * `projection`：指定坐标方式，可以为：`'aitoff'`、`'hammer'`、 `'lambert'`、`'mollweide'`、 `'polar'`、 `'rectilinear'`。当`projection='polar'`等价于`ploar=True`
    * `sharex`关键字参数：指定`subplot`与其他`Axes`(由该参数值指定）共享`xaxis attribute`
    * `sharey`关键字参数：指定`subplot`是否与其他`Axes`(由该参数值指定）共享`yaxis attribute`

3. 你可以通过`pyplot.subplots()`函数一次性的创建多个`SubPlot`。

> > 

> `pyplot.subplot()`每次只会创建一个`SubPlot`。



![pyplot.subplots](./../imgs/pyplot_subplots.JPG)

其参数有：

    * `nrows`：行数，默认为1

    * `ncols`：列数，默认为1

    * `sharex`：

        * 如果为`True`，则所有`SubPlot`的`X axis`被共享。此时只有最后一行的`X`轴可见。
        * 如果为`False`，则`SubPlot`的`X axis`不共享，每一个`SbuPlot`的`X`轴可见。
        * 如果为字符串`all`，则等效于`True`
        * 如果为字符串`none`，则当小于`False`
        * 如果为字符串`row`，则每一行的`SubPlot`共享一个`X`轴（与`False`等效）
        * 如果为字符串`col`，则每一列的`SubPlot`共享一个`X`轴（与`True`等效）

    ![pyplot.subplots(sharex=True)](./../imgs/pyplot_subplots_sharex.JPG)

    ![pyplot.subplots(sharex='row')](./../imgs/pyplot_subplots_sharey.JPG)

    ![pyplot.subplots(sharex='col')](./../imgs/pyplot_subplots_sharexy.JPG)

    * `sharey`：

        * 如果为`True`，则所有`SubPlot`的`Y axis`被共享。此时只有第一列的`Y`轴可见。
        * 如果为`False`，则`SubPlot`的`Y axis`不共享，每一个`SbuPlot`的`Y`轴可见。
        * 如果为字符串`all`，则等效于`True`
        * 如果为字符串`none`，则当小于`False`
        * 如果为字符串`row`，则每一行的`SubPlot`共享一个`Y`轴（与`True`等效）
        * 如果为字符串`col`，则每一列的`SubPlot`共享一个`Y`轴（与`False`等效）

    * `squeeze`：

        * 如果为`True`：

            * 如果只创建了一个`SubPlot`，则返回一个变量（创建的SubPlot对象)
            * 如果创建了`N*1`或者`1*N`个`SubPlot`，则返回一个1维向量
            * 如果创建了`N*M`个`SubPlot`（其中`N>1`,`M>1`），则返回一个2维向量

        * 如果为`False`则始终返回一个2维向量


    * `subplot_kw`：一个字典参数，用于传递给`Axes.add_subplot()`来创建`SubPlot`

    * `gridspec_kw`：一个字典参数，用于传递给`GridSpec`构造函数来创建`SubPlot`存放的网格

    * `fig_kw`：一个字典参数，用于传递给`pyplot.figure()`函数。所有前述未能识别的感激案子参数都会传到这里。


其返回值为`figure,ax`。其中`figure`是一个`Figure`对象；`ax`取决于`squeeze`参数。


### 2. 使用 pyplot.subplot2grid() 函数

1. 使用`pyplot.subplot2grid()`函数时，你只需要提供网格形状以及`SubPlot`位置即可，如： `ax=pyplot.subplot2grid((2,2),(0,0))`，它等价于`ax=pyplot.subplot(2,2,1)`。其中`subplot2grid()`的位置坐标从0开始。

2. `subplot2grid()`支持`SubPlot`横跨或者纵跨多个单元格。`colspan`关键字参数指定纵向的跨度；`rowspan`guan尖子参数指定横向的跨度。

![pyplot.subplot2grid()](./../imgs/pyplot_subplot2grid.JPG)


### 3. 使用 GridSpec 和 SubplotSpec

1. 你可以直接创建`matplotlib.gridspec.GridSpec`然后通过它来创建`SubPlot`。如：

```
xxxxxxxxxx  gs=matplotlib.gridspec.GridSpec(2,2) #网格2行2列  matplotlib.pyplot.subplot(gs[0,0])
```

等价于`matplotlib.pyplot.subplot2grid((2,2),(0,0))`

2. `GridSpec`对对象提供了类似`array`的索引方法，其索引的结果是一个`SubplotSpec`对象实例。如果你想创建横跨多个网格的`SubplotSpec`，那么你需要对`GridSpec`对象执行分片索引，如`pyplot.subplot(gs[0,:-1])`。

![使用`GridSpec`和`SubplotSpec`](./../imgs/GridSpec.JPG)

3. 如果你使用`GridSpec`，那么你可以调整由`GridSpec`创建的`SubplotSpec`的`layout parameter`。如：

```
xxxxxxxxxx  gs=gridspec.GridSpec(3,3)  gs.update(left=0.05,right=0.48,wspace=0.05)
```

这种用法类似于`subplots_adjust`，但是它仅仅影响由本`GridSpec`创建的`SubplotSpec`。其中`gs.update()`的关键字参数有：


* `left`关键字参数：`subplot`左侧宽度
* `right`关键字参数：`subplot`右侧宽度
* `bottom`关键字参数：`subplot`底部高度
* `top`关键字参数：`subplot`顶部高度
* `wspace`关键字参数：`subplot`之间的空白宽度
* `hspace`关键字参数：`subplot`之间的空白的高度

1. 你可以从`SubplotSpec`创建`GridSpec`。此时`layout parameter`由该`SubplotSpec`指定。如：

```
xxxxxxxxxx  gs0=gridspec.GridSpec(1,2)  gs00=gridspec.GridSpecFromSubplotSpec(3,3,subplot_spec=gs0[0])  matplotlib.gridspec.GridSpecFromSubplotSpec(nrows, ncols, subplot_spec,  wspace=None, hspace=None,height_ratios=None,width_ratios=None)
```

创建一个`GridSpec`，它的`subplot layout parameter`继承自指定的`SubplotSpec`。 其中`nrows`为网格行数，`ncols`为网格列数，`subplot_spec`为指定的`SubplotSpec`。


![从`SubplotSpec`创建`GridSpec`](./../imgs/GridSpec_from_SubplotSpec.JPG)

1. 默认情况下，`GridSpec`创建的网格都是相同大小的。当然你可以调整相对的高度和宽度。注意这里只有相对大小（即比例）是有意义的，绝对大小值是没有意义的。如：

```
xxxxxxxxxx  gs=gridspec.GridSpec(2,2,width_ratios=[1,2],height_ratios=[4,1]  plt.subplot(gs[0]  ....
```

这里`width_ratios`关键字参数指定了一行中，各列的宽度比例（有多少列就有多少个数字）； `height_ratios`关键字参数指定了一列中，各行的高度比例（有多少行就有多少个数字）。

![不同大小的`GridSpec`网格](./../imgs/GridSpec_different_size.JPG)

2. GridSpec.tight_layout()

`GridSpec.tight_layout(fig, renderer=None, pad=1.08, h_pad=None, w_pad=None,rect=None)`: `tight_layout`能够自动调整`subplot param`从而使得`subplot`适应`figure area`。 它仅仅检查`ticklabel、axis label、title`等内容是否超出绘制区域。其参数为：

    * `fig`关键字参数：`Figure`对象，图表。
    * `pad`关键字参数：一个浮点数，单位是`fontsize`，表示`figure edge` 和 `edges of subplots`之间的 填充区域。
    * `h_pad`关键字参数：一个浮点数，单位是`fontsize`，示`subplots`之间的高度，默认为`pad`。
    * `w_pad`关键字参数：一个浮点数，单位是`fontsize`，示`subplots`之间的宽度，默认为`pad`。
    * `rect`关键字参数：如果给定了该参数为一个列表或元组（是一个矩形的四要素，分别代表左下角坐标，宽度，高度），则指定了网格的轮廓矩形，所有的`subplots`都位于该矩形中。其坐标系是`figure coordinate`，从`[0...1]`，如果没有提供该参数，则默认为`(0, 0, 1, 1)`。

当然你可以使用`matplotlib.pyplot.tight_layout()`来达到同样的效果。

![`GridSpec.tight_layout()`](./../imgs/tight_layout.JPG)


## 五、 Path

1. `matplotlib.patch`对象底层的对象就是`Path`。它的基本用法如下：

```
xxxxxxxxxx  import matplotlib.pyplot as plt  from matplotlib.path import Path  import matplotlib.patches as patches  verts = [  (0., 0.), # left, bottom  (0., 1.), # left, top  (1., 1.), # right, top  (1., 0.), # right, bottom  (0., 0.), # ignored  ]  codes = [Path.MOVETO,  Path.LINETO,  Path.LINETO,  Path.LINETO,  Path.CLOSEPOLY,  ]  path = Path(verts, codes)  fig = plt.figure()  ax = fig.add_subplot(111)  patch = patches.PathPatch(path)  ax.add_patch(patch)  ax.set_xlim(-2,2)  ax.set_ylim(-2,2)  plt.show()
```

![`Path`](./../imgs/Path.JPG)

2. `PATH`对象的创建通过`matplotlib.path.Path(verts,codes)`创建，其中：

    * `verts`：`PATH`的顶点。这些顶点必须构成一个封闭曲线。其中每个顶点必须指定`x`坐标和`y`坐标。

    * `codes`：指示如何使用这些`PATH`顶点。它与`verts`关系是一一对应的。有如下指令：

        * `Path.STOP`：结束`path`的标记
        * `Path.MOVETO`：画笔提起并移动到指定的顶点
        * `Path.LINETO`：画笔画直线，从`current position`到指定的顶点
        * `Path.CURVE3`:画笔画二阶贝塞尔曲线，从`current position`到指定的`end point`， 其中还有一个参数是指定的`control point`
        * `Path.CURVE4`：画笔画三阶贝塞尔曲线，从`current position`到指定的`end point`， 其中还有两个参数是指定的`control points`
        * `Path.CLOSEPOLY`：指定的`point`参数被忽略。该指令画一条线段， 从`current point`到`start point`


可以通过`matplotlib.patches.PathPatch(path)`来构建一个`PathPatch`对象，然后通过`Axes.add_patch(patch)`向`Axes`添加`PathPatch`对象.这样就添加了`Path`到图表中。

![贝塞尔曲线](./../imgs/bezier_path.JPG)

3. 在`matplotlib`中所有简单的`patch primitive`，如`Rectangle`、`Circle`、`Polygon`等等，都是由简单的`Path`来实现的。而创建大量的`primitive`的函数如`hist()`和`bar()`（他们创建了大量的`Rectanle`）可以使用一个`compound path`来高效地实现。

> > 

> 但是实际上`bar()`创建的是一系列的`Rectangle`，而没有用到`compound path`，这是由于历史原因，是历史遗留问题。（`bar()`函数先于`Coupound Path`出现）



下面是一个`Compound Path`的例子：

```
xxxxxxxxxx  ...   verts = np.zeros((nverts, 2))  # nverts为顶点的个数加1（一个终止符）  codes = np.ones(nverts, int) * Path.LINETO  ## 设置 codes :codes分成5个一组，  ## 每一组以Path.MOVETO开始，后面是3个Path.LINETO，最后是Path.CLOSEPOLY   codes[0::5] = Path.MOVETO  codes[4::5] = Path.CLOSEPOLY  ## 设置顶点 verts ##  ...  ## 创建 Path 、PathPatch并添加  ##  barpath = Path(verts, codes)  patch = patches.PathPatch(barpath, facecolor='green',edgecolor='yellow', alpha=0.5)  fig = plt.figure()  ax = fig.add_subplot(111)  ax.add_patch(patch)  ax.show()
```

> > 

> 在创建`Axes`或者`SubPlot`时，可以给构造函数提供一个`axisbg`参数来指定背景色




## 六、 path effect

1. `matplotlib`的`patheffects`模块提供了一些函数来绘制`path effect`，该模块还定义了很多`effect`类。可以应用`path effect`的`Artist`有：`Patch`、`Line2D`、`Collection`以及`Text`。每个`Artist`的`path effect`可以通过`.set_path_effects()`方法控制，其参数是一个可迭代对象，迭代的结果是`AbstractPathEffect`实例；也可以通过`Artist`构造函数的`path_effects=`关键字参数控制。

> > 

> 注意：`effect`类的关键字参数比如背景色、前景色等与`Artist`不同。因为这些`effect`类是更低层次的操作。



2. 所有的`effect`类都继承自`matplotlib.patheffects.AbstractPathEffect`类。`AbstractPathEffect`的子类要覆盖`AbstractPathEffect`类的`.draw_path(...)`方法。

`AbstractPathEffect`类的构造函数有个`offset`关键字参数，表示`effect`偏移(默认为`(0,0)`)

3. 最简单的`effect`是`normal effect`，它是`matplotlib.patheffects.Normal`类。它简单的绘制`Artist`，不带任何`effect`。

如：

```
xxxxxxxxxx  import matplotlib.pyplot as plt  import matplotlib.patheffects as path_effects  fig = plt.figure(figsize=(5, 1.5))  text = fig.text(0.5, 0.5, 'Hello path effects world!\nThis is the normal path effect.',  ha='center', va='center', size=20)  text.set_path_effects([path_effects.Normal()])  plt.show()
```

![`normal effect`](./../imgs/normal_effect.JPG)

4. 我们可以在基于`Path`的`Artist`上应用`drop-shadow effect`（下沉效果）。如可以在`filled patch Artist`上应用`matplotlib.patheffects.SimplePatchShadow`，在`line patch Artist`上应用`matplotlib.patheffects.SimpleLineShadow`。

![`drop-shadow effect`](./../imgs/drop_shadow_effect.JPG)

你可以通过`path_effects=[path_effects.with*()]`来指定`path_effects`参数，或者直接通过`path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()]`来指定`path_effects`参数。

    * 前者会自动地在`normal effect`后跟随指定的`effect`
    * 后者会显式的指定`effect`

5. `Strok effect`可以用于制作出`stand-out effect`（突出效果）。

![`stand-out effect`](./../imgs/stand_out_effect.JPG)

6. `PathPatchEffect`是一个通用的`path effect`类。如果对某个`PathPatch`设置了`PathPatchEffect`，则该`effect`的`.draw_path(...)`方法执行的是由初始`PathPatch`计算的得到的一个新的`PathPatch`。

与一般的`effect`类不同，`PathPatchEffect`类的关键字参数是与`PathPatch`一致的，因为除了`offset`关键字参数外，其他的任何关键字参数都会传递给`PathPatch`构造函数。如：

```
xxxxxxxxxx  import matplotlib.pyplot as plt  import matplotlib.patheffects as path_effects  fig = plt.figure(figsize=(8, 1))  t = fig.text(0.02, 0.5, 'Hatch shadow', fontsize=75, weight=1000, va='center')  t.set_path_effects([path_effects.PathPatchEffect(offset=(4, -4), hatch='xxxx',  facecolor='gray'),  path_effects.PathPatchEffect(edgecolor='white', linewidth=1.1,  facecolor='black')])  plt.show()
```

![`PathPatchEffect`](./../imgs/PathPatchEffect.JPG)


## 七、坐标变换

1. `matplotlib`中有四个坐标系：

    * 用户级的`data`坐标系：坐标转换对象为`ax.transData`。它是用户级坐标系，由`xlim`和`ylim`控制
    * `Axes`坐标系：坐标转换对象为`ax.transAxes`。它是`Axes`的坐标系，`(0,0)`为`Axes`的左下角，`(1,1)`为`Axes`的右上角。
    * `Figure`坐标系：坐标转换对象为`fig.transFigure`。它是`Figure`的坐标系，`(0,0)`为`Figure`的左下角，`(1,1)`为`Figure`的右上角。
    * `display`坐标系：它没有坐标转换对象。它显示的是`display`的像素坐标系，`(0,0)`为`display`的左下角，`(width,height)`为`display`的右上角。

前面三个坐标系的坐标转换对象有方法执行坐标转换，这些方法接受输入并产生输出：输入为本坐标系内的坐标点，输出为`display`坐标系中的坐标。（因此`display`坐标系没有坐标转换对象）。当然他们也有相关方法将来自于`display`坐标系中的坐标转换回本坐标系内的坐标。

2. 在`Artist`的构造函数中传入`transform`关键字参数（其值为坐标转换对象），就能够切换坐标系。如：`ax.text(0.05,0.95,label,"This is a Text",transform=ax.transAxes)`，将`Text`放置于`Axes`坐标系中的`(0.05,0.95)`位置处。

> > 

> 通常不建议直接使用`display`坐标系。因为它固定了绝对坐标，导致你`resize`图表时你必须重新定位坐标。所以你必须监听`resize`事件，非常麻烦。




### 1. 用户的 data 坐标系

1. 当调用`ax.set_xlimit(x_min,x_max)`以及`ax.set_ylimit(y_min,y_max)`时，即建立起了用户`data`坐标系。左下角坐标为`(x_min,y_min)`，右上角坐标为`(x_max,y_max)`。

> > 

> 有时候你可能并没有显式调用`.set_xlimit()`以及`.set_ylimit()`。其实`matplotlib`会隐式调用它们来设置坐标轴的数据范围。



```
xxxxxxxxxx  import matplotlib.pyplot as plt  fig = plt.figure()  ax = fig.add_subplot(111)  ax.set_xlim(0, 10)  ax.set_ylim(-1, 1)  type(ax.transData)  ax.transData.transform((5, 0))
```

2. 你可以调用`ax.transData`返回`data`坐标系的坐标转换对象。对该坐标转换对象调用`.transform(point)`方法会返回`point`在`display`坐标系下的坐标。其中`point`是点在`data`坐标系下的坐标`(x,y)`。你也可以给`.transform()`方法一次传入多个点的坐标，此时输出也是对应于`display`坐标系下的一系列坐标。

3. 你可以对`ax.trandData`返回的坐标转换对象调用`.inverted()`方法。该方法返回的是一个坐标逆转换对象。对该坐标逆转换对象调用`.transform(point)`方法会返回`point`在`data`坐标系下的坐标。其中`point`是点在`display`坐标系下的坐标`(x,y)`。你也可以给`.transform()`方法一次传入多个点的坐标，此时输出也是对应于`data`坐标系下的一系列坐标。

4. 当你调用了`ax.set_xlim()`或者`ax.set_ylim()`时，坐标转换对象会实时更新。

![用户的`data`坐标系](./../imgs/data_transform.JPG)


### 2. Axes 坐标系

1. 在`Axes`坐标系中，`(0,0)`位于`Axes`的左下角，`(1,1)`位于`Axes`的右上角，`(0.5,0.5)`位于`Axes`的中心。当然你可以引用位于这之外的点，如`(-0.1,1.1)`。
2. 通常如果你需要在`Axes`中放置一些文字说明，那么一般都是采用`Axes`坐标系来定位。这样无论图形怎么缩放，这些`Text`都能位于正确的位置。
3. 你也可以在`Axes`中通过`Axes`坐标系添加一些`Patch`，但是通常建议在`data`坐标系下添加。因为你在`Axes`中添加的图表当图表缩放时可能会出现问题。

### 3. 混合坐标系

1. 有时候你需要混合`data`坐标系和`Axes`坐标系。通过`matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes)` 能够返回一个混合坐标系，该坐标系中：`x`坐标为`data`坐标系，`y`坐标为`Axes`坐标系。因此该坐标系中`(1,1)`表示的是`data`坐标系中`x=1`但是`y`位于最上方的点。

![混合坐标系](./../imgs/blended_transform.JPG)

2. 有两个函数返回特定的混合坐标系：

    * `matplotlib.axes.Axes.get_xaxis_transform()`:等价于 `matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes)`。 `x`坐标为`data`坐标系，`y`坐标为`Axes`坐标系。常用于绘制`x`轴的`label`、`tick`、`gridline`。
    * `matplotlib.axes.Axes.get_yaxis_transform().`:等价于 `matplotlib.transforms.blended_transform_factory(ax.transAxes,ax.transData)`。 `x`坐标为`Axes`坐标系，`y`坐标为`data`坐标系。常用于绘制`y`轴的`label`、`tick`、`gridline`。


### 4. 利用坐标变换制造阴影效果

1. `matplotlib.transform.ScaledTranslation(xt, yt, scale_trans)`创建一个新的坐标转换对象，该坐标转换由`xt`和`yt`经过`scale_trans`坐标转换而来。

> > 

> 它创建的是一个偏移对于的坐标变换。偏移的坐标是位于`scale_trans`中的。



    * 制作阴影的时候，将阴影的`zorder`调小，从而使得阴影首先绘制并位于底层

    * 当`scale_trans`为`fig.dpi_scale_trans`坐标转换对象时，`xt`,`yt`的单位是像素。还有一个方法也能达到同样的效果：`matplotlib.transforms.offset_copy(trans,x=xt,y=yt,units='inches')`，但是该方法返回的坐标转换对象是`trans`合成了偏移之后的效果。

    ![制造阴影效果](./../imgs/transform_make_shadow_effect.JPG)



### 5. 直角坐标系、对数坐标系、极坐标系

1. 通过`Axes.set_xscale(value,**kwargs)`/`Axes.set_yscale(value,**kwargs)`方法可以设置`x`轴/`y`轴是否对数坐标。其中`value`可以为:

    * `linear`：线性
    * `log`：对数。其中`basex`|`basey`关键字指定对数的基<br></br>
    * `logit`：以2为底的对数
    * `symlog`：对数，其中`basex`|`basey`关键字指定对数的基

你也可以通过`matplotlib.pyplot.xscale()`和`matplotlib.pyplot.yscale()`来设置对数坐标。一定要先添加数据后设置对数坐标。

![对数坐标](./../imgs/log_coorinate.JPG)

2. 通过`Figure.add_axes((left,bottom,width,height), projection='polar')`或者`Figure.add_axes((left,bottom,width,height), polar=True)`方法可以创建一个极坐标的`Axes`。其中`polar`关键字是为了兼容旧代码，新代码推荐用`projection`关键字，因为`projection`关键字不仅可以设置极坐标，还可以设置自定义坐标（它将坐标统一为映射关系）。

> > 

> `Figure.add_subplot(...)`也是同样的设置



![级坐标](./../imgs/polar_coordinate.JPG)


## 八、 3D 绘图

1. 3D绘图与2D绘图的调用方法几乎相同，除了增加一个 `projection='3d'`的关键字参数。

```
xxxxxxxxxx  import matplotlib.pyplot as plt  from mpl_toolkits.mplot3d import Axes3D  fig=plt.figure()  ax=fig.add_addsubplot(111,projection='3d') # 旧式写法  ax=Axes3D(fig) #新式写法
```

![3d_new_style](../imgs/3d_new_style.JPG)

2. 绘制直线：`Axes3D.plot(xs, ys, *args, **kwargs)`。其参数为：

    * `xs,ys`：点的 `x,y`坐标
    * `zs`：点的`z`坐标。该值可以是一个标量（表示对所有点都取同一个值）；也可以是个数组或列表，表示每个点一个值
    * `zdir`：指定那个是`z`轴。其值可以是`'x'`或者`'y'`或者`'z'`
    * 剩下的关键字参数与`Axes.plot()`相同

3. 绘制散点图：`Axes3D.scatter(xs, ys, zs=0, zdir=’z’, s=20, c=’b’, depthshade=True, *args, **kwargs)`。其参数为：

    * `xs,ys`：点的 `x,y`坐标
    * `zs`：点的`z`坐标。该值可以是一个标量（表示对所有点都取同一个值）；也可以是个数组或列表，表示每个点一个值
    * `zdir`：指定那个是`z`轴。其值可以是`'x'`或者`'y'`或者`'z'`
    * `s`：散点的大小（单位为 `point^2`).该值可以是一个标量（表示对所有点都取同一个值）；也可以是个数组或列表，表示每个点一个值
    * `c`：散点的颜色。你可以将它设为一个颜色字符串，表示所有的点都是一个颜色。或者是个 `cmap`，指定颜色图
    * `depthshade`：一个布尔值。如果为`True`，则通过对`marker`设置阴影来展示层次关系
    * 剩下的关键字参数与`Axes.scatter()`相同

4. 绘制线框：`Axes3D.plot_wireframe(X, Y, Z, *args, **kwargs)`。其参数为：

    * `X,Y`：点的 `x,y`坐标
    * `Z`：点的`z`坐标。该值可以是一个标量（表示对所有点都取同一个值）；也可以是个数组或列表，表示每个点一个值
    * `rstride`：行的步长
    * `cstride`：列的步长
    * 剩下的关键字传递给`LineCollection`


## 九、技巧

### 1. 共享坐标轴

1. 当你通过`pyplot.subplot()`、`pyplot.axes()`函数或者`Figure.add_subplot()`、`Figure.add_axes()`方法创建一个`Axes`时，你可以通过`sharex`关键字参数传入另一个`Axes`表示共享X轴；或者通过`sharey`关键字参数传入另一个`Axes`表示共享Y轴。

共享轴线时，当你缩放某个`Axes`时，另一个`Axes`也跟着缩放。

![共享坐标轴](./../imgs/share_axis.JPG)


### 2. 创建多个 subplot

1. 如果你想创建网格中的许多`subplot`，旧式风格的代码非常繁琐：

```
xxxxxxxxxx  #旧式风格  fig=plt.figure()  ax1=fig.add_subplot(221)  ax2=fig.add_subplot(222,sharex=ax1,sharey=ax1)  ax3=fig.add_subplot(223,sharex=ax1,sharey=ax1)  ax4=fig.add_subplot(224,sharex=ax1,sharey=ax1)
```

新式风格的代码直接利用`pyplot.subplots()`函数一次性创建：


```
xxxxxxxxxx    #新式风格的代码    fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2,sharex=True,sharey=True)    ax1.plot(...)    ax2.plot(...)    ...
```

它创建了`Figure`和对应所有网格`SubPlot`。你也可以不去解包而直接：

```
xxxxxxxxxx    #新式风格的代码    fig,axs=plt.subplots(2,2,sharex=True,sharey=True)    ax1=axs[0,0]    ax2=axs[0,1]    ax3=axs[1,0]    ax4=axs[1,1]    ...    ...
```

返回的`axs`是一个`nrows*ncols`的`array`，支持`numpy`的索引。

### 3. 调整日期显示

1. 当`x`轴为时间日期时，有可能间隔太密集导致显示都叠加在一起。此时可以用`matplotlib.figure.Figure.autofmt_xdate()`函数来自动调整X轴日期的显式。

你也可以调整X轴的显示格式。当X轴为时间时，其显示由`Axes.fmt_xdata`属性来提供。该属性是一个函数对象或者函数，接受一个日期参数，返回该日期的显示字符串。`matplotlib`已经提供了许多`date formatter`，你可以直接使用`ax.fmt_xdata=matplotlib.dates.DateFormatter('%Y-%m-%d')`

![日期显示](./../imgs/axis_date_adjust.JPG)


### 4. 放置 text box

1. 当你在`Axes`中放置`text box`时，你最好将它放置在`axes coordinates`下，这样当你调整X轴或者Y轴时，它能够自动调整位置。

你也可以使用`Text`的`.bbox`属性来让这个`Text`始终放在某个`Patch`中。其中`.bbox`是个字典，它存放的是该`Patch`实例的属性。

![text_box](./../imgs/text_box.JPG)


### 5. LATEX文字

1. 要想在文本中使用`LATEX`，你需要使用`'$...$'`这种字符串（即使用`'$'`作为界定符）。通常建议使用`raw`字符串，即`r'$...$'`的格式，因为原生字符串不会转义`'\'`，从而使得大量的`LATEX`词法能够正确解析。

### 6. 平移坐标轴：

1. `Axes.spines`是个字典，它存放了四个键，分别为： `Axes.spines['left],Axes.spines['right],Axes.spines['top],Axes.spines['bottom]` 他们都是一个`matplotlib.spines.Spine`对象，该对象继承自`matplotlib.patches.Patch`对象，主要是设置图形边界的边框。

    * `Spine.set_color('none')`：不显示这条边线

    * `Spine.set_position((position))`：将边线移动到指定坐标，其中`position`是一个二元元组，指定了 `(position type,amount)`，`position type`可以是：

        * `outward`：在绘图区域之外放置边线，离开绘图区域的距离由 `amount`指定（负值则在会去区域内绘制）<br></br>
        * `axes`：在 `Axes coordinate`内放置边线（从 0.0 到 1.0 ）
        * `data`：在 `data coordinate` 内放置边线

    你也可以指定`position`为 ： `'center'`，等价于 `('axes',0.5)`；或者 `'zero'`，等价于 `('data',0.0)` ![move_axis](./../imgs/move_axis.JPG)



### 7. 清除绘图

1. 你可以通过 `pyplot`来清除绘图：

    * `pyplot.cla()`：清除`current axis`。非当前`axis`不受影响
    * `pyplot.clf()`：清除`current figure`。但是它不关闭`window`
    * `pyplot.close()`：关闭`window`

2. 你也可以通过面向对象的方法：

    * `Figure.clf()`：清除该`Figure`对象的所有内容。


### 8. 清除X坐标和Y坐标：

```
xxxxxxxxxx  Axes.set_xticks(())  Axes.set_yticks(())  Axes.set_axis_off() #清除 tick 和边框
```

### 9. 设置中文

在`linux` 下，为了支持中文，则在开头设置：

```
xxxxxxxxxximport matplotlib.pyplot as pltplt.rcParams['font.sans-serif'] = ['SimHei']  #matplotlib 中文字体
```




</body>