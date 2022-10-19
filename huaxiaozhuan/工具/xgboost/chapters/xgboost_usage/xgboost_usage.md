<body class="typora-export">
# Xgboost使用

## 一、安装

1. 安装步骤：

    * 下载源码，编译`libxgboost.so` （对于`windows` 则是 `libxgboost.dll` ）

    ```
git clone --recursive https://github.com/dmlc/xgboost# 对于 windows 用户，需要执行：#   git submodule init#   git submodule updatecd xgboostmake -j4
    ```

    如果需要支持`GPU`，则执行下面的编译步骤：

    ```
xxxxxxxxxxcd xgboostmkdir buildcd buildcmake .. -DUSE_CUDA=ONcd ..make -j4
    ```

    * 安装`python` 支持

    ```
xxxxxxxxxxcd python-packagesudo python setup.py install
    ```



## 二、调参

### 2.1 调参指导

1. 当出现过拟合时，有两类参数可以缓解：

    * 第一类参数：用于直接控制模型的复杂度。包括`max_depth,min_child_weight,gamma` 等参数
    * 第二类参数：用于增加随机性，从而使得模型在训练时对于噪音不敏感。包括`subsample,colsample_bytree`

你也可以直接减少步长`eta`，但是此时需要增加`num_round` 参数。

2. 当遇到数据不平衡时（如广告点击率预测任务），有两种方式提高模型的预测性能：

    * 如果你关心的是预测的`AUC`：

        * 你可以通过`scale_pos_weight` 参数来平衡正负样本的权重
        * 使用`AUC` 来评估

    * 如果你关心的是预测的正确率：

        * 你不能重新平衡正负样本
        * 设置`max_delta_step` 为一个有限的值（如 1），从而有助于收敛



### 2.2 参数

#### 2.2.1. 通用参数

1. `booster`： 指定了使用那一种`booster`。可选的值为：

    * `'gbtree'`： 表示采用`xgboost` (默认值)

    * `'gblinear'`： 表示采用线性模型。

    `'gblinear'` 使用带`l1,l2` 正则化的线性回归模型作为基学习器。因为`boost` 算法是一个线性叠加的过程，而线性回归模型也是一个线性叠加的过程。因此叠加的最终结果就是一个整体的线性模型，`xgboost` 最后会获得这个线性模型的系数。

    * `'dart'`： 表示采用`dart booster`


2. `silent`： 如果为 0（默认值），则表示打印运行时的信息；如果为 1， 则表示`silent mode`（ 不打印这些信息）

3. `nthread`： 指定了运行时的并行线程的数量。如果未设定该参数，则默认值为可用的最大线程数。

4. `num_pbuffer`： 指定了`prediction buffer` 的大小。通常设定为训练样本的数量。该参数由`xgboost` 自动设定，无需用户指定。

该`buffer` 用于保存上一轮`boostring step` 的预测结果。

5. `num_feature`： 样本的特征数量。通常设定为特征的最大维数。该参数由`xgboost` 自动设定，无需用户指定。


#### 2.2.2 tree booster 参数

针对`tree booster` 的参数（适用于`booster=gbtree,dart`) ：

1. `eta`： 也称作学习率。默认为 0.3 。范围为 `[0,1]`

2. `gamma`： 也称作最小划分损失`min_split_loss`。 它刻画的是：对于一个叶子节点，当对它采取划分之后，损失函数的降低值的阈值。

    * 如果大于该阈值，则该叶子节点值得继续划分
    * 如果小于该阈值，则该叶子节点不值得继续划分

该值越大，则算法越保守（尽可能的少划分）。默认值为 0

3. `max_depth`： 每棵子树的最大深度。其取值范围为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-42-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.577ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -806.1 2500.7 1109.7" width="5.808ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M118 -250V750H255V710H158V-210H255V-250H118Z" id="E42-MJMAIN-5B" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E42-MJMAIN-30" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E42-MJMAIN-2C" stroke-width="0"></path><path d="M55 217Q55 305 111 373T254 442Q342 442 419 381Q457 350 493 303L507 284L514 294Q618 442 747 442Q833 442 888 374T944 214Q944 128 889 59T743 -11Q657 -11 580 50Q542 81 506 128L492 147L485 137Q381 -11 252 -11Q166 -11 111 57T55 217ZM907 217Q907 285 869 341T761 397Q740 397 720 392T682 378T648 359T619 335T594 310T574 285T559 263T548 246L543 238L574 198Q605 158 622 138T664 94T714 61T765 51Q827 51 867 100T907 217ZM92 214Q92 145 131 89T239 33Q357 33 456 193L425 233Q364 312 334 337Q285 380 233 380Q171 380 132 331T92 214Z" id="E42-MJMAIN-221E" stroke-width="0"></path><path d="M22 710V750H159V-250H22V-210H119V710H22Z" id="E42-MJMAIN-5D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E42-MJMAIN-5B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="278" xlink:href="#E42-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="778" xlink:href="#E42-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1222" xlink:href="#E42-MJMAIN-221E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2222" xlink:href="#E42-MJMAIN-5D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-42" type="math/tex">[0,\infty]</script>， 0 表示没有限制，默认值为6。

该值越大，则子树越复杂；值越小，则子树越简单。

4. `min_child_weight`： 子节点的权重阈值。它刻画的是：对于一个叶子节点，当对它采取划分之后，它的所有子节点的权重之和的阈值。

    * 如果它的所有子节点的权重之和大于该阈值，则该叶子节点值得继续划分
    * 如果它的所有子节点的权重之和小于该阈值，则该叶子节点不值得继续划分

所谓的权重：

    * 对于线性模型(`booster=gblinear`)，权重就是：叶子节点包含的样本数量。 因此该参数就是每个节点包含的最少样本数量。
    * 对于树模型（`booster=gbtree,dart`），权重就是：叶子节点包含样本的所有二阶偏导数之和。

该值越大，则算法越保守（尽可能的少划分）。默认值为 1

5. `max_delta_step`： 每棵树的权重估计时的最大`delta step`。取值范围为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-42-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.577ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -806.1 2500.7 1109.7" width="5.808ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M118 -250V750H255V710H158V-210H255V-250H118Z" id="E42-MJMAIN-5B" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E42-MJMAIN-30" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E42-MJMAIN-2C" stroke-width="0"></path><path d="M55 217Q55 305 111 373T254 442Q342 442 419 381Q457 350 493 303L507 284L514 294Q618 442 747 442Q833 442 888 374T944 214Q944 128 889 59T743 -11Q657 -11 580 50Q542 81 506 128L492 147L485 137Q381 -11 252 -11Q166 -11 111 57T55 217ZM907 217Q907 285 869 341T761 397Q740 397 720 392T682 378T648 359T619 335T594 310T574 285T559 263T548 246L543 238L574 198Q605 158 622 138T664 94T714 61T765 51Q827 51 867 100T907 217ZM92 214Q92 145 131 89T239 33Q357 33 456 193L425 233Q364 312 334 337Q285 380 233 380Q171 380 132 331T92 214Z" id="E42-MJMAIN-221E" stroke-width="0"></path><path d="M22 710V750H159V-250H22V-210H119V710H22Z" id="E42-MJMAIN-5D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E42-MJMAIN-5B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="278" xlink:href="#E42-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="778" xlink:href="#E42-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1222" xlink:href="#E42-MJMAIN-221E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2222" xlink:href="#E42-MJMAIN-5D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-42" type="math/tex">[0,\infty]</script>，0 表示没有限制，默认值为 0 。

通常该参数不需要设置，但是在逻辑回归中，如果类别比例非常不平衡时，该参数可能有帮助。

6. `subsample`： 对训练样本的采样比例。取值范围为 `(0,1]`，默认值为 1 。

如果为 `0.5`， 表示随机使用一半的训练样本来训练子树。它有助于缓解过拟合。

7. `colsample_bytree`： 构建子树时，对特征的采样比例。取值范围为 `(0,1]`， 默认值为 1。

如果为 `0.5`， 表示随机使用一半的特征来训练子树。它有助于缓解过拟合。

8. `colsample_bylevel`： 寻找划分点时，对特征的采样比例。取值范围为 `(0,1]`， 默认值为 1。

如果为 `0.5`， 表示随机使用一半的特征来寻找最佳划分点。它有助于缓解过拟合。

9. `lambda`： `L2` 正则化系数（基于`weights`的正则化），默认为 1。 该值越大则模型越简单

10. `alpha`： `L1` 正则化系数（基于`weights`的正则化），默认为 0。 该值越大则模型越简单

11. `tree_method`： 指定了构建树的算法，可以为下列的值：（默认为`'auto'` )

    * `'auto'`： 使用启发式算法来选择一个更快的`tree_method`：

        * 对于小的和中等的训练集，使用`exact greedy` 算法分裂节点
        * 对于非常大的训练集，使用近似算法分裂节点
        * 旧版本在单机上总是使用`exact greedy` 分裂节点

    * `'exact'`： 使用`exact greedy` 算法分裂节点

    * `'approx'`： 使用近似算法分裂节点

    * `'hist'`： 使用`histogram` 优化的近似算法分裂节点（比如使用了`bin cacheing` 优化）

    * `'gpu_exact'`： 基于`GPU` 的`exact greedy` 算法分裂节点

    * `'gpu_hist'`： 基于`GPU` 的`histogram` 算法分裂节点


注意：分布式，以及外存版本的算法只支持 `'approx','hist','gpu_hist'` 等近似算法

12. `sketch_eps`： 指定了分桶的步长。其取值范围为 `(0,1)`， 默认值为 0.03 。

它仅仅用于 `tree_medhod='approx'`。

它会产生大约<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-5-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.628ex" role="img" style="vertical-align: -1.405ex;" viewbox="0 -956.9 3647.3 1562" width="8.471ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E5-MJMAIN-31" stroke-width="0"></path><path d="M295 316Q295 356 268 385T190 414Q154 414 128 401Q98 382 98 349Q97 344 98 336T114 312T157 287Q175 282 201 278T245 269T277 256Q294 248 310 236T342 195T359 133Q359 71 321 31T198 -10H190Q138 -10 94 26L86 19L77 10Q71 4 65 -1L54 -11H46H42Q39 -11 33 -5V74V132Q33 153 35 157T45 162H54Q66 162 70 158T75 146T82 119T101 77Q136 26 198 26Q295 26 295 104Q295 133 277 151Q257 175 194 187T111 210Q75 227 54 256T33 318Q33 357 50 384T93 424T143 442T187 447H198Q238 447 268 432L283 424L292 431Q302 440 314 448H322H326Q329 448 335 442V310L329 304H301Q295 310 295 316Z" id="E5-MJMAIN-73" stroke-width="0"></path><path d="M36 46H50Q89 46 97 60V68Q97 77 97 91T97 124T98 167T98 217T98 272T98 329Q98 366 98 407T98 482T98 542T97 586T97 603Q94 622 83 628T38 637H20V660Q20 683 22 683L32 684Q42 685 61 686T98 688Q115 689 135 690T165 693T176 694H179V463L180 233L240 287Q300 341 304 347Q310 356 310 364Q310 383 289 385H284V431H293Q308 428 412 428Q475 428 484 431H489V385H476Q407 380 360 341Q286 278 286 274Q286 273 349 181T420 79Q434 60 451 53T500 46H511V0H505Q496 3 418 3Q322 3 307 0H299V46H306Q330 48 330 65Q330 72 326 79Q323 84 276 153T228 222L176 176V120V84Q176 65 178 59T189 49Q210 46 238 46H254V0H246Q231 3 137 3T28 0H20V46H36Z" id="E5-MJMAIN-6B" stroke-width="0"></path><path d="M28 218Q28 273 48 318T98 391T163 433T229 448Q282 448 320 430T378 380T406 316T415 245Q415 238 408 231H126V216Q126 68 226 36Q246 30 270 30Q312 30 342 62Q359 79 369 104L379 128Q382 131 395 131H398Q415 131 415 121Q415 117 412 108Q393 53 349 21T250 -11Q155 -11 92 58T28 218ZM333 275Q322 403 238 411H236Q228 411 220 410T195 402T166 381T143 340T127 274V267H333V275Z" id="E5-MJMAIN-65" stroke-width="0"></path><path d="M27 422Q80 426 109 478T141 600V615H181V431H316V385H181V241Q182 116 182 100T189 68Q203 29 238 29Q282 29 292 100Q293 108 293 146V181H333V146V134Q333 57 291 17Q264 -10 221 -10Q187 -10 162 2T124 33T105 68T98 100Q97 107 97 248V385H18V422H27Z" id="E5-MJMAIN-74" stroke-width="0"></path><path d="M370 305T349 305T313 320T297 358Q297 381 312 396Q317 401 317 402T307 404Q281 408 258 408Q209 408 178 376Q131 329 131 219Q131 137 162 90Q203 29 272 29Q313 29 338 55T374 117Q376 125 379 127T395 129H409Q415 123 415 120Q415 116 411 104T395 71T366 33T318 2T249 -11Q163 -11 99 53T34 214Q34 318 99 383T250 448T370 421T404 357Q404 334 387 320Z" id="E5-MJMAIN-63" stroke-width="0"></path><path d="M41 46H55Q94 46 102 60V68Q102 77 102 91T102 124T102 167T103 217T103 272T103 329Q103 366 103 407T103 482T102 542T102 586T102 603Q99 622 88 628T43 637H25V660Q25 683 27 683L37 684Q47 685 66 686T103 688Q120 689 140 690T170 693T181 694H184V367Q244 442 328 442Q451 442 463 329Q464 322 464 190V104Q464 66 466 59T477 49Q498 46 526 46H542V0H534L510 1Q487 2 460 2T422 3Q319 3 310 0H302V46H318Q379 46 379 62Q380 64 380 200Q379 335 378 343Q372 371 358 385T334 402T308 404Q263 404 229 370Q202 343 195 315T187 232V168V108Q187 78 188 68T191 55T200 49Q221 46 249 46H265V0H257L234 1Q210 2 183 2T145 3Q42 3 33 0H25V46H41Z" id="E5-MJMAIN-68" stroke-width="0"></path><path d="M0 -62V-25H499V-62H0Z" id="E5-MJMAIN-5F" stroke-width="0"></path><path d="M36 -148H50Q89 -148 97 -134V-126Q97 -119 97 -107T97 -77T98 -38T98 6T98 55T98 106Q98 140 98 177T98 243T98 296T97 335T97 351Q94 370 83 376T38 385H20V408Q20 431 22 431L32 432Q42 433 61 434T98 436Q115 437 135 438T165 441T176 442H179V416L180 390L188 397Q247 441 326 441Q407 441 464 377T522 216Q522 115 457 52T310 -11Q242 -11 190 33L182 40V-45V-101Q182 -128 184 -134T195 -145Q216 -148 244 -148H260V-194H252L228 -193Q205 -192 178 -192T140 -191Q37 -191 28 -194H20V-148H36ZM424 218Q424 292 390 347T305 402Q234 402 182 337V98Q222 26 294 26Q345 26 384 80T424 218Z" id="E5-MJMAIN-70" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="3407" x="0" y="220"></rect><use transform="scale(0.707)" x="2159" xlink:href="#E5-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-396)"><use transform="scale(0.707)" xlink:href="#E5-MJMAIN-73" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use transform="scale(0.707)" x="394" xlink:href="#E5-MJMAIN-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="922" xlink:href="#E5-MJMAIN-65" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1366" xlink:href="#E5-MJMAIN-74" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1755" xlink:href="#E5-MJMAIN-63" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2199" xlink:href="#E5-MJMAIN-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2755" xlink:href="#E5-MJMAIN-5F" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="3255" xlink:href="#E5-MJMAIN-65" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="3699" xlink:href="#E5-MJMAIN-70" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="4255" xlink:href="#E5-MJMAIN-73" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></svg></span><script id="MathJax-Element-5" type="math/tex">\frac {1}{\text{sketch_eps}}</script>个分桶。它并不会显示的分桶，而是会每隔 `sketch_pes` 个单位（一个单位表示最大值减去最小值的区间）统计一次。

用户通常不需要调整该参数。

13. `scale_pos_weight`： 用于调整正负样本的权重，常用于类别不平衡的分类问题。默认为 1。

一个典型的参数值为： `负样本数量/正样本数量`

14. `updater`： 它是一个逗号分隔的字符串，指定了一组需要运行的`tree updaters`，用于构建和修正决策树。默认为 `'grow_colmaker,prune'` 。

该参数通常是自动设定的，无需用户指定。但是用户也可以显式的指定。

15. `refresh_leaf`： 它是一个`updater plugin`。 如果为 `true`，则树节点的统计数据和树的叶节点数据都被更新；否则只有树节点的统计数据被更新。默认为 1

16. `process_type`： 指定要执行的处理过程（如：创建子树、更新子树）。该参数通常是自动设定的，无需用户指定。

17. `grow_policy`： 用于指定子树的生长策略。仅仅支持`tree_method='hist'`。 有两种策略：

    * `'depthwise'`： 优先拆分那些靠近根部的子节点。默认为`'depthwise'`
    * `'lossguide'`： 优先拆分导致损失函数降低最快的子节点

