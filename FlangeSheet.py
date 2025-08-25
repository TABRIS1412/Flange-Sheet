import sys
import os
# 添加当前目录到系统路径中，确保能正确导入flangeWindow模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
except ImportError:
    print("=" * 60)
    print("错误：未找到 PyQt5 库")
    print("=" * 60)
    print("请在终端中运行以下命令来安装 PyQt5：")
    print("  pip install PyQt5")
    print("")
    print("如果你使用的是虚拟环境，请确保已激活该环境：")
    print("  Windows: venv\\Scripts\\activate")
    print("  macOS/Linux: source venv/bin/activate")
    print("然后再次运行安装命令：")
    print("  pip install PyQt5")
    print("")
    print("更多信息请参考：https://pypi.org/project/PyQt5/")
    print("=" * 60)
    sys.exit(1)
import pandas as pd
from pathlib import Path as pth
import webbrowser
import flangeWindow
from datetime import datetime
import json
from cryptography.fernet import Fernet
import hashlib
import uuid

# 导入资源文件
try:
    import img_source_rc
except ImportError:
    print("警告：无法导入资源文件 img_source_rc.py")
    print("这可能导致界面中的图片无法正常显示")


def get_machine_code():
    """
    生成本机机器码（基于硬件信息）
    与registration_key_validator.py中的方法保持一致
    """
    # 使用MAC地址和一些其他信息作为示例硬件信息
    mac = uuid.getnode()
    machine_code = hashlib.md5(str(mac).encode('utf-8')).hexdigest()
    return machine_code


class FlangePiece:

    def __init__(self, std, tp, dn, pn):

        fl_dict = {'HGT20592<PN系列>': 'HGT20592', 'HGT20615<class系列>': 'HGT20615',
                   'HGT20623<大直径>': 'HGT20623',
                   '带颈对焊<WN>': '带颈对焊', '带颈平焊<SO>': '带颈平焊',
                   '承插焊<SW>':'承插焊', '板式平焊<PL>':'板式平焊',
                   '不锈钢衬里法兰盖<BL(S)>':'不锈钢衬里法兰盖',
                   '对焊环松套<PJ/SE>':'对焊环松套', '法兰盖<BL>':'法兰盖',
                   '螺纹<Th>':'螺纹', '平焊环松套<PJ/RJ>':'平焊环松套', '整体<IF>':'整体',
                   '长高颈<LWN>':'长高颈', '带颈对焊A系列<WN>':'带颈对焊A系列',
                   '带颈对焊B系列<WN>':'带颈对焊B系列',
                   'A系列法兰盖<BL>':'A系列法兰盖', 'B系列法兰盖<BL>':'B系列法兰盖',
                   'NBT47023<容器法兰>':'NBT47023', '带颈对焊<WN_容器>':'带颈对焊'}

        self.std = fl_dict[std]
        self.tp = fl_dict[tp]
        self.dn = dn
        self.pn = pn


    def read_flangePiece_data(self):
        path =  str(pth.cwd())+ "\\Data\\" + str(self.std) + "_" + str(self.tp) + ".csv"

        df = pd.read_csv(path, dtype={'DN': "str", 'PN': "str"})
        # print(df)
        self.sizex = df[(df["DN"] == self.dn) &
                               (df["PN"] == self.pn)]


