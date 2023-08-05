import argparse
import os
import re
from pathlib import Path


class Finder(object):

    def __init__(self, dir_path, kw, name_only, is_re, return_container, rmf=None, rml=None, qr=None, rt=None,
                 full_match=False):
        self.path = dir_path
        self.sep = "<<<***0...>>>"
        self.kw = kw
        self.kw_re = re.compile(fr"{kw}")
        self.name_only = name_only
        self.is_re = is_re
        self.full_match = full_match
        self.rmf = rmf
        self.rml = rml
        self.qr = qr
        self.rt_switch = True if rt is not None else False
        self.rt = rt if rt is not None else ''
        self.return_container = return_container

    def start(self):
        f_lis = []
        for root, sub_dir, file_names in os.walk(self.path):
            f_lis += [os.path.join(root, file_name) for file_name in file_names]
        container = self.get_container(f_lis) if not self.is_re else self.get_container_re(f_lis)
        if self.return_container:
            return container
        ft = " >>> "
        for match, type_line_id in container.items():
            type_str = 'file content'
            if isinstance(type_line_id, str):
                if not self.is_re:
                    match_str = match.replace(self.kw, f"\033[0;31;48m{self.kw}\033[0m")
                else:
                    match_str = re.sub(fr'(?P<kw>{self.kw})', self.make_re_color, match)
                if f'{self.sep}dir_name' in type_line_id:
                    type_str = 'folder'
                if f'{self.sep}file_name' in type_line_id:
                    type_str = 'file name'
                print(f"{ft}[ {type_str} ] [ {match_str} ]")
            else:
                lines_set = set()
                del_lines = list()
                print(f"in file [ {match} ]: ")
                for line in type_line_id:
                    line_no, line_str = line.split(self.sep)
                    if line not in lines_set:
                        lines_set.add(line)
                        if not self.is_re:
                            line_str = line_str.replace(self.kw, f"\033[0;31;48m{self.kw}\033[0m")
                        else:
                            line_str = re.sub(fr'(?P<kw>{self.kw})', self.make_re_color, line_str)
                        print(f"{ft}[ {line_no} ] [ {line_str} ]")
                    if self.rml or self.rt_switch:
                        if not self.qr:
                            is_rm = True if 'y' in input("change this line? ").lower() else False
                            if is_rm:
                                del_lines.append(line)
                        else:
                            del_lines.append(line)
                self.delete_lines(match, del_lines)
                print()
            if self.rmf:
                mp = Path(match)
                if not self.qr:
                    is_rm = True if 'y' in input("remove the above files? ").lower() else False
                    if is_rm:
                        mp.rmdir() if mp.is_dir() else os.remove(str(mp.absolute()))
                        print(f'file: \033[0;31;48m"{match}" ✘\033[0m')
                else:
                    mp.rmdir() if mp.is_dir() else os.remove(str(mp.absolute()))
                    print(f'file: \033[0;31;48m"{match}" ✘\033[0m')

    def delete_lines(self, match, dl_lines):
        dl_lines = [x.split(self.sep) for x in dl_lines]
        line_no = {int(x[0]) for x in dl_lines if x[0] and isinstance(x[0], str) and x[0].isdigit()}
        dlp = Path(match)
        raw_lines = dlp.read_text()
        # new_file = re.sub(self.kw, self.rt, raw_lines)

        raw_lines = raw_lines.split("\n")
        new_lines = []
        rpl_lines = []
        for num, rl in enumerate(raw_lines, 1):
            if num not in line_no:
                new_lines.append(rl)
            else:
                rpl = re.sub(self.kw, self.rt, rl) if self.is_re else rl.replace(self.kw, self.rt)
                rpl_lines.append([num, rl, rpl])
                new_lines.append(rpl)
        new_file = "\n".join(new_lines)

        dlp.write_text(new_file, encoding="utf-8")
        for ln, l_str, lp_str in rpl_lines:
            print(f'line [ \033[0;31;48m{ln}\033[0m ]: \033[1;31;48m"{l_str}" ✘\033[0m')
            print("replace to")
            print(f'line [ \033[0;32;48m{ln}\033[0m ]: \033[1;32;48m"{lp_str}" ✔\033[0m')
            print()

    @staticmethod
    def make_re_color(matched):
        res = f"\033[0;31;48m{matched.group('kw')}\033[0m"
        return res

    def get_container(self, lis):
        container = dict()
        for f in lis:
            if self.name_only:
                fs = f.split(os.sep)
                fsn = [os.sep.join(fs[:-1]), fs[-1]]
                if self.kw in fsn[0]:
                    container[fsn[0]] = f'{self.sep}dir_name'
                if self.kw in fsn[1]:
                    container[os.sep.join(fsn)] = f'{self.sep}file_name'
            else:
                try:
                    with open(f, 'r') as rf:
                        lines = rf.readlines()
                    lines_with_kw = []
                    line_count = 0
                    for line in lines:
                        line_count += 1
                        if self.kw in line:
                            l_str = f'{line_count}{self.sep}{line.strip()}'
                            lines_with_kw.append(l_str)
                    # lines_with_kw = [f'{lines.index(x)+1}{self.sep}{x.strip()}' for x in lines if self.kw in x]
                    if lines_with_kw:
                        container[f] = lines_with_kw
                except Exception as E:
                    pass
        return container

    def get_container_file_name_only(self):
        container = dict()
        cmd = f"find {self.path} -name '{self.kw}' "

    def look_for_line_no(self, file, line):
        no_lis = []
        for num, li in enumerate(file.split('\n'), start=1):
            if line.strip().strip('\n') in li:
                no_lis.append(num)
        return no_lis

    def get_container_re(self, lis):
        container = dict()
        for f in lis:
            if self.name_only:
                if self.sep in f:
                    f = f.replace(self.sep, ''.join([f"\\{x}" for x in self.sep]))
                fs = f.split(os.sep)
                fsn = [os.sep.join(fs[:-1]), fs[-1]]
                if re.findall(self.kw, fsn[0]):
                    container[fsn[0]] = f'{self.sep}dir_name'
                if re.findall(self.kw, fsn[1]):
                    container[os.sep.join(fsn)] = f'{self.sep}file_name'
            else:
                try:
                    if self.full_match:
                        with open(f, 'r') as rfa:
                            file = rfa.read()
                        if self.sep in file:
                            file = file.replace(self.sep, ''.join([f"\\{x}" for x in self.sep]))
                        file_with_kw = re.findall(self.kw_re, file)
                        if file_with_kw:
                            for line in file_with_kw:
                                li_nos = self.look_for_line_no(file, line)
                                for num in li_nos:
                                    container[f] = f"{num}{self.sep}{line}"
                    else:
                        with open(f, 'r') as rf:
                            lines = rf.readlines()
                        lines = [x.replace(self.sep, ''.join([f"\\{x}" for x in self.sep])) if self.sep in x else x for
                                 x in lines]
                        lines_with_kw = [f'{lines.index(x) + 1}{self.sep}{x.strip()}' for x in lines if
                                         re.findall(self.kw, x)]
                        if lines_with_kw:
                            container[f] = lines_with_kw
                except Exception as E:
                    pass
        return container


