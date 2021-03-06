#/usr/bin/env pyton
# -*- coding: utf-8 -*-
'''
#
# python cookbook 第二章 文件
# Writer：xin.change.the.world@gmail.com
# Date：2014-06-04
# github: https://github.com/xin-change-the-world/python-cookbook
#
'''
'''
2.1　读取文件 59
2.2　写入文件 62
2.3　搜索和替换文件中的文本 64
2.4　从文件中读取指定的行 65
2.5　计算文件的行数 66
2.6　处理文件中的每个词 68
2.7　随机输入/输出 70
2.8　更新随机存取文件 71
2.9　从zip文件中读取数据 73
2.10　处理字符串中的zip文件 74
2.11　将文件树归档到一个压缩的tar文件 76
2.12　将二进制数据发送到Windows的标准输出 77
2.13　使用C++的类iostream语法 78
2.14　回退输入文件到起点 80
2.15　用类文件对象适配真实文件对象 83
2.16　遍历目录树 84
2.17　在目录树中改变文件扩展名 85
2.18　从指定的搜索路径寻找文件 86
2.19　根据指定的搜索路径和模式寻找文件 87
2.20　在Python的搜索路径中寻找文件 88
2.21　动态地改变Python搜索路径 89
2.22　计算目录间的相对路径 91
2.23　跨平台地读取无缓存的字符 93
2.24　在Mac OS X平台上统计PDF文档的页数 94
2.25　在Windows平台上修改文件属性 95
2.26　从OpenOffice.org文档中提取文本 96
2.27　从微软Word文档中抽取文本 97
2.28　使用跨平台的文件锁 98
2.29　带版本号的文件名 100
2.30　计算CRC-64循环冗余码校验 102
'''
'''
2.0 引言
'''
input = open('data', 'r')
output = open('spam', 'w')
#open接受由斜线字符（/）分隔开的目录和文件名构成的文件路径，而不管操作系统本身的倾向
'''
2.1 读取文件
'''
#最方便的方法是一次性读取文件中的所有内容并放置到一个大字符串中
all_the_text = open('thefile.txt').read()#文本文件中的所有文本
all_the_data = open('abinfile','rb').read()#二进制文件中的所有数据
#为安全起见，最好给打开的文件对象指定一个名字，这样在完成操作后，可以迅速关闭文件，
#防止一些无用的文件对象占用内存
file_object = open('thefile.txt')
try:
    all_the_text = file_object.read()
finally:
    file_object.close()
#注意不要把open也放到try里面去，因为如果open的时候出错了，那么就没有什么东西绑定到
#file_object对象上，在finally里，也就没有file_object需要关闭
#不一定非要用try/finally，但是用了效果更好，因为它可以保证文件对象被关闭，即使在读取中发生了严重错误
'''
#最简单、最快，也最具Python风格的方法是逐行读取文本文件内容，并将读取的数据放置到一个字符串列表中：
list_of_all_the_lines = file_object.readlines()
#这样读出的每行文本末尾都带有“\n”符号，如果不想这样，还可以这样写：
list_of_all_the_lines = file_object.read().splitlines()
list_of_all_the_lines = file_object.read().split('\n')
list_of_all_the_lines = [L.rstrip('\n') for L in file_object]
'''
#最简单最快的逐行处理文本文件的方法是，用一个简单的for循环语句:
'''
for line in file_object:
    process line
#这样会在每行末尾留下“\n”，可以这样：
for line in file_object:
    line = line.rstrip('\n')
    process line
#或者你想去除每行末尾的空白符（不只是“\n”）
line = line.rstrip()
'''
#如果不确定文本文件会用什么样的换行符，可以讲open的第二个参数设定为'rU'指定通用换行符转化
#无论什么平台，各种换行符都被映射成'\n'
#如果选择一次读取文件的一小部分，而不是全部，方式就有点不同了。
#下面例子，一次读取一个二进制文件的100个字节，一直读到文件末尾
file_object = open('abinfile', 'rb')
try:
    while True:
        chunk = file_object.read(100)
        if not chunk:
            break
        #do_something_with(chunk)