class FlangeWindow(QMainWindow, flangeWindow.Ui_flangeWindow):


    def __init__(self, parent=None):
        super(FlangeWindow, self).__init__(parent)
        self.setupUi(self)

        std_list = ['HGT20592<PN系列>']
        # , 'HGT20615<class系列>', 'HGT20623<大直径>', 'NBT47023<容器法兰>'
        self.cB_std.addItems(std_list)
        self.cB_std.setCurrentIndex(-1)

        t_std_list = ['HG20533(Ia)系列', 'GB12459/GBT13401<AB系列>', 'ANSI B36.10M、B36.19M<A>', 'HGJ514<无缝管><B>_供参考', 'HGJ528Ⅱ系列<有缝管><B>_供参考']
        self.cB_t_std.addItems(t_std_list)
        self.cB_t_std.setCurrentIndex(0)

        # mfm_list = ['突面<RF>', '凹凸面<FM_M>', '榫槽面<T_G>', '全平面<FF>', '环面R_J' ]
        # self.cB_mfm.addItems(mfm_list)
        # self.cB_mfm.setCurrentIndex(-1)

    def set_tp_list(self):

        zzz = self.cB_tp.currentText()
        self.cB_tp.clear()

        if self.cB_std.currentText() == 'HGT20592<PN系列>':
            tp_list = ['带颈对焊<WN>', '带颈平焊<SO>', '承插焊<SW>', '板式平焊<PL>',
                       '对焊环松套<PJ/SE>', '法兰盖<BL>',
                       '螺纹<Th>', '平焊环松套<PJ/RJ>', '整体<IF>']
            # '不锈钢衬里法兰盖<BL(S)>',
        elif self.cB_std.currentText() == 'HGT20615<class系列>':
            tp_list = ['带颈对焊<WN>', '带颈平焊<SO>', '承插焊<SW>', '对焊环松套<PJ/SE>',
                       '法兰盖<BL>', '螺纹<Th>', '长高颈<LWN>', '整体<IF>']
        elif self.cB_std.currentText() == 'HGT20623<大直径>':
            tp_list = ['带颈对焊A系列<WN>', '带颈对焊B系列<WN>',
                       'A系列法兰盖<BL>', 'B系列法兰盖<BL>']
        elif self.cB_std.currentText() == 'NBT47023<容器法兰>':
            tp_list = ['带颈对焊<WN_容器>']

        self.cB_tp.addItems(tp_list)
        try:
            self.cB_tp.setCurrentText(zzz)
        except:
            pass

    def set_mfm_list(self):

        ttt = self.cB_mfm.currentText()
        self.cB_mfm.clear()
        mfm_list = ['突面<RF>', '凹凸面<FM_M>', '榫槽面<T_G>', '环面R_J',  '全平面<FF>']

        if self.cB_std.currentText() == 'NBT47023<容器法兰>':
            mfm_list = ['平密封面', '凹凸密封面', '榫槽密封面']

        else:

            if self.cB_tp.currentText() == '板式平焊<PL>' \
                    or self.cB_tp.currentText() == '螺纹<Th>':
                mfm_list = ['突面<RF>', '全平面<FF>']
            elif self.cB_tp.currentText() == '带颈平焊<SO>':
                mfm_list = ['突面<RF>', '凹凸面<FM_M>', '榫槽面<T_G>', '全平面<FF>']
            elif self.cB_tp.currentText() == '承插焊<SW>' \
                    or self.cB_tp.currentText() == '平焊环松套<PJ/RJ>' \
                    or self.cB_tp.currentText() == '不锈钢衬里法兰盖<BL(S)>':
                if self.cB_std.currentText() == 'HGT20592<PN系列>':
                    mfm_list = ['突面<RF>', '凹凸面<FM_M>', '榫槽面<T_G>']
                elif self.cB_std.currentText() == 'HGT20615<class系列>':
                    mfm_list = ['突面<RF>', '凹凸面<FM_M>', '榫槽面<T_G>','环面R_J']
            elif self.cB_tp.currentText() == '对焊环松套<PJ/SE>':
                mfm_list = ['突面<RF>']
            elif self.cB_tp.currentText() in ['带颈对焊A系列<WN>', '带颈对焊B系列<WN>',\
                           'A系列法兰盖<BL>', 'B系列法兰盖<BL>']:
                mfm_list = ['突面<RF>', '环面R_J']

        self.cB_mfm.addItems(mfm_list)
        try:
            self.cB_mfm.setCurrentText(ttt)
        except:
            pass

    def set_dn_list(self):

        dn_list_10_2000 = ['10', '15', '20', '25', '32', '40', '50', '65', '80', '100',
                           '125', '150', '200', '250', '300', '350', '400', '450', '500', '600',
                           '700', '800', '900', '1000', '1200', '1400', '1600', '1800', '2000']
        dn_list_10_600 = dn_list_10_2000[:20]
        dn_list_10_300 = dn_list_10_2000[:15]
        dn_list_10_400 = dn_list_10_2000[:17]
        dn_list_10_350 = dn_list_10_2000[:16]
        dn_list_10_1200 = dn_list_10_2000[:25]
        dn_list_15_300 = dn_list_10_2000[1:15]
        dn_list_15_400 = dn_list_10_2000[1:17]
        dn_list_10_50 = dn_list_10_2000[:7]
        dn_list_10_150 = dn_list_10_2000[:12]
        dn_list_40_600 = dn_list_10_2000[5:20]

        dn_c_list_15_600 = ['1/2"', '3/4"', '1"', '1 1/4"', '1 1/2"', '2"', '2 1/2"',
                            '3"', '4"', '5"', '6"', '7"', '8"', '10"', '12"', '14"',
                            '16"', '18"', '20"', '24"']
        dn_c_list_15_65 = dn_c_list_15_600[:7]
        dn_c_list_15_300 = dn_c_list_15_600[:15]
        dn_c_list_25_300 = dn_c_list_15_600[2:15]
        dn_c_list_15_80 = dn_c_list_15_600[:8]
        dn_c_list_25_80 = dn_c_list_15_600[2:8]
        dn_c_list_15_150 = dn_c_list_15_600[:11]
        dn_c_list_25_600 = dn_c_list_15_600[2:]

        dn_c_list_650_1500 = ['26"','28"','30"','32"','34"','36"','38"','40"',
                              '42"','44"','46"','48"','50"','52"','54"','56"','58"','60"']
        dn_c_list_650_900 = dn_c_list_650_1500[:6]
        dn_c_list_650_1000 = dn_c_list_650_1500[:8]

        xxx = self.cB_dn.currentText()
        self.cB_dn.clear()

        if self.cB_std.currentText() == 'HGT20592<PN系列>':
            dn_list = dn_list_10_2000
        elif self.cB_std.currentText() == 'HGT20615<class系列>':
            dn_list = dn_c_list_15_600
        elif self.cB_std.currentText() == 'HGT20623<大直径>':
            dn_list = dn_c_list_650_1500
        elif self.cB_std.currentText() == 'NBT47023<容器法兰>':
            dn_list = ['300','350','400','450','500','550','600','650','700','800','900','1000','1100',
                       '1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200',
                       '2300','2400','2500','2600']

        try:
            if self.cB_std.currentText() == 'HGT20592<PN系列>':

                if self.cB_tp.currentText() == '板式平焊<PL>':

                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentIndex() == -1 or self.cB_pn.currentText()  == '2,5':
                            dn_list = dn_list_10_2000
                        elif self.cB_pn.currentText() in ['6', '10', '16', '25', '40']:
                            dn_list = dn_list_10_600
                    if self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentIndex() == -1 or self.cB_pn.currentText()  == '2,5':
                            dn_list = dn_list_10_2000
                        elif self.cB_pn.currentText() in ['6', '10', '16']:
                            dn_list = dn_list_10_600

                elif self.cB_tp.currentText() == '带颈平焊<SO>':

                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentIndex() == -1:
                            dn_list = dn_list_10_2000
                        elif self.cB_pn.currentText() == '6':
                            dn_list = dn_list_10_300
                        elif self.cB_pn.currentText() in ['10', '16', '25', '40']:
                            dn_list = dn_list_10_600
                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>' \
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['10','16','25','40']:
                            dn_list = dn_list_10_600
                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() == '6':
                            dn_list = dn_list_10_300
                        elif self.cB_pn.currentText() in ['10','16']:
                            dn_list = dn_list_10_600

                elif self.cB_tp.currentText() == '带颈对焊<WN>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['10','16']:
                            dn_list = dn_list_10_2000
                        elif self.cB_pn.currentText() in ['25', '40']:
                            dn_list = dn_list_10_600
                        elif self.cB_pn.currentText() == '63':
                            dn_list = dn_list_10_400
                        elif self.cB_pn.currentText() == '100':
                            dn_list = dn_list_10_350
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_10_300
                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['10', '16', '25', '40']:
                            dn_list = dn_list_10_600
                        elif self.cB_pn.currentText() == '63':
                            dn_list = dn_list_10_400
                        elif self.cB_pn.currentText() == '100':
                            dn_list = dn_list_10_350
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_10_300
                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['10', '16']:
                            dn_list = dn_list_10_2000
                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['63', '100']:
                            dn_list = dn_list_15_400
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_15_300

                elif self.cB_tp.currentText() == '整体<IF>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['6', '10', '16']:
                            dn_list = dn_list_10_2000
                        elif self.cB_pn.currentText() == '25':
                            dn_list = dn_list_10_1200
                        elif self.cB_pn.currentText() == '40':
                            dn_list = dn_list_10_600
                        elif self.cB_pn.currentText() in ['63', '100']:
                            dn_list = dn_list_15_400
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_10_300

                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['10', '16', '25', '40']:
                            dn_list = dn_list_10_600
                        elif self.cB_pn.currentText() in ['63', '100']:
                            dn_list = dn_list_10_400
                        elif self.cB_pn.currentText() in ['160']:
                            dn_list = dn_list_10_300

                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['6', '10', '16']:
                            dn_list = dn_list_10_2000

                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['63','100']:
                            dn_list = dn_list_15_400
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_15_300

                elif self.cB_tp.currentText() == '承插焊<SW>':
                    if self.cB_mfm.currentText() == '突面<RF>'\
                            or self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['10', '16', '25', '40','63', '100']:
                            dn_list = dn_list_10_50

                elif self.cB_tp.currentText() == '螺纹<Th>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['6', '10', '16', '25', '40']:
                            dn_list = dn_list_10_150
                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['6', '10', '16']:
                            dn_list = dn_list_10_150

                elif self.cB_tp.currentText() == '对焊环松套<PJ/SE>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['6','10','16','25','40']:
                            dn_list = dn_list_10_600

                elif self.cB_tp.currentText() == '平焊环松套<PJ/RJ>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['6', '10', '16']:
                            dn_list = dn_list_10_600
                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['10', '16']:
                            dn_list = dn_list_10_600

                elif self.cB_tp.currentText() == '法兰盖<BL>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['2,5', '6']:
                            dn_list = dn_list_10_2000
                        elif self.cB_pn.currentText() in ['10','16']:
                            dn_list = dn_list_10_1200
                        elif self.cB_pn.currentText() in ['25', '40']:
                            dn_list = dn_list_10_600
                        elif self.cB_pn.currentText() in ['63', '100']:
                            dn_list = dn_list_10_400
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_10_300

                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['10', '16', '25', '40']:
                            dn_list = dn_list_10_600
                        elif self.cB_pn.currentText() in ['63', '100']:
                            dn_list = dn_list_10_400
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_10_300

                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['2,5', '6']:
                            dn_list = dn_list_10_2000
                        elif self.cB_pn.currentText() in ['10', '16']:
                            dn_list = dn_list_10_1200

                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['63', '100']:
                            dn_list = dn_list_15_400
                        elif self.cB_pn.currentText() == '160':
                            dn_list = dn_list_15_300

                elif self.cB_tp.currentText() == '不锈钢衬里法兰盖<BL(S)>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['6', '10', '16', '25', '40']:
                            dn_list = dn_list_40_600
                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['10', '16', '25', '40']:
                            dn_list = dn_list_40_600
            elif self.cB_std.currentText() == 'HGT20615<class系列>':
                if self.cB_tp.currentText() == '带颈平焊<SO>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150','class_300', 'class_600', 'class_900']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_1500']:
                            dn_list = dn_c_list_15_65

                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_1500']:
                            dn_list = dn_c_list_15_65

                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_15_600

                elif self.cB_tp.currentText() == '带颈对焊<WN>' \
                        or self.cB_tp.currentText() == '长高颈<LWN>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150','class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300

                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300

                    elif self.cB_mfm.currentText() == '全平面<FF>':
                         if self.cB_pn.currentText() in ['class_150']:
                             dn_list = dn_c_list_15_600

                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_25_300
                        elif self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300

                elif self.cB_tp.currentText() == '整体<IF>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300
                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300
                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_15_600
                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_25_300
                        elif self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300
                elif self.cB_tp.currentText() == '承插焊<SW>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300', 'class_600']:
                            dn_list = dn_c_list_15_80
                        elif self.cB_pn.currentText() in ['class_900', 'class_1500']:
                            dn_list = dn_c_list_15_65
                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['class_300', 'class_600']:
                            dn_list = dn_c_list_15_80
                        elif self.cB_pn.currentText() in ['class_900', 'class_1500']:
                            dn_list = dn_c_list_15_65
                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_25_80
                        elif self.cB_pn.currentText() in ['class_300', 'class_600']:
                            dn_list = dn_c_list_15_80
                        elif self.cB_pn.currentText() in ['class_900', 'class_1500']:
                            dn_list = dn_c_list_15_65
                elif self.cB_tp.currentText() == '螺纹<Th>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300']:
                            dn_list = dn_c_list_15_150
                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_15_150
                elif self.cB_tp.currentText() == '对焊环松套<PJ/SE>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300', 'class_600']:
                            dn_list = dn_c_list_15_600

                elif self.cB_tp.currentText() == '法兰盖<BL>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300
                    elif self.cB_mfm.currentText() == '凹凸面<FM_M>'\
                            or self.cB_mfm.currentText() == '榫槽面<T_G>':
                        if self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300
                    elif self.cB_mfm.currentText() == '全平面<FF>':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_15_600
                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['class_150']:
                            dn_list = dn_c_list_25_600
                        elif self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900', 'class_1500']:
                            dn_list = dn_c_list_15_600
                        elif self.cB_pn.currentText() in ['class_2500']:
                            dn_list = dn_c_list_15_300

            elif self.cB_std.currentText() == 'HGT20623<大直径>':
                if self.cB_tp.currentText() == '带颈对焊A系列<WN>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300', 'class_600']:
                            dn_list = dn_c_list_650_1500
                        elif self.cB_pn.currentText() in ['class_900']:
                            dn_list = dn_c_list_650_1000

                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900']:
                            dn_list = dn_c_list_650_900

                elif self.cB_tp.currentText() == '带颈对焊B系列<WN>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300']:
                            dn_list = dn_c_list_650_1500
                        elif self.cB_pn.currentText() in ['class_600', 'class_900']:
                            dn_list = dn_c_list_650_900

                elif self.cB_tp.currentText() == 'A系列法兰盖<BL>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300', 'class_600']:
                            dn_list = dn_c_list_650_1500
                        elif self.cB_pn.currentText() in ['class_900']:
                            dn_list = dn_c_list_650_1000

                    elif self.cB_mfm.currentText() == '环面R_J':
                        if self.cB_pn.currentText() in ['class_300', 'class_600', 'class_900']:
                            dn_list = dn_c_list_650_900

                elif self .cB_tp.currentText() == 'B系列法兰盖<BL>':
                    if self.cB_mfm.currentText() == '突面<RF>':
                        if self.cB_pn.currentText() in ['class_150', 'class_300']:
                            dn_list = dn_c_list_650_1500
                        elif self.cB_pn.currentText() in ['class_600', 'class_900']:
                            dn_list = dn_c_list_650_900
            elif self.cB_std.currentText() == 'NBT47023<容器法兰>':
                if self.cB_pn.currentText() in ['6']:
                    dn_list = ['1300','1400','1500','1600','1700','1800','1900','2000','2100','2200',
                       '2300','2400','2500','2600']
                elif self.cB_pn.currentText() in ['40']:
                    dn_list = ['300','350','400','450','500','550','600','650','700','800','900','1000','1100',
                       '1200','1300','1400','1500','1600','1700','1800','1900','2000']
                elif self.cB_pn.currentText() in ['64']:
                    dn_list = ['300','350','400','450','500','550','600','650','700','800','900','1000','1100',
                       '1200']


        except Exception as result:
            pass
        finally:
            self.cB_dn.addItems(dn_list)
            try:
                self.cB_dn.setCurrentText(xxx)
            except:
                pass

    def set_pn_list(self):
        yyy = self.cB_pn.currentText()
        self.cB_pn.clear()
        pn_list = ['-']
        if self.cB_std.currentText() == 'HGT20592<PN系列>':
            pn_list = ['2,5', '6', '10','16','25','40','63','100','160']
            if self.cB_tp.currentText() == "板式平焊<PL>":
                pn_list = ['2,5', '6', '10','16','25','40']
            elif self.cB_tp.currentText() == '带颈对焊<WN>':
                pn_list = ['10','16','25','40','63','100','160']
            elif self.cB_tp.currentText() == "整体<IF>":
                pn_list = ['6','10','16','25','40','63','100','160']
            elif self.cB_tp.currentText() == "承插焊<SW>":
                pn_list = ['10','16','25','40','63','100']
            elif self.cB_tp.currentText() == "螺纹<Th>" \
                    or self.cB_tp.currentText() == "对焊环松套<PJ/SE>" \
                    or self.cB_tp.currentText() == "不锈钢衬里法兰盖<BL(S)>" \
                    or self.cB_tp.currentText() == "带颈平焊<SO>":
                pn_list = ['6', '10', '16', '25', '40']
            elif self.cB_tp.currentText() == "平焊环松套<PJ/RJ>":
                pn_list = ['6','10','16']

        elif self.cB_std.currentText() == 'HGT20615<class系列>'\
                or self.cB_std.currentText() == 'HGT20623<大直径>':
            pn_list = ['class_150','class_300', 'class_600', 'class_900', 'class_1500', 'class_2500']
            if self.cB_tp.currentText() == "带颈平焊<SO>" \
                    or self.cB_tp.currentText() == "承插焊<SW>":
                pn_list = ['class_150', 'class_300', 'class_600', 'class_900', 'class_1500']
            elif self.cB_tp.currentText() == "螺纹<Th>":
                pn_list = ['class_150', 'class_300']
            elif self.cB_tp.currentText() == "对焊环松套<PJ/SE>":
                pn_list = ['class_150', 'class_300', 'class_600']
            elif self.cB_tp.currentText() == "带颈对焊A系列<WN>" \
                    or self.cB_tp.currentText() == "带颈对焊B系列<WN>" \
                    or self.cB_tp.currentText() == "A系列法兰盖<BL>" \
                    or self.cB_tp.currentText() == "B系列法兰盖<BL>":
                pn_list = ['class_150', 'class_300', 'class_600', 'class_900']
        elif self.cB_std.currentText() == 'NBT47023<容器法兰>':
            pn_list = ['6', '10', '16', '25', '40','64']

        self.cB_pn.addItems(pn_list)
        try:
            self.cB_pn.setCurrentText(yyy)
        except:
            self.cB_pn.setCurrentIndex(-1)

    def choose_tp(self):

        if self.cB_tp.currentText() == '带颈对焊<WN>':
            self.tW_size.setCurrentIndex(0)  # 设置tab标签为序号为0的项
        elif self.cB_tp.currentText() == "带颈平焊<SO>":
            self.tW_size.setCurrentIndex(1)
        elif self.cB_tp.currentText() == "承插焊<SW>":
            self.tW_size.setCurrentIndex(2)
        elif self.cB_tp.currentText() == "板式平焊<PL>":
            self.tW_size.setCurrentIndex(3)
        # elif self.cB_tp.currentText() == "不锈钢衬里法兰盖<BL(S)>":
        #     self.tW_size.setCurrentIndex(4)
        elif self.cB_tp.currentText() == "对焊环松套<PJ/SE>":
            if self.cB_std.currentText() == "HGT20592<PN系列>":
                self.tW_size.setCurrentIndex(5)
            elif self.cB_std.currentText() == "HGT20615<class系列>":
                self.tW_size.setCurrentIndex(15)
        elif self.cB_tp.currentText() == "法兰盖<BL>":
            self.tW_size.setCurrentIndex(6)
        elif self.cB_tp.currentText() == "螺纹<Th>":
            self.tW_size.setCurrentIndex(7)
        elif self.cB_tp.currentText() == "平焊环松套<PJ/RJ>":
            self.tW_size.setCurrentIndex(8)
        elif self.cB_tp.currentText() == "整体<IF>":
            self.tW_size.setCurrentIndex(9)
        elif self.cB_tp.currentText() == "长高颈<LWN>":
            self.tW_size.setCurrentIndex(10)
        elif self.cB_tp.currentText() == "带颈对焊A系列<WN>" \
                or self.cB_tp.currentText() == "带颈对焊B系列<WN>":
            self.tW_size.setCurrentIndex(11)
        # elif self.cB_tp.currentText() == "带颈对焊B系列<WN>":
        #     self.tW_size.setCurrentIndex(12)
        elif self.cB_tp.currentText() == "A系列法兰盖<BL>" \
                or self.cB_tp.currentText() == "B系列法兰盖<BL>":
            self.tW_size.setCurrentIndex(13)
        elif self.cB_tp.currentText() == "带颈对焊<WN_容器>":
            self.tW_size.setCurrentIndex(14)

        else:
            self.tW_size.setCurrentIndex(0)


    def choose_mfm(self):

        if self.cB_mfm.currentText() == '突面<RF>':  # 突面的尺寸可以在法兰上标注
            self.tW_mfm.setCurrentIndex(0)  # 设置tab标签为序号为0的项
        elif self.cB_mfm.currentText() == "凹凸面<FM_M>":
            self.tW_mfm.setCurrentIndex(1)
        elif self.cB_mfm.currentText() == "榫槽面<T_G>":
            self.tW_mfm.setCurrentIndex(2)
        elif self.cB_mfm.currentText() == "全平面<FF>":
            self.tW_mfm.setCurrentIndex(3)
        elif self.cB_mfm.currentText() == "环面R_J":
            self.tW_mfm.setCurrentIndex(4)

        elif self.cB_mfm.currentText() == '平密封面':
            self.tW_mfm.setCurrentIndex(5)
        elif self.cB_mfm.currentText() == '凹凸密封面':
            self.tW_mfm.setCurrentIndex(6)
        elif self.cB_mfm.currentText() == '榫槽密封面':
            self.tW_mfm.setCurrentIndex(7)

        else:
            self.tW_mfm.setCurrentIndex(0)

    def buid_flange_piece(self):

        # 初始化所有标签为默认值，确保每次更新时旧值被清除
 #       self._clear_all_labels()

        if self.cB_std.currentIndex() != -1 and self.cB_tp.currentIndex() != -1 \
               and self.cB_dn.currentIndex() != -1 and self.cB_pn.currentIndex() != -1:
            try:
                self.a_flange = FlangePiece(self.cB_std.currentText(), self.cB_tp.currentText(),
                                        self.cB_dn.currentText(), self.cB_pn.currentText())
                self.a_flange.read_flangePiece_data()
                # print(self.a_flange.sizex.info())


                if self.cB_tp.currentText() == '带颈对焊<WN>':  # 几个标准的法兰尺寸是不一样的，需要单独画图

                    try:
                        self.lbs_wn_k.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_wn_c.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_wn_d.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        self.lbs_wn_h.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                        # self.lbs_wn_h1.setText(str(self.a_flange.sizex.iloc[0].at['H1_mean']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_wn_nl.setText(nl)
                        nab = str(self.a_flange.sizex.iloc[0].at['N_A']) \
                              + '(' + str(self.a_flange.sizex.iloc[0].at['N_B']) + ')'
                        self.lbs_wn_NAB.setText(nab)
                        a1ab = str(self.a_flange.sizex.iloc[0].at['A1_A']) \
                              + '(' + str(self.a_flange.sizex.iloc[0].at['A1_B']) + ')'
                        self.lbs_wn_A1AB.setText(a1ab)

                        # self.lbs_wn_s.setText(str(self.a_flange.sizex.iloc[0].at['S_min']))
                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_wn_k.setText("-")
                        self.lbs_wn_c.setText('-')
                        self.lbs_wn_d.setText('-')
                        self.lbs_wn_h.setText('-')
                        self.lbs_wn_nl.setText('-')
                        self.lbs_wn_NAB.setText('-')
                        self.lbs_wn_A1AB.setText('-')

                elif self.cB_tp.currentText() == "带颈平焊<SO>":
                    try:
                        self.lbs_so_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_so_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_so_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        self.lbs_so_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                        # self.lbs_wn_h1.setText(str(self.a_flange.sizex.iloc[0].at['H1_mean']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_so_nl.setText(nl)
                        nab = str(self.a_flange.sizex.iloc[0].at['N_A']) \
                                 +'('+str(self.a_flange.sizex.iloc[0].at['N_B']) + ')'
                        self.lbs_so_NAB.setText(nab)
                        b1ab = str(self.a_flange.sizex.iloc[0].at['B1_A']) \
                                 + '(' + str(self.a_flange.sizex.iloc[0].at['B1_B']) + ')'
                        self.lbs_so_B1_AB.setText(b1ab)

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_so_K.setText('-')
                        self.lbs_so_C.setText('-')
                        self.lbs_so_D.setText('-')
                        self.lbs_so_H.setText('-')
                        self.lbs_so_nl.setText('-')
                        self.lbs_so_NAB.setText('-')
                        self.lbs_so_B1_AB.setText('-')

                elif self.cB_tp.currentText() == "承插焊<SW>":

                    try:
                        self.lbs_sw_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_sw_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_sw_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        self.lbs_sw_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                        self.lbs_sw_U.setText(str(self.a_flange.sizex.iloc[0].at['U']))
                        # self.lbs_wn_h1.setText(str(self.a_flange.sizex.iloc[0].at['H1_mean']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_sw_nl.setText(nl)
                        nab = str(self.a_flange.sizex.iloc[0].at['N'])
                        self.lbs_sw_N.setText(nab)
                        b2ab = str(self.a_flange.sizex.iloc[0].at['B2_A']) \
                               + '(' + str(self.a_flange.sizex.iloc[0].at['B2_B']) + ')'
                        self.lbs_sw_B2.setText(b2ab)

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_sw_K.setText('-')
                        self.lbs_sw_C.setText('-')
                        self.lbs_sw_D.setText('-')
                        self.lbs_sw_H.setText('-')
                        self.lbs_sw_U.setText('-')
                        self.lbs_sw_nl.setText('-')
                        self.lbs_sw_N.setText('-')
                        self.lbs_sw_B2.setText('-')

                elif self.cB_tp.currentText() == "板式平焊<PL>":

                    try:
                        self.lbs_pl_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_pl_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_pl_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_pl_nl.setText(nl)
                        b1ab = str(self.a_flange.sizex.iloc[0].at['B1_A']) \
                                 + '(' + str(self.a_flange.sizex.iloc[0].at['B1_B']) + ')'
                        self.lbs_pl_B1AB.setText(b1ab)

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_pl_K.setText('-')
                        self.lbs_pl_C.setText('-')
                        self.lbs_pl_D.setText('-')
                        self.lbs_pl_nl.setText('-')
                        self.lbs_pl_B1AB.setText('-')


                elif self.cB_tp.currentText() == "不锈钢衬里法兰盖<BL(S)>":
                    pass
                elif self.cB_tp.currentText() == "对焊环松套<PJ/SE>":
                    if self.cB_std.currentText() == "HGT20592<PN系列>":
                        try:
                            self.lbs_pjse_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                            self.lbs_pjse_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                            self.lbs_pjse_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                            nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                            self.lbs_pjse_nl.setText(nl)
                            b1ab = str(self.a_flange.sizex.iloc[0].at['B1_A']) \
                                     + '(' + str(self.a_flange.sizex.iloc[0].at['B1_B']) + ')'
                            self.lbs_pjse_B1.setText(b1ab)
                            a1ab = str(self.a_flange.sizex.iloc[0].at['A1_A']) \
                                   + '(' + str(self.a_flange.sizex.iloc[0].at['A1_B']) + ')'
                            self.lbs_pjse_A1.setText(a1ab)
                            self.lbs_pjse_d.setText(str(self.a_flange.sizex.iloc[0].at['RF_d']))
                            self.lbs_pjse_h.setText(str(self.a_flange.sizex.iloc[0].at['h']))
                            self.lbs_pjse_S1.setText(str(self.a_flange.sizex.iloc[0].at['S1']))

                        except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                            self.lbs_pjse_K.setText('-')
                            self.lbs_pjse_C.setText('-')
                            self.lbs_pjse_D.setText('-')
                            self.lbs_pjse_nl.setText('-')
                            self.lbs_pjse_B1.setText('-')
                            self.lbs_pjse_A1.setText('-')
                            self.lbs_pjse_d.setText('-')
                            self.lbs_pjse_h.setText('-')
                            self.lbs_pjse_S1.setText('-')

                    elif self.cB_std.currentText() == "HGT20615<class系列>":
                        try:
                            self.lbs_pjsec_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                            self.lbs_pjsec_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                            self.lbs_pjsec_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                            nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(
                                self.a_flange.sizex.iloc[0].at['L'])
                            self.lbs_pjsec_nl.setText(nl)
                            b1a = str(self.a_flange.sizex.iloc[0].at['B1_A'])
                            self.lbs_pjsec_B.setText(b1a)
                            a1a = str(self.a_flange.sizex.iloc[0].at['A1_A'])
                            self.lbs_pjsec_A.setText(a1a)
                            self.lbs_pjsec_d.setText(str(self.a_flange.sizex.iloc[0].at['RF_d']))
                            self.lbs_pjsec_h.setText(str(self.a_flange.sizex.iloc[0].at['h']))
                            self.lbs_pjsec_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                            self.lbs_pjsec_N.setText(str(self.a_flange.sizex.iloc[0].at['N']))
                            self.lbs_pjsec_S1.setText('-')


                        except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                            self.lbs_pjse_K.setText('-')
                            self.lbs_pjse_C.setText('-')
                            self.lbs_pjse_D.setText('-')
                            self.lbs_pjse_nl.setText('-')
                            self.lbs_pjse_B1.setText('-')
                            self.lbs_pjse_A1.setText('-')
                            self.lbs_pjse_d.setText('-')
                            self.lbs_pjse_h.setText('-')
                            # self.lbs_pjse_S1.setText('-')


                elif self.cB_tp.currentText() == "法兰盖<BL>":

                    try:
                        self.lbs_bl_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_bl_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_bl_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_bl_nl.setText(nl)

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_bl_K.setText('-')
                        self.lbs_bl_C.setText('-')
                        self.lbs_bl_D.setText('-')
                        self.lbs_bl_nl.setText('-')

                elif self.cB_tp.currentText() == "螺纹<Th>":

                    try:
                        self.lbs_th_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_th_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_th_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        self.lbs_th_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                        self.lbs_th_N.setText(str(self.a_flange.sizex.iloc[0].at['N']))
                        # self.lbs_wn_h1.setText(str(self.a_flange.sizex.iloc[0].at['H1_mean']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_th_nl.setText(nl)
                        self.lbs_th_LW.setText(str(self.a_flange.sizex.iloc[0].at['LW']))

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_th_K.setText('-')
                        self.lbs_th_C.setText('-')
                        self.lbs_th_D.setText('-')
                        self.lbs_th_H.setText('-')
                        self.lbs_th_N.setText('-')
                        self.lbs_th_nl.setText('-')
                        self.lbs_th_LW.setText('-')

                elif self.cB_tp.currentText() == "平焊环松套<PJ/RJ>":

                    try:
                        self.lbs_pjrj_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_pjrj_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_pjrj_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_pjrj_nl.setText(nl)
                        b1ab = str(self.a_flange.sizex.iloc[0].at['B1_A']) \
                                 + '(' + str(self.a_flange.sizex.iloc[0].at['B1_B']) + ')'
                        self.lbs_pjrj_B1.setText(b1ab)
                        a1ab = str(self.a_flange.sizex.iloc[0].at['A1_A']) \
                               + '(' + str(self.a_flange.sizex.iloc[0].at['A1_B']) + ')'
                        self.lbs_pjrj_A1.setText(a1ab)
                        b2ab = str(self.a_flange.sizex.iloc[0].at['B2_A']) \
                               + '(' + str(self.a_flange.sizex.iloc[0].at['B2_B']) + ')'
                        self.lbs_pjrj_B2.setText(b2ab)
                        self.lbs_pjrj_d.setText(str(self.a_flange.sizex.iloc[0].at['H_d']))
                        self.lbs_pjrj_F.setText(str(self.a_flange.sizex.iloc[0].at['F']))

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_pjrj_K.setText('-')
                        self.lbs_pjrj_C.setText('-')
                        self.lbs_pjrj_D.setText('-')
                        self.lbs_pjrj_nl.setText('-')
                        self.lbs_pjrj_B1.setText('-')
                        self.lbs_pjrj_A1.setText('-')
                        self.lbs_pjrj_B2.setText('-')
                        self.lbs_pjrj_d.setText('-')
                        self.lbs_pjrj_F.setText('-')

                elif self.cB_tp.currentText() == "整体<IF>":

                    try:
                        self.lbs_if_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_if_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_if_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        self.lbs_if_Smin.setText(str(self.a_flange.sizex.iloc[0].at['S_min']))
                        # self.lbs_wn_h1.setText(str(self.a_flange.sizex.iloc[0].at['H1_mean']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_if_nl.setText(nl)
                        self.lbs_if_N.setText(str(self.a_flange.sizex.iloc[0].at['N']))

                        # self.lbs_wn_s.setText(str(self.a_flange.sizex.iloc[0].at['S_min']))
                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_if_K.setText("-")
                        self.lbs_if_C.setText('-')
                        self.lbs_if_D.setText('-')
                        self.lbs_if_Smin.setText('-')
                        self.lbs_if_nl.setText('-')
                        self.lbs_if_N.setText('-')

                elif self.cB_tp.currentText() == "长高颈<LWN>":

                    try:
                        self.lbs_lwn_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_lwn_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_lwn_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        self.lbs_lwn_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                        # self.lbs_wn_h1.setText(str(self.a_flange.sizex.iloc[0].at['H1_mean']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_lwn_nl.setText(nl)
                        self.lbs_lwn_N.setText(str(self.a_flange.sizex.iloc[0].at['N_A']))

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_lwn_K.setText('-')
                        self.lbs_lwn_C.setText('-')
                        self.lbs_lwn_D.setText('-')
                        self.lbs_lwn_H.setText('-')
                        self.lbs_lwn_nl.setText('-')
                        self.lbs_lwn_N.setText('-')

                elif self.cB_tp.currentText() == "带颈对焊A系列<WN>" \
                        or self.cB_tp.currentText() == "带颈对焊B系列<WN>":

                    try:
                        self.lbs_awn_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_awn_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_awn_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_awn_nl.setText(nl)
                        self.lbs_awn_A.setText(str(self.a_flange.sizex.iloc[0].at['A1_A']))
                        self.lbs_awn_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                        self.lbs_awn_N.setText(str(self.a_flange.sizex.iloc[0].at['N_A']))
                        self.lbs_awn_B.setText('-')

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_awn_K.setText('-')
                        self.lbs_awn_C.setText('-')
                        self.lbs_awn_D.setText('-')
                        self.lbs_awn_nl.setText('-')
                        self.lbs_awn_A.setText('-')
                        self.lbs_awn_H.setText('-')
                        self.lbs_awn_N.setText('-')
                        self.lbs_awn_B.setText('-')

                # elif self.cB_tp.currentText() == "带颈对焊B系列<WN>":
                #     pass
                elif self.cB_tp.currentText() == "A系列法兰盖<BL>" \
                        or self.cB_tp.currentText() == "B系列法兰盖<BL>":
                    try:
                        self.lbs_abl_K.setText(str(self.a_flange.sizex.iloc[0].at['K']))  # 选取第0行某一列的值
                        self.lbs_abl_C.setText(str(self.a_flange.sizex.iloc[0].at['C']))
                        self.lbs_abl_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        nl = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['L'])
                        self.lbs_abl_nl.setText(nl)

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_awn_K.setText('-')
                        self.lbs_awn_C.setText('-')
                        self.lbs_awn_D.setText('-')
                        self.lbs_awn_nl.setText('-')


