import json
import os
import re
import time
from argparse import ArgumentParser, RawTextHelpFormatter
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import requests
from BaseColor.base_colors import green, blue, hgreen, hred, red, hblue
from PIL import Image
from skimage import draw
from skimage.feature import match_template


def tell_the_datetime(time_stamp=None, compact_mode=False, date_sep="-", time_sep=":"):
    time_stamp = time_stamp if time_stamp else time.time()
    if not compact_mode:
        format_str = f'%Y{date_sep}%m{date_sep}%d %H{time_sep}%M{time_sep}%S'
    else:
        format_str = f'%Y{date_sep}%m{date_sep}%d{date_sep}%H{date_sep}%M{date_sep}%S'
    tm = time.strftime(format_str, time.gmtime(time_stamp + (8 * 3600)))
    return tm


def tell_timestamp(time_str=None, str_format='%Y-%m-%d-%H-%M-%S'):
    if time_str:
        time_lis = re.findall(r'\d+', time_str)
        sep_list = re.findall(r"[^\d]+", time_str)
        str_format = ''
        format_base = ["%Y", "%m", "%d", "%H", "%M", "%S"]
        for i in range(len(time_lis)):
            if i < len(sep_list):
                str_format += format_base[i] + sep_list[i]
            else:
                str_format += format_base[i]
    else:
        time_str = tell_the_datetime(compact_mode=True)
    try:
        return int(time.mktime(time.strptime(time_str, str_format)))
    except ValueError as V:
        print(f"[ tell_timestamp ] Error: {V}")
        raise KeyboardInterrupt


