How to USE?
============

帮助命令::

    ./run.sh <option>
    OPTIONS:
        -b, build               Build package.
        -d, dist                Distribute package. (Source/Wheel)
        -u, upload              Upload package.(PYPA)
        -c, clean               Clean all temp files.
        -cpc, clean_pip_cache   Clean pip cache directory.


Upload package
================

step 1: 首先需要配置pip上传目的源, 添加文件~/.pypirc

文件内容::

    [distutils]
    index-servers=pypi

    [pypi]
    repository=https://upload.pypi.org/legacy/  # <your repo url>
    username=<your username>
    password=<your password>

step 2: 然后执行upload命令,将package上传到目的源.

命令::

    ./run.sh upload