18. `max_leaves`： 最多的叶子节点。如果为0，则没有限制。默认值为 0 。

该参数仅仅和`grow_policy='lossguide'` 关系较大。

19. `max_bin`： 指定了最大的分桶数量。默认值为 256 。

该参数仅仅当 `tree_method='hist','gpu_hist'` 时有效。

20. `predictor`： 指定预测器的算法，默认为`'cpu_predictor'`。可以为：

    * `'cpu_predictor'`： 使用`CPU` 来预测
    * `'gpu_predictor'`： 使用`GPU` 来预测。对于`tree_method='gpu_exact,gpu_hist'`， `'gpu_redictor'` 是默认值。


#### 2.2.3 dart booster 参数

1. `sample_type`： 它指定了丢弃时的策略：

    * `'uniform'`： 随机丢弃子树（默认值）
    * `'weighted'`： 根据权重的比例来丢弃子树

2. `normaliz_type` ：它指定了归一化策略：

    * `'tree'`： 新的子树将被缩放为：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-6-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.395ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -956.9 1913.5 1461.5" width="4.444ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E6-MJMAIN-31" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E6-MJMATHI-4B" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E6-MJMAIN-2B" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E6-MJMATHI-3BD" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="1673" x="0" y="220"></rect><use transform="scale(0.707)" x="933" xlink:href="#E6-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-388)"><use transform="scale(0.707)" x="0" xlink:href="#E6-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="889" xlink:href="#E6-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1667" xlink:href="#E6-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></svg></span><script id="MathJax-Element-6" type="math/tex">\frac{1}{K+\nu}</script>； 被丢弃的子树被缩放为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-7-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.044ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -806.1 1913.5 1310.7" width="4.444ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E7-MJMATHI-3BD" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E7-MJMATHI-4B" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E7-MJMAIN-2B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="1673" x="0" y="220"></rect><use transform="scale(0.707)" x="918" xlink:href="#E7-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="573"></use><g transform="translate(60,-388)"><use transform="scale(0.707)" x="0" xlink:href="#E7-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="889" xlink:href="#E7-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1667" xlink:href="#E7-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></svg></span><script id="MathJax-Element-7" type="math/tex">\frac{\nu}{K+\nu}</script>。其中<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-12-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.41ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -504.6 530 607.1" width="1.231ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E12-MJMATHI-3BD" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E12-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-12" type="math/tex">\nu</script>为学习率，<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-17-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.877ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -755.9 889 808.1" width="2.065ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E17-MJMATHI-4B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E17-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-17" type="math/tex">K</script>为被丢弃的子树的数量
    * `'forest'`：新的子树将被缩放为：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-10-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.395ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -956.9 1638.4 1461.5" width="3.805ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E10-MJMAIN-31" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E10-MJMAIN-2B" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E10-MJMATHI-3BD" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="1398" x="0" y="220"></rect><use transform="scale(0.707)" x="738" xlink:href="#E10-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-376)"><use transform="scale(0.707)" x="0" xlink:href="#E10-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="500" xlink:href="#E10-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1278" xlink:href="#E10-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></svg></span><script id="MathJax-Element-10" type="math/tex">\frac{1}{1+\nu}</script>； 被丢弃的子树被缩放为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-11-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.044ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -806.1 1638.4 1310.7" width="3.805ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E11-MJMATHI-3BD" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E11-MJMAIN-31" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E11-MJMAIN-2B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="1398" x="0" y="220"></rect><use transform="scale(0.707)" x="723" xlink:href="#E11-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="573"></use><g transform="translate(60,-376)"><use transform="scale(0.707)" x="0" xlink:href="#E11-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="500" xlink:href="#E11-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1278" xlink:href="#E11-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></svg></span><script id="MathJax-Element-11" type="math/tex">\frac{\nu}{1+\nu}</script>。其中<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-12-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.41ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -504.6 530 607.1" width="1.231ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E12-MJMATHI-3BD" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E12-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-12" type="math/tex">\nu</script>为学习率

3. `rate_drop`： `dropout rate`，指定了当前要丢弃的子树占当前所有子树的比例。范围为`[0.0,1.0]`， 默认为 `0.0`。

4. `one_drop`： 如果该参数为`true`，则在`dropout` 期间，至少有一个子树总是被丢弃。默认为 0 。

5. `skip_drop`： 它指定了不执行 `dropout` 的概率，其范围是`[0.0,1.0]`， 默认为 0.0 。

如果跳过了`dropout`，则新的子树直接加入到模型中（和`xgboost` 相同的方式）


#### 2.2.4 linear booster 参数

1. `lambda`： `L2` 正则化系数（基于`weights` 的正则化），默认为 0。 该值越大则模型越简单

2. `alpha`： `L1` 正则化系数（基于`weights`的正则化），默认为 0。 该值越大则模型越简单

3. `lambda_bias`： `L2` 正则化系数（ 基于`bias` 的正则化），默认为 0.

没有基于`bias` 的 `L1` 正则化，因为它不重要。


#### 2.4.5 tweedie regression 参数：

1. `weedie_variance_power`： 指定了`tweedie` 分布的方差。取值范围为 `(1,2)` ，默认为 1.5 。

越接近1，则越接近泊松分布；越接近2，则越接近 `gamma` 分布。


#### 2.4.6 学习任务参数

1. `objective`：指定任务类型，默认为`'reg:linear'` 。

    * `'reg:linear'`： 线性回归模型。它的模型输出是连续值

    * `'reg:logistic'`： 逻辑回归模型。它的模型输出是连续值，位于区间`[0,1]` 。

    * `'binary:logistic'`： 二分类的逻辑回归模型，它的模型输出是连续值，位于区间`[0,1]` ，表示取正负类别的概率。

    它和`'reg:logistic'` 几乎完全相同，除了有一点不同：

        * `'reg:logistic'` 的默认`evaluation metric` 是 `rmse` 。
        * `'binary:logistic'` 的默认`evaluation metric` 是 `error`

    * `'binary:logitraw'`： 二分类的逻辑回归模型，输出为分数值（在`logistic` 转换之前的值）

    * `'count:poisson'`： 对 `count data` 的 `poisson regression`， 输出为泊松分布的均值。

    * `'multi:softmax'`： 基于`softmax` 的多分类模型。此时你需要设定`num_class` 参数来指定类别数量。

    * `'multi:softprob'`： 基于`softmax` 的多分类模型，但是它的输出是一个矩阵：`ndata*nclass`，给出了每个样本属于每个类别的概率。

    * `'rank:pairwise'`： 排序模型（优化目标为最小化`pairwise loss` ）

    * `'reg:gamma'`： `gamma regression`， 输出为伽马分布的均值。

    * `'reg:tweedie'`： `'tweedie regression'`。


2. `base_score`： 所有样本的初始预测分，它用于设定一个初始的、全局的`bias`。 默认为 0.5 。

    * 当迭代的数量足够大时，该参数没有什么影响

3. `eval_metric`： 用于验证集的评估指标。其默认值和`objective` 参数高度相关。

回归问题的默认值是`rmse`； 分类问题的默认值是`error`； 排序问题的默认值是 `mean average precision` 。

你可以指定多个`evaluation metrics`。

> > 

> 如果有多个验证集，以及多个评估指标.则： 使用最后一个验证集的最后一个评估指标来做早停。但是还是会计算出所有的验证集的所有评估指标。



    * `'rmse'`： 均方误差。

    * `'mae'`： 绝对值平均误差

    * `'logloss'`： 负的对数似然函数

    * `'error'`： 二分类的错误率。它计算的是：`预测错误的样本数/所有样本数`

    所谓的预测是：正类概率大于0.5的样本预测为正类；否则为负类（即阈值为 0.5 ）

    * `'error@t'`： 二分类的错误率。但是它的阈值不再是 0.5， 而是由字符串`t` 给出（它是一个数值转换的字符串）

    * `'merror'`： 多类分类的错误率。它计算的是：`预测错误的样本数/所有样本数`

    * `'mlogloss'`： 多类分类的负对数似然函数

    * `'auc'`： `AUC` 得分

    * `'ndcg'`： `Normalized Discounted Cumulative Gain` 得分

    * `'map'`： `Mean average precision` 得分

    * `'ndcg@n','map@n'`： `n` 为一个整数，用于切分验证集的`top` 样本来求值。

    * `'ndcg-','map-','ndcg@n-','map@n-'`： NDCG and MAP will evaluate the score of a list without any positive samples as 1. By adding “-” in the evaluation metric XGBoost will evaluate these score as 0 to be consistent under some conditions. training repeatedly

    * `poisson-nloglik`： 对于泊松回归，使用负的对数似然

    * `gamma-nloglik`： 对于伽马回归，使用负的对数似然

    * `gamma-deviance`： 对于伽马回归，使用残差的方差

    * `tweedie-nloglik`： 对于`tweedie` 回归，使用负的对数似然


4. `seed`： 随机数种子，默认为 0 。


## 三、外存计算

1. 对于`external-memory` 和 `in-memory` 计算，二者几乎没有区别。除了在文件名上有所不同。

    * `in-memory` 的文件名为：`filename`

    * `external-memory` 的文件名为：`filename#cacheprefix`。其中：

        * `filename`：是你想加载的数据集 （ `libsvm` 文件 ） 的路径名

        >         > 

        > 当前只支持导入`libsvm` 格式的文件



        * `cacheprefix`： 指定的`cache` 文件的路径名。`xgboost` 将使用它来做`external memory cache` 。


    如：

    ```
xxxxxxxxxxdtrain = xgb.DMatrix('../data/my_data.txt.train#train_cache.cache')
    ```

    此时你会发现在`my_data.txt` 所在的位置会由`xgboost` 创建一个`my_cache.cache` 文件。


2. 推荐将`nthread` 设置为真实`CPU` 的数量。

    * 现代的`CPU`都支持超线程，如 `4核8线程`。此时`nthread` 设置为 `4` 而不是 `8`

3. 对于分布式计算，外存计算时文件名的设定方法也相同：

```
xxxxxxxxxxdata = "hdfs:///path-to-data/my_data.txt.train#train_cache.cache"
```


## 四、 GPU计算

1. `xgboost` 支持使用`gpu` 计算，前提是安装时开启了`GPU` 支持

2. 要想使用`GPU` 训练，需要指定`tree_method` 参数为下列的值：

    * `'gpu_exact'`： 标准的`xgboost` 算法。它会对每个分裂点进行精确的搜索。相对于`'gpu_hist'`，它的训练速度更慢，占用更多内存
    * `'gpu_hist'`：使用`xgboost histogram` 近似算法。它的训练速度更快，占用更少内存

3. 当`tree_method` 为`'gpu_exact'，'gpu_hist'` 时，模型的`predict` 默认采用`GPU` 加速。

你可以通过设置`predictor` 参数来指定`predict` 时的计算设备：

    * `'cpu_predictor'`： 使用`CPU` 来执行模型预测
    * `'gpu_predictor'`： 使用`GPU` 来执行模型预测

4. 多`GPU` 可以通过`grow_gpu_hist` 参数和 `n_gpus` 参数配合使用。

    * 可以通过`gpu_id` 参数来选择设备，默认为 0 。如果非0，则`GPU` 的编号规则为 `mod(gpu_id + i) % n_visible_devices for i in 0~n_gpus-1`<br></br>
    * 如果`n_gpus` 设置为 `-1`，则所有的`GPU` 都被使用。它默认为 1 。

5. 多`GPU` 不一定比单个`GPU` 更快，因为`PCI`总线的带宽限制，数据传输速度可能成为瓶颈。

6. GPU 计算支持的参数：
<figure><table><thead><tr><th style="text-align:center;">parameter</th><th style="text-align:center;">gpu_exact</th><th style="text-align:center;">gpu_hist</th></tr></thead><tbody><tr><td style="text-align:center;">subsample</td><td style="text-align:center;">✘</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">colsample_bytree</td><td style="text-align:center;">✘</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">colsample_bylevel</td><td style="text-align:center;">✘</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">max_bin</td><td style="text-align:center;">✘</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">gpu_id</td><td style="text-align:center;">✔</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">n_gpus</td><td style="text-align:center;">✘</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">predictor</td><td style="text-align:center;">✔</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">grow_policy</td><td style="text-align:center;">✘</td><td style="text-align:center;">✔</td></tr><tr><td style="text-align:center;">monotone_constraints</td><td style="text-align:center;">✘</td><td style="text-align:center;">✔</td></tr></tbody></table></figure>

## 五、单调约束

1. 在模型中可能会有一些单调的约束：当<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-13-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.461ex" role="img" style="vertical-align: -0.472ex;" viewbox="0 -856.4 2772 1059.4" width="6.438ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z" id="E13-MJMATHI-78" stroke-width="0"></path><path d="M674 636Q682 636 688 630T694 615T687 601Q686 600 417 472L151 346L399 228Q687 92 691 87Q694 81 694 76Q694 58 676 56H670L382 192Q92 329 90 331Q83 336 83 348Q84 359 96 365Q104 369 382 500T665 634Q669 636 674 636ZM84 -118Q84 -108 99 -98H678Q694 -104 694 -118Q694 -130 679 -138H98Q84 -131 84 -118Z" id="E13-MJMAIN-2264" stroke-width="0"></path><path d="M79 43Q73 43 52 49T30 61Q30 68 85 293T146 528Q161 560 198 560Q218 560 240 545T262 501Q262 496 260 486Q259 479 173 263T84 45T79 43Z" id="E13-MJMAIN-2032" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E13-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="849" xlink:href="#E13-MJMAIN-2264" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1905,0)"><use x="0" xlink:href="#E13-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E13-MJMAIN-2032" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g></g></svg></span><script id="MathJax-Element-13" type="math/tex">x \le x^\prime</script>时：

    * 若<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-14-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.694ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -856.4 21524.1 1160" width="49.992ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z" id="E14-MJMATHI-66" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E14-MJMAIN-28" stroke-width="0"></path><path d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z" id="E14-MJMATHI-78" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E14-MJMAIN-31" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E14-MJMAIN-2C" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E14-MJMAIN-32" stroke-width="0"></path><path d="M78 250Q78 274 95 292T138 310Q162 310 180 294T199 251Q199 226 182 208T139 190T96 207T78 250ZM525 250Q525 274 542 292T585 310Q609 310 627 294T646 251Q646 226 629 208T586 190T543 207T525 250ZM972 250Q972 274 989 292T1032 310Q1056 310 1074 294T1093 251Q1093 226 1076 208T1033 190T990 207T972 250Z" id="E14-MJMAIN-22EF" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T89 425T135 442Q171 442 195 424T225 390T231 369Q231 367 232 367L243 378Q304 442 382 442Q436 442 469 415T503 336T465 179T427 52Q427 26 444 26Q450 26 453 27Q482 32 505 65T540 145Q542 153 560 153Q580 153 580 145Q580 144 576 130Q568 101 554 73T508 17T439 -10Q392 -10 371 17T350 73Q350 92 386 193T423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 180T152 343Q153 348 153 366Q153 405 129 405Q91 405 66 305Q60 285 60 284Q58 278 41 278H27Q21 284 21 287Z" id="E14-MJMATHI-6E" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E14-MJMAIN-29" stroke-width="0"></path><path d="M674 636Q682 636 688 630T694 615T687 601Q686 600 417 472L151 346L399 228Q687 92 691 87Q694 81 694 76Q694 58 676 56H670L382 192Q92 329 90 331Q83 336 83 348Q84 359 96 365Q104 369 382 500T665 634Q669 636 674 636ZM84 -118Q84 -108 99 -98H678Q694 -104 694 -118Q694 -130 679 -138H98Q84 -131 84 -118Z" id="E14-MJMAIN-2264" stroke-width="0"></path><path d="M79 43Q73 43 52 49T30 61Q30 68 85 293T146 528Q161 560 198 560Q218 560 240 545T262 501Q262 496 260 486Q259 479 173 263T84 45T79 43Z" id="E14-MJMAIN-2032" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E14-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="550" xlink:href="#E14-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(939,0)"><use x="0" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E14-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="1964" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2409,0)"><use x="0" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E14-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="3434" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3879" xlink:href="#E14-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5218" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5662" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6234" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6679" xlink:href="#E14-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8018" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(8462,0)"><use x="0" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E14-MJMATHI-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="9559" xlink:href="#E14-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10225" xlink:href="#E14-MJMAIN-2264" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11281" xlink:href="#E14-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11831" xlink:href="#E14-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(12220,0)"><use x="0" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E14-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="13246" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(13690,0)"><use x="0" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E14-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="14716" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="15161" xlink:href="#E14-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="16499" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(16944,0)"><use x="0" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E14-MJMAIN-2032" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><use x="17810" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="18255" xlink:href="#E14-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="19594" xlink:href="#E14-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(20038,0)"><use x="0" xlink:href="#E14-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E14-MJMATHI-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="21135" xlink:href="#E14-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-14" type="math/tex">f(x_1,x_2,\cdots,x,\cdots,x_{n}) \le f(x_1,x_2,\cdots,x^\prime,\cdots,x_{n})</script>，则称该约束为单调递增约束
    * 若<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-15-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.694ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -856.4 21524.1 1160" width="49.992ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z" id="E15-MJMATHI-66" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E15-MJMAIN-28" stroke-width="0"></path><path d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z" id="E15-MJMATHI-78" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E15-MJMAIN-31" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E15-MJMAIN-2C" stroke-width="0"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" id="E15-MJMAIN-32" stroke-width="0"></path><path d="M78 250Q78 274 95 292T138 310Q162 310 180 294T199 251Q199 226 182 208T139 190T96 207T78 250ZM525 250Q525 274 542 292T585 310Q609 310 627 294T646 251Q646 226 629 208T586 190T543 207T525 250ZM972 250Q972 274 989 292T1032 310Q1056 310 1074 294T1093 251Q1093 226 1076 208T1033 190T990 207T972 250Z" id="E15-MJMAIN-22EF" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T89 425T135 442Q171 442 195 424T225 390T231 369Q231 367 232 367L243 378Q304 442 382 442Q436 442 469 415T503 336T465 179T427 52Q427 26 444 26Q450 26 453 27Q482 32 505 65T540 145Q542 153 560 153Q580 153 580 145Q580 144 576 130Q568 101 554 73T508 17T439 -10Q392 -10 371 17T350 73Q350 92 386 193T423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 180T152 343Q153 348 153 366Q153 405 129 405Q91 405 66 305Q60 285 60 284Q58 278 41 278H27Q21 284 21 287Z" id="E15-MJMATHI-6E" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E15-MJMAIN-29" stroke-width="0"></path><path d="M83 616Q83 624 89 630T99 636Q107 636 253 568T543 431T687 361Q694 356 694 346T687 331Q685 329 395 192L107 56H101Q83 58 83 76Q83 77 83 79Q82 86 98 95Q117 105 248 167Q326 204 378 228L626 346L360 472Q291 505 200 548Q112 589 98 597T83 616ZM84 -118Q84 -108 99 -98H678Q694 -104 694 -118Q694 -130 679 -138H98Q84 -131 84 -118Z" id="E15-MJMAIN-2265" stroke-width="0"></path><path d="M79 43Q73 43 52 49T30 61Q30 68 85 293T146 528Q161 560 198 560Q218 560 240 545T262 501Q262 496 260 486Q259 479 173 263T84 45T79 43Z" id="E15-MJMAIN-2032" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E15-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="550" xlink:href="#E15-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(939,0)"><use x="0" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E15-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="1964" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2409,0)"><use x="0" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E15-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="3434" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="3879" xlink:href="#E15-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5218" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5662" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6234" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6679" xlink:href="#E15-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="8018" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(8462,0)"><use x="0" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E15-MJMATHI-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="9559" xlink:href="#E15-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10225" xlink:href="#E15-MJMAIN-2265" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11281" xlink:href="#E15-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="11831" xlink:href="#E15-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(12220,0)"><use x="0" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E15-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="13246" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(13690,0)"><use x="0" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E15-MJMAIN-32" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="14716" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="15161" xlink:href="#E15-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="16499" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(16944,0)"><use x="0" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E15-MJMAIN-2032" xmlns:xlink="http://www.w3.org/1999/xlink" y="513"></use></g><use x="17810" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="18255" xlink:href="#E15-MJMAIN-22EF" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="19594" xlink:href="#E15-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(20038,0)"><use x="0" xlink:href="#E15-MJMATHI-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="808" xlink:href="#E15-MJMATHI-6E" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="21135" xlink:href="#E15-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-15" type="math/tex">f(x_1,x_2,\cdots,x,\cdots,x_{n}) \ge f(x_1,x_2,\cdots,x^\prime,\cdots,x_{n})</script>，则称该约束为单调递减约束