def find():
    dp = ' *** 这是一个在文件夹下所有的地方查找关键字的工具，支持正则表达式'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("keyword", type=str, default='', help=f'{da}要查找的关键字，必须值')
    parser.add_argument("-f", "--folder", type=str, dest="folder", default='', help=f'{da}需要查找的文件夹，默认运行目录')
    parser.add_argument("-r", "--re_mode", type=str, dest="re_mode", nargs='?', default='n',
                        help=f'{da}y/n 是否以正则方式查找，默认n')
    parser.add_argument("-fm", "--full_match", type=str, dest="full_match", nargs='?', default='n',
                        help=f'{da}y/n 是否全匹配，默认n')
    parser.add_argument("-o", "--filename_only", type=str, dest="filename_only", nargs='?', default='n',
                        help=f'{da}y/n 是否只查找文件夹名和文件名，默认n')
    parser.add_argument("-rmf", "--remove_file", type=str, dest="remove_file", nargs='?', default='n',
                        help=f'{da}y/n 是否删除找到的文件，默认n')
    parser.add_argument("-rml", "--remove_line", type=str, dest="remove_line", nargs='?', default='n',
                        help=f'{da}y/n 是否删除找到的行，默认n')
    parser.add_argument("-qr", "--quietly_remove", type=str, dest="quietly_remove", nargs='?', default='n',
                        help=f'{da}y/n 是否不经确认直接删除，默认n')
    parser.add_argument("-rt", "--replace_to", type=str, dest="replace_to", default=None,
                        help=f'{da}替换，支持 python re.sub 的操作')
    args = parser.parse_args()

    keyword = args.keyword
    folder = args.folder
    re_mode = args.re_mode
    full_match = args.full_match
    remove_file = args.remove_file
    remove_line = args.remove_line
    quietly_remove = args.quietly_remove
    filename_only = args.filename_only
    replace_to = args.replace_to
    remove_file = True if remove_file is None or remove_file.lower() == 'y' else False
    remove_line = True if remove_line is None or remove_line.lower() == 'y' else False
    quietly_remove = True if quietly_remove is None or quietly_remove.lower() == 'y' else False
    re_mode = True if re_mode is None or re_mode.lower() == 'y' else False
    full_match = True if full_match is None or full_match.lower() == 'y' else False
    filename_only = True if filename_only is None or filename_only.lower() == 'y' else False
    replace_to = replace_to if replace_to is not None and replace_to != 'None' else None

    kw = keyword
    if not kw:
        raise ValueError('关键字是必须的: findkw "xxx"')

    if not folder:
        folder = os.getcwd()

    fd = Finder(folder, kw, filename_only, re_mode, False, remove_file, remove_line, quietly_remove, replace_to,
                full_match)
    fd.start()


if __name__ == '__main__':
    fdr = Finder(
        "/home/ga/Guardian/For-Longqi/tunnel_test_spider/tunnel_test_spider/",
        "OH_NO_REDIS.*?(\{[^\}]+\})",
        False, True, True, False, False, False, None, full_match=True
    )
    print(fdr.start())
