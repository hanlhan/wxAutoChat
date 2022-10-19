<body class="typora-export">
# pandas 0.19

## 一、基本数据结构

1. `Pandas`的两个主要数据结构： `Series`和`DateFrame`

### 1. Series

1. 创建： `class pandas.Series(data=None, index=None, dtype=None, name=None, copy=False,fastpath=False)`:

参数：

    * `data`：它可以是一个字典、`array-like`、标量。表示`Series`包含的数据，如果是序列/数组，则它必须是一维的
    * 如果是字典，则字典的键指定了`label`。如果你同时使用了`index`，则以`index`为准。
    * 如果是标量，则结果为：该标量扩充为`index`长度相同的列表。
    * `index`：一个`array-like`或者一个`Index`对象。它指定了`label`。其值必须唯一而且`hashable`，且长度与`data`一致。如果`data`是一个字典，则`index`将会使用该字典的`key`（此时`index`不起作用）。如果未提供，则使用`np.arange(n)`。
    * `name`：一个字符串，为`Series`的名字。
    * `dtype`：指定数据类型。如果为`None`，则数据类型被自动推断
    * `copy`：一个布尔值。如果为`True`，则拷贝输入数据`data`

![create](../imgs/Series/create.JPG)

2. 还可以通过类方法创建`Series`：`Series.from_array(arr, index=None, name=None, dtype=None,` `copy=False, fastpath=False)`：其中`arr`可以是一个字典、`array-like`、标量。其他参数见1.

3. 我们可以将`Series`转换成其他数据类型：

    * `.to_dict()`：转换成字典，格式为`{label->value}`
    * `.to_frame([name])`：转换成`DataFrame`。`name`为`Index`的名字
    * `.tolist()`：转换成列表

![transform](../imgs/Series/transform.JPG)

4. 可以将`Series`转换成字符串：

```
.to_string(buf=None, na_rep='NaN', float_format=None, header=True, index=True,   length=False, dtype=False, name=False, max_rows=None)
```

    * `buf`：一个`StringIO-like`对象，是写入的`buffer`
    * `na_rep`：一个字符串，代表数值`NaN`
    * `float_format`：浮点数的格式化函数。应用于浮点列
    * `header`：一个布尔值。如果为`True`，则添加头部信息（`index name`）
    * `index`：一个布尔值。如果为`True`，则添加`index labels`
    * `length`：一个布尔值。如果为`True`，则添加`Series`的长度信息
    * `dtype`：一个布尔值。如果为`True`，则添加`dtype`信息
    * `name`：一个布尔值。如果为`True`，则添加`Series name`
    * `max_rows`：一个整数值，给出了最大转换的行数。如果为`None`，则转换全部。

返回转换后的字符串。 ![to_string](../imgs/Series/to_string.JPG)


### 2. Index

1. `class pandas.Index(data=None, dtype=None, copy=False, name=None,` `fastpath=False, tupleize_cols=True)`：创建`Index`对象。

参数：

    * `data`：一个`array-like`，必须是一维的
    * `name`：一个字符串，为`Index`的名字。
    * `dtype`：指定数据类型。如果为`None`，则默认为`object`
    * `copy`：一个布尔值。如果为`True`，则拷贝输入数据`data`
    * `tupleize_cols`：一个布尔值，如果可能则尽量创建`MultiIndex`对象

![create](../imgs/Index/create.JPG)

2. `Index`对象负责管理轴`label`和其他元数据（比如轴`name`）。构建`Series/DataFrame`时，传给`index/columns`关键字的任何数组或者序列都将被转化成一个`Index`。`Index` 对象是`immutable`，因此用户无法对其进行修改。这样才能够使得`Index`对象在多个数据结构之间安全共享<br></br>

3. 存在多种索引类型。

    * `Index`：最泛化的`Index`对象，将轴`label`表示为一个`Python`对象组成的`Numpy`数组
    * `Int64Index`：针对整数的特殊`Index`
    * `MultiIndex`：层次化索引对象，表示单个轴上的多层索引。可以看做由元组组成的数组
    * `DatatimeIndex`：存储纳秒级时间戳，用`numpy`的`datatime64`类型表示
    * `PeriodIndex`：针对`Period`数据（时间间隔）的特殊`Index`

4. `Index`的功能类似一个固定大小的集合。其类似于集合的方法有（因为`Index`不可变，因此返回的都是新的`Index`对象）：

    * `.copy([name,deep,dtype])`：返回一份`Index`的拷贝。
    * `.append(other)`：连接另一个`Index`对象，产生一个新的`Index`对象。注意重复的`label`并不会合并
    * `.difference(other)`：计算差集，返回一个`Index`对象
    * `.intersection(other)`：计算交集，返回一个`Index`对象
    * `.union(other)`：计算并集，返回一个新的`Index`对象
    * `.isin(values[, level])`：计算`Index`中各`label`是否在`values`中
    * `.delete(loc)`：删除下标`loc`处的元素，得到新的`Index`
    * `.drop(labels[, errors])`：删除传入的`labels`，得到新的`Index`
    * `.insert(loc, item)`：在指定下标位置插入值，得到新的`Index`
    * `.unique()`：返回`Index`中唯一值的数组，得到新的`Index`

![method_set](../imgs/Index/method_set.JPG)

5. 我们可以将`Index`转换成其他数据类型：

    * `.astype(dtype,[,copy])`：转换成另一个数据类型的`Index`，其`label`的`dtype`被转换成指定的值
    * `.tolist()`：转换成列表
    * `.to_series(**kwargs)`：转换成`Series`，`Series`的数据和`label`相同

![transform](../imgs/Index/transform.JPG)

6. `Index`提供的选取方法有：

    * `.get_indexer(target[, method, limit, ...])` ：获取`target`（一个`Index`对象）对应的下标列表。

        * `target`：一个`Index`对象。我们要考察的就是`Index`中的每个`label`在`self`中的下标序列。

        * `method`：指定`label`的匹配方法。可以为`None`，表示严格匹配（如果不存在则下标为 -1）。如果为`'pad'/'ffill'`，则：若未找到匹配的，则使用前向匹配。如果为`'backfill'/'bfill'`，则：若未找到匹配的，则使用后向匹配。如果为`'nearest'`，则：若未找到匹配的，则使用最近邻匹配。

        >         > 

        > 匹配时，假设你的`Index`的`label`是有序排列的（要么是升序，要么是降序）



        * `limit`：一个整数，指定前向/后向/最近填充时：如果有连续的`k`个`NaN`，则只填充其中`limit`个。

        * `tolerance`：一个整数，用于给出在不匹配时，连续采用前向/后向/最近邻匹配的跨度的最大值。


    * `.get_level_values(level)`：返回指定`level`的`Index`，用于`MultiIndex`。

    * `.get_loc(key[, method, tolerance])`：返回指定`label`处的下标，由`key`指定。其中`method`和`tolerance`参数见上述。如果`method=None`，且`key`指定的`label`找不到，则抛出异常。

    * `.get_value(series, key)`：寻找`Series`指定`label`处的值。若`key`指定的`label`找不到，则抛出异常。

    * `.slice_locs([start, end, step, kind])`：计算给定`start label`和`end label`之间的下标序列，返回代表该下标序列的切片或者数组。其中不包括`end`。 ![select](../imgs/Index/select.JPG)



### 3. MultiIndex

1. `MultiIndex`代表的是多级索引对象。它继承自`Index`，其中的多级`label`采用元组对象来表示。在`MultiIndex`内部，并不直接保存元组对象，而是使用多个`Index`对象保存索引中每级的`label`。

2. `class pandas.MultiIndex(levels=None, labels=None, sortorder=None, names=None,` `copy=False, verify_integrity=True, _set_identity=True, name=None, **kwargs)`

参数：

    * `levels`：一个数组的列表，给出了每一级的`level`。

    * `labels`：一个数组的列表，给出了每一级`level`的下标。第`i`级`label`是这样产生的：

        * 首先获取`labels[i]`，它是一个下标序列，代表第<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-8-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 345 858.4" width="0.801ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E8-MJMATHI-69" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E8-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-8" type="math/tex">i</script>级。
        * 假设第 `k`位置为整数 3，在第<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-8-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 345 858.4" width="0.801ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E8-MJMATHI-69" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E8-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-8" type="math/tex">i</script>级第<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-17-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 521 858.4" width="1.21ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E17-MJMATHI-6B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E17-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-17" type="math/tex">k</script>位的`label`就是`levels[i][3]`。

    * `sortorder`：一个整数，给出了已经排序好了的`level`级别。

    * `names`：一个字符串序列，给出了每个`Index`的`name`。其中每个级别对应一个`Index`

    * `copy`：一个布尔值。如果为`True`，则拷贝基础数据

    * `verify_integrity`：一个布尔值。如果为`True`，则检测各级别的`label/level`都是连续的且有效的

    * `name`：指定了本`MultiIndex`的名字


你也可以通过下面的类方法来创建`MultiIndex`：

    * `MultiIndex.from_arrays(arrays[, sortorder, ...])`：将二维序列转换为`MultiIndex`。其中`arrays`为`array-like`的序列，每个`array-like`按顺序的给出了一列`label`（一个级别）
    * `MultiIndex.from_tuples(tuples[, sortorder, ...])` ：将元组序列转换为`MultiIndex`。其中`tuples`为`tuple-like`的序列，每个`array-like`按顺序的给出了一行`label`对（不同级别的一对）
    * `MultiIndex.from_product(iterables[, ...])`：根据多个可迭代对象生成一个`MultiIndex`，其中使用笛卡尔积的算法。其中`iterables`为可迭代对象的序列

你也可以通过传递一个元组列表给`Index()`，并且将`tupleize_cols`设置为`True`来创建`MultiIndex`

![MultiIndex_create](../imgs/Index/MultiIndex_create.JPG)


### 4. DataFrame

1. `DataFrame` 是一个表格型的数据结构，它含有一组有序的列，每一列都可以是不同的值类型（数值、日期、`object`类型）。其中`object`类型可以保存任何`python`对象，比如字符串。同一列必须是相同的值类型。

    * `DataFrame` 既有行索引，又有列索引。他可以被看作为`Series`组成的字典（共用同一个行索引）
    * `DataFrame`中面向行和面向列的操作基本上是平衡的。其实`DataFrame`中的数据是以一个或者多个二维块存放的

![DataFrameImg](../imgs/DataFrame/DataFrameImg.png)

2. `class pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)`：

    * `data`：可以是一个二维数组、字典、或者`DataFrame`。
    * `index`：一个`Index`或者`array-like`对象（必须为一维的），它指定了行标签。如果未提供，则使用`np.arange(n)`。
    * `columns`：一个`Index`或者`array-like`对象（必须为一维的），它指定了列标签。如果未提供，则使用`np.arange(n)`。
    * `dtype`：指定数据类型。如果为`None`，则数据类型被自动推断
    * `copy`：一个布尔值。如果为`True`，则拷贝输入数据`data`

常见的构造`DataFrame`有以下情况：

    * 二维`ndarray`：`data`就是数据，此时可以传入`index/columns`参数 ![create_ndarray](../imgs/DataFrame/create_ndarray.JPG)
    * 一个字典，其中字典的值为一维数组、一维列表、一维元组：此时每个键就是列索引，对应的值就是列数据。要求所有序列的长度相同 ![create_dict_list](../imgs/DataFrame/create_dict_list.JPG)
    * `numpy`的结构化数组：类似于由数组组成的字典
    * `Series`组成的字典：此时每个键就是列索引，对应的`Series`就是列数据。如果没有显式的指定行索引，那么各个`Series`的索引将会被合并成`DataFrame`的行索引。 ![create_dict_Series](../imgs/DataFrame/create_dict_Series.JPG)
    * 字典的字典：各个内层字典会成为一列，键会被合并成结果的行索引。跟`Series 组成的字典`情况一致
    * 字典或者`Series`的列表：每一项将会成为`DataFrame`的一行。字典的键、`Series`索引的并集将会成为`DataFrame`的列索引 ![create_list_Series](../imgs/DataFrame/create_list_Series.JPG)
    * 列表、元组组成的列表：类似于二维`ndarray`
    * 另一个`DataFrame`：该`DataFrame`的索引将会被沿用，除非显式指定其他索引 ![create_frame](../imgs/DataFrame/create_frame.JPG)
    * `numpy`的`MaskedArray`：类似于二维`ndarray`，只是掩码值在结果`DataFrame`中会变成`NA/缺失值`

> > 

> `columns`/`index`有两种作用：如果构造的`DataFrame`没有索引，则它们分别给索引赋值；如果构造的`DataFrame`已有索引，则它们按照指定顺序排列指定的索引。



3. 可以通过下面的类方法从其他数据结构中创建`DataFrame`：

    * `DataFrame.from_dict(data, orient='columns', dtype=None)`：从字典中创建`DataFrame`。

        * `data`：是个字典，其格式为： `{key:array-like}`或者`{key:dict}`。
        * `orient`：指定了`key`为行还是列。参数的值为`'columns'`（`key`为列的`label`，默认行为）；或者`'index'`（`key`为行的`label`）
        * `dtype`：数据类型。如果为`None`，则自动推断。


![from_dict](../imgs/DataFrame/from_dict.JPG)

    * `DataFrame.from_items(items, columns=None, orient='columns')`：从元组序列中创建`DataFrame`。

        * `items`：为元组序列，元组格式为：`(key,value)`，其中`value`为表示一维数据的序列或者`Series`对象。

        * `columns`：一个序列，给出列的`labels`。

            * 当`orient='index'`时必须传入（此时`key` 指定的是行的`label`），且长度不能大于`DataFrame`的列数。
            * 当`orient='columns`时，`key`就是列的`label`，此时`columns`关键字参数指定的列`label`必须等于某个`key`；否则抛出异常。


    * `orient`：参见`.from_dict`的解释。


![from_items](../imgs/DataFrame/from_items.JPG)

4. 你可以将`DataFrame`转换为其他数据类型。

    * `.to_dict(*args, **kwargs)`方法：转换成字典。参数`orient`决定了转换方式。

        * `orient ='dict'`：字典的形式为： `{col_label:{index_label:value}}`（默认行为）
        * `orient ='list'`：字典的形式为： `{col_label:[values]}`
        * `orient ='series'`：字典的形式为： `{col_label:Series(values)}`
        * `orient ='split'`：字典的形式为： `{'index':[index_labels],'columns':[col_labels],'data':[values]}`
        * `orient ='records'`：字典的形式为： `[{col_label:value},...,{col_label:value}]`
        * `orient ='index'`：字典的形式为： `{index_label:{col_label:value}}`
        * 你可以使用简化字符串，如`'s'`代表`'series'`，`'sp'`代表`'split'`

    * `.to_records(index=True, convert_datetime64=True)`方法：转换成结构数组。

        * `index`：一个布尔值。如果为`True`，则结果中包含`index`
        * `convert_datetime64`：一个布尔值，如果为`True`，则转换`DatetimeIndex`为`datetime.datetime`


![transform_1](../imgs/DataFrame/transform_1.JPG) ![transform_2](../imgs/DataFrame/transform_2.JPG)

5. 可以将`DateFrame`转换成字符串：

```
xxxxxxxxxxto_string(buf=None, columns=None, col_space=None, header=True, index=True,  na_rep='NaN', formatters=None, float_format=None, sparsify=None,   index_names=True, justify=None, line_width=None, max_rows=None,  max_cols=None, show_dimensions=False)
```

    * `buf`：一个`StringIO-like`对象，是写入的`buffer`

    * `columns`：一个序列，指定了列标签的一个子集，该子集的数据被输出

    * `col_space`：一个整数，指定了每一列的最小宽度

    * `header`：一个布尔值。如果为`True`，则添加头部信息（`column labels`）

    * `index`：一个布尔值。如果为`True`，则添加`index labels`

    * `na_rep`：一个字符串，代表数值`NaN`

    * `float_format`：浮点数的格式化函数（单参数）。应用于浮点列

    * `formatters`：一个单参数函数的列表（列表长度等于列数）或者一个单参数函数的字典。

        * 如果是列表，则根据列号，对应使用格式化函数
        * 如果是字典，则根据列`label`，对应使用格式化函数<br></br>

    * `sparsify`：一个布尔值。Set to False for a DataFrame with a hierarchical index to print every multiindex key at each row, default True

    * `index_names`：一个布尔值。如果为`True`，则添加`index names`

    * `justify`：指定`column label`的对齐方式。可以为`'left'`（左对齐），或者`'right'`（右对齐）。默认为`None`


返回转换后的字符串。

![to_string](../imgs/DataFrame/to_string.JPG)


## 二、 内部数据结构

1. `Index`的结构如图所示（实线为普通属性，虚线为`property`属性或者`getset_descriptor`）： ![Index](../imgs/Index/Index.JPG)

    * `.name`为普通属性，返回`Index`的名字 ![Index_name](../imgs/Index/Index_name.JPG)
    * `.values/._values`为`property`属性，返回`Index`的内部数据的视图
    * `._data`为普通属性，返回`Index`的内部数据 ![Index_data1](../imgs/Index/Index_data1.JPG) ![Index_data2](../imgs/Index/Index_data2.JPG) ![Index_data3](../imgs/Index/Index_data3.JPG) ![Index_data4](../imgs/Index/Index_data4.JPG)
    * `.shape`为`property`属性，返回内部数据的形状 ![Index_shape](../imgs/Index/Index_shape.JPG)
    * `._engine`为标签映射管理器，它负责管理`label`和下标之间的映射 ![Index_engine](../imgs/Index/Index_engine.JPG)
    * `ObjectEngine`对象使用一个哈希表对象`PyObjectHashTable`对象（由`ObjectEngine`对象的`.mmaping`属性给出，该属性是一个`getset_descriptor`）将标签映射到其对应的整数下标的。 ![Engine_mapping](../imgs/Index/Engine_mapping.JPG)

2. `MultiIndex`的结构如图所示 ![MultiIndex](../imgs/Index/MultiIndex.JPG)

    * `.name`为普通属性，返回`MultiIndex`的名字。同`Index`

    * `.values/._values`为`property`属性，返回`MultiIndex`的内部数据的视图。同`Index`

    >     > 

    > `._data`为`None`，这里是与`Index`不同。




![MultiIndex_pre](../imgs/Index/MultiIndex_pre.JPG) ![MultiIndex_data](../imgs/Index/MultiIndex_data.JPG)

    * `.shape`为`property`属性，返回内部属性的形状 。同`Index`
    * `._engine`为标签映射管理器，它负责管理`label`和下标之间的映射。同`Index`
    * `.labels`为`property`属性，它返回一个`FrozenList`（不可变列表），列表中存储每一级的`label`对应的下标（也就是创建`MultiIndex`时传入的`labels`参数），以`FrozenNDArray`的数据类型。 ![MultiIndex_labels](../imgs/Index/MultiIndex_labels.JPG)
    * `.levels`为`property`属性，它返回一个`FrozenList`（不可变列表），列表中存储每一级的`label`（也就是创建`MultiIndex`时传入的`levels`参数），以`Index`的数据类型。 ![MultiIndex_levels](../imgs/Index/MultiIndex_levels.JPG)

3. `Seris`的结构如图所示（实线为普通属性，虚线为`property`属性或者`getset_descriptor`）： ![Series](../imgs/Series/Series.JPG)

    * `._name`为普通属性，返回`Seris`的名字；`.name`为`property`属性，返回的也是`Seris`名字 ![Series_name1](../imgs/Series/Series_name1.JPG) ![Series_name2](../imgs/Series/Series_name2.JPG)
    * `.dtype/.dtypes`为`property`属性，返回`Series`的数据类型。 ![Series_dtype1](../imgs/Series/Series_dtype1.JPG) ![Series_dtype2](../imgs/Series/Series_dtype2.JPG)
    * `.ftype/ftypes`为`property`属性，返回一个字符串，说明`Series`是否稀疏数据。（二者返回的字符串的值相同，但不是同一个字符串对象） ![Series_ftype1](../imgs/Series/Series_ftype1.JPG) ![Series_ftype2](../imgs/Series/Series_ftype2.JPG)
    * `.values/._values`为`property`属性，返回`Series`的内部数据的视图 ![Series_values1](../imgs/Series/Series_values1.JPG) ![Series_values2](../imgs/Series/Series_values2.JPG)
    * `.index`为普通属性，返回`Series`的索引 ![Series_index](../imgs/Series/Series_index.JPG)
    * `.shape`为`property`属性，返回`Series`的数据的形状 ![Series_shape](../imgs/Series/Series_shape.JPG)
    * `._data`为普通属性，它返回的是一个`SingleBlockManager`对象，该对象负责管理内部数据。 ![Series_data](../imgs/Series/Series_data.JPG)
    * `SingleBlockManager`的`.shape`属性为`property`属性，返回内部数据的形状 ![SingleBlockManager_shape](../imgs/Series/SingleBlockManager_shape.JPG)
    * `SingleBlockManager`的`.blocks`属性为普通属性，返回一个列表，该列表只有一个元素，该元素为一个`IntBlock`对象（或者其他的`xxxBlock`对象），代表了内部数据。 ![SingleBlockManager_blocks](../imgs/Series/SingleBlockManager_blocks.JPG)
    * `IntBlock`的`.values`属性为普通属性，它返回内部数据：一个`ndarray`。 ![IntBlock_values](../imgs/Series/IntBlock_values.JPG)
    * `IntBlock`的`.shape`属性为`property`属性，它返回内部数据的形状 ![IntBlock_shape](../imgs/Series/IntBlock_shape.JPG)

4. `DataFrame`的结构如图所示（实线为普通属性，虚线为`property`属性或者`getset_descriptor`）：<br></br>![DataFrame](../imgs/DataFrame/DataFrame.JPG)

    * `.index/columns`属性都为普通属性，它们返回的都是一个`Index`对象，参考`Series`。 ![DataFrame_index_columns](../imgs/DataFrame/DataFrame_index_columns.JPG)

    * `.dtypes`属性为`property`属性，给出了每列的数值类型。它返回的是一个`Series`。并且没有`.dtype`属性，这一点与`Series`不同。 ![DataFrame_dtypes](../imgs/DataFrame/DataFrame_dtypes.JPG)

    * `.ftypes`属性为`property`属性，给出了每列是否为`sparse/dense`的。它返回的是一个`Series`。并且没有`.ftype`属性，这一点与`Series`不同。 ![DataFrame_ftypes](../imgs/DataFrame/DataFrame_ftypes.JPG)

    * `.values/._values/.shape`属性都为`property`属性，参考`Series`。 ![DataFrame_values_shape](../imgs/DataFrame/DataFrame_values_shape.JPG)

    * `._data`属性为普通属性，它返回的是一个`BlockManager`对象，该对象负责管理内部数据。该对象的`.block`属性（普通属性）返回一个列表，该列表里面有多个元素。 `DataFrame`尽量用一个数组保存类型相同的列。

    * 每个元素都为一个`xxBlock`对象。如`IntBlock/FloatBlock...`

        * 一个`xxBlock` 可能存储多个列的数据（这些列的数据都是同一个类型）

    * `xxBlock`对象的`.values`属性（普通属性）就是存储的某个列（或者某些类型相同的列）的内部数据，一个`ndarray`

    * `xxBlock`对象的`.shape`属性（`property`属性）就是存储的某个列（或者某些类型相同的列）的内部数据的形状 ![DataFrame_data](../imgs/DataFrame/DataFrame_data.JPG)

    * `.blocks`属性为`property`属性。该属性返回一个字典，该字典的键为不同的数值类型，该字典的值为该数值类型的数值组成的`DataFrame` ![DataFrame_blocks](../imgs/DataFrame/DataFrame_blocks.JPG)



## 三、 下标存取

### 1. [ ] 操作符

1. 对于`Index`对象，可以通过`[]`来选取数据，它类似于一维`ndarray`的索引。下标可以为下列几种下标对象：

    * 一个整数下标。此时返回对应的`label`

    * 一个整数`slice`。此时返回对应的`Index`（根据一维`labels`先切片，再组装成`Index`）

    * 一个`array-like`对象（元素可以为下标或者布尔值）。此时返回对应的`Index`。（根据一维`labels`先索引，再组装成`Index`）

    * 由`None`组成的二元组，其中`None`相当于新建一个轴。

        * 如果`None`为第一个元素，则新建的轴为 0 轴；
        * 如果`None`为第二个元素，则新建的轴为 1 轴。
        * 另外`idx[None]`等价于`idx[None,:]`，但是`idx[None]`返回的是`ndarray`。
        * 它并没有将`Index` 转换成`MultiIndex`，只是将`Index`内部的数据数组扩充了一个轴


> > 

> Index 的索引只支持整数/整数`slice`/整数序列/布尔序列/整数数组/布尔数组/None 等。



![slect_sq_brackets_index](../imgs/slect_sq_brackets_index.JPG)

2. 对于`Series`对象，可以通过`[]`来选取数据，它类似于一维`ndarray`的索引。下标可以为下列几种下标对象：

    * 一个整数下标/一个属性（属性名为某个`label`）/字典索引（键为`label`）：返回对应的数值

    * 一个整数切片/一个`label`切片：返回对应的`Series`。（根据一维`Series`先切片，再组装成`Series`）。注意：`label`切片同时包含了起始`label`和终止`label`

    * 一个整数`array-like`/一个`label array-like`/一个布尔`ndarray`：返回对应的`Series`。（根据一维`Series`先索引，再组装成`Series`）

    * 一个二维整数`array-like`/二维`label array-like`：返回对应值组成的二维`ndarray`

    >     > 

    > 注意：`Series`必须使用布尔数组来索引，不支持布尔序列来索引(抛出`KeyError`异常)。




![slect_sq_brackets_series1](../imgs/slect_sq_brackets_series1.JPG) ![slect_sq_brackets_series2](../imgs/slect_sq_brackets_series2.JPG)

3. 对于`DataFrame`对象，可以通过`[]`来选取数据。下标可以为下列几种下标对象：

    * 一个属性（属性名为某个`column label`）/字典索引（键为`column label`）：返回对应的列对应的`Series`

    >     > 

    > 不可以使用单个整数来索引



    * 一个整数切片/一个`row label`切片：返回对应的行组成的`DataFrame`。注意：`label`切片同时包含了起始`label`和终止`label`

    * 一个一维`label array-like`:返回对应的列组成的`DataFrame`

    * 一个布尔数组：返回数组中`True`对应的行组成的`DataFrame`。

    * 一个布尔`DataFrame`：将该布尔`DataFrame`中的`False`对应的元素设置为`NaN`（布尔`DataFrame`中没有出现的值为`False`）


![slect_sq_brackets_df1](../imgs/slect_sq_brackets_df1.JPG) ![slect_sq_brackets_df2](../imgs/slect_sq_brackets_df2.JPG)

4. `Series`对象除了支持使用位置作为下标存取元素之外，还可以使用索引标签来存取元素。这个功能与字典类似，因此它也支持字典的一些方法，如`Series.iteritems()`。 ![iteritems](../imgs/Series/iteritems.JPG)

5. 对于`Series/DataFrame`切片方式的索引，返回的结果与原始对象共享基础数据。对于采用其他方式的索引，返回的结果并不与元素对象共享基础数据。 ![same_base](../imgs/same_base.JPG)

6. 对于`DataFrame`的赋值与列删除：

    * 将列表或者数组赋值给某个列时，其长度必须跟`DataFrame`的行数匹配。
    * 将标量赋值给某个列时，会将标量扩充
    * 将`Series`赋值给某个列时，会精确匹配`DataFrame`的索引。如果`DataFrame`中某个`label`在`Series`中找不到，则赋值`NaN`（空位都将被填上缺失值）
    * 为不存在的列赋值会创建出一个新列（必须用字典的形式，不能用属性赋值的形式）
    * 关键字`del`用于删除列（必须用字典的形式，不能用属性赋值的形式）

![assign_1](../imgs/DataFrame/assign_1.JPG) ![assign_2](../imgs/DataFrame/assign_2.JPG)

7. 对于`Series`的赋值与删除：

    * 对于单个索引或者切片索引，要求右侧数值的长度与左侧相等
    * 为不存在的`label`赋值会创建出一个新行（必须用字典的形式，不能用属性赋值的形式）
    * 关键字`del`用于删除行（必须用字典的形式，不能用属性赋值的形式） ![assign](../imgs/Series/assign.JPG)

8. 如果`Series/DataFrame`的索引有重复`label`，则数据的选取行为将有所不同：

    * 如果索引对应多个`label`，则`Series`返回一个`Sereis`，`DataFrame`返回一个`DataFrame`
    * 如果索引对应单个`label`，则`Series`返回一个标量值，`DataFrame`返回一个`Series`

你可以通过`Index.is_unique`属性得知索引是否有重复的。

    * 对于`[]`、字典索引、属性索引或者`.loc/.ix`存取器，结论如上所述
    * 对于`.at`存取器：如果索引对应单个`label`，索引结果正常。如果索引对应多个`label`，则`Series`返回一个一维`ndarray`；`DataFrame`则抛出异常。 ![select_label_nounique](../imgs/select_label_nounique1.JPG) ![select_label_nounique](../imgs/select_label_nounique2.JPG)

9. 对于`Series/DataFrame`，它们可以使用`ndarray`的接口。因此可以通过`ndarray` 的索引规则来索引它们。

```
xxxxxxxxxxdf=pd.DataFrame(...)df[:,0] #使用了 ndarray 的索引方式
```

​


### 2. loc/iloc/ix 存取器

1. 对于`Series`， `.loc[]`的下标对象可以为：

    * 单个`label`，此时返回对应的值
    * `label`的`array-like`、`label slice`以及布尔`array-like`：返回对应值组成的`Series`

![series_loc](../imgs/select_loc_series.JPG)

2. 对于`DataFrame`，`.loc[]`的下标对象是一个元组，其中两个元素分别与`DataFrame`的两个轴对应。如果下标不是元组，则该下标对应的是第0轴，第一轴为默认值`:`。

    * 每个轴的下标都支持单个`label`、`label array-like`、`label slice`、布尔`array-like`。
    * 若获取的是某一列或者某一行，则返回的是`Series`；若返回的是多行或者多列，则返回的是`DataFrame`；如果返回的是某个值，则是普通的标量。

![select_loc_df1](../imgs/select_loc_df1.JPG) ![select_loc_df2](../imgs/select_loc_df2.JPG)

3. `.iloc[]`和`.loc[]`类似，但是`.iloc[]`使用整数下标，而不是使用`label`。

    * 注意整数切片不包括最后一个值。

![select_iloc1](../imgs/select_iloc1.JPG) ![select_iloc2](../imgs/select_iloc2.JPG)

4. `.ix[]`存取器综合了`.iloc/.loc`：它可以混合使用`label`和位置下标

    * 注意：如果有整数索引，则应该使用`.loc/.iloc`从而避免混淆

![select_ix1](../imgs/select_ix1.JPG) ![select_ix2](../imgs/select_ix2.JPG)

5. `Index`对象不能使用`loc/iloc/ix`存取器

6. 对于`.loc/.iloc/.ix`：如果某轴的索引为`array-like`或者布尔`array-like`，则返回的结果与原来的对象不再共享基础数据。如果轴的索引全部都是`slice`或者单个整数、单个`label`，则返回的结果与原来的对象共享基础数据。 ![select_data_share](../imgs/select_data_share.JPG)


### 3. at/iat 存取器

1. `.at`和`.iat`分别使用`label`和整数下标获取单个值。它类似于`.loc/.iloc`，但是`.at/.iat`的速度更快

    * 每个索引只能是单个`label`或者单个整数