finally:
    file_object.close()
#给read方法传入一个参数N，确保了read方法只读取下N个字节，或更少（接近文件末尾）
#当到达文件末尾时，返回空字符串。
#复杂的循环最好被封装成可复用的生成器（generator）
#对于这个例子我们只能将其逻辑的一部分进行封装，因为yield关键字不被允许出现在
#try/finally语句的try子句中。如果要抛弃try/finall语句对文件关闭的保护，可以这样：
def read_file_by_chunks(filename, chunksize=100):
    file_object = open(filename, 'rb')
    while True:
        chunk = file_object.read(chunksize)
        if not chunk:
            break
        yield chunk#返回chunk，函数中断执行
    file_object.close()
'''
for chunk in read_file_by_chunks('abinfile'):
    do_something_with(chunk)
'''
#逐行读取文本文件的任务更常见。只需对文件应用循环语句
'''
for line in open('thefile.txt', 'rU')
    do_something_with(line)
'''
#为了100%确保完成操作之后没有无用的已打开的文件对象存在，可以将上述代码修改得更加严密稳固：
def do_something_with(s):
    print s
file_object = open('thefile.txt','rU')
try:
    for line in file_object:
        do_something_with(line)
finally:
    file_object.close()
'''
2.2 写入文件
'''
#最简单的写入
all_the_text = "this is all the text"
open('thefile.txt', 'w').write(all_the_text)#写入文本到文本文件
open('abinfile', 'wb').write(all_the_data)  #写入数据到二进制文件
#不过最好还是给文件对象指定一个名字，这样在操作完成后就可以调用close关闭了
file_object = open('thefile.txt', 'w')
file_object.write(all_the_text)
file_object.close()
#可是很多时候，想写入的数据不是在一个大字符串中，而是在一个字符串列表（或其他序列中）
#为此，应该使用writelines方法（并不局限于行写入，而且二进制文件和文本文件都适用）
list_of_text_strings = ['a','b','c']
#file_object.writelines(list_of_text_strings)
#open('abinfile','wb').writelines(list_of_text_data)#二进制文件写入
#当然也可以把子串拼接成大字符串（比如调用''.join）再调用write写入
#或者在循环中写入，但直接调用writelines要比上面两种方式快得多
#'w'允许写入，'wb'允许写入二进制文件（原文件清空），'a'或'ab'是追加，'r+b'同时读和写
#只有文件被正确关闭之后，才能确信数据被写入了磁盘，而不是暂存于内存中的临时缓存中
'''
2.3 搜索和替换文件中的文本
'''
#需要将文件中的某个字符串改变成另一个
#字符串对象的replace方法提供了字符串替换的最简单的办法
#下面的代码支持从一个特定的文件（或标准输入）读取数据，然后写入一个指定的文件（或标准输出）
import os, sys
nargs = len(sys.argv)
if not 3 <= nargs <=5:
    print "usage: %s search_text replace_text [infile [outfile]]" % \
          os.path.basename(sys.argv[0])
else:
    stext = sys.argv[1]
    rtext = sys.argv[2]
    input_file = sys.stdin
    output_file = sys.stdout
    if nargs > 3:
        input_file = open(sys.argv[3])
    if nargs > 4:
        output_file = open(sys.argv[4], 'w')
    for s in input_file:
        output_file.write(s.replace(stext, rtext))
    output.close()
    input.close()
#一句实现
#output_file.write(input_file.read().replace(stext, rtext))
'''
2.4 从文件中读取指定的行
'''
#python标准库linecache模块非常适合这个任务
import linecache
#theline = linecache.getline(thefilepath, desired_line_number)
#linecache读取并缓存你指定名字的文件中的所有文本，所以，如果文件非常大，
#而你只需要其中一行，为此，linecache则显得不是那么必要，如果这部分可能是你的瓶颈
#可以使用显式的循环，并将其封装在一个函数中，这样可以获得速度上的提升
def getline(thefilepath, desired_line_number):
    if desired_line_number < 1: return ''
    for current_line_number, line in enumerate(open(thefilepath, 'rU')):
        if current_line_number == desired_line_number - 1:return line
    return ''
