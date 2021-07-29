import pickle as pk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re

import time

#DATA0 = 'data/plot0_005_tic.pk'
DICT1 = 'data/alldict_1/'

SAVEMASSSTRIDE = 100
#ori_mass_range = [0, 1200]
#ori_scan_range = [0, 1400]
COLOR_BG = 'skyblue'
COLOR_SELECT = 'b'
COLOR_TIC = 'black'
TICPROP = 10


class EventFactory(object):
    def __init__(self, ax, alldata, mass_range, scan_range, view_len=0.1):
        self.ax = ax
        self.ori_data = alldata
        self.min_scan_len = 5
        self.min_mass_len = 5
        self.zoom_param = 1.2
        self.init_info()
        self.draw_label = None
        self.draw_value = None
        self.colors_dict = {}
        self.ori_mass_range = mass_range
        self.ori_scan_range = scan_range
        self.mass_range = self.ori_mass_range
        self.scan_range = self.ori_scan_range
        self.view_len = view_len
        self.draw_all()

    def mouse_move(self, event):
        if not event.inaxes:
            return
        self.del_text_while_move(event)
        label_name, value = self.resolve_location(event.xdata, event.ydata)
        if label_name is None:
            return
        if label_name == 'mass':
            tstr = 'mass = ' + str(value)
            self.label_move = event.inaxes.text3D(value,
                                                  -0.3 * (self.scan_range[1] - self.scan_range[0]) + self.scan_range[0],
                                                  0, tstr, bbox=dict(facecolor='green', alpha=0.3))
            self.label_name = 'mass'
            self.value = value
        else:
            tstr = 'scan = ' + str(value)
            self.label_move = event.inaxes.text3D((self.mass_range[1] - self.mass_range[0]) * 0.2 + self.mass_range[1],
                                                  value, 0, tstr, bbox=dict(facecolor='green', alpha=0.3))
            self.label_name = 'scan'
            self.value = value

        self.set_lim()
        plt.draw()

    def mouse_press(self, event):
        if not event.inaxes:
            self.last_position_xy = None
            self.last_press_time = None
            return

        this_press_time = time.time()
        if self.last_press_time is None:
            self.last_press_time = this_press_time
            self.last_position_xy = (event.xdata, event.ydata)

        elif (this_press_time - self.last_press_time) < 0.5 and self.dis(self.last_position_xy,
                                                                         (event.xdata, event.ydata)) < 10E-3:
            self.double_click_flag = True
            self.double_click()
            return


        else:
            self.last_press_time = this_press_time
            self.last_position_xy = (event.xdata, event.ydata)

    def mouse_release(self, event):
        if not event.inaxes:
            self.last_position_xy = None
            self.last_press_time = None
            return
        release_time = time.time()
        if self.double_click_flag:
            self.double_click_flag = False
            return
        if self.last_press_time is None:
            return
        if release_time - self.last_press_time < 0.3 and self.dis(self.last_position_xy,
                                                                  (event.xdata, event.ydata)) < 10E-3:
            self.click_on(event)
        elif release_time - self.last_press_time > 0.5 and self.dis(self.last_position_xy,
                                                                    (event.xdata, event.ydata)) > 10E-3:
            self.zoom_by_mouse(event)

    def scroll(self, event):
        if not event.inaxes:
            return
        self.zoom_by_scroll(event)

    def click_on(self, event):
        self.del_line_while_click()
        if self.label_name is None:
            return
        elif self.label_name == 'mass':
            self.draw_mass()

        else:
            self.draw_scan()

        self.set_lim()
        plt.draw()

    def double_click(self):
        self.init_info()
        self.draw_label = None
        self.draw_value = None
        self.mass_range = self.ori_mass_range
        self.scan_range = self.ori_scan_range

        self.draw_all()
        self.double_click_flag = True

    def draw_all(self):
        t = time.time()
        ## 画整张图，初始化其他状态
        self.all_data = [[], [], []]
        # 准备数据
        for i, mass in enumerate(self.ori_data[0]):
            if mass < self.mass_range[0] or mass > self.mass_range[1]:
                continue
            self.all_data[0].append(mass)
            self.all_data[2].append(self.ori_data[2][i][self.scan_range[0]:self.scan_range[1]])

        self.all_data[1] = self.ori_data[1][self.scan_range[0]:self.scan_range[1]]

        # 清空画板,初始化各个状态
        self.ax.cla()
        self.init_info()
        self.mass_lim = 0.1 * (self.mass_range[1] - self.mass_range[0])
        self.scan_lim = 0.1 * (self.scan_range[1] - self.scan_range[0])
        view_len = int(self.view_len * (self.scan_range[1] - self.scan_range[0]))
        self.view_range = [-view_len, view_len]

        # 画上原始线

        self.ax.set_xlabel('mass')
        self.ax.set_ylabel('scan')
        self.ax.set_zlabel('intensity')
        x = self.all_data[0]
        y = self.all_data[1]
        z = self.all_data[2]

        tmp_y = np.array(y)
        ylimit = len(y)
        L = len(x)
        for i in range(L):
            tmp_x = np.full(ylimit, x[i])
            tmp_z = np.array(z[i])
            self.ax.plot(tmp_x, tmp_y, tmp_z, linewidth=0.4, zorder=1)

        if len(self.colors_dict) == 0:
            for line in self.ax.lines:
                self.colors_dict[line.get_data_3d()[0][0]] = line.get_color()
        else:
            for line in self.ax.lines:
                line.set_color(self.colors_dict[line.get_data_3d()[0][0]])

        self.ori_len = len(self.ax.lines)
        for i in range(self.ori_len):
            tline = \
            self.ax.plot(np.array([0]), np.array([0]), np.array([0]), color=self.ax.lines[i].get_color(), linewidth=0.6,
                         zorder=3)[0]
            self.scan_lines.append(tline)

        self.line = \
        self.ax.plot(np.array([0]), np.array([0]), np.array([0]), color=COLOR_SELECT, linewidth=0.8, zorder=2)[0]
        # 画出TIC
        tmp_z = np.array(self.ori_data[3][self.scan_range[0]:self.scan_range[1]]) / TICPROP
        tmp_x = np.full(ylimit, self.mass_range[0])
        self.tic_line = self.ax.plot(tmp_x, tmp_y, tmp_z, color=COLOR_TIC, linewidth=0.8, zorder=0)[0]
        self.scan_tic = \
        self.ax.plot(np.array([0]), np.array([0]), np.array([0]), linestyle="-.", color=COLOR_TIC, linewidth=0.4,
                     zorder=0)[0]

        for line in self.ax.lines:
            self.colors.append(line.get_color())

        if self.draw_label == 'mass' and self.mass_range[0] < self.draw_value < self.mass_range[1]:
            self.value = self.draw_value
            self.label_name = self.draw_label
            self.draw_mass()
        elif self.draw_label == 'scan' and self.scan_range[0] < self.draw_value < self.scan_range[1]:
            self.value = self.draw_value
            self.label_name = self.draw_label
            self.draw_scan()

        elif self.draw_label == 'mass' or self.draw_label == 'scan':
            for i in range(self.ori_len):
                self.ax.lines[i].set_color(COLOR_BG)

        self.set_lim()
        plt.draw()
        print(time.time() - t)

    def draw_mass(self):
        y_data = None
        z_data = None
        for line in self.ax.lines:
            tmp = line.get_data_3d()[0][0]
            if tmp == self.value:
                y_data = line.get_data_3d()[1]
                z_data = line.get_data_3d()[2]
                x_data = np.full(len(z_data), self.value)
                break

        self.line.set_data_3d(x_data, y_data, z_data)
        tstr = self.label_name + ' = ' + str(self.value)
        self.label_press = self.ax.text3D(self.value,
                                          -0.3 * (self.scan_range[1] - self.scan_range[0]) + self.scan_range[0], 0,
                                          tstr, bbox=dict(facecolor='red', alpha=0.3))
        for i in range(self.ori_len):
            self.ax.lines[i].set_color(COLOR_BG)

        self.line.set_color(COLOR_SELECT)
        self.draw_label = 'mass'
        self.draw_value = self.value

    def draw_scan(self):
        x_data = []
        y_data = []
        z_data = []
        begin = self.value + self.view_range[0]
        if begin < self.scan_range[0]:
            begin = self.scan_range[0]

        end = self.value + self.view_range[1]
        if end > self.scan_range[1]:
            end = self.scan_range[1]

        L = end - begin
        x_data.append(self.mass_range[0])
        y_data.append(self.value)
        z_data.append(0)
        for i, item in enumerate(self.all_data[0]):
            x_data.append(item)
            x_data.append(item)
            x_data.append(item)
            y_data.append(self.value)
            y_data.append(self.value)
            y_data.append(self.value)
            z_data.append(0)
            z_data.append(self.all_data[2][i][self.value - self.scan_range[0]])

            z_data.append(0)
            tmp_x = np.full(L, item)
            tmp_y = np.array(list(range(begin, end)))
            tmp_z = np.array(self.all_data[2][i][begin - self.scan_range[0]:end - self.scan_range[0]])

            self.scan_lines[i].set_data_3d(tmp_x, tmp_y, tmp_z)
            self.points.append(self.ax.scatter(item, self.value, self.all_data[2][i][self.value - self.scan_range[0]],
                                               c=self.colors[i], s=8, marker='_'))

        x_data.append(self.mass_range[1])
        y_data.append(self.value)
        z_data.append(0)
        x_data = np.array(x_data)
        y_data = np.array(y_data)
        z_data = np.array(z_data)
        self.line.set_data_3d(x_data, y_data, z_data)
        self.scan_tic.set_data_3d(np.array([self.mass_range[0], self.mass_range[0]]),
                                  np.array([self.value, self.value]),
                                  np.array([0, self.ori_data[3][self.value] / TICPROP]))
        tstr = self.label_name + ' = ' + str(self.value)
        self.label_press = self.ax.text3D((self.mass_range[1] - self.mass_range[0]) * 0.2 + self.mass_range[1],
                                          self.value, 0, tstr, bbox=dict(facecolor='red', alpha=0.3))
        for i in range(self.ori_len):
            self.ax.lines[i].set_color(COLOR_BG)

        self.draw_label = 'scan'
        self.draw_value = self.value

    def zoom_by_mouse(self, event):
        if self.last_position_xy is None:
            return
        label1, value1 = self.resolve_location(self.last_position_xy[0], self.last_position_xy[1])
        if label1 is None:
            return
        label2, value2 = self.resolve_location(event.xdata, event.ydata)
        if label2 != label1:
            return

        tstr1 = self.ax.format_coord(self.last_position_xy[0], self.last_position_xy[1])
        tstr2 = self.ax.format_coord(event.xdata, event.ydata)

        ans1 = re.match('x=(.*) , y=(.*), z=(.*)', tstr1)
        ans2 = re.match('x=(.*) , y=(.*), z=(.*)', tstr2)
        if ans1 is None or ans2 is None:
            return

        if label1 == 'mass':
            x1 = float(ans1.group(1))
            x2 = float(ans2.group(1))
            x1 = int(x1)
            x2 = int(x2)

            self.mass_range = [min(x1, x2), max(x1, x2)]

        elif label1 == 'scan':
            y1 = float(ans1.group(2))
            y2 = float(ans2.group(2))
            y1 = int(y1)
            y2 = int(y2)

            self.scan_range = [min(y1, y2), max(y1, y2)]

        self.draw_all()

    def zoom_by_scroll(self, event):
        label, value = self.resolve_location(event.xdata, event.ydata)
        if label is None:
            return
        tstr = self.ax.format_coord(event.xdata, event.ydata)
        ans = re.match('x=(.*) , y=(.*), z=(.*)', tstr)

        if label == 'mass':
            low, high = self.calculation_range(self.mass_range, int(float(ans.group(1))), event.button,
                                               self.min_mass_len, self.ori_mass_range)
            self.mass_range = [low, high]

        elif label == 'scan':
            low, high = self.calculation_range(self.scan_range, int(float(ans.group(2))), event.button,
                                               self.min_scan_len, self.ori_scan_range)
            self.scan_range = [low, high]

        self.draw_all()

    def del_text_while_move(self, event):
        if self.label_move:
            self.label_move.set_text('')
            event.inaxes.texts.remove(self.label_move)

        self.label_move = None
        self.label_name = None
        self.value = None
        self.set_lim()
        plt.draw()

    def del_line_while_click(self):
        if self.label_press:
            self.label_press.set_text('')
            self.ax.texts.remove(self.label_press)
        L = len(self.points)
        for i in range(L):
            self.points[i].remove()

        for i in range(L):
            item = self.points.pop()
            del (item)

        for line in self.scan_lines:
            line.set_data_3d(np.array([0]), np.array([0]), np.array([0]))
        self.scan_tic.set_data_3d(np.array([0]), np.array([0]), np.array([0]))
        self.label_press = None
        self.draw_label = None
        self.draw_value = None
        i = 0
        for item in self.ax.lines:
            item.set_color(self.colors[i])
            i += 1

        self.line.set_data_3d(np.array([0]), np.array([0]), np.array([0]))
        self.set_lim()
        plt.draw()

    def resolve_location(self, xdata, ydata):
        tstr = self.ax.format_coord(xdata, ydata)
        ans = re.match('x=(.*) , y=(.*), z=(.*)', tstr)
        if ans is None:
            return None, None

        x = float(ans.group(1))
        y = float(ans.group(2))
        z = float(ans.group(3))

        A = ((self.mass_range[0] - 0.5) <= x <= self.mass_range[1]) and (
                    self.scan_range[0] - self.scan_lim <= y <= self.scan_range[0] + self.scan_lim)
        B = ((self.mass_range[1] - self.mass_lim) <= x <= (self.mass_range[1] + self.mass_lim)) and (
                    self.scan_range[0] <= y <= (self.scan_range[1] + 0.5))

        if not A and not B:
            return None, None

        label_name = None
        if B:
            value = int(round(y))
            if value < self.scan_range[0]:
                value = self.scan_range[0]
            if value > self.scan_range[1]:
                value = self.scan_range[1]
            return 'scan', value

        else:
            label_name = 'mass'
            if x > self.mass_range[1] + 1 or x < self.mass_range[0] - 1:
                return None, None
            minm = self.mass_range[1]
            mass = 0
            for line in self.ax.lines:
                tmp = line.get_data_3d()[0][0]
                if abs(tmp - x) < minm:
                    minm = abs(tmp - x)
                    mass = tmp

            return 'mass', mass

    def calculation_range(self, ori_range, aim_pos, button, min_len, max_range):
        ori_len = ori_range[1] - ori_range[0] + 1
        if button == 'down':
            # 放大
            aim_len = int(ori_len * self.zoom_param)
        else:
            # 缩小
            aim_len = int(ori_len / self.zoom_param)

        if aim_len >= (max_range[1] - max_range[0] + 1):
            return max_range[0], max_range[1]

        elif aim_len <= min_len:
            aim_len = min_len

        left = int(((aim_pos - ori_range[0] + 1) / ori_len) * aim_len)
        right = aim_len - left
        low = aim_pos - left
        if low < max_range[0]:
            tmp = max_range[0] - low
            low = max_range[0]
            right = right + tmp

        high = aim_pos + right
        if high > max_range[1]:
            tmp = high - max_range[1]
            high = max_range[1]
            left = max(left - tmp, max_range[0])

        return low, high

    def dis(self, pos1, pos2):
        x = (pos1[0] - pos2[0]) ** 2
        y = (pos1[1] - pos2[1]) ** 2
        ret = np.sqrt(x + y)
        return ret

    def init_info(self):
        self.last_position_xy = None
        self.last_press_time = None
        self.double_click_flag = False
        self.scan_lines = []
        self.line = None
        self.label_move = None
        self.label_press = None
        self.points = []
        self.ori_len = None
        self.label_name = None
        self.value = None
        self.colors = []

    def set_lim(self):
        self.ax.set_xlim3d(left=self.mass_range[0])
        self.ax.set_xlim3d(right=self.mass_range[1])
        self.ax.set_ylim3d(bottom=self.scan_range[0])
        self.ax.set_ylim3d(top=self.scan_range[1])
        self.ax.set_zlim3d(bottom=0)