class ImageTool(object):

    def __init__(self):
        self.threshold_value = 90
        self._image_show = None
        self.color = {
            'red': [255, 0, 0],
            'yellow': [255, 255, 0],
            'green': [0, 255, 0],
            'cyan': [0, 255, 255],
            'blue': [0, 0, 255],
            'magenta': [255, 0, 255],
            'white': [255, 255, 255],
            'silver': [192, 192, 192],
            'gray': [128, 128, 128],
            'black': [0, 0, 0],
        }

    def locate(self, template_path, template_resize=1.0, img_path=None, locate_center=True, threshold_value=None,
               as_gray=False,
               as_binary=False, img_shape_times=1.0, return_score_only=False):
        if threshold_value:
            self.threshold_value = threshold_value
        if img_path:
            img_array = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times)
            self._image_show = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary,
                                              shape_times=img_shape_times)
        else:
            img_array = self._get_screen_shot(as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times)

        template_array = self._load_img(template_path, as_gray=as_gray, as_binary=as_binary,
                                        shape_times=template_resize)

        result = self._get_result_score(template_array=template_array, image_array=img_array)
        score = (round(result.max(), 4) if result is not None else 0) * 100
        if return_score_only:
            return {"score": score, "template_path": template_path}
        if score and score > self.threshold_value:
            ij = np.unravel_index(np.argmax(result), result.shape)
            if not as_gray:
                c, x, y = ij[::-1]
                tem_h, tem_w, tc = template_array.shape
                ih, iw, ic = img_array.shape
            else:
                x, y = ij[::-1]
                tem_h, tem_w = template_array.shape
                ih, iw = img_array.shape
            x, y = int(x), int(y)
            center = [int(x + tem_w / 2), int(y + tem_h / 2)]
            print(f"[ {green(tell_the_datetime())} ]\n "
                  f"    matching image: [ {blue(img_path or 'ScreenShot')} ]\n "
                  f"    using template: [ {blue(template_path)} ]\n "
                  f"    >>> locate success! score: {hgreen(score)}\n")
            self._draw_box(x, y, tem_h, tem_w, ih, iw, 2, color="red")
            return center if locate_center else [int(x), int(y)]
        else:
            print(f"[ {green(tell_the_datetime())} ]\n "
                  f"    matching image: [ {blue(img_path or 'ScreenShot')} ]\n "
                  f"    using template: [ {blue(template_path)} ]\n "
                  f"    >>> score not pass! score: {hred(score)}\n")

    def patch_locate(self, template_path_list, template_resize=1.0, img_path=None, locate_center=True,
                     threshold_value=None, as_gray=False,
                     as_binary=False, img_shape_times=1.0):
        if threshold_value:
            self.threshold_value = threshold_value
        if img_path:
            img_array = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times)
            self._image_show = self._load_img(img_path, as_gray=as_gray, as_binary=as_binary,
                                              shape_times=img_shape_times)
        else:
            img_array = self._get_screen_shot(as_gray=as_gray, as_binary=as_binary, shape_times=img_shape_times)

        for template_path in template_path_list:
            template_array = self._load_img(template_path, as_gray=as_gray, as_binary=as_binary,
                                            shape_times=template_resize)

            result = self._get_result_score(template_array=template_array, image_array=img_array)
            score = (round(result.max(), 4) if result is not None else 0) * 100
            if score and score > self.threshold_value:
                ij = np.unravel_index(np.argmax(result), result.shape)
                if not as_gray:
                    c, x, y = ij[::-1]
                    tem_h, tem_w, tc = template_array.shape
                    ih, iw, ic = img_array.shape
                else:
                    x, y = ij[::-1]
                    tem_h, tem_w = template_array.shape
                    ih, iw = img_array.shape
                x, y = int(x), int(y)
                center = [int(x + tem_w / 2), int(y + tem_h / 2)]
                print(f"[ {green(tell_the_datetime())} ]\n "
                      f"    matching image: [  {blue(img_path or 'ScreenShot')}  ]\n "
                      f"    using template: [ {blue(template_path)} ]\n "
                      f"    >>> locate success! score: {hgreen(score)}\n")
                self._draw_box(x, y, tem_h, tem_w, ih, iw, 2, color="red")
                return center if locate_center else [int(x), int(y)]
            else:
                print(f"[ {green(tell_the_datetime())} ]\n "
                      f"    matching image: [  {blue(img_path or 'ScreenShot')}  ]\n "
                      f"    using template: [ {blue(template_path)} ]\n "
                      f"    >>> score not pass! score: {hred(score)}\n")

    def _get_screen_shot(self, as_gray=False, as_binary=False, shape_times=1.0):
        screenshot_base_path = "/tmp/for_image_locate_screenshot/"
        if not os.path.exists(screenshot_base_path):
            os.makedirs(screenshot_base_path, exist_ok=True)
        tmp_path = os.path.join(screenshot_base_path, f"{tell_the_datetime(compact_mode=True)}.png")
        pyautogui.screenshot(tmp_path)
        tmp_array = self._load_img(tmp_path, as_gray=as_gray, as_binary=as_binary, shape_times=shape_times)
        self._image_show = tmp_array
        os.remove(tmp_path)
        return tmp_array

    def _draw_box(self, x, y, th, tw, ih, iw, weight=1, color='red'):
        self._image_show = np.array(Image.fromarray(self._image_show).convert("RGB"))
        for Y in range(y, y + weight):
            for X in range(x, x + tw + weight):
                if Y > ih:
                    Y = ih
                if X > iw:
                    X = iw
                self.draw_color(X, Y, color=self.color.get(color))
        for Y in range(y, y + th):
            for X in range(x + tw, x + tw + weight):
                Y = Y if Y <= ih else ih
                X = X if X <= iw else iw
                self.draw_color(X, Y, color=self.color.get(color))
        for Y in range(y + th, y + th + weight):
            for X in range(x, x + tw + weight):
                Y = Y if Y <= ih else ih
                X = X if X <= iw else iw
                self.draw_color(X, Y, color=self.color.get(color))
        for Y in range(y, y + th):
            for X in range(x, x + weight):
                Y = Y if Y <= ih else ih
                X = X if X <= iw else iw
                self.draw_color(X, Y, color=self.color.get(color))

    def draw_color(self, px, py, color=None):
        if color is None:
            color = [255, 255, 255]
        draw_y = np.array([py, py, py + 1, py + 1])
        draw_x = np.array([px, px + 1, px + 1, px])
        rr, cc = draw.polygon(draw_y, draw_x)
        draw.set_color(self._image_show, [rr, cc], color)

    @staticmethod
    def _get_result_score(template_array, image_array):
        result = None
        try:
            result = match_template(image_array, template_array)
            # result = match_template(template_array, image_array)
        except ValueError as e:
            print('sth wrong when matching the template : {}'.format(e))
        finally:
            return result

    @staticmethod
    def _load_img(file_path, as_gray=False, as_binary=False, shape_times=None):
        convert_to = 'RGB'
        if as_gray:
            convert_to = 'L'
        if as_binary:
            convert_to = '1'
        img = Image.open(file_path).convert(convert_to)
        img = img.resize((int(x * shape_times) for x in img.size)) if shape_times else img
        img = np.array(img)
        return img

    @staticmethod
    def load_image_from_url(url):
        if re.findall('^https?://', url):
            res = requests.request("GET", url)
            img = res.content
        else:
            if not re.findall('^/', url):
                base_path = os.getcwd()
                path = os.path.join(base_path, url)
            else:
                path = url
            with open(path, 'rb') as rf:
                img = rf.read()
        bio = BytesIO()
        bio.write(img)
        return bio

    def show(self):
        if self._image_show is not None:
            plt.imshow(self._image_show, plt.cm.gray)
            plt.show()