# 剩余法兰尺寸设置及密封面尺寸设置

                elif self.cB_tp.currentText() == "带颈对焊<WN_容器>":
                    try:
                        self.lbs_nbt_D.setText(str(self.a_flange.sizex.iloc[0].at['D']))
                        nd = str(self.a_flange.sizex.iloc[0].at['n']) + '×Φ' + str(self.a_flange.sizex.iloc[0].at['d'])
                        self.lbs_nbt_d.setText(nd)

                        self.lbs_nbt_h.setText(str(self.a_flange.sizex.iloc[0].at['h']))
                        self.lbs_nbt_DN.setText(str(self.a_flange.sizex.iloc[0].at['DN']))
                        self.lbs_nbt_D1.setText(str(self.a_flange.sizex.iloc[0].at['D1']))

                        self.lbs_nbt_dta0.setText(str(self.a_flange.sizex.iloc[0].at['dta0']))
                        self.lbs_nbt_dta1.setText(str(self.a_flange.sizex.iloc[0].at['dta1']))
                        self.lbs_nbt_dta2.setText(str(self.a_flange.sizex.iloc[0].at['dta2']))
                        self.lbs_nbt_Th.setText(str(self.a_flange.sizex.iloc[0].at['Th']))

                    except:  # 标签读不到数的时候，标签要初始化，否则会显示上次的值，错误引导
                        self.lbs_nbt_D.setText('-')
                        self.lbs_nbt_d.setText('-')

                        self.lbs_nbt_h.setText('-')
                        self.lbs_nbt_DN.setText('-')
                        self.lbs_nbt_D1.setText('-')

                        self.lbs_nbt_dta0.setText('-')
                        self.lbs_nbt_dta1.setText('-')
                        self.lbs_nbt_dta2.setText('-')
                        self.lbs_nbt_Th.setText('-')

                #密封面尺寸设置
                try:
                    self.lbs_mfm_rf_d.setText(str(self.a_flange.sizex.iloc[0].at['RF_d']))
                except:
                    self.lbs_mfm_rf_d.setText('-')

                try:
                    self.lbs_mfm_rf_f1.setText(str(self.a_flange.sizex.iloc[0].at['RF_f1']))
                except:
                    self.lbs_mfm_rf_f1.setText('-')

                try:
                    self.lbs_mfm_f1.setText(str(self.a_flange.sizex.iloc[0].at['f1']))
                except:
                    self.lbs_mfm_f1.setText('-')

                try:
                    self.lbs_mfm_x.setText(str(self.a_flange.sizex.iloc[0].at['X']))
                except:
                    self.lbs_mfm_x.setText('-')

                try:
                    self.lbs_mfm_f2.setText(str(self.a_flange.sizex.iloc[0].at['f2']))
                except:
                    self.lbs_mfm_f2.setText('-')

                try:
                    self.lbs_mfm_y.setText(str(self.a_flange.sizex.iloc[0].at['Y']))
                except:
                    self.lbs_mfm_y.setText('-')

                try:
                    self.lbs_mfm_d.setText(str(self.a_flange.sizex.iloc[0].at['d']))
                except:
                    self.lbs_mfm_d.setText('-')

                try:
                    self.lbs_mfm_f3.setText(str(self.a_flange.sizex.iloc[0].at['f3']))
                except:
                    self.lbs_mfm_f3.setText('-')

                try:
                    self.lbs_tg_d.setText(str(self.a_flange.sizex.iloc[0].at['d']))
                except:
                    self.lbs_tg_d.setText('-')

                try:
                    self.lbs_tg_w.setText(str(self.a_flange.sizex.iloc[0].at['W']))
                except:
                    self.lbs_tg_w.setText('-')

                try:
                    self.lbs_tg_x.setText(str(self.a_flange.sizex.iloc[0].at['X']))
                except:
                    self.lbs_tg_x.setText('-')

                try:
                    self.lbs_tg_y.setText(str(self.a_flange.sizex.iloc[0].at['Y']))
                except:
                    self.lbs_tg_y.setText('-')

                try:
                    self.lbs_tg_z.setText(str(self.a_flange.sizex.iloc[0].at['Z']))
                except:
                    self.lbs_tg_z.setText('-')

                try:
                    self.lbs_tg_f1.setText(str(self.a_flange.sizex.iloc[0].at['f1']))
                except:
                    self.lbs_tg_f1.setText('-')

                try:
                    self.lbs_tg_f2.setText(str(self.a_flange.sizex.iloc[0].at['f2']))
                except:
                    self.lbs_tg_f2.setText('-')

                try:
                    self.lbs_tg_f3.setText(str(self.a_flange.sizex.iloc[0].at['f3']))
                except:
                    self.lbs_tg_f3.setText('-')

                try:
                    self.lbs_rj_d.setText(str(self.a_flange.sizex.iloc[0].at['RJ_d']))
                except:
                    self.lbs_rj_d.setText('-')

                try:
                    self.lbs_rj_e.setText(str(self.a_flange.sizex.iloc[0].at['E']))
                except:
                    self.lbs_rj_e.setText('-')

                try:
                    self.lbs_rj_f.setText(str(self.a_flange.sizex.iloc[0].at['F']))
                except:
                    self.lbs_rj_f.setText('-')

                try:
                    self.lbs_rj_p.setText(str(self.a_flange.sizex.iloc[0].at['P']))
                except:
                    self.lbs_rj_p.setText('-')

                try:
                    self.lbs_rj_e2.setText(str(self.a_flange.sizex.iloc[0].at['E']))
                except:
                    self.lbs_rj_e2.setText('-')



                try:
                    self.lbs_rq1_D3.setText(str(self.a_flange.sizex.iloc[0].at['D3']))
                    self.lbs_rq2_D2.setText(str(self.a_flange.sizex.iloc[0].at['D2']))
                    self.lbs_rq2_D3.setText(str(self.a_flange.sizex.iloc[0].at['D3']))
                    self.lbs_rq2_D4.setText(str(self.a_flange.sizex.iloc[0].at['D4']))
                    self.lbs_rq3_a.setText(str(self.a_flange.sizex.iloc[0].at['a']))
                    self.lbs_rq3_a1.setText(str(self.a_flange.sizex.iloc[0].at['a1']))
                    self.lbs_rq3_D2.setText(str(self.a_flange.sizex.iloc[0].at['D2']))
                    self.lbs_rq3_D3.setText(str(self.a_flange.sizex.iloc[0].at['D3']))
                    self.lbs_rq3_D4.setText(str(self.a_flange.sizex.iloc[0].at['D4']))

                    self.lbs_rq1_dta.setText(str(self.a_flange.sizex.iloc[0].at['dta']))
                    self.lbs_rq1_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))

                    self.lbs_rq2_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                    self.lbs_rq2_HH.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                    self.lbs_rq2_dta.setText(str(self.a_flange.sizex.iloc[0].at['dta']))
                    self.lbs_rq2_dtaa.setText(str(self.a_flange.sizex.iloc[0].at['dta']))

                    self.lbs_rq3_H.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                    self.lbs_rq3_HH.setText(str(self.a_flange.sizex.iloc[0].at['H']))
                    self.lbs_rq3_dta.setText(str(self.a_flange.sizex.iloc[0].at['dta']))
                    self.lbs_rq3_dtaa.setText(str(self.a_flange.sizex.iloc[0].at['dta']))

                except:
                    self.lbs_rq1_D3.setText('-')
                    self.lbs_rq2_D2.setText('-')
                    self.lbs_rq2_D3.setText('-')
                    self.lbs_rq2_D4.setText('-')
                    self.lbs_rq3_a.setText('-')
                    self.lbs_rq3_a1.setText('-')
                    self.lbs_rq3_D2.setText('-')
                    self.lbs_rq3_D3.setText('-')
                    self.lbs_rq3_D4.setText('-')

                    self.lbs_rq1_dta.setText('-')
                    self.lbs_rq1_H.setText('-')

                    self.lbs_rq2_H.setText('-')
                    self.lbs_rq2_HH.setText('-')
                    self.lbs_rq2_dta.setText('-')
                    self.lbs_rq2_dtaa.setText('-')

                    self.lbs_rq3_H.setText('-')
                    self.lbs_rq3_HH.setText('-')
                    self.lbs_rq3_dta.setText('-')
                    self.lbs_rq3_dtaa.setText('-')

                # 不同密封面螺栓设置
                try:
                    self.lbth_rf_lsr.setText("突面<六角头螺栓> "+str(self.a_flange.sizex.iloc[0].at['Th'])
                                            + "/ 长度 " + str(self.a_flange.sizex.iloc[0].at['LSR']))
                except:
                    self.lbth_rf_lsr.setText('突面<六角头螺栓>/ 长度 -')

                try:
                    self.lbth_rf_lzr.setText("突面<全螺纹/双头螺柱> " + str(self.a_flange.sizex.iloc[0].at['Th'])
                                             + "/ 长度 " + str(self.a_flange.sizex.iloc[0].at['LZR']))
                except:
                    self.lbth_rf_lzr.setText('突面<全螺纹/双头螺柱>/ 长度 -')

                try:
                    self.lbth_mfm_lzm.setText("凹凸面<全螺纹/双头螺柱> " + str(self.a_flange.sizex.iloc[0].at['Th'])
                                             + '/ 长度 ' + str(self.a_flange.sizex.iloc[0].at['LZM']))
                except:
                    self.lbth_mfm_lzm.setText('凹凸面<全螺纹/双头螺柱>/ 长度 -')

                try:
                    self.lbth_rj_lzj.setText("环连接面<全螺纹/双头螺柱> " + str(self.a_flange.sizex.iloc[0].at['Th'])
                                             + '/ 长度 ' + str(self.a_flange.sizex.iloc[0].at['LZJ']))
                except:
                    self.lbth_rj_lzj.setText('环连接面<全螺纹/双头螺柱>/ 长度 -')

            except Exception:
                # print("没有这种类型的法兰，请重新选择: %s" %result) # 这里可以设计一个对话框显示
                # QMessageBox.information(self, "出错啦！",
                #                         "这种规格的选择找不到对应的数据，重新选择一下应该就可以了！")
                pass

    def set_t_sch(self):
        t111 = self.cB_t_sch.currentText()

        if self.cB_t_std.currentText() == 'HGJ514<无缝管><B>_供参考':

            self.cB_t_sch.clear()
            t_sch_list = ['PN25', 'PN40', 'PN63', 'PN100']
            t_sch_dict = {'25':'PN25', '40':'PN40', '63': 'PN63', '100': 'PN100'}
            self.cB_t_sch.addItems(t_sch_list)

            if self.cB_pn.currentText() in ['25', '40', '63', '100']:
                self.cB_t_sch.setCurrentText(t_sch_dict[self.cB_pn.currentText()])
            else:
                self.cB_t_sch.setCurrentIndex(-1)

        elif self.cB_t_std.currentText() == 'HGJ528Ⅱ系列<有缝管><B>_供参考':
            self.cB_t_sch.clear()
            t_sch_list = ['PN10', 'PN16', 'PN25']
            t_sch_dict = {'10':'PN10', '16':'PN16', '25': 'PN25'}
            self.cB_t_sch.addItems(t_sch_list)

            if self.cB_pn.currentText() in ['10', '16', '25']:
                self.cB_t_sch.setCurrentText(t_sch_dict[self.cB_pn.currentText()])
            else:
                self.cB_t_sch.setCurrentIndex(-1)

        elif self.cB_t_std.currentText() == 'GB12459/GBT13401<AB系列>':
            self.cB_t_sch.clear()
            t_sch_list = ['Sch5s','Sch10s','Sch20s','LG','Sch20','Sch30','STD','Sch40',
                          'Sch60','XS','Sch80','Sch100','Sch120','Sch140','Sch160']
            self.cB_t_sch.addItems(t_sch_list)

        elif self.cB_t_std.currentText() == 'ANSI B36.10M、B36.19M<A>':
            self.cB_t_sch.clear()
            t_sch_list = ['Sch5s','Sch10s','Sch10','Sch20','Sch30','Sch40s','STD','Sch40',
                          'Sch60','Sch80s','XS','Sch80','Sch100','Sch120','Sch140','Sch160','XXS']
            self.cB_t_sch.addItems(t_sch_list)

        elif self.cB_t_std.currentText() == 'HG20533(Ia)系列':
            self.cB_t_sch.clear()
            t_sch_list = ['Sch5s','Sch10s','Sch10','Sch20','Sch30','Sch40s','Sch40',
                          'Sch60','Sch60s','Sch80','Sch100','Sch120','Sch140','Sch160']
            self.cB_t_sch.addItems(t_sch_list)

        try:
            self.cB_t_sch.setCurrentText(t111)
        except:
            self.cB_t_sch.setCurrentIndex(0)

    # def _clear_all_labels(self):
    #     """清除所有标签的值，确保不会显示上次的结果"""
    #     # WN标签
    #     self.lbs_wn_k.setText("-")
    #     self.lbs_wn_c.setText('-')
    #     self.lbs_wn_d.setText('-')
    #     self.lbs_wn_h.setText('-')
    #     self.lbs_wn_nl.setText('-')
    #     self.lbs_wn_NAB.setText('-')
    #     self.lbs_wn_A1AB.setText('-')
        
    #     # SO标签
    #     self.lbs_so_K.setText('-')
    #     self.lbs_so_C.setText('-')
    #     self.lbs_so_D.setText('-')
    #     self.lbs_so_H.setText('-')
    #     self.lbs_so_nl.setText('-')
    #     self.lbs_so_NAB.setText('-')
    #     self.lbs_so_B1_AB.setText('-')
        
    #     # SW标签
    #     self.lbs_sw_K.setText('-')
    #     self.lbs_sw_C.setText('-')
    #     self.lbs_sw_D.setText('-')
    #     self.lbs_sw_H.setText('-')
    #     self.lbs_sw_U.setText('-')
    #     self.lbs_sw_N.setText('-')
    #     self.lbs_sw_B2.setText('-')
    #     self.lbs_sw_nl.setText('-')
        
    #     # PL标签
    #     self.lbs_pl_K.setText('-')
    #     self.lbs_pl_C.setText('-')
    #     self.lbs_pl_D.setText('-')
    #     self.lbs_pl_N.setText('-')
    #     self.lbs_pl_nl.setText('-')
        
    #     # BL标签
    #     self.lbs_bl_K.setText('-')
    #     self.lbs_bl_C.setText('-')
    #     self.lbs_bl_D.setText('-')
    #     self.lbs_bl_nl.setText('-')
        
    #     # Th标签
    #     self.lbs_th_K.setText('-')
    #     self.lbs_th_C.setText('-')
    #     self.lbs_th_D.setText('-')
    #     self.lbs_th_A.setText('-')
    #     self.lbs_th_nl.setText('-')
        
    #     # PJ/RJ标签
    #     self.lbs_pjrj_K.setText('-')
    #     self.lbs_pjrj_C.setText('-')
    #     self.lbs_pjrj_D.setText('-')
    #     self.lbs_pjrj_H.setText('-')
    #     self.lbs_pjrj_B2.setText('-')
    #     self.lbs_pjrj_d.setText('-')
    #     self.lbs_pjrj_F.setText('-')
    #     self.lbs_pjrj_nl.setText('-')
        
    #     # IF标签
    #     self.lbs_if_K.setText("-")
    #     self.lbs_if_C.setText('-')
    #     self.lbs_if_D.setText('-')
    #     self.lbs_if_Smin.setText('-')
    #     self.lbs_if_nl.setText('-')
    #     self.lbs_if_N.setText('-')
        
    #     # LWN标签
    #     self.lbs_lwn_K.setText('-')
    #     self.lbs_lwn_C.setText('-')
    #     self.lbs_lwn_D.setText('-')
    #     self.lbs_lwn_H.setText('-')
    #     self.lbs_lwn_nl.setText('-')
    #     self.lbs_lwn_N.setText('-')
        
    #     # A/B WN标签
    #     self.lbs_awn_K.setText('-')
    #     self.lbs_awn_C.setText('-')
    #     self.lbs_awn_D.setText('-')
    #     self.lbs_awn_nl.setText('-')
    #     self.lbs_awn_A.setText('-')
    #     self.lbs_awn_H.setText('-')
    #     self.lbs_awn_N.setText('-')
    #     self.lbs_awn_B.setText('-')
        
    #     # A/B BL标签
    #     self.lbs_abl_K.setText('-')
    #     self.lbs_abl_C.setText('-')
    #     self.lbs_abl_D.setText('-')
    #     self.lbs_abl_nl.setText('-')
        
    #     # NBT标签
    #     self.lbs_nbt_D.setText('-')
    #     self.lbs_nbt_d.setText('-')
    #     self.lbs_nbt_h.setText('-')
    #     self.lbs_nbt_DN.setText('-')
    #     self.lbs_nbt_D1.setText('-')
    #     self.lbs_nbt_dta0.setText('-')
    #     self.lbs_nbt_dta1.setText('-')
    #     self.lbs_nbt_dta2.setText('-')
    #     self.lbs_nbt_Th.setText('-')
        
    #     # 密封面标签
    #     self.lbs_mfm.setText('-')
        
    #     # 螺栓标签
    #     self.lbth_rf_lsr.setText('突面<六角头螺栓>/ 长度 -')
    #     self.lbth_rf_lzr.setText('突面<全螺纹/双头螺柱>/ 长度 -')
    #     self.lbth_mfm_lzm.setText('凹凸面<全螺纹/双头螺柱>/ 长度 -')
    #     self.lbth_rj_lzj.setText('环连接面<全螺纹/双头螺柱>/ 长度 -')

    def buid_t(self):
        df = None
        if self.cB_t_std.currentText() == 'HGJ514<无缝管><B>_供参考':
            path = str(pth.cwd()) + "\\Data\\HGJ514无缝管.csv"

            df = pd.read_csv(path, dtype={'DN': "str", 'DN2': "str"})
            try:
                if self.cB_std.currentText() == 'HGT20592<PN系列>':
                    df2 = df[(df["DN"] == self.cB_dn.currentText())]

                elif self.cB_std.currentText() == 'HGT20615<class系列>' \
                        or self.cB_std.currentText() == 'HGT20623<大直径>':
                    df2 = df[(df["DN2"] == self.cB_dn.currentText())]

                self.lbt_d.setText('(' + str(df2.iloc[0].at['D_o']) + ')')
                self.lbt_t.setText(str(df2.iloc[0].at[self.cB_t_sch.currentText()]))

            except:
                self.lbt_d.setText('(-)')
                self.lbt_t.setText('-')

        elif self.cB_t_std.currentText() == 'HGJ528Ⅱ系列<有缝管><B>_供参考':
            path = str(pth.cwd())+ "\\Data\\HGJ528_2有缝管.csv"

            df = pd.read_csv(path, dtype={'DN': "str", 'DN2': "str"})

            try:
                if self.cB_std.currentText() == 'HGT20592<PN系列>':
                    df2 = df[(df["DN"] == self.cB_dn.currentText())]

                elif self.cB_std.currentText() == 'HGT20615<class系列>' \
                        or self.cB_std.currentText() == 'HGT20623<大直径>':
                    df2 = df[(df["DN2"] == self.cB_dn.currentText())]

                self.lbt_csss_d.setText('(' + str(df2.iloc[0].at['D_o']) + ')')
                self.lbt_cst.setText('碳钢:' + str(df2.iloc[0].at[self.cB_t_sch.currentText() + '_CS']))
                self.lbt_sst.setText('不锈钢:' + str(df2.iloc[0].at[self.cB_t_sch.currentText() + '_SS']))

            except:
                self.lbt_csss_d.setText('(-)')
                self.lbt_cst.setText('-')
                self.lbt_sst.setText('-')

        elif self.cB_t_std.currentText() == 'GB12459/GBT13401<AB系列>':
            path = str(pth.cwd())+ "\\Data\\GB12459_GBT13401.csv"

            df = pd.read_csv(path, dtype={'DN': "str", 'DN2': "str"})

            try:
                if self.cB_std.currentText() == 'HGT20592<PN系列>':
                    df2 = df[(df["DN"] == self.cB_dn.currentText())]

                elif self.cB_std.currentText() == 'HGT20615<class系列>' \
                        or self.cB_std.currentText() == 'HGT20623<大直径>':
                    df2 = df[(df["DN2"] == self.cB_dn.currentText())]

                dab = str(df2.iloc[0].at['D_o_A']) + "(" + str(df2.iloc[0].at['D_o_B']) + ")"
                self.lbt_dab.setText(dab)
                self.lbt_dab_t.setText(str(df2.iloc[0].at[self.cB_t_sch.currentText()]))

            except:
                self.lbt_dab.setText('-')
                self.lbt_dab_t.setText('-')

        elif self.cB_t_std.currentText() == 'ANSI B36.10M、B36.19M<A>':
            path = str(pth.cwd())+ "\\Data\\ANSIB36.10M_B36.19M.csv"

            df = pd.read_csv(path, dtype={'DN': "str", 'DN2': "str"})

            try:
                if self.cB_std.currentText() == 'HGT20592<PN系列>':
                    df2 = df[(df["DN"] == self.cB_dn.currentText())]

                elif self.cB_std.currentText() == 'HGT20615<class系列>' \
                        or self.cB_std.currentText() == 'HGT20623<大直径>':
                    df2 = df[(df["DN2"] == self.cB_dn.currentText())]

                self.lbt_d.setText(str(df2.iloc[0].at['D_o']))
                self.lbt_t.setText(str(df2.iloc[0].at[self.cB_t_sch.currentText()]))

            except:
                self.lbt_d.setText('-')
                self.lbt_t.setText('-')

        elif self.cB_t_std.currentText() == 'HG20533(Ia)系列':
            path = str(pth.cwd())+ "\\Data\\HG20553(Ia)系列.csv"

            df = pd.read_csv(path, dtype={'DN': "str", 'DN2': "str"})
            pass
            try:
                if self.cB_std.currentText() == 'HGT20592<PN系列>':
                    df2 = df[(df["DN"] == self.cB_dn.currentText())]

                elif self.cB_std.currentText() == 'HGT20615<class系列>' \
                        or self.cB_std.currentText() == 'HGT20623<大直径>':
                    df2 = df[(df["DN2"] == self.cB_dn.currentText())]

                self.lbt_d.setText(str(df2.iloc[0].at['D_o']))
                self.lbt_t.setText(str(df2.iloc[0].at[self.cB_t_sch.currentText()]))

            except:
                self.lbt_d.setText('-')
                self.lbt_t.setText('-')

    def choose_t(self):
        if self.cB_t_std.currentText() == 'HGJ514<无缝管><B>_供参考':
            self.tW_t.setCurrentIndex(0)
        elif self.cB_t_std.currentText() == 'HGJ528Ⅱ系列<有缝管><B>_供参考':
            self.tW_t.setCurrentIndex(2)
        elif self.cB_t_std.currentText() == 'GB12459/GBT13401<AB系列>':
            self.tW_t.setCurrentIndex(1)
        elif self.cB_t_std.currentText() == 'ANSI B36.10M、B36.19M<A>'\
                or self.cB_t_std.currentText() == 'HG20533(Ia)系列':
            self.tW_t.setCurrentIndex(0)