![select_at_iat](../imgs/select_at_iat.JPG)

2. 对于`DataFrame`，`.lookup(row_labels, col_labels)`类似于：`.loc[row_labels, col_labels]`，但是`.lookup`返回的是一维`ndarray`。

    * 要求`row_labels`和`col_labels`长度相同。`(row_labels[0],col_labels[0]`决定了结果中第一个元素的位置，...`(row_labels[i],col_labels[i]`决定了结果中第 `i+1`个元素的位置， ![select_lookup](../imgs/select_lookup.JPG)

3. `DataFrame.get_value(index, col, takeable=False)`等价于`.loc[index, col]`，它返回单个值。而`Series.get_value(label, takeable=False)`等价于`.loc[label]`，它也返回单个值 ![select_get_value](../imgs/select_get_value.JPG)

4. `.get(key[, default])`方法与字典的`get()`方法的用法相同。对于`DataFrame`，`key`为`col_label` ![select_get](../imgs/select_get.JPG)

5. `.head([n=5])`和`.tail([n=5])`返回头部/尾部`n`行数据 ![select_head_tail](../imgs/select_head_tail.JPG)


### 4. query 方法

1. 对于`DataFrame`，当需要根据一定的条件对行进行过滤时，通常可以先创建一个布尔数组，然后使用该数组获取`True`对应的行。另一个方案就是采用`query(expr, inplace=False, **kwargs)`方法：

    * `expr`是个运算表达式字符串，如`'label1 >3 and label2<5'`
    * 表达式中的变量名表示对应的列，可以使用`not/and/or`等关键字进行向量布尔运算。该方法会筛选出那些满足条件的行。
    * 如果希望在表达式中使用`Python`变量，则在变量名之前使用`@`
    * `inplace`是个布尔值，如果为`True`，则原地修改。否则返回一份拷贝。 ![select_query](../imgs/select_query.JPG)


### 5. 多级索引

1. 对于`.loc/.ix/[]`，其下标可以指定多级索引中，每级索引上的标签。

    * 多级索引轴对应的下标是一个下标元组，该元组中每个元素与索引中每级索引对应
    * 如果下标不是元组，则将其转换成长度为 1 的元组
    * 如果元组的长度比索引的层数少，则在其后面补充`slice(None)` ![select_multiIndex1](../imgs/select_multiIndex1.JPG) ![select_multiIndex2](../imgs/select_multiIndex2.JPG) ![select_multiIndex3](../imgs/select_multiIndex3.JPG)


### 6. 整数 label

1. `label`不一定是字符串，也有可能是整数（如`RangeIndex/Int64Index`等）。尤其是当`label`是自动生成的时候。

    * 当你的`label`是整数时，面向整数的下标索引总是面向`label`的，而不是面向`position`的。因此推荐使用`.loc`来基于`label`索引，使用`.iloc`来基于`position`索引。

![Index_numlabel1](../imgs/Index_numlabel1.JPG) ![Index_numlabel2](../imgs/Index_numlabel2.JPG)


## 四、 运算

### 1. 数值运算

1. 当进行数值运算时，`pandas`会按照标签对齐元素：运算符会对标签相同的两个元素进行计算。对于`DataFrame`，对齐会同时发生在行和列上。

    * 当某一方的标签不存在时，默认以`NaN`填充。缺失值会在运算过程中传播。

> > 

> 由于`NaN`是浮点数中的一个特殊值，因此结果的元素类型被转换为`float64`



    * 结果的索引是双方索引的并集。

2. 除了支持加减乘除等运算符之外，`pandas`还提供了对应的函数： `add/sub/mul/div/mod(other, axis='columns', level=None, fill_value=None)`:

    * `other`：一个`DataFrame/Series`或者一个`array-like`，或者一个标量值
    * `axis`：指定操作的轴。可以为`0/1/'index'/'columns'` 。其意义是：操作发生在哪个轴上。
    * `fill_value`：指定替换掉`NaN`的值。可以为`None`（不替换），或者一个浮点值。注意：如果发现两个`NaN`相加，则结果仍然还是`NaN`，而并不会是两个`fill_value`相加。
    * `level`：一个整数或者`label`，用于多级索引的运算。

全部运算操作函数为：

```
xxxxxxxxxx  add,sub,mul,div,truediv,floordiv,mod,pow,radd,rsub,rmul,rdiv,rtruediv,  rfloordiv,rmod,rpow # 这些的参数为 other,axis,level,fill_value  lt,gt,le,ge,ne,eq# 这些的参数为 ohter,axis,level
```

对于`DataFrame`和`Series`的运算，默认会用`DataFrame`的每一行与`Series`运算。如果你希望使用`DataFrame`的每一列与`Series`运算，则必须使用二元操作函数，并且指定`axis=0`（表示操作匹配的轴）。

![operate1](../imgs/operate1.JPG) ![operate2](../imgs/operate2.JPG) ![operate3](../imgs/operate3.JPG)


### 2. 排序

1. `.sort_index()`方法的作用是根据`label`排序（而不是对存放的数据排序）。

```
xxxxxxxxxx  DataFrame/Series.sort_index(axis=0, level=None, ascending=True, inplace=False,   kind='quicksort', na_position='last', sort_remaining=True)
```

    * `axis`：指定沿着那个轴排序。如果为`0/'index'`，则对沿着0轴，对行`label`排序；如果为`1/'columns'`，则沿着 1轴对列`label`排序。<br></br>
    * `level`：一个整数、`label`、整数列表、`label list`或者`None`。对于多级索引，它指定在哪一级上排序。
    * `ascending`：一个布尔值，如果为`True`，则升序排序；如果是`False`，则降序排序。
    * `inplace`：一个布尔值，如果为`True`，则原地修改。如果为`False`，则返回排好序的新对象
    * `kind`:一个字符串，指定排序算法。可以为`'quicksort'/'mergesort'/'heapsort'`。注意只有归并排序是稳定排序的
    * `na_position`：一个字符串，值为`'first'/'last'`，指示：将`NaN`排在最开始还是最末尾。
    * `sort_remaining`：一个布尔值。如果为`True`，则当多级索引排序中，指定`level`的索引排序完毕后，对剩下`level`的索引也排序。 ![sort_index1](../imgs/sort_index1.JPG) ![sort_index2](../imgs/sort_index2.JPG)

2. `.sort_values()`方法的作用是根据元素值进行排序。

```
xxxxxxxxxx  DataFrame/Series.sort_values(by, axis=0, ascending=True, inplace=False,   kind='quicksort', na_position='last')  Series.sort_values(axis=0, ascending=True, inplace=False,   kind='quicksort', na_position='last')
```

    * `by`：一个字符串或者字符串的列表，指定希望对那些`label`对应的列或者行的元素进行排序。对于`DataFrame`，必须指定该参数。而`Series`不能指定该参数。

        * 如果是一个字符串列表，则排在前面的`label`的优先级较高。

        >         > 

        > 它指定了用于比较的字段




    * `axis`：指定沿着那个轴排序。如果为`0/'index'`，则沿着0轴排序（此时`by`指定列`label`，根据该列的各元素大小，重排列各行）；如果为`1/'columns'`，则沿着 1轴排序（此时`by`指定行`label`，根据该行的各元素大小，重排列各列）。<br></br>

    * `ascending`：一个布尔值，如果为`True`，则升序排序；如果是`False`，则降序排序。

    * `inplace`：一个布尔值，如果为`True`，则原地修改。如果为`False`，则返回排好序的新对象

    * `kind`:一个字符串，指定排序算法。可以为`'quicksort'/'mergesort'/'heapsort'`。注意只有归并排序是稳定排序的

    * `na_position`：一个字符串，值为`'first'/'last'`，指示：将`NaN`排在最开始还是最末尾。


![sort_values1](../imgs/sort_values1.JPG) ![sort_values2](../imgs/sort_values2.JPG)

3. `DataFrame/Series.sortlevel(level=0, axis=0, ascending=True,` `inplace=False, sort_remaining=True)`：根据单个`level`中的`label`对数据进行排列（稳定的）

    * `axis`：指定沿着那个轴排序。如果为`0/'index'`，则沿着0轴排序 ；如果为`1/'columns'`，则沿着 1轴排序
    * `level`：一个整数，指定多级索引的`level`
    * `ascending`：一个布尔值，如果为`True`，则升序排序；如果是`False`，则降序排序。
    * `inplace`：一个布尔值，如果为`True`，则原地修改。如果为`False`，则返回排好序的新对象
    * `sort_remaining`：一个布尔值。如果为`True`，则当多级索引排序中，指定`level`的索引排序完毕后，对剩下`level`的索引也排序。

![sort_level0](../imgs/sort_level0.JPG) ![sort_level1](../imgs/sort_level1.JPG)

4. `.rank()`方法的作用是在指定轴上计算各数值的排，其中相同数值的排名是相同的。

```
xxxxxxxxxx  DataFrame/Series.rank(axis=0, method='average', numeric_only=None,  na_option='keep', ascending=True, pct=False)
```

    * `axis`：指定沿着那个轴排名。如果为`0/'index'`，则沿着行排名（对列排名）；如果为`1/'columns'`，则沿着列排名（对行排名）。

    * `method`：一个字符串，指定相同的一组数值的排名。假设数值 `v`一共有`N`个。现在轮到对`v`排序，设当前可用的排名为`k`。

        * `'average'`：为各个等值平均分配排名，这`N`个数的排名都是
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display" style="text-align: center;"><span class="MathJax_SVG" id="MathJax-Element-1-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="5.963ex" role="img" style="vertical-align: -1.756ex;" viewbox="0 -1811.3 12697.5 2567.2" width="29.491ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E1-MJSZ1-2211" stroke-width="0"></path><path d="M234 637Q231 637 226 637Q201 637 196 638T191 649Q191 676 202 682Q204 683 299 683Q376 683 387 683T401 677Q612 181 616 168L670 381Q723 592 723 606Q723 633 659 637Q635 637 635 648Q635 650 637 660Q641 676 643 679T653 683Q656 683 684 682T767 680Q817 680 843 681T873 682Q888 682 888 672Q888 650 880 642Q878 637 858 637Q787 633 769 597L620 7Q618 0 599 0Q585 0 582 2Q579 5 453 305L326 604L261 344Q196 88 196 79Q201 46 268 46H278Q284 41 284 38T282 19Q278 6 272 0H259Q228 2 151 2Q123 2 100 2T63 2T46 1Q31 1 31 10Q31 14 34 26T39 40Q41 46 62 46Q130 49 150 85Q154 91 221 362L289 634Q287 635 234 637Z" id="E1-MJMATHI-4E" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E1-MJMAIN-2212" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E1-MJMAIN-31" stroke-width="0"></path><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E1-MJMATHI-69" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E1-MJMAIN-3D" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E1-MJMAIN-30" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E1-MJMAIN-28" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E1-MJMATHI-4B" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E1-MJMAIN-2B" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E1-MJMAIN-29" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E1-MJMAIN-32" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="6042" x="0" y="220"></rect><g transform="translate(60,766)"><use x="0" xlink:href="#E1-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1056,476)"><use transform="scale(0.707)" x="0" xlink:href="#E1-MJMATHI-4E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="888" xlink:href="#E1-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1666" xlink:href="#E1-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E1-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="345" xlink:href="#E1-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1123" xlink:href="#E1-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="2687" xlink:href="#E1-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3076" xlink:href="#E1-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4187" xlink:href="#E1-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5188" xlink:href="#E1-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5533" xlink:href="#E1-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="2577" xlink:href="#E1-MJMATHI-4E" xmlns:xlink="http://www.w3.org/1999/xlink" y="-686"></use></g><use x="6559" xlink:href="#E1-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7615" xlink:href="#E1-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8726" xlink:href="#E1-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(9504,0)"><g transform="translate(342,0)"><rect height="60" stroke="none" width="2730" x="0" y="220"></rect><g transform="translate(60,676)"><use x="0" xlink:href="#E1-MJMATHI-4E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1110" xlink:href="#E1-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2110" xlink:href="#E1-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="1115" xlink:href="#E1-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="-686"></use></g></g></g></svg></span></span><script id="MathJax-Element-1" type="math/tex; mode=display">\frac{\sum_{i=0}^{N-1}(K+i)}{N}=K+\frac{N-1}{2}</script>
        ​

        * `'min'`：使用可用的最小的排名，这`N`个数的排名都是 `k`

        * `'max'`：使用可用的最大的排名，这`N`各数的排名都是 `k+N-1`

        * `'first`：根据元素数据中出现的顺序依次分配排名，即按照它们出现的顺序，其排名分别为 `k,k+1,...k+N-1`

        * `'dense`：类似于 `'min'`，但是排名并不会跳跃。即比`v`大的下一个数值排名为`k+1`，而不是`k+N`


    * `numeric_only` :一个布尔值。如果为`True`，则只对`float/int/bool`数据排名。仅对`DataFrame`有效

    * `na_option`：一个字符串，指定对`NaN`的处理。可以为：

        * `'keep'`：保留`NaN`在原位置
        * `'top'`:如果升序，则`NaN`安排最大的排名
        * `'bottom'`:如果升序，则`NaN`安排最小的排名

    * `ascending`：一个布尔值，如果为`True`，则升序排名；如果是`False`，则降序排名。

    * `pct`：一个布尔值。如果为`True`，则计算数据的百分位数，而不是排名。


![rank1](../imgs/rank1.JPG) ![rank2](../imgs/rank2.JPG) ![rank3](../imgs/rank3.JPG)


### 3. 统计

1. `Series`和`DataFrame`对象都支持`Numpy`的数组接口，因此可以直接使用`Numpy`提供的`ufunc`函数对它们进行运算。这些函数通常都有三个常用参数：

    * `axis`：指定运算沿着哪个轴进行
    * `level`：如果轴是多级索引`MultiIndex`，则根据`level`分组计算
    * `skipna`：运算是否自动跳过`NaN`

下面的方法使用如下的两个`Series`和`DataFrame`: ![stats0](../imgs/stats0.JPG)

2. 数值运算类方法：（下面的`DataFrame`方法对于`Series`也适用）

    * `DataFrame.abs()`：计算绝对值（只对数值元素进行计算）

    * `DataFrame.all([axis, bool_only, skipna, level])`：返回指定轴上：是否所有元素都为`True`或者非零。`bool_only`为`True`则仅考虑布尔型的数据。

    * `DataFrame.any([axis, bool_only, skipna, level])` ：返回指定轴上：是否存在某个元素都为`True`或者非零。`bool_only`为`True`则仅考虑布尔型的数据。

    * `DataFrame.clip([lower, upper, axis])` ：将指定轴上的数据裁剪到`[lower,upper]`这个闭区间之内。超过`upper`的值裁剪成`upper`；小于`lower`的值裁剪成`lower`。

    * `DataFrame.clip_lower(threshold[, axis])`：返回一份拷贝，该拷贝是在指定轴上：向下裁剪到`threshold`

    * `DataFrame.clip_upper(threshold[, axis])`：返回一份拷贝，该拷贝是在指定轴上：向上裁剪到`threshold`

    * `DataFrame.prod([axis, skipna, level, ...])` ：计算指定轴上的乘积

    * `DataFrame.sum([axis, skipna, level, ...])`：沿着指定轴，计算样本的和

    * `DataFrame.cumsum([axis, skipna])` ：计算沿着`axis`轴的累积和。

    * `DataFrame.cumprod([axis, skipna])` ：计算沿着`axis`轴的累积乘积。

    * `DataFrame.count([axis, level, numeric_only])`：计算沿着`axis`轴，`level`级索引的非`NaN`值的数量。如果`numeric_only`为`True`，则只考虑数值和布尔类型。

    >     > 

    > 对于`Series`，只有`level`一个参数。



    * `DataFrame.round([decimals])` ：对元素指定小数点位数。`decimals`可以为一个整数（所有的元素都按照该小数点位数）、一个字典（根据列`label`指定） ![stats_compute0](../imgs/stats_compute0.JPG) ![stats_compute1](../imgs/stats_compute1.JPG) ![stats_compute2](../imgs/stats_compute2.JPG)


3. 最大最小：（下面的`DataFrame`方法对于`Series`也适用）

    * `DataFrame.max([axis, skipna, level, ...])`： 沿着指定轴，计算最大值

    * `DataFrame.min([axis, skipna, level, ...])`： 沿着指定轴，计算最小值

    * `Series.argmax([axis, skipna, ...])`： 计算最大值的索引位置（一个整数值）

    >     > 

    > pandas 0.20 以后，它返回的不再是索引位置，而是索引 label，等价于 idxmax



    * `Series.argmin([axis, skipna, ...])`： 计算最小值的索引位置（一个整数值）

    >     > 

    > pandas 0.20 以后，它返回的不再是索引位置，而是索引 label，等价于 idxmin



    * `Series.idxmax([axis, skipna, ...])`： 计算最大值的索引`label`

    * `Series.idxmin([axis, skipna, ...])`： 计算最小值的索引`label`

    * `DataFrame.cummax([axis, skipna])` ：计算沿着`axis`轴的累积最大值。

    * `DataFrame.cummin([axis, skipna])` ：计算沿着`axis`轴的累积最最小值。

    * `DataFrame.quantile([q, axis, numeric_only, ...])`：计算指定轴上样本的百分位数。`q`为一个浮点数或者一个`array-like`。每个元素都是 `0~1`之间。如 0.5代表 50%分位

    * `DataFrame.rank([axis, method, numeric_only, ...])`：计算指定轴上的排名。

    * `DataFrame.pct_change([periods, fill_method, ...])`：计算百分比变化。`periods`为相隔多少个周期。它计算的是：`(s[i+periods]-s[i])/s[i]`，注意结果并没有乘以 100。

    * `Series.nlargest( *args,**kwargs)`：计算最大的`N`个数。参数为：

        * `n`：最大的多少个数
        * `keep`：遇到重复值时怎么处理。可以为：`'first'/'last'`。

    * `Series.nsmallest( *args,**kwargs)`：计算最小的`N`个数。参数同上。


![stats_minmax0](../imgs/stats_minmax0.JPG) ![stats_minmax1](../imgs/stats_minmax1.JPG)

4. 统计类方法：（下面的`DataFrame`方法对于`Series`也适用）

    * `DataFrame.mean([axis, skipna, level, ...])`：沿着指定轴，计算平均值

    * `DataFrame.median([axis, skipna, level, ...])`：沿着指定轴，计算位于中间大小的数

    * `DataFrame.var([axis, skipna, level, ddof, ...])`：沿着指定轴，计算样本的方差

    * `DataFrame.std([axis, skipna, level, ddof, ...])`：沿着指定轴，计算样本的标准差

    * `DataFrame.mad([axis, skipna, level])`：沿着指定轴，根据平均值计算平均绝对离差

    * `DataFrame.diff([periods, axis])`：沿着指定轴的一阶差分。`periods`为间隔。

    * `DataFrame.skew([axis, skipna, level, ...])`：沿着指定轴计算样本的偏度（二阶矩）<br></br>

    * `DataFrame.kurt([axis, skipna, level, ...])`：沿着指定轴，计算样本的峰度（四阶矩）

        * 对随机变量<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-16-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.877ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -755.9 852 808.1" width="1.979ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M42 0H40Q26 0 26 11Q26 15 29 27Q33 41 36 43T55 46Q141 49 190 98Q200 108 306 224T411 342Q302 620 297 625Q288 636 234 637H206Q200 643 200 645T202 664Q206 677 212 683H226Q260 681 347 681Q380 681 408 681T453 682T473 682Q490 682 490 671Q490 670 488 658Q484 643 481 640T465 637Q434 634 411 620L488 426L541 485Q646 598 646 610Q646 628 622 635Q617 635 609 637Q594 637 594 648Q594 650 596 664Q600 677 606 683H618Q619 683 643 683T697 681T738 680Q828 680 837 683H845Q852 676 852 672Q850 647 840 637H824Q790 636 763 628T722 611T698 593L687 584Q687 585 592 480L505 384Q505 383 536 304T601 142T638 56Q648 47 699 46Q734 46 734 37Q734 35 732 23Q728 7 725 4T711 1Q708 1 678 1T589 2Q528 2 496 2T461 1Q444 1 444 10Q444 11 446 25Q448 35 450 39T455 44T464 46T480 47T506 54Q523 62 523 64Q522 64 476 181L429 299Q241 95 236 84Q232 76 232 72Q232 53 261 47Q262 47 267 47T273 46Q276 46 277 46T280 45T283 42T284 35Q284 26 282 19Q279 6 276 4T261 1Q258 1 243 1T201 2T142 2Q64 2 42 0Z" id="E16-MJMATHI-58" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E16-MJMATHI-58" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-16" type="math/tex">X</script>，<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-11-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.811ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -906.7 8230.2 1210.2" width="19.115ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M492 213Q472 213 472 226Q472 230 477 250T482 285Q482 316 461 323T364 330H312Q311 328 277 192T243 52Q243 48 254 48T334 46Q428 46 458 48T518 61Q567 77 599 117T670 248Q680 270 683 272Q690 274 698 274Q718 274 718 261Q613 7 608 2Q605 0 322 0H133Q31 0 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q146 66 215 342T285 622Q285 629 281 629Q273 632 228 634H197Q191 640 191 642T193 659Q197 676 203 680H757Q764 676 764 669Q764 664 751 557T737 447Q735 440 717 440H705Q698 445 698 453L701 476Q704 500 704 528Q704 558 697 578T678 609T643 625T596 632T532 634H485Q397 633 392 631Q388 629 386 622Q385 619 355 499T324 377Q347 376 372 376H398Q464 376 489 391T534 472Q538 488 540 490T557 493Q562 493 565 493T570 492T572 491T574 487T577 483L544 351Q511 218 508 216Q505 213 492 213Z" id="E11-MJMATHI-45" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E11-MJMAIN-28" stroke-width="0"></path><path d="M42 0H40Q26 0 26 11Q26 15 29 27Q33 41 36 43T55 46Q141 49 190 98Q200 108 306 224T411 342Q302 620 297 625Q288 636 234 637H206Q200 643 200 645T202 664Q206 677 212 683H226Q260 681 347 681Q380 681 408 681T453 682T473 682Q490 682 490 671Q490 670 488 658Q484 643 481 640T465 637Q434 634 411 620L488 426L541 485Q646 598 646 610Q646 628 622 635Q617 635 609 637Q594 637 594 648Q594 650 596 664Q600 677 606 683H618Q619 683 643 683T697 681T738 680Q828 680 837 683H845Q852 676 852 672Q850 647 840 637H824Q790 636 763 628T722 611T698 593L687 584Q687 585 592 480L505 384Q505 383 536 304T601 142T638 56Q648 47 699 46Q734 46 734 37Q734 35 732 23Q728 7 725 4T711 1Q708 1 678 1T589 2Q528 2 496 2T461 1Q444 1 444 10Q444 11 446 25Q448 35 450 39T455 44T464 46T480 47T506 54Q523 62 523 64Q522 64 476 181L429 299Q241 95 236 84Q232 76 232 72Q232 53 261 47Q262 47 267 47T273 46Q276 46 277 46T280 45T283 42T284 35Q284 26 282 19Q279 6 276 4T261 1Q258 1 243 1T201 2T142 2Q64 2 42 0Z" id="E11-MJMATHI-58" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E11-MJMATHI-6B" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E11-MJMAIN-29" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E11-MJMAIN-2C" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E11-MJMAIN-3D" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E11-MJMAIN-31" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E11-MJMAIN-32" stroke-width="0"></path><path d="M78 250Q78 274 95 292T138 310Q162 310 180 294T199 251Q199 226 182 208T139 190T96 207T78 250ZM525 250Q525 274 542 292T585 310Q609 310 627 294T646 251Q646 226 629 208T586 190T543 207T525 250ZM972 250Q972 274 989 292T1032 310Q1056 310 1074 294T1093 251Q1093 226 1076 208T1033 190T990 207T972 250Z" id="E11-MJMAIN-22EF" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E11-MJMATHI-45" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="764" xlink:href="#E11-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1153,0)"><use x="0" xlink:href="#E11-MJMATHI-58" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1215" xlink:href="#E11-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><use x="2480" xlink:href="#E11-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2869" xlink:href="#E11-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3314" xlink:href="#E11-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4113" xlink:href="#E11-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5168" xlink:href="#E11-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5668" xlink:href="#E11-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6113" xlink:href="#E11-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6613" xlink:href="#E11-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7058" xlink:href="#E11-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-11" type="math/tex">E(X^{k}),k=1,2,\cdots</script>若存在，则称它为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-16-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.877ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -755.9 852 808.1" width="1.979ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M42 0H40Q26 0 26 11Q26 15 29 27Q33 41 36 43T55 46Q141 49 190 98Q200 108 306 224T411 342Q302 620 297 625Q288 636 234 637H206Q200 643 200 645T202 664Q206 677 212 683H226Q260 681 347 681Q380 681 408 681T453 682T473 682Q490 682 490 671Q490 670 488 658Q484 643 481 640T465 637Q434 634 411 620L488 426L541 485Q646 598 646 610Q646 628 622 635Q617 635 609 637Q594 637 594 648Q594 650 596 664Q600 677 606 683H618Q619 683 643 683T697 681T738 680Q828 680 837 683H845Q852 676 852 672Q850 647 840 637H824Q790 636 763 628T722 611T698 593L687 584Q687 585 592 480L505 384Q505 383 536 304T601 142T638 56Q648 47 699 46Q734 46 734 37Q734 35 732 23Q728 7 725 4T711 1Q708 1 678 1T589 2Q528 2 496 2T461 1Q444 1 444 10Q444 11 446 25Q448 35 450 39T455 44T464 46T480 47T506 54Q523 62 523 64Q522 64 476 181L429 299Q241 95 236 84Q232 76 232 72Q232 53 261 47Q262 47 267 47T273 46Q276 46 277 46T280 45T283 42T284 35Q284 26 282 19Q279 6 276 4T261 1Q258 1 243 1T201 2T142 2Q64 2 42 0Z" id="E16-MJMATHI-58" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E16-MJMATHI-58" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-16" type="math/tex">X</script>的<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-17-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 521 858.4" width="1.21ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E17-MJMATHI-6B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E17-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-17" type="math/tex">k</script>阶原点矩，简称<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-17-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 521 858.4" width="1.21ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E17-MJMATHI-6B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E17-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-17" type="math/tex">k</script>阶矩。若<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-15-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.811ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -906.7 12395.4 1210.2" width="28.789ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M492 213Q472 213 472 226Q472 230 477 250T482 285Q482 316 461 323T364 330H312Q311 328 277 192T243 52Q243 48 254 48T334 46Q428 46 458 48T518 61Q567 77 599 117T670 248Q680 270 683 272Q690 274 698 274Q718 274 718 261Q613 7 608 2Q605 0 322 0H133Q31 0 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q146 66 215 342T285 622Q285 629 281 629Q273 632 228 634H197Q191 640 191 642T193 659Q197 676 203 680H757Q764 676 764 669Q764 664 751 557T737 447Q735 440 717 440H705Q698 445 698 453L701 476Q704 500 704 528Q704 558 697 578T678 609T643 625T596 632T532 634H485Q397 633 392 631Q388 629 386 622Q385 619 355 499T324 377Q347 376 372 376H398Q464 376 489 391T534 472Q538 488 540 490T557 493Q562 493 565 493T570 492T572 491T574 487T577 483L544 351Q511 218 508 216Q505 213 492 213Z" id="E15-MJMATHI-45" stroke-width="0"></path><path d="M118 -250V750H255V710H158V-210H255V-250H118Z" id="E15-MJMAIN-5B" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E15-MJMAIN-28" stroke-width="0"></path><path d="M42 0H40Q26 0 26 11Q26 15 29 27Q33 41 36 43T55 46Q141 49 190 98Q200 108 306 224T411 342Q302 620 297 625Q288 636 234 637H206Q200 643 200 645T202 664Q206 677 212 683H226Q260 681 347 681Q380 681 408 681T453 682T473 682Q490 682 490 671Q490 670 488 658Q484 643 481 640T465 637Q434 634 411 620L488 426L541 485Q646 598 646 610Q646 628 622 635Q617 635 609 637Q594 637 594 648Q594 650 596 664Q600 677 606 683H618Q619 683 643 683T697 681T738 680Q828 680 837 683H845Q852 676 852 672Q850 647 840 637H824Q790 636 763 628T722 611T698 593L687 584Q687 585 592 480L505 384Q505 383 536 304T601 142T638 56Q648 47 699 46Q734 46 734 37Q734 35 732 23Q728 7 725 4T711 1Q708 1 678 1T589 2Q528 2 496 2T461 1Q444 1 444 10Q444 11 446 25Q448 35 450 39T455 44T464 46T480 47T506 54Q523 62 523 64Q522 64 476 181L429 299Q241 95 236 84Q232 76 232 72Q232 53 261 47Q262 47 267 47T273 46Q276 46 277 46T280 45T283 42T284 35Q284 26 282 19Q279 6 276 4T261 1Q258 1 243 1T201 2T142 2Q64 2 42 0Z" id="E15-MJMATHI-58" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E15-MJMAIN-2212" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E15-MJMAIN-29" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E15-MJMATHI-6B" stroke-width="0"></path><path d="M22 710V750H159V-250H22V-210H119V710H22Z" id="E15-MJMAIN-5D" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E15-MJMAIN-2C" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E15-MJMAIN-3D" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E15-MJMAIN-31" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E15-MJMAIN-32" stroke-width="0"></path><path d="M78 250Q78 274 95 292T138 310Q162 310 180 294T199 251Q199 226 182 208T139 190T96 207T78 250ZM525 250Q525 274 542 292T585 310Q609 310 627 294T646 251Q646 226 629 208T586 190T543 207T525 250ZM972 250Q972 274 989 292T1032 310Q1056 310 1074 294T1093 251Q1093 226 1076 208T1033 190T990 207T972 250Z" id="E15-MJMAIN-22EF" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E15-MJMATHI-45" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="764" xlink:href="#E15-MJMAIN-5B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1042" xlink:href="#E15-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1431" xlink:href="#E15-MJMATHI-58" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2505" xlink:href="#E15-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3505" xlink:href="#E15-MJMATHI-45" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4269" xlink:href="#E15-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4658" xlink:href="#E15-MJMATHI-58" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5510" xlink:href="#E15-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5899,0)"><use x="0" xlink:href="#E15-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E15-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><use x="6756" xlink:href="#E15-MJMAIN-5D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7034" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7479" xlink:href="#E15-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8278" xlink:href="#E15-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9334" xlink:href="#E15-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9834" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10278" xlink:href="#E15-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10778" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11223" xlink:href="#E15-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-15" type="math/tex">E[(X-E(X))^{k}],k=1,2,\cdots</script>存在，则称它为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-16-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.877ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -755.9 852 808.1" width="1.979ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M42 0H40Q26 0 26 11Q26 15 29 27Q33 41 36 43T55 46Q141 49 190 98Q200 108 306 224T411 342Q302 620 297 625Q288 636 234 637H206Q200 643 200 645T202 664Q206 677 212 683H226Q260 681 347 681Q380 681 408 681T453 682T473 682Q490 682 490 671Q490 670 488 658Q484 643 481 640T465 637Q434 634 411 620L488 426L541 485Q646 598 646 610Q646 628 622 635Q617 635 609 637Q594 637 594 648Q594 650 596 664Q600 677 606 683H618Q619 683 643 683T697 681T738 680Q828 680 837 683H845Q852 676 852 672Q850 647 840 637H824Q790 636 763 628T722 611T698 593L687 584Q687 585 592 480L505 384Q505 383 536 304T601 142T638 56Q648 47 699 46Q734 46 734 37Q734 35 732 23Q728 7 725 4T711 1Q708 1 678 1T589 2Q528 2 496 2T461 1Q444 1 444 10Q444 11 446 25Q448 35 450 39T455 44T464 46T480 47T506 54Q523 62 523 64Q522 64 476 181L429 299Q241 95 236 84Q232 76 232 72Q232 53 261 47Q262 47 267 47T273 46Q276 46 277 46T280 45T283 42T284 35Q284 26 282 19Q279 6 276 4T261 1Q258 1 243 1T201 2T142 2Q64 2 42 0Z" id="E16-MJMATHI-58" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E16-MJMATHI-58" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-16" type="math/tex">X</script>的<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-17-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 521 858.4" width="1.21ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E17-MJMATHI-6B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E17-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-17" type="math/tex">k</script>阶中心矩。

    * `DataFrame.describe([percentiles, include, ...])`：获取顺序统计量以及其他的统计结果。

        * `percentiles`：一个`array-like`。每个元素都是 `0~1`之间。如 0.5代表 50%分位
        * `include,exclude`：指定包含/不包含哪些列（通过`dtype`来指定）。可以为`None/'all'`，或者一个`dtype`列表<br></br>

    * `DataFrame.corr([method, min_periods])`：计算任意两个列之间的非`NAN`的、按照索引对齐的值的相关系数。`method`为相关系数的类型，可以为：

        * `'pearson'`：标准的相关系数
        * `'kendall'`：`Kendall Tau`相关系数
        * `'spearman'`：`Spearman rank`相关系数

    而`min_periods`：一个整数。它指定为了生成一个有效的相关系数，每一对列数据的最短长度。

    * `DataFrame.corrwith(other[, axis, drop])` ：计算两个`DataFrame`的行-行、列-列的相关系数。

        * `axis`：如果为`0/'index'`则沿着0轴，则计算列-列之间的相关系数。如果为`1/'columns'`，则沿着1轴，计算行-行之间的相关系数
        * `drop`：一个布尔值。如果为`True`，则如果某行/列都是`NaN`，则抛弃该行/列。如果为`False`，则返回全部。<br></br>

    * `DataFrame.cov([min_periods])`：计算任意两列之间的协方差。`min_periods`指定为了生成一个有效的协方差，每一对列数据的最短长度。

        * 对于`Series`，其调用为：`Series.cov(other,[min_periods])`