class FlowTool(object):

    def __init__(self, operate_list, project_name=None):
        """
        step by step
        :param operate_list:
                [{
                    "name": "search image and click",
                    "method": "SearchClick",
                    "icon_path": "/root/... .../image.png",
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "speed": "fast",  # "slow", "mid"
                    "pre_delay": None,
                    "sub_delay": 2,
                },{
                    "name": "search image with multi icons, if one of them matched, then click",
                    "method": "MulSearchClick",
                    "icon_paths": ["/root/... .../image1.png", "/root/... .../image2.png", ...],
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "speed": "fast",  # "slow", "mid"
                    "pre_delay": None,
                    "sub_delay": 2,
                },
                {
                    "name": "open chrome and enter url",
                    "method": "EnterUrl",
                    "url": "http://www.xxx.com",
                    "speed": "fast",
                    "pre_delay": None,
                    "sub_delay": 2,
                },
                {
                    "name": "wait the icon show",
                    "method": "WaitIcon",
                    "icon_path": "/root/... .../icon.png",
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "interval": 1,
                    "after_showed": "NextStep",   # "Return"
                    "time_out": 120,
                    "if_timeout": "End",    #  "NextStep", "Return", "JumpToStep4"
                },
                {
                    "name": "wait until the icon gone",
                    "method": "WaitIconGone",
                    "icon_path": "/root/... .../icon.png",
                    "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
                    "interval": 1,
                    "after_gone": "NextStep",   # "Return"
                    "time_out": 120,
                    "if_timeout": "End",    #  "NextStep", "Return", "JumpToStep5"
                },
                {
                    "name": "save data to a file with vim",
                    "method": "SaveWithVim",
                    "save_path": "/root/... .../icon.json",
                },
                {
                    "name": "terminal opera",
                    "method": "TermCommand",
                    "Command": "redis-cli -p xxxx rpush GrCookies 'diahwdioawafdoanwf;ona;owdaow'",
                },
                {
                    "name": "move mouse to a position and click",
                    "method": "Click",
                    "position": "TopLeft",  #  "TopRight", "BottomLeft", "BottomRight", or [1000, 1000],
                    "pre_delay": None,
                    "sub_delay": 2,
                },
                ...]
        """
        self.project_name = project_name if project_name else f"Project_{tell_the_datetime(compact_mode=True, date_sep='_')}"
        self.operate_list = operate_list
        self.it = ImageTool()
        self.default_match_opt = {
            "template_resize": 1.0,
            "threshold_value": 90,
            "as_gray": True,
            "as_binary": False,
            "img_shape_times": 1.0,
        }
        self.base_path = os.path.split(os.path.abspath(__file__))[0]
        self.default_chrome_icon = os.path.join(self.base_path, "resource/icons/chrome_icon.png")
        self.screen_width, self.screen_height = pyautogui.size()
        self.ms_dic = dict()
        self.total_steps = 0
        self._ready_steps()
        self.methods = self._method_map()

    def _method_map(self):
        return {
            "SearchClick": self._search_and_click,
            "MulSearchClick": self._multi_search_and_click,
            "EnterUrl": self._open_chrome_and_enter_url,
            "WaitIcon": self._wait_icon_show,
            "WaitIconGone": self._wait_icon_gone,
            "SaveWithVim": self._save_data_with_vim,
            "TermCommand": self._save_data_with_vim,
            "Click": self._mouse_click,
            "HotKey": self._hot_key,
            "InputABC": self._input_abc,
        }

    def _ready_steps(self):
        print("steps: ")
        count = 1
        for step_data in self.operate_list:
            self.ms_dic[count] = step_data
            print(f"    [ {green(count)} ] -- [ {green(step_data.get('name'))} ]")
            count += 1
        self.total_steps = len(self.operate_list)

    def _search_and_click(self, params):
        icon_path = params.get("icon_path")
        match_options = params.get("match_options")
        speed = params.get("speed") or "fast"
        not_locate = params.get("not_locate") or "exit"  # "exit", "next1", "jump1"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 1
        jump_step = re.findall(r'\d+', not_locate)

        match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
        time.sleep(int(pre_delay))
        icon_position = self.it.locate(
            template_path=icon_path,
            threshold_value=match_options.get('threshold_value'),
            as_gray=match_options.get('as_gray'),
            as_binary=match_options.get('as_binary'),
            img_shape_times=match_options.get('img_shape_times'),
        )
        if icon_position:
            delay = self._speed(speed)
            self._delay_move(*icon_position, delay=delay)
            pyautogui.click()
            time.sleep(sub_delay)
            return {'next': int(params.get('cur_step', 1)) + 1, "pack": {"position": icon_position}}
        else:
            if not_locate.lower() == "exit":
                print(f"System exit because can not locate template: \n    {icon_path}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': jump_step}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': int(params.get('cur_step', 1)) + int(jump_step)}

    def _multi_search_and_click(self, params):
        icon_paths = params.get("icon_paths")
        match_options = params.get("match_options")
        not_locate = params.get("not_locate") or "next1"    # jump1
        speed = params.get("speed") or "fast"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 1
        jump_step = re.findall(r'\d+', not_locate)

        match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
        time.sleep(int(pre_delay))
        icon_position = self.it.patch_locate(
            template_path_list=icon_paths,
            threshold_value=match_options.get('threshold_value'),
            as_gray=match_options.get('as_gray'),
            as_binary=match_options.get('as_binary'),
            img_shape_times=match_options.get('img_shape_times'),
        )
        if icon_position:
            delay = self._speed(speed)
            self._delay_move(*icon_position, delay=delay)
            pyautogui.click()
            time.sleep(sub_delay)
            return {'next': int(params.get('cur_step', 1)) + 1, "pack": {"position": icon_position}}
        else:
            not_locate = not_locate.lower()
            if not_locate == "exit":
                print(f"System exit because can not locate template: \n    {icon_paths}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': jump_step}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': int(params.get('cur_step', 1)) + int(jump_step)}

    def _open_chrome_and_enter_url(self, params):
        url = params.get("url")
        not_locate = params.get("not_locate") or "next1"    # jump1
        chrome_icon = params.get("chrome_icon")
        speed = params.get("speed") or "fast"
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 5
        jump_step = re.findall(r'\d+', not_locate)

        time.sleep(pre_delay)
        if not chrome_icon or not os.path.exists(chrome_icon):
            chrome_icon = self.default_chrome_icon
        chrome_position = self.it.locate(
            template_path=chrome_icon,
            as_gray=True,
        )
        if chrome_position:
            self._delay_move(*chrome_position)
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'l')
            self._delay_write(url, self._speed(speed))
            pyautogui.press('enter')
            time.sleep(sub_delay)
            return {'next': int(params.get('cur_step', 1)) + 1, "pack": {"position": chrome_position}}
        else:
            not_locate = not_locate.lower()
            if not_locate == "exit":
                print(f"System exit because can not locate chrome icon: \n    {chrome_icon}")
                raise KeyboardInterrupt
            elif "jump" in not_locate.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': jump_step}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': int(params.get('cur_step', 1)) + int(jump_step)}

    def _wait_icon_show(self, params):
        """
        "icon_path": "/root/... .../icon.png",
        "interval": 1,
        "after_showed": "NextStep",   # "ReturnPosition"
        "time_out": 120,
        "if_timeout": "End",    #  "NextStep", "JumpToStep4"
        "match_options": {
                                    "threshold_value": 90,
                                    "as_gray": True,
                                    "as_binary": False
                                    "img_shape_times": 1.0
                                }
        :return:
        """
        icon_path = params.get("icon_path")
        match_options = params.get("match_options")
        interval = int(params.get("interval")) or 1
        after_showed = params.get("after_showed") or "next1"
        time_out = int(params.get("time_out")) or 120
        if_timeout = params.get("if_timeout") or "exit"

        match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
        show_sta = False
        times_start = time.time()
        icon_position = [0, 0]
        while True:
            if time.time() - times_start > time_out:
                break
            icon_position = self.it.locate(
                template_path=icon_path,
                template_resize=match_options.get("template_resize"),
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                img_shape_times=match_options.get('img_shape_times'),
            )
            if icon_position:
                show_sta = True
                break
            time.sleep(interval)
        jump_step = re.findall(r'\d+', after_showed)

        if show_sta:
            jump_step = jump_step[0] if jump_step else 1
            r_dic = {'next': int(params.get('cur_step', 1)) + int(jump_step), 'pack': {'position': icon_position}}
            return r_dic
        else:
            if_timeout = if_timeout.lower()
            if if_timeout == 'exit':
                print(red("\nSys out because icon not found!"))
                print(f"    [ {red(icon_path)} ]\n    [ {tell_the_datetime()} ]")
                raise KeyboardInterrupt
            elif "jump" in if_timeout.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': jump_step}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': int(params.get('cur_step', 1)) + int(jump_step)}

    def _wait_icon_gone(self, params):
        icon_path = params.get("icon_path")
        match_options = params.get("match_options")
        interval = int(params.get("interval")) or 1
        after_gone = params.get("after_gone") or "next1"
        time_out = int(params.get("time_out")) or 120
        if_timeout = params.get("if_timeout") or "exit"

        match_options = match_options if isinstance(match_options, dict) else self.default_match_opt
        gone_sta = False
        times_start = time.time()
        icon_position = [0, 0]
        count = 0
        while True:
            if count > 1 and count % 10 == 0:
                print(f"icon still exist: \n  {icon_path}")
            if time.time() - times_start > time_out:
                break
            icon_position = self.it.locate(
                template_path=icon_path,
                template_resize=match_options.get("template_resize"),
                threshold_value=match_options.get('threshold_value'),
                as_gray=match_options.get('as_gray'),
                img_shape_times=match_options.get('img_shape_times'),
            )
            if not icon_position:
                gone_sta = True
                break
            time.sleep(interval)
            count += 1
        jump_step = re.findall(r'\d+', after_gone)
        if gone_sta:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step), 'pack': {'position': icon_position}}
        else:
            if_timeout = if_timeout.lower()
            if if_timeout == 'exit':
                print(red("\nSys out because timeout when waiting icon gone!"))
                print(f"    [ {red(icon_path)} ]\n    [ {tell_the_datetime()} ]")
                raise KeyboardInterrupt
            elif "jump" in if_timeout.lower():
                jump_step = jump_step[0] if jump_step else 0
                return {'next': jump_step}
            else:
                jump_step = jump_step[0] if jump_step else 1
                return {'next': int(params.get('cur_step', 1)) + int(jump_step)}

    def _save_data_with_vim(self, params):
        file_full_path = params.get("file_full_path")
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 1
        after = params.get("after") or 'next1'

        time.sleep(pre_delay)
        pyautogui.hotkey('ctrl', 'alt', 't')
        time.sleep(0.7)
        self._delay_write(f"vim {file_full_path}", 0.01)
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press(['g', 'g', 'd'])
        pyautogui.hotkey('shift', 'G')
        time.sleep(0.1)
        pyautogui.press('i')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'shift', 'v')
        inserting_vim = True
        while inserting_vim:
            time.sleep(0.5)
            inserting_vim = self.it.locate(
                template_path=os.path.join(self.base_path, 'resource/icons/vim_insert_end.png'),
                threshold_value=95,
                as_gray=True,
                # img_shape_times=1.0
            )
        pyautogui.press('esc')
        time.sleep(0.1)
        pyautogui.hotkey('shift', ';')
        time.sleep(0.1)
        self._delay_write("wq", 0.01)
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'shift', 'q')
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step)}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': jump_step}

    def _terminal_operations(self, params):
        cmd = params.get("cmd")
        root_password = params.get("root_password")
        after = params.get("after") or 'next1'

        pyautogui.hotkey('ctrl', 'alt', 't')
        time.sleep(0.7)
        self._delay_write(f"{cmd}", 0.01)
        time.sleep(0.3)
        pyautogui.press('enter')
        if self.it.locate(
                template_path=os.path.join(self.base_path, 'resource/icons/terminal_input_password.png'),
                as_gray=True,
        ):
            if root_password:
                self._delay_write(f"{root_password}", 0.01)
                time.sleep(0.3)
                pyautogui.press('enter')
            else:
                print("please input password!")
                self._wait_icon_gone({
                    "icon_path": os.path.join(self.base_path, 'resource/icons/terminal_input_password.png'),
                    "match_options": {'as_gray': True},
                    "time_out": 1000000}
                )

        jump_step = re.findall(r'\d+', after.lower())
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step)}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': jump_step}

    def _hot_key(self, params):
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 1
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)
        key_list = params.get('key_list')
        if len(key_list) > 1:
            pyautogui.hotkey(*key_list)
        else:
            pyautogui.press(*key_list)
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step)}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': jump_step}

    def _input_abc(self, params):
        pre_delay = params.get("pre_delay") or 0
        sub_delay = params.get("sub_delay") or 1
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)
        words = params.get('words')
        self._delay_write(f"{words}", 0.01)
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step)}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': jump_step}

    def _mouse_click(self, params):
        """
        position: TopLeft",  #  "center", "TopRight", "BottomLeft", "BottomRight", or [1000, 1000],
        :return:
        """
        position = params.get("position")
        pre_delay = int(params.get("pre_delay")) or 0
        sub_delay = int(params.get("sub_delay")) or 1
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)
        if position == 'TopLeft':
            self._delay_move(1, 1)
        elif position == 'TopRight':
            self._delay_move(self.screen_width - 1, 1)
        elif position == 'center':
            self._delay_move(int(self.screen_width / 2), int(self.screen_height / 2))
        elif position == 'BottomLeft':
            self._delay_move(0, self.screen_height - 1)
        elif position == 'BottomRight':
            self._delay_move(self.screen_width + 1, self.screen_height - 1)
        elif isinstance(position, list):
            self._delay_move(*position)
        pyautogui.click()
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step)}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': jump_step}

    def _mouse_drag(self, params):
        """
        position: TopLeft",  #  "center", "TopRight", "BottomLeft", "BottomRight", or [1000, 1000],
        :return:
        """
        position = params.get("position")
        pre_delay = int(params.get("pre_delay")) or 0
        sub_delay = int(params.get("sub_delay")) or 1
        after = params.get("after") or 'next1'
        time.sleep(pre_delay)
        if position == 'TopLeft':
            self._delay_move(1, 1)
        elif position == 'TopRight':
            self._delay_move(self.screen_width - 1, 1)
        elif position == 'center':
            self._delay_move(int(self.screen_width / 2), int(self.screen_height / 2))
        elif position == 'BottomLeft':
            self._delay_move(0, self.screen_height - 1)
        elif position == 'BottomRight':
            self._delay_move(self.screen_width + 1, self.screen_height - 1)
        elif isinstance(position, list):
            self._delay_drag(*position)
        time.sleep(sub_delay)

        jump_step = re.findall(r'\d+', after.lower())
        if 'next' in after:
            jump_step = jump_step[0] if jump_step else 1
            return {'next': int(params.get('cur_step', 1)) + int(jump_step)}
        else:
            jump_step = jump_step[0] if jump_step else 0
            return {'next': jump_step}

    @staticmethod
    def _speed(speed):
        if isinstance(speed, int) or isinstance(speed, float):
            return speed
        if speed == 'fast':
            delay = 0.5
        elif speed == 'mid':
            delay = 1
        else:
            delay = 2
        return delay

    @staticmethod
    def _delay_move(x, y, delay=0.5):
        pyautogui.moveTo(x, y, duration=delay, tween=pyautogui.easeInOutQuad)

    @staticmethod
    def _delay_drag(x, y, delay=2):
        pyautogui.dragTo(x, y, duration=delay, tween=pyautogui.easeInOutExpo)

    @staticmethod
    def _delay_write(words, delay_for_each=0.1):
        pyautogui.write(words, interval=delay_for_each)

    def start(self):
        step = 1
        pre_pack = {}
        try:
            while True:
                step_data = self.ms_dic.get(step)
                if step_data:
                    name = step_data.get("name")
                    method = step_data.get("method")
                    params = step_data
                    params['cur_step'] = step
                    if pre_pack:
                        params.update(pre_pack)
                    print(f"running step: [ {hgreen(step)} ] -- [ {name} ]")
                    run_result = self.methods.get(method)(params=params)
                    step = run_result.get('next')
                    pre_pack = run_result.get("pack")
                else:
                    print("all process done!")
                    break
        except KeyboardInterrupt:
            print(red(f"[ {tell_the_datetime()} ] sys exit!"))