2. 如果想在`xgboost` 中添加单调约束，则可以设置`monotone_constraints` 参数。

假设样本有 2 个特征，则：

    * `params['monotone_constraints'] = "(1,-1)"` ：表示第一个特征是单调递增；第二个特征是单调递减
    * `params['monotone_constraints'] = "(1,0)"` ：表示第一个特征是单调递增；第二个特征没有约束
    * `params['monotone_constraints'] = "(1,1)"` ：表示第一个特征是单调递增；第二个特征是单调递增

> > 

> 右侧的 `1` 表示单调递增约束；`0` 表示无约束； `-1` 表示单调递减约束。 有多少个特征，就对应多少个数值。




## 六、 DART booster

1. 在`GBDT` 中，越早期加入的子树越重要；越后期加入的子树越不重要。

2. `DART booster` 原理：为了缓解过拟合，采用`dropout` 技术，随机丢弃一些树。

3. 由于引入了随机性，因此`dart` 和`gbtree` 有以下的不同：

    * 训练速度更慢
    * 早停不稳定

4. `DART booster` 也是使用与提升树相同的前向分步算法

    * 第<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-16-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.41ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -504.6 878 607.1" width="2.039ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E16-MJMATHI-6D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E16-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-16" type="math/tex">m</script>步，假设随机丢弃<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-17-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.877ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -755.9 889 808.1" width="2.065ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E17-MJMATHI-4B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E17-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-17" type="math/tex">K</script>棵，被丢弃的树的下标为集合<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-18-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 778 858.4" width="1.807ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E18-MJAMS-4B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E18-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-18" type="math/tex">\mathbb K</script>。

    令<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-19-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.811ex" role="img" style="vertical-align: -0.938ex;" viewbox="0 -806.1 5918.8 1210.2" width="13.747ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E19-MJMATHI-44" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E19-MJMAIN-3D" stroke-width="0"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E19-MJSZ1-2211" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E19-MJMATHI-6B" stroke-width="0"></path><path d="M84 250Q84 372 166 450T360 539Q361 539 377 539T419 540T469 540H568Q583 532 583 520Q583 511 570 501L466 500Q355 499 329 494Q280 482 242 458T183 409T147 354T129 306T124 272V270H568Q583 262 583 250T568 230H124V228Q124 207 134 177T167 112T231 48T328 7Q355 1 466 0H570Q583 -10 583 -20Q583 -32 568 -40H471Q464 -40 446 -40T417 -41Q262 -41 172 45Q84 127 84 250Z" id="E19-MJMAIN-2208" stroke-width="0"></path><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E19-MJAMS-4B" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E19-MJMATHI-68" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E19-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1105" xlink:href="#E19-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2161,0)"><use x="0" xlink:href="#E19-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E19-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E19-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E19-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(4874,0)"><use x="0" xlink:href="#E19-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E19-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></g></svg></span><script id="MathJax-Element-19" type="math/tex">D=\sum_{k\in \mathbb K}h_k</script>，第<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-20-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.41ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -504.6 878 607.1" width="2.039ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E20-MJMATHI-6D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E20-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-20" type="math/tex">m</script>棵树为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-33-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.344ex" role="img" style="vertical-align: -0.588ex;" viewbox="0 -755.9 1296.8 1009.2" width="3.012ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E33-MJMATHI-68" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E33-MJMATHI-6D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E33-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E33-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></svg></span><script id="MathJax-Element-33" type="math/tex">h_m</script>。则目标函数为：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-22-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.395ex" role="img" style="vertical-align: -0.938ex;" viewbox="0 -1057.4 23312 1461.5" width="54.144ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M62 -22T47 -22T32 -11Q32 -1 56 24T83 55Q113 96 138 172T180 320T234 473T323 609Q364 649 419 677T531 705Q559 705 578 696T604 671T615 645T618 623V611Q618 582 615 571T598 548Q581 531 558 520T518 509Q503 509 503 520Q503 523 505 536T507 560Q507 590 494 610T452 630Q423 630 410 617Q367 578 333 492T271 301T233 170Q211 123 204 112L198 103L224 102Q281 102 369 79T509 52H523Q535 64 544 87T579 128Q616 152 641 152Q656 152 656 142Q656 101 588 40T433 -22Q381 -22 289 1T156 28L141 29L131 20Q111 0 87 -11Z" id="E22-MJCAL-4C" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E22-MJMAIN-3D" stroke-width="0"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E22-MJSZ1-2211" stroke-width="0"></path><path d="M234 637Q231 637 226 637Q201 637 196 638T191 649Q191 676 202 682Q204 683 299 683Q376 683 387 683T401 677Q612 181 616 168L670 381Q723 592 723 606Q723 633 659 637Q635 637 635 648Q635 650 637 660Q641 676 643 679T653 683Q656 683 684 682T767 680Q817 680 843 681T873 682Q888 682 888 672Q888 650 880 642Q878 637 858 637Q787 633 769 597L620 7Q618 0 599 0Q585 0 582 2Q579 5 453 305L326 604L261 344Q196 88 196 79Q201 46 268 46H278Q284 41 284 38T282 19Q278 6 272 0H259Q228 2 151 2Q123 2 100 2T63 2T46 1Q31 1 31 10Q31 14 34 26T39 40Q41 46 62 46Q130 49 150 85Q154 91 221 362L289 634Q287 635 234 637Z" id="E22-MJMATHI-4E" stroke-width="0"></path><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" id="E22-MJMATHI-69" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E22-MJMAIN-31" stroke-width="0"></path><path d="M228 637Q194 637 192 641Q191 643 191 649Q191 673 202 682Q204 683 217 683Q271 680 344 680Q485 680 506 683H518Q524 677 524 674T522 656Q517 641 513 637H475Q406 636 394 628Q387 624 380 600T313 336Q297 271 279 198T252 88L243 52Q243 48 252 48T311 46H328Q360 46 379 47T428 54T478 72T522 106T564 161Q580 191 594 228T611 270Q616 273 628 273H641Q647 264 647 262T627 203T583 83T557 9Q555 4 553 3T537 0T494 -1Q483 -1 418 -1T294 0H116Q32 0 32 10Q32 17 34 24Q39 43 44 45Q48 46 59 46H65Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Q285 635 228 637Z" id="E22-MJMATHI-4C" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E22-MJMAIN-28" stroke-width="0"></path><path d="M21 287Q21 301 36 335T84 406T158 442Q199 442 224 419T250 355Q248 336 247 334Q247 331 231 288T198 191T182 105Q182 62 196 45T238 27Q261 27 281 38T312 61T339 94Q339 95 344 114T358 173T377 247Q415 397 419 404Q432 431 462 431Q475 431 483 424T494 412T496 403Q496 390 447 193T391 -23Q363 -106 294 -155T156 -205Q111 -205 77 -183T43 -117Q43 -95 50 -80T69 -58T89 -48T106 -45Q150 -45 150 -87Q150 -107 138 -122T115 -142T102 -147L99 -148Q101 -153 118 -160T152 -167H160Q177 -167 186 -165Q219 -156 247 -127T290 -65T313 -9T321 21L315 17Q309 13 296 6T270 -6Q250 -11 231 -11Q185 -11 150 11T104 82Q103 89 103 113Q103 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E22-MJMATHI-79" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E22-MJMAIN-2C" stroke-width="0"></path><path d="M112 560L249 694L257 686Q387 562 387 560L361 531Q359 532 303 581L250 627L195 580Q182 569 169 557T148 538L140 532Q138 530 125 546L112 560Z" id="E22-MJMAIN-5E" stroke-width="0"></path><path d="M694 -11T694 -19T688 -33T678 -40Q671 -40 524 29T234 166L90 235Q83 240 83 250Q83 261 91 266Q664 540 678 540Q681 540 687 534T694 519T687 505Q686 504 417 376L151 250L417 124Q686 -4 687 -5Q694 -11 694 -19Z" id="E22-MJMAIN-3C" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E22-MJMATHI-6D" stroke-width="0"></path><path d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z" id="E22-MJMAIN-2212" stroke-width="0"></path><path d="M84 520Q84 528 88 533T96 539L99 540Q106 540 253 471T544 334L687 265Q694 260 694 250T687 235Q685 233 395 96L107 -40H101Q83 -38 83 -20Q83 -19 83 -17Q82 -10 98 -1Q117 9 248 71Q326 108 378 132L626 250L378 368Q90 504 86 509Q84 513 84 520Z" id="E22-MJMAIN-3E" stroke-width="0"></path><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E22-MJMATHI-44" stroke-width="0"></path><path d="M227 0Q212 3 121 3Q40 3 28 0H21V62H117L245 213L109 382H26V444H34Q49 441 143 441Q247 441 265 444H274V382H246L281 339Q315 297 316 297Q320 297 354 341L389 382H352V444H360Q375 441 466 441Q547 441 559 444H566V382H471L355 246L504 63L545 62H586V0H578Q563 3 469 3Q365 3 347 0H338V62H366Q366 63 326 112T285 163L198 63L217 62H235V0H227Z" id="E22-MJMAINB-78" stroke-width="0"></path><path d="M-169 694Q-169 707 -160 715T-142 723Q-127 723 -119 716T-107 698T-90 673T-53 648Q-33 637 -33 619Q-33 602 -45 595T-87 573T-144 532Q-165 513 -176 513Q-189 513 -197 522T-206 543Q-206 556 -188 574L-175 588H-347L-519 589Q-542 597 -542 618Q-542 623 -541 627T-537 635T-532 640T-527 644T-522 648L-519 649H-149Q-169 676 -169 694Z" id="E22-MJMAINB-20D7" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E22-MJMAIN-29" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E22-MJMAIN-2B" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E22-MJMATHI-3BD" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E22-MJMATHI-68" stroke-width="0"></path><path d="M152 251Q152 646 388 850H416Q422 844 422 841Q422 837 403 816T357 753T302 649T255 482T236 250Q236 124 255 19T301 -147T356 -251T403 -315T422 -340Q422 -343 416 -349H388Q359 -325 332 -296T271 -213T212 -97T170 56T152 251Z" id="E22-MJSZ1-28" stroke-width="0"></path><path d="M305 251Q305 -145 69 -349H56Q43 -349 39 -347T35 -338Q37 -333 60 -307T108 -239T160 -136T204 27T221 250T204 473T160 636T108 740T60 807T35 839Q35 850 50 850H56H69Q197 743 256 566Q305 425 305 251Z" id="E22-MJSZ1-29" stroke-width="0"></path><path d="M55 454Q55 503 75 546T127 617T197 665T272 695T337 704H352Q396 704 404 703Q527 687 596 615T666 454Q666 392 635 330T559 200T499 83V80H543Q589 81 600 83T617 93Q622 102 629 135T636 172L637 177H677V175L660 89Q645 3 644 2V0H552H488Q461 0 456 3T451 20Q451 89 499 235T548 455Q548 512 530 555T483 622T424 656T361 668Q332 668 303 658T243 626T193 560T174 456Q174 380 222 233T270 20Q270 7 263 0H77V2Q76 3 61 89L44 175V177H84L85 172Q85 171 88 155T96 119T104 93Q109 86 120 84T178 80H222V83Q206 132 162 199T87 329T55 454Z" id="E22-MJMAIN-3A9" stroke-width="0"></path><path d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z" id="E22-MJMATHI-66" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E22-MJCAL-4C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="967" xlink:href="#E22-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2023,0)"><use x="0" xlink:href="#E22-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1493" xlink:href="#E22-MJMATHI-4E" xmlns:xlink="http://www.w3.org/1999/xlink" y="674"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E22-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="345" xlink:href="#E22-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1123" xlink:href="#E22-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><use x="4493" xlink:href="#E22-MJMATHI-4C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5341,0)"><use xlink:href="#E22-MJSZ1-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(458,0)"><use x="0" xlink:href="#E22-MJMATHI-79" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="692" xlink:href="#E22-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="1291" xlink:href="#E22-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1736,0)"><use x="1" xlink:href="#E22-MJMATHI-79" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="60" xlink:href="#E22-MJMAIN-5E" xmlns:xlink="http://www.w3.org/1999/xlink" y="-13"></use><g transform="translate(560,408)"><use transform="scale(0.707)" x="0" xlink:href="#E22-MJMAIN-3C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="778" xlink:href="#E22-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1655" xlink:href="#E22-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2434" xlink:href="#E22-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="2934" xlink:href="#E22-MJMAIN-3E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use transform="scale(0.707)" x="792" xlink:href="#E22-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-379"></use></g><use x="5243" xlink:href="#E22-MJMAIN-2212" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="6244" xlink:href="#E22-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7072" xlink:href="#E22-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(7461,0)"><use x="0" xlink:href="#E22-MJMAINB-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="574" xlink:href="#E22-MJMAINB-20D7" xmlns:xlink="http://www.w3.org/1999/xlink" y="6"></use><use transform="scale(0.707)" x="858" xlink:href="#E22-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="8411" xlink:href="#E22-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9023" xlink:href="#E22-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10023" xlink:href="#E22-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(10553,0)"><use x="0" xlink:href="#E22-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E22-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="11850" xlink:href="#E22-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(12239,0)"><use x="0" xlink:href="#E22-MJMAINB-78" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="574" xlink:href="#E22-MJMAINB-20D7" xmlns:xlink="http://www.w3.org/1999/xlink" y="6"></use><use transform="scale(0.707)" x="858" xlink:href="#E22-MJMATHI-69" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="13190" xlink:href="#E22-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="13579" xlink:href="#E22-MJSZ1-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="-1"></use></g><use x="19600" xlink:href="#E22-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="20601" xlink:href="#E22-MJMAIN-3A9" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="21323" xlink:href="#E22-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(21712,0)"><use x="0" xlink:href="#E22-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="692" xlink:href="#E22-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="22923" xlink:href="#E22-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-22" type="math/tex">\mathcal L=\sum_{i=1}^NL\left(y_i,\hat y^{<m-1>}_i-D(\mathbf {\vec x}_i)+\nu h_m(\mathbf{\vec x}_i)\right)+\Omega(f_m)</script>。

    * 由于`dropout` 在设定目标函数时引入了随机丢弃，因此如果直接引入<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-33-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.344ex" role="img" style="vertical-align: -0.588ex;" viewbox="0 -755.9 1296.8 1009.2" width="3.012ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E33-MJMATHI-68" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E33-MJMATHI-6D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E33-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E33-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></svg></span><script id="MathJax-Element-33" type="math/tex">h_m</script>，则会引起超调。因此引入缩放因子，这称作为归一化：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-24-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.278ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -906.7 16560.8 1411.3" width="38.464ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z" id="E24-MJMATHI-66" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E24-MJMATHI-6D" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E24-MJMAIN-3D" stroke-width="0"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E24-MJSZ1-2211" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E24-MJMATHI-6B" stroke-width="0"></path><path d="M166 -215T159 -215T147 -212T141 -204T139 -197Q139 -190 144 -183L306 133H70Q56 140 56 153Q56 168 72 173H327L406 327H72Q56 332 56 347Q56 360 70 367H426Q597 702 602 707Q605 716 618 716Q625 716 630 712T636 703T638 696Q638 692 471 367H707Q722 359 722 347Q722 336 708 328L451 327L371 173H708Q722 163 722 153Q722 140 707 133H351Q175 -210 170 -212Q166 -215 159 -215Z" id="E24-MJMAIN-2260" stroke-width="0"></path><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E24-MJAMS-4B" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E24-MJMATHI-68" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E24-MJMAIN-2B" stroke-width="0"></path><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E24-MJMATHI-3B1" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E24-MJMAIN-28" stroke-width="0"></path><path d="M84 250Q84 372 166 450T360 539Q361 539 377 539T419 540T469 540H568Q583 532 583 520Q583 511 570 501L466 500Q355 499 329 494Q280 482 242 458T183 409T147 354T129 306T124 272V270H568Q583 262 583 250T568 230H124V228Q124 207 134 177T167 112T231 48T328 7Q355 1 466 0H570Q583 -10 583 -20Q583 -32 568 -40H471Q464 -40 446 -40T417 -41Q262 -41 172 45Q84 127 84 250Z" id="E24-MJMAIN-2208" stroke-width="0"></path><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E24-MJMATHI-62" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E24-MJMATHI-3BD" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E24-MJMAIN-29" stroke-width="0"></path><path d="M152 251Q152 646 388 850H416Q422 844 422 841Q422 837 403 816T357 753T302 649T255 482T236 250Q236 124 255 19T301 -147T356 -251T403 -315T422 -340Q422 -343 416 -349H388Q359 -325 332 -296T271 -213T212 -97T170 56T152 251Z" id="E24-MJSZ1-28" stroke-width="0"></path><path d="M305 251Q305 -145 69 -349H56Q43 -349 39 -347T35 -338Q37 -333 60 -307T108 -239T160 -136T204 27T221 250T204 473T160 636T108 740T60 807T35 839Q35 850 50 850H56H69Q197 743 256 566Q305 425 305 251Z" id="E24-MJSZ1-29" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E24-MJMATHI-66" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="692" xlink:href="#E24-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use><use x="1488" xlink:href="#E24-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2544,0)"><use x="0" xlink:href="#E24-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E24-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E24-MJMAIN-2260" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1299" xlink:href="#E24-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(5335,0)"><use x="0" xlink:href="#E24-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E24-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="6602" xlink:href="#E24-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="7602" xlink:href="#E24-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(8409,0)"><use xlink:href="#E24-MJSZ1-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(458,0)"><use x="0" xlink:href="#E24-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E24-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E24-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E24-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(3170,0)"><use x="0" xlink:href="#E24-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E24-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="4437" xlink:href="#E24-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5437" xlink:href="#E24-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5866" xlink:href="#E24-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(6396,0)"><use x="0" xlink:href="#E24-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E24-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="7693" xlink:href="#E24-MJSZ1-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="-1"></use></g></g></svg></span><script id="MathJax-Element-24" type="math/tex">f_m = \sum_{k\ne \mathbb K} h_k+\alpha\left(\sum_{k\in\mathbb K}h_k+b \nu h_m\right)</script>。

        * 其中<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-25-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 429 858.4" width="0.996ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E25-MJMATHI-62" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E25-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-25" type="math/tex">b</script>为新的子树与丢弃的子树的权重之比，<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-26-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.41ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -504.6 640 607.1" width="1.486ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E26-MJMATHI-3B1" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E26-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-26" type="math/tex">\alpha</script>为修正因子。

        * 令<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-27-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.511ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -1007.2 6220.3 1511.8" width="14.447ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M289 629Q289 635 232 637Q208 637 201 638T194 648Q194 649 196 659Q197 662 198 666T199 671T201 676T203 679T207 681T212 683T220 683T232 684Q238 684 262 684T307 683Q386 683 398 683T414 678Q415 674 451 396L487 117L510 154Q534 190 574 254T662 394Q837 673 839 675Q840 676 842 678T846 681L852 683H948Q965 683 988 683T1017 684Q1051 684 1051 673Q1051 668 1048 656T1045 643Q1041 637 1008 637Q968 636 957 634T939 623Q936 618 867 340T797 59Q797 55 798 54T805 50T822 48T855 46H886Q892 37 892 35Q892 19 885 5Q880 0 869 0Q864 0 828 1T736 2Q675 2 644 2T609 1Q592 1 592 11Q592 13 594 25Q598 41 602 43T625 46Q652 46 685 49Q699 52 704 61Q706 65 742 207T813 490T848 631L654 322Q458 10 453 5Q451 4 449 3Q444 0 433 0Q418 0 415 7Q413 11 374 317L335 624L267 354Q200 88 200 79Q206 46 272 46H282Q288 41 289 37T286 19Q282 3 278 1Q274 0 267 0Q265 0 255 0T221 1T157 2Q127 2 95 1T58 0Q43 0 39 2T35 11Q35 13 38 25T43 40Q45 46 65 46Q135 46 154 86Q158 92 223 354T289 629Z" id="E27-MJMATHI-4D" stroke-width="0"></path><path d="M112 560L249 694L257 686Q387 562 387 560L361 531Q359 532 303 581L250 627L195 580Q182 569 169 557T148 538L140 532Q138 530 125 546L112 560Z" id="E27-MJMAIN-5E" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E27-MJMAIN-3D" stroke-width="0"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E27-MJSZ1-2211" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E27-MJMATHI-6B" stroke-width="0"></path><path d="M166 -215T159 -215T147 -212T141 -204T139 -197Q139 -190 144 -183L306 133H70Q56 140 56 153Q56 168 72 173H327L406 327H72Q56 332 56 347Q56 360 70 367H426Q597 702 602 707Q605 716 618 716Q625 716 630 712T636 703T638 696Q638 692 471 367H707Q722 359 722 347Q722 336 708 328L451 327L371 173H708Q722 163 722 153Q722 140 707 133H351Q175 -210 170 -212Q166 -215 159 -215Z" id="E27-MJMAIN-2260" stroke-width="0"></path><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E27-MJAMS-4B" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E27-MJMATHI-68" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E27-MJMATHI-4D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="411" xlink:href="#E27-MJMAIN-5E" xmlns:xlink="http://www.w3.org/1999/xlink" y="228"></use><use x="1328" xlink:href="#E27-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2384,0)"><use x="0" xlink:href="#E27-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E27-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E27-MJMAIN-2260" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1299" xlink:href="#E27-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(5175,0)"><use x="0" xlink:href="#E27-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E27-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></g></svg></span><script id="MathJax-Element-27" type="math/tex">\hat M=\sum_{k\ne \mathbb K} h_k</script>。采用归一化的原因是：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-33-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.344ex" role="img" style="vertical-align: -0.588ex;" viewbox="0 -755.9 1296.8 1009.2" width="3.012ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E33-MJMATHI-68" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E33-MJMATHI-6D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E33-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E33-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></svg></span><script id="MathJax-Element-33" type="math/tex">h_m</script>试图缩小<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-31-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.461ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -1007.2 1051 1059.4" width="2.441ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M289 629Q289 635 232 637Q208 637 201 638T194 648Q194 649 196 659Q197 662 198 666T199 671T201 676T203 679T207 681T212 683T220 683T232 684Q238 684 262 684T307 683Q386 683 398 683T414 678Q415 674 451 396L487 117L510 154Q534 190 574 254T662 394Q837 673 839 675Q840 676 842 678T846 681L852 683H948Q965 683 988 683T1017 684Q1051 684 1051 673Q1051 668 1048 656T1045 643Q1041 637 1008 637Q968 636 957 634T939 623Q936 618 867 340T797 59Q797 55 798 54T805 50T822 48T855 46H886Q892 37 892 35Q892 19 885 5Q880 0 869 0Q864 0 828 1T736 2Q675 2 644 2T609 1Q592 1 592 11Q592 13 594 25Q598 41 602 43T625 46Q652 46 685 49Q699 52 704 61Q706 65 742 207T813 490T848 631L654 322Q458 10 453 5Q451 4 449 3Q444 0 433 0Q418 0 415 7Q413 11 374 317L335 624L267 354Q200 88 200 79Q206 46 272 46H282Q288 41 289 37T286 19Q282 3 278 1Q274 0 267 0Q265 0 255 0T221 1T157 2Q127 2 95 1T58 0Q43 0 39 2T35 11Q35 13 38 25T43 40Q45 46 65 46Q135 46 154 86Q158 92 223 354T289 629Z" id="E31-MJMATHI-4D" stroke-width="0"></path><path d="M112 560L249 694L257 686Q387 562 387 560L361 531Q359 532 303 581L250 627L195 580Q182 569 169 557T148 538L140 532Q138 530 125 546L112 560Z" id="E31-MJMAIN-5E" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E31-MJMATHI-4D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="411" xlink:href="#E31-MJMAIN-5E" xmlns:xlink="http://www.w3.org/1999/xlink" y="228"></use></g></svg></span><script id="MathJax-Element-31" type="math/tex">\hat M</script>到目标之间的 `gap`； 而<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-32-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.877ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -755.9 828 808.1" width="1.923ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E32-MJMATHI-44" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E32-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-32" type="math/tex">D</script>也会试图缩小<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-31-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.461ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -1007.2 1051 1059.4" width="2.441ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M289 629Q289 635 232 637Q208 637 201 638T194 648Q194 649 196 659Q197 662 198 666T199 671T201 676T203 679T207 681T212 683T220 683T232 684Q238 684 262 684T307 683Q386 683 398 683T414 678Q415 674 451 396L487 117L510 154Q534 190 574 254T662 394Q837 673 839 675Q840 676 842 678T846 681L852 683H948Q965 683 988 683T1017 684Q1051 684 1051 673Q1051 668 1048 656T1045 643Q1041 637 1008 637Q968 636 957 634T939 623Q936 618 867 340T797 59Q797 55 798 54T805 50T822 48T855 46H886Q892 37 892 35Q892 19 885 5Q880 0 869 0Q864 0 828 1T736 2Q675 2 644 2T609 1Q592 1 592 11Q592 13 594 25Q598 41 602 43T625 46Q652 46 685 49Q699 52 704 61Q706 65 742 207T813 490T848 631L654 322Q458 10 453 5Q451 4 449 3Q444 0 433 0Q418 0 415 7Q413 11 374 317L335 624L267 354Q200 88 200 79Q206 46 272 46H282Q288 41 289 37T286 19Q282 3 278 1Q274 0 267 0Q265 0 255 0T221 1T157 2Q127 2 95 1T58 0Q43 0 39 2T35 11Q35 13 38 25T43 40Q45 46 65 46Q135 46 154 86Q158 92 223 354T289 629Z" id="E31-MJMATHI-4D" stroke-width="0"></path><path d="M112 560L249 694L257 686Q387 562 387 560L361 531Q359 532 303 581L250 627L195 580Q182 569 169 557T148 538L140 532Q138 530 125 546L112 560Z" id="E31-MJMAIN-5E" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E31-MJMATHI-4D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="411" xlink:href="#E31-MJMAIN-5E" xmlns:xlink="http://www.w3.org/1999/xlink" y="228"></use></g></svg></span><script id="MathJax-Element-31" type="math/tex">\hat M</script>到目标之间的 `gap`。

        如果同时引入随机丢弃的子树集合<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-32-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.877ex" role="img" style="vertical-align: -0.121ex;" viewbox="0 -755.9 828 808.1" width="1.923ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E32-MJMATHI-44" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E32-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-32" type="math/tex">D</script>，以及新的子树<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-33-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.344ex" role="img" style="vertical-align: -0.588ex;" viewbox="0 -755.9 1296.8 1009.2" width="3.012ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E33-MJMATHI-68" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E33-MJMATHI-6D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E33-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E33-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g></svg></span><script id="MathJax-Element-33" type="math/tex">h_m</script>，则会引起超调。

        * 有两种归一化策略：

            * `'tree'`： 新加入的子树具有和每个丢弃的子树一样的权重，假设都是都是<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-38-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.278ex" role="img" style="vertical-align: -1.055ex;" viewbox="0 -956.9 988.6 1411.3" width="2.296ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E38-MJMAIN-31" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E38-MJMATHI-4B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="748" x="0" y="220"></rect><use transform="scale(0.707)" x="279" xlink:href="#E38-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><use transform="scale(0.707)" x="84" xlink:href="#E38-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-548"></use></g></g></svg></span><script id="MathJax-Element-38" type="math/tex">\frac 1K</script>。

            此时<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-35-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.278ex" role="img" style="vertical-align: -1.055ex;" viewbox="0 -956.9 2751.2 1411.3" width="6.39ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E35-MJMATHI-62" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E35-MJMAIN-3D" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E35-MJMAIN-31" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E35-MJMATHI-4B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E35-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="706" xlink:href="#E35-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1484,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="748" x="0" y="220"></rect><use transform="scale(0.707)" x="279" xlink:href="#E35-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><use transform="scale(0.707)" x="84" xlink:href="#E35-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-548"></use></g></g></g></svg></span><script id="MathJax-Element-35" type="math/tex">b=\frac 1K</script>，则有：
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display" style="text-align: center;"><span class="MathJax_SVG" id="MathJax-Element-1-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="7.247ex" role="img" style="vertical-align: -3.04ex;" viewbox="0 -1811.3 31774.9 3120.1" width="73.8ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E1-MJMATHI-3B1" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E1-MJMAIN-28" stroke-width="0"></path><path d="M60 948Q63 950 665 950H1267L1325 815Q1384 677 1388 669H1348L1341 683Q1320 724 1285 761Q1235 809 1174 838T1033 881T882 898T699 902H574H543H251L259 891Q722 258 724 252Q725 250 724 246Q721 243 460 -56L196 -356Q196 -357 407 -357Q459 -357 548 -357T676 -358Q812 -358 896 -353T1063 -332T1204 -283T1307 -196Q1328 -170 1348 -124H1388Q1388 -125 1381 -145T1356 -210T1325 -294L1267 -449L666 -450Q64 -450 61 -448Q55 -446 55 -439Q55 -437 57 -433L590 177Q590 178 557 222T452 366T322 544L56 909L55 924Q55 945 60 948Z" id="E1-MJSZ2-2211" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E1-MJMATHI-6B" stroke-width="0"></path><path d="M84 250Q84 372 166 450T360 539Q361 539 377 539T419 540T469 540H568Q583 532 583 520Q583 511 570 501L466 500Q355 499 329 494Q280 482 242 458T183 409T147 354T129 306T124 272V270H568Q583 262 583 250T568 230H124V228Q124 207 134 177T167 112T231 48T328 7Q355 1 466 0H570Q583 -10 583 -20Q583 -32 568 -40H471Q464 -40 446 -40T417 -41Q262 -41 172 45Q84 127 84 250Z" id="E1-MJMAIN-2208" stroke-width="0"></path><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E1-MJAMS-4B" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E1-MJMATHI-68" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E1-MJMAIN-2B" stroke-width="0"></path><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E1-MJMATHI-62" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E1-MJMATHI-3BD" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E1-MJMATHI-6D" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E1-MJMAIN-29" stroke-width="0"></path><path d="M758 -1237T758 -1240T752 -1249H736Q718 -1249 717 -1248Q711 -1245 672 -1199Q237 -706 237 251T672 1700Q697 1730 716 1749Q718 1750 735 1750H752Q758 1744 758 1741Q758 1737 740 1713T689 1644T619 1537T540 1380T463 1176Q348 802 348 251Q348 -242 441 -599T744 -1218Q758 -1237 758 -1240Z" id="E1-MJSZ4-28" stroke-width="0"></path><path d="M33 1741Q33 1750 51 1750H60H65Q73 1750 81 1743T119 1700Q554 1207 554 251Q554 -707 119 -1199Q76 -1250 66 -1250Q65 -1250 62 -1250T56 -1249Q55 -1249 53 -1249T49 -1250Q33 -1250 33 -1239Q33 -1236 50 -1214T98 -1150T163 -1052T238 -910T311 -727Q443 -335 443 251Q443 402 436 532T405 831T339 1142T224 1438T50 1716Q33 1737 33 1741Z" id="E1-MJSZ4-29" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E1-MJMAIN-3D" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E1-MJMATHI-4B" stroke-width="0"></path><path d="M55 166Q55 241 101 304T222 367Q260 367 296 349T362 304T421 252T484 208T554 189Q616 189 655 236T694 338Q694 350 698 358T708 367Q722 367 722 334Q722 260 677 197T562 134H554Q517 134 481 152T414 196T355 248T292 293T223 311Q179 311 145 286Q109 257 96 218T80 156T69 133Q55 133 55 166Z" id="E1-MJMAIN-223C" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E1-MJMAIN-31" stroke-width="0"></path><path d="M180 96T180 250T205 541T266 770T353 944T444 1069T527 1150H555Q561 1144 561 1141Q561 1137 545 1120T504 1072T447 995T386 878T330 721T288 513T272 251Q272 133 280 56Q293 -87 326 -209T399 -405T475 -531T536 -609T561 -640Q561 -643 555 -649H527Q483 -612 443 -568T353 -443T266 -270T205 -41Z" id="E1-MJSZ2-28" stroke-width="0"></path><path d="M35 1138Q35 1150 51 1150H56H69Q113 1113 153 1069T243 944T330 771T391 541T416 250T391 -40T330 -270T243 -443T152 -568T69 -649H56Q43 -649 39 -647T35 -637Q65 -607 110 -548Q283 -316 316 56Q324 133 324 251Q324 368 316 445Q278 877 48 1123Q36 1137 35 1138Z" id="E1-MJSZ2-29" stroke-width="0"></path><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E1-MJMATHI-44" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E1-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(806,0)"><use xlink:href="#E1-MJSZ4-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(792,0)"><use x="0" xlink:href="#E1-MJSZ2-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(26,-1108)"><use transform="scale(0.707)" x="0" xlink:href="#E1-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E1-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E1-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(2402,0)"><use x="0" xlink:href="#E1-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E1-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="3669" xlink:href="#E1-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4669" xlink:href="#E1-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5098" xlink:href="#E1-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5628,0)"><use x="0" xlink:href="#E1-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E1-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="6925" xlink:href="#E1-MJSZ4-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="8801" xlink:href="#E1-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9857" xlink:href="#E1-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(10664,0)"><use xlink:href="#E1-MJSZ4-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(792,0)"><use x="0" xlink:href="#E1-MJSZ2-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(26,-1108)"><use transform="scale(0.707)" x="0" xlink:href="#E1-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E1-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E1-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(2402,0)"><use x="0" xlink:href="#E1-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E1-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="3669" xlink:href="#E1-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(4447,0)"><g transform="translate(342,0)"><rect height="60" stroke="none" width="1009" x="0" y="220"></rect><use x="239" xlink:href="#E1-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="676"></use><use x="60" xlink:href="#E1-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-686"></use></g></g><g transform="translate(5918,0)"><use x="0" xlink:href="#E1-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E1-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="7215" xlink:href="#E1-MJSZ4-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="18949" xlink:href="#E1-MJMAIN-223C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="20005" xlink:href="#E1-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(20811,0)"><use xlink:href="#E1-MJSZ2-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><use x="597" xlink:href="#E1-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1319" xlink:href="#E1-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(2097,0)"><g transform="translate(342,0)"><rect height="60" stroke="none" width="1009" x="0" y="220"></rect><use x="239" xlink:href="#E1-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="676"></use><use x="60" xlink:href="#E1-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-686"></use></g></g><use x="3568" xlink:href="#E1-MJSZ2-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="-1"></use></g><use x="25143" xlink:href="#E1-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="26249" xlink:href="#E1-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="27305" xlink:href="#E1-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(27945,0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="2761" x="0" y="220"></rect><g transform="translate(60,676)"><use x="0" xlink:href="#E1-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1111" xlink:href="#E1-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2111" xlink:href="#E1-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="936" xlink:href="#E1-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-686"></use></g></g><use x="30946" xlink:href="#E1-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span></span><script id="MathJax-Element-1" type="math/tex; mode=display">\alpha\left(\sum_{k\in\mathbb K}h_k+b \nu h_m\right)=\alpha\left(\sum_{k\in\mathbb K}h_k+\frac \nu K h_m\right) \sim \alpha\left(1+\frac \nu K\right)D=\alpha \frac{K+\nu}{K}D</script>
            要想缓解超调，则应该使得<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-40-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.044ex" role="img" style="vertical-align: -0.938ex;" viewbox="0 -906.7 11119.7 1310.7" width="25.827ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E40-MJMATHI-3B1" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E40-MJMAIN-28" stroke-width="0"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E40-MJSZ1-2211" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E40-MJMATHI-6B" stroke-width="0"></path><path d="M84 250Q84 372 166 450T360 539Q361 539 377 539T419 540T469 540H568Q583 532 583 520Q583 511 570 501L466 500Q355 499 329 494Q280 482 242 458T183 409T147 354T129 306T124 272V270H568Q583 262 583 250T568 230H124V228Q124 207 134 177T167 112T231 48T328 7Q355 1 466 0H570Q583 -10 583 -20Q583 -32 568 -40H471Q464 -40 446 -40T417 -41Q262 -41 172 45Q84 127 84 250Z" id="E40-MJMAIN-2208" stroke-width="0"></path><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E40-MJAMS-4B" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E40-MJMATHI-68" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E40-MJMAIN-2B" stroke-width="0"></path><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E40-MJMATHI-62" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E40-MJMATHI-3BD" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E40-MJMATHI-6D" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E40-MJMAIN-29" stroke-width="0"></path><path d="M152 251Q152 646 388 850H416Q422 844 422 841Q422 837 403 816T357 753T302 649T255 482T236 250Q236 124 255 19T301 -147T356 -251T403 -315T422 -340Q422 -343 416 -349H388Q359 -325 332 -296T271 -213T212 -97T170 56T152 251Z" id="E40-MJSZ1-28" stroke-width="0"></path><path d="M305 251Q305 -145 69 -349H56Q43 -349 39 -347T35 -338Q37 -333 60 -307T108 -239T160 -136T204 27T221 250T204 473T160 636T108 740T60 807T35 839Q35 850 50 850H56H69Q197 743 256 566Q305 425 305 251Z" id="E40-MJSZ1-29" stroke-width="0"></path><path d="M55 166Q55 241 101 304T222 367Q260 367 296 349T362 304T421 252T484 208T554 189Q616 189 655 236T694 338Q694 350 698 358T708 367Q722 367 722 334Q722 260 677 197T562 134H554Q517 134 481 152T414 196T355 248T292 293T223 311Q179 311 145 286Q109 257 96 218T80 156T69 133Q55 133 55 166Z" id="E40-MJMAIN-223C" stroke-width="0"></path><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E40-MJMATHI-44" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E40-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(806,0)"><use xlink:href="#E40-MJSZ1-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(458,0)"><use x="0" xlink:href="#E40-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E40-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E40-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E40-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(3170,0)"><use x="0" xlink:href="#E40-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E40-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="4437" xlink:href="#E40-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5437" xlink:href="#E40-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5866" xlink:href="#E40-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(6396,0)"><use x="0" xlink:href="#E40-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E40-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="7693" xlink:href="#E40-MJSZ1-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="-1"></use></g><use x="9235" xlink:href="#E40-MJMAIN-223C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10291" xlink:href="#E40-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-40" type="math/tex">\alpha\left(\sum_{k\in\mathbb K}h_k+b \nu h_m\right) \sim D</script>，则有：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-37-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.395ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -956.9 3887.1 1461.5" width="9.028ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E37-MJMATHI-3B1" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E37-MJMAIN-3D" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E37-MJMATHI-4B" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E37-MJMAIN-2B" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E37-MJMATHI-3BD" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E37-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="917" xlink:href="#E37-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1695,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="1673" x="0" y="220"></rect><use transform="scale(0.707)" x="738" xlink:href="#E37-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-388)"><use transform="scale(0.707)" x="0" xlink:href="#E37-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="889" xlink:href="#E37-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1667" xlink:href="#E37-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></g></svg></span><script id="MathJax-Element-37" type="math/tex">\alpha=\frac{K}{K+\nu}</script>。

            * `'forest'`：新加入的子树的权重等于丢弃的子树的权重之和。假设被丢弃的子树权重都是<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-38-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.278ex" role="img" style="vertical-align: -1.055ex;" viewbox="0 -956.9 988.6 1411.3" width="2.296ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E38-MJMAIN-31" stroke-width="0"></path><path d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z" id="E38-MJMATHI-4B" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><g transform="translate(120,0)"><rect height="60" stroke="none" width="748" x="0" y="220"></rect><use transform="scale(0.707)" x="279" xlink:href="#E38-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><use transform="scale(0.707)" x="84" xlink:href="#E38-MJMATHI-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-548"></use></g></g></svg></span><script id="MathJax-Element-38" type="math/tex">\frac 1K</script>， 则此时<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-39-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="1.994ex" role="img" style="vertical-align: -0.238ex;" viewbox="0 -755.9 2262.6 858.4" width="5.255ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E39-MJMATHI-62" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E39-MJMAIN-3D" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E39-MJMAIN-31" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E39-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="706" xlink:href="#E39-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1762" xlink:href="#E39-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-39" type="math/tex">b=1</script>，则有：