'''
2.5 计算文件的行数
'''
#最简单的办法就是讲文件读取放入一个行列表中，计算列表长度
#count = len(open(thefilepath, 'rU').readlines())
#对于非常大的文件，这种方式会很慢，可以用循环计数
count = -1
for count, line in enumerate(open('thefile.txt', 'rU')):
    pass
count += 1
#如果行结束标记是“\n”或者含有“\n”(windows)，还可以：
count = 0
thefile = open("thefile.txt", 'rb')
while True:
    buffer = thefile.read(8192*1024)
    if not buffer:
        break
    count += buffer.count('\n')
thefile.close()
'''
2.6 处理文件中的每个词
'''
for line in open("thefile.txt"):
    for word in line.split():
        do_something_with(word)
#正则版
import re
re_word = re.compile(r"[\w'-]+")
for line in open("thefile.txt"):
    for word in re_word.finditer(line):
        do_something_with(word.group(0))
#这里词被定义为数字字母，连字符或单引号构成的序列
#通常把迭代封装成迭代器对象是个好主意，这种封装也很常见和易于使用
def words_of_file(thefilepath, line_to_words = str.split):
    the_file = open(thefilepath)
    for line in the_file:
        for word in line_to_words(line):
            yield word
    the_file.close()
for word in words_of_file("file.txt"):
    do_something_with(word)
'''
2.7 随机出入/输出
'''
#给定一个包含很多固定长度记录的二进制文件，你想读取其中某一条记录，而且不需要逐条读取记录
#解决方案：一条记录相对于文件头部的偏移字节，就是这条记录的长度再乘以记录的条数（正整数从0开始计数）
#因此，可以直接将读取位置设置在正确的点上，然后读取数据，比如如果每条记录长度是48字节长，则从二进制文件中
#读取第七条记录方法如下：
thefile = open('data', 'rb')
record_size = 48
record_number = 6
thefile.seek(record_size * record_number)
buffer = thefile.read(record_size)
#本方法适用于二进制文件，不适用于文本文件
'''
2.8 更新随机存取文件
'''
#给定一个包含很多固定长度记录的大二进制文件，你想读取其中某一条记录，并且修改该条记录的
#某些字段的值，然后写回到文件中
#解决方案：读取记录，解包，执行任何需要的数据更新，然后将所有字段重新组合成记录，接着找到正确的位置，最后再写入
import struct
format_string = '81'  #或者说一条记录是八个四字节整数
thefile = open('data', 'r+b')
record_size = struct.calcsize(format_string)
#record_numberb
thefile.seek(record_size * record_number)
buffer = thefile.read(record_size)
fields = list(struct.unpack(format_string, buffer))
#进行计算，并修改相关的字段，然后：
buffer = struct.pack(format_string, *fields)
thefile.seek(record_size * record_number)
thefile.write(buffer)
thefile.close()
'''
2.9 从zip文件中读取数据
'''
#你想直接检查一个zip格式的归档文件中部分或者所有的文件，同时还要避免将这些文件展开到磁盘上
import zipfile
z = zipfile.ZipFile('zipfile.zip', 'r')
for filename in z.namelist():
    print 'File:',filename,
    bytes = z.read(filename)
    print 'has', len(bytes), 'bytes'