def load_mission_from_json(jf_path):
    with open(jf_path, 'r') as rf:
        m_list = json.loads(rf.read())

    ft = FlowTool(operate_list=m_list)
    ft.start()


def start_missions():
    dp = '    自动化流程小工具，如果还不清楚怎么使用，请参考 README.md。\n' \
         '    https://github.com/ga1008/basecolors'
    # da = "--->      "
    da = ""
    parser = ArgumentParser(description=dp, formatter_class=RawTextHelpFormatter, add_help=True)
    parser.add_argument("json_file", type=str, help=f'{da}json format step file path, see README.md')
    parser.add_argument("-l", "--loop", type=bool, dest="loop", default=False, help=f'{da}is loop operation? ')
    parser.add_argument("-s", "--start_time", type=str, dest="start_time", default=None,
                        help=f'{da}when to start, default NOW')
    parser.add_argument("-e", "--end_time", type=str, dest="end_time", default=None,
                        help=f'{da}when to end, default FOREVER')

    args = parser.parse_args()
    json_file = args.json_file
    loop = args.loop
    start_time = args.start_time or tell_the_datetime()
    end_time = args.end_time or tell_the_datetime(time_stamp=(time.time() + 3600 * 24 * 365 * 10000))

    if not os.path.exists(json_file):
        print(hred(f"File Not Exists!\n    {json_file}"))
        exit(1)
    if not loop:
        load_mission_from_json(json_file)
    else:
        start_sec = tell_timestamp(start_time)
        end_sec = tell_timestamp(end_time)
        count = 1
        while True:
            now_sec = time.time()
            if now_sec > end_sec:
                print("mission complete!")
                break
            if now_sec > start_sec:
                print(f"running mission with json file [ {hblue(count)} ]: \n    {blue(json_file)}")
                load_mission_from_json(json_file)
            time.sleep(1)
            count += 1