# def draw_one_mass(dict_list, mass, scanstride=1, digital=1):
#     draw_data = []
#     mass = np.round(mass, digital)
#     for i in range(len(dict_list)):
#         if i % scanstride != 0:
#             continue
#         if mass in dict_list[i].keys():
#             one_val = dict_list[i][mass]
#         else:
#             one_val = 0
#         draw_data.append(one_val)
#     return draw_data
#
#
# def data_filter(data_file, mass_range, scan_range, mass_list=None):
#     ret_data = [[], [], []]  # x,y,z
#     if mass_list is None:
#         f = open(data_file, 'rb')
#         rawdata = pk.load(f)
#         for i, mass in enumerate(rawdata[0]):
#             if mass < mass_range[0] or mass > mass_range[1]:
#                 continue
#             ret_data[0].append(mass)
#             ret_data[2].append(rawdata[2][i][scan_range[0]:scan_range[1]])
#
#         ret_data[1] = rawdata[1][scan_range[0]:scan_range[1]]
#         tic = rawdata[3][scan_range[0]:scan_range[1]]
#
#     else:
#         last_index = None
#         for mass in mass_list:
#             if mass < mass_range[0] or mass > mass_range[1]:
#                 continue
#             index = int(mass / SAVEMASSSTRIDE)
#             if index != last_index:
#                 f = open(data_file + str(index) + '.pk', 'rb')
#                 rawalldata = pk.load(f)
#             last_index = index
#             ret_data[0].append(mass)
#             z_data = draw_one_mass(rawalldata, mass)[scan_range[0]:scan_range[1]]
#             ret_data[2].append(z_data)
#
#         ret_data[1] = list(range(scan_range[0], scan_range[1]))
#
#     ret_data.append(tic)
#     return ret_data
#
#
# def draw_3d_plot(data_file, mass_range, scan_range, mass_list=None):
#     # 准备数据，[0]:mass, [1]:range(1400), [2]:intensity
#     alldata = data_filter(data_file, mass_range, scan_range, mass_list)
#     fig = plt.figure(figsize=(12, 8))
#     ax = plt.gca(projection='3d')
#     plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
#     ax.disable_mouse_rotation()
#
#     cursor = EventFactory(ax, alldata, mass_range, scan_range)
#     plt.connect('motion_notify_event', cursor.mouse_move)
#     plt.connect('button_press_event', cursor.mouse_press)
#     plt.connect('button_release_event', cursor.mouse_release)
#     plt.connect('scroll_event', cursor.scroll)
#
#     plt.show()


# if __name__ == '__main__':
#     draw_3d_plot(DATA0, ori_mass_range, ori_scan_range)