#zipfile模块现在还不能处理分卷zip文件和带有注释的zip文件，注意，要使用r作为标志参数，而不是rb
#如果zip文件中包含一些Python模块，（.py或.pyc）也许还有一些其他数据文件，可以把这个文件的路径加入到Python的sys.path中
#并用import语句来导入处于这个zip文件中的模块。示例：
import zipfile, tempfile, os, sys
handle, filename = tempfile.mkstemp('.zip')
os.close(handle)
z = zipfile.ZipFile(filename, 'w')
z.writestr('hello.py', 'def f():return "hello world from "+__file__\n')
z.close()
sys.path.insert(0, filename)
import hello
print hello.f()
os.unlink(filename)
'''
2.10 处理字符串中的zip文件
'''
#解决这种问题，正是Python标准库的cStringIO模块的拿手好戏
import cStringIO, zipfile
class ZipString(ZipFile):
    def __init__(self, datastring):
        ZipFile.__init__(self, cStringIO.StringIO(datastring))
#cStringIO模块可以将一串字节封装起来，让你像访问文件对象一样访问其中的数据
import zipfile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
class ZipString(ZipFile):
    def __init__(self, datastring):
        ZipFile.__init__(self, StringIO(datastring))

'''
2.11 将文件树归档到一个压缩的tar文件
'''
#需要将一个文件树中的所有文件和子目录归档到一个tar归档文件，然后用流行的gzip方式或者更高压缩率的bzip2方式来压缩
#Python标准库的tarfile模块直接提供了这两种压缩方式，你只需调用tarfile.TarFile.open创建归档文件时，传入一个选项字符串以指定需要的压缩方式即可
import tarfile, os
def make_tar(folder_to_backup, dest_folder, compression = 'bz2'):
    if compression:
        dest_ext = '.' + compression
    else:
        dest_ext = ''
    arcname = os.path.basename(folder_to_backup)
    dest_name = '%s.tar%s' % (arcname, dest_ext)
    dest_path = os.path.join(dest_folder, dest_name)
    if compression:
        dest_cmp = ':' + compression
    else:
        dest_cmp = ''
    out = tarfile.TarFile.open(dest_path, 'w'+dest_cmp)
    out.add(folder_to_backup, arcname)
    out.close()
    return dest_path
'''
2.12 将二进制数据发送到Windows的标准输出
'''
import sys
if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
'''
2.13 使用C++的类iostream语法
'''
#你喜欢C++基于ostream和操纵符（插入了这种特定的对象后，它会在stream中产生特定的效果）的I/O方式，并想将此形式用在自己的Python程序中
'''
2.14 回退输入文件到起点
'''
#需要创建一个输入文件对象（数据可能来自于网络socket或者其他输入文件句柄），此文件对象允许回退到起点，这样就可以完全读取其中所有的数据
#解决方案：将文件对象封装到一个合适的类中
from cStringIO import StringIO
class RewindableFile(object):
    """封装一个文件句柄以便重定位到开始位置"""
    def __init__(self, input_file):
        """将input_file封装到一个支持回退的类文件对象中"""
        self.file = input_file
        self.buffer_file = StringIO()
        self.at_start = True
        try:
            self.start = input_file.tell()
        except(IOError, AttributeError):
            self.start = 0
        self._use_buffer = True
    def seek(self, offset, whence = 0):
        """根据给定的字节定位
        #必须：whence == 0 and offset == self.start
        """
        if whence != 0:
            raise ValueError("whence=%r; expecting 0" % (whence,))
        if offset != self.start:
            raise ValueError("offset=%r; expecting %s" % (offset, self.start))
        self.rewind()
    def rewind(self):
        """回到起始位置"""
        self.buffer_file.seek(0)
        self.at_start = True
    def tell(self):
        """返回文件的当前位置（必须在开始处）"""
        if not self.at_start:
            raise TypeError("RewindableFile can't tell expect at start of file")
        return self.start
    def _read(self, size):
        if size < 0:    #一直读到文件末尾
            y = self.file.read()
            if self._use_buffer:
                self.buffer_file.write(y)
            return self.buffer_file.read() + y
        elif size == 0:    #不必读空字符串
            return ""
        x = self.buffer_file.read(size)
        if len(x) < size:
            y = self.file.read(size - len(x))
            if self._use_buffer:
                self.buffer_file.write(y)
            return x + y
        return x
    def read(self, size = -1):
        """根据size指定的大小读取数据
        #默认为-1，意味着一直读到文件结束
        """
        x = self._read(size)
        if self.at_start and x:
            self.at_start = False
        self._check_no_buffer()
        return x
    def readline(self):
        """从文件中读取一行"""
        #buffer_file中有吗？
        s = self.buffer_file.read.line()
        if s[-1:] == "\n":
            return s
        #没有，从输入文件中读取一行
        t = self.file.readline()
        if self._use_buffer:
            self.buffer_file.write(t)
        self._check_no_buffer()
        return s + t
    def readlines(self):
        """读取文件中所有剩余的行"""
        return self.read().splitlines(True)
    def _check_no_buffer(self):
        #如果'nobuffer'被调用，而且我们也完成了对缓存文件的处理
        #那就删掉缓存，把所有的东西都重定向到原来的输入文件
        if not self._use_buffer and \
            self.buffer_file.tell() == len(self.buffer_file.getvalue()):
            #为了获得尽可能高的性能，我们重新绑定了self中的所有相关方法
            for n in "seek tell read readline readlines".split():
                setattr(self, n, getattr(self.file, n, None))
            del self.buffer_file
    def nobuffer(self):
        """通知RewindableFile，一旦缓存耗尽就停止继续使用缓存"""
        self._use_buffer = False