<span class="MathJax_Preview"></span><span class="MathJax_SVG_Display" style="text-align: center;"><span class="MathJax_SVG" id="MathJax-Element-2-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="7.247ex" role="img" style="vertical-align: -3.04ex;" viewbox="0 -1811.3 24117.9 3120.1" width="56.016ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E2-MJMATHI-3B1" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E2-MJMAIN-28" stroke-width="0"></path><path d="M60 948Q63 950 665 950H1267L1325 815Q1384 677 1388 669H1348L1341 683Q1320 724 1285 761Q1235 809 1174 838T1033 881T882 898T699 902H574H543H251L259 891Q722 258 724 252Q725 250 724 246Q721 243 460 -56L196 -356Q196 -357 407 -357Q459 -357 548 -357T676 -358Q812 -358 896 -353T1063 -332T1204 -283T1307 -196Q1328 -170 1348 -124H1388Q1388 -125 1381 -145T1356 -210T1325 -294L1267 -449L666 -450Q64 -450 61 -448Q55 -446 55 -439Q55 -437 57 -433L590 177Q590 178 557 222T452 366T322 544L56 909L55 924Q55 945 60 948Z" id="E2-MJSZ2-2211" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E2-MJMATHI-6B" stroke-width="0"></path><path d="M84 250Q84 372 166 450T360 539Q361 539 377 539T419 540T469 540H568Q583 532 583 520Q583 511 570 501L466 500Q355 499 329 494Q280 482 242 458T183 409T147 354T129 306T124 272V270H568Q583 262 583 250T568 230H124V228Q124 207 134 177T167 112T231 48T328 7Q355 1 466 0H570Q583 -10 583 -20Q583 -32 568 -40H471Q464 -40 446 -40T417 -41Q262 -41 172 45Q84 127 84 250Z" id="E2-MJMAIN-2208" stroke-width="0"></path><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E2-MJAMS-4B" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E2-MJMATHI-68" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E2-MJMAIN-2B" stroke-width="0"></path><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E2-MJMATHI-62" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E2-MJMATHI-3BD" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E2-MJMATHI-6D" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E2-MJMAIN-29" stroke-width="0"></path><path d="M758 -1237T758 -1240T752 -1249H736Q718 -1249 717 -1248Q711 -1245 672 -1199Q237 -706 237 251T672 1700Q697 1730 716 1749Q718 1750 735 1750H752Q758 1744 758 1741Q758 1737 740 1713T689 1644T619 1537T540 1380T463 1176Q348 802 348 251Q348 -242 441 -599T744 -1218Q758 -1237 758 -1240Z" id="E2-MJSZ4-28" stroke-width="0"></path><path d="M33 1741Q33 1750 51 1750H60H65Q73 1750 81 1743T119 1700Q554 1207 554 251Q554 -707 119 -1199Q76 -1250 66 -1250Q65 -1250 62 -1250T56 -1249Q55 -1249 53 -1249T49 -1250Q33 -1250 33 -1239Q33 -1236 50 -1214T98 -1150T163 -1052T238 -910T311 -727Q443 -335 443 251Q443 402 436 532T405 831T339 1142T224 1438T50 1716Q33 1737 33 1741Z" id="E2-MJSZ4-29" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E2-MJMAIN-3D" stroke-width="0"></path><path d="M55 166Q55 241 101 304T222 367Q260 367 296 349T362 304T421 252T484 208T554 189Q616 189 655 236T694 338Q694 350 698 358T708 367Q722 367 722 334Q722 260 677 197T562 134H554Q517 134 481 152T414 196T355 248T292 293T223 311Q179 311 145 286Q109 257 96 218T80 156T69 133Q55 133 55 166Z" id="E2-MJMAIN-223C" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E2-MJMAIN-31" stroke-width="0"></path><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E2-MJMATHI-44" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E2-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(806,0)"><use xlink:href="#E2-MJSZ4-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(792,0)"><use x="0" xlink:href="#E2-MJSZ2-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(26,-1108)"><use transform="scale(0.707)" x="0" xlink:href="#E2-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E2-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E2-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(2402,0)"><use x="0" xlink:href="#E2-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E2-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="3669" xlink:href="#E2-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4669" xlink:href="#E2-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5098" xlink:href="#E2-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5628,0)"><use x="0" xlink:href="#E2-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E2-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="6925" xlink:href="#E2-MJSZ4-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="8801" xlink:href="#E2-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="9857" xlink:href="#E2-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(10664,0)"><use xlink:href="#E2-MJSZ4-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(792,0)"><use x="0" xlink:href="#E2-MJSZ2-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(26,-1108)"><use transform="scale(0.707)" x="0" xlink:href="#E2-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E2-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E2-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(2402,0)"><use x="0" xlink:href="#E2-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E2-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="3669" xlink:href="#E2-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="4669" xlink:href="#E2-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(5199,0)"><use x="0" xlink:href="#E2-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E2-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="6496" xlink:href="#E2-MJSZ4-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="18230" xlink:href="#E2-MJMAIN-223C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="19286" xlink:href="#E2-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(20092,0)"><use x="0" xlink:href="#E2-MJMAIN-28" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="389" xlink:href="#E2-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1111" xlink:href="#E2-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2111" xlink:href="#E2-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2641" xlink:href="#E2-MJMAIN-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g><use x="23289" xlink:href="#E2-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span></span><script id="MathJax-Element-2" type="math/tex; mode=display">\alpha\left(\sum_{k\in\mathbb K}h_k+b \nu h_m\right)=\alpha\left(\sum_{k\in\mathbb K}h_k+ \nu h_m\right) \sim \alpha\left(1+ \nu \right)D</script>
            要想缓解超调，则应该使得<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-40-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.044ex" role="img" style="vertical-align: -0.938ex;" viewbox="0 -906.7 11119.7 1310.7" width="25.827ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E40-MJMATHI-3B1" stroke-width="0"></path><path d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z" id="E40-MJMAIN-28" stroke-width="0"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" id="E40-MJSZ1-2211" stroke-width="0"></path><path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" id="E40-MJMATHI-6B" stroke-width="0"></path><path d="M84 250Q84 372 166 450T360 539Q361 539 377 539T419 540T469 540H568Q583 532 583 520Q583 511 570 501L466 500Q355 499 329 494Q280 482 242 458T183 409T147 354T129 306T124 272V270H568Q583 262 583 250T568 230H124V228Q124 207 134 177T167 112T231 48T328 7Q355 1 466 0H570Q583 -10 583 -20Q583 -32 568 -40H471Q464 -40 446 -40T417 -41Q262 -41 172 45Q84 127 84 250Z" id="E40-MJMAIN-2208" stroke-width="0"></path><path d="M22 666Q22 676 33 683H351L358 679Q368 665 358 655Q351 648 324 648Q288 645 280 637Q275 631 274 605T273 477L275 343L382 446Q473 530 492 553T512 599Q512 617 502 631T475 648Q455 651 455 666Q455 677 465 680T510 683H593H720Q732 676 732 666Q732 659 727 654T713 648Q670 648 589 581Q567 562 490 489T413 415Q413 413 554 245T711 61Q737 35 751 35Q758 35 763 29T768 15Q768 6 758 -1H624Q491 -1 486 3Q480 10 480 17Q480 25 487 30T506 35Q518 36 520 38T520 48L400 195L302 310L286 297L273 283V170Q275 65 277 57Q280 41 300 38Q302 37 324 35Q349 35 358 28Q367 17 358 3L351 -1H33Q22 4 22 16Q22 35 60 35Q101 38 106 52Q111 60 111 341T106 632Q100 645 60 648Q22 648 22 666ZM240 341V553Q240 635 246 648H138Q141 641 142 638T144 603T146 517T146 341Q146 131 145 89T139 37Q138 36 138 35H246Q240 47 240 129V341ZM595 632L615 648H535L542 637Q542 636 544 625T549 610V595L562 606Q565 608 577 618T595 632ZM524 226L386 388Q386 389 378 382T358 361Q330 338 330 333Q330 332 330 332L331 330L533 90Q558 55 558 41V35H684L671 50Q667 54 524 226Z" id="E40-MJAMS-4B" stroke-width="0"></path><path d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z" id="E40-MJMATHI-68" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E40-MJMAIN-2B" stroke-width="0"></path><path d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z" id="E40-MJMATHI-62" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E40-MJMATHI-3BD" stroke-width="0"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" id="E40-MJMATHI-6D" stroke-width="0"></path><path d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z" id="E40-MJMAIN-29" stroke-width="0"></path><path d="M152 251Q152 646 388 850H416Q422 844 422 841Q422 837 403 816T357 753T302 649T255 482T236 250Q236 124 255 19T301 -147T356 -251T403 -315T422 -340Q422 -343 416 -349H388Q359 -325 332 -296T271 -213T212 -97T170 56T152 251Z" id="E40-MJSZ1-28" stroke-width="0"></path><path d="M305 251Q305 -145 69 -349H56Q43 -349 39 -347T35 -338Q37 -333 60 -307T108 -239T160 -136T204 27T221 250T204 473T160 636T108 740T60 807T35 839Q35 850 50 850H56H69Q197 743 256 566Q305 425 305 251Z" id="E40-MJSZ1-29" stroke-width="0"></path><path d="M55 166Q55 241 101 304T222 367Q260 367 296 349T362 304T421 252T484 208T554 189Q616 189 655 236T694 338Q694 350 698 358T708 367Q722 367 722 334Q722 260 677 197T562 134H554Q517 134 481 152T414 196T355 248T292 293T223 311Q179 311 145 286Q109 257 96 218T80 156T69 133Q55 133 55 166Z" id="E40-MJMAIN-223C" stroke-width="0"></path><path d="M287 628Q287 635 230 637Q207 637 200 638T193 647Q193 655 197 667T204 682Q206 683 403 683Q570 682 590 682T630 676Q702 659 752 597T803 431Q803 275 696 151T444 3L430 1L236 0H125H72Q48 0 41 2T33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM703 469Q703 507 692 537T666 584T629 613T590 629T555 636Q553 636 541 636T512 636T479 637H436Q392 637 386 627Q384 623 313 339T242 52Q242 48 253 48T330 47Q335 47 349 47T373 46Q499 46 581 128Q617 164 640 212T683 339T703 469Z" id="E40-MJMATHI-44" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E40-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(806,0)"><use xlink:href="#E40-MJSZ1-28" xmlns:xlink="http://www.w3.org/1999/xlink"></use><g transform="translate(458,0)"><use x="0" xlink:href="#E40-MJSZ1-2211" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1056,-286)"><use transform="scale(0.707)" x="0" xlink:href="#E40-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="521" xlink:href="#E40-MJMAIN-2208" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1188" xlink:href="#E40-MJAMS-4B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g><g transform="translate(3170,0)"><use x="0" xlink:href="#E40-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E40-MJMATHI-6B" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="4437" xlink:href="#E40-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5437" xlink:href="#E40-MJMATHI-62" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="5866" xlink:href="#E40-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(6396,0)"><use x="0" xlink:href="#E40-MJMATHI-68" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="814" xlink:href="#E40-MJMATHI-6D" xmlns:xlink="http://www.w3.org/1999/xlink" y="-213"></use></g><use x="7693" xlink:href="#E40-MJSZ1-29" xmlns:xlink="http://www.w3.org/1999/xlink" y="-1"></use></g><use x="9235" xlink:href="#E40-MJMAIN-223C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="10291" xlink:href="#E40-MJMATHI-44" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-40" type="math/tex">\alpha\left(\sum_{k\in\mathbb K}h_k+b \nu h_m\right) \sim D</script>，则有：<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-41-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="3.395ex" role="img" style="vertical-align: -1.172ex;" viewbox="0 -956.9 3612 1461.5" width="8.389ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M34 156Q34 270 120 356T309 442Q379 442 421 402T478 304Q484 275 485 237V208Q534 282 560 374Q564 388 566 390T582 393Q603 393 603 385Q603 376 594 346T558 261T497 161L486 147L487 123Q489 67 495 47T514 26Q528 28 540 37T557 60Q559 67 562 68T577 70Q597 70 597 62Q597 56 591 43Q579 19 556 5T512 -10H505Q438 -10 414 62L411 69L400 61Q390 53 370 41T325 18T267 -2T203 -11Q124 -11 79 39T34 156ZM208 26Q257 26 306 47T379 90L403 112Q401 255 396 290Q382 405 304 405Q235 405 183 332Q156 292 139 224T121 120Q121 71 146 49T208 26Z" id="E41-MJMATHI-3B1" stroke-width="0"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" id="E41-MJMAIN-3D" stroke-width="0"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" id="E41-MJMAIN-31" stroke-width="0"></path><path d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z" id="E41-MJMAIN-2B" stroke-width="0"></path><path d="M74 431Q75 431 146 436T219 442Q231 442 231 434Q231 428 185 241L137 51H140L150 55Q161 59 177 67T214 86T261 119T312 165Q410 264 445 394Q458 442 496 442Q509 442 519 434T530 411Q530 390 516 352T469 262T388 162T267 70T106 5Q81 -2 71 -2Q66 -2 59 -1T51 1Q45 5 45 11Q45 13 88 188L132 364Q133 377 125 380T86 385H65Q59 391 59 393T61 412Q65 431 74 431Z" id="E41-MJMATHI-3BD" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E41-MJMATHI-3B1" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="917" xlink:href="#E41-MJMAIN-3D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><g transform="translate(1695,0)"><g transform="translate(397,0)"><rect height="60" stroke="none" width="1398" x="0" y="220"></rect><use transform="scale(0.707)" x="738" xlink:href="#E41-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="571"></use><g transform="translate(60,-376)"><use transform="scale(0.707)" x="0" xlink:href="#E41-MJMAIN-31" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="500" xlink:href="#E41-MJMAIN-2B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use transform="scale(0.707)" x="1278" xlink:href="#E41-MJMATHI-3BD" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></g></g></g></svg></span><script id="MathJax-Element-41" type="math/tex">\alpha=\frac{1}{1+\nu}</script>。





