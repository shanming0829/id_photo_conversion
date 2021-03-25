#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : Tue Mar 23 2021
# @Author  : Shanming Liu
# @File    : image_converter.py
# @Version : 1.0.0
"""
 照片尺寸，宽*高（单位：像素）
 1寸照片：295*413
 2寸照片：413*626
 5寸照片（横版）：1500*1050
 6寸照片（横版）：1800*1200
 """
import os
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog

WIDTH_1IN = 295
HEIGHT_1IN = 413

WIDTH_2IN = 413
HEIGHT_2IN = 626

WIDTH_5IN = 1500
HEIGHT_5IN = 1050

# 非全景6寸照片
WIDTH_6IN = 1950
HEIGHT_6IN = 1300

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cut_photo_with_rate(photo: Image.Image, width: int, height: int):
    rate = height / width
    img_width, img_height = photo.size
    img_rate = img_height / img_width

    if img_rate < rate:
        # 左右裁剪
        x = (img_width - int(img_height * width / height)) // 2
        cutted_photo = photo.crop((x, 0, img_width - x, img_height))
    else:
        # 下裁剪, 保持头像一直存在
        y = int(img_width * height / width)
        cutted_photo = photo.crop((0, 0, img_width, img_height - y))
    return cutted_photo


def cut_photo(photo: Image.Image, choice: int):
    """
    将照片按照比例进行裁剪成1寸、2寸.
以1寸照片为例，其高：宽 = 1.4，为了使原始照片不失真，应该按照这个1.4的比例进行裁剪,
若大于1.4说明高度多了，需要进行上下裁剪；若小于1.4说明宽度多了，需要进行左右裁剪。
    :param photo: 待处理的照片
    :param choice: <int> 1代表1寸，2代表2寸
    :return: 处理后的照片
    """
    if choice == 1:
        return cut_photo_with_rate(photo, WIDTH_1IN, HEIGHT_1IN)
    if choice == 2:
        return cut_photo_with_rate(photo, WIDTH_2IN, HEIGHT_2IN)


def resize_photo(photo: Image.Image, choice: int):
    '''
    缩放照片
    :param photo: 待处理的照片
    :param choice: <int> 1代表1寸，2代表2寸
    :return: 处理后的照片
    '''
    if choice == 1:
        resized_photo = photo.resize((WIDTH_1IN, HEIGHT_1IN))
        return resized_photo
    if choice == 2:
        resized_photo = photo.resize((WIDTH_2IN, HEIGHT_2IN))
        return resized_photo


def layout_photo_5_1(photo):
    """
    在5寸照片上排版1寸照片
    :param photo: 待处理照片1寸
    :return: 处理后的照片
    """
    bk = Image.new("RGB", (WIDTH_5IN, HEIGHT_5IN), (255, 255, 255))
    draw = ImageDraw.Draw(bk)  # 创建画笔
    draw.line([(0, HEIGHT_5IN / 2), (WIDTH_5IN, HEIGHT_5IN / 2)],
              fill=128)  # 横线
    draw.line([(WIDTH_5IN * 0.25, 0), (WIDTH_5IN * 0.25, HEIGHT_5IN)],
              fill=128)  # 第1条竖线
    draw.line([(WIDTH_5IN * 0.5, 0), (WIDTH_5IN * 0.5, HEIGHT_5IN)],
              fill=128)  # 第2条竖线
    draw.line([(WIDTH_5IN * 0.75, 0), (WIDTH_5IN * 0.75, HEIGHT_5IN)],
              fill=128)  # 第3条竖线

    focus_point = [0.125 * WIDTH_5IN, 0.25 * HEIGHT_5IN]
    start_point = [
        focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN
    ]
    for i in range(0, 2):
        for k in range(0, 4):
            bk.paste(photo, (int(start_point[0] + (k * WIDTH_5IN / 4)),
                             int(start_point[1] + 0.5 * i * HEIGHT_5IN)))
    return bk


def layout_photo_5_2(photo):
    """
    在5寸照片上排版2寸照片
    :param photo: 待处理照片2寸
    :return: 处理后的照片
    """
    bk = Image.new("RGB", (HEIGHT_5IN, WIDTH_5IN), (255, 255, 255))  # 竖版排版
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, WIDTH_5IN / 2), (WIDTH_5IN, WIDTH_5IN / 2)], fill=128)  # 横线
    draw.line([(HEIGHT_5IN * 0.5, 0), (HEIGHT_5IN * 0.5, WIDTH_5IN)],
              fill=128)  # 竖线
    focus_point = [0.25 * HEIGHT_5IN, 0.25 * WIDTH_5IN]
    start_point = [
        focus_point[0] - 0.5 * WIDTH_2IN, focus_point[1] - 0.5 * HEIGHT_2IN
    ]
    #print(focus_point,start_point)
    for i in range(0, 2):
        for k in range(0, 2):
            bk.paste(photo, (int(start_point[0] + (k * HEIGHT_5IN / 2)),
                             int(start_point[1] + 0.5 * i * WIDTH_5IN)))
    return bk