'''
2.15 用类文件对象适配真实文件对象
'''
#需要传递一个类似文件的对象（比如，调用urllib.urlopen返回的结果）给一个函数或者方法
#但这个函数或方法要求只接受真实的文件对象（比如，像marshal.load这样的函数）
import types, tempfile
CHUNK_SIZE = 16 * 1024
def adapt_file(fileObj):
    if isinstance(fileObj, file):return fileObj
    tmpFileObj = tempfile.TemporaryFile
    while True:
        data = fileObj.read(CHUNK_SIZE)
        if not data:break
        tmpFileObj.write(data)
    fileObj.close()
    tmpFileObj.seek(0)
    return tmpFileObj
'''
2.16 遍历目录树
'''
#需要检查一个目录，或者某个包含子目录的目录树，并根据某种模式迭代所有的文件（也可能包含子目录）
#Python标准库模块os中的生成器os.walk对于这个任务来说完全够用了，不过我们可以给它打扮打扮，封装成自己的函数
import os, fnmatch
def all_files(root, patterns='*', single_level=False, yield_folders=False):
    #将模式从字符串中取出放入列表中
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if single_level:
            break
thefiles = list(all_files('D:\go-project\python-cookbook', '*.py;*.pyc'))
#区分大小写
#用"*.[Hh][Tt][Mm][Ll]"替换"*.html"
'''
2.17 在目录树中改变文件扩展名
'''
#需要在一个目录的子树中重命名一系列文件，具体的说，你想将某一指定类型的文件的扩展名改成另一种扩展名
#用Python标准库提供的os.walk函数来处理子目录中的所有文件，任务变得非常容易
import os
def swapextensions(dir, before, after):
    if before[:1] != '.':
        before = '.' + before
    thelen = -len(before)
    if after[:1] != '.':
        after = '.' + after
    for path, subdirs, files in os.walk(dir):
        for oldfile in files:
            if oldfile[thelen:] == before:
                oldfile = os.path.join(path, oldfile)
                newfile = oldfile[:thelen] + after
                os.rename(oldfile, newfile)
'''
if __name__=='__main__':
    import sys
    if len(sys.argv) != 4:
        print "Usage: swapext rootdir before after"
        sys.exit(100)
    swapextensions(sys.argv[1], sys.argv[2], sys.argv[3])
'''
'''
2.18 从指定的搜索路径寻找文件
'''
import os
def search_file(filename, search_path, pathsep=os.pathsep):
    """给定一个搜索路径，根据请求的名字找到文件"""
    for path in search_path.split(pathsep):
        candidate = os.path.join(path, filename)
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)
    return None
