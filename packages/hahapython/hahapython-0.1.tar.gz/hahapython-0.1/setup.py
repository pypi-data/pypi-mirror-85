#conding:utf-8
#通过setuptools模块导入所需的函数
from setuptools import setup,find_packages
setup(
       name="hahapython",
       version="0.1",
       author="伊泽瑞尔",
       url="http://www.baidu.com",
       packages=find_packages("src"),  #src就是模块的保存目录
       package_dir ={"":"src"},  #告诉setuptools包都在src下
       package_data={    #配置其他的文件的打包处理
       #任何包中含有.txt文件，都包含它
       "":["*.txt","*.info","*.properties"],
       #包含demo包data文件夹中的*.bat文件
       "":["data/*.*"]
       },
       exclude=["*.test","*.test.*","test.*","test"] #取消所有的测试包
 )