def layout_photo_5_mix(photo1, photo2):
    """
    在5寸照片上混合排版1寸、2寸照片
    :param photo1: 待处理照片1寸
    :param photo2: 待处理照片2寸
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [WIDTH_5IN, HEIGHT_5IN], (255, 255, 255))
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, HEIGHT_5IN / 2), (WIDTH_5IN, HEIGHT_5IN / 2)],
              fill=128)  # 横线
    draw.line([(WIDTH_5IN * 0.25, 0), (WIDTH_5IN * 0.25, HEIGHT_5IN)],
              fill=128)  # 第1条竖线
    draw.line([(WIDTH_5IN * 0.5, 0), (WIDTH_5IN * 0.5, HEIGHT_5IN)],
              fill=128)  # 第2条竖线

    focus_point = [0.125 * WIDTH_5IN, 0.25 * HEIGHT_5IN]
    start_point = [
        focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN
    ]
    focus_point2 = [0.75 * WIDTH_5IN, 0.25 * HEIGHT_5IN]
    start_point2 = [
        focus_point2[0] - 0.5 * HEIGHT_2IN, focus_point2[1] - 0.5 * WIDTH_2IN
    ]

    for i in range(0, 2):
        for k in range(0, 2):
            bk.paste(photo1, (int(start_point[0] + (k * WIDTH_5IN / 4)),
                              int(start_point[1] + 0.5 * i * HEIGHT_5IN)))

    bk.paste(photo2, (int(start_point2[0]), int(start_point2[1])))
    bk.paste(photo2,
             (int(start_point2[0]), int(start_point2[1] + 0.5 * HEIGHT_5IN)))
    return bk


def layout_photo_6_1(photo: Image.Image):
    """
    在6寸照片上排版2寸照片
    :param photo: 待处理照片1寸
    :return: 处理后的照片
    """
    bk = Image.new("RGB", (HEIGHT_6IN, WIDTH_6IN), (255, 255, 255))  # 竖版排版
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, WIDTH_6IN * 0.25), (WIDTH_6IN, WIDTH_6IN * 0.25)],
              fill=128)  # 横线
    draw.line([(0, WIDTH_6IN * 0.5), (WIDTH_6IN, WIDTH_6IN * 0.5)],
              fill=128)  # 横线
    draw.line([(0, WIDTH_6IN * 0.75), (WIDTH_6IN, WIDTH_6IN * 0.75)],
              fill=128)  # 横线
    draw.line([(HEIGHT_6IN * 0.25, 0), (HEIGHT_6IN * 0.25, WIDTH_6IN)],
              fill=128)  # 竖线
    draw.line([(HEIGHT_6IN * 0.5, 0), (HEIGHT_6IN * 0.5, WIDTH_6IN)],
              fill=128)  # 竖线
    draw.line([(HEIGHT_6IN * 0.75, 0), (HEIGHT_6IN * 0.75, WIDTH_6IN)],
              fill=128)  # 竖线
    focus_point = [0.125 * HEIGHT_6IN, 0.125 * WIDTH_6IN]
    start_point = [
        focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN
    ]
    # print(focus_point,start_point)
    for i in range(0, 4):
        for k in range(0, 4):
            bk.paste(photo, (int(start_point[0] + (k * HEIGHT_6IN / 4)),
                             int(start_point[1] + i * 0.25 * WIDTH_6IN)))
    return bk


def layout_photo_6_2(photo):
    """
    在6寸照片上排版2寸照片
    :param photo: 待处理照片2寸
    :return: 处理后的照片
    """
    bk = Image.new("RGB", (WIDTH_6IN, HEIGHT_6IN), (255, 255, 255))
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, HEIGHT_6IN / 2), (WIDTH_6IN, HEIGHT_6IN / 2)],
              fill=128)  # 横线
    draw.line([(WIDTH_6IN * 0.25, 0), (WIDTH_6IN * 0.25, HEIGHT_6IN)],
              fill=128)  # 第1条竖线
    draw.line([(WIDTH_6IN * 0.5, 0), (WIDTH_6IN * 0.5, HEIGHT_6IN)],
              fill=128)  # 第2条竖线
    draw.line([(WIDTH_6IN * 0.75, 0), (WIDTH_6IN * 0.75, HEIGHT_6IN)],
              fill=128)  # 第3条竖线
    focus_point = [0.125 * WIDTH_6IN, 0.25 * HEIGHT_6IN]
    start_point = [
        focus_point[0] - 0.5 * WIDTH_2IN, focus_point[1] - 0.5 * HEIGHT_2IN
    ]
    for i in range(0, 2):
        for k in range(0, 4):
            bk.paste(photo, (int(start_point[0] + (k * WIDTH_6IN / 4)),
                             int(start_point[1] + 0.5 * i * HEIGHT_6IN)))
    return bk


def layout_photo_6_mix(photo1, photo2):
    """
    在6寸照片上混合排版1寸、2寸照片
    :param photo1: 待处理照片1寸
    :param photo2: 待处理照片2寸
    :return: 处理后的照片
    """
    bk = Image.new("RGB", (WIDTH_6IN, HEIGHT_6IN), (255, 255, 255))
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, HEIGHT_6IN * 0.5), (WIDTH_6IN, HEIGHT_6IN / 2)],
              fill=128)  # 横线
    draw.line([(0, HEIGHT_6IN * 0.25), (WIDTH_6IN * 0.5, HEIGHT_6IN * 0.25)],
              fill=128)  # 短横线
    draw.line([(0, HEIGHT_6IN * 0.75), (WIDTH_6IN * 0.5, HEIGHT_6IN * 0.75)],
              fill=128)  # 短横线
    draw.line([(WIDTH_6IN * 0.25, 0), (WIDTH_6IN * 0.25, HEIGHT_6IN)],
              fill=128)  # 第1条竖线
    draw.line([(WIDTH_6IN * 0.5, 0), (WIDTH_6IN * 0.5, HEIGHT_6IN)],
              fill=128)  # 第2条竖线
    draw.line([(WIDTH_6IN * 0.75, 0), (WIDTH_6IN * 0.75, HEIGHT_6IN)],
              fill=128)  # 第3条竖线
    focus_point = [0.125 * WIDTH_6IN, 0.125 * HEIGHT_6IN]
    start_point = [
        focus_point[0] - 0.5 * HEIGHT_1IN, focus_point[1] - 0.5 * WIDTH_1IN
    ]
    for i in range(0, 4):
        for k in range(0, 2):
            bk.paste(photo1, (int(start_point[0] + (0.25 * k * WIDTH_6IN)),
                              int(start_point[1] + 0.25 * i * HEIGHT_6IN)))
    focus_point2 = [0.625 * WIDTH_6IN, 0.25 * HEIGHT_6IN]
    start_point2 = [
        focus_point2[0] - 0.5 * WIDTH_2IN, focus_point2[1] - 0.5 * HEIGHT_2IN
    ]
    for i in range(0, 2):
        for k in range(0, 2):
            bk.paste(photo2, (int(start_point2[0] + (0.25 * k * WIDTH_6IN)),
                              int(start_point2[1] + 0.5 * i * HEIGHT_6IN)))
    bk.show()
    return bk


def convert_image(source, idInch, photoInch):
    im = Image.open(source)
    photo1 = resize_photo(cut_photo(im, 1), 1)
    photo2 = resize_photo(cut_photo(im, 2), 2)
    if idInch == '1' or idInch == '2':
        fun_name = f'layout_photo_{photoInch}_{idInch}'
        file_path = os.path.join(BASEDIR, f'{photoInch}_{idInch}.jpg')
        globals()[fun_name](photo1 if idInch == '1' else photo2).save(
            file_path)
    else:
        fun_name = f'layout_photo_{photoInch}_mix'
        file_path = os.path.join(BASEDIR, f'{photoInch}_mix.jpg')
        globals()[fun_name](photo1, photo2).save(file_path)

    return file_path


# layout_photo_5_1(resize_photo(cut_photo(im, 1), 1)).save('5_1.jpg')
# layout_photo_5_2(resize_photo(cut_photo(im, 2), 2)).save('5_2.jpg')
# layout_photo_6_1(resize_photo(cut_photo(im, 1), 1)).save('6_1.jpg')
# layout_photo_6_2(resize_photo(cut_photo(im, 2), 2)).save('6_2.jpg')
# layout_photo_5_mix(resize_photo(cut_photo(im, 1), 1),
#                    resize_photo(cut_photo(im, 2),
#                                 2).rotate(90, expand=True)).save('5_1_mix.jpg')
# layout_photo_6_mix1(
#     resize_photo(cut_photo(im, 1), 1).rotate(90, expand=True),
#     resize_photo(cut_photo(im, 2), 2)).save('6_mix1.jpg')
# layout_photo_6_mix2(resize_photo(cut_photo(im, 1), 1),
#                     resize_photo(cut_photo(im, 2), 2)).save('6_mix2.jpg')