def locate_image():
    dp = '    自动化流程小工具，如果还不清楚怎么使用，请参考 README.md。\n' \
         '    https://github.com/ga1008/basecolors'
    # da = "--->      "
    da = ""
    parser = ArgumentParser(description=dp, formatter_class=RawTextHelpFormatter, add_help=True)
    parser.add_argument("template_image_path", type=str, help=f'{da}the template image path')
    parser.add_argument("-tr", "--template_resize", type=float, dest="template_resize",
                        default=1.0, help=f'{da}resize the template to 1.5/0.7/2 times...')
    parser.add_argument("-th", "--threshold_value", type=int, dest="threshold_value",
                        default=90, help=f'{da} int type, 0-100')
    parser.add_argument("-ag", "--as_gray", dest="as_gray", action='store_true',
                        default=False, help=f'{da} turn the image to gray, it will faster the not')
    parser.add_argument("-ab", "--as_binary", dest="as_binary", action='store_true',
                        default=False, help=f'{da} turn the image to white or black mode, '
                                            f'more faster, but may fail the match in most time')
    parser.add_argument("-ip", "--image_path", type=str, dest="image_path",
                        default=None, help=f'{da}the image wait tobe match, if you not input this param, '
                                           f'program will automatic get a screenshot')
    parser.add_argument("-ir", "--image_resize", type=float, dest="image_resize",
                        default=1.0, help=f'{da}resize the image')
    args = parser.parse_args()
    it = ImageTool()
    print("searching ...")
    it.locate(
        template_path=args.template_image_path,
        template_resize=args.template_resize,
        threshold_value=args.threshold_value,
        as_gray=args.as_gray,
        as_binary=args.as_binary,
        img_path=args.image_path,
        img_shape_times=args.image_resize,
    )
    it.show()


if __name__ == '__main__':
    # it = ImageTool()
    # time.sleep(3)
    # tlc = it.locate(
    #     template_path="/home/ga/Guardian/For-TiZi/flow_operate/resource/icons/terminal_input_password.png",
    #     template_resize=1.0,
    #     as_gray=True,
    #     as_binary=False,
    #     threshold_value=48,
    #     img_shape_times=1.0,
    # )
    # it.show()
    jfp = "/home/ga/Guardian/For-TiZi/flow_operate/test_files/tm1.json"
    load_mission_from_json(jfp)
