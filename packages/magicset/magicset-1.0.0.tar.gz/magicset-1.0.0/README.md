#### magicbox
    magicset常用组件集合。update:2020-11-12,  By:8034.com

#### magicbox 功能列表：

    1) 按规则生成身份证号 
    2) 图片简易处理 -> Require: pip install Pillow
    3）


 
#### 使用说明：




## 扩展

    ## 打包 检查
    python setup.py check 
    ## 打包 生成
    python setup.py sdist
    ## 上传
    twine upload dist/*
    ## 使用
    pip install magicset 
    ## 更新
    pip install --upgrade magicset
    ## 卸载
    pip uninstall -y magicset 

## MANIFEST.in 
    include pat1 pat2 ...   #include all files matching any of the listed patterns
    exclude pat1 pat2 ...   #exclude all files matching any of the listed patterns
    recursive-include dir pat1 pat2 ...  #include all files under dir matching any of the listed patterns
    recursive-exclude dir pat1 pat2 ... #exclude all files under dir matching any of the listed patterns
    global-include pat1 pat2 ...    #include all files anywhere in the source tree 
    matching — & any of the listed patterns
    global-exclude pat1 pat2 ...    #exclude all files anywhere in the source tree matching — & any of the listed patterns
    prune dir   #exclude all files under dir
    graft dir   #include all files under dir