![stats_stats0](../imgs/stats_stats0.JPG) ![stats_stats1](../imgs/stats_stats1.JPG) ![stats_stats2](../imgs/stats_stats2.JPG)

5. 对于`Series`：唯一值、值计数、成员资格：

    * `Series.unique()`：返回`Series`中唯一值组成的一维`ndarray`

    * `Series.value_counts(normalize=False, sort=True, ascending=False,` `bins=None, dropna=True)`：对`Series`中的数进行计数。如果`normalize`为`True`，则返回频率而不是频数。`sort`为`True`则结果根据出现的值排序，排序方式由`ascending`指定。

        * `bins`是一个整数或者`None`。如果它为整数，则使用半开半闭区间来统计，它给出了该区间的数量。

    * `Series.isin(values)`：返回一个布尔数组，给出`Series`中各值是否位于`values`中。

    >     > 

    > `DataFrame`也有此方法。




![stats_unique](../imgs/stats_unique.JPG)

6. 对于多级索引，可以通过`level`参数来指定在某个轴上的操作索引级别。如果`level=None`，则不考虑索引的多级。 ![stats_stats_multiIndex](../imgs/stats_stats_multiIndex.JPG)


## 五、变换

### 1. 索引和轴的变换

1. 重新索引：`Series/DataFrame.reindex(index=None, **kwargs)`：

    * `index`：一个`array-like`对象，给出了新的`index`的`label`

    * `method`：当新的`label`的值缺失时，如何处理。参数值可以为：

        * `None`：不做任何处理，缺失地方填充`NaN`
        * `'backfill'/'bfill'`：用下一个可用的值填充该空缺（后向填充）
        * `'pad'/'ffill'`：用上一个可用的值填充该空缺（前向填充）
        * `'nearest'`：用最近的可用值填充该空缺

    * `copy`：一个布尔值，如果为`True`，则返回一个新的`Series`对象（即使传入的`index`与原来的`index`相同）

    * `level`：一个整数或者`name`，在`MultiIndex`的指定级别上匹配简单索引

    * `fill_value`：一个标量。指定缺失值的填充数据，默认为`NaN`（如果该参数与`method`同时出现，则以`method`为主）

    * `limit`：一个整数，指定前向/后向填充时：如果有连续的`k`个`NaN`，则只填充其中`limit`个。它与`method`配合

    * `tolerance`：一个整数，用于给出在不匹配时，连续采用前向/后向/最近邻匹配的跨度的最大值。它与`method`配合


对于`DataFrame`，多了关键字参数：

    * `columns`：一个`array-like`对象，给出了新的`columns`的`label`

对于`DataFrame`，如果`.reindex()`只传入一个序列，则默认会重索引行`label`。如果同时重索引行`label`和列`label`，则`method`插值只能按照行来进行（即 0 轴）

![reindex](../imgs/reindex0.JPG) ![reindex](../imgs/reindex1.JPG) ![reindex](../imgs/reindex2.JPG)

2. 将列数据变成行索引（只对`DataFrame`有效，因为`Series`没有列索引），其中：`col label`变成`index name`，列数据变成行`label`：

```
xxxxxxxxxx  DataFrame.set_index(keys, drop=True, append=False, inplace=False,   verify_integrity=False)
```

    * `keys`： 指定了一个或者一列的`column label`。这些列将会转换为行`index`
    * `drop`：一个布尔值。如果为`True`，则`keys`对应的列会被删除；否则这些列仍然被保留
    * `append`：一个布尔值。如果为`True`，则原有的行索引将保留（此时一定是个多级索引）；否则抛弃原来的行索引。
    * `inplace`：一个布尔值。如果为`True`，则原地修改并且返回`None`
    * `verify_integrity`：一个布尔值。如果为`True`，则检查新的`index`是否有重复值。否则会推迟到检测过程到必须检测的时候。

![set_index0](../imgs/set_index0.JPG) ![set_index1](../imgs/set_index1.JPG)

3. `reset_index`会将层次化的行`index`转移到列中，成为新的一列。同时`index` 变成一个整数型的，从0开始编号：

```
xxxxxxxxxx  DataFrame.reset_index(level=None, drop=False, inplace=False,   col_level=0, col_fill='')  Series.reset_index(level=None, drop=False, name=None, inplace=False)
```

    * `level`：一个整数、`str`、元组或者列表。它指定了将从层次化的`index`中移除的`level`。如果为`None`，则移除所有的`level`
    * `drop`：一个布尔值。如果为`True`，则并不会插入新的列。如果为`False`，则插入新的列（由`index`，组成，其列名为`'index'`）。
    * `inplace`：一个布尔值。如果为`True`，则原地修改并且返回`None`
    * `col_level`：如果列索引也是多层次的，则决定插入到列索引的哪个`level`。
    * `col_fill`：如果列索引也是多层次的，则决定插入之后其他`level`的索引如何命名的。默认情况下就是重复该`index name`

对于`Series`，`name`就是插入后，对应的列`label`

4. 丢弃某条轴上的一个或者多个`label`：`Series/DataFrame.drop(labels[, axis, level, inplace, errors])`:

    * `labels`：单个`label`或者一个`label`序列，代表要被丢弃的`label`
    * `axis`：一个整数，或者轴的名字。默认为 0 轴
    * `level`：一个整数或者`level`名字，用于`MultiIndex`。因为可能在多个`level`上都有同名的`label`。
    * `inplace`：一个布尔值。如果为`True`，则原地修改并且返回`None`
    * `errors`：可以为`'ignore'/'raise'`

![drop](../imgs/drop.JPG)

5. `DataFrame`的`.T`方法会对`DataFrame`进行转置，使得行与列互换（行索引与列索引也互换） ![DataFrame_T](../imgs/DataFrame/T.JPG)

6. 交换两个轴： `DataFrame/Series.swapaxes(axis1, axis2, copy=True)` ![swapaxes](../imgs/swapaxes.JPG)

7. 交换多级索引的两个`level`：`DataFrame/Series.swaplevel(i=-2, j=-1, axis=0, copy=True)`<br></br>

    * `i/j`为两个`level`的整数`position`，也可以是`name`字符串。 ![swaplevel](../imgs/swaplevel.JPG)

8. 想修改轴`label`有两种方案：

    * 可以采用`Index.map(mapper)`方法。其中`mapper`是个可调用对象，它对每个`label`进行调用然后返回新的`label`。该函数返回一个新的`Index`对象。然后将其赋值给`pandas`对象的`.index/.columns`属性。

    * 调用`.rename`方法：

    ```
xxxxxxxxxx  Series.rename(index=None, **kwargs)  DataFrame.rename(index=None, columns=None, **kwargs)
    ```

        * `index/columns`：一个标量、`dict-like`、或者一个函数。

            * 标量：修改了`Series.name`属性。但是对于`DataFrame`会抛出异常
            * `dict-like`或者函数：应用于对应轴的`label`上

        * `copy`：如果为`True`，则拷贝底层数据（此时`inplace=False`）

        * `inplace`：一个布尔值。如果为`True`，则原地修改，此时忽略`copy`参数。否则新创建对象。



![rename0](../imgs/rename0.JPG) ![rename1](../imgs/rename1.JPG)


### 2. 合并数据

1. 对于`DataFrame`，`merge()`方法可以根据一个或者多个键将不同`DataFrame`的行连接接起来。它实现的就是数据库的连接操作。

```
xxxxxxxxxx  DataFrame.merge(right, how='inner', on=None, left_on=None, right_on=None,   left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'),  copy=True, indicator=False)
```

    * `right`：另一个`DataFrame`对象

    * `how`：指定连接类型。可以为：

        * `'left'`：左连接。只使用左边`DataFrame`的连接键
        * `'right'`：右连接。只使用右边`DataFrame`的连接键
        * `'outer'`：外连接。使用两个`DataFrame`的连接键的并集
        * `'inner'`：内连接。使用两个`DataFrame`的连接键的交集

    * `on`：一个`label`或者`label list`。它指定用作连接键的列的`label`。并且必须在两个`DataFrame`中这些`label`都存在。如果它为`None`，则默认使用两个`DataFrame`的列`label`的交集。你可以通过`left_on/right_on`分别指定两侧`DataFrame`对齐的连接键。

    * `left_on`：一个`label`或者`label list`。指定左边`DataFrame`用作连接键的列，参考`on`

    * `right_on`：一个`label`或者`label list`。指定右边`DataFrame`用作连接键的列，参考`on`

    * `left_index`：一个布尔值。如果为`True`，则使用左边的`DataFrame`的行的`index value`来作为连接键来合并

    * `right_index`：一个布尔值。如果为`True`，则使用右边的`DataFrame`的行的`index value`来作为连接键来合并

    * `sort`：一个布尔值。如果为`True`，则在结果中，对合并采用的连接键进行排序

    * `suffixes`：一个二元序列。对于结果中同名的列，它会添加前缀来指示它们来自哪个`DataFrame`

    * `copy`：一个布尔值。如果为`True`，则拷贝基础数据。否则不拷贝数据

    * `indicator`：一个字符串或者布尔值。

        * 如果为`True`，则结果中多了一列称作`_merge`，该列给出了每一行来自于那个`DataFrame`
        * 如果为字符串，则结果中多了一列（该列名字由`indicator`字符串给出），该列给出了每一行来自于那个`DataFrame`


说明：

    * 如果合并的序列来自于行的`index value`，则使用`left_index`或者`right_index`参数。如果是使用了`left_index=True`，则必须使用`right_index=True`，或者指定`right_on`。此时`right_on`为第二个`DataFrame`的行`label`。此时所有对键的操作都针对`index label`，而不再是`column label`。
    * 如果不显示指定连接的键，则默认使用两个`DataFrame`的`column label`的交集中的第一个`label`。
    * 如果根据列来连接，则结果的`index label`是`RangeIndex`（连续整数）。如果根据行`label value`连接，则结果的`index label/column label`来自两个`DataFrame`
    * 对于层次化索引的数据，你必须以列表的形式指明用作合并键的多个列。

![merge0](../imgs/merge0.JPG) ![merge1](../imgs/merge1.JPG) ![merge2](../imgs/merge2.JPG)

2. 函数`pandas.merge(left, right, how='inner', on=None, left_on=None, right_on=None,` `left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True,` `indicator=False)`作用与`left.merge(right)`相同。

3. 如果所有的连接键来自于某列值，则可以使用`DataFrame.join()`函数。它是`.merge()`的简化版。

```
xxxxxxxxxx  DataFrame.join(other, on=None, how='left', lsuffix='', rsuffix='', sort=False)
```

    * `other`：一个`DataFrame`，或者一个`Series`（要求它的`name`非空），或者一个`DataFrame`序列。`Series`的`name`作用等同`DataFrame`的`column label`
    * `on`：指定以调用者的那个`column`对应的列为键。
    * `how`：参考`merge`的`how`
    * `lsuffic/rsuffix`：参考`merge`的`suffixes`。如果结果中有重名的列，则必须指定它们之一。
    * `sort`：一个布尔值。如果为`True`，则在结果中，对合并采用的连接键进行排序

如果是`Series`，则连接键为`Series`的`index value`。此外，`DataFrame`默认使用 `index value`（这与`merge()`不同）。

![join0](../imgs/join0.JPG) ![join1](../imgs/join1.JPG)

4. `pandas.concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False,` `keys=None, levels=None, names=None, verify_integrity=False, copy=True)`函数：它将多个`DataFrame/Series`对象拼接起来。

    * `objs`：一个序列，序列元素为`Series/DataFrame/Panel`等。你也可以传入一个字典，此时字典的键将作为`keys`参数。

    * `axis`：指定拼接沿着哪个轴。可以为`0/'index'/`，表示沿着 0 轴拼接。可以为`1/'columns'`，表示沿着 1轴拼接。

    * `join`：可以为`'inner'/'outer'`，指定如何处理其他轴上的索引。

    >     > 

    > 即：其他轴上的 col 如何拼接



    * `join_axes`：一个`Index`对象的列表。你可以指定拼接结果中，其他轴上的索引而不是交集或者并集（`join`参数使用时，其他轴的索引是计算得出的）。

    * `verify_integrity`：一个布尔值。如果为`True`，则检查新连接的轴上是否有重复索引，如果有则抛出异常。

    * `keys`：一个序列。它用于区分拼接结果中，这些行/列来分别来自哪里。在必要的时候将建立多级索引，`keys`作为最外层的索引。如果`objs`是个字典，则使用字典的键作为`keys`。

    >     > 

    > 它用于建立拼接结果的 index



    * `levels`：一个序列。与`keys`配合使用，指定多级索引各级别上的索引。如果为空，则从`keys`参数中推断。（推荐为空）

    * `names`：一个序列。与`keys`配合使用，用于建立多级索引的`names`。

    * `ignore_index`：一个布尔值。如果为`True`，则不使用拼接轴上的`index value`，代替以`RangeIndex`，取值为`0,1,...`

    * `copy`：一个布尔值。如果为`True`，则拷贝数据。


![concat0](../imgs/concat0.JPG) ![concat1](../imgs/concat1.JPG) ![concat2](../imgs/concat2.JPG)

5. `Series/DataFrame.combine_first()`也是一种合并方式。它用参数对象中的数据给调用者打补丁。

```
xxxxxxxxxx  Series.combine_first(other)  DataFrame.combine_first(other)
```

    * `other`：`Series`中必须为另一个`Series`，`DataFrame`中必须为另一个`DataFrame`

结果的`index/columns`是两个的并集。结果中每个元素值这样产生：

    * 如果调用者不是`NaN`，则选择调用者的值
    * 如果调用者是`NaN`，则选择参数的值（此时无论参数的值是否`NaN`）

![combine_first0](../imgs/combine_first0.JPG) ![combine_first1](../imgs/combine_first1.JPG)

6. `Series/DataFrame.combine()`也是一种合并。

```
xxxxxxxxxx  Series.combine(other, func, fill_value=nan)  DataFrame.combine(other, func, fill_value=None, overwrite=True)
```

    * `other`：`Series`中必须为另一个`Series`，`DataFrame`中必须为另一个`DataFrame`

    * `func`：一个函数，该函数拥有两个位置参数。第一个参数来自于调用者，第二个参数来自于`other`。

        * 对于`Series`，两个参数都是标量值，对应它们对齐后的元素值。返回值就是结果对应位置处的值。
        * 对于`DataFrame`，这两个参数都是`Series`，即对应的列。

    * `fill_value`：一个标量 。在合并之前先用它来填充 `NaN`。

    * `overwrite`：如果为`True`，则原地修改调用者。如果为`False`，则返回一个新建的对象。


对于`Series`，结果的`index`是两个的并集。结果中每个元素值这样产生：

    * 将两个`Series`在同一个`index`的两个标量值分别传给`func`
    * `func`的返回值就是结果`Series`在该`index`处的值

对于`DataFrame`，结果的`index/columns`是两个的并集。结果中每列这样产生：

    * 将两个`DataFrame`在同一个`column label`的两列值分别传给`func`
    * `func`的返回值就是结果`DataFrame`在该`column label`列的值

![combine0](../imgs/combine0.JPG) ![combine1](../imgs/combine1.JPG)


### 3. 索引旋转

1. `DataFrame.stack()`方法将数据的列索引旋转为行索引。注意：它跟转置不同，转置会同时旋转数据。

```
xxxxxxxxxx  DataFrame.stack(level=-1, dropna=True)
```

    * `level`：一个整数、字符串或者整数字符串的列表。如果列索引为多级索引，它指定了将哪个级别的索引旋转为行索引
    * `dropna`：一个布尔值。如果为`True`，则如果结果中某行全为`NaN`，则抛弃该行。

与`DataFrame.stack()`对应的就是`DataFrame.unstack()`方法。它将数据的行索引转换为列索引。注意：它跟转置不同，转置会同时旋转数据。<br></br>

```
xxxxxxxxxxDataFrame.unstack(level=-1, fill_value=None)
```

    * `level`：一个整数、字符串或者整数字符串的列表。如果行索引为多级索引，它指定了将哪个级别的索引旋转为列索引
    * `fill_value`：一个标量。如果结果中有`NaN`，则使用`fill_value`替换。

旋转时，比如列索引旋转为行索引，则新的行索引是个多级索引，最内层的一级就是原来的列索引。

![stack_unstack0](../imgs/stack_unstack0.JPG) ![stack_unstack1](../imgs/stack_unstack1.JPG)

2. `DataFrame.pivot()`方法重排数据。它是一个快捷方式，它使用`set_index`将列数据变成行索引，然后使用`unstack`将行索引转为列索引。

```
xxxxxxxxxx  DataFrame.pivot(index=None, columns=None, values=None)
```

    * `index`：一个字符串。指定了一个`column name`，用该列数据来`set_index`（将该列数据变成行索引，删除了原来的旧的行索引）。如果为`None`，则不执行`set_index`

    * `columns`：一个字符串，指定了哪个列数据作为结果的`columns labels`。

    >     > 

    > 实际上对 index,clumns 指定的列数据均 set_index，然后仅对 columns 对应的列数据 unstack



    * `values`：一个字符串，指定了哪个列数据作为结果的数据。如果未提供，则剩余的所有列都将作为结果的数据。


![pivot](../imgs/pivot.JPG)


## 六、数据清洗

### 1. 移除重复数据

1. `Series/DataFrame.duplicated(*args, **kwargs)`：返回一个布尔`Series`，指示调用者中，哪些行是重复的（重复行标记为`True`）。

    * `keep`：一个字符串或者`False`，指示如何标记。它代替了废弃的参数`take_last`

        * `'first'`：对于重复数据，第一次出现时标记为`False`，后面出现时标记为`True`
        * `'last'`：对于重复数据，最后一次出现时标记为`False`，前面出现时标记为`True`
        * `False`：对于重复数据，所有出现的地方都标记为`True`


而`Series/DataFrame.drop_duplicates(*args, **kwargs)`：返回重复行被移除之后的`Series/DataFrame`。

    * `keep`：一个字符串或者`False`，指示如何删除。 它代替了废弃的参数`take_last`

        * `'first'`：对于重复数据，保留第一次出现，后面出现时删除
        * `'last'`：对于重复数据，最后一次出现时保留，前面出现时删除
        * `False`：对于重复数据，删除所有出现的位置

    * `inplace`：一个布尔值。如果为`True`，则原地修改。否则返回新建的对象。


对于`DataFrame`，还有个 `subset`参数。它是`column label`或者其列表，给出了考虑哪些列的重复值。默认考虑所有列。（即一行中哪些字段需要被考虑）<br></br>

![duplicates0](../imgs/duplicates0.JPG) ![duplicates1](../imgs/duplicates1.JPG) ![duplicates2](../imgs/duplicates2.JPG)


### 2. apply

1. 你可以使用`numpy`的`ufunc`函数操作`pandas`对象。

2. 有时，你希望将函数应用到由各列或者各行形成的一维数组上，此时`DataFrame`的`.apply()`方法即可实现此功能。 `.apply(func, axis=0, broadcast=False, raw=False, reduce=None, args=(), **kwds)`

    * `func`：一个可调用对象，它会应用于每一行或者每一列
    * `axis`：指定应用于行还是列。如果为`0/'index'`，则沿着0轴计算（应用于每一列）；如果为`1/'columns'`，则沿着1轴计算（应用于每一行）。
    * `broadcast`：一个布尔值，如果为`True`，则结果为`DataFrame`（不足的部分通过广播来填充）
    * `raw`：一个布尔值。如果为`False`，则转换每一行/每一列为一个`Series`，然后传给 `func` 作为参数。如果`True`，则`func`接受到的是`ndarray`，而不是`Series`
    * `reduce`：一个布尔值。用于判断当`DataFrame`为空时，应该返回一个`Series`还是返回一个`DataFrame`。如果为`True`，则结果为`Series`；如果为`False`，则结果为`DataFrame`。
    * `args`：传递给`func`的额外的位置参数（第一个位置参数始终为`Series/ndarray`） ![apply_df](../imgs/apply_df.JPG)

3. 有时，你希望将函数应用到`DataFrame`中的每个元素，则可以使用`.applymap(func)`方法。之所以不叫`map`，是因为`Series`已经有个`.map`方法。 ![applymap_df](../imgs/applymap_df.JPG)

4. `Series`的`.apply()`方法应用到`Series`的每个元素上： `.apply(func, convert_dtype=True, args=(), **kwds)`

    * `func`：一个可调用对象，它会应用于每个元素
    * `convert_dtype`：一个布尔值。如果为`True`，则`pandas`会自动匹配`func`结果的最佳`dtype`；如果为`False`，则`dtype=object`
    * `args`：传递给`func`的额外的位置参数。
    * `kwds`：传递给`func`的额外的关键字参数。

返回结果可能是`Series`，也可能是`DataFrame`（比如，`func`返回一个`Series`) ![apply_series](../imgs/apply_series.JPG)

5. `Series`的`.map(arg,na_action=None)`方法会应用到`Series`的每个元素上：

    * `arg`：一个函数、字典或者`Series`。如果为字典或者`Series`，则它是一种映射关系，键/`index label`就是自变量，值就是返回值。
    * `na_action`：如果为`ignore`，则忽略`NaN`

返回相同`index`的一个`Series` ![map_series](../imgs/map_series.JPG)


### 3. 缺失数据

1. `pands`对象上的所有描述统计都排除了缺失数据。 ![NaN0](../imgs/NaN0.JPG)

2. `DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)`：根据各`label`的值中是否存在缺失数据来对轴`label`进行过滤。

    * `axis`：指定沿着哪个轴进行过滤。如果为`0/'index'`，则沿着0轴；如果为`1/'columns'`，则沿着1轴。你也可以同时提供两个轴（以列表或者元组的形式）
    * `how`：指定过滤方式。如果为`'any'`，则如果该`label`对应的数据中只要有任何`NaN`，则抛弃该`label`；如果为`'all'`，则如果该`label`对应的数据中必须全部为`NaN`才抛弃该`label`。
    * `thresh`：一个整数，要求该`label`必须有`thresh`个非`NaN`才保留下来。它比`how`的优先级较高。
    * `subset`：一个`label`的`array-like`。比如`axis=0`，则`subset`为轴 1 上的标签，它指定你考虑哪些列的子集上的`NaN`
    * `inplace`：一个布尔值。如果为`True`，则原地修改。否则返回一个新创建的`DataFrame`

对于`Series`，其签名为： `Series.dropna(axis=0, inplace=False, **kwargs)`

![NaN_dropna0](../imgs/NaN_dropna0.JPG) ![NaN_dropna1](../imgs/NaN_dropna1.JPG) ![NaN_dropna2](../imgs/NaN_dropna2.JPG)

3. `DataFrame/Series.fillna(value=None, method=None, axis=None, inplace=False, limit=None,` `downcast=None, **kwargs)`：用指定值或者插值方法来填充缺失数据。

    * `value`：一个标量、字典、`Series`或者`DataFrame`。注意：`value`与`method`只能指定其中之一，不能同时提供。

        * 如果为标量，则它指定了填充`NaN`的数据。
        * 如果为`Series/dict`，则它指定了填充每个`index`的数据
        * 如果为`DataFrame`，则它指定了填充每个`DataFrame`单元的数据

    * `method`：指定填充方式。可以为`None`，也可以为：

        * `'backfill'/'bfill'`：使用下一个可用的有效值来填充（后向填充）
        * `'ffill'/'pad'`：使用前一个可用的有效值来填充（前向填充）

    * `axis`：指定沿着哪个轴进行填充。如果为`0/'index'`，则沿着0轴；如果为`1/'columns'`，则沿着1轴

    * `inplace`：一个布尔值。如果为`True`，则原地修改。否则返回一个新创建的`DataFrame`

    * `limit`：一个整数。如果`method`提供了，则当有连续的`N`个`NaN`时，只有其中的`limit`个`NaN`会被填充（注意：对于前向填充和后向填充，剩余的空缺的位置不同）

    * `downcast`：一个字典，用于类型转换。字典形式为： `{label->dtype}`，`dtype`可以为字符串，也可以为`np.float64`等。


![NaN_fillna0](../imgs/NaN_fillna0.JPG) ![NaN_fillna1](../imgs/NaN_fillna1.JPG) ![NaN_fillna2](../imgs/NaN_fillna2.JPG)

4. `DataFrame/Series.isnull()`：返回一个同样尺寸的布尔类型的对象，来指示每个值是否是`null`

`DataFrame/Series.notnull()`：返回一个同样尺寸的布尔类型的对象，来指示每个值是否是`not null` ![NaN_isnull](../imgs/NaN_isnull.JPG)

5. `fillna()`方法可以看作是值替换的一种特殊情况。更通用的是值替换`replace()`方法。

```
xxxxxxxxxx  Series/DataFrame.replace(to_replace=None, value=None, inplace=False, limit=None,   regex=False, method='pad', axis=None)
```

    * `to_replace`：一个字符串、正则表达式、列表、字典、`Series`、数值、`None`。指示了需要被替换的那些值

        * 字符串：则只有严格等于该字符串的那些值才被替换

        * 正则表达式：只有匹配该正则表达式的那些值才被替换（`regex=True`）

        * 列表：

            * 如果`to_place` 和`value`都是列表，则它们必须长度严格相等
            * 如果`regex=True`，则列表中所有字符串都是正则表达式。

        * 字典：字典的键对应了被替换的值，字典的值给出了替换值。如果是嵌套字典，则最外层的键给出了`column`名

        * `None`：此时`regex`必须是个字符串，该字符串可以表示正则表达式、列表、字典、`ndarray`等。如果`value`也是`None`，则`to_replace`必须是个嵌套字典。


    * `value`：一个字符串、正则表达式、列表、字典、`Series`、数值、`None`。给出了替换值。如果是个字典，则键指出了将填充哪些列（不在其中的那些列将不被填充）

    * `inplace`：一个布尔值。如果为`True`，则原地修改。否则创建新对象。

    * `limit`：一个整数，指定了连续填充的最大跨度。

    * `regex`：一个布尔值，或者与`to_replace`类型相同。

        * 如果为`True`，则`to_replace`必须是个字符串。
        * 如果是个字符串，则`to_replace`必须为`None`，因为它会被视作过滤器

    * `method`：指定填充类型。可以为`'pad'/'ffill'/'bfill'`。当`to_replace`是个列表时该参数有效。


![replace0](../imgs/replace0.JPG) ![replace1](../imgs/replace1.JPG) ![replace2](../imgs/replace2.JPG)

6. `interpolate`是通过前后数据插值来填充`NaN`。

```
xxxxxxxxxx  Series/DataFrame.interpolate(method='linear', axis=0, limit=None, inplace=False,  limit_direction='forward', downcast=None, **kwargs)
```

    * `method`：一个字符串，指定插值的方法。

        * `'linear'`：线性插值。只有它支持`MultiIndex`
        * `'index'`/`'values'`：使用索引标签的整数下标来辅助插值
        * `'nearest', 'zero', 'slinear', 'quadratic', 'cubic',`

    `'barycentric', 'polynomial'`使用`scipy.interpolate.interp1d`。对于`'polynomial'/'spline'` ，你需要传入一个`order`（一个整数）

        * `'krogh', 'piecewise_polynomial', 'spline', 'pchip','akima'`也使用了`scipy`的插值算法。它们使用索引标签的整数下标来辅助插值。
        * `'time'`： interpolation works on daily and higher resolution data to interpolate given length of interval

    * `axis`：指定插值的轴。如果为`0/'index'`则沿着0 轴；如果为`1/'columns'`则沿着 1 轴

    * `limit`：一个整数，指定插值时，如果有`K`个连续的`NaN`，则只插值其中的`limit`个

    * `limit_direction`：一个字符串。当设定了`limit`时，指定处理前面`limit`个`NaN`，还是后面`limit`个`NaN`。可以为`'forward'/'backward'/'both'`

    * `inplace`：一个布尔值。如果为`True`，则原地修改。否则创建新对象。

    * `downcast`：指定是否自动向下执行类型转换、

    * 其他参数是传递给`scipy`的插值函数的。


![interpolate0](../imgs/interpolate0.JPG) ![interpolate1](../imgs/interpolate1.JPG) ![interpolate2](../imgs/interpolate2.JPG)


### 4. 离散化

1. 连续数据常常会被离散化或者拆分成面元`bin`。可以通过`pandas.cut()`函数来实现：

```
xxxxxxxxxx  pandas.cut(x, bins, right=True, labels=None, retbins=False, precision=3,  include_lowest=False)
```

    * `x`：一维的数据。

    * `bins`：一个整数或者一个序列。

        * 整数：它指定了划分区间的数量。每个区间是等长的，且最左侧的区间的左侧比`x`最小值小`0.1%`；最右侧的区间的右侧比`x`最大值大`0.1%`。
        * 一个序列：它给出了`bins`的每个划分点。

    * `right`：一个布尔值。如果为`True`，则区间是左开右闭；否则区间是左闭右开的区间。

    * `labels`：一个`array`或者`None`。如果为一个`array`，则它指定了结果`bins`的`label`（要求长度与`bins`数量相同）。如果为`None`，则使用区间来表示。

    * `retbins`：一个布尔值。如果为`True`，则返回`bins`

    * `precision`：一个整数，给出存储和显示`bin label`的精度

    * `include_lowest`：一个布尔值。如果为`True`，则最左侧`bin`的左侧是闭区间


