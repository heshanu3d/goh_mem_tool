import struct, sys, os, keyboard, re, time, yaml, signal

def read_uint32_from_file(file_path, offset):
    with open(file_path, 'rb') as file:
        file.seek(offset)
        data = file.read(4)  # Read 4 bytes for uint64_t
        value = struct.unpack('I', data)[0]  # 'I' is for unsigned int (uint32_t)
        return value
def read_uint64_from_file(file_path, offset):
    with open(file_path, 'rb') as file:
        file.seek(offset)
        data = file.read(8)  # Read 8 bytes for uint64_t
        value = struct.unpack('Q', data)[0]  # 'Q' is for unsigned long long (uint64_t)
        return value

def find_start(file_path):
    idx_start = file_path.find('-') + 1
    idx_end = file_path.rfind('-')
    return int(file_path[idx_start:idx_end], 16)

def find_bin_files(directory):
    bin_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.bin'):
            bin_files.append(filename)
    return bin_files    

def load_code():
    # 打开并读取 YAML 文件
    with open('code.yaml', 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    #for k, v in data.items():
        #print(k, v)
    return data

def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == "__main__":    
    args = sys.argv
    if len(args) != 2:
        print('please run :')
        print('python mem_searcher.py 76CEF78704')
        print('Or')
        print('python mem_searcher.py 76CEF78A24')
        print('请注意: 地址跟物品栏序号关联')
        exit(1)

    code =load_code()
    signal.signal(signal.SIGINT, signal_handler)

    file_path = '' # 'com.goplaytoday.guildofheroes-76ce074000-76cf074000.bin'
    bin_files = find_bin_files('.')
    if len(bin_files) == 0:
        print('could not find binary for search')
        exit(1)
    elif len(bin_files) > 1:
        for i, bin_file in enumerate(bin_files):
            print(i, bin_file)
        while True:
            try:
                user_input = input("请输入对应数字来指定搜索的binary文件: ")
                number = int(user_input)
                print(f'你选择的binary文件是: {bin_files[number]}')
                file_path = bin_files[number]
                break
            except ValueError:
                print("输入的不是有效的数字，请输入一个整数。")
    else:
        file_path = bin_files[0]
    
    start = find_start(file_path)
    print(f'{hex(start)}')
    offset = int(args[-1], 16) - start
    print(f'{hex(offset)}')
    
    seq = read_uint32_from_file(file_path, offset)
    print(f'seq at addr {offset + start}: {seq:#010d}')  # Print in decimal format
    print(f'seq at addr {offset + start}: {seq:#010x}')  # Print in hex format
    
    try_cnt = 0
    _seq = seq
    _offset = offset
    while try_cnt < 1000 and _seq != 1:
        _offset -= 0xA0
        _seq = read_uint32_from_file(file_path, _offset)
        try_cnt += 1
    
    seq_init_flag = True
    if (seq != 1 and try_cnt > 1000) or try_cnt-seq > 1:
        print('find seq = 1 failed')
        seq_init_flag = False
    else:
        seq = _seq
        offset = _offset
        print(f'find seq = 1 success, ofs: {offset:#6x}, addr: {offset+start:#12x}, try_cnt: {try_cnt}')
    
    def read_gamedata(seq_addr_relative):
        seq  = read_uint32_from_file(file_path, seq_addr_relative)
        cnt  = read_uint32_from_file(file_path, seq_addr_relative + 4)
        type = read_uint32_from_file(file_path, seq_addr_relative + 104)
        return seq, cnt, type

    def interact():
        print('进入交互模式:')
        print('    h/help : 帮助')
        print('    rd/read: 读取指定地址')
        print('    q: 退出')
        while True:
            print('#interact> ', end='')
            user_input = input()
            user_input = user_input.strip()
            if user_input == 'q':
                return
            elif user_input == 'help' or user_input == 'h':
                print('rd 7c8f')
                print('read 7c8f')
            elif bool(re.match('^\s*(rd|read)\s+[0-9A-Fa-f]+\s*$', user_input)):
                res = re.findall('^\s*(rd|read)\s+([0-9A-Fa-f]+)\s*$', user_input)
                if len(res) > 0:
                    res = res[0]
                    abs_addr = res[1]
                    # 高位补全
                    if len(abs_addr) < len(args[1]):
                        abs_addr_len = len(abs_addr)
                        abs_addr = args[1][0:len(args[1]) - abs_addr_len] + abs_addr
                        abs_addr = int(abs_addr, 16)
                    else:
                        abs_addr = int(abs_addr, 16)
                    v = read_uint32_from_file(file_path, abs_addr-start)
                    print(f'addr {abs_addr:#10x}, val {v:#10x}   {v:#10d}')
            elif user_input == '':
                pass
            else:
                print('input error!')

    def PrintFunc(s, c, t, ofs, show=True):
        def calculate_cn_length(s):
            length = 0
            for char in s:
                # 判断字符是否为中文
                if '\u4e00' <= char <= '\u9fff':
                    length += 1
                #else:
                #    length += 1
            return length

        info = 'unknown'
        if t in code.keys():
            info = code[t]
        if show:
            print(f'seq = {s:#11d}, cnt = {c:#11d}, type = {t:#11d}, info:{info:<{16-calculate_cn_length(info)}s}, addr: {ofs+start:#12x}')
        return f'seq = {s:#11d}, cnt = {c:#11d}, type = {t:#11d}, info:{info:<{16-calculate_cn_length(info)}s}, addr: {ofs+start:#12x}'
        
    def fastmode():
        print('进入快速模式:')
        print('    n : 向后查找')
        print('    p : 向前查找')
        print('    q : 退出')
        s, c, t = read_gamedata(offset)
        PrintFunc(s, c, t, offset)

        _offset = offset
        while True:
            if keyboard.is_pressed('n'):
                _offset += 0xA0
                s, c, t = read_gamedata(_offset)
                PrintFunc(s, c, t, _offset)
            elif keyboard.is_pressed('p'):
                _offset -= 0xA0
                s, c, t = read_gamedata(_offset)
                PrintFunc(s, c, t, _offset)
            elif keyboard.is_pressed('q'):
                break
            else:
                pass
            time.sleep(0.01)
    def search(user_input, forwards=True):
        print_list = []
    #while True:
        #user_input = input()
        #user_input = user_input.strip()
        if user_input == 'q':
            return
        if user_input == 'help' or user_input == 'h':
            if forwards:
                print('单条件查找:')
                print('    seq=2:  查找seq=2的条目')
                print('    cnt=3:  查找cnt=2的条目')
                print('    type=3: 查找type=2的条目')
                print('多重条件查找:')
                print('    type=3 if seq=2: seq=2且type=2的条目')
                print('    cnt=2 if type>1000: cnt=2且type>1000的条目')
                print('    seq<1000 if info!=unknown: seq<1000且info已知的条目')
        elif   bool(re.match('^\s*(seq|cnt|type)([<=>!]+)([0-9]+)\s*(if\s+(seq|cnt|type|info)([<=>!]+)([\d\w\u4e00-\u9fa5\-_]+))*$', user_input)):
            res = re.findall('^\s*(seq|cnt|type)([<=>!]+)([0-9]+)\s*(if\s+(seq|cnt|type|info)([<=>!]+)([\d\w\u4e00-\u9fa5\-_]+))*$', user_input)
            if len(res) > 0:
                condition = False
                res = res[0]
                # print(res)
                # now ,after res = res[0], res will be
                #('seq', '2')
                #('seq', '2', 'if type=2', 'type', '=', '2')
                #     0,   1,           2,      3,   4,   5
                action = res[0]
                operations = { '<': lambda x, y: x < y, '=': lambda x, y: x == y, '>': lambda x, y: x > y, '!=': lambda x,y : x != y}
                cmp_1  = res[1]
                val = int(res[2])
                if res[3] != '':
                    condition = True
                _offset = offset
                if action == 'seq':
                    ofs = 0
                elif action == 'cnt':
                    ofs = 4
                elif action == 'type':
                    ofs = 104
                while True:
                    try:
                        v = read_uint32_from_file(file_path, _offset + ofs)
                        if operations[cmp_1](v, val):
                            s, c, t = read_gamedata(_offset)
                            if condition:
                                cond = {'seq':s, 'cnt':c, 'type':t, 'info':code[t] if t in code.keys() else 'unknown'}
                                cmp_2 = res[5]
                                if res[4] == 'info':
                                    cond_v = res[6]
                                else:
                                    cond_v = int(res[6])
                                out = False
                                if operations[cmp_2](cond[res[4]], cond_v):
                                    print_list.append(PrintFunc(s, c, t, _offset, True if forwards else False))
                            else:
                                print_list.append(PrintFunc(s, c, t, _offset, True if forwards else False))
                        if forwards:
                            _offset += 0xA0
                        else:
                            _offset -= 0xA0
                    except Exception as e:
                        if forwards:
                            print('search end')
                        break
                if not forwards:
                    while len(print_list) > 0:
                        print(print_list.pop())
        elif user_input == '':
            pass
        else:
            print('input error!')
    def searchmode():
        print('进入查找模式:')
        print('    h/help : 帮助')
        print('    seq=2:  查找seq=2的条目')
        print('    cnt=3:  查找cnt=2的条目')
        print('    type=3: 查找type=2的条目')
        print('    q: 退出')
        while True:
            print('#search> ', end='')
            user_input = input()
            user_input = user_input.strip()
            search(user_input, False)
            search(user_input)
            if user_input == 'q':
                return
    def dumpmode():
        print('dumping...')
        print('    h/help : 帮助')
        print('    q: 退出')
        while True:
            print('#dump> ', end='')
            user_input = input()
            user_input = user_input.strip()
            if user_input == 'q':
                return
            elif user_input == 'help' or user_input == 'h':
                print('not ready yet')
            elif user_input == '':
                pass
    tips = True
    while True:
        if tips:
            print('请选择模式:')
            print('    i:  交互模式')
            print('    f:  快速模式')
            print('    d:  dump模式')
            print('    s:  查找模式')
            print('    q:  退出')
        else:
            tips = True
        print('#root> select mode and enter: ', end='')
        user_input = input()
        user_input = user_input.strip()
        if user_input == 'q':
            exit(0)
        elif user_input == 'i':
            interact()
        elif user_input == 'f':
            fastmode()
        elif user_input == 'd':
            dumpmode()
        elif user_input == 's':
            searchmode()
        else:
            tips = False