def check_license():
    """
    检查许可证状态
    
    Returns:
        bool or dict: False表示许可证无效，dict表示许可证有效并包含详细信息
    """
    storage_file = "license.dat"
    key_file = "license.key"
    
    # 检查许可证文件是否存在
    if not os.path.exists(storage_file) or not os.path.exists(key_file):
        return False
    
    try:
        # 获取本机机器码用于验证
        local_machine_code = get_machine_code()
        
        # 加载加密密钥
        with open(key_file, "rb") as f:
            key = f.read()
        cipher = Fernet(key)
        
        # 从文件读取加密数据
        with open(storage_file, "rb") as f:
            encrypted_data = f.read()
        
        # 解密数据
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # 将JSON字符串转换为字典
        registration_info = json.loads(decrypted_data.decode('utf-8'))
        
        # 检查机器码是否匹配
        stored_machine_code = registration_info.get('machine_code')
        if stored_machine_code != local_machine_code:
            return False
        
        # 检查是否过期
        expiry_date_str = registration_info.get('expiry_date')
        if not expiry_date_str:
            return False
        
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
        current_date = datetime.now()
        
        # 如果已过期，返回False
        if current_date > expiry_date:
            return False
        
        # 返回到期日期信息
        remaining_days = (expiry_date - current_date).days
        return {
            'valid': True,
            'expiry_date': expiry_date_str,
            'remaining_days': remaining_days
        }
        
    except Exception as e:
        # 解密或解析失败，许可证无效
        return False