返回的是一个`Categorical`对象或者`Series`对象。该函数类似于`numpy.histogram()`函数。

2. 另外一个划分的函数是：

```
xxxxxxxxxx pandas.qcut(x, q, labels=None, retbins=False, precision=3)
```

    * `q`：一个整数或者序列。

        * 整数：它指定了划分区间的数量。
        * 一个序列：它给出了百分比划分点。比如`[0,0.25,0.5,0.75,0.1]`。`0.25`代表`25%`划分点。如果数据不在任何区间内，则标记为`NaN`。

    * 其他参数与`cut`相同。(`qcut`没有`bins`参数）


![cut0](../imgs/cut0.JPG) ![cut1](../imgs/cut1.JPG) ![cut2](../imgs/cut2.JPG)


## 七、 字符串操作

1. 通过`Series.map()`方法，所有字符串和正则表达式方法都能应用于各个值。但是如果存在`NaN`就会报错。为了解决这个问题，`pandas`提供了一些能够跳过`NaN`值的字符串操作方法。

2. `Series.str`能够将`Series`的值当作字符串处理，并且你可以通过`Series.str.func`来应用某些函数。其中`func`可以为：

    * `Series.str.capitalize()`
    * `Series.str.cat([others, sep, na_rep])`
    * `Series.str.center(width[, fillchar])`
    * `Series.str.contains(pat[, case=True, flags=0, na=nan, regex=True])`
    * `Series.str.count(pat[, flags])`
    * `Series.str.decode(encoding[, errors])`
    * `Series.str.encode(encoding[, errors])`
    * `Series.str.endswith(pat[, na])`
    * `Series.str.extract(pat[, flags, expand])`
    * `Series.str.extractall(pat[, flags])`
    * `Series.str.find(sub[, start, end])`
    * `Series.str.findall(pat[, flags])`
    * `Series.str.get(i)`
    * `Series.str.index(sub[, start, end])`
    * `Series.str.join(sep)`
    * `Series.str.len()`
    * `Series.str.ljust(width[, fillchar])`
    * `Series.str.lower()`
    * `Series.str.lstrip([to_strip])`
    * `Series.str.match(pat[, case=True, flags=0, na=nan, as_indexer=False])`
    * `Series.str.normalize(form)`
    * `Series.str.pad(width[, side, fillchar])`
    * `Series.str.partition([pat, expand])`
    * `Series.str.repeat(repeats)`
    * `Series.str.replace(pat, repl[, n, case, flags])`
    * `Series.str.rfind(sub[, start, end])`
    * `Series.str.rindex(sub[, start, end])`
    * `Series.str.rjust(width[, fillchar])`
    * `Series.str.rpartition([pat, expand])`
    * `Series.str.rstrip([to_strip])`
    * `Series.str.slice([start, stop, step])`
    * `Series.str.slice_replace([start, stop, repl])`
    * `Series.str.split([pat, n, expand])`
    * `Series.str.rsplit([pat, n, expand])`
    * `Series.str.startswith(pat[, na])`
    * `Series.str.strip([to_strip])`
    * `Series.str.swapcase()`
    * `Series.str.title()`
    * `Series.str.translate(table[, deletechars])`
    * `Series.str.upper()`
    * `Series.str.wrap(width, **kwargs)`
    * `Series.str.zfill(width)`
    * `Series.str.isalnum()`
    * `Series.str.isalpha()`
    * `Series.str.isdigit()`
    * `Series.str.isspace()`
    * `Series.str.islower()`
    * `Series.str.isupper()`
    * `Series.str.istitle()`
    * `Series.str.isnumeric()`
    * `Series.str.isdecimal()`
    * `Series.str.get_dummies([sep])`

![str](../imgs/str.JPG)

3. 你也可以通过`Series.str[:3]`这种索引操作来进行子串截取。或者使用`Series.str.get()`方法进行截取。 ![str_get](../imgs/str_get.JPG)


## 八、 聚合与分组

### 1. 分组

1. 分组运算的过程为：拆分-应用-合并

    * 拆分阶段：`Series/DataFrame`等数据根据你提供的一个或者多个键，被拆分为多组
    * 应用阶段：根据你提供的一个函数应用到这些分组上
    * 合并阶段：将函数的执行结果合并到最终结果中

2. 分组中有两种数据：源数据（被分组的对象），分组数据（用于划分源数据的）。

    * 源数据每一行(axis=0) 对应于分组数据中的一个元素。分组数据中每一个唯一值对应于一个分组。
    * 当分组数据也在源数据中时，可以直接通过指定列名来指定分组数据（值相同的为同一组）。

3. `.groupby()`方法是分组方法：

```
xxxxxxxxxx  Series/DataFrame.groupby(by=None, axis=0, level=None, as_index=True, sort=True,   group_keys=True, squeeze=False, **kwargs)
```

    * `by`：一个`mapping function`、`list of function`、一个字典、一个序列、一个元组、一个`list of column name`。它指定了分组数据。

        * 如果传入了函数，则在每个`index value`上调用函数来产生分组数据

        * 如果是`Series`或者字典，则根据每个`index value`在字典/`Series`中的值来产生分组数据

        * 如果是个`column label`，则使用该`label`抽取出来的一列数据产生分组数据

        * 如果是个`column label`的`list`，则使用一组`column label`抽取出来的多列数据作为分组数据。

        * 如果是个序列，则它直接指定了分组数据。

        * 如果是个序列的序列，则使用这些序列拼接成一个`MulitiIndex`，然后根据这个`MultiIndex`替换掉`index`后，根据`label value`来分组。（事实上并没有替换，只是用于说明这个过程）

        >         > 

        > 如果`axis=1`，则`index label`替换成`column label`




    * `axis`：指定沿着哪个轴分组。可以为`0/'index'`，表示沿着 0轴。可以为`1/'columns'`，表示沿着 1轴

    * `level`：一个整数、`level name`或者其序列。如果`axis`是个`MultiIndex`，则在指定级别上的索引来分组

    * `as_index`：一个布尔值。如果为`True`，则将`group label`作为输出的`index`。如果为`False`，则输出是`SQL`风格的分组（此时分组的`key`作为一列，而不是作为`index`）。`Series`中，该参数必须为`True`。

    * `sort`：一个布尔值。如果为`True`，则对分组的键进行排序。

    * `group_keys`：一个布尔值。如果为`True`，且调用了函数来决定分组，则添加分组键来区分不同的数据（否则你不知道每一行数据都对应于哪里）

    * `squeeze`：一个布尔值。如果为`True`，则尽可能的缩减结果的类型。


该函数返回一个`GroupBy`对象。

![groupby0](../imgs/groupby0.JPG) ![groupby1](../imgs/groupby1.JPG) ![groupby2](../imgs/groupby2.JPG)

4. 我们可以使用`dtype`来分组，此时`by=df.dtypes,axis=1`： ![groupby_dtype](../imgs/groupby_dtype.JPG)

5. 对于由`DataFrame`产生的`GroupBy`对象，我们可以用一个或者一组列名对其索引。它其实一个语法糖。

    * 如果索引是一个列名，则`df.groupby('key1')['data1']` 等价于`df['data1'].groupby(df['key1'])`

    * 如果索引是一个元组和序列，则 `df.groupby('key1')[['data1','data2']]` 并不等价于 `df[['data1','data2']].groupby(df['key1'])`，而是等同于 `df.groupby(df['key1'])`

        * 之所以用 `[['data1','data2']]`，是因为`df[['data1','data2']]`与`df['data1','data2']`语义不同。后者表示某个`label`是个元组，该元组的值为`'data1','data2'`。



![groupby_sugar](../imgs/groupby_sugar.JPG)

### 2. GroupBy对象

1. `GroupBy`对象是一个迭代器对象。迭代结果产生一组二元元组（由分组名和数据块组成）。

    * 如果有多重键，则元组的第一个元素将是由键组成的元组。
    * `dict(list(GroupBy_obj))`将生产一个字典，方便引用<br></br>

![GroupBy_iter1](../imgs/GroupBy_iter1.JPG) ![GroupBy_iter2](../imgs/GroupBy_iter2.JPG)

2. * `GroupBy.groups`属性返回一个字典： `{group name->group labels}`
    * `GroupBy.indices`属性返回一个字典：`{group name->group indices}`

![GroupBy_groups_indices](../imgs/GroupBy_groups_indices.JPG)

3. `GroupBy`的统计函数有（排除了`NaN`）：

    * `GroupBy.count()` ：计算各分组的非`NaN`的数量
    * `GroupBy.cumcount([ascending])`：计算累积分组数量
    * `GroupBy.first()`：计算每个分组的第一个非`NaN`值
    * `GroupBy.head([n])` ：返回每个分组的前 `n`个值
    * `GroupBy.last()` ：计算每个分组的最后一个非`NaN`值
    * `GroupBy.max()`：计算每个分组的最大值
    * `GroupBy.mean(*args, **kwargs)`：计算每个分组的均值
    * `GroupBy.median()`：计算每个分组的中位数
    * `GroupBy.min()`：计算每个分组的最小值
    * `GroupBy.nth(n[, dropna])`：计算每个分组第`n`行数据。 如果`n`是个整数列表，则也返回一个列表。
    * `GroupBy.ohlc()`：计算每个分组的开始、最高、最低、结束值
    * `GroupBy.prod()`：计算每个分组的乘
    * `GroupBy.size()`：计算每个分组的大小（包含了`NaN`）
    * `GroupBy.sem([ddof])` ：计算每个分组的`sem`（与均值的绝对误差之和）
    * `GroupBy.std([ddof])` ：计算每个分组的标准差
    * `GroupBy.sum()`：计算每个分组的和
    * `GroupBy.var([ddof])`：计算每个分组的方差
    * `GroupBy.tail([n])` ：返回每个分组的尾部 `n`个值

另外`SeriesGroupBy/DataFrameGroupBy`也支持`Series/DataFrame`的统计类方法以及其他方法：

```
xxxxxxxxxx  #SeriesGroupBy - DataFrameGroupBy 都有的方法：  .agg(arg, *args, **kwargs)  .all([axis, bool_only, ...])   .any([axis, bool_only, ...])  .bfill([limit])  .corr([method, min_periods])  .count()   .cov([min_periods])   .cummax([axis, skipna])   .cummin([axis, skipna])   .cumprod([axis])   .cumsum([axis])   .describe([percentiles, ...])   .diff([periods, axis])     .ffill([limit])   .fillna([value, method, ...])   .hist(data[, column, by, ...])   .idxmax([axis, skipna])   .idxmin([axis, skipna])   .mad([axis, skipna, level])  .pct_change([periods, ...])   .plot   .quantile([q, axis, ...])   .rank([axis, method, ...])   .resample(rule, *args, **kwargs)   .shift([periods, freq, axis])  .size()   .skew([axis, skipna, level, ...])   .take(indices[, axis, ...])  .tshift([periods, freq, axis])   #SeriesGroupBy独有的方法  SeriesGroupBy.nlargest(*args, **kwargs)   SeriesGroupBy.nsmallest(*args, **kwargs)   SeriesGroupBy.nunique([dropna])   SeriesGroupBy.unique()  SeriesGroupBy.value_counts([normalize, ...])     #DataFrameGroupBy独有的方法  DataFrameGroupBy.corrwith(other[, axis, drop])   DataFrameGroupBy.boxplot(grouped[, ...])
```

![GroupBy_method0](../imgs/GroupBy_method0.JPG) ![GroupBy_method1](../imgs/GroupBy_method1.JPG)

4. 如果你希望使用自己的聚合函数，只需要将其传入`.aggregate(func, *args, **kwargs)`或者`.agg()`方法即可。其中`func`接受一维数组，返回一个标量值。

    * 注意：自定义聚合函数会慢得多。这是因为在构造中间分组数据块时存在非常大的开销（函数调用、数据重排等）
    * 你可以将前面介绍的`GroupBy`的统计函数名以字符串的形式传入。
    * 如果你传入了一组函数或者函数名，则得到的结果中，相应的列就用对应的函数名命名。如果你希望提供一个自己的名字，则使用`(name,function)`元组的序列。其中`name`用作结果列的列名。
    * 如果你希望对不同的列采用不同的聚合函数，则向`agg()`传入一个字典。字典的键就是列名，值就是你希望对该列采用的函数。

![GroupBy_agg0](../imgs/GroupBy_agg0.JPG) ![GroupBy_agg1](../imgs/GroupBy_agg1.JPG)

5. `.get_group(key)`可以获取分组键对应的数据。

    * `key` ：不同的分组就是依靠它来区分的

6. `GroupBy`的下标操作将获得一个只包含源数据中指定列的新`GroupBy`对象

7. `GroupBy`类定义了`__getattr__()`方法，当获取`GroupBy`中未定义的属性时：

    * 如果属性名是源数据对象的某列的名称则，相当于`GroupBy[name]`，即获取针对该列的`GroupBy`对象
    * 如果属性名是源数据对象的方法，则相当于通过`.apply(name)`对每个分组调用该方法。


### 3. 分组级运算

1. `agg/aggregate`只是分组级运算其中的一种。它接受一维数组，返回一个标量值。

2. `transform`是另一个分组级运算。它也接受一维数组。只能返回两种结果：要么是一个标量值（该标量值将被广播），或者一个相同大小的结果数组。

    * 你无法通过字典来对不同的列进行不同的`transform`

```
xxxxxxxxxx  GroupBy.transform(func, *args, **kwargs)
```

![GroupBy_transform](../imgs/GroupBy_transform.JPG)

3. `apply`是另一个分组级运算。它是最一般化的分组级运算。它将待处理的对象拆分成多个片段，然后对各个片段调用传入的函数，最后尝试将各个片段组合到一起。

```
xxxxxxxxxx  GroupBy.apply(func, *args, **kwargs)
```

    * `func`：运算函数。其第一个位置参数为待处理对象。其返回值是一个标量值或者`pandas`对象。
    * `args/kwargs`是传递给`func`的额外的位置参数与关键字参数。

对于`DataFrame`的`.groupby`时，传递给`func`的第一个参数是`DataFrame`；对于`Series`的`.groupby`，传递给`func`的第一个参数是`Series`。

![GroupBy_apply](../imgs/GroupBy_apply.JPG)

4. `pd.cut()/qcut()`函数返回的是`Categorical`对象。我们可以用它作为`.groupby()`的`by`参数的值。这样可以实现桶分析。 ![GroupBy_cut](../imgs/Groupby_cut.JPG)


### 4. 透视表和交叉表

1. 透视表`pivot table`是一种数据汇总工具。它根据一个或者多个键对数据进行聚合，并根据行和列上的分组键将数据分配到各个单元格中。

    * 你可以通过`.groupby`功能以及索引的变换来手工实现这种功能

2. `DataFrame.pivot_table()`方法，以及`pandas.pivot_table()`函数都可以实现这种功能

```
xxxxxxxxxx  pandas.pivot_table(data, values=None, index=None, columns=None, aggfunc='mean',   fill_value=None, margins=False, dropna=True, margins_name='All')
```

    * `data`：一个`DataFrame`对象
    * `values`：指定哪些列将被聚合。默认聚合所有的数值列。
    * `index`：一个`index label`、一个`Grouper`、一个数组，或者前面这些类型的一个列表。它指定关于分组的列名或者其他分组键，出现在结果透视表的行
    * `columns`：一个`column label`、一个`Grouper`、一个数组，或者前面这些类型的一个列表。它指定关于分组的列名或者其他分组键，出现在结果透视表的列
    * `aggfunc`：一个函数或者函数的列表。默认为`numpy.mean`。它作为聚合函数。如果为函数的列表，则结果中会出现多级索引，函数名就是最外层的索引名。
    * `fill_value`：一个标量，用于替换`NaN`
    * `margins`：一个布尔值。如果为`True`，则添加行/列的总计。
    * `dropna`：一个布尔值。如果为`True`，则结果不包含这样的列：该列所有元素都是`NaN`
    * `margins_name`：一个字符串。当`margins=True`时，`margin`列的列名。

![pivot_table0](../imgs/pivot_table0.JPG) ![pivot_table1](../imgs/pivot_table1.JPG) ![pivot_table2](../imgs/pivot_table2.JPG)

3. 交叉表`cross-tabulation:crosstab`是一种用于计算分组频率的特殊透视表。我们可以使用`pivot_table()`函数实现透视表的功能，但是直接使用更方便：

```
xxxxxxxxxx  pandas.crosstab(index, columns, values=None, rownames=None, colnames=None,   aggfunc=None, margins=False, dropna=True, normalize=False)
```

    * `index`：一个`array-like`、`Series`或者前两种的列表。它给出了行的计算频数的数据。

    * `columns`：一个`array-like`、`Series`或者前两种的列表。它给出了列的计算频数的数据。

    * `values`：一个`array-like`，该数据用于聚合。如果出现了`values`，则必须提供`aggfunc`。

    * `aggfunc`：一个函数对象，是聚合函数。如果出现了`aggfunc`，则必须提供`values`。

    * `rownames`：一个序列。如果非空，则必须和结果的`row index`的`level`数量相等<br></br>

    * `colnames`：一个序列。如果非空，则必须和结果的`column index`的`level`数量相等<br></br>

    * `margins`：一个布尔值。如果为`True`，则添加行/列的总计。

    * `dropna`：一个布尔值。如果为`True`，则结果不包含这样的列：该列所有元素都是`NaN`

    * `normalize`：一个布尔值、字符串（`'all'/'index'/'columns'`）、或者整数`0/1`。它指定是否进行归一化处理（归一化为频率），否则就是频数。

        * 如果`'all'/True`，则对所有数据进行归一化
        * 如果为`'index'`：则对每一行归一化
        * 如果为`'columns'`：则对每一列归一化
        * 如果`margins`为`True`，则对`margins`也归一化。


`values`的作用是这样的：首先根据`index-columns`建立坐标。行坐标来自`index`，列坐标来自`columns`。在`index-columns-values`中，同一个坐标下的`values`组成`Series`。这个`Series`被`aggfunc`进行聚合，`aggfunc`接受一个`Series`，返回一个标量。此时就不再是对坐标点进行计数了，而是对`values`进行聚合。

![crosstab0](../imgs/crosstab0.JPG) ![crosstab1](../imgs/crosstab1.JPG) ![crosstab2](../imgs/crosstab2.JPG)


## 九、时间序列

1. `Pandas` 提供了表示时间点、时间段、时间间隔等三种与时间有关的类型，以及元素为这些类型的索引对象。`pandas`还提供了许多与时间序列相关的函数。

### 1. Python 中的时间

1. `Python`中，关于时间、日期处理的库有三个：`time`、`datetime`、`Calendar`。其中：`datetime`又有`datetime.date/datetime.time/datetime.datetime`三个类

#### 1.1 时区

1. 所有的时间都有一个时区。同样一个时间戳，根据不同的时区，它可以转换成不同的时间。
2. `pytz`模块的`common_timezones`可以获取常用的表示时区的字符串。你可以通过`pytz.timezone('timezone_str')`来创建时区对象。 ![timezone](../imgs/timezone.JPG)

#### 1.2 time 模块

1. `time`模块中，时间有三种表现形式：

    * `Unix`时间戳。指的是从`1970`年以来的秒数
    * 本地时间的`struct_time`形式：一个命名元组，第一位为年、第二位为月....
    * `UTC`时间的`struct_time`的形式：类似于上面的，只是为`UTC`时间。区别在于：前者是本地时间`local time`，后者是`UTC`时间

2. 查看当前时间的三种表现形式：

    * `Unix`时间戳： `time.time()`
    * `local struct_time`： `time.localtime()`
    * `utc struct_time`：`time.gmtime()`

![time_3kind_time](../imgs/time_3kind_time.JPG)

3. 三种格式之间的转换：

    * `timestamp--->local time`：`time.localtime(time_stamp)`
    * `timestamp--->utc time`：`time.gmtime(time_stamp)`
    * `local time--->timestamp`：`time.mktime(local_time)`
    * `utc time---> timestamp`：`calendar.timegm(utc_time)`

![time_time_invert](../imgs/time_time_invert.JPG)

4. 三种格式的时间转换为字符串：

    * `timestamp`：`time.ctime(time_stamp)`
    * `local struct_time time/utc struct_time time`：`time.asctime(struct_time)`<br></br>
    * 对于`local struct_time time/utc struct_time time`：你也可以使用`time.strftime(format_str,struct_time)` 来自定义格式化串。其中`format_str`为格式化串。

字符串转换为`struct_time`：`time.strptime(time_str,format_str)`。其中`format_str`为格式化串。 ![time_str_time](../imgs/time_str_time.JPG)

5. 查看当前时区： `time.timezone`。它返回的是距离`UTC`时间的距离（单位为秒）（>0，在美洲;<=0，在大多数欧洲，亚洲，非洲）。你无法通过修改它的值来修改时区。`time`模块使用的是系统的时区。 ![time_timezone](../imgs/time_timezone.JPG)


#### 1.3 datetime 模块

1. `datetime`模块中主要包含四个类：

    * `datetime.time`：时间类。只包含时、分、秒、微秒等时间信息
    * `datetime.date`：日期类。值包含年月日星期等日期信息
    * `datetime.datetime`：日期时间类。包含上述两者的全部信息
    * `datetime.timedelta`：日期时间间隔类，用来表示两个`datetime`之间的差值。

2. `datetime.time`的构造函数为：

```
xxxxxxxxxx  time([hour[, minute[, second[, microsecond[, tzinfo]]]]])
```

其中`tzinfo`就是时区对象。`0<=hour<24`，`0<=minute<60`，`0<=second<60`，`0<=microsecond<1000000`，否则抛出异常。`tzinfo`默认为`None`


属性有：

* `hour/minute/second/microsecond/tzinfo`

方法有：

* `time.replace([hour[, minute[, second[, microsecond[, tzinfo]]]]])`：替换对应的值，返回一个新的对象
* `time.isoformat()`：返回一个`ISO 8601`格式的字符串。
* `time.strftime(format)`：格式化`datetime.time`对象
* `time.tzname()`：如果时区为为`None`，则返回`None`。否则返回时区名称

![datetime_time](../imgs/datetime_time.JPG)

1. `datetime.date`的构造函数为：

```
xxxxxxxxxx  datetime.date(year, month, day)
```

    * `month`取值为`[1,12]`；`day`取值为`[1,num]`，`num`取决于指定的年和月有多少天

类方法有：`date.today()/date.fromtimestamp(timestamp)`

属性有：`year/month/day`

方法有：<br></br>

    * 运算：`date1-date2`、`date1+timedelta`、`date1-timedelta`、`date1<date2`
    * `date.replace(year,month,day)`：替换掉对应值，返回新对象
    * `date.timetuple()`：返回一个`time.struct_time`类型的元组
    * `date.weekday()`：返回代表星期几的数字。`0`为周日
    * `date.isoweekday()`：返回代表星期几的数字。`7`为周日
    * `date.isocalendar()`：返回一个元组`(ISO year,IOS week num,ISO weekday)`
    * `date.isoformat()`：返回一个`ISO 8601`格式的字符串。
    * `date.ctime()`：等价于`time.ctime(time.mktime(d.timetuple()))`
    * `date.strftime(format)`：格式化`datetime.date`对象

![datetime_date](../imgs/datetime_date.JPG)

2. `datetime.datetime`的构造函数为：

```
xxxxxxxxxx  datetime.datetime(year, month, day, hour=0, minute=0,   second=0, microsecond=0, tzinfo=None)
```

类方法有：

    * `datetime.today()`：返回当前的时间日期
    * `datetime.now(tz=None)`：返回指定时区当前的时间日期。如果`tz=None`，则等价于`datetime.today()`
    * `datetime.utcnow()`：返回当前的`UTC`时间日期
    * `datetime.fromtimestamp(timestamp, tz=None)`：根据时间戳，创建指定时区下的时间日期。
    * `datetime.utcfromtimestamp(timestamp)`：根据时间戳，创建`UTC`下的时间日期。
    * `datetime.combine(date, time)`：从`date`和`time`对象中创建`datetime`
    * `datetime.strptime(date_string, format)`：从字符串中创建`datetime`

属性有：`year/month/day/hour/minute/second/microsecond/tzinfo`

方法有：

    * 运算：`datetime1-datetime2`、`datetime1+timedelta`、 `datetime1-timedelta`、`datetime1<datetime2`
    * `datetime.date()`：返回一个`date`对象
    * `datetime.time()`：返回一个`time`对象（该`time`的`tzinfo=None`）
    * `datetime.timetz()`：返回一个`time`对象（该`time`的`tzinfo`为`datetime`的`tzinfo`）
    * `datetime.replace([year[, month[, day[, hour[, minute[, second` `[, microsecond[, tzinfo]]]]]]]])`：替换掉指定值，返回新对象
    * `datetime.astimezone(tz=None)` ：调整时区。如果`tz=None`，则默认采用系统时区。注意，调整前后的`UTC`时间是相同的。
    * `datetime.tzname()`：返回时区名字
    * `datetime.timetuple()`：返回一个`time.struct_time`这样的命名元组
    * `datetime.utctimetuple()`：返回一个`time.struct_time`这样的命名元组，注意它是在`UTC`时间下的，而不是`local time`下的
    * `datetime.timestamp()`：返回一个时间戳
    * `datetime.weekday()`：返回代表星期几的数字。`0`为周日
    * `datetime.isoweekday()`：返回代表星期几的数字。`7`为周日
    * `datetime.isocalendar()`：返回一个元组`(ISO year,IOS week num,ISO weekday)`
    * `datetime.isoformat(sep='T')`：返回一个`ISO 8601`格式的字符串。
    * `datetime.ctime()`：等价于`time.ctime(time.mktime(d.timetuple()))`
    * `datetime.strftime(format)`：格式化`datetime.datetime`对象。

注意：不能将`tzinfo=None`和`tzinfo!=None`的两个`datetime`进行运算。

3. 下面是常用的格式化字符串的定义：

    * `'%Y'`：4位数的年
    * `'%y'`：2位数的年
    * `'%m'`：2位数的月 `[01,12]`
    * `'%d'`：2位数的日 `[01,31]`
    * `'%H'`：小时（24小时制）`[00,23]`
    * `'%I'`：小时（12小时制）`[01,12]`
    * `'%M'`：2位数的分`[00,59]`
    * `'%S'`：秒`[00,61]`，`61`秒用于闰秒
    * `'%w'`：用整数表示的星期几`[0,6]`，0 表示星期日
    * `'%U'`：每年的第几周`[00,53]`。星期天表示每周的第一天。每年的第一个星期天之前的那几天被认为是第 0 周
    * `'%W'`：每年的第几周`[00,53]`。星期一表示每周的第一天。每年的第一个星期一之前的那几天被认为是第 0 周
    * `'%z'`：以`+HHMM`或者`-HHMM`表示的`UTC`时区偏移量。如果未指定时区，则返回空字符串。
    * `'%F'`：以`%Y-%m-%d`简写的形式
    * `'%D'`：以`%m/%d/%y`简写的形式
    * `'%a'`：星期几的简称
    * `'%A'`：星期几的全称
    * `'%b'`：月份的简称
    * `'%B'`：月份的全称
    * `'%c'`：完整的日期和时间<br></br>
    * `'%q'`：季度`[01,04]`

![datetime_datetime](../imgs/datetime_datetime.JPG)

4. `timedelta`代表一段时间。其构造：

```
xxxxxxxxxx  datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,  minutes=0, hours=0, weeks=0)
```

在内部，只存储秒、微秒。其他时间单位都转换为秒和微秒。


实例属性（只读）：

* `days/seconds/microseconds`

实例方法：

* `timedelta.total_seconds()`：返回总秒数。

![datetime_timedelta](../imgs/datetime_timedelta.JPG)

### 2. 时间点 Timestamp

1. 时间点：`Timestamp`对象从`Python`的`datetime`类继承，它表示时间轴上的一个点。

```
xxxxxxxxxx  pd.Timestamp(ts_input=<object object at 0x0000000001E8F340>, freq=None, tz=None,   unit=None, year=None, month=None, day=None, hour=None, minute=None,   second=None, microsecond=None, tzinfo=None, offset=None)
```

参数：

    * `ts_input`：一个`datetime-like/str/int/float`，该值将被转换成`Timestamp`
    * `freq`：一个字符串或者`DateOffset`，给出了偏移量
    * `tz`：一个字符串或者`pytz.timezone`对象，给出了时区
    * `unit`：一个字符串。当`ts_input`为整数或者浮点数时，给出了转换单位
    * `offset`：废弃的，推荐使用`freq`
    * 其他的参数来自于`datetime.datetime`。它们要么使用位置参数，要么使用关键字参数，但是不能混用

![Timestamp_create](../imgs/Timestamp_create.JPG)

属性有：

    * `year/month/day/hour/minute/second/microsecond/nanosecond`，这些属性都为整数
    * `tzinfo`：时区信息（默认为`None`），它是一个`datetime.tzinfo`对象<br></br>
    * `dayofweek/dayofyear/days_in_mounth/freqstr/quarter/weekofyear/...`
    * `value`:保存的是`UTC`时间戳（自`UNIX`纪元1970年1月1日以来的纳秒数），该值在时区转换过程中保持不变

![Timestamp_property](../imgs/Timestamp_property.JPG)

类方法有：

    * `combine(date, time)`：通过`datetime.date`和`datetime.time`创建一个`Timestamp`
    * `fromtimestamp(ts)`：通过时间戳创建一个`Timestamp`
    * `now(tz=None)`：创建一个指定时区的当前时间。
    * `doday(tz=None)`：创建一个指定时区的当前时间。
    * `utcfromtimestamp(ts)`：从时间戳创建一个`UTC Timestamp`，其`tzinfo=None`
    * `utcnow()`：创建一个当前的`UTC Timestamp`，其`tzinfo=UTC`

![Timestamp_cls_method](../imgs/Timestamp_cls_method.JPG)

方法有：

    * `.astimezone(tz)/.tz_convert(tz)`：将一个`tz-aware Timestamp`转换时区
    * `.isoformat(sep='T')`：返回一个`ISO 8601`格式的字符串。
    * `.normalize()`：将`Timestamp`调整到午夜（保留`tzinfo`）
    * `replace(**kwds)`：调整对应值，返回一个新对象
    * `.to_period(self, freq=None)`：返回一个`Period`对象`
    * `.tz_localize(self, tz, ambiguous='raise', errors='raise')`：将一个`tz-naive Timestamp` ，利用`tz`转换为一个`tz-aware Timestamp`
    * `.to_pydatetime(...)`：转换为`python datetime`对象
    * `.to_datetime64(...)`：转换为`numpy.datetime64`对象
    * 从`datetime.date/datetime.datetime`继承而来的方法

![Timestamp_method0](../imgs/Timestamp_method0.JPG) ![Timestamp_method1](../imgs/Timestamp_method1.JPG)

默认情况下，`pands`中的`Timestamp`是`tz-naive`，即`tz`字段为`None`。 `Timestamp`提供了方便的时区转换功能。如果`tz`非空，则是`tz-aware Timestamp`。不同时区的时间可以比较，但是`naive Timestamp`和`localized Timestamp`无法比较。

`Timestamp`的减法，要求两个`Timestamp`要么都是同一个时区下，要么都是`tz-naive`的。<br></br>

2. `DateOffset`对象：是一个表示日期偏移对象。`Timestamp`加一个日期偏移，结果还是一个`Timestamp`对象。其声明为：

```
xxxxxxxxxx  pd.DateOffset(n=1, normalize=False, **kwds)
```

通常我们使用的是其子类（它们位于`pandas.tseries.offsets`中）：

    * `Day`：日历日
    * `BusinessDay`：工作日<br></br>
    * `Hour`：小时
    * `Minute`：分钟
    * `Second`：秒
    * `Milli`：毫秒
    * `Micro`：微秒
    * `MonthEnd`：每月最后一个日历日
    * `BusinessMonthEnd`：每月最后一个工作日<br></br>
    * `MonthBegin`：每月第一个日历日
    * `BusinessMonthBegin`：每月第一个工作日<br></br>
    * `Week`：每周几

`Day(2)`：表示两个工作日。

`DateOffset`对象可以加在`datetime/Timestamp`对象上。如果是`MonthEnd`这种加上`Timestamp`，则第一次增量会将原日期向前滚动到符合频率规则的下一个日期。

    * 你可以通过`DateOffset.rollforward(time_stamp)`、`DateOffset.rollback(time_stamp)`来显式地将日期向前或者向后滚动

![DateOffset](../imgs/DateOffset.JPG)

3. 利用 `str(dt_obj)`函数或者`datetime.strftime(format_str)`方法，可以将`datetime`对象和`Timestamp`对象格式化为字符串。而利用`datetime.strptime(dt_str,format_str)`类方法，可以从字符串中创建日期。其中`dt_str`为日期字符串，如`'2011-11-12'`；`format_str`为格式化字符串，如`'%Y-%m-%d'`。

    * `datetime.strptime`是对已知格式进行日期解析的最佳方式。
    * 对于一些常见的日期格式，使用`dateutil`这个第三方包中的`parser.parse(dt_str)`，它几乎可以解析所有的日期表示形式。
    * `pandas.to_datetime()`方法可以解析多种不同的日期表示形式，将字符串转换为日期。对于标准日期格式的解析非常快。如果发现无法解析（如不是一个日期），则返回一个`NaT`（`Not a Time`），它是时间戳数据中的`NA`值。

4. `Timedelta`对象：表示时间间隔。它等价于`datetime.timedelta`类。

```
xxxxxxxxxx  pd.Timedelta(value=<object object at 0x00000000004BF340>, unit=None, **kwargs)
```

参数：

    * `value`：一个`Timedelta`对象，或者`datetime.timedelta`，或者`np.timedelta64`、或者一个整数，或者一个字符串。指定了时间间隔
    * `unit`：一个字符串，指明了当输入时整数时，其单位。可以为`'D'/'h'/'m'/'s'/'ms'/'us'/'ns'`
    * `days/seconds/microseconds/nanoseconds`：都是数值。给出了某个时间单位下的时间间隔

方法：

    * `to_timedelta64()`：返回一个`numpy.timedelta64`类型（按照纳秒的精度）
    * `total_seconds()`：返回总的时间间隔，单位秒（精度为纳秒）
    * `to_pytimedelta()`：返回一个`datetime.timedelta`对象

属性：

    * `components`：返回各成分的命名元组
    * `days/seconds/microseconds/nanoseconds`：返回各个成分
    * `delta`：返回总的时常（纳秒计）

一个时间间隔有天数、秒数等等属性。注意：所有的这些值与对应的单位相乘的和，才是总的时间间隔。

两个`Timestamp`相减可以得到时间间隔`Timedelta`

> > 

> `DateOffset`也一定程度上表示时间间隔，但是`DateOffset`更侧重于按照某个固定的频率的间隔，比如一天、一个月、一周等。



![Timedelta](../imgs/Timedelta.JPG)


### 3. 时间段 Period

1. `Period`表示一个标准的时间段（如某年，某月）。时间段的长短由`freq`属性决定。

```
xxxxxxxxxx  pd.Period(value=None, freq=None, ordinal=None, year=None, month=None,   quarter=None, day=None, hour=None, minute=None, second=None)
```

参数：

    * `value`：一个`Period`对象或者字符串（如`'4Q2016'`），它表示一个时区段。默认为`None`
    * `freq`：一个字符串，表示区间长度。可选的值从下面函数获取：
    * `pandas.tseries.frequencies._period_code_map.keys()`
    * `pandas.tseries.frequencies._period_alias_dictionary()`
    * 其他的参数和前面的其他类的构造函数类似。其中`quarter`表示季度。

属性：

    * `day/dayofweek/dayofyear/hour/minute/quarter/second/` `year/week/weekday/weekofyear/year`：对应的属性
    * `end_time`：区间结束的`Timestamp`。`start_time`：区间开始的`Timestamp`
    * `freq`

方法：

    * `.asfreq(freq,how)`：转换为其他区间。其中`freq`为字符串。`how`可以为`'E'/'end'`，表示包含区间结束；`'S'/'start'`表示包含区间开始。
    * `.now(freq)`：返回当期日期对应`freq`下的`Period`
    * `strftime(format)`：给出`Period`的格式化字符串表示
    * `to_timestamp(freq,how)`：转换为`Timestamp`。<br></br>

![Period](../imgs/Period.JPG)

2. `pands`中的频率是由一个基础频率和一个倍数组成。

    * 基础频率通常以一个字符串别名表示，如`'M'`表示每月，`'H'`表示每小时。
    * 对于每个基础频率，都有一个`DateOffset`对象与之对应。如`pandas.tseries.offsets`中的`Hour/Minute`。`Hour(4)`表示日期偏移为 4小时。
    * 倍数为基础频率之前的数字，如`'4H'`。也可以组合多个频率`4H30min`

有些频率描述的时间点并不是均匀间隔的。如`'M'`就取决于每个月的天数。下面是一些常用的基础频率

    * `'D'`：偏移量类型为`Day`，为每日历日
    * `'B'`：偏移量类型为`BusinessDay`，为每工作日<br></br>
    * `'H'`：偏移量类型为`Hour`，为每小时
    * `'T'`或者`'min'`：偏移量类型为`Minute`，为每分钟
    * `'S'`：偏移量类型为`Second`，为每秒
    * `'L'`或者`'ms'`：偏移量类型为`Milli`，为每毫秒
    * `'U'`：偏移量类型为`Micro`，为每微秒
    * `'M'`：偏移量类型为`MonthEnd`，为每月最后一个日历日
    * `'BM'`：偏移量类型为`BusinessMonthEnd`，为每月最后一个工作日<br></br>
    * `'MS'`：偏移量类型为`MonthBegin`，为每月第一个日历日
    * `'BMS'`：偏移量类型为`BusinessMonthBegin`，为每月第一个工作日<br></br>
    * `'W-Mon'...'W-TUE`：偏移量类型为`Week`，为指定星期几(`MON/TUE/WED/THU/FRI/SAT/SUN`)开始算起，每周<br></br>

3. 调用`Timestamp`对象的`.to_period(freq)`方法能将时间点转化为包含该时间点的时间段。 ![Timestamp_to_period](../imgs/Timestamp_to_period.JPG)

4. `Period`的`.asfreq()`方法可以实现时间段的频率转换。 ![Period_visio](../imgs/Period_visio.JPG)

创建`Period`时，我们可以传入一个`Timestamp`的各分量（由`year/month...`等提供）。创建的`Period`是包含该时刻，且指定频率。在使用`Timestamp.to_period(freq)`也是如此。

给定一个频率的`Period`，如果转换到更低频的`Period`，则非常简单：返回指定频率下的包含本`Period`的那个`Period`即可。如果想转换到更高频的`Period`，则由于在本`Period`下，对应了很多个高频的`Period`，则返回哪一个，由`how`参数指定：

    * `how=S`：返回最开头的那个`Period`
    * `how=E`：返回最末尾的那个`Period`

而`Period.to_timestamp(freq,how)`方法中，我们首先进行时间段的频率转换，然后提取该频率的`Period`开始处的`Timestamp`

![Period_asfreq](../imgs/Period_asfreq.JPG)

5. 如果两个`Period`对象有相同的频率，则它们的差就是它们之间的单位数量。


### 4. DatetimeIndex

1. `DatetimeIndex`是一种索引，它的各个标量值是`Timestamp`对象，它用`numpy`的`datetime64`数据类型以纳秒形式存储时间戳。

```
xxxxxxxxxx  pd.DatetimeIndex(data=None, freq=None, start=None, end=None, periods=None,  copy=False, name=None, tz=None, verify_integrity=True, normalize=False,  closed=None, ambiguous='raise', dtype=None, **kwargs)
```

    * `data`：一个`array-like`对象，给出了各个时间
    * `copy`：一个布尔值，如果为`True` 则拷贝基础数据
    * `freq`：一个字符串或者`DateOffset`对象，给出了频率
    * `start`：一个`datetime-like`，指定了起始时间。如果`data=None`，则使用它来生成时间
    * `periods`：一个整数（大于0），指定生成多少个时间。如果`data=None`，则使用它来生成时间
    * `end`：一个`datetime-like`，指定了结束时间。如果`data=None`且`periods=None`，则使用它来生成时间
    * `closed`：一个字符串或者`None`。用于指示区间的类型。可以为`'left'`（左闭右开），`'right'`（左开右闭），`None`（左闭右闭）
    * `tz`： 一个字符串，指定了时区。如果非空，则返回的是`localized DatetimeIndex`
    * `name`：指定了`Index`的名字

![DatetimeIndex](../imgs/DatetimeIndex.JPG)

2. `pandas.date_range()`函数可以生成指定长度的`DatetimeIndex`

```
xxxxxxxxxx  pandas.date_range(start=None, end=None, periods=None, freq='D', tz=None,   normalize=False,name=None, closed=None, **kwargs)
```

各参数意义参考`DatetimeIndex`的构造函数。

3. 对于以`DatetimeIndex`为索引的`Series`，我们可以通过指定`Timestamp`切片来截取指定时间区间的数据（也可以是对应的字符串来指定`Timestamp`）。注意：这里的`Timestamp`可以并不是`DatetimeIndex`的`key`。

![DatetimeIndex_select0](../imgs/DatetimeIndex_select0.JPG) ![DatetimeIndex_select1](../imgs/DatetimeIndex_select1.JPG)

4. `DatetimeIndex`的方法有：（`DatetimeIndex`继承自`Index`，因此它有`Index`的所有方法）

    * `indexer_at_time(time, asof=False)`：返回指定`time`的位置
    * `indexer_between_time( start_time, end_time, include_start=True,` `include_end=True)`：返回指定的两个时间之间的索引的位置
    * `normalize()`：将时间调整到午夜
    * `to_period( freq=None)`：以指定`freq`转换到`PeriodIndex`
    * `to_perioddelta( freq)`：计算不同索引值的`Timedelta`，然后转换成一个`TimedeldaIndex`
    * `to_pydatetime`/`tz_convert`/`tz_localize`：对每个时间使用`Timestamp`对应的方法

任何`Timestamp`的属性都可以作用于`DatetimeIndex`。 ![DatetimeIndex_method](../imgs/DatetimeIndex_method.JPG)


### 5. PeriodIndex

1. 如果将一个`Period`序列作为索引，则该索引就是`PeriodIndex`类型。其各位置的值为`Period`对象。

```
xxxxxxxxxx  pd.PeriodIndex(data=None, ordinal=None, freq=None, start=None, end=None,  periods=None, copy=False, name=None, tz=None, dtype=None, **kwargs)
```

    * `data`：一个`array-like`对象，给出了各个时间段
    * `copy`：一个布尔值，如果为`True` 则拷贝基础数据
    * `freq`：一个字符串或者`period`对象，给出了频率
    * `start`：一个`period-like`，指定了起始时间段。如果`data=None`，则使用它来生成时间段
    * `periods`：一个整数（大于0），指定生成多少个时间段。如果`data=None`，则使用它来生成时间段
    * `end`：一个`period-like`，指定了结束时间段。如果`data=None`且`periods=None`，则使用它来生成时间段
    * `year/month/quarter/day/hour/minute/second`：一个整数、`array`或者`Series` 。通过它们可以组装出一个`Period`序列。
    * `tz`： 一个字符串，指定了时区。如果非空，则返回的是`localized DatetimeIndex`
    * `name`：指定了`Index`的名字

![PeriodIndex](../imgs/PeriodIndex.JPG)

2. `pandas.period_range()`函数可以生成指定长度的`PeriodIndex`

```
xxxxxxxxxx  pd.period_range(start=None, end=None, periods=None, freq='D', name=None)
```

参数意义参见`PeriodIndex`的构造函数。

3. `PeriodIndex`的方法有：（`PeriodIndex`继承自`Index`，因此它有`Index`的所有方法）

    * `asfreq( freq=None, how='E')`：转换成另一种频率的时间段
    * `to_timestamp(self, freq=None, how='start')`：转成`DatetimeIndex`
    * `tz_convert(self, tz)/tz_localize(self, tz, infer_dst=False)`：转成对应时区的`DatetimeIndex`

任何`Period`的属性都可以作用于`PeriodIndex`。 ![PeriodIndex_method](../imgs/PeriodIndex_method.JPG)


### 6. resample 和频率转换

1. `Series/DataFrame`有一个`shift()`方法用于执行单纯的前移或者后移操作，：

```
xxxxxxxxxx  Series/DataFrame.shift(periods=1, freq=None, axis=0)
```

    * `periods`:一个整数（可以为负的），指定移动的数量。对于时间序列，单位由`freq`指定。
    * `freq`：一个`DateOffset/timedelta`或者一个频率字符串。指定移动的单位。注意，如果为`PeriodIndex`，则`freq`必须和它匹配。
    * `axis`：为`0/'index'`表示沿着0轴移动；为`1/'columns'`表示沿着1轴移动

如果为时间序列，则该方法移动并建立一个新的索引，但是`Series/DataFrame`的值不变。对于非时间序列，则保持索引不变，而移动`Series/DataFrame`的值。

> > 

> 本质上，时间序列和非时间序列都是`index_i-->value_i`转换成`index_i+n-->value_i`。只是时间序列截取的都是有效值，非时间序列截取了`NaN`而已。



![TimeSeries_shift0](../imgs/TimeSeries_shift0.JPG) ![TimeSeries_shift1](../imgs/TimeSeries_shift1.JPG) ![shift](../imgs/shift.JPG)

2. 重采样`resampling`指的是将时间序列从一个频率转换到另一个频率的处理过程。

    * 将高频数据转换到低频数据称作降采样。降采样时，待聚合的数据不必拥有固定的频率，期望的频率（低频的）会自动划分聚合的`bin`的边界。这些`bin`将时间序列拆分为多个片段。这些片段都是半开放的，一个数据点只能属于一个片段，所有的片段的并集组成了整个时间帧。在对数据降采样时，只需要考虑两样：
    * 各个区间哪边是闭合的
    * 如何标记各个聚合`bin`，用区间的开头还是结尾
    * 将低频数据转换到高频数据称作升采样。将数据转换到高频时，就不需要聚合了，而是插值，默认引入缺失值。插值的填充和填充方式与`fillna/reindex`的一样。
    * 在对时间段`Period`进行重采样时，升采样稍微麻烦点，因为你必须决定：哪个高频区间代表原区间。就像`asfreq`一样，`convention`可以设置为`'end'/'start'`

有些重采样并不划分到上述两者之中。比如将`W-WED`（每周三）转换到`W-FRI`（每周五）。另外，由于`Period`是时间区间，所以升采样和降采样的规则就比较严格：

    * 降采样中，目标频率必须包含原频率。如`Day->Month`，目标频率为每月，原频率为每天。
    * 升采样中，原频率必须包含目标频率。如`Day->Hour`，目标频率为每小时，原频率为每天。

如果不满足这些条件，则会引发异常。

3. `resample` 方法：

```
xxxxxxxxxx  Series/DataFrame.resample(rule, how=None, axis=0, fill_method=None, closed=None,   label=None, convention='start', kind=None, loffset=None, limit=None,   base=0, on=None, level=None)
```

    * `rule`：一个字符串，指定了重采样的目标频率

    * `axis`：为`0/'index'`表示沿着0轴重采样；为`1/'columns'`表示沿着1轴重采样

    * `closed`：一个字符串，指定降采样中，各时间段的哪一端是闭合的。如果为`'right'`，则是左开右闭区间；如果为`'left'`，则是左闭右开区间

    * `label`：在降采样中，如何设置聚合值的标签。可以为`'right'/'left'`（面元的右边界或者左边界）。如：`9:30~9:35`这5分钟会被标记为`9:30`或者`9:35`

    * `how`：用于产生聚合值的函数名或者数组函数。可以为`'mean'/'ohlc'/np.max`等。默认为`'mean'`，其他常用的有：`'first'/'last'/'median'/'ohlc'/'max'/'min'`。

    >     > 

    > `how`被废弃了，而是采用`.resample().mean()`这种方案。



    * `convention`：当重采样时期时，将低频转换到高频所采用的约定。可以为`'s'/'start'`（用第一个高频）或者`'e'/'end'`（用最后一个高频）

    * `loffset`：一个`timedelta`，用于调整面元（`bin`）标签。如`'-1s'`，会将用于将聚合的结果标签调早1秒，从而更容易表示它代表哪个区间。比如`12:00:00`你就难以判别是哪个区间，而`11:59:59`就很容易知道它是那个区间。

    >     > 

    > 你也可以对调用结果对象使用`.shift()`方法来实现该目的，这样就不必设置`loffset`了



    * `base`：一个整数，默认为0.用于聚合过程中，当频率可以整除`1D`（比如`4H`）时，第一个完整的分组从哪个元素开始的。如`rule='4H'`，`base=2`，则`Series[0:1]`作为一个分组，`Series[2:6]....`作为一个分组....

    * `on`：一个字符串，对于`DataFrame`，它指定了重采样的列。该列必须是`datetime-like`

    * `level`：一个字符串或者整数。对于`MultiIndex`，该参数指定了被重采样的子索引

    * `fill_method`：一个字符串，指定升采样时，如何插值。如`'ffill'/'bfill'`。默认不插值

    >     > 

    > 该参数被废弃。推荐使用`.resample().ffill()`这种方案。而`limit`作为`ffill()`的参数。



    * `limit`：一个整数。指定向前或者向后填充时，运行连续填充的最大单元数量

    * `kind`：一个字符串，指定聚合到时间段`Period`还是时间戳`Timestamp`。默认聚合到时间序列的索引类型


![resample0](../imgs/resample0.JPG) ![resample1](../imgs/resample1.JPG) ![resample2](../imgs/resample2.JPG) ![resample3](../imgs/resample3.JPG) ![resample4](../imgs/resample4.JPG)

4. `OHLC`重采样是计算`bin`中的四个值：开盘值（第一个值）、收盘值（最后一个值）、最高值（最大值）、最低值（最小值）

5. 另一种降采样的办法是：使用`groupby`功能。如：

```
xxxxxxxxxx  series.groupby(lambda x:x.month).mean()
```

如果你想根据年份来聚合，则使用`x.year`。


![resample_groupby](../imgs/resample_groupby.JPG)

## 十、 DataFrame 绘图

1. `matplotlib`是一种比较低级的工具，`pandas`中有许多利用`DataFrame`对象数据组织特点来创建标准图表的高级绘图方法。

2. `Series/DataFrame.plot()`：绘制图形。

```
xxxxxxxxxx  Series.plot(kind='line', ax=None, figsize=None, use_index=True, title=None, grid=None,  legend=False, style=None, logx=False, logy=False,loglog=False,xticks=None,yticks=None,  xlim=None, ylim=None, rot=None, fontsize=None, colormap=None, table=False, yerr=None,   xerr=None, label=None, secondary_y=False, **kwds)  DataFrame.plot(x=None, y=None, kind='line', ax=None, subplots=False, sharex=None,   sharey=False, layout=None, figsize=None, use_index=True, title=None, grid=None,   legend=True, style=None, logx=False, logy=False, loglog=False, xticks=None,   yticks=None, xlim=None, ylim=None, rot=None, fontsize=None, colormap=None,  table=False, yerr=None, xerr=None, secondary_y=False, sort_columns=False, **kwds)
```

    * `kind`：绘制的类型。可以为：`'line'`、`'bar'`、`'barh'`（水平的`bar`）、`'hist'`、`'box'`、`'kde'`（核密度估计）、`'density'`（类似`kde`）、`'area'`、`'pie'`
    * `ax`：一个`Axes`实例对象。如果为空，则是`plt.gca()`的返回值（当前`Axes`）
    * `figsize`：一个元组，指定图片大小（单位为英寸）
    * `use_index`：一个布尔值。如果为`True`，则使用`index`作为`X`轴。
    * `title`：图形的标题
    * `grid`：一个布尔值。如果为`True`，则开启网格
    * `legend`：一个布尔值，如果为`True`，则放置图例
    * `style`：一个列表或者字典，给出了每一列的线型
    * `logx`：一个布尔值，如果为`True`，则`x`轴为对数型
    * `logy`：一个布尔值，如果为`True`，则`y`轴为对数型
    * `loglog`：一个布尔值，如果为`True`，则`x`轴和`y`轴都为对数型
    * `xticks`：一个序列，用于给出`xticks`
    * `yticks`：一个序列，用于给出`yticks`
    * `xlim`：一个二元的元组或者序列，给出`x`轴范围
    * `ylim`：一个二元的元组或者序列，给出`y`轴范围
    * `rot`：一个整数，给出了`x`轴和`y`轴`tick`旋转角度（不是弧度）。
    * `fontsize`：一个整数，给出了`xtick/ytick`的字体大小
    * `colormap`：一个字符串或者`colormap`对象，给出了`colormap`
    * `colorbar`：一个布尔值。如果为`True`，则绘制`colorbar`（只用于`scatter`和`hexbin`图中）
    * `position`：一个浮点数。给出了`bar`图中，各`bar`的对其位置（0表示`bar`的左侧与它的坐标 对其；1表示`bar`的右侧与它的坐标对其）
    * `layout`：一个元组。给出了`(rows,columns)`
    * `table`：一个布尔值或者`Series/DataFrame`。如果为`True`，则将本`Series/DataFrame`绘制为一个表格；如果为`Series/DataFrame`，则将该参数绘制为表格
    * `yerr`：用于绘制`Error Bar`
    * `xerr`：用于绘制`Error Bar`
    * `label`：`plot`的`label`参数
    * `secondary_y`：一个布尔值或者一个整数序列。如果为`True`，则`y`轴绘制在右侧
    * `mark_right`：一个布尔值，如果为`True`且`secondary_y=True`，则在图例中标记为`right`
    * `kwds`：传递给`matplotlib`中的`plot`函数的其他关键字参数

在`DataFrame.plot`中，下面的参数意义为：

    * `x`：`label`或者`position`
    * `y`： `label`或者`position`
    * `subplots`：一个布尔值，如果为`True`，则将每一列作为一个子图来绘制
    * `sharex`：一个布尔值。如果为`True`，且`subplots=True`，则子图共享`x`轴
    * `sharey`：一个布尔值。如果为`True`，且`subplots=True`，则子图共享`y`轴
    * `stacked`：一个布尔值。在`bar`中，如果为`True`，则将柱状图堆积起来
    * `sort_columns`：一个布尔值。如果为`True`，则根据列名来决定绘制的先后顺序。

它们返回的是`AxesSubplot`对象，或者`AxesSubplot`的`ndarray`

![plot0](../imgs/plot0.JPG) ![plot1](../imgs/plot1.JPG) ![plot2](../imgs/plot2.JPG) ![plot3](../imgs/plot3.JPG) ![plot4](../imgs/plot4.JPG) ![plot5](../imgs/plot5.JPG) ![plot6](../imgs/plot6.JPG) ![plot7](../imgs/plot7.JPG) ![plot8](../imgs/plot8.JPG)

3. 给出一组序列，我们可以手工绘制每个序列的散布图，以及各自的核密度估计。我们可以使用`scatter_matrix`函数：

```
xxxxxxxxxx  pandas.tools.plotting.scatter_matrix(frame, alpha=0.5, figsize=None, ax=None,   grid=False, diagonal='hist', marker='.', density_kwds=None, hist_kwds=None,   range_padding=0.05, **kwds)
```

    * `frame`：为`DataFrame`对象
    * `diagonal`：选择对角线上的图形类型。可以为`'hist'/'kde'`
    * `hist_kwds`：绘制`hist`的参数
    * `density_kwds`：绘制`kde`的参数
    * `range_padding`：一个浮点数，用于延伸`x/y`轴的范围。如果它为`0.1`，表示`x`轴延伸`x_max-xmin`的0.1倍 每一个子图是这样生成的：以`DataFrame`中某一列为横坐标，另一列为纵坐标生成的散点图。

![scatter_matrix](../imgs/scatter_matrix.JPG)


## 十一、 移动窗口函数

1. 时间序列的移动窗口上的各种统计函数是一种常见的操作。这一类函数我们称作移动窗口函数

    * 与其他统计函数一样，移动窗口函数也排除了`NA`值

    * 所谓移动窗口，就是两层含义：

        * 窗口：统计函数作用的对象为该窗口内的数值
        * 移动：该窗口是移动的，每个窗口对应一个统计量 。最终生成一个统计量序列


2. 计算移动窗口的平均值：

```
xxxxxxxxxx  Series/DataFrame.rolling(window, min_periods=None, freq=None, center=False,   win_type=None, on=None, axis=0)
```

    * `window`：一个整数或者一个`offset`。如果是个整数，则给出了窗口的大小（窗口大小是固定的）。如果是个`offset`，则每个窗口对应一个时间段，因此窗口大小不固定。
    * `min_periods`：一个整数。给出了窗口内有效值的数量。
    * `freq`：一个字符串或者`DateOffset`对象，该参数被废弃。它用于对数据重采样，因为我们一般使用`resample()`来完成，所以该参数被废弃。
    * `center`：一个布尔值。如果为`True`，则聚合结果的`label`为窗口的中心点的索引。默认情况下，聚合结果的`label`为窗口的最右点的索引。（因为一个聚合结果对应了 `window`个数据，因此该聚合结果可选的索引可以从这些数据的索引中选取）
    * `win_type`：一个字符串，给出了窗口类型
    * `on`：一个字符串。对于`DataFrame`，它指定在哪一`column`上进行移动平均。否则是`index`
    * `axis`：一个整数。指定沿着0轴还是1轴移动平均。如果为`0/'index'`则沿着0轴；如果为`1/'columns'`则沿着0轴

窗口类型可以为：

    * `'boxcar'`
    * `'triang'`<br></br>
    * `'blackman'`
    * `'hamming'`<br></br>
    * `'bartlett'`<br></br>
    * `'parzen'`
    * `'bohman'`<br></br>
    * `'blackmanharris'`<br></br>
    * `'nuttall'`<br></br>
    * `'barthann'`<br></br>
    * `'kaiser'`（需要`beta`参数），该参数由后面的`.mean()`等方法给出
    * `'guassian'`（需要`std`参数），该参数由后面的`.mean()`等方法给出
    * `'general_gaussian'`（需要`power,width`参数），该参数由后面的`.mean()`等方法给出
    * `'slepian'`（需要`width`参数），该参数由后面的`.mean()`等方法给出

该方法返回一个`Window`对象，你可以在该对象上调用`.mean()/.sum()/.agg()/.aggregate()`等方法。

![rolling0](../imgs/rolling0.JPG) ![rolling1](../imgs/rolling1.JPG) ![rolling2](../imgs/rolling2.JPG)

3. 计算移动窗口的指数加权平均值：

```
xxxxxxxxxx  Series/DataFrame.ewm(com=None, span=None, halflife=None, alpha=None, min_periods=0,   freq=None, adjust=True, ignore_na=False, axis=0)
```

    * `com`：一个浮点数，以`center of mass`的方式给出了衰减因子。<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-18-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.395ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -956.9 9443.2 1461.5" width="21.933ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E18-MJMATHI-3B1" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E18-MJMAIN-3D" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E18-MJMAIN-31" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E18-MJMAIN-2B" stroke-width="0"></path><path d="M34 159Q34 268 120 355T306 442Q362 442 394 418T427 355Q427 326 408 306T360 285Q341 285 330 295T319 325T330 359T352 380T366 386H367Q367 388 361 392T340 400T306 404Q276 404 249 390Q228 381 206 359Q162 315 142 235T121 119Q121 73 147 50Q169 26 205 26H209Q321 26 394 111Q403 121 406 121Q410 121 419 112T429 98T420 83T391 55T346 25T282 0T202 -11Q127 -11 81 37T34 159Z" id="E18-MJMATHI-63" stroke-width="0"></path><path d="M201 -11Q126 -11 80 38T34 156Q34 221 64 279T146 380Q222 441 301 441Q333 441 341 440Q354 437 367 433T402 417T438 387T464 338T476 268Q476 161 390 75T201 -11ZM121 120Q121 70 147 48T206 26Q250 26 289 58T351 142Q360 163 374 216T388 308Q388 352 370 375Q346 405 306 405Q243 405 195 347Q158 303 140 230T121 120Z" id="E18-MJMATHI-6F" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E18-MJMATHI-6D" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E18-MJMAIN-2C" stroke-width="0"></path><path d="M69 609Q69 637 87 653T131 669Q154 667 171 652T188 609Q188 579 171 564T129 549Q104 549 87 564T69 609ZM247 0Q232 3 143 3Q132 3 106 3T56 1L34 0H26V46H42Q70 46 91 49Q100 53 102 60T104 102V205V293Q104 345 102 359T88 378Q74 385 41 385H30V408Q30 431 32 431L42 432Q52 433 70 434T106 436Q123 437 142 438T171 441T182 442H185V62Q190 52 197 50T232 46H255V0H247Z" id="E18-MJMAIN-69" stroke-width="0"></path><path d="M273 0Q255 3 146 3Q43 3 34 0H26V46H42Q70 46 91 49Q99 52 103 60Q104 62 104 224V385H33V431H104V497L105 564L107 574Q126 639 171 668T266 704Q267 704 275 704T289 705Q330 702 351 679T372 627Q372 604 358 590T321 576T284 590T270 627Q270 647 288 667H284Q280 668 273 668Q245 668 223 647T189 592Q183 572 182 497V431H293V385H185V225Q185 63 186 61T189 57T194 54T199 51T206 49T213 48T222 47T231 47T241 46T251 46H282V0H273Z" id="E18-MJMAIN-66" stroke-width="0"></path><path d="M83 616Q83 624 89 630T99 636Q107 636 253 568T543 431T687 361Q694 356 694 346T687 331Q685 329 395 192L107 56H101Q83 58 83 76Q83 77 83 79Q82 86 98 95Q117 105 248 167Q326 204 378 228L626 346L360 472Q291 505 200 548Q112 589 98 597T83 616ZM84 -118Q84 -108 99 -98H678Q694 -104 694 -118Q694 -130 679 -138H98Q84 -131 84 -118Z" id="E18-MJMAIN-2265" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E18-MJMAIN-30" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E18-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="917" xlink:href="#E18-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1695,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="2293" x="0" y="220"></rect><use transform="scale(0.707)" x="1371" xlink:href="#E18-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-376)"><use transform="scale(0.707)" x="0" xlink:href="#E18-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="500" xlink:href="#E18-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1278" xlink:href="#E18-MJMATHI-63" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1711" xlink:href="#E18-MJMATHI-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2196" xlink:href="#E18-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g><use x="4507" xlink:href="#E18-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(4951,0)"><use xlink:href="#E18-MJMAIN-69" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="278" xlink:href="#E18-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="5813" xlink:href="#E18-MJMATHI-63" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6246" xlink:href="#E18-MJMATHI-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6731" xlink:href="#E18-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7887" xlink:href="#E18-MJMAIN-2265" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8943" xlink:href="#E18-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-18" type="math/tex">\alpha=\frac{1}{1+com},\text{if} \; com \ge 0</script>
    * `span`：一个浮点数，以`span`的方式给出了衰减因子。<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-19-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.628ex" role="img" style="vertical-align: -1.405ex;" viewbox="0 -956.9 9963.9 1562" width="23.142ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E19-MJMATHI-3B1" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E19-MJMAIN-3D" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E19-MJMAIN-32" stroke-width="0"></path><path d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z" id="E19-MJMATHI-73" stroke-width="0"></path><path d="M23 287Q24 290 25 295T30 317T40 348T55 381T75 411T101 433T134 442Q209 442 230 378L240 387Q302 442 358 442Q423 442 460 395T497 281Q497 173 421 82T249 -10Q227 -10 210 -4Q199 1 187 11T168 28L161 36Q160 35 139 -51T118 -138Q118 -144 126 -145T163 -148H188Q194 -155 194 -157T191 -175Q188 -187 185 -190T172 -194Q170 -194 161 -194T127 -193T65 -192Q-5 -192 -24 -194H-32Q-39 -187 -39 -183Q-37 -156 -26 -148H-6Q28 -147 33 -136Q36 -130 94 103T155 350Q156 355 156 364Q156 405 131 405Q109 405 94 377T71 316T59 280Q57 278 43 278H29Q23 284 23 287ZM178 102Q200 26 252 26Q282 26 310 49T356 107Q374 141 392 215T411 325V331Q411 405 350 405Q339 405 328 402T306 393T286 380T269 365T254 350T243 336T235 326L232 322Q232 321 229 308T218 264T204 212Q178 106 178 102Z" id="E19-MJMATHI-70" stroke-width="0"></path><path d="M33 157Q33 258 109 349T280 441Q331 441 370 392Q386 422 416 422Q429 422 439 414T449 394Q449 381 412 234T374 68Q374 43 381 35T402 26Q411 27 422 35Q443 55 463 131Q469 151 473 152Q475 153 483 153H487Q506 153 506 144Q506 138 501 117T481 63T449 13Q436 0 417 -8Q409 -10 393 -10Q359 -10 336 5T306 36L300 51Q299 52 296 50Q294 48 292 46Q233 -10 172 -10Q117 -10 75 30T33 157ZM351 328Q351 334 346 350T323 385T277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q217 26 254 59T298 110Q300 114 325 217T351 328Z" id="E19-MJMATHI-61" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T89 425T135 442Q171 442 195 424T225 390T231 369Q231 367 232 367L243 378Q304 442 382 442Q436 442 469 415T503 336T465 179T427 52Q427 26 444 26Q450 26 453 27Q482 32 505 65T540 145Q542 153 560 153Q580 153 580 145Q580 144 576 130Q568 101 554 73T508 17T439 -10Q392 -10 371 17T350 73Q350 92 386 193T423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 180T152 343Q153 348 153 366Q153 405 129 405Q91 405 66 305Q60 285 60 284Q58 278 41 278H27Q21 284 21 287Z" id="E19-MJMATHI-6E" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E19-MJMAIN-2B" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E19-MJMAIN-31" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E19-MJMAIN-2C" stroke-width="0"></path><path d="M69 609Q69 637 87 653T131 669Q154 667 171 652T188 609Q188 579 171 564T129 549Q104 549 87 564T69 609ZM247 0Q232 3 143 3Q132 3 106 3T56 1L34 0H26V46H42Q70 46 91 49Q100 53 102 60T104 102V205V293Q104 345 102 359T88 378Q74 385 41 385H30V408Q30 431 32 431L42 432Q52 433 70 434T106 436Q123 437 142 438T171 441T182 442H185V62Q190 52 197 50T232 46H255V0H247Z" id="E19-MJMAIN-69" stroke-width="0"></path><path d="M273 0Q255 3 146 3Q43 3 34 0H26V46H42Q70 46 91 49Q99 52 103 60Q104 62 104 224V385H33V431H104V497L105 564L107 574Q126 639 171 668T266 704Q267 704 275 704T289 705Q330 702 351 679T372 627Q372 604 358 590T321 576T284 590T270 627Q270 647 288 667H284Q280 668 273 668Q245 668 223 647T189 592Q183 572 182 497V431H293V385H185V225Q185 63 186 61T189 57T194 54T199 51T206 49T213 48T222 47T231 47T241 46T251 46H282V0H273Z" id="E19-MJMAIN-66" stroke-width="0"></path><path d="M83 616Q83 624 89 630T99 636Q107 636 253 568T543 431T687 361Q694 356 694 346T687 331Q685 329 395 192L107 56H101Q83 58 83 76Q83 77 83 79Q82 86 98 95Q117 105 248 167Q326 204 378 228L626 346L360 472Q291 505 200 548Q112 589 98 597T83 616ZM84 -118Q84 -108 99 -98H678Q694 -104 694 -118Q694 -130 679 -138H98Q84 -131 84 -118Z" id="E19-MJMAIN-2265" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E19-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="917" xlink:href="#E19-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1695,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="2509" x="0" y="220"></rect><use transform="scale(0.707)" x="1524" xlink:href="#E19-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-376)"><use transform="scale(0.707)" x="0" xlink:href="#E19-MJMATHI-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="469" xlink:href="#E19-MJMATHI-70" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="972" xlink:href="#E19-MJMATHI-61" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1501" xlink:href="#E19-MJMATHI-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2101" xlink:href="#E19-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2878" xlink:href="#E19-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g><use x="4722" xlink:href="#E19-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5167,0)"><use xlink:href="#E19-MJMAIN-69" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="278" xlink:href="#E19-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="6029" xlink:href="#E19-MJMATHI-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6498" xlink:href="#E19-MJMATHI-70" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7001" xlink:href="#E19-MJMATHI-61" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7530" xlink:href="#E19-MJMATHI-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8408" xlink:href="#E19-MJMAIN-2265" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9463" xlink:href="#E19-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-19" type="math/tex">\alpha=\frac {2}{span+1},\text{if}\; span \ge 1</script>
    * `halflife`：一个浮点数，以`halflife`的方式给出了衰减因子：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-20-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="4.212ex" role="img" style="vertical-align: -1.405ex;" viewbox="0 -1208.2 15668.1 1813.3" width="36.39ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E20-MJMATHI-3B1" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E20-MJMAIN-3D" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E20-MJMAIN-31" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E20-MJMAIN-2212" stroke-width="0"></path><path d="M28 218Q28 273 48 318T98 391T163 433T229 448Q282 448 320 430T378 380T406 316T415 245Q415 238 408 231H126V216Q126 68 226 36Q246 30 270 30Q312 30 342 62Q359 79 369 104L379 128Q382 131 395 131H398Q415 131 415 121Q415 117 412 108Q393 53 349 21T250 -11Q155 -11 92 58T28 218ZM333 275Q322 403 238 411H236Q228 411 220 410T195 402T166 381T143 340T127 274V267H333V275Z" id="E20-MJMAIN-65" stroke-width="0"></path><path d="M201 0Q189 3 102 3Q26 3 17 0H11V46H25Q48 47 67 52T96 61T121 78T139 96T160 122T180 150L226 210L168 288Q159 301 149 315T133 336T122 351T113 363T107 370T100 376T94 379T88 381T80 383Q74 383 44 385H16V431H23Q59 429 126 429Q219 429 229 431H237V385Q201 381 201 369Q201 367 211 353T239 315T268 274L272 270L297 304Q329 345 329 358Q329 364 327 369T322 376T317 380T310 384L307 385H302V431H309Q324 428 408 428Q487 428 493 431H499V385H492Q443 385 411 368Q394 360 377 341T312 257L296 236L358 151Q424 61 429 57T446 50Q464 46 499 46H516V0H510H502Q494 1 482 1T457 2T432 2T414 3Q403 3 377 3T327 1L304 0H295V46H298Q309 46 320 51T331 63Q331 65 291 120L250 175Q249 174 219 133T185 88Q181 83 181 74Q181 63 188 55T206 46Q208 46 208 23V0H201Z" id="E20-MJMAIN-78" stroke-width="0"></path><path d="M36 -148H50Q89 -148 97 -134V-126Q97 -119 97 -107T97 -77T98 -38T98 6T98 55T98 106Q98 140 98 177T98 243T98 296T97 335T97 351Q94 370 83 376T38 385H20V408Q20 431 22 431L32 432Q42 433 61 434T98 436Q115 437 135 438T165 441T176 442H179V416L180 390L188 397Q247 441 326 441Q407 441 464 377T522 216Q522 115 457 52T310 -11Q242 -11 190 33L182 40V-45V-101Q182 -128 184 -134T195 -145Q216 -148 244 -148H260V-194H252L228 -193Q205 -192 178 -192T140 -191Q37 -191 28 -194H20V-148H36ZM424 218Q424 292 390 347T305 402Q234 402 182 337V98Q222 26 294 26Q345 26 384 80T424 218Z" id="E20-MJMAIN-70" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E20-MJMAIN-28" stroke-width="0"></path><path d="M42 46H56Q95 46 103 60V68Q103 77 103 91T103 124T104 167T104 217T104 272T104 329Q104 366 104 407T104 482T104 542T103 586T103 603Q100 622 89 628T44 637H26V660Q26 683 28 683L38 684Q48 685 67 686T104 688Q121 689 141 690T171 693T182 694H185V379Q185 62 186 60Q190 52 198 49Q219 46 247 46H263V0H255L232 1Q209 2 183 2T145 3T107 3T57 1L34 0H26V46H42Z" id="E20-MJMAIN-6C" stroke-width="0"></path><path d="M28 214Q28 309 93 378T250 448Q340 448 405 380T471 215Q471 120 407 55T250 -10Q153 -10 91 57T28 214ZM250 30Q372 30 372 193V225V250Q372 272 371 288T364 326T348 362T317 390T268 410Q263 411 252 411Q222 411 195 399Q152 377 139 338T126 246V226Q126 130 145 91Q177 30 250 30Z" id="E20-MJMAIN-6F" stroke-width="0"></path><path d="M329 409Q373 453 429 453Q459 453 472 434T485 396Q485 382 476 371T449 360Q416 360 412 390Q410 404 415 411Q415 412 416 414V415Q388 412 363 393Q355 388 355 386Q355 385 359 381T368 369T379 351T388 325T392 292Q392 230 343 187T222 143Q172 143 123 171Q112 153 112 133Q112 98 138 81Q147 75 155 75T227 73Q311 72 335 67Q396 58 431 26Q470 -13 470 -72Q470 -139 392 -175Q332 -206 250 -206Q167 -206 107 -175Q29 -140 29 -75Q29 -39 50 -15T92 18L103 24Q67 55 67 108Q67 155 96 193Q52 237 52 292Q52 355 102 398T223 442Q274 442 318 416L329 409ZM299 343Q294 371 273 387T221 404Q192 404 171 388T145 343Q142 326 142 292Q142 248 149 227T179 192Q196 182 222 182Q244 182 260 189T283 207T294 227T299 242Q302 258 302 292T299 343ZM403 -75Q403 -50 389 -34T348 -11T299 -2T245 0H218Q151 0 138 -6Q118 -15 107 -34T95 -74Q95 -84 101 -97T122 -127T170 -155T250 -167Q319 -167 361 -139T403 -75Z" id="E20-MJMAIN-67" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E20-MJMAIN-30" stroke-width="0"></path><path d="M78 60Q78 84 95 102T138 120Q162 120 180 104T199 61Q199 36 182 18T139 0T96 17T78 60Z" id="E20-MJMAIN-2E" stroke-width="0"></path><path d="M164 157Q164 133 148 117T109 101H102Q148 22 224 22Q294 22 326 82Q345 115 345 210Q345 313 318 349Q292 382 260 382H254Q176 382 136 314Q132 307 129 306T114 304Q97 304 95 310Q93 314 93 485V614Q93 664 98 664Q100 666 102 666Q103 666 123 658T178 642T253 634Q324 634 389 662Q397 666 402 666Q410 666 410 648V635Q328 538 205 538Q174 538 149 544L139 546V374Q158 388 169 396T205 412T256 420Q337 420 393 355T449 201Q449 109 385 44T229 -22Q148 -22 99 32T50 154Q50 178 61 192T84 210T107 214Q132 214 148 197T164 157Z" id="E20-MJMAIN-35" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E20-MJMAIN-29" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E20-MJMATHI-68" stroke-width="0"></path><path d="M33 157Q33 258 109 349T280 441Q331 441 370 392Q386 422 416 422Q429 422 439 414T449 394Q449 381 412 234T374 68Q374 43 381 35T402 26Q411 27 422 35Q443 55 463 131Q469 151 473 152Q475 153 483 153H487Q506 153 506 144Q506 138 501 117T481 63T449 13Q436 0 417 -8Q409 -10 393 -10Q359 -10 336 5T306 36L300 51Q299 52 296 50Q294 48 292 46Q233 -10 172 -10Q117 -10 75 30T33 157ZM351 328Q351 334 346 350T323 385T277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q217 26 254 59T298 110Q300 114 325 217T351 328Z" id="E20-MJMATHI-61" stroke-width="0"></path><path d="M117 59Q117 26 142 26Q179 26 205 131Q211 151 215 152Q217 153 225 153H229Q238 153 241 153T246 151T248 144Q247 138 245 128T234 90T214 43T183 6T137 -11Q101 -11 70 11T38 85Q38 97 39 102L104 360Q167 615 167 623Q167 626 166 628T162 632T157 634T149 635T141 636T132 637T122 637Q112 637 109 637T101 638T95 641T94 647Q94 649 96 661Q101 680 107 682T179 688Q194 689 213 690T243 693T254 694Q266 694 266 686Q266 675 193 386T118 83Q118 81 118 75T117 65V59Z" id="E20-MJMATHI-6C" stroke-width="0"></path><path d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z" id="E20-MJMATHI-66" stroke-width="0"></path><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E20-MJMATHI-69" stroke-width="0"></path><path d="M39 168Q39 225 58 272T107 350T174 402T244 433T307 442H310Q355 442 388 420T421 355Q421 265 310 237Q261 224 176 223Q139 223 138 221Q138 219 132 186T125 128Q125 81 146 54T209 26T302 45T394 111Q403 121 406 121Q410 121 419 112T429 98T420 82T390 55T344 24T281 -1T205 -11Q126 -11 83 42T39 168ZM373 353Q367 405 305 405Q272 405 244 391T199 357T170 316T154 280T149 261Q149 260 169 260Q282 260 327 284T373 353Z" id="E20-MJMATHI-65" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E20-MJMAIN-2C" stroke-width="0"></path><path d="M69 609Q69 637 87 653T131 669Q154 667 171 652T188 609Q188 579 171 564T129 549Q104 549 87 564T69 609ZM247 0Q232 3 143 3Q132 3 106 3T56 1L34 0H26V46H42Q70 46 91 49Q100 53 102 60T104 102V205V293Q104 345 102 359T88 378Q74 385 41 385H30V408Q30 431 32 431L42 432Q52 433 70 434T106 436Q123 437 142 438T171 441T182 442H185V62Q190 52 197 50T232 46H255V0H247Z" id="E20-MJMAIN-69" stroke-width="0"></path><path d="M273 0Q255 3 146 3Q43 3 34 0H26V46H42Q70 46 91 49Q99 52 103 60Q104 62 104 224V385H33V431H104V497L105 564L107 574Q126 639 171 668T266 704Q267 704 275 704T289 705Q330 702 351 679T372 627Q372 604 358 590T321 576T284 590T270 627Q270 647 288 667H284Q280 668 273 668Q245 668 223 647T189 592Q183 572 182 497V431H293V385H185V225Q185 63 186 61T189 57T194 54T199 51T206 49T213 48T222 47T231 47T241 46T251 46H282V0H273Z" id="E20-MJMAIN-66" stroke-width="0"></path><path d="M84 520Q84 528 88 533T96 539L99 540Q106 540 253 471T544 334L687 265Q694 260 694 250T687 235Q685 233 395 96L107 -40H101Q83 -38 83 -20Q83 -19 83 -17Q82 -10 98 -1Q117 9 248 71Q326 108 378 132L626 250L378 368Q90 504 86 509Q84 513 84 520Z" id="E20-MJMAIN-3E" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E20-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="917" xlink:href="#E20-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1973" xlink:href="#E20-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2695" xlink:href="#E20-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(3696,0)"><use xlink:href="#E20-MJMAIN-65" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="444" xlink:href="#E20-MJMAIN-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="972" xlink:href="#E20-MJMAIN-70" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="5224" xlink:href="#E20-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5613,0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="2674" x="0" y="220"></rect><g transform="translate(158,581)"><use transform="scale(0.707)" xlink:href="#E20-MJMAIN-6C" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use transform="scale(0.707)" x="278" xlink:href="#E20-MJMAIN-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="778" xlink:href="#E20-MJMAIN-67" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1278" xlink:href="#E20-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1178,0)"><use transform="scale(0.707)" xlink:href="#E20-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use transform="scale(0.707)" x="500" xlink:href="#E20-MJMAIN-2E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="778" xlink:href="#E20-MJMAIN-35" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use transform="scale(0.707)" x="2945" xlink:href="#E20-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(60,-403)"><use transform="scale(0.707)" x="0" xlink:href="#E20-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="576" xlink:href="#E20-MJMATHI-61" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1105" xlink:href="#E20-MJMATHI-6C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1403" xlink:href="#E20-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1953" xlink:href="#E20-MJMATHI-6C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2251" xlink:href="#E20-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2596" xlink:href="#E20-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="3146" xlink:href="#E20-MJMATHI-65" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g><use x="8527" xlink:href="#E20-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8916" xlink:href="#E20-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(9360,0)"><use xlink:href="#E20-MJMAIN-69" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="278" xlink:href="#E20-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="10222" xlink:href="#E20-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10798" xlink:href="#E20-MJMATHI-61" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11327" xlink:href="#E20-MJMATHI-6C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11625" xlink:href="#E20-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="12175" xlink:href="#E20-MJMATHI-6C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="12473" xlink:href="#E20-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="12818" xlink:href="#E20-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="13368" xlink:href="#E20-MJMATHI-65" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="14112" xlink:href="#E20-MJMAIN-3E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="15168" xlink:href="#E20-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-20" type="math/tex">\alpha=1-\exp(\frac{\log(0.5)}{halflife}),\text{if}\; halflife \gt 0</script>
    * `alpha`：一个浮点数，为光滑因子。这种方式直接给出了<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-25-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.41ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -504.6 640 607.1" width="1.486ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E25-MJMATHI-3B1" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E25-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-25" type="math/tex">\alpha</script>，要求<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-22-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.227ex" role="img" style="vertical-align: -0.472ex;" viewbox="0 -755.9 4307.1 958.9" width="10.004ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E22-MJMAIN-30" stroke-width="0"></path><path d="M694 -11T694 -19T688 -33T678 -40Q671 -40 524 29T234 166L90 235Q83 240 83 250Q83 261 91 266Q664 540 678 540Q681 540 687 534T694 519T687 505Q686 504 417 376L151 250L417 124Q686 -4 687 -5Q694 -11 694 -19Z" id="E22-MJMAIN-3C" stroke-width="0"></path><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E22-MJMATHI-3B1" stroke-width="0"></path><path d="M674 636Q682 636 688 630T694 615T687 601Q686 600 417 472L151 346L399 228Q687 92 691 87Q694 81 694 76Q694 58 676 56H670L382 192Q92 329 90 331Q83 336 83 348Q84 359 96 365Q104 369 382 500T665 634Q669 636 674 636ZM84 -118Q84 -108 99 -98H678Q694 -104 694 -118Q694 -130 679 -138H98Q84 -131 84 -118Z" id="E22-MJMAIN-2264" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E22-MJMAIN-31" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E22-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="777" xlink:href="#E22-MJMAIN-3C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1833" xlink:href="#E22-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2751" xlink:href="#E22-MJMAIN-2264" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3807" xlink:href="#E22-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-22" type="math/tex">0 \lt \alpha \le 1</script>
    * `min_periods`:一个整数。给出了窗口内有效值的数量。
    * `adjust`：一个布尔值。见下面的解释。
    * `ignore_na`：一个布尔值，如果为`True`，则计算权重时，忽略缺失值。

加权移动平均的计算公式为：
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display" style="text-align: center;"><span class="MathJax_SVG" id="MathJax-Element-2-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="7.013ex" role="img" style="vertical-align: -2.923ex;" viewbox="0 -1761.1 7790.4 3019.6" width="18.094ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M21 287Q21 301 36 335T84 406T158 442Q199 442 224 419T250 355Q248 336 247 334Q247 331 231 288T198 191T182 105Q182 62 196 45T238 27Q261 27 281 38T312 61T339 94Q339 95 344 114T358 173T377 247Q415 397 419 404Q432 431 462 431Q475 431 483 424T494 412T496 403Q496 390 447 193T391 -23Q363 -106 294 -155T156 -205Q111 -205 77 -183T43 -117Q43 -95 50 -80T69 -58T89 -48T106 -45Q150 -45 150 -87Q150 -107 138 -122T115 -142T102 -147L99 -148Q101 -153 118 -160T152 -167H160Q177 -167 186 -165Q219 -156 247 -127T290 -65T313 -9T321 21L315 17Q309 13 296 6T270 -6Q250 -11 231 -11Q185 -11 150 11T104 82Q103 89 103 113Q103 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E2-MJMATHI-79" stroke-width="0"></path><path d="M26 385Q19 392 19 395Q19 399 22 411T27 425Q29 430 36 430T87 431H140L159 511Q162 522 166 540T173 566T179 586T187 603T197 615T211 624T229 626Q247 625 254 615T261 596Q261 589 252 549T232 470L222 433Q222 431 272 431H323Q330 424 330 420Q330 398 317 385H210L174 240Q135 80 135 68Q135 26 162 26Q197 26 230 60T283 144Q285 150 288 151T303 153H307Q322 153 322 145Q322 142 319 133Q314 117 301 95T267 48T216 6T155 -11Q125 -11 98 4T59 56Q57 64 57 83V101L92 241Q127 382 128 383Q128 385 77 385H26Z" id="E2-MJMATHI-74" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E2-MJMAIN-3D" stroke-width="0"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E2-MJSZ1-2211" stroke-width="0"></path><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E2-MJMATHI-69" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E2-MJMAIN-30" stroke-width="0"></path><path d="M580 385Q580 406 599 424T641 443Q659 443 674 425T690 368Q690 339 671 253Q656 197 644 161T609 80T554 12T482 -11Q438 -11 404 5T355 48Q354 47 352 44Q311 -11 252 -11Q226 -11 202 -5T155 14T118 53T104 116Q104 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Q21 293 29 315T52 366T96 418T161 441Q204 441 227 416T250 358Q250 340 217 250T184 111Q184 65 205 46T258 26Q301 26 334 87L339 96V119Q339 122 339 128T340 136T341 143T342 152T345 165T348 182T354 206T362 238T373 281Q402 395 406 404Q419 431 449 431Q468 431 475 421T483 402Q483 389 454 274T422 142Q420 131 420 107V100Q420 85 423 71T442 42T487 26Q558 26 600 148Q609 171 620 213T632 273Q632 306 619 325T593 357T580 385Z" id="E2-MJMATHI-77" stroke-width="0"></path><path d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z" id="E2-MJMATHI-78" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E2-MJMAIN-2212" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E2-MJMATHI-79" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="692" xlink:href="#E2-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1123" xlink:href="#E2-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1901,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="5371" x="0" y="220"></rect><g transform="translate(60,766)"><use x="0" xlink:href="#E2-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1493" xlink:href="#E2-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="674"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E2-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="345" xlink:href="#E2-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1123" xlink:href="#E2-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(2470,0)"><use x="0" xlink:href="#E2-MJMATHI-77" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1012" xlink:href="#E2-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><g transform="translate(3530,0)"><use x="0" xlink:href="#E2-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(572,-150)"><use transform="scale(0.707)" x="0" xlink:href="#E2-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="361" xlink:href="#E2-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1139" xlink:href="#E2-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g><g transform="translate(920,-886)"><use x="0" xlink:href="#E2-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1493" xlink:href="#E2-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="674"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E2-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="345" xlink:href="#E2-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1123" xlink:href="#E2-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(2470,0)"><use x="0" xlink:href="#E2-MJMATHI-77" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1012" xlink:href="#E2-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></g></g></g></g></svg></span></span><script id="MathJax-Element-2" type="math/tex; mode=display">y_t = \frac{\sum_{i=0}^{t} w_i x_{t-i}}{\sum_{i=0}^t w_i}</script>
其中<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-23-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.76ex" role="img" style="vertical-align: -0.588ex;" viewbox="0 -504.6 927.3 757.9" width="2.154ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z" id="E23-MJMATHI-78" stroke-width="0"></path><path d="M26 385Q19 392 19 395Q19 399 22 411T27 425Q29 430 36 430T87 431H140L159 511Q162 522 166 540T173 566T179 586T187 603T197 615T211 624T229 626Q247 625 254 615T261 596Q261 589 252 549T232 470L222 433Q222 431 272 431H323Q330 424 330 420Q330 398 317 385H210L174 240Q135 80 135 68Q135 26 162 26Q197 26 230 60T283 144Q285 150 288 151T303 153H307Q322 153 322 145Q322 142 319 133Q314 117 301 95T267 48T216 6T155 -11Q125 -11 98 4T59 56Q57 64 57 83V101L92 241Q127 382 128 383Q128 385 77 385H26Z" id="E23-MJMATHI-74" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E23-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E23-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></svg></span><script id="MathJax-Element-23" type="math/tex">x_t</script>为输入值。

    * 当`adjust=True`时，<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-24-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.811ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -906.7 5877.9 1210.2" width="13.652ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M580 385Q580 406 599 424T641 443Q659 443 674 425T690 368Q690 339 671 253Q656 197 644 161T609 80T554 12T482 -11Q438 -11 404 5T355 48Q354 47 352 44Q311 -11 252 -11Q226 -11 202 -5T155 14T118 53T104 116Q104 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Q21 293 29 315T52 366T96 418T161 441Q204 441 227 416T250 358Q250 340 217 250T184 111Q184 65 205 46T258 26Q301 26 334 87L339 96V119Q339 122 339 128T340 136T341 143T342 152T345 165T348 182T354 206T362 238T373 281Q402 395 406 404Q419 431 449 431Q468 431 475 421T483 402Q483 389 454 274T422 142Q420 131 420 107V100Q420 85 423 71T442 42T487 26Q558 26 600 148Q609 171 620 213T632 273Q632 306 619 325T593 357T580 385Z" id="E24-MJMATHI-77" stroke-width="0"></path><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E24-MJMATHI-69" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E24-MJMAIN-3D" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E24-MJMAIN-28" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E24-MJMAIN-31" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E24-MJMAIN-2212" stroke-width="0"></path><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E24-MJMATHI-3B1" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E24-MJMAIN-29" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E24-MJMATHI-77" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1012" xlink:href="#E24-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1337" xlink:href="#E24-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2393" xlink:href="#E24-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2782" xlink:href="#E24-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3504" xlink:href="#E24-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4504" xlink:href="#E24-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5144,0)"><use x="0" xlink:href="#E24-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E24-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g></g></svg></span><script id="MathJax-Element-24" type="math/tex">w_i=(1-\alpha)^{i}</script>，此时：
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display"><span class="MathJax_SVG" id="MathJax-Element-3-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="13.083ex" role="img" style="vertical-align: -9.343ex;" viewbox="0 -1610.3 38699.6 5633" width="89.883ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M21 287Q21 301 36 335T84 406T158 442Q199 442 224 419T250 355Q248 336 247 334Q247 331 231 288T198 191T182 105Q182 62 196 45T238 27Q261 27 281 38T312 61T339 94Q339 95 344 114T358 173T377 247Q415 397 419 404Q432 431 462 431Q475 431 483 424T494 412T496 403Q496 390 447 193T391 -23Q363 -106 294 -155T156 -205Q111 -205 77 -183T43 -117Q43 -95 50 -80T69 -58T89 -48T106 -45Q150 -45 150 -87Q150 -107 138 -122T115 -142T102 -147L99 -148Q101 -153 118 -160T152 -167H160Q177 -167 186 -165Q219 -156 247 -127T290 -65T313 -9T321 21L315 17Q309 13 296 6T270 -6Q250 -11 231 -11Q185 -11 150 11T104 82Q103 89 103 113Q103 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E3-MJMATHI-79" stroke-width="0"></path><path d="M26 385Q19 392 19 395Q19 399 22 411T27 425Q29 430 36 430T87 431H140L159 511Q162 522 166 540T173 566T179 586T187 603T197 615T211 624T229 626Q247 625 254 615T261 596Q261 589 252 549T232 470L222 433Q222 431 272 431H323Q330 424 330 420Q330 398 317 385H210L174 240Q135 80 135 68Q135 26 162 26Q197 26 230 60T283 144Q285 150 288 151T303 153H307Q322 153 322 145Q322 142 319 133Q314 117 301 95T267 48T216 6T155 -11Q125 -11 98 4T59 56Q57 64 57 83V101L92 241Q127 382 128 383Q128 385 77 385H26Z" id="E3-MJMATHI-74" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E3-MJMAIN-3D" stroke-width="0"></path><path d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z" id="E3-MJMATHI-78" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E3-MJMAIN-2B" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E3-MJMAIN-28" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E3-MJMAIN-31" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E3-MJMAIN-2212" stroke-width="0"></path><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E3-MJMATHI-3B1" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E3-MJMAIN-29" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E3-MJMAIN-32" stroke-width="0"></path><path d="M78 250Q78 274 95 292T138 310Q162 310 180 294T199 251Q199 226 182 208T139 190T96 207T78 250ZM525 250Q525 274 542 292T585 310Q609 310 627 294T646 251Q646 226 629 208T586 190T543 207T525 250ZM972 250Q972 274 989 292T1032 310Q1056 310 1074 294T1093 251Q1093 226 1076 208T1033 190T990 207T972 250Z" id="E3-MJMAIN-22EF" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E3-MJMAIN-30" stroke-width="0"></path><path d="M78 60Q78 84 95 102T138 120Q162 120 180 104T199 61Q199 36 182 18T139 0T96 17T78 60Z" id="E3-MJMAIN-2E" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(7127,0)"><use x="0" xlink:href="#E3-MJMATHI-79" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="692" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1123" xlink:href="#E3-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1901,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="22026" x="0" y="220"></rect><g transform="translate(60,715)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1149" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2149" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2538" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3260" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4261" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4901" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5290,0)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(572,-150)"><use transform="scale(0.707)" x="0" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="361" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1139" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="7343" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8343" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8732" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9454" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10454" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(11094,0)"><use x="0" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E3-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><g transform="translate(11937,0)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(572,-150)"><use transform="scale(0.707)" x="0" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="361" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1139" xlink:href="#E3-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="13990" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="14990" xlink:href="#E3-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="16385" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="17385" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="17774" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="18496" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="19496" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(20136,0)"><use x="0" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><g transform="translate(20881,0)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E3-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></g><g transform="translate(2980,-726)"><use x="0" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="722" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1722" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2111" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2833" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3833" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4473" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5085" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6085" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6474" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7196" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8196" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(8836,0)"><use x="0" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E3-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="408"></use></g><use x="9679" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10457" xlink:href="#E3-MJMAIN-2E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10901" xlink:href="#E3-MJMAIN-2E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11346" xlink:href="#E3-MJMAIN-2E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11791" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="12569" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="12958" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="13680" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="14680" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(15320,0)"><use x="0" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="408"></use></g></g></g></g></g><g transform="translate(7368,-2956)"><use x="0" xlink:href="#E3-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(778,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="22026" x="0" y="220"></rect><g transform="translate(60,715)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1149" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2149" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2538" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3260" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4261" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4901" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5290,0)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(572,-150)"><use transform="scale(0.707)" x="0" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="361" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1139" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="7343" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8343" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8732" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9454" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10454" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(11094,0)"><use x="0" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E3-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><g transform="translate(11937,0)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(572,-150)"><use transform="scale(0.707)" x="0" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="361" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1139" xlink:href="#E3-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="13990" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="14990" xlink:href="#E3-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="16385" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="17385" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="17774" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="18496" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="19496" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(20136,0)"><use x="0" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><g transform="translate(20881,0)"><use x="0" xlink:href="#E3-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E3-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></g><g transform="translate(7952,-726)"><use x="0" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="722" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1722" xlink:href="#E3-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2111" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2833" xlink:href="#E3-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3833" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(4473,0)"><use x="0" xlink:href="#E3-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(389,288)"><use transform="scale(0.707)" x="0" xlink:href="#E3-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="361" xlink:href="#E3-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1139" xlink:href="#E3-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></g></g><use x="23322" xlink:href="#E3-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></svg></span></span><script id="MathJax-Element-3" type="math/tex; mode=display">y_t = \frac{x_t + (1 - \alpha)x_{t-1} + (1 - \alpha)^{2} x_{t-2} + \cdots + (1 - \alpha)^{t} x_{0}}{1 + (1 - \alpha) + (1 - \alpha)^{2} + ... + (1 - \alpha)^{t}}\\ =\frac{x_t + (1 - \alpha)x_{t-1} + (1 - \alpha)^{2} x_{t-2} + \cdots + (1 - \alpha)^{t} x_{0}}{1-(1-\alpha)^{t+1}}\alpha</script>
    * 当`adjust=False`时
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display"><span class="MathJax_SVG" id="MathJax-Element-4-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="5.145ex" role="img" style="vertical-align: -3.974ex;" viewbox="0 -504.6 38699.6 2215.4" width="89.883ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M21 287Q21 301 36 335T84 406T158 442Q199 442 224 419T250 355Q248 336 247 334Q247 331 231 288T198 191T182 105Q182 62 196 45T238 27Q261 27 281 38T312 61T339 94Q339 95 344 114T358 173T377 247Q415 397 419 404Q432 431 462 431Q475 431 483 424T494 412T496 403Q496 390 447 193T391 -23Q363 -106 294 -155T156 -205Q111 -205 77 -183T43 -117Q43 -95 50 -80T69 -58T89 -48T106 -45Q150 -45 150 -87Q150 -107 138 -122T115 -142T102 -147L99 -148Q101 -153 118 -160T152 -167H160Q177 -167 186 -165Q219 -156 247 -127T290 -65T313 -9T321 21L315 17Q309 13 296 6T270 -6Q250 -11 231 -11Q185 -11 150 11T104 82Q103 89 103 113Q103 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E4-MJMATHI-79" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E4-MJMAIN-30" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E4-MJMAIN-3D" stroke-width="0"></path><path d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z" id="E4-MJMATHI-78" stroke-width="0"></path><path d="M26 385Q19 392 19 395Q19 399 22 411T27 425Q29 430 36 430T87 431H140L159 511Q162 522 166 540T173 566T179 586T187 603T197 615T211 624T229 626Q247 625 254 615T261 596Q261 589 252 549T232 470L222 433Q222 431 272 431H323Q330 424 330 420Q330 398 317 385H210L174 240Q135 80 135 68Q135 26 162 26Q197 26 230 60T283 144Q285 150 288 151T303 153H307Q322 153 322 145Q322 142 319 133Q314 117 301 95T267 48T216 6T155 -11Q125 -11 98 4T59 56Q57 64 57 83V101L92 241Q127 382 128 383Q128 385 77 385H26Z" id="E4-MJMATHI-74" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E4-MJMAIN-28" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E4-MJMAIN-31" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E4-MJMAIN-2212" stroke-width="0"></path><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E4-MJMATHI-3B1" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E4-MJMAIN-29" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E4-MJMAIN-2B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(17698,0)"><use x="0" xlink:href="#E4-MJMATHI-79" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="692" xlink:href="#E4-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1221" xlink:href="#E4-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2277,0)"><use x="0" xlink:href="#E4-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E4-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></g><g transform="translate(14420,-1386)"><use x="0" xlink:href="#E4-MJMATHI-79" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="692" xlink:href="#E4-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1123" xlink:href="#E4-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2178" xlink:href="#E4-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2567" xlink:href="#E4-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3290" xlink:href="#E4-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4290" xlink:href="#E4-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4930" xlink:href="#E4-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5319,0)"><use x="0" xlink:href="#E4-MJMATHI-79" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(490,-150)"><use transform="scale(0.707)" x="0" xlink:href="#E4-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="361" xlink:href="#E4-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1139" xlink:href="#E4-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="7290" xlink:href="#E4-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8290" xlink:href="#E4-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(8930,0)"><use x="0" xlink:href="#E4-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E4-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></g></g></svg></span></span><script id="MathJax-Element-4" type="math/tex; mode=display">y_0= x_0 \\ y_t = (1 - \alpha) y_{t-1} + \alpha x_t</script>
它等价于
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display" style="text-align: center;"><span class="MathJax_SVG" id="MathJax-Element-5-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="5.846ex" role="img" style="vertical-align: -2.339ex;" viewbox="0 -1509.8 11460.5 2517" width="26.618ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M580 385Q580 406 599 424T641 443Q659 443 674 425T690 368Q690 339 671 253Q656 197 644 161T609 80T554 12T482 -11Q438 -11 404 5T355 48Q354 47 352 44Q311 -11 252 -11Q226 -11 202 -5T155 14T118 53T104 116Q104 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Q21 293 29 315T52 366T96 418T161 441Q204 441 227 416T250 358Q250 340 217 250T184 111Q184 65 205 46T258 26Q301 26 334 87L339 96V119Q339 122 339 128T340 136T341 143T342 152T345 165T348 182T354 206T362 238T373 281Q402 395 406 404Q419 431 449 431Q468 431 475 421T483 402Q483 389 454 274T422 142Q420 131 420 107V100Q420 85 423 71T442 42T487 26Q558 26 600 148Q609 171 620 213T632 273Q632 306 619 325T593 357T580 385Z" id="E5-MJMATHI-77" stroke-width="0"></path><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E5-MJMATHI-69" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E5-MJMAIN-3D" stroke-width="0"></path><path d="M434 -231Q434 -244 428 -250H410Q281 -250 230 -184Q225 -177 222 -172T217 -161T213 -148T211 -133T210 -111T209 -84T209 -47T209 0Q209 21 209 53Q208 142 204 153Q203 154 203 155Q189 191 153 211T82 231Q71 231 68 234T65 250T68 266T82 269Q116 269 152 289T203 345Q208 356 208 377T209 529V579Q209 634 215 656T244 698Q270 724 324 740Q361 748 377 749Q379 749 390 749T408 750H428Q434 744 434 732Q434 719 431 716Q429 713 415 713Q362 710 332 689T296 647Q291 634 291 499V417Q291 370 288 353T271 314Q240 271 184 255L170 250L184 245Q202 239 220 230T262 196T290 137Q291 131 291 1Q291 -134 296 -147Q306 -174 339 -192T415 -213Q429 -213 431 -216Q434 -219 434 -231Z" id="E5-MJMAIN-7B" stroke-width="0"></path><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E5-MJMATHI-3B1" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E5-MJMAIN-28" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E5-MJMAIN-31" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E5-MJMAIN-2212" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E5-MJMAIN-29" stroke-width="0"></path><path d="M69 609Q69 637 87 653T131 669Q154 667 171 652T188 609Q188 579 171 564T129 549Q104 549 87 564T69 609ZM247 0Q232 3 143 3Q132 3 106 3T56 1L34 0H26V46H42Q70 46 91 49Q100 53 102 60T104 102V205V293Q104 345 102 359T88 378Q74 385 41 385H30V408Q30 431 32 431L42 432Q52 433 70 434T106 436Q123 437 142 438T171 441T182 442H185V62Q190 52 197 50T232 46H255V0H247Z" id="E5-MJMAIN-69" stroke-width="0"></path><path d="M273 0Q255 3 146 3Q43 3 34 0H26V46H42Q70 46 91 49Q99 52 103 60Q104 62 104 224V385H33V431H104V497L105 564L107 574Q126 639 171 668T266 704Q267 704 275 704T289 705Q330 702 351 679T372 627Q372 604 358 590T321 576T284 590T270 627Q270 647 288 667H284Q280 668 273 668Q245 668 223 647T189 592Q183 572 182 497V431H293V385H185V225Q185 63 186 61T189 57T194 54T199 51T206 49T213 48T222 47T231 47T241 46T251 46H282V0H273Z" id="E5-MJMAIN-66" stroke-width="0"></path><path d="M694 -11T694 -19T688 -33T678 -40Q671 -40 524 29T234 166L90 235Q83 240 83 250Q83 261 91 266Q664 540 678 540Q681 540 687 534T694 519T687 505Q686 504 417 376L151 250L417 124Q686 -4 687 -5Q694 -11 694 -19Z" id="E5-MJMAIN-3C" stroke-width="0"></path><path d="M26 385Q19 392 19 395Q19 399 22 411T27 425Q29 430 36 430T87 431H140L159 511Q162 522 166 540T173 566T179 586T187 603T197 615T211 624T229 626Q247 625 254 615T261 596Q261 589 252 549T232 470L222 433Q222 431 272 431H323Q330 424 330 420Q330 398 317 385H210L174 240Q135 80 135 68Q135 26 162 26Q197 26 230 60T283 144Q285 150 288 151T303 153H307Q322 153 322 145Q322 142 319 133Q314 117 301 95T267 48T216 6T155 -11Q125 -11 98 4T59 56Q57 64 57 83V101L92 241Q127 382 128 383Q128 385 77 385H26Z" id="E5-MJMATHI-74" stroke-width="0"></path><path d="M618 -943L612 -949H582L568 -943Q472 -903 411 -841T332 -703Q327 -682 327 -653T325 -350Q324 -28 323 -18Q317 24 301 61T264 124T221 171T179 205T147 225T132 234Q130 238 130 250Q130 255 130 258T131 264T132 267T134 269T139 272T144 275Q207 308 256 367Q310 436 323 519Q324 529 325 851Q326 1124 326 1154T332 1205Q369 1358 566 1443L582 1450H612L618 1444V1429Q618 1413 616 1411L608 1406Q599 1402 585 1393T552 1372T515 1343T479 1305T449 1257T429 1200Q425 1180 425 1152T423 851Q422 579 422 549T416 498Q407 459 388 424T346 364T297 318T250 284T214 264T197 254L188 251L205 242Q290 200 345 138T416 3Q421 -18 421 -48T423 -349Q423 -397 423 -472Q424 -677 428 -694Q429 -697 429 -699Q434 -722 443 -743T465 -782T491 -816T519 -845T548 -868T574 -886T595 -899T610 -908L616 -910Q618 -912 618 -928V-943Z" id="E5-MJSZ3-7B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E5-MJMATHI-77" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1012" xlink:href="#E5-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1337" xlink:href="#E5-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2393,0)"><use xlink:href="#E5-MJSZ3-7B" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(917,0)"><g transform="translate(-15,0)"><g transform="translate(0,600)"><use x="0" xlink:href="#E5-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="640" xlink:href="#E5-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1029" xlink:href="#E5-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1751" xlink:href="#E5-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2751" xlink:href="#E5-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(3391,0)"><use x="0" xlink:href="#E5-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E5-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g></g><g transform="translate(0,-681)"><use x="0" xlink:href="#E5-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="389" xlink:href="#E5-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1111" xlink:href="#E5-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2111" xlink:href="#E5-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2751,0)"><use x="0" xlink:href="#E5-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="550" xlink:href="#E5-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g></g></g><g transform="translate(5109,0)"><g transform="translate(0,600)"><use xlink:href="#E5-MJMAIN-69" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="278" xlink:href="#E5-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="834" xlink:href="#E5-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1456" xlink:href="#E5-MJMAIN-3C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2512" xlink:href="#E5-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(0,-681)"><use xlink:href="#E5-MJMAIN-69" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="278" xlink:href="#E5-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="834" xlink:href="#E5-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1456" xlink:href="#E5-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2512" xlink:href="#E5-MJMATHI-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></g></g></svg></span></span><script id="MathJax-Element-5" type="math/tex; mode=display">w_i = \begin{cases} \alpha (1 - \alpha)^{i} & \text{if } i < t \\ (1 - \alpha)^{i} & \text{if } i = t \end{cases}</script>
上式中的<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-25-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.41ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -504.6 640 607.1" width="1.486ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E25-MJMATHI-3B1" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E25-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-25" type="math/tex">\alpha</script>有四种方式，其中最简单的就是直接设置 `alpha`参数。剩下的三种就是间接给出：
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display" style="text-align: center;"><span class="MathJax_SVG" id="MathJax-Element-6-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="10.749ex" role="img" style="vertical-align: -4.6ex; margin-bottom: -0.191ex;" viewbox="0 -2565.2 20882.7 4627.8" width="48.502ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E6-MJMATHI-3B1" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E6-MJMAIN-3D" stroke-width="0"></path><path d="M434 -231Q434 -244 428 -250H410Q281 -250 230 -184Q225 -177 222 -172T217 -161T213 -148T211 -133T210 -111T209 -84T209 -47T209 0Q209 21 209 53Q208 142 204 153Q203 154 203 155Q189 191 153 211T82 231Q71 231 68 234T65 250T68 266T82 269Q116 269 152 289T203 345Q208 356 208 377T209 529V579Q209 634 215 656T244 698Q270 724 324 740Q361 748 377 749Q379 749 390 749T408 750H428Q434 744 434 732Q434 719 431 716Q429 713 415 713Q362 710 332 689T296 647Q291 634 291 499V417Q291 370 288 353T271 314Q240 271 184 255L170 250L184 245Q202 239 220 230T262 196T290 137Q291 131 291 1Q291 -134 296 -147Q306 -174 339 -192T415 -213Q429 -213 431 -216Q434 -219 434 -231Z" id="E6-MJMAIN-7B" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E6-MJMAIN-32" stroke-width="0"></path><path d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z" id="E6-MJMATHI-73" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E6-MJMAIN-2B" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E6-MJMAIN-31" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E6-MJMAIN-2C" stroke-width="0"></path><path d="M273 0Q255 3 146 3Q43 3 34 0H26V46H42Q70 46 91 49Q99 52 103 60Q104 62 104 224V385H33V431H104V497L105 564L107 574Q126 639 171 668T266 704Q267 704 275 704T289 705Q330 702 351 679T372 627Q372 604 358 590T321 576T284 590T270 627Q270 647 288 667H284Q280 668 273 668Q245 668 223 647T189 592Q183 572 182 497V431H293V385H185V225Q185 63 186 61T189 57T194 54T199 51T206 49T213 48T222 47T231 47T241 46T251 46H282V0H273Z" id="E6-MJMAIN-66" stroke-width="0"></path><path d="M28 214Q28 309 93 378T250 448Q340 448 405 380T471 215Q471 120 407 55T250 -10Q153 -10 91 57T28 214ZM250 30Q372 30 372 193V225V250Q372 272 371 288T364 326T348 362T317 390T268 410Q263 411 252 411Q222 411 195 399Q152 377 139 338T126 246V226Q126 130 145 91Q177 30 250 30Z" id="E6-MJMAIN-6F" stroke-width="0"></path><path d="M36 46H50Q89 46 97 60V68Q97 77 97 91T98 122T98 161T98 203Q98 234 98 269T98 328L97 351Q94 370 83 376T38 385H20V408Q20 431 22 431L32 432Q42 433 60 434T96 436Q112 437 131 438T160 441T171 442H174V373Q213 441 271 441H277Q322 441 343 419T364 373Q364 352 351 337T313 322Q288 322 276 338T263 372Q263 381 265 388T270 400T273 405Q271 407 250 401Q234 393 226 386Q179 341 179 207V154Q179 141 179 127T179 101T180 81T180 66V61Q181 59 183 57T188 54T193 51T200 49T207 48T216 47T225 47T235 46T245 46H276V0H267Q249 3 140 3Q37 3 28 0H20V46H36Z" id="E6-MJMAIN-72" stroke-width="0"></path><path d="M295 316Q295 356 268 385T190 414Q154 414 128 401Q98 382 98 349Q97 344 98 336T114 312T157 287Q175 282 201 278T245 269T277 256Q294 248 310 236T342 195T359 133Q359 71 321 31T198 -10H190Q138 -10 94 26L86 19L77 10Q71 4 65 -1L54 -11H46H42Q39 -11 33 -5V74V132Q33 153 35 157T45 162H54Q66 162 70 158T75 146T82 119T101 77Q136 26 198 26Q295 26 295 104Q295 133 277 151Q257 175 194 187T111 210Q75 227 54 256T33 318Q33 357 50 384T93 424T143 442T187 447H198Q238 447 268 432L283 424L292 431Q302 440 314 448H322H326Q329 448 335 442V310L329 304H301Q295 310 295 316Z" id="E6-MJMAIN-73" stroke-width="0"></path><path d="M36 -148H50Q89 -148 97 -134V-126Q97 -119 97 -107T97 -77T98 -38T98 6T98 55T98 106Q98 140 98 177T98 243T98 296T97 335T97 351Q94 370 83 376T38 385H20V408Q20 431 22 431L32 432Q42 433 61 434T98 436Q115 437 135 438T165 441T176 442H179V416L180 390L188 397Q247 441 326 441Q407 441 464 377T522 216Q522 115 457 52T310 -11Q242 -11 190 33L182 40V-45V-101Q182 -128 184 -134T195 -145Q216 -148 244 -148H260V-194H252L228 -193Q205 -192 178 -192T140 -191Q37 -191 28 -194H20V-148H36ZM424 218Q424 292 390 347T305 402Q234 402 182 337V98Q222 26 294 26Q345 26 384 80T424 218Z" id="E6-MJMAIN-70" stroke-width="0"></path><path d="M137 305T115 305T78 320T63 359Q63 394 97 421T218 448Q291 448 336 416T396 340Q401 326 401 309T402 194V124Q402 76 407 58T428 40Q443 40 448 56T453 109V145H493V106Q492 66 490 59Q481 29 455 12T400 -6T353 12T329 54V58L327 55Q325 52 322 49T314 40T302 29T287 17T269 6T247 -2T221 -8T190 -11Q130 -11 82 20T34 107Q34 128 41 147T68 188T116 225T194 253T304 268H318V290Q318 324 312 340Q290 411 215 411Q197 411 181 410T156 406T148 403Q170 388 170 359Q170 334 154 320ZM126 106Q126 75 150 51T209 26Q247 26 276 49T315 109Q317 116 318 175Q318 233 317 233Q309 233 296 232T251 223T193 203T147 166T126 106Z" id="E6-MJMAIN-61" stroke-width="0"></path><path d="M41 46H55Q94 46 102 60V68Q102 77 102 91T102 122T103 161T103 203Q103 234 103 269T102 328V351Q99 370 88 376T43 385H25V408Q25 431 27 431L37 432Q47 433 65 434T102 436Q119 437 138 438T167 441T178 442H181V402Q181 364 182 364T187 369T199 384T218 402T247 421T285 437Q305 442 336 442Q450 438 463 329Q464 322 464 190V104Q464 66 466 59T477 49Q498 46 526 46H542V0H534L510 1Q487 2 460 2T422 3Q319 3 310 0H302V46H318Q379 46 379 62Q380 64 380 200Q379 335 378 343Q372 371 358 385T334 402T308 404Q263 404 229 370Q202 343 195 315T187 232V168V108Q187 78 188 68T191 55T200 49Q221 46 249 46H265V0H257L234 1Q210 2 183 2T145 3Q42 3 33 0H25V46H41Z" id="E6-MJMAIN-6E" stroke-width="0"></path><path d="M83 616Q83 624 89 630T99 636Q107 636 253 568T543 431T687 361Q694 356 694 346T687 331Q685 329 395 192L107 56H101Q83 58 83 76Q83 77 83 79Q82 86 98 95Q117 105 248 167Q326 204 378 228L626 346L360 472Q291 505 200 548Q112 589 98 597T83 616ZM84 -118Q84 -108 99 -98H678Q694 -104 694 -118Q694 -130 679 -138H98Q84 -131 84 -118Z" id="E6-MJMAIN-2265" stroke-width="0"></path><path d="M34 159Q34 268 120 355T306 442Q362 442 394 418T427 355Q427 326 408 306T360 285Q341 285 330 295T319 325T330 359T352 380T366 386H367Q367 388 361 392T340 400T306 404Q276 404 249 390Q228 381 206 359Q162 315 142 235T121 119Q121 73 147 50Q169 26 205 26H209Q321 26 394 111Q403 121 406 121Q410 121 419 112T429 98T420 83T391 55T346 25T282 0T202 -11Q127 -11 81 37T34 159Z" id="E6-MJMATHI-63" stroke-width="0"></path><path d="M370 305T349 305T313 320T297 358Q297 381 312 396Q317 401 317 402T307 404Q281 408 258 408Q209 408 178 376Q131 329 131 219Q131 137 162 90Q203 29 272 29Q313 29 338 55T374 117Q376 125 379 127T395 129H409Q415 123 415 120Q415 116 411 104T395 71T366 33T318 2T249 -11Q163 -11 99 53T34 214Q34 318 99 383T250 448T370 421T404 357Q404 334 387 320Z" id="E6-MJMAIN-63" stroke-width="0"></path><path d="M28 218Q28 273 48 318T98 391T163 433T229 448Q282 448 320 430T378 380T406 316T415 245Q415 238 408 231H126V216Q126 68 226 36Q246 30 270 30Q312 30 342 62Q359 79 369 104L379 128Q382 131 395 131H398Q415 131 415 121Q415 117 412 108Q393 53 349 21T250 -11Q155 -11 92 58T28 218ZM333 275Q322 403 238 411H236Q228 411 220 410T195 402T166 381T143 340T127 274V267H333V275Z" id="E6-MJMAIN-65" stroke-width="0"></path><path d="M27 422Q80 426 109 478T141 600V615H181V431H316V385H181V241Q182 116 182 100T189 68Q203 29 238 29Q282 29 292 100Q293 108 293 146V181H333V146V134Q333 57 291 17Q264 -10 221 -10Q187 -10 162 2T124 33T105 68T98 100Q97 107 97 248V385H18V422H27Z" id="E6-MJMAIN-74" stroke-width="0"></path><path d="M41 46H55Q94 46 102 60V68Q102 77 102 91T102 122T103 161T103 203Q103 234 103 269T102 328V351Q99 370 88 376T43 385H25V408Q25 431 27 431L37 432Q47 433 65 434T102 436Q119 437 138 438T167 441T178 442H181V402Q181 364 182 364T187 369T199 384T218 402T247 421T285 437Q305 442 336 442Q351 442 364 440T387 434T406 426T421 417T432 406T441 395T448 384T452 374T455 366L457 361L460 365Q463 369 466 373T475 384T488 397T503 410T523 422T546 432T572 439T603 442Q729 442 740 329Q741 322 741 190V104Q741 66 743 59T754 49Q775 46 803 46H819V0H811L788 1Q764 2 737 2T699 3Q596 3 587 0H579V46H595Q656 46 656 62Q657 64 657 200Q656 335 655 343Q649 371 635 385T611 402T585 404Q540 404 506 370Q479 343 472 315T464 232V168V108Q464 78 465 68T468 55T477 49Q498 46 526 46H542V0H534L510 1Q487 2 460 2T422 3Q319 3 310 0H302V46H318Q379 46 379 62Q380 64 380 200Q379 335 378 343Q372 371 358 385T334 402T308 404Q263 404 229 370Q202 343 195 315T187 232V168V108Q187 78 188 68T191 55T200 49Q221 46 249 46H265V0H257L234 1Q210 2 183 2T145 3Q42 3 33 0H25V46H41Z" id="E6-MJMAIN-6D" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E6-MJMAIN-30" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E6-MJMAIN-2212" stroke-width="0"></path><path d="M201 0Q189 3 102 3Q26 3 17 0H11V46H25Q48 47 67 52T96 61T121 78T139 96T160 122T180 150L226 210L168 288Q159 301 149 315T133 336T122 351T113 363T107 370T100 376T94 379T88 381T80 383Q74 383 44 385H16V431H23Q59 429 126 429Q219 429 229 431H237V385Q201 381 201 369Q201 367 211 353T239 315T268 274L272 270L297 304Q329 345 329 358Q329 364 327 369T322 376T317 380T310 384L307 385H302V431H309Q324 428 408 428Q487 428 493 431H499V385H492Q443 385 411 368Q394 360 377 341T312 257L296 236L358 151Q424 61 429 57T446 50Q464 46 499 46H516V0H510H502Q494 1 482 1T457 2T432 2T414 3Q403 3 377 3T327 1L304 0H295V46H298Q309 46 320 51T331 63Q331 65 291 120L250 175Q249 174 219 133T185 88Q181 83 181 74Q181 63 188 55T206 46Q208 46 208 23V0H201Z" id="E6-MJMAIN-78" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E6-MJMAIN-28" stroke-width="0"></path><path d="M42 46H56Q95 46 103 60V68Q103 77 103 91T103 124T104 167T104 217T104 272T104 329Q104 366 104 407T104 482T104 542T103 586T103 603Q100 622 89 628T44 637H26V660Q26 683 28 683L38 684Q48 685 67 686T104 688Q121 689 141 690T171 693T182 694H185V379Q185 62 186 60Q190 52 198 49Q219 46 247 46H263V0H255L232 1Q209 2 183 2T145 3T107 3T57 1L34 0H26V46H42Z" id="E6-MJMAIN-6C" stroke-width="0"></path><path d="M329 409Q373 453 429 453Q459 453 472 434T485 396Q485 382 476 371T449 360Q416 360 412 390Q410 404 415 411Q415 412 416 414V415Q388 412 363 393Q355 388 355 386Q355 385 359 381T368 369T379 351T388 325T392 292Q392 230 343 187T222 143Q172 143 123 171Q112 153 112 133Q112 98 138 81Q147 75 155 75T227 73Q311 72 335 67Q396 58 431 26Q470 -13 470 -72Q470 -139 392 -175Q332 -206 250 -206Q167 -206 107 -175Q29 -140 29 -75Q29 -39 50 -15T92 18L103 24Q67 55 67 108Q67 155 96 193Q52 237 52 292Q52 355 102 398T223 442Q274 442 318 416L329 409ZM299 343Q294 371 273 387T221 404Q192 404 171 388T145 343Q142 326 142 292Q142 248 149 227T179 192Q196 182 222 182Q244 182 260 189T283 207T294 227T299 242Q302 258 302 292T299 343ZM403 -75Q403 -50 389 -34T348 -11T299 -2T245 0H218Q151 0 138 -6Q118 -15 107 -34T95 -74Q95 -84 101 -97T122 -127T170 -155T250 -167Q319 -167 361 -139T403 -75Z" id="E6-MJMAIN-67" stroke-width="0"></path><path d="M78 60Q78 84 95 102T138 120Q162 120 180 104T199 61Q199 36 182 18T139 0T96 17T78 60Z" id="E6-MJMAIN-2E" stroke-width="0"></path><path d="M164 157Q164 133 148 117T109 101H102Q148 22 224 22Q294 22 326 82Q345 115 345 210Q345 313 318 349Q292 382 260 382H254Q176 382 136 314Q132 307 129 306T114 304Q97 304 95 310Q93 314 93 485V614Q93 664 98 664Q100 666 102 666Q103 666 123 658T178 642T253 634Q324 634 389 662Q397 666 402 666Q410 666 410 648V635Q328 538 205 538Q174 538 149 544L139 546V374Q158 388 169 396T205 412T256 420Q337 420 393 355T449 201Q449 109 385 44T229 -22Q148 -22 99 32T50 154Q50 178 61 192T84 210T107 214Q132 214 148 197T164 157Z" id="E6-MJMAIN-35" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E6-MJMATHI-68" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E6-MJMAIN-29" stroke-width="0"></path><path d="M41 46H55Q94 46 102 60V68Q102 77 102 91T102 124T102 167T103 217T103 272T103 329Q103 366 103 407T103 482T102 542T102 586T102 603Q99 622 88 628T43 637H25V660Q25 683 27 683L37 684Q47 685 66 686T103 688Q120 689 140 690T170 693T181 694H184V367Q244 442 328 442Q451 442 463 329Q464 322 464 190V104Q464 66 466 59T477 49Q498 46 526 46H542V0H534L510 1Q487 2 460 2T422 3Q319 3 310 0H302V46H318Q379 46 379 62Q380 64 380 200Q379 335 378 343Q372 371 358 385T334 402T308 404Q263 404 229 370Q202 343 195 315T187 232V168V108Q187 78 188 68T191 55T200 49Q221 46 249 46H265V0H257L234 1Q210 2 183 2T145 3Q42 3 33 0H25V46H41Z" id="E6-MJMAIN-68" stroke-width="0"></path><path d="M11 179V252H277V179H11Z" id="E6-MJMAIN-2D" stroke-width="0"></path><path d="M69 609Q69 637 87 653T131 669Q154 667 171 652T188 609Q188 579 171 564T129 549Q104 549 87 564T69 609ZM247 0Q232 3 143 3Q132 3 106 3T56 1L34 0H26V46H42Q70 46 91 49Q100 53 102 60T104 102V205V293Q104 345 102 359T88 378Q74 385 41 385H30V408Q30 431 32 431L42 432Q52 433 70 434T106 436Q123 437 142 438T171 441T182 442H185V62Q190 52 197 50T232 46H255V0H247Z" id="E6-MJMAIN-69" stroke-width="0"></path><path d="M84 520Q84 528 88 533T96 539L99 540Q106 540 253 471T544 334L687 265Q694 260 694 250T687 235Q685 233 395 96L107 -40H101Q83 -38 83 -20Q83 -19 83 -17Q82 -10 98 -1Q117 9 248 71Q326 108 378 132L626 250L378 368Q90 504 86 509Q84 513 84 520Z" id="E6-MJMAIN-3E" stroke-width="0"></path><path d="M712 899L718 893V876V865Q718 854 704 846Q627 793 577 710T510 525Q510 524 509 521Q505 493 504 349Q504 345 504 334Q504 277 504 240Q504 -2 503 -4Q502 -8 494 -9T444 -10Q392 -10 390 -9Q387 -8 386 -5Q384 5 384 230Q384 262 384 312T383 382Q383 481 392 535T434 656Q510 806 664 892L677 899H712Z" id="E6-MJSZ4-23A7" stroke-width="0"></path><path d="M718 -893L712 -899H677L666 -893Q542 -825 468 -714T385 -476Q384 -466 384 -282Q384 3 385 5L389 9Q392 10 444 10Q486 10 494 9T503 4Q504 2 504 -239V-310V-366Q504 -470 508 -513T530 -609Q546 -657 569 -698T617 -767T661 -812T699 -843T717 -856T718 -876V-893Z" id="E6-MJSZ4-23A9" stroke-width="0"></path><path d="M389 1159Q391 1160 455 1160Q496 1160 498 1159Q501 1158 502 1155Q504 1145 504 924Q504 691 503 682Q494 549 425 439T243 259L229 250L243 241Q349 175 421 66T503 -182Q504 -191 504 -424Q504 -600 504 -629T499 -659H498Q496 -660 444 -660T390 -659Q387 -658 386 -655Q384 -645 384 -425V-282Q384 -176 377 -116T342 10Q325 54 301 92T255 155T214 196T183 222T171 232Q170 233 170 250T171 268Q171 269 191 284T240 331T300 407T354 524T383 679Q384 691 384 925Q384 1152 385 1155L389 1159Z" id="E6-MJSZ4-23A8" stroke-width="0"></path><path d="M384 150V266Q384 304 389 309Q391 310 455 310Q496 310 498 309Q502 308 503 298Q504 283 504 150Q504 32 504 12T499 -9H498Q496 -10 444 -10T390 -9Q386 -8 385 2Q384 17 384 150Z" id="E6-MJSZ4-23AA" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E6-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="917" xlink:href="#E6-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1973,0)"><g transform="translate(0,2480)"><use x="0" xlink:href="#E6-MJSZ4-23A7" xmlns:xlink="http://www.w3.org/1999/xlink" y="-899"></use><g transform="translate(0,-1354.3837359443355) scale(1,1.5980120514333407)"><use xlink:href="#E6-MJSZ4-23AA" xmlns:xlink="http://www.w3.org/1999/xlink"></use></g><use x="0" xlink:href="#E6-MJSZ4-23A8" xmlns:xlink="http://www.w3.org/1999/xlink" y="-2481"></use><g transform="translate(0,-3585.7475924030045) scale(1,1.5980120514333407)"><use xlink:href="#E6-MJSZ4-23AA" xmlns:xlink="http://www.w3.org/1999/xlink"></use></g><use x="0" xlink:href="#E6-MJSZ4-23A9" xmlns:xlink="http://www.w3.org/1999/xlink" y="-3562"></use></g><g transform="translate(1056,0)"><g transform="translate(-15,0)"><g transform="translate(0,1605)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="1355" x="0" y="220"></rect><use transform="scale(0.707)" x="708" xlink:href="#E6-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-376)"><use transform="scale(0.707)" x="0" xlink:href="#E6-MJMATHI-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="469" xlink:href="#E6-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1246" xlink:href="#E6-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="1595" xlink:href="#E6-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(0,96)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="1329" x="0" y="220"></rect><use transform="scale(0.707)" x="690" xlink:href="#E6-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-376)"><use transform="scale(0.707)" x="0" xlink:href="#E6-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="500" xlink:href="#E6-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1278" xlink:href="#E6-MJMATHI-63" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="1569" xlink:href="#E6-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(0,-1578)"><use x="0" xlink:href="#E6-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="722" xlink:href="#E6-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1722,0)"><use xlink:href="#E6-MJMAIN-65" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="444" xlink:href="#E6-MJMAIN-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="972" xlink:href="#E6-MJMAIN-70" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="3250" xlink:href="#E6-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(3639,0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="2094" x="0" y="220"></rect><g transform="translate(59,549)"><use transform="scale(0.707)" xlink:href="#E6-MJMAIN-6C" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use transform="scale(0.707)" x="278" xlink:href="#E6-MJMAIN-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="778" xlink:href="#E6-MJMAIN-67" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1070,0)"><use transform="scale(0.707)" xlink:href="#E6-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use transform="scale(0.707)" x="500" xlink:href="#E6-MJMAIN-2E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="778" xlink:href="#E6-MJMAIN-35" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use transform="scale(0.707)" x="1192" xlink:href="#E6-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="-559"></use></g></g><use x="5973" xlink:href="#E6-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6362" xlink:href="#E6-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(7625,0)"><g transform="translate(0,1605)"><use xlink:href="#E6-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="306" xlink:href="#E6-MJMAIN-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="806" xlink:href="#E6-MJMAIN-72" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1448" xlink:href="#E6-MJMAIN-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1842" xlink:href="#E6-MJMAIN-70" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2398" xlink:href="#E6-MJMAIN-61" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2898" xlink:href="#E6-MJMAIN-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3704" xlink:href="#E6-MJMATHI-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4450" xlink:href="#E6-MJMAIN-2265" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5506" xlink:href="#E6-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(0,96)"><use xlink:href="#E6-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="306" xlink:href="#E6-MJMAIN-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="806" xlink:href="#E6-MJMAIN-72" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1448" xlink:href="#E6-MJMAIN-63" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1892" xlink:href="#E6-MJMAIN-65" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2336" xlink:href="#E6-MJMAIN-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2892" xlink:href="#E6-MJMAIN-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3281" xlink:href="#E6-MJMAIN-65" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3725" xlink:href="#E6-MJMAIN-72" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4367" xlink:href="#E6-MJMAIN-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4867" xlink:href="#E6-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5423" xlink:href="#E6-MJMAIN-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6256" xlink:href="#E6-MJMAIN-61" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6756" xlink:href="#E6-MJMAIN-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7150" xlink:href="#E6-MJMAIN-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7794" xlink:href="#E6-MJMATHI-63" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8504" xlink:href="#E6-MJMAIN-2265" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9560" xlink:href="#E6-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><g transform="translate(0,-1578)"><use xlink:href="#E6-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="306" xlink:href="#E6-MJMAIN-6F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="806" xlink:href="#E6-MJMAIN-72" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1448" xlink:href="#E6-MJMAIN-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2004" xlink:href="#E6-MJMAIN-61" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2504" xlink:href="#E6-MJMAIN-6C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2782" xlink:href="#E6-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3088" xlink:href="#E6-MJMAIN-2D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3421" xlink:href="#E6-MJMAIN-6C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3699" xlink:href="#E6-MJMAIN-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3977" xlink:href="#E6-MJMAIN-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4283" xlink:href="#E6-MJMAIN-65" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4977" xlink:href="#E6-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5830" xlink:href="#E6-MJMAIN-3E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6886" xlink:href="#E6-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></g></g></svg></span></span><script id="MathJax-Element-6" type="math/tex; mode=display">\alpha = \begin{cases} \frac{2}{s + 1}, & \text{for span}\ s \geq 1\\ \frac{1}{1 + c}, & \text{for center of mass}\ c \geq 0\\ 1 - \exp(\frac{\log 0.5}{h}), & \text{for half-life}\ h > 0 \end{cases}</script>
该函数返回的是一个`EWM`对象。其统计方法有：

    * `mean()`：指数加权移动平均的均值
    * `var()`：指数加权移动平均的方差
    * `std()`：指数加权移动平均的标准差
    * `corr()`：指数加权移动平均的相关系数
    * `cov()`：指数加权移动平均的协方差

![ewm0](../imgs/ewm0.JPG) ![ewm1](../imgs/ewm1.JPG) ![ewm2](../imgs/ewm2.JPG)

4. 拓展窗口是`rolling`窗口的特殊情况：当窗口大小等于序列长度。另外`expanding`窗口中，如果数据有空缺，则剔除空缺值再计算。

```
xxxxxxxxxx  DataFrame/Series.expanding(min_periods=1, freq=None, center=False, axis=0)
```

    * `min_periods`：一个整数。给出了窗口内有效值的数量。
    * `freq`：一个字符串或者`DateOffset`对象，该参数被废弃。它用于对数据重采样，因为我们一般使用`resample()`来完成，所以该参数被废弃。
    * `center`：一个布尔值。如果为`True`，则`label`为窗口的中心的值。默认情况下，`label`为窗口的右侧的值。
    * `axis`：一个整数。指定沿着0轴还是1轴移动平均。如果为`0/'index'`则沿着0轴；如果为`1/'columns'`则沿着0轴

它返回一个`Expanding`对象。

它的统计方法如下：

    * `count()` ：有效值数量
    * `sum()` ：和
    * `mean()` ：均值
    * `median()` ：中位数
    * `min()` ：最小值
    * `max()` ：最大值
    * `std()` ：标准差
    * `var()` ：方差
    * `skew()` ：斜度
    * `kurt()` ：峰度
    * `quantile()` ：百分位数
    * `apply()` ：通用处理函数。其参数为一个可调用对象，该可调用对象接受一个序列，返回一个标量。
    * `cov()` ：协方差
    * `corr()` ：相关系数

![expanding0](../imgs/expanding0.JPG) ![expanding1](../imgs/expanding1.JPG)

> > 

> 在`Center`中，`2016-11-01`为中心的话，它右侧有4个数据，左侧理论上有5个数据（窗口总长为10），而左侧为空，因此第一个窗口就是前 5 个数据的统计量。




## 十二、 数据加载和保存

### 1. 文本文件

1. `read_csv`可以读取文本文件(`.csv` 格式):

```
xxxxxxxxxx  pandas.read_csv(filepath_or_buffer, sep=', ', delimiter=None, header='infer',  names=None, index_col=None, usecols=None, squeeze=False, prefix=None,   mangle_dupe_cols=True, dtype=None, engine=None, converters=None, true_values=None,  false_values=None, skipinitialspace=False,skiprows=None, nrows=None,na_values=None,  keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True,   parse_dates=False, infer_datetime_format=False,keep_date_col=False,date_parser=None,  dayfirst=False, iterator=False, chunksize=None, compression='infer', thousands=None,   decimal='.', lineterminator=None, quotechar='"', quoting=0, escapechar=None,  comment=None, encoding=None, dialect=None, tupleize_cols=False,   error_bad_lines=True, warn_bad_lines=True, skipfooter=0, skip_footer=0,   doublequote=True, delim_whitespace=False, as_recarray=False,  compact_ints=False, use_unsigned=False, low_memory=True,   buffer_lines=None, memory_map=False, float_precision=None)
```

    * `filepath_or_buffer`：一个字符串，或者一个`pathlib.Path`对象，或者任何拥有`.read()`方法的对象。它指定了被解析的文件的位置。如果是个字符串，则必须是个`URL`（其中包含了协议名，如`http//,ftp//,file//`等）

    * `sep`：一个字符串，指定了分隔符。默认为`','`。如果设定为`None`，则自动决议分隔符。

        * 如果字符串长度大于1，则自动解析为正则表达式。如`'\s+\`解析为空白符

    * `delimiter`：一个字符串，指定了分隔符。它是`sep`参数的另一个候选参数

    * `delim_whitespace`：一个布尔值。如果为`True`，则将空白符（连续的空白或者单个空白）作为分隔符。此时不需要提供`delimiter`参数。它等价于`sep='\s+'`

    * `header`：一个整数或者整数列表。它指定了那些行是标题行，0表示第一行。如果你指定了`header=[1,3,5]`，则第三行（行`id=2`）和第五行（行`id=4`）被忽略（不被解析）。

        * 如果`names`参数为空，则`header`默认值为 0.如果`names`参数提供了，则`header`默认值为`None`



```
- 该参数会忽略注释行。
- 如果`skip_blank_lines=True`，则该参数会忽略空白行。因此`header=0`表示第一个有效的数据行
```

* `names`：一个`array-like`。它给出了列名。

    * 如果文件不包含标题行，则你需要显式通过`names`传入列名
    * 如果`mangle_dupe_cols=True`，则可以传入重复的列名。否则不允许重复列名

* `index_col`：一个整数，或者序列，或者`False`。它指定哪一列作为`row labels`。如果你指定了一个序列，则使用`MultiIndex`。如果为`False`，则不采用任何列作为`row labels`

* `usecols`：一个`array-like`。它指定：你将采用哪些列来组装`DataFrame`。该参数各元素必须要么是代表位置的整数，要么是代表列名的字符串

* `as_recarray`：一个布尔值。被废弃的参数。

* `squeeze`：一个布尔值。如果为`True`，则当解析结果只有一列数据时，返回一个`Series`而不是`DataFrame`

* `prefix`：一个字符串。当没有标题时，你可以提供这个参数来给列名加一个前缀。（如果不加前缀，则列名就是`0,1,2...`）

* `mangle_dupe_cols`：一个布尔值。如果为`True`，则重复的列名`X,X...`被修改为`X.0,X.1,...`。如果为`False`，则重复的列名这样处理：后面的覆盖前面的

* `dtype`：一个`Type name`或者字典：`column->type`。它可以给出每个列的类型。

* `engine`：一个字符串，指定用什么解析引擎。可以为`'c'/'python'`。`c`更快，但是`python`拥有更多特性

* `converters`：一个字典，给出了每一列的转换函数。字典的键为代表列的位置的整数，或者代表列的名字的字符串。字典的值为可调用对象，参数为一个标量（就是每个元素值）

* `true_values`：一个列表，给出了哪些值被认为是`True`

* `false_values`：一个列表，给出了哪些值被认为是`False`

* `skipinitialspace`：一个布尔值。如果为`True`，则跳过分隔符之后的空白符

* `skiprows`：一个`array-like`或者整数。如果为序列，则指定跳过哪些行（从0计数）；如果为整数，则指定跳过文件开头的多少行。注意：空行和注释行也包括在内，这一点和`header`不同。

* `skipfooter`：一个整数。指定跳过文件结尾的多少行。不支持`engine='c'`

* `skip_footer`：被废弃的参数

* `nrows`：一个整数。指定读取多少行。

* `na_values`：一个标量、字符串、字典、列表。指定哪些被识别为`NAN`。默认的`NAN`为列表`['nan','NAN','NULL'....]`

* `keep_default_na`：一个布尔值。如果为`True`，则当你指定了`na_values`时，默认的`NAN`被追加到`na_values`上；否则指定的`na_values`代替了默认的`NAN`

* `na_filter`：一个布尔值。如果为`True`，则不检查`NaN`，此时解析速度大大加快（但是要求你的数据确实没有`NAN`）

* `verbose`：一个布尔值。如果为`True`，输出解析日志

* `skip_blank_lines`：一个布尔值。如果为`True`，则跳过空白行，而不是解析为`NaN`

* `parse_dates`：一个布尔值、整数列表、标签列表、或者`list of list or dict`。对于`iso8601`格式的日期字符串，解析速度很快。

    * 如果为布尔值：如果为`True`，则解析`index`为日期
    * 如果为整数列表或者标签列表，则解析对应的列为日期
    * 如果列表的列表，如`[[1,3]]`，则将列1和列3组合在一起，解析成一个单独的日期列
    * 如果为字典，如`{'aaa':[1,3]}`，则将列1和列3组合在一起，解析成一个单独的日期列，日期列的名字为`'aaa'`。

* `infer_datetime_format`：一个布尔值。如果为`True`，且`parse_dates`非空，则`pandas`试图从数据中推断日期格式。

* `keep_date_col`：一个布尔值。如果为`True`，并且`parse_dates`使用多个列合成一列日期，则保留原有的列

* `date_parser`：一个函数对象。它将一列字符串转换成一列日期。

* `dayfirse`：一个字符串。如果为`True`，则日期格式为`DD/MM`

* `iterator`：一个布尔值。如果为`True`，则返回一个`TextFileReader`对象，该对象可以用于迭代或者`.get_chunk()`来返回数据块

* `chunksize`：一个整数。指定`TextFileReader`对象`.get_chunk()`返回的数据块的大小。

* `compression`：一个字符串。可以为`'infer','gzip','bz2','zip','xz',None`。如果文件为压缩文件，则它用于指定解压格式

* `thousands`：一个字符串。指定了数值中千位数的分隔符，如`999,999,999`

* `decimal`：一个字符串，指定了小数点的分隔符，如`9.999`

* `float_precision`：一个字符串。指定了`C engine`的转换浮点数的精度。`None`普通转换，`'high'`为高精度转换，`'round_trip'`为`round_trip`转换。

* `lineterminator`：一个长度为1的字符串。指定了`C engine`中的换行符

* `quotechar`：一个长度为1的字符串，它指定了引用字符。比如`"aaa,bbb"`，这种数据是引用数据。如果你用`,`分隔，则有问题。在引用字符包围的数据中，不考虑分隔符。

* `comment`：一个长度为1的字符串，指定了注释字符。如果该字符串出现在行中，则行末的字符不被解析。如果该字符串出现在行首，则本行不被就解析。

* `encoding`：一个字符串，指定了编码类型

* `error_bad_lines`：一个布尔值。如果为`True`，则如果某一行有太多字段，则函数抛出异常。如果为`False`，则抛弃该行，顺利解析。只用于`C engine`

* `warn_bad_lines`：一个布尔值。如果为`True`，且`error_bad_lines=False`，则对于异常的行，输出警告

* `buffer_lines/compact_ints /use_unsigned`：被废弃的参数

* `memory_map`：如果为`True`，且`filepath`是一个文件名，则使用内存映射，将文件映射到内存中。


![read_csv0](../imgs/read_csv0.JPG) ![read_csv1](../imgs/read_csv1.JPG)

1. `read_table`也能完成`read_csv`的功能。二者接口一致。

```
xxxxxxxxxx  pandas.read_table(filepath_or_buffer, sep='\t', delimiter=None, header='infer',   names=None, index_col=None, usecols=None, squeeze=False, prefix=None,   mangle_dupe_cols=True, dtype=None, engine=None, converters=None, true_values=None,  false_values=None, skipinitialspace=False,skiprows=None, nrows=None, na_values=None,  keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True,  parse_dates=False,infer_datetime_format=False,keep_date_col=False, date_parser=None,  dayfirst=False, iterator=False, chunksize=None, compression='infer', thousands=None,  decimal='.', lineterminator=None, quotechar='"', quoting=0, escapechar=None,  comment=None, encoding=None, dialect=None, tupleize_cols=False,   error_bad_lines=True, warn_bad_lines=True, skipfooter=0, skip_footer=0,  doublequote=True, delim_whitespace=False, as_recarray=False,  compact_ints=False, use_unsigned=False, low_memory=True,  buffer_lines=None, memory_map=False, float_precision=None)
```

2. `DataFrame/Series.to_csv`方法可以将数据写入到文件中

```
xxxxxxxxxx  DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None,  columns=None, header=True, index=True, index_label=None, mode='w',   encoding=None, compression=None, quoting=None, quotechar='"',  line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None,   doublequote=True, escapechar=None, decimal='.')  Series.to_csv(path=None, index=True, sep=', ', na_rep='', float_format=None,   header=False, index_label=None, mode='w', encoding=None, date_format=None,   decimal='.')
```

    * `path_or_buf`：一个字符串或者`file`对象。指定写入的文件。如果为空，则返回一个字符串而不是写入文件
    * `sep`：一个字符串，指定字段的分隔符
    * `na_rep`：一个字符串，指定`NaN`的代表字符串
    * `float_format`：一个字符串，指定了浮点数的格式化字符串
    * `columns`：一个序列，指定要写入哪些列
    * `header`：一个布尔值或者字符串列表。如果为`True`，则写出列名。如果为字符串列表，则它直接指定了列名的别名
    * `index`：一个布尔值。如果为`True`，则输出`index label`
    * `mode`：一个字符串，文件操作的读写模式。默认为`'w'`
    * `encoding`：一个字符串，指定编码方式
    * `compression`：一个字符串，指定压缩格式
    * `line_terminator`：一个字符串，指定换行符
    * `chunksize`：一个整数，指定了一次写入多少行
    * `date_format`：一个字符串，给出了日期格式化字符串
    * `decimal`：一个字符串，给出了小数点的格式
    * `tupleize_cols`：一个布尔值。如果为`True`，则`MultiIndex`被写成`list of tuples`

![to_csv](../imgs/to_csv.JPG)


### 2. Json

1. `read_json`能够读取`Json`文件：

```
xxxxxxxxxx  pandas.read_json(path_or_buf=None, orient=None, typ='frame', dtype=True,   convert_axes=True, convert_dates=True, keep_default_dates=True, numpy=False,  precise_float=False, date_unit=None, encoding=None, lines=False)
```

    * `path_or_buf`：一个字符串或者一个`file-like`对象。如果是个字符串，则必须是个`URL`（其中包含了协议名，如`http//,ftp//,file//`等）
    * `orient`：一个字符串，指定了期望的`JSON`格式。可选的格式有（参考`to_json`的实例）：
    * `'split'`：`JSON`是个类似字典的格式：`{index -> [index], columns -> [columns], data -> [values]}`
    * `'records'`：`JSON` 是个类似列表的格式：`[{column -> value}, ... , {column -> value}]`
    * `'index'`： `JSON`是个类似字典的格式`{index -> {column -> value}}`
    * `'columns'`：`JSON` 是个类似字典的格式`{column -> {index -> value}}`
    * `'values'`：`JSON`就是值的序列

