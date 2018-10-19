# cbot 
## a chinese chat robot
### Introduction to cbot usage：
##### version：0.1.0
####how to install cbot:
#####pip install cbot
#####if you got an error when install python-Levenshtein package
#####you can download .whl file and install this package:[python-levenshtein](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-levenshtein)
####If you want to use it locally:
```angular2html
from cbot import CBot
cbot = CBot('cbotName')

# If you start from scratch
# cbot.train()
# while True:
#     que = input('me：')
#     reponse = cbot.get_response(str(que))
#     print('cbot：', reponse)


# If you want to train some data first
# The data set must be list type.
# And the next sentence is the answer to the last sentence.
trainList = [
    '早',
    '早上好',
    '早饭吃了么',
    '还没呢！，你呢？',
    '我也没吃',
    '我们一起吃早饭去吧',
    '好呀'
]

cbot.train(trainList)
while True:
    que = input('me：')
    reponse = cbot.get_response(str(que))
    print('cbot：', reponse)
```
####If you want to use it with turing api:
```angular2html
from cbot import CBot

cbot = CBot('felix')
cbot.turing_key = ''  # you should git an api key at http://www.tuling123.com/
while True:
    que = input('我：')
    reponse = cbot.get_response(str(que), api='turing')
    print('CBot：', reponse)
```

###Now have fun!
###If you get a bug,you can send the bug to my email.
###Here is my email:felix2@foxmail.com