'''
if __name__=='__main__':
    search_path = '/bin' + os.pathsep + '/usr/bin' #;on Windows, :on UNIX
    file_file = search_file('ls', search_path)
    if find_file:
        print "File 'is' found at %s" % find_file
    else:
        print "File 'ls' not found"
'''
'''
2.19 根据指定的搜索路径和模式寻找文件
'''
#基本上需要循环路径中所有的目录。这个循环最好被封装成一个生成器
import glob, os
def all_files(pattern, search_path, pathsep=os.pathsep):
    """给定搜索路径，找出所有满足匹配条件的文件"""
    for path in search_path.split(pathsep):
        for match in glob.glob(os.path.join(path, pattern)):
            yield match
print all_files('*.pye', os.environ['PATH']).next()

for match in all_files('*.pye', os.enveiron['PATH']):
    print match

print list(all_files('*.pye', os.environ['PATH']))

'''
2.20 在Python的搜索路径中寻找文件
'''
#任务：一个大的Python应用程序包括了资源文件（比如Glade项目文件、SQL模板）
#和图片以及Python包。你想把所有这些相关文件和用到他们的Python包储存起来
#可以再Python的sys.path中寻找文件或目录
import sys, os
class Error(Exception):pass
def _find(pathname, matchFunc=os.path.isfile):
    for dirname in sys.path:
        candidate = os.path.join(dirname, pathname)
        if matchFunc(candidate):
            return candidate
    raise Error("Can't find file %s" % pathname)
def findFile(pathname):
    return _find(pathname)
def findDir(path):
    return _find(path, matchFunc=os.path.isdir)

'''
2.21 动态地改变Python搜索路径
'''
#模块必须处于Python搜索路径中才能被导入，但你不想设置个永久性的大路径，因为那样可能会影响性能
#所以，你希望能够动态地改变这个路径
#只需要简单地在Python的sys.path中加入一个“目录”。不过要小心重复的情况
def AddSysPath(new_path):
    """AddSysPath(new_path)：给Python的sys.path增加一个目录
        如果此目录不存在或者已经在sys.path中了，则不操作
        返回1表示成功，-1表示new_path不存在，0表示已经在sys.path中了
    """
    import sys, os
    #避免加入一个不存在的目录
    if not os.path.exists(new_path): return -1
    #将路径标准化，Windows是大小写不敏感的，所以若确定在Windows下，将其转成小写
    new_path = os.path.abspath(new_path)
    if sys.platform == 'win32':
        new_path = new_path.lower()
    #检查当前所有的路径
    for x in sys.path:
        x = os.path.abspath(x)
        if sys.platform == 'win32'
            x = x.lower()
        if new_path in (x, x + os.sep):
            return 0
    sys.path.append(new_path)
    #如果想让new_path在sys.path处于最前
    #使用：sys.path.insert(0, new_path)
    return 1
'''
if __name__=='__main__':
    #测试，显示用法
    import sys
    print 'Before':
    for x in sys.path: print x
    if sys.platform == 'win32':
        print AddSysPath('c:\\Temp')
        print AddSysPath('c:\\temp')
    else:
        print AddSysPath('/usr/lib/my_modules')
    print 'After':
    for x in sys.path: print x
'''

'''
2.22 计算目录间的相对路径
'''
#需要知道一个目录对另一个目录的相对路径是什么——比如，有时候需要创建一个符号链接
#或者一个相对的URL引用
#最简单的方法就是把目录拆分到一个目录的列表中，然后对列表进行处理。
import os, itertools
def all_equal(elements):
    '''若所有元素都相等，则返回True，否则返回False'''
    first_element = elements[0]
    for other_element in elements[1:]:
        if other_element != first_element: return False
def common_prefix(*sequences):
    '''
    返回所有序列开头部分功能元素的列表
    紧接一个各序列的不同尾部的列表
    '''
    #如果没有sequence，完成
    if not sequences: return [],[]
    #并行地循环序列
    common = []
    for elements in itertools.izip(*sequences):
        #若所有元素相等，跳出循环
        if not all_equal(elements): break
        #得到一个共同的元素，添加到末尾并继续
        common.append(elements[0])
    #返回相同的头部和各自不同的尾部
    return common, [sequence[len(common):] for sequence in sequences]