## 七、Python API

### 7.1 数据接口

#### 7.1.1 数据格式

1. `xgboost` 的数据存储在`DMatrix` 对象中

2. `xgboost` 支持直接从下列格式的文件中加载数据：

    * `libsvm` 文本格式的文件。其格式为：

    ```
xxxxxxxxxx [label] [index1]:[value1] [index2]:[value2] ... [label] [index1]:[value1] [index2]:[value2] ... ...
    ```

    * `xgboost binary buffer` 文件


```
xxxxxxxxxxdtrain = xgb.DMatrix('train.svm.txt') #libsvm 格式dtest = xgb.DMatrix('test.svm.buffer') # xgboost binary buffer 文件
```

3. `xgboost` 也支持从二维的`numpy array` 中加载数据

```
xxxxxxxxxxdata = np.random.rand(5, 10)  label = np.random.randint(2, size=5) dtrain = xgb.DMatrix(data, label=label)#从 numpy array 中加载
```

4. 你也可以从`scipy.sparse array` 中加载数据

```
xxxxxxxxxxcsr = scipy.sparse.csr_matrix((dat, (row, col)))dtrain = xgb.DMatrix(csr)
```


#### 7.1.2 DMatrix

1. `DMatrix`： 由`xgboost` 内部使用的数据结构，它存储了数据集，并且针对了内存消耗和训练速度进行了优化。

