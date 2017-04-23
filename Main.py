# -*- coding: UTF-8 -*-#
__author__ = 'Rik'

import requests
# HTTP LIB requests: http://docs.python-requests.org/en/latest/

class CodeSearch1024():
    def __init__(self, codeWithMask, parent=None):
        self.url='http://cl.giit.us/register.php'
        self.codeWithMask = codeWithMask
        # self.chars = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.chars = '0123456789'
        self.chars1 = '0123456789'#'abcdefghijklmnopqrstuvwxyz'
        self.chars2 = '0123456789'

    def getMaskCount(self):
        count = 0
        for ch in self.codeWithMask:
            if ch == '*':
                count += 1
        return count

    def getAndNumber(self):
        count = 0
        for _ in self.codeWithMask:
            if _ == '@':
                count += 1
        return  count

    def start(self, samemask = False):
        maskCount = self.getMaskCount()
        andCount = self.getAndNumber()
        print maskCount, andCount
        self.codeWithMask = self.codeWithMask.replace('*','%s')
        if maskCount>3:
            print(u'暂时不能处理大于3个隐藏字符的邀请码')
            return
        if maskCount == 0:
            code = self.codeWithMask
            result = self.doReg(code,0)
            if result == 'found':
                print('%s found!' % (code))
                return
            else:
                print('%s %s!' % (code,result))
        # elif samemask:
        #     for ch in self.chars:
        #         code = self.codeWithMask % ((ch,)*maskCount)
        #         result = self.doReg(code,0)
        #         if result == 'found':
        #             print('%s found!' % (code))
        #             return
        #         else:
        #             print('%s %s!' % (code,result))
        elif maskCount == 1:
            for ch in self.chars:
                code = self.codeWithMask % (ch)
                result = self.doReg(code,0)
                if result == 'found':
                    print('%s found!' % (code))
                    return
                else:
                    print('%s %s!' % (code,result))
        elif maskCount == 2 and not andCount:
            for ch1 in self.chars:
                for ch2 in self.chars:
                    code = self.codeWithMask % (ch1,ch2)
                    result = self.doReg(code,0)
                    if result == 'found':
                        print('%s found!' % (code))
                        return
                    else:
                        print('%s %s!' % (code,result))

        elif maskCount == 3:
            for ch1 in self.chars:
                for ch2 in self.chars:
                    for ch3 in self.chars:
                        code = self.codeWithMask % (ch1,ch2,ch3)
                        result = self.doReg(code,2)
                        if result == 'found':
                            print('%s found!' % (code))
                            return
                        else:
                            print('%s %s!' % (code,result))
        #可以是2个相同的,@为字母#为数字
        elif samemask and andCount:
            for ch in self.chars:
                code = self.codeWithMask % ((ch,)*maskCount)
                if '@' in code:
                    codeWithChar = code.replace('@','%s')
                    for abc in 'abcdef':
                        codeTure = codeWithChar % ((abc,)*andCount)
                        result = self.doReg(code,0)
                        if result == 'found':
                            print('%s found!' % (code))
                            return
                        else:
                            print('%s %s!' % (code,result))
        print('done!')


    def doReg(self,code,n):
        #可重试5次
        if n>5:
            return 'timeout'

        postData = {'regname':'youngytj',
                        'regpwd':'999999',
                        'regpwdrepeat':'999999',
                        'regemail':'youngytj@sina.com',
                        'invcode':code,
                        'forward':'',
                        'step':'2'
                   }
        try:
            r = requests.post(url=self.url,data=postData)
            html = r.text.encode(r.encoding).decode('gbk')
            # print html
            if html.find(u'邀請碼錯誤')>-1:
                return 'incorrect'
            else:
                return 'found'
        except:
            return self.doReg(code,n+1) #递归


#用法示例
#code = raw_input(u'Please input a code: ') # e.g.: *8m*9754yupt307t
# code = '77c4e**e935*03c8'
# code = 'eb8d58e*d14ee*ba'
# code = 'eb8d58e9d14ee0ba'
code = 'b55@a*a*049ec0@c'

print 'code is', code
print 'Running'
reg = CodeSearch1024(code)
reg.start(True)

raw_input()