# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 10:37:55 2022

@author: Serein
"""
import time
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.util import add_cyclic_point
import cartopy.mpl.ticker as cticker
import cartopy.feature as cfeature
import cartopy
import numpy as np
import cmaps
import pandas as pd
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import warnings

# 忽略警告
warnings.filterwarnings("ignore")
# 防止中文出错
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["KaiTi"]
plt.rcParams["axes.unicode_minus"] = False
# 防止中文出错
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
# matplotlib.rcParams['font.family']='sans-serif'
plt.rcParams["axes.unicode_minus"] = False


def ID():
    """
    编写 李芳
    845728580@qq.com

    """
    print("编写: 李芳")
    print("845728580@qq.com")
    t = time.localtime()
    print(time.strftime("%Y年%m月%H时%M分%S秒", t))


def max_min(data):

    data_max = np.nanmax(data)
    data_min = np.nanmin(data)
    data = [data_min, data_max]
    return data


def savefig(file, dpi=200):
    """
    存图
    ----------
    file : 路径
    dpi : 像素大小，默认 200.
    
    """
    plt.savefig(file, dpi=dpi, bbox_inches="tight")


def jp(data, data_number=0):
    data = np.array(data)
    jp_data = data - data.mean(data_number)
    return jp_data


def nor(data, data_number=0):
    """
    标准化
    ----------
    data : 一维数组
    默认转换为 numpy 型    
    Returns
    -------
    nor_data : numpy
    返回 标准化后的一维数组

    """
    data = np.array(data)
    nor_data = (data - data.mean(data_number)) / data.std(data_number)
    return nor_data


def fig_bar_type(fig, fig_ax):
    """
    条形图 子图类型
    ----------
    fig : 画布
    fig_ax : add_axes、add_subplot

    Returns
    -------
    fig_bar : 子图类型

    """
    if type(fig_ax) == list:
        fig_bar = fig.add_axes(fig_ax)
    if type(fig_ax) == int:
        fig_bar = fig.add_subplot(fig_ax)
    return fig_bar


def fig_map_type(fig, fig_ax, proj_lon=0):
    """
    球坐标下 子图类型
    ----------
    fig : 画布
    fig_ax : add_axes、add_subplot

    Returns
    -------
    fig_map : 地图子图类型

    """
    proj = ccrs.PlateCarree(central_longitude=proj_lon)
    if type(fig_ax) == list:
        fig_map = fig.add_axes(fig_ax, projection=proj)
    if type(fig_ax) == int:
        fig_map = fig.add_subplot(fig_ax, projection=proj)
    return fig_map


def cycle_data(data, lon, lat):
    """
    循环 除去360°白条
    ----------
    data : 二维数据，
    lon : 经度，
    lat : 维度，

    Returns
    -------
    lon : 经度，
    lat : 维度，
    cdata : 数据 二维

    """
    cdata, cycle_lon = add_cyclic_point(data, coord=lon)
    LON, LAT = np.meshgrid(cycle_lon, lat)
    return LON, LAT, cdata


def fig(x, y):
    """
    画布大小
    ----------
    x : 长
    y : 宽，

    Returns
    -------
    fig
    """
    fig = plt.figure(figsize=(x, y))
    return fig


def PLC_map(ax, img_extent, lon_spec, lat_spec, size, china=True):
    """
    柱状投影 
    ----------
    ax : 子图.
    img_extent :经纬度范围.
    lon_spec : 经度间隔.
    lat_spec : 纬度间隔.
    size : 刻度大小
       默认 None.
    china: True,默认绘制中国国界

    Returns
    -------
    None.

    """

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAKES.with_scale("50m"))
    if china:
        ax.add_geometries(
            Reader(r"D:\data\china_map\river1.shp").geometries(),
            ccrs.PlateCarree(),
            facecolor="none",
            edgecolor="b",
            zorder=1,
            linewidth=0.6,
        )
        ax.add_geometries(
            Reader(r"D:\data\map\bou2_4l.shp").geometries(),
            ccrs.PlateCarree(),
            facecolor="none",
            edgecolor="k",
            zorder=2,
            linewidth=0.7,
        )
    ax.set_xticks(
        np.arange(img_extent[0], img_extent[1] + lon_spec, lon_spec),
        crs=ccrs.PlateCarree(),
    )
    ax.set_yticks(
        np.arange(img_extent[2], img_extent[3] + lat_spec, lat_spec),
        crs=ccrs.PlateCarree(),
    )
    lon_formatter = cticker.LongitudeFormatter()
    lat_formatter = cticker.LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    plt.xticks(fontsize=size)  # 设置标签大小
    plt.yticks(fontsize=size)


def draw_hgt(
    fig,
    hgt,
    lon,
    lat,
    levels,
    img_extent,
    lon_spec,
    lat_spec,
    hgt_fig,
    proj_lon=0,
    contour=True,
    colors="black",
    contour_lw=None,
    contour_ls=None,
    contour_clabel=False,
    bbox=False,
    contourf=False,
    cmap="jet",
    cbar_fig=None,
    cbar=True,
    cbar_title=None,
    cbar_label=None,
    cbar_orientation="horizontal",
    size=None,
    china=True,
    title=None,
    title_size=None,
    title_number=None,
):
    """
    绘制等值线图

    ----------
    fig : 画布,
    hgt : 位势高度,
    lon : 经度,
    lat : 纬度,
    levels : 等值线层次,
    cmap : 填色的颜色,
    img_extent : 绘图范围,
    lon_spec : 经度间隔,
    lat_spec : 维度间隔,
    hgt_fig : hgt位势高度子图大小
             [0.1 ,0.1,0.7,0.7].
    proj_lon=0：默认 中心经度维0
    contour : 是否绘制等值线
             默认 True  ； False.
    colors: 等值线颜色
    contour_lw: 粗细
    contour_ls: 线型{None, 'solid', 'dashed', 'dashdot', 'dotted'}
    contour_clabel : 是否绘制等值线标签
                    默认 False.
    bbox : 是否绘制标签边框  Flase.
    contourf : 是否绘制填色图
              默认 False.
    cbar_fig :色标子图大小   e.g.[0.1 ,0.1,0.6,0.01].
              默认 None.
    cbar : True,
               默认绘制色标
    cbar_title : 色标标题
    cbar_label : 色标标签
    cbar_orientation : 色标方向
    水平='horizontal';垂直=‘vertical’,
    size : 刻度大小,
    china=True:默认绘制中国
    title : 标题,
    title_size :标题大小,
    title_number : 标题序号,

    Returns
    -------
    返回ax
    位势高度子图ax

    """

    # 绘制等值线图
    if type(fig) == matplotlib.figure.Figure:
        ax = fig_map_type(fig, hgt_fig, proj_lon)
    # if type(fig)==cartopy.mpl.geoaxes.GeoAxes:
    #        ax=fig
    # if type(fig)==cartopy.mpl.geoaxes.GeoAxesSubplot:
    #        ax=fig

    PLC_map(ax, img_extent, lon_spec, lat_spec, size=size, china=china)
    ax.set_extent(img_extent, crs=ccrs.PlateCarree())
    if contourf != False:
        c1 = ax.contourf(
            lon,
            lat,
            hgt,
            levels=levels,
            cmap=cmap,
            zorder=0,
            transform=ccrs.PlateCarree(),
            extend="both",
        )
        if cbar:
            axc = fig.add_axes(cbar_fig)
            cbar = plt.colorbar(c1, cax=axc, orientation=cbar_orientation)
            cbar.ax.tick_params(labelsize=size, direction="in")
            cbar.set_ticks(levels)
            cbar.set_label(cbar_label, size=title_size)
            axc.set_title(cbar_title, fontsize=title_size)
    if contour != False:
        c11 = ax.contour(
            lon,
            lat,
            hgt,
            colors=colors,
            zorder=3,
            levels=levels,
            linewidths=contour_lw,
            linestyles=contour_ls,
        )
        if contour_clabel:
            ml = ax.clabel(c11, inline=True, fontsize=10, fmt="%i", use_clabeltext=True)
            if bbox:
                for m in ml:
                    m.set_bbox({"fc": "w"})  # 给每根线加上框
    # 底图

    ax.set_title(title, size=title_size)
    ax.set_title(title_number, loc="left", fontsize=title_size)
    plt.tight_layout()
    return ax


def draw_bar(
    fig,
    x,
    y,
    bar_fig,
    ylim,
    nor=True,
    size=None,
    title=None,
    title_number=None,
    title_size=None,
):
    """
    条形图 绘制pc序列
    ----------
    fig : 画布，
    x : x轴 一般为年份，
    y : y轴 一般为指数(可标准化后)，
    bar_fig :条形图子图大小 e.g.[0.1,0.1,0.5,0.5]，
    ylim :指数范围 e.g.(-3.1,3.1)
    nor : 默认 True 进行标准化
    size : 刻度大小
    title : 标题
    title_number :标题序号
    title_size : 标题大小

    Returns
    -------
    fig_ax : 返回条形图子图


    """
    if nor:
        y = (y - y.mean(0)) / y.std()
    fig_ax = fig_bar_type(fig, bar_fig)
    c_color = []  # 条形图颜色：红+，蓝-
    for i in range(int(x[0]), int(x[-1]) + 1):
        if y[i - int(x[0])] >= 0:
            c_color.append("red")
        elif y[i - int(x[0])] < 0:
            c_color.append("blue")
    # 设置标题
    fig_ax.set_title(title, fontsize=title_size)
    fig_ax.set_title(title_number, loc="left", fontsize=title_size)
    # 设置轴范围
    fig_ax.set_ylim(ylim)
    # y=0设置为虚线
    fig_ax.axhline(0, linestyle="--", c="g")
    # 设置刻度值大小
    plt.xticks(size=size)
    plt.yticks(size=size)
    # 绘制条形图
    fig_ax.bar(x, y, color=c_color)
    fig_ax.grid(b=False)
    plt.tight_layout()
    return fig_ax


def draw_uv(
    fig,
    u,
    v,
    lon,
    lat,
    barbs_fig,
    barbs_num,
    img_extent,
    lon_spec,
    lat_spec,
    size=None,
    proj_lon=0,
    china=True,
    title=None,
    title_number=None,
    title_size=None,
    contour_hgt=False,
    hgt=None,
    lon_hgt=None,
    lat_hgt=None,
    lev_hgt=None,
    contour_lw=None,
    contour_ls=None,
    barbs=True,
    barbs_length=7,
    pivot="tip",
    quiver=False,
    quiver_cf=False,
    color="k",
    cmap="RdBu_r",
    scale=None,
    width=0.005,
    headwidth=3,
    headlength=4.5,
):
    """
    绘制uv风场,可选择高度场叠加
    ----------
    fig : 画布.
    u : u风场.
    v : v风场.
    barbs_fig : 风场子图大小.
    barbs_num : uv风场间隔.
    barbs_length : 风向标长度.
    img_extent : 绘图范围.
    lon_spec : 经度间隔.
    lat_spec : 维度间隔
    size : 刻度大小
          默认 None.
    proj_lon : 默认 中心经度为0.
    china : True
           默认绘制中国。
    title : 标题
           默认 None.
    title_size :标题大小
                默认None.
    title_number : 标题序号
                  默认 None.
    contour_hgt : 是否添加高度场
                  默认Flase.
    hgt :高度场
         默认 None.
    lon_hgt : 高度场经
             默认 None.
    lat_hgt : 高度场纬度
             默认 None.
    lev_hgt : 高度场间隔层次
             默认 None.
    contour_lw:None,线宽
    contour_ls:None,线型
    barbs : 绘制风向标图
           默认 True.
    barbs_length : 风杆长度
                  默认 7.
    pivot : 风杆位置'tip'、'middle'
            默认'tip'.
    quiver : 是否绘制风矢量图
             默认 False.
    quiver_cf : 矢量图是否填色
              默认 False.
    color : 矢量箭头颜色
           默认 黑色 'k'.
    cmap : 矢量箭头填色
          默认 'RdBu_r'.
    scale : 矢量箭头数量
           默认 None.
    width : 箭杆的宽度
           默认 0.005.
    headwidth :  箭头的宽度
               默认 3.
    headlength :  箭头的长度
                默认 4.5.

    Returns
    -------
    ax : 返回风场子图baras的ax

    """
    ax = fig_map_type(fig, barbs_fig, proj_lon)
    lon, lat = np.meshgrid(lon, lat)
    ax.set_extent(img_extent, crs=ccrs.PlateCarree())
    if contour_hgt == True:
        ax.contour(
            lon_hgt,
            lat_hgt,
            hgt,
            colors="k",
            levels=lev_hgt,
            linewidths=contour_lw,
            linestyles=contour_ls,
            transform=ccrs.PlateCarree(),
        )
    if barbs == True:
        # 绘制风羽
        ax.barbs(
            lon[::barbs_num, ::barbs_num],
            lat[::barbs_num, ::barbs_num],
            u[::barbs_num, ::barbs_num].values,
            v[::barbs_num, ::barbs_num].values,
            length=barbs_length,
            pivot=pivot,
            transform=ccrs.PlateCarree(),
        )
    if quiver:
        windspeed = np.sqrt(u ** 2 + v ** 2)
        if quiver_cf == True:
            ax.quiver(
                lon[::barbs_num, ::barbs_num],
                lat[::barbs_num, ::barbs_num],
                u[::barbs_num, ::barbs_num].values,
                v[::barbs_num, ::barbs_num].values,
                windspeed[::barbs_num, ::barbs_num].values,
                scale=scale,
                cmap=cmap,
                width=width,
                headwidth=headwidth,
                headlength=headlength,
                transform=ccrs.PlateCarree(),
            )
        if quiver_cf == False:
            ax.quiver(
                lon[::barbs_num, ::barbs_num],
                lat[::barbs_num, ::barbs_num],
                u[::barbs_num, ::barbs_num].values,
                v[::barbs_num, ::barbs_num].values,
                scale=scale,
                color=color,
                width=width,
                headwidth=headwidth,
                headlength=headlength,
                transform=ccrs.PlateCarree(),
            )
    # 底图
    PLC_map(ax, img_extent, lon_spec, lat_spec, size, china)
    # 绘制标题
    ax.set_title(title, size=title_size)
    ax.set_title(title_number, loc="left", fontsize=title_size)
    plt.tight_layout()
    return ax


ID()
