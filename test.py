import json
import os
import shutil

import yaml
import logging

from pathlib import Path

logger = logging.getLogger()


def create_strm_file(dest_file, dest_dir, library_dir):
    """
    生成strm文件
    :param dest_file:
    :param dest_dir:
    :param library_dir:
    :return:
    """
    try:
        # 获取视频文件名和目录
        video_name = Path(dest_file).name

        dest_path = Path(dest_file).parent

        # 构造.strm文件路径
        strm_path = os.path.join(dest_path, f"{os.path.splitext(video_name)[0]}.strm")

        if os.path.exists(strm_path):
            print(f"strm文件已存在，跳过处理::: {strm_path}")
            return

        # 本地挂载路径转为emby路径
        library_dir = dest_file.replace(dest_dir, library_dir)

        print(f"dest_file 处理文件::: {dest_file}")
        print(f"video_name 文件名字::: {video_name}")
        print(f"dest_path parent 文件目录::: {dest_path}")
        print(f"strm_path strm路径::: {strm_path}")
        print(f"emby_play_path emby播放地址::: {library_dir}")

        # 写入.strm文件
        with open(strm_path, "w") as f:
            f.write(library_dir)

        print(f"已写入 {strm_path}::: {library_dir}")
    except Exception as e:
        print(str(e))

def copy_files(source_dir, dest_dir, library_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    video_formats = ('.mp4', '.avi', '.rmvb', '.wmv', '.mov', '.mkv', '.flv', '.ts', '.webm', '.iso', '.mpg')

    for root, dirs, files in os.walk(source_dir):
        # 如果遇到名为'extrafanart'的文件夹，则跳过处理该文件夹，继续处理其他文件夹
        if "extrafanart" in dirs:
            dirs.remove("extrafanart")

        for file in files:
            source_file = os.path.join(root, file)
            print(f"处理源文件::: {source_file}")

            dest_file = os.path.join(dest_dir, os.path.relpath(source_file, source_dir))
            print(f"开始生成目标文件::: {dest_file}")

            # 创建目标目录中缺少的文件夹
            if not os.path.exists(Path(dest_file).parent):
                os.makedirs(Path(dest_file).parent)

            # 如果目标文件已存在，跳过处理
            if os.path.exists(dest_file):
                print(f"文件已存在，跳过处理::: {dest_file}")
                continue

            if file.lower().endswith(video_formats):
                # 如果视频文件小于1MB，则直接复制，不创建.strm文件
                if os.path.getsize(source_file) < 1024 * 1024:
                    print(f"视频文件小于1MB的视频文件到:::{dest_file}")
                    shutil.copy2(source_file, dest_file)
                else:
                    # 创建.strm文件
                    create_strm_file(dest_file, dest_dir, library_dir)
            else:
                # 复制文件
                print(f"复制其他文件到:::{dest_file}")
                shutil.copy2(source_file, dest_file)


filepath = os.path.join("/mnt", "config.yaml")

with open(filepath, "r") as f:  # 用with读取文件更好
    configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

monitor_confs = configs["sync"]["monitor_confs"]
if not isinstance(monitor_confs, list):
    monitor_confs = [monitor_confs]

# 存储目录监控配置
for monitor_conf in monitor_confs:
    if not isinstance(monitor_conf, dict):
        monitor_conf = json.loads(monitor_conf)
    source_dir = monitor_conf.get("source_dir")
    dest_dir = monitor_conf.get("dest_dir")
    library_dir = monitor_conf.get("library_dir")

    print(f"source::: {source_dir}")
    print(f"dest_dir::: {dest_dir}")
    print(f"library_dir::: {library_dir}")

    print(f"开始初始化生成strm文件 {source_dir}")

    # 批量生成strm文件
    copy_files(source_dir, dest_dir, library_dir)

    print(f"{source_dir} 初始化生成strm文件完成")