```
xxxxxxxxxxxgboost.DMatrix(data, label=None, missing=None, weight=None, silent=False,      feature_names=None, feature_types=None, nthread=None)
```

    * 参数：

        * `data`：表示数据集。可以为：

            * 一个字符串，表示文件名。数据从该文件中加载
            * 一个二维的 `numpy array`， 表示数据集。

        * `label`：一个序列，表示样本标记。

        * `missing`： 一个值，它是缺失值的默认值。

        * `weight`：一个序列，给出了数据集中每个样本的权重。

        * `silent`： 一个布尔值。如果为`True`，则不输出中间信息。

        * `feature_names`： 一个字符串序列，给出了每一个特征的名字

        * `feature_types`： 一个字符串序列，给出了每个特征的数据类型

        * `nthread`：



2. 属性：

    * `feature_names`： 返回每个特征的名字
    * `feature_types`： 返回每个特征的数据类型

3. 方法：

    * `.get_base_margin()`： 返回一个浮点数，表示`DMatrix` 的 `base margin`。

    `.set_base_margin(margin)`： 设置`DMatrix` 的 `base margin`

        * 参数：`margin`： t一个序列，给出了每个样本的`prediction margin`

    * `.get_float_info(field)`： 返回一个`numpy array`， 表示`DMatrix` 的 `float property` 。

    `.set_float_info(field,data)`： 设置`DMatrix` 的 `float property` 。

    `.set_float_info_npy2d(field,data)`： 设置`DMatrix` 的 `float property` 。这里的`data` 是二维的`numpy array`

        * 参数：

            * `field`： 一个字符串，给出了`information` 的字段名。注：意义未知。
            * `data`： 一个`numpy array`，给出了数据集每一个点的`float information`


    * `.get_uint_info(field)`： 返回`DMatrix` 的 `unsigned integer property` 。

    `.set_unit_info(field,data)`： 设置`DMatrix` 的 `unsigned integer property` 。

        * 参数：

            * `field`： 一个字符串，给出了`information` 的字段名。注：意义未知。
            * `data`： 一个`numpy array`， 给出了数据集每个点的`uint information`

        * 返回值：一个`numpy array`，表示数据集的`unsigned integer information`


    * `.get_label()`： 返回一个`numpy array`，表示`DMatrix` 的 `label` 。

    `.set_label(label)`： 设置样本标记。

    `.set_label_npy2d(label)`： 设置样本标记。这里的`label` 为二维的`numpy array`

        * 参数： `label`： 一个序列，表示样本标记

    * `.get_weight()`： 一个`numpy array`，返回`DMatrix` 的样本权重。

    `.set_weight(weight)`： 设置样本权重。

    `.set_weight_npy2d(weight)`： 设置样本权重。这里的`weight` 为二维的`numpy array`

        * 参数：`weight`：一个序列，表示样本权重

    * `.num_col()`： 返回`DMatrix` 的列数

        * 返回值：一个整数，表示特征的数量

    * `.num_row()`： 返回`DMatrix` 的行数

        * 返回值：一个整数，表示样本的数量

    * `save_binary(fname,silent=True)`： 保存`DMatrix` 到一个 `xgboost buffer` 文件中

        * 参数：

            * `fname`： 一个字符串，表示输出的文件名
            * `silent`： 一个布尔值。如果为`True`，则不输出中间信息。


    * `.set_group(group)`： 设置`DMatrix` 每个组的大小（用于排序任务）

        * 参数：`group`： 一个序列，给出了每个组的大小

    * `slice(rindex)`： 切分`DMaxtrix` ，返回一个新的`DMatrix`。 该新的`DMatrix` 仅仅包含`rindex`

        * 参数：`rindex`： 一个列表，给出了要保留的`index`
        * 返回值：一个新的`DMatrix` 对象


4. 示例：

`data/train.svm.txt` 的内容：

```
xxxxxxxxxx1 1:1 2:21 1:2 2:31 1:3 2:41 1:4 2:50 1:5 2:60 1:6 2:70 1:7 2:80 1:8 2:9
```

测试代码：

```
​ximport xgboost as xgtimport numpy as np​class MatrixTest:  '''  测试 DMatrix  '''  def __init__(self):    self._matrix1 = xgt.DMatrix('data/train.svm.txt')    self._matrix2 = xgt.DMatrix(data=np.arange(0, 12).reshape((4, 3)),                        label=[1, 2, 3, 4], weight=[0.5, 0.4, 0.3, 0.2],                        silent=False, feature_names=['a', 'b', 'c'],                        feature_types=['int','int','float'], nthread=2)​  def print(self,matrix):    print('feature_names:%s'%matrix.feature_names)    print('feature_types:%s' % matrix.feature_types)  def run_get(self,matrix):    print('get_base_margin():', matrix.get_base_margin())    print('get_label():', matrix.get_label())    print('get_weight():', matrix.get_weight())    print('num_col():', matrix.num_col())    print('num_row():', matrix.num_row())​  def test(self):    print('查看 matrix1 :')    self.print(self._matrix1)    # feature_names:['f0', 'f1', 'f2']    # feature_types:None        print('\n查看 matrix2 :')    self.print(self._matrix2)    # feature_names:['a', 'b', 'c']    # feature_types:['int', 'int', 'float']        print('\n查看 matrix1 get:')    self.run_get(self._matrix1)    # get_base_margin(): []    # get_label(): [1. 1. 1. 1. 0. 0. 0. 0.]    # get_weight(): []    # num_col(): 3    # num_row(): 8        print('\n查看 matrix2 get:')    self.run_get(self._matrix2)    # get_base_margin(): []    # get_label(): [1. 2. 3. 4.]    # get_weight(): [0.5 0.4 0.3 0.2]    # num_col(): 3    # num_row(): 4        print(self._matrix2.slice([0,1]).get_label())    # [1. 2.]
```

​


### 7.2 模型接口

#### 7.2.1 Booster

1. `Booster` 是`xgboost` 的模型，它包含了训练、预测、评估等任务的底层实现。

```
xxxxxxxxxxxbgoost.Booster(params=None,cache=(),model_file=None)
```

    * 参数：

        * `params`： 一个字典，给出了模型的参数。

        该`Booster` 将调用`self.set_param(params)` 方法来设置模型的参数。

        * `cache`：一个列表，给出了缓存的项。其元素是`DMatrix` 的对象。模型从这些`DMatrix` 对象中读取特征名字和特征类型（要求这些`DMatrix` 对象具有相同的特征名字和特征类型）

        * `model_file`： 一个字符串，给出了模型文件的位置。

        如果给出了`model_file`，则调用`self.load_model(model_file)` 来加载模型。



2. 属性：

通过方法来存取、设置属性。