注意：如果`type=='series'`，则允许的`'orients= {'split','records','index'}`，默认为`'index'`，且如果为`'index'`，则要求索引为唯一的。如果`type=='frame'`，则允许上所有的格式，默认为`'columns'`，且如果为`'index'/'columns'`，则要求`DataFrame.index`为唯一的；如果`'index'/'columns'/'records'`，则要求`DataFrame.columns`为唯一的

    * `typ`：一个字符串，指定将`JSON`转换为`Series/DataFrame`那一种。可以为`'series'`，'`frame'`
    * `dtype`：一个布尔值或者字典。如果为`True`，则自动推断数值类型。如果为`False`，则不推断类型。如果为字典，则给出了每一列的数值类型
    * `convert_axes`：一个布尔值，如果为`True`，则试图转换到合适的数值类型
    * `convert_dates`：一个布尔值，如果为`True`，则试图转换日期列为日期。它转换下面这些列名的列：列名以`'_at'/'_time'`结束、列名以`'timestamp'`开始、列名为`'mofified'/'date'`
    * `keep_default_dates`：一个布尔值。如果为`True`，则当转换日期列时，保留原列
    * `numpy`：一个布尔值，如果为`True`，则直接转换为`ndarray`
    * `precise_float`：一个布尔值，如果为`True`，则使用解析为更高精度的浮点数
    * `date_unit`：一个字符串。用于转换时间戳到日期。它提供时间戳的单位，如`'s'/'ms'`
    * `lines`：一个布尔值。如果为`True`，则读取文件的每一行作为一个`JSON` -`encoding`：一个字符串，指定编码方式

![read_json](../imgs/read_json.JPG)

2. 将`pandas`对象保存成`JSON`：

```
xxxxxxxxxx  Series/DataFrame.to_json(path_or_buf=None, orient=None, date_format='epoch',  double_precision=10, force_ascii=True, date_unit='ms', default_handler=None,   lines=False)
```

    * `path_or_buf`：指定保存的地方。如果为`None`，则该函数返回一个`StringIO`对象
    * `orient`参数：参考`read_json()`
    * `date_format`：一个字符串，指定日期转换格式。可以为`'epoch'`（从`1970-1-1`日以来的毫秒数）、`'iso'`
    * `double_precision`：一个整数，指定了浮点数的精度
    * `force_ascii`：一个布尔值，如果为`True`，则将`encoded string`转换成`ASCII`
    * `date_unit`：一个字符串，参考`read_json`
    * `default_handler`：一个可调用对象。用于处理当对象无法转换成`JSON`的情况。它只有一个参数，就是被转换的对象
    * `lines`：一个布尔值。如果`orient='records'`时，输出换行符。对其他格式则抛出异常

![to_json](../imgs/to_json.JPG)


### 3. 二进制文件

1. `pandas.read_pickle(path)`可以从`pickle`文件中读取数据，`path`为`pickle`文件的文件名。

`Series/DataFrame.to_pickle(path)`：将`Series/DataFrame`保存到`pickle`文件中，`path`为`pickle`文件的文件名。

![read_to_pickle](../imgs/read_to_pickle.JPG)


### 4. Excel 文件

1. `read_excel`读取`Excel`文件。需要用到第三方包`xlrd/xlwt`，前者读`excel`，后者写`excel`

```
xxxxxxxxxx  pandas.read_excel(io, sheetname=0, header=0, skiprows=None, skip_footer=0,  index_col=None, names=None, parse_cols=None, parse_dates=False, date_parser=None,  na_values=None, thousands=None, convert_float=True, has_index_names=None,  converters=None, true_values=None, false_values=None, engine=None,   squeeze=False, **kwds)
```

    * `io`：一个字符串，或者`file-like`对象。如果是个字符串，则必须是个`URL`（其中包含了协议名，如`http//,ftp//,file//`等）
    * `sheetname`：一个字符串或者整数，或者列表。它指定选取`Excel`文件中哪个`sheet`。字符串指定的是`sheet`名，整数指定的是`sheet`的位置（0为第一个`sheet`）
    * `engine`：一个字符串，指定了读写`Excel`的引擎。可以为：`io.excel.xlsx.writer`、`io.excel.xls.writer`、`io.excel.xlsm.writer`、
    * 其他参数参考`read_csv`

