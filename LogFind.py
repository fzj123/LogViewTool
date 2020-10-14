import mmap
import contextlib
import re


def logFind(file_path, search_word):
    list_all = []
    list_contents = []
    f = open(file_path, 'r')
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        while True:
            line = m.readline().strip()
            if line.find(search_word.encode()) >= 0:
                list_line = re.split(r'(?:[\|\[\]])', line.decode())
                #list_line = re.split(r'(?:[\[*\]])', line.decode())
                print("结果：%s" % (line.decode()))
                list_one = list(filter(None, list_line))
                print(list_one)
                list_all.append(list_one)
            elif m.tell() == m.size():
                break
            else:
                pass
        print(list_all)

        for i in list_all:
            for j in list_all:
                if i[2] == j[2] and i[5] == 'THREAD_BEGIN' and j[5] == 'THREAD_END':
                   list_content = list(set(i).union(set(j)))                 
                   list_content_tmp = list(filter(lambda x: x =='THREAD_BEGIN' or x =='THREAD_END' or x =='null' or x == 'LogInfo:', list_content))
                   list_content = list(set(list_content).difference(set(list_content_tmp)))
                   list_content.sort() 
                   list_contents.append(list_content)

        print('内容统计：%s' %list_contents)

        # print(list(set(list_all[0]).union(set(list_all[1]))))

    return list_contents


    


if __name__ == '__main__':
    a = logFind('C:\\Users\\Administrator\\Downloads\\cre.log',
                '[/cre/updateFolderACLForShare]')