def show_license_validator():
    """
    显示许可证验证GUI
    """
    try:
        # 导入并运行许可证验证器
        from registration_key_validator import main as validator_main
        validator_main()
        return True  # 表示验证界面已显示
    except ImportError:
        print("无法加载许可证验证器GUI")
        print("请确保registration_key_validator.py文件存在")
        return False
    except Exception as e:
        print(f"启动许可证验证器时出错: {str(e)}")
        return False


def check_and_run():
    """
    检查许可证并运行应用程序
    """
    # 首先检查许可证
    license_result = check_license()
    
    # 导入必要的Qt模块
    import sys
    from PyQt5.QtWidgets import QApplication, QMessageBox
    
    # 确保只有一个QApplication实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    while True:  # 循环直到用户选择退出或成功启动
        if not license_result:
            # 许可证无效或已过期
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("许可证验证")
            msg_box.setText("许可证无效或已过期")
            msg_box.setInformativeText("点击确定打开许可证验证界面")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.setDefaultButton(QMessageBox.Ok)
            
            ret = msg_box.exec_()
            if ret == QMessageBox.Ok:
                # 显示许可证验证GUI
                show_license_validator()
                # 验证界面关闭后，重新检查许可证状态
                license_result = check_license()
                if license_result:
                    # 如果现在许可证有效，显示成功信息
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setWindowTitle("许可证验证")
                    msg_box.setText("许可证激活成功")
                    msg_box.setInformativeText(f"到期时间: {license_result['expiry_date']} (剩余 {license_result['remaining_days']} 天)")
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()
                    # 成功激活后，跳出循环，准备启动主程序
                    break
                else:
                    # 许可证仍然无效，继续循环
                    continue
            else:
                # 用户选择取消，退出程序
                return False
        else:
            # 许可证有效
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("许可证验证")
            msg_box.setText("许可证有效")
            msg_box.setInformativeText(f"到期时间: {license_result['expiry_date']} (剩余 {license_result['remaining_days']} 天)")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setDefaultButton(QMessageBox.Ok)
            
            msg_box.exec_()
            # 许可证有效，跳出循环，准备启动主程序
            break
    
    # 如果到达这里，说明许可证已验证通过，可以启动主程序
    return True


if __name__ == "__main__":
    result = check_and_run()  # 检查许可证状态
    if result:  # 如果许可证检查通过，才启动应用程序
        import sys
        from PyQt5.QtWidgets import QApplication
        
        # 确保只有一个QApplication实例
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        myWin = FlangeWindow()  # 创建主窗口对象
        myWin.show()
        sys.exit(app.exec_())