![read_excel](../imgs/read_excel.JPG)

2. 保存`DataFrame`到`Excel`文件：

```
xxxxxxxxxx  DataFrame.to_excel(excel_writer, sheet_name='Sheet1', na_rep='',   float_format=None, columns=None, header=True, index=True, index_label=None,   startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None,   inf_rep='inf', verbose=True)
```

    * `excel_writer`：一个字符串（文件名）或者一个`ExcelWriter`对象
    * `sheet_name`：一个字符串，指定`sheet`名
    * `na_rep`：一个字符串，代表`NaN`
    * `startrow/startcol`：指定了左上角的单元格的位置
    * `engine`：一个字符串，指定了读写`Excel`的引擎。可以为：`io.excel.xlsx.writer`、`io.excel.xls.writer`、`io.excel.xlsm.writer`、
    * `merge_cells`：一个布尔值。如果为`True`，则多级索引中，某些索引会合并单元格
    * `inf_rep`：一个字符串，只代表无穷大。

![to_excel](../imgs/to_excel.JPG)


### 5. HTML 表格

1. `read_html`可以将`HTML`中的`<table></table>`解析为一个`DataFrame`列表。

```
xxxxxxxxxx  pandas.read_html(io, match='.+', flavor=None, header=None, index_col=None,   skiprows=None, attrs=None, parse_dates=False, tupleize_cols=False,   thousands=', ', encoding=None, decimal='.', converters=None,   na_values=None, keep_default_na=True)
```

    * `io`：为一个字符串或者一个`file-like`对象。
    * `match`：一个字符串或者正则表达式。`HTML`中的`<table></table>`中，只要匹配这个正则表达式的表格都被处理。默认的为匹配任何非空的表格
    * `flavor`：一个字符串，指定了解析引擎。可以为`'bs4'`或者`'html5lib'`或者`'lxml'`
    * `attrs`：一个字典。它筛选出你要解析哪些表格
    * 其他参数参考`read_csv`