def relpath(p1, p2, sep=os.path.sep, pardir=os.path.pardir):
    '''
    返回p1对p2的相对路径
    特殊情况：空串，if p1 == p2；p2 如果p2和p1完全没有相同的元素
    '''
    common, (u1, u2) = common_prefix(p1.split(sep), p2.split(sep))
    if not common:
        return p2 #如果完全没有共同元素，则路径是绝对路径
    return sep.join( [pardir]*len(u1) + u2 )
def test(p1, p2, sep=os.path.sep):
    '''调用relpath函数，打印调用参数和结果'''
    print "from",p1,"to",p2,"->", relpath(p1, p2, sep)
'''
if __name__=='__main__':
    test('/a/b/c/d','/a/b/c1/d1', '/')
    test('/a/b/c/d','/a/b/c/d', '/')
    test('c:/x/y/z','d:/x/y/z', '/')
'''
'''
2.23 跨平台地读取无缓存的字符
'''
#任务：你的程序需要从标准输出中，读取无缓存的单个的字符，兼容Windows和类UNIX
try:
    from msvcrt import getch
except ImportError:
    '''我们不在Windows中，所以可以尝试类UNIX的方式'''
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
'''
2.24 在Mac OS X平台上统计PDF文档的页数
'''
#!/usr/bin python
import CoreGraphics
def pageCount(pdfPath):
    '''返回指定路径的PDF文档的页数'''
    pdf = CoreGraphics.CGPDFDocumentCreateWithProvider(
            CoreGraphics.CGDataProviderCreateWithFilename(pdfPath)
        )
    return pdf.getNumberOfPages()

'''
2.25 在Windows平台上修改文件属性
'''
import win32con, win32api, os
#创建一个文件并展示如何操纵它
thefile = 'test'
f = open('test', 'w')
f.close()
#设置成隐藏文件
win32api.SetFileAttributes(thefile, win32con.FILE_ATTRIBUTE_HIDDEN)
#设置成只读文件
win32api.SetFileAttributes(thefile, win32con.FILE_ATTRIBUTE_READONLY)
#为了删除它先把他设置成普通文件
win32api.SetFileAttributes(thefile, win32con.FILE_ATTRIBUTE_NORMAL)
#最后删除该文件
os.remove(thefile)

'''
2.26 从OpenOffice.org文档中提取文本
'''
#OpenOffice.org文档其实就是一个聚合了XML文件的zip文件，遵循一种良好的文档规范。
#如果只是为了访问其中的数据，我们甚至不用安装OpenOffice.org
import zipfile, re
rx_stripxml = re.compile("<[^>]*?>", re.DOTALL|re.MULTILINE)
def convert_OO(filename, want_text=True):
    """将一个OpenOffice.org文件转换成XML或文本"""
    zf = zipfile.ZipFile(filename, "r")
    data = zf.read("content.xml")
    zf.close()
    if want_text:
        data = "".join(rx_stripxml.sub("",data).split())
    return data
'''
2.27 从微软Word文档中抽取文本
'''
import fnmatch, os, sys, win32com.client
wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")
try:
    for path, dirs, files in os.walk(sys.argv[1]):
        for filename in files:
            if not fnmatch.fnmatch(filename, '*.doc'): continue
            doc = os.path.abspath(os.path.join(path, filename))
            print "processing %s" % doc
            wordapp.Document.Open(doc)
            docastxt = doc[:-3] + 'txt'
            wordapp.ActiveDocument.SaveAd(docastxt, FileFormat=win32com.client.constants.wdFormatText)
            wordapp.ActiveDocument.Close()
finally:
    #确保即使有异常发生Word仍能被正常关闭
    wordapp.Quit()
'''
2.28 使用跨平台的文件锁
'''
'''
2.29 带版本号的文件名
'''
'''
2.30 计算CRC-64循环冗余码校验
'''
