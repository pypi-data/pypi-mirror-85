# coding=utf-8

# @Time: 2020/3/11 11:05
# @Auther: liyubin

import datetime
from airtest.core.api import *
from airtest.core.api import swipe as swipe_air # 为统一config关键字，与swipe函数冲突
from super_sweetest.globals import g
from super_sweetest.log import logger
from super_sweetest.locator import locating_air_element
from super_sweetest.config import element_wait_timeout
from super_sweetest.config import rgb_flag
from super_sweetest.servers.ai_server import aip_ocr
from super_sweetest.servers.ai_server import get_words
from super_sweetest.servers.ai_server import replace_punctuate
from super_sweetest.servers.ai_server import is_language
from super_sweetest.servers.ai_server import get_copywriting
from super_sweetest.servers.ai_server import is_copywriting
from super_sweetest.servers.ai_server import valid_lds_ui
from super_sweetest.servers.ai_server import get_ui_results
from super_sweetest.snapshot import get_air_screenshot
from super_sweetest.servers.common import write_data, read_data



def get_width_height():
    width, height = g.poco.get_screen_size()
    return width, height


def swipe(step):
    """
    1、通过传入的固定坐标滑动

    2、获取设备分辨率计算合适的坐标
    :param poco: 对象
    :param num_list: (0.2, 0.2, 2, 6)
    :return:
    width 宽 w1 w2 小数   0.1-0.9
    height 高  h1 h2 正数 1-9
    """
    num_list = locating_air_element(step)
    duration = step['data'].get('持续时间', 1)


    # 固定坐标滑动
    # start_x = int(num_list[0])
    # start_y = int(num_list[1])
    #
    # end_x = int(num_list[2])
    # end_y = int(num_list[3])
    # if duration:
    #     swipe_air((start_x, start_y), (end_x, end_y), float(duration))
    # else:
    #     swipe_air((start_x, start_y), (end_x, end_y))

    # 相对坐标滑动
    w1 = float(num_list[0])
    w2 = float(num_list[1])
    h1 = float(num_list[2])
    h2 = float(num_list[3])
    width, height = get_width_height()
    start_pt = (float(width * w1), float(height // h1))
    end_pt = (float(width * w2), float(height // h2))

    if duration:
        swipe_air(start_pt, end_pt, float(duration))
    else:
        swipe_air(start_pt, end_pt)
    sleep(1)


def swipe_photo(step):
    value = locating_air_element(step)
    v1 = value[0]
    v2 = value[1]
    swipe_air(Template(filename=v1, rgb=rgb_flag), Template(filename=v2, rgb=rgb_flag))


def tap(step):
    duration = step['data'].get('持续时间', 0.01)
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    if duration:
        touch(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value), duration=float(duration))
    else:
        touch(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def tap_point(step):
    """
    相对坐标点击 TAP_POINT
    point :相对坐标点
    times :点击次数
    :param step:
    :return:
    """
    point, times = locating_air_element(step)
    point1 = point[0]
    point2 = point[1]
    width, height = get_width_height()
    touch([point1*width, point2*height], times=times)


def input(step):
    by, value = locating_air_element(step)
    data = step['data']
    for key in data:
        if by.lower() == 'text':
            if g.platform.lower() == 'air_android':
                g.poco(text=value).set_text(data[key])
            else:
                # ios poco(value).set_text(value)
                g.poco(value).set_text(data[key])
        elif by.lower() == 'textmatches':
            g.poco(textMatches=value).set_text(data[key])
        else:
            if key.startswith('text'):
                text(data['text'], False)
            else:
                text(data[key], False)


def click(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        try:
            if g.platform.lower() == 'air_android':
                g.poco(text=value).click()
            else:
                # ios
                g.poco(value).click()
        except Exception as e:
            sleep(1)
            if g.platform.lower() == 'air_android':
                g.poco(text=value).click()
            else:
                # ios
                g.poco(value).click()
            logger.info('retry poco click, element: %s error msg: %s' % (value, e))
    elif by.lower() == 'textmatches':
        g.poco(textMatches=value).click()
    else:
        assert False, '请指定 element 中 value值：%s 对应的 by 类型为： text'% value


def check(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    assert exists(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def notcheck(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    assert_not_exists(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def check_text(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        if g.platform.lower() == 'air_android':
            assert g.poco(text=value).exists(), '检查文本 %s 失败'%value
        else:
            # ios
            assert g.poco(value).exists(), '检查文本 %s 失败' % value
    elif by.lower() == 'textmatches':
        assert g.poco(textMatches=value).exists(), '模糊检查文本 %s 失败' % value


def notcheck_text(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        if g.platform.lower() == 'air_android':
            if g.poco(text=value).exists(): raise '反向检查文本 %s 失败'%value
        else:
            # ios
            if g.poco(value).exists(): raise '反向检查文本 %s 失败' % value
    elif by.lower() == 'textmatches':
        if g.poco(textMatches=value).exists(): raise  '模糊反向检查文本 %s 失败' % value


def wait_(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    wait(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value), timeout=element_wait_timeout)


def back(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def home(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def menu(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def power(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def delete():
    # 删除输入框内容
    for i in range(30):
        keyevent('KEYCODE_DEL')


def wake_(step):
    """唤醒手机"""
    wake()


############################AI识别#############################

def read_and_write_word(image_path, file_name, new_words):
    """
    读取旧的文本-去重-写入新的文本
    :param image_path: snapshot/plan_name/AI/
    :param file_name: 文件名称.json
    :param new_words: 文本内容 list []
    :return:
    """
    text_path = os.path.join(image_path, file_name)
    if not os.path.exists(text_path):
        write_data(file_name=text_path, data_=[], flag='json', mode='w+')
    read_data_ = read_data(file_name=text_path, flag='json')
    write_data(file_name=text_path, data_=list(set(new_words + read_data_)), flag='json', mode='w+')


def ai_(step):
    """
    AI智能识别
    :param file: 图片地址
    :return:
    """
    # 路径生成
    image_path = os.path.join('snapshot', g.plan_name, 'AI')
    image_path if os.path.exists(image_path) else os.mkdir(image_path)
    time_ms = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S%f')  # 含微秒的日期时间
    file = os.path.join(image_path, time_ms + '.png')
    logger.info('截图所在位置： {}'.format(file))
    # 图片截取
    get_air_screenshot(file)

    # 图像识别
    response_lds_ui = valid_lds_ui(file)
    get_lds_ui_response = get_ui_results(response_lds_ui) # 最后先判断UI异常，再判断文本异常
    logger.info('UI识别结果： {}'.format(response_lds_ui))

    # 通过识别后correct / error / default 目录分类保存
    max_score = 0 # 最大值
    max_name = '' # 最大值对应的name
    for name, score in get_lds_ui_response.items():
        if score > max_score:
            max_score = score
            max_name = name
    max_name_file = os.path.join(image_path, max_name)
    max_name_file if os.path.exists(max_name_file) else os.mkdir(max_name_file)
    lds_ui_name_file = os.path.join(max_name_file, time_ms + '.png') # 按识别分数分类保存
    from PIL import Image
    img = Image.open(file)
    img.save(lds_ui_name_file)
    screen_file_for_maxname = 'UI识别后图片以最大分数: {0} 分类保存在：{1}'.format(max_name, lds_ui_name_file)
    logger.info(screen_file_for_maxname)

    # 识别图像中文本
    words = aip_ocr(file)
    words = get_words(words)
    logger.info('识别后文本： {}'.format(words))
    new_words = replace_punctuate(words, baidu_aip=True)  # 忽略百度AIP识别后异常符号

    # 通过图像中文本识别出语言
    language = is_language(word_list=new_words)
    logger.info('识别出的语言: {}'.format(language))

    # 将识别出的文本保存在本地
    read_and_write_word(image_path, g.plan_name + '_识别文本记录.json', new_words)

    # 通过文案语言类型对文本识别
    officers_data = get_copywriting(language)
    logger.info('文案内容： {}'.format(officers_data))
    flag_list = []
    result_list = []
    error_words = [] # 文案识别后错误文本，最后写入错误识别记录
    for word in new_words:
        # 识别后词语的文案检查
        flag = is_copywriting(word, officers_data)
        result = '文本识别结果： {0},  文本： {1} '.format(flag, word)
        logger.info(result)
        flag_list.append(flag)
        result_list.append(result)
        error_words.append(word) if not flag else None

    # 文案识别错误的文本单独记录
    read_and_write_word(image_path, g.plan_name + '_识别文本error记录.json', error_words)

    # 图片识别结束抛出异常，报告中展示
    result_list.append(screen_file_for_maxname)

    # 检查UI识别 与 文本识别结果，抛出异常
    ui_flag = max_name == 'correct' and max_score > 80 # 最大值name是correct是True, 分数阈值 80
    text_flag = False not in flag_list
    assert (ui_flag and text_flag), ('UI识别结果：{}'.format(str(get_lds_ui_response)), result_list)  # 文本识别结果检查