![read_html](../imgs/read_html.JPG)

2. 可以通过`DataFrame.to_html()`转换为`HTML`的表格：

```
xxxxxxxxxx  DataFrame.to_html(buf=None, columns=None, col_space=None, header=True,  index=True, na_rep='NaN', formatters=None, float_format=None,   sparsify=None, index_names=True, justify=None, bold_rows=True,   classes=None, escape=True, max_rows=None, max_cols=None, show_dimensions=False,   notebook=False, decimal='.', border=None)
```

    * `bold_rows`：一个布尔值。如果为`True`，则让`row label`加粗
    * `classes`：一个字符串或者列表或者元组，给出了`table`的`css class`
    * `escape`：一个布尔值，如果为`True`，则将字符`<>&`为安全的`HTML`字符
    * `max_rows`：一个整数，指定最大输出行数。默认显示全部的行
    * `decimal`：一个字符串，指定了小数点的格式
    * `border`：一个整数，给出了`border`属性的值。
    * `buf`：指定将`HTML`写到哪里，它是一个`StringIO-like`对象
    * `col_space`：一个整数，给出每一列最小宽度
    * `header`：一个布尔值，如果为`True`，则打印列名
    * `columns`：一个序列，指定要输出哪些列
    * `index`：一个布尔值，如果为`True`，则打印`index labels`
    * `formatters`：一个一元函数的列表，或者一元函数的字典。给出了每一列的转换成字符串的函数
    * `float_format`：一个一元函数，给出了浮点数转换成字符串的函数
    * `justify`：左对齐还是右对齐。可以为`'left'`/`'right'`