3. 方法：

    * `.attr(key)`： 获取`booster` 的属性。如果该属性不存在，则返回`None`

        * 参数：

            * `key`： 一个字符串，表示要获取的属性的名字


    * `.set_attr(**kwargs)`： 设置`booster` 的属性

        * 参数：`kwargs`： 关键字参数。注意：参数的值目前只支持字符串。

        如果参数的值为`None`，则表示删除该参数


    * `.attributes()`： 以字典的形式返回`booster` 的属性

    * `.set_param(params,value=None)`： 设置`booster` 的参数

        * 参数：

            * `params`： 一个列表（元素为键值对）、一个字典、或者一个字符串。表示待设置的参数
            * `value`： 如果`params` 为字符串，那么`params` 就是键，而`value`就是参数值。


    * `.boost(dtrain,grad,hess)`： 执行一次训练迭代

        * 参数：

            * `dtrain`： 一个 `DMatrix` 对象，表示训练集
            * `grad`： 一个列表，表示一阶的梯度
            * `hess`： 一个列表，表示二阶的偏导数


    * `.update(dtrain,iteration,fobj=None)`： 对一次迭代进行更新

        * 参数：

            * `dtrain`： 一个 `DMatrix` 对象，表示训练集
            * `iteration`： 一个整数，表示当前的迭代步数编号
            * `fobj`： 一个函数，表示自定义的目标函数


    由于`Booster` 没有`.train()` 方法，因此需要用下面的策略进行迭代：

    ```
xxxxxxxxxxfor i in range(0,100):      booster.update(train_matrix,iteration=i)
    ```

    * `.copy()`： 拷贝当前的`booster`，并返回一个新的`Booster` 对象

    * `.dump_model(fout,fmap='',with_stats=False)`： `dump` 模型到一个文本文件中。

        * 参数：

            * `fout`： 一个字符串，表示输出文件的文件名

            * `fmap`： 一个字符串，表示存储`feature map` 的文件的文件名。`booster` 需要从它里面读取特征的信息。

            该文件每一行依次代表一个特征。每一行的格式为：`feature name:feature type`。 其中`feature type` 为`int`、`float` 等表示数据类型的字符串。

            * `with_stats`： 一个布尔值。如果为`True`，则输出`split` 的统计信息



    * `.get_dump(fmap='',with_stats=False,dump_format='text')`： `dump` 模型为字符的列表（而不是存到文件中）。

        * 参数：

            * `fmap`： 一个字符串，表示存储`feature map` 的文件的文件名。`booster` 需要从它里面读取特征的信息。
            * `with_stats`： 一个布尔值。如果为`True`，则输出`split` 的统计信息
            * `dump_format`： 一个字符串，给出了输出的格式

        * 返回值：一个字符串的列表。每个字符串描述了一棵子树。


    * `.eval(data,name='eval',iteration=0)`： 对模型进行评估

        * 参数：

            * `data`： 一个`DMatrix` 对象，表示数据集
            * `name`： 一个字符串，表示数据集的名字
            * `iteration`： 一个整数，表示当前的迭代编号

        * 返回值：一个字符串，表示评估结果


    * `.eval_set(evals,iteration=0,feval=None)`： 评估一系列的数据集

        * 参数：

            * `evals`： 一个列表，列表元素为元组`(DMatrix,string)`， 它给出了待评估的数据集
            * `iteration`： 一个整数，表示当前的迭代编号
            * `feval`： 一个函数，给出了自定义的评估函数

        * 返回值：一个字符串，表示评估结果


    * `.get_fscore(fmap='')`： 返回每个特征的重要性

        * 参数：

            * `fmap`： 一个字符串，给出了`feature map` 文件的文件名。`booster` 需要从它里面读取特征的信息。

        * 返回值：一个字典，给出了每个特征的重要性


    * `.get_score(fmap='',importance_type='weight')`： 返回每个特征的重要性

        * 参数：

            * `fmap`： 一个字符串，给出了`feature map` 文件的文件名。`booster` 需要从它里面读取特征的信息。

            * `importance_type`： 一个字符串，给出了特征的衡量指标。可以为：

                * `'weight'`： 此时特征重要性衡量标准为：该特征在所有的树中，被用于划分数据集的总次数。
                * `'gain'`： 此时特征重要性衡量标准为：该特征在树的`'cover'` 中，获取的平均增益。


        * 返回值：一个字典，给出了每个特征的重要性


    * `.get_split_value_histogram(feature,fmap='',bins=None,as_pandas=True)`： 获取一个特征的划分`value histogram`。

        * 参数：

            * `feature`： 一个字符串，给出了划分特征的名字
            * `fmap`： 一个字符串，给出了`feature map` 文件的文件名。`booster` 需要从它里面读取特征的信息。
            * `bins`： 最大的分桶的数量。如果`bins=None` 或者 `bins>n_unique`，则分桶的数量实际上等于`n_unique`。 其中 `n_unique` 是划分点的值的`unique`
            * `as_pandas` ：一个布尔值。如果为`True`，则返回一个`pandas.DataFrame`； 否则返回一个`numpy ndarray`。

        * 返回值：以一个`numpy ndarray` 或者 `pandas.DataFrame` 形式返回的、代表拆分点的`histogram` 的结果。


    * `.load_model(fname)`： 从文件中加载模型。

        * 参数：`fname`： 一个文件或者一个内存`buffer`， `xgboost` 从它加载模型

    * `.save_model(fname)`： 保存模型到文件中

        * 参数：`fname`： 一个字符串，表示文件名

    * `save_raw()`： 将模型保存成内存`buffer`

        * 返回值：一个内存`buffer`，代表该模型

    * `.load_rabit_checkpoint()`： 从`rabit checkpoint` 中初始化模型。

        * 返回值：一个整数，表示模型的版本号

    * `.predict(data,output_margin=False,ntree_limit=0,pred_leaf=False,pred_contribs=False,approx_contribs=False)`： 执行预测

    >     > 

    > 该方法不是线程安全的。对于每个 `booster` 来讲，你只能在某个线程中调用它的`.predict` 方法。如果你在多个线程中调用`.predict` 方法，则可能会有问题。

    > 

    > 要想解决该问题，你必须在每个线程中调用`booster.copy()` 来拷贝该`booster` 到每个线程中



        * 参数：

            * `data`： 一个 `DMatrix` 对象，表示测试集

            * `output_margin`： 一个布尔值。表示是否输出原始的、未经过转换的`margin value`

            * `ntree_limit`： 一个整数。表示使用多少棵子树来预测。默认值为0，表示使用所有的子树。

            如果训练的时候发生了早停，则你可以使用`booster.best_ntree_limit`。

            * `pred_leaf`： 一个布尔值。如果为`True`，则会输出每个样本在每个子树的哪个叶子上。它是一个`nsample x ntrees` 的矩阵。

            每个子树的叶节点都是从`1` 开始编号的。

            * `pred_contribs`： 一个布尔值。如果为`True`， 则输出每个特征对每个样本预测结果的贡献程度。它是一个`nsample x ( nfeature+1)` 的矩阵。

            之所以加1，是因为有`bias` 的因素。它位于最后一列。

            其中样本所有的贡献程度相加，就是该样本最终的预测的结果。

            * `approx_contribs`： 一个布尔值。如果为`True`，则大致估算出每个特征的贡献程度。


        * 返回值：一个`ndarray`，表示预测结果



4. `Booster` 没有 `train` 方法。因此有两种策略来获得训练好的 `Booster`

    * 从训练好的模型的文件中`.load_model()` 来获取
    * 多次调用`.update()` 方法

5. 示例：

```
xxxxxxxxxximport xgboost as xgtimport numpy as npimport pandas as pdfrom sklearn.model_selection import train_test_split​_label_map={  # 'Iris-setosa':0, #经过裁剪的，去掉了 iris 中的 setosa 类  'Iris-versicolor':0,  'Iris-virginica':1}class BoosterTest:  '''  测试 Booster  '''  def __init__(self):    df=pd.read_csv('./data/iris.csv')    _feature_names=['Sepal Length','Sepal Width','Petal Length','Petal Width']    x=df[_feature_names]    y=df['Class'].map(lambda x:_label_map[x])​    train_X,test_X,train_Y,test_Y=train_test_split(x,y,            test_size=0.3,stratify=y,shuffle=True,random_state=1)    self._train_matrix=xgt.DMatrix(data=train_X,label=train_Y,                        eature_names=_feature_names,                        feature_types=['float','float','float','float'])    self._validate_matrix = xgt.DMatrix(data=test_X, label=test_Y,                         feature_names=_feature_names,                        feature_types=['float', 'float', 'float', 'float'])    self._booster=xgt.Booster(params={      'booster':'gbtree',      'silent':0,#打印消息      'eta':0.1, #学习率      'max_depth':5,      'tree_method':'exact',      'objective':'binary:logistic',      'eval_metric':'auc',      'seed':321},      cache=[self._train_matrix,self._validate_matrix])​  def test_attribute(self):    '''    测试属性的设置和获取    :return:    '''    self._booster.set_attr(key1= '1')    print('attr:key1 -> ',self._booster.attr('key1'))    print('attr:key2 -> ',self._booster.attr('key2'))    print('attributes -> ',self._booster.attributes())  def test_dump_model(self):    '''    测试 dump 模型    :return:    '''    _dump_str=self._booster.get_dump(fmap='model/booster.feature',                                     with_stats=True,dump_format='text')    print('dump:',_dump_str[0][:20]+'...' if _dump_str else [])    self._booster.dump_model('model/booster.model',                             fmap='model/booster.feature',with_stats=True)  def test_train(self):    '''    训练    :return:    '''    for i in range(0,100):      self._booster.update(self._train_matrix,iteration=i)      print(self._booster.eval(self._train_matrix, name='train', iteration=i))      print(self._booster.eval(self._validate_matrix,name='eval',iteration=i))  def test_importance(self):    '''    测试特征重要性    :return:    '''    print('fscore:',self._booster.get_fscore('model/booster.feature'))    print('score.weight:', self._booster.get_score(importance_type='weight'))    print('score.gain:', self._booster.get_score(importance_type='gain'))​  def test(self):    self.test_attribute()    # attr:key1 ->  1    # attr:key2 ->  None    # attributes ->  {'key1': '1'}    self.test_dump_model()    # dump: []    self.test_train()    # [0]   train-auc:0.980816    # [0]   eval-auc:0.933333    # ...    # [99]  train-auc:0.998367    # [99]  eval-auc:0.995556    self.test_dump_model()    # dump: 0:[f2<4.85] yes=1,no...    self.test_importance()    # score: {'f2': 80, 'f3': 72, 'f0': 6, 'f1': 5}    # score.weight: {'Petal Length': 80, 'Petal Width': 72, 'Sepal Length': 6, 'Sepal Width': 5}    # score.gain: {'Petal Length': 3.6525380337500004, 'Petal Width': 2.2072901486111114, 'Sepal Length': 0.06247816666666667, 'Sepal Width': 0.09243024}​if __name__ == '__main__':  BoosterTest().test()
```


#### 7.2.2 直接学习

1. `xgboost.train()`： 使用给定的参数来训练一个`booster`

```
xxxxxxxxxxxgboost.train(params, dtrain, num_boost_round=10, evals=(), obj=None, feval=None,   maximize=False, early_stopping_rounds=None, evals_result=None, verbose_eval=True,   xgb_model=None, callbacks=None, learning_rates=None)
```

    * 参数：

        * `params`： 一个列表（元素为键值对）、一个字典，表示训练的参数

        * `dtrain`：一个`DMatrix` 对象，表示训练集

        * `num_boost_round`： 一个整数，表示`boosting` 迭代数量

        * `evals`： 一个列表，元素为`(DMatrix,string)`。 它给出了训练期间的验证集，以及验证集的名字（从而区分验证集的评估结果）。

        * `obj`：一个函数，它表示自定义的目标函数

        * `feval`： 一个函数，它表示自定义的`evaluation` 函数

        * `maximize`： 一个布尔值。如果为`True`，则表示是对`feval` 求最大值；否则为求最小值

        * `early_stopping_rounds`：一个整数，表示早停参数。

        如果在`early_stopping_rounds` 个迭代步内，验证集的验证误差没有下降，则训练停止。

            * 该参数要求`evals` 参数至少包含一个验证集。如果`evals` 参数包含了多个验证集，则使用最后的一个。

            * 返回的模型是最后一次迭代的模型（而不是最佳的模型）。

            * 如果早停发生，则模型拥有三个额外的字段：

                * `.best_score`： 最佳的分数
                * `.best_iteration`： 最佳的迭代步数
                * `.best_ntree_limit`： 最佳的子模型数量


        * `evals_result`： 一个字典，它给出了对测试集要进行评估的指标。

        * `verbose_eval`： 一个布尔值或者整数。

            * 如果为`True`，则`evalutation metric` 将在每个`boosting stage` 打印出来
            * 如果为一个整数，则`evalutation metric` 将在每隔`verbose_eval`个`boosting stage` 打印出来。另外最后一个`boosting stage`，以及早停的`boosting stage` 的 `evalutation metric` 也会被打印

        * `learning_rates`： 一个列表，给出了每个迭代步的学习率。

            * 你可以让学习率进行衰减

        * `xgb_model`： 一个`Booster`实例，或者一个存储了`xgboost` 模型的文件的文件名。它给出了待训练的模型。

        这种做法允许连续训练。

        * `callbacks`： 一个回调函数的列表，它给出了在每个迭代步结束之后需要调用的那些函数。

        你可以使用`xgboost` 中预定义的一些回调函数（位于`xgboost.callback` 模块） 。如：

        `xgboost.reset_learning_rate(custom_rates)`


    * 返回值：一个`Booster` 对象，表示训练好的模型


2. `xgboost.cv()`： 使用给定的参数执行交叉验证 。它常用作参数搜索 。

```
xxxxxxxxxxxgboost.cv(params, dtrain, num_boost_round=10, nfold=3, stratified=False, folds=None,     metrics=(), obj=None, feval=None, maximize=False, early_stopping_rounds=None,     fpreproc=None, as_pandas=True, verbose_eval=None, show_stdv=True, seed=0,     callbacks=None, shuffle=True)
```

    * 参数：

        * `params`： 一个列表（元素为键值对）、一个字典，表示训练的参数

        * `dtrain`：一个`DMatrix` 对象，表示训练集

        * `num_boost_round`： 一个整数，表示`boosting` 迭代数量

        * `nfold`： 一个整数，表示交叉验证的`fold` 的数量

        * `stratified`： 一个布尔值。如果为`True`，则执行分层采样

        * `folds`： 一个`scikit-learn` 的 `KFold` 实例或者`StratifiedKFold` 实例。

        * `metrics`：一个字符串或者一个字符串的列表，指定了交叉验证时的`evaluation metrics`

        如果同时在`params` 里指定了`eval_metric`，则`metrics` 参数优先。

        * `obj`：一个函数，它表示自定义的目标函数

        * `feval`： 一个函数，它表示自定义的`evaluation` 函数

        * `maximize`： 一个布尔值。如果为`True`，则表示是对`feval` 求最大值；否则为求最小值

        * `early_stopping_rounds`：一个整数，表示早停参数。

        如果在`early_stopping_rounds` 个迭代步内，验证集的验证误差没有下降，则训练停止。

            * 返回`evaluation history` 结果中的最后一项是最佳的迭代步的评估结果

        * `fpreproc`： 一个函数。它是预处理函数，其参数为`(dtrain,dtest,param)`， 返回值是经过了变换之后的 `(dtrain,dtest,param)`

        * `as_pandas`： 一个布尔值。如果为`True`，则返回一个`pandas.DataFrame` ；否则返回一个`numpy.ndarray`

        * `verbose_eval`： 参考 `xgboost.train()`

        * `show_stdv`： 一个布尔值。是否`verbose` 中打印标准差。

        它对返回结果没有影响。返回结果始终包含标准差。

        * `seed`： 一个整数，表示随机数种子

        * `callbacks`： 参考 `xgboost.train()`

        * `shuffle`： 一个布尔值。如果为`True`，则创建`folds` 之前先混洗数据。


    * 返回值：一个字符串的列表，给出了`evaluation history` 。它给的是早停时刻的`history`(此时对应着最优模型)，早停之后的结果被抛弃。


3. 示例：

```
xxxxxxxxxxclass TrainTest:  def __init__(self):    df = pd.read_csv('./data/iris.csv')    _feature_names = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']    x = df[_feature_names]    y = df['Class'].map(lambda x: _label_map[x])​    train_X, test_X, train_Y, test_Y = train_test_split(x, y, test_size=0.3,                 stratify=y, shuffle=True, random_state=1)    self._train_matrix = xgt.DMatrix(data=train_X, label=train_Y,                 feature_names=_feature_names,                feature_types=['float', 'float', 'float', 'float'])    self._validate_matrix = xgt.DMatrix(data=test_X, label=test_Y,                feature_names=_feature_names,                feature_types=['float', 'float', 'float', 'float'])​  def train_test(self):    params={      'booster':'gbtree',      'eta':0.01,      'max_depth':5,      'tree_method':'exact',      'objective':'binary:logistic',      'eval_metric':['logloss','error','auc']    }    eval_rst={}    booster=xgt.train(params,self._train_matrix,num_boost_round=20,         evals=([(self._train_matrix,'valid1'),(self._validate_matrix,'valid2')]),         early_stopping_rounds=5,evals_result=eval_rst,verbose_eval=True)    ## 训练输出    # Multiple eval metrics have been passed: 'valid2-auc' will be used for early stopping.    # Will train until valid2-auc hasn't improved in 5 rounds.    # [0]   valid1-logloss:0.685684 valid1-error:0.042857   valid1-auc:0.980816 valid2-logloss:0.685749 valid2-error:0.066667   valid2-auc:0.933333    # ...    # Stopping. Best iteration:    # [1]   valid1-logloss:0.678149 valid1-error:0.042857   valid1-auc:0.99551  valid2-logloss:0.677882 valid2-error:0.066667   valid2-auc:0.966667        print('booster attributes:',booster.attributes())    # booster attributes: {'best_iteration': '1', 'best_msg': '[1]\tvalid1-logloss:0.678149\tvalid1-error:0.042857\tvalid1-auc:0.99551\tvalid2-logloss:0.677882\tvalid2-error:0.066667\tvalid2-auc:0.966667', 'best_score': '0.966667'}         print('fscore:', booster.get_fscore())    # fscore: {'Petal Length': 8, 'Petal Width': 7}        print('eval_rst:',eval_rst)    # eval_rst: {'valid1': {'logloss': [0.685684, 0.678149, 0.671075, 0.663787, 0.656948, 0.649895], 'error': [0.042857, 0.042857, 0.042857, 0.042857, 0.042857, 0.042857], 'auc': [0.980816, 0.99551, 0.99551, 0.99551, 0.99551, 0.99551]}, 'valid2': {'logloss': [0.685749, 0.677882, 0.670747, 0.663147, 0.656263, 0.648916], 'error': [0.066667, 0.066667, 0.066667, 0.066667, 0.066667, 0.066667], 'auc': [0.933333, 0.966667, 0.966667, 0.966667, 0.966667, 0.966667]}}      def cv_test(self):    params = {      'booster': 'gbtree',      'eta': 0.01,      'max_depth': 5,      'tree_method': 'exact',      'objective': 'binary:logistic',      'eval_metric': ['logloss', 'error', 'auc']    }​    eval_history = xgt.cv(params, self._train_matrix,num_boost_round=20,          nfold=3,stratified=True,metrics=['error', 'auc'],         early_stopping_rounds=5,verbose_eval=True,shuffle=True)    ## 训练输出    # [0]   train-auc:0.974306+0.00309697   train-error:0.0428743+0.0177703 test-auc:0.887626+0.0695933 test-error:0.112374+0.0695933    #....    print('eval_history:', eval_history)    # eval_history:    test-auc-mean  test-auc-std  test-error-mean  test-error-std  \    # 0       0.887626      0.069593         0.112374        0.069593       # 1       0.925821      0.020752         0.112374        0.069593       # 2       0.925821      0.020752         0.098485        0.050631   ​    # train-auc-mean  train-auc-std  train-error-mean  train-error-std      # 0        0.974306       0.003097          0.042874          0.01777      # 1        0.987893       0.012337          0.042874          0.01777      # 2        0.986735       0.011871          0.042874          0.01777
```


