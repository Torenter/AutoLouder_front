import os
def get_translators():
    file_t = open('{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)),'translators.txt','r'))
    file_d = ''.join(file_t)
    file_t.close()
    file_d = file_d.split('\n')
    file_s = {}
    for _ in file_d:
        if _ != '':
            file_s[_]=1
    return file_s
if __name__ == "__main__":
    print("Должен быть импортирован")