![to_html0](../imgs/to_html0.JPG) ![to_html1](../imgs/to_html1.JPG) ![to_html2](../imgs/to_html2.JPG)


### 6. SQL

1. `read_sql_table`从指定数据表中，提取你所需要的列。

```
xxxxxxxxxx  pandas.read_sql_table(table_name, con, schema=None, index_col=None,  coerce_float=True, parse_dates=None, columns=None, chunksize=None)
```

    * `table_name`：一个字符串，指定了数据库的表名

    * `con`：一个`SQLAlchemy conectable`或者一个`database string URI`，指定了连接对象它就是`SQLAlchemy`中的`Engine`对象。

    * `schema`：一个字符串，给出了`SQL schema`（在`mysql`中就是`database`）

    * `index_col`：一个字符串或者字符串列表，指定哪一列或者哪些列作为`index`

    * `coerce_float`：一个布尔值，如果为`True`，则试图转换结果到数值类型

    * `parse_dates`：一个列表或者字典。指定如何解析日期：

        * 列名的列表：这些列将被解析为日期
        * 字典`{col_name:format_str}`：给出了那些列被解析为日期，以及解析字符串
        * 字典`{col_name:arg dict}`：给出了哪些列被解析为日期，`arg dict`将传递给`pandas.to_datetime()`函数来解析日期

    * `columns`：一个列表，给出了将从`sql`中提取哪些列

    * `chunksize`：一个整数。如果给出了，则函数返回的是一个迭代器，每次迭代时，返回`chunksize`行的数据。


2. `read_sql_query`可以选择`select query`语句。因此你可以执行多表联合查询。

```
xxxxxxxxxx  pandas.read_sql_query(sql, con, index_col=None, coerce_float=True,  params=None, parse_dates=None, chunksize=None)
```

    * `sql`：一个`SQL`查询字符串，或者`SQLAlchemy Selectable`对象。
    * `params`：一个列表，元组或者字典。用于传递给`sql`查询语句。比如：`sql`为`uses %(name)s...`，因此`params`为`{'name':'xxxx'}`
    * 其他参数见`read_sql_table`

![read_sql](../imgs/read_sql.JPG)

3. `read_sql`是前两者的一个包装，它可以根据`sql`参数，自由地选择使用哪个方式。

```
xxxxxxxxxx  pandas.read_sql(sql, con, index_col=None, coerce_float=True, params=None,  parse_dates=None, columns=None, chunksize=None)
```

    * `sql`：一个数据表名，或者查询字符串，或者`SQLAlchemy Selectable`对象。如果为表名，则使用`read_sql_table`；如果为后两者，则使用`read_sql_query`

4. `pandas`对象的`.to_sql()`方法用于插入数据库。

```
xxxxxxxxxx  Series/DataFrame.to_sql(name, con, flavor=None, schema=None, if_exists='fail',  index=True, index_label=None, chunksize=None, dtype=None)
```

    * `name`：一个字符串，指定表名
    * `con`：一个`SQLAlchemy conectable`或者一个`database string URI`，指定了连接对象。它就是`SQLAlchemy`中的`Engine`对象。
    * `flavor`：被废弃的参数
    * `schema`：一个字符串，指定了`SQL schema`
    * `if_exists`：一个字符串，指定当数据表已存在时如何。可以为：
    * `'fail'`：什么都不做（即不存储数据）
    * `'replace'`：删除数据表，创建新表，然后插入数据
    * `'append'`：如果数据表不存在则创建数据表然后插入数据。入股数据表已存在，则追加数据
    * `index`：一个布尔值。如果为`True`，则将`index`作为一列数据插入数据库
    * `index_label`：`index`的存储名。如果`index=True`，且`index_label=None`，则使用`index.name`
    * `chunksize`：一个整数。 如果为`None`，则一次写入所有的记录。如果非空，则一次写入`chunksize`大小的记录
    * `dtype`：一个字典。给出了各列的存储类型。

![to_sql](../imgs/to_sql.JPG)

</body>