#### 7.2.3 Scikit-Learn API

1. `xgboost` 给出了针对`scikit-learn` 接口的`API`

2. `xgboost.XGBRegressor`： 它实现了`scikit-learn` 的回归模型`API`

```
xxxxxxxxxxclass xgboost.XGBRegressor(max_depth=3, learning_rate=0.1, n_estimators=100,      silent=True, objective='reg:linear', booster='gbtree', n_jobs=1, nthread=None,      gamma=0, min_child_weight=1, max_delta_step=0, subsample=1, colsample_bytree=1,     colsample_bylevel=1, reg_alpha=0, reg_lambda=1, scale_pos_weight=1,      base_score=0.5, random_state=0, seed=None, missing=None, **kwargs)
```

参数：

    * `max_depth`： 一个整数，表示子树的最大深度

    * `learning_rate`： 一个浮点数，表示学习率

    * `n_estimators`：一个整数，表示预期需要学习的子树的数量

    * `silent`： 一个布尔值。如果为`False`，则打印中间信息

    * `objective`： 一个字符串或者可调用对象，指定了目标函数。其函数签名为：`objective(y_true,y_pred) -> gra,hess`。 其中：

        * `y_true`： 一个形状为`[n_sample]` 的序列，表示真实的标签值
        * `y_pred`： 一个形状为`[n_sample]` 的序列，表示预测的标签值
        * `grad`： 一个形状为`[n_sample]` 的序列，表示每个样本处的梯度
        * `hess`： 一个形状为`[n_sample]` 的序列，表示每个样本处的二阶偏导数

    * `booster`： 一个字符串。指定了用哪一种基模型。可以为：`'gbtree','gblinear','dart'`

    * `n_jobs`： 一个整数，指定了并行度，即开启多少个线程来训练。如果为`-1`，则使用所有的`CPU`

    * `gamma`： 一个浮点数，也称作最小划分损失`min_split_loss`。 它刻画的是：对于一个叶子节点，当对它采取划分之后，损失函数的降低值的阈值。

        * 如果大于该阈值，则该叶子节点值得继续划分
        * 如果小于该阈值，则该叶子节点不值得继续划分

    * `min_child_weight`： 一个整数，子节点的权重阈值。它刻画的是：对于一个叶子节点，当对它采取划分之后，它的所有子节点的权重之和的阈值。

        * 如果它的所有子节点的权重之和大于该阈值，则该叶子节点值得继续划分
        * 如果它的所有子节点的权重之和小于该阈值，则该叶子节点不值得继续划分

    所谓的权重：

        * 对于线性模型(`booster=gblinear`)，权重就是：叶子节点包含的样本数量。 因此该参数就是每个节点包含的最少样本数量。
        * 对于树模型（`booster=gbtree,dart`），权重就是：叶子节点包含样本的所有二阶偏导数之和。

    * `max_delta_step`： 一个整数，每棵树的权重估计时的最大`delta step`。取值范围为<span class="MathJax_Preview"></span><span class="MathJax_SVG" id="MathJax-Element-42-Frame" style="font-size: 100%; display: inline-block;" tabindex="-1"><svg focusable="false" height="2.577ex" role="img" style="vertical-align: -0.705ex;" viewbox="0 -806.1 2500.7 1109.7" width="5.808ex" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M118 -250V750H255V710H158V-210H255V-250H118Z" id="E42-MJMAIN-5B" stroke-width="0"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" id="E42-MJMAIN-30" stroke-width="0"></path><path d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z" id="E42-MJMAIN-2C" stroke-width="0"></path><path d="M55 217Q55 305 111 373T254 442Q342 442 419 381Q457 350 493 303L507 284L514 294Q618 442 747 442Q833 442 888 374T944 214Q944 128 889 59T743 -11Q657 -11 580 50Q542 81 506 128L492 147L485 137Q381 -11 252 -11Q166 -11 111 57T55 217ZM907 217Q907 285 869 341T761 397Q740 397 720 392T682 378T648 359T619 335T594 310T574 285T559 263T548 246L543 238L574 198Q605 158 622 138T664 94T714 61T765 51Q827 51 867 100T907 217ZM92 214Q92 145 131 89T239 33Q357 33 456 193L425 233Q364 312 334 337Q285 380 233 380Q171 380 132 331T92 214Z" id="E42-MJMAIN-221E" stroke-width="0"></path><path d="M22 710V750H159V-250H22V-210H119V710H22Z" id="E42-MJMAIN-5D" stroke-width="0"></path></defs><g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"><use x="0" xlink:href="#E42-MJMAIN-5B" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="278" xlink:href="#E42-MJMAIN-30" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="778" xlink:href="#E42-MJMAIN-2C" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="1222" xlink:href="#E42-MJMAIN-221E" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use><use x="2222" xlink:href="#E42-MJMAIN-5D" xmlns:xlink="http://www.w3.org/1999/xlink" y="0"></use></g></svg></span><script id="MathJax-Element-42" type="math/tex">[0,\infty]</script>，0 表示没有限制，默认值为 0 。

    * `subsample`：一个浮点数，对训练样本的采样比例。取值范围为 `(0,1]`，默认值为 1 。

    如果为 `0.5`， 表示随机使用一半的训练样本来训练子树。它有助于缓解过拟合。

    * `colsample_bytree`： 一个浮点数，构建子树时，对特征的采样比例。取值范围为 `(0,1]`， 默认值为 1。

    如果为 `0.5`， 表示随机使用一半的特征来训练子树。它有助于缓解过拟合。

    * `colsample_bylevel`： 一个浮点数，寻找划分点时，对特征的采样比例。取值范围为 `(0,1]`， 默认值为 1。

    如果为 `0.5`， 表示随机使用一半的特征来寻找最佳划分点。它有助于缓解过拟合。

    * `reg_alpha`： 一个浮点数，是`L1` 正则化系数。它是`xgb` 的`alpha` 参数

    * `reg_lambda`： 一个浮点数，是`L2` 正则化系数。它是`xgb` 的`lambda` 参数

    * `scale_pos_weight`： 一个浮点数，用于调整正负样本的权重，常用于类别不平衡的分类问题。默认为 1。

    一个典型的参数值为： `负样本数量/正样本数量`

    * `base_score`：一个浮点数， 给所有样本的一个初始的预测得分。它引入了全局的`bias`

    * `random_state`： 一个整数，表示随机数种子。

    * `missing`： 一个浮点数，它的值代表发生了数据缺失。默认为`np.nan`

    * `kwargs`： 一个字典，给出了关键字参数。它用于设置`Booster` 对象


3. `xgboost.XGBClassifier` ：它实现了`scikit-learn` 的分类模型`API`

```
xxxxxxxxxxclass xgboost.XGBClassifier(max_depth=3, learning_rate=0.1, n_estimators=100,      silent=True, objective='binary:logistic', booster='gbtree', n_jobs=1,     nthread=None, gamma=0, min_child_weight=1, max_delta_step=0, subsample=1,     colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lambda=1,     scale_pos_weight=1, base_score=0.5, random_state=0, seed=None,      missing=None, **kwargs)
```

参数参考`xgboost.XGBRegressor`

4. `xgboost.XGBClassifier` 和 `xgboost.XGBRegressor` 的方法：

    * `.fit()`： 训练模型

    ```
xxxxxxxxxxfit(X, y, sample_weight=None, eval_set=None, eval_metric=None,    early_stopping_rounds=None,verbose=True, xgb_model=None)
    ```

    参数：

        * `X`： 一个`array-like`，表示训练集

        * `y`： 一个序列，表示标记

        * `sample_weight`： 一个序列，给出了每个样本的权重

        * `eval_set`： 一个列表，元素为`(X,y)`，给出了验证集及其标签。它们用于早停。

        如果有多个验证集，则使用最后一个

        * `eval_metric`： 一个字符串或者可调用对象，用于`evaluation metric`

            * 如果为字符串，则是内置的度量函数的名字
            * 如果为可调用对象，则它的签名为`(y_pred,y_true)==>(str,value)`

        * `early_stopping_rounds`： 指定早停的次数。参考`xgboost.train()`

        * `verbose`： 一个布尔值。如果为`True`，则打印验证集的评估结果。

        * `xgb_model`：一个`Booster`实例，或者一个存储了`xgboost` 模型的文件的文件名。它给出了待训练的模型。

        这种做法允许连续训练。


    * `.predict()`：执行预测

    ```
xxxxxxxxxxpredict(data, output_margin=False, ntree_limit=0)
    ```

    参数:

        * `data`： 一个 `DMatrix` 对象，表示测试集

        * `output_margin`： 一个布尔值。表示是否输出原始的、未经过转换的`margin value`

        * `ntree_limit`： 一个整数。表示使用多少棵子树来预测。默认值为0，表示使用所有的子树。

        如果训练的时候发生了早停，则你可以使用`booster.best_ntree_limit`。


    返回值：一个`ndarray`，表示预测结果

        * 对于回归问题，返回的就是原始的预测结果
        * 对于分类问题，返回的就是预测类别(阈值为 0.5 )

    * `.predict_proba(data, output_margin=False, ntree_limit=0)` ： 执行预测，预测的是各类别的概率

    参数：参考`.predict()`

    返回值：一个`ndarray`，表示预测结果

    >     > 

    > 它只用于分类问题，返回的是预测各类别的概率



    * `.evals_result()`： 返回一个字典，给出了各个验证集在各个验证参数上的历史值

    它不同于`cv()` 函数的返回值。`cv()` 函数返回`evaluation history` 是早停时刻的。而这里返回的是所有的历史值


5. 示例：

```
xxxxxxxxxxclass SKLTest:  def __init__(self):    df = pd.read_csv('./data/iris.csv')    _feature_names = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']    x = df[_feature_names]    y = df['Class'].map(lambda x: _label_map[x])​    self.train_X, self.test_X, self.train_Y, self.test_Y = \      train_test_split(x, y, test_size=0.3, stratify=y, shuffle=True, random_state=1)        def train_test(self):    clf=xgt.XGBClassifier(max_depth=3,learning_rate=0.1,n_estimators=100)    clf.fit(self.train_X,self.train_Y,eval_metric='auc',            eval_set=[( self.test_X,self.test_Y),],            early_stopping_rounds=3)    # 训练输出:    # Will train until validation_0-auc hasn't improved in 3 rounds.    # [0]   validation_0-auc:0.933333    # ...    # Stopping. Best iteration:    # [2]   validation_0-auc:0.997778    print('evals_result:',clf.evals_result())    # evals_result: {'validation_0': {'auc': [0.933333, 0.966667, 0.997778, 0.997778, 0.997778]}}    print('predict:',clf.predict(self.test_X))    # predict: [1 1 0 0 0 1 1 1 0 0 0 1 1 0 1 1 0 1 0 0 0 0 0 1 1 0 0 1 1 0]
```


### 7.3 绘图API

1. `xgboost.plot_importance()`：绘制特征重要性

```
xxxxxxxxxxxgboost.plot_importance(booster, ax=None, height=0.2, xlim=None, ylim=None,       title='Feature importance', xlabel='F score', ylabel='Features',       importance_type='weight', max_num_features=None, grid=True,        show_values=True, **kwargs)
```

参数：

    * `booster`： 一个`Booster`对象， 一个 `XGBModel` 对象，或者由`Booster.get_fscore()` 返回的字典

    * `ax`： 一个`matplotlib Axes` 对象。特征重要性将绘制在它上面。

    如果为`None`，则新建一个`Axes`

    * `grid`： 一个布尔值。如果为`True`，则开启`axes grid`

    * `importance_type`： 一个字符串，指定了特征重要性的类别。参考`Booster.get_fscore()`

    * `max_num_features`： 一个整数，指定展示的特征的最大数量。如果为`None`，则展示所有的特征

    * `height`： 一个浮点数，指定`bar` 的高度。它传递给`ax.barh()`

    * `xlim`： 一个元组，传递给 `axes.xlim()`

    * `ylim`： 一个元组，传递给 `axes.ylim()`

    * `title`： 一个字符串，设置`Axes` 的标题。默认为`"Feature importance"`。 如果为`None`，则没有标题

    * `xlabel`： 一个字符串，设置`Axes` 的`X` 轴标题。默认为`"F score"`。 如果为`None`，则`X` 轴没有标题

    * `ylabel`：一个字符串，设置`Axes` 的`Y` 轴标题。默认为`"Features"`。 如果为`None`，则`Y` 轴没有标题

    * `show_values`： 一个布尔值。如果为`True`，则在绘图上展示具体的值。

    * `kwargs`： 关键字参数，用于传递给`ax.barh()`


返回`ax` （一个`matplotlib Axes` 对象）

2. `xgboost.plot_tree()`： 绘制指定的子树。

```
xxxxxxxxxxxgboost.plot_tree(booster, fmap='', num_trees=0, rankdir='UT', ax=None, **kwargs)
```

参数：

    * `booster`： 一个`Booster`对象， 一个 `XGBModel` 对象

    * `fmap`： 一个字符串，给出了`feature map` 文件的文件名

    * `num_trees`： 一个整数，制定了要绘制的子数的编号。默认为 0

    * `rankdir`： 一个字符串，它传递给`graphviz`的`graph_attr`

    * `ax`： 一个`matplotlib Axes` 对象。特征重要性将绘制在它上面。

    如果为`None`，则新建一个`Axes`

    * `kwargs`： 关键字参数，用于传递给`graphviz` 的`graph_attr`


返回`ax` （一个`matplotlib Axes` 对象）

3. `xgboost.tp_graphviz()`： 转换指定的子树成一个`graphviz` 实例。

在`IPython`中，可以自动绘制`graphviz` 实例；否则你需要手动调用`graphviz` 对象的`.render()` 方法来绘制。

```
xxxxxxxxxxxgboost.to_graphviz(booster, fmap='', num_trees=0, rankdir='UT', yes_color='#0000FF',     no_color='#FF0000', **kwargs)
```

参数：

    * `yes_color`： 一个字符串，给出了满足`node condition` 的边的颜色
    * `no_color`： 一个字符串，给出了不满足`node condition` 的边的颜色
    * 其它参数参考 `xgboost.plot_tree()`

返回`ax` （一个`matplotlib Axes` 对象）

4. 示例：

```
xxxxxxxxxxclass PlotTest:  def __init__(self):    df = pd.read_csv('./data/iris.csv')    _feature_names = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']    x = df[_feature_names]    y = df['Class'].map(lambda x: _label_map[x])​    train_X, test_X, train_Y, test_Y = train_test_split(x, y,           test_size=0.3, stratify=y, shuffle=True, random_state=1)    self._train_matrix = xgt.DMatrix(data=train_X, label=train_Y,              feature_names=_feature_names,             feature_types=['float', 'float', 'float', 'float'])    self._validate_matrix = xgt.DMatrix(data=test_X, label=test_Y,              feature_names=_feature_names,             feature_types=['float', 'float', 'float', 'float'])​  def plot_test(self):    params = {      'booster': 'gbtree',      'eta': 0.01,      'max_depth': 5,      'tree_method': 'exact',      'objective': 'binary:logistic',      'eval_metric': ['logloss', 'error', 'auc']    }    eval_rst = {}    booster = xgt.train(params, self._train_matrix,             num_boost_round=20, evals=([(self._train_matrix, 'valid1'),                                         (self._validate_matrix, 'valid2')]),             early_stopping_rounds=5, evals_result=eval_rst, verbose_eval=True)    xgt.plot_importance(booster)    plt.show()
```

![xgb_importance](../imgs/xgb_importance.png)



</body>