import pandas as pd
import numpy as np
import os
import jieba
from pyecharts.charts import Bar, Line, Pie, Map, Scatter, Page
from pyecharts import options as opts

def draw_heat(df, path):
    # 发布热度
    time_num = df.upload_time.value_counts().sort_index()
    print(time_num)
    # print(time_num.index)
    # 某天的播放量
    time_view = df.groupby(by=['upload_time'])['view_num'].sum()
    print(time_view)

    # 折线图
    line1 = Line(init_opts=opts.InitOpts(width='1350px', height='750px'))
    line1.add_xaxis(time_num.index.tolist())
    line1.add_yaxis('发布数量', time_num.values.tolist(),
                    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),  # 标记最小点及最大点
                                                            opts.MarkPointItem(type_='max')]),
                    yaxis_index=0,
                    # color = "#d14a61",  # 系列 label 颜色，红色
                    )
    line1.add_yaxis('播放总量', time_view.values.tolist(),
                    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),
                                                            opts.MarkPointItem(type_='max')]),
                    yaxis_index=1,
                    # color="#5793f3", # 系列 label 颜色蓝色
                    )

    line1.extend_axis(
        yaxis=opts.AxisOpts(
            name="播放总量",  # 坐标轴名称
            type_="value",  # 'value'适用于连续数据。
            min_=0,  # 坐标轴刻度最小值
            max_=int(time_view.max()),  # 坐标轴刻度最大值
            position="right",  # 轴的位置侧
        )
    )

    line1.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="发布数量",
            min_=0,
            max_=int(time_num.max()),
            position="left",
            # 轴线颜色
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        ),
        title_opts=opts.TitleOpts(title='近两月俄乌局势视频发布热度/播放热度走势图', pos_left='5%'),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate='45')),
    )


    line1.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=3),
                          label_opts=opts.LabelOpts(is_show=False)
                          )
    line1.render(path)
    return df

def draw_partition(df, path):
    region_num = df.region.value_counts().sort_index()
    # print(region_num.head())
    # print(type(region_num))


    columns = region_num.index.tolist()
    # print(columns)
    data = region_num.values.tolist()
    # print(data)

    # 设置饼形图
    pie = Pie()
    pie.add("",
            [list(z) for z in zip(columns, data)],
            radius=["40%", "55%"],
            center=["35%", "50%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
            )
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="近两月俄乌局势B站各视频分区发布数量"),
        legend_opts=opts.LegendOpts(pos_left="65%",
                                    orient="vertical"
                                    ),
    )


    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    pie.render(path)
    return df

def draw_play(df, path):
    region_view = df.groupby(by=['region'])['view_num'].sum()
    region_view = region_view.sort_values()
    # print(region_view)
    columns = region_view.index.tolist()
    # print(columns)
    data = region_view.values.tolist()

    bar = (
        Bar(init_opts=opts.InitOpts(width='1350px', height='750px'))
            .add_xaxis(columns)
            .add_yaxis("播放量", data,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),
                                                               opts.MarkPointItem(type_='max')]),
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title="近两月俄乌局势B站各视频分区播放总量"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate='45')),
                             )


            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    bar.render(path)
    return df


#设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 1000)

cwd = os.getcwd()
cwd = cwd[:cwd.find('script')]
saveName = cwd + 'data/search_data/' + "ewu.csv"
df = pd.read_csv(saveName,header=0,encoding="utf-8-sig")
# print(df.shape)#数据大小（行、列）
# print(df.head()#数据内容

def change_data(x_col):
    # 提取数值
    s_num = df[x_col].str.extract('(\d+\.*\d*)').astype('float')
    # 提取单位
    s_unit = df[x_col].str.extract('([\u4e00-\u9fa5]+)')
    s_unit = s_unit.replace('万', 10000).replace(np.nan, 1)
    s_multiply = s_num * s_unit
    return s_multiply

# 去重
df = df.drop_duplicates()
# 删除列
df.drop('video_url', axis=1, inplace=True)
# 转换单位
df['view_num'] = change_data(x_col='view_num')
df['danmu'] = change_data(x_col='danmu')
# 筛选时间
df = df[(df['upload_time'] >= '2022-01-01') & (df['title'].astype('str').str.contains('俄乌'))]
# print(df.head())

save_heat = cwd + 'data/search_data/' + "heat.html"
draw_heat(df, save_heat)

save_partition = cwd + 'data/search_data/' + "partition.html"
draw_partition(df, save_partition)

save_play = cwd + 'data/search_data/' + "play.html"
draw_play(df, save_play)