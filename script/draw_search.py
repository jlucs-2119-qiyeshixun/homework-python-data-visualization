import jieba
from pyecharts.charts import Bar, Line, Pie, Map, Scatter, Page #引入柱状图、折线图、饼状图、地图
from pyecharts import options as opts

def draw_heat(df, path):
    # 发布热度
    time_num = df.upload_time.value_counts().sort_index()  # time_num中包含的是日期，及每个日期内有多少个视频发布
    print(time_num)
    # print(time_num.index)
    # 某天的播放量(https://www.cnblogs.com/zhoudayang/p/5534593.html)
    time_view = df.groupby(by=['upload_time'])['view_num'].sum()  # 如果需要按照列A进行分组，将同一组的列B求和
    print(time_view)

    # 折线图（不同的图的叠加https://[pyecharts学习笔记]——Grid并行多图、组合图、多 X/Y 轴）
    line1 = Line(init_opts=opts.InitOpts(width='1350px', height='750px'))
    line1.add_xaxis(time_num.index.tolist())
    line1.add_yaxis('发布数量', time_num.values.tolist(),
                    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),  # 标记最小点及最大点
                                                            opts.MarkPointItem(type_='max')]),
                    # 添加第一个轴，索引为0,（默认也是0）
                    yaxis_index=0,
                    # color = "#d14a61",  # 系列 label 颜色，红色
                    )
    line1.add_yaxis('播放总量', time_view.values.tolist(),
                    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),
                                                            opts.MarkPointItem(type_='max')]),
                    yaxis_index=1,  # 上面的折线图图默认索引为0，这里设置折线图y 轴索引为1
                    # color="#5793f3", # 系列 label 颜色蓝色
                    )

    # 新加入一个y轴(索引值是1)下方是对其的详细配置
    line1.extend_axis(
        yaxis=opts.AxisOpts(
            name="播放总量",  # 坐标轴名称
            type_="value",  # 坐标轴类型  'value': 数值轴，适用于连续数据。
            min_=0,  # 坐标轴刻度最小值
            max_=int(time_view.max()),  # 坐标轴刻度最大值
            position="right",  # 轴的位置  侧
            # 轴线配置
            # axisline_opts=opts.AxisLineOpts(
            #     # 轴线颜色（默认黑色）
            #     linestyle_opts=opts.LineStyleOpts(color="#5793f3")
            # ),
            # 轴标签显示格式
            # axislabel_opts=opts.LabelOpts(formatter="{value} c"),
        )
    )

    # 全局配置（全局配置中默认已经存在一个y轴了（默认索引值是0），要想更改此左侧的y轴必须更改此处的）
    line1.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="发布数量",
            min_=0,
            max_=int(time_num.max()),
            position="left",
            # offset=80, # Y 轴相对于默认位置的偏移，在相同的 position 上有多个 Y 轴的时候有用。
            # 轴线颜色
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        ),
        title_opts=opts.TitleOpts(title='俄乌局势视频发布热度/播放热度走势图', pos_left='5%'),  # 标题
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate='45')),  # x轴的标签倾斜度为垂直
    )

    # 系列配置项，不显示标签（不会将折线上的每个点的值都在图中显示出来）
    line1.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=3),
                          label_opts=opts.LabelOpts(is_show=False)
                          )
    line1.render(path)
    return df

