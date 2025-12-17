book={}
while True:
    #print('請輸入要使用的功能')
    #print('a.新增項目與值 b.查詢 c.更新資料 d.離開')
    choose = input()
    if choose == 'a':
        #print('請輸入要新增的項目')
        #判斷是否重複
        new = input()
        #重複了
        if new in book:
            print('Data:',new,'exists')    
        #可新增
        elif new not in book:             #等同else:
            #print('請輸入要新增項目的值')
            val = input()
            book[new] = val
            print('Data:',new,', Value:',book[new],'Added successfully')  
    elif choose == 'b':
        #print('請輸入要查詢的項目')
        #查詢是否存在
        key = input()
        if key in book:
            print('The value of', key ,'is', book[key] )  
        #不存在
        else:
            print('Data:',key,'not exists')  
    elif choose == 'c':
        #print('請輸入要修改的項目')
        update = input()            #輸入
        #存在
        if update in book :        #判斷
            #print('請輸入要更新的數值')
            x = input()        #輸入
            book[update] = x       #更新
            print('The value of',update,'has updated to',book[update] )    
        #不存在
        else:    
            print('Data:',update,'not exists')  
           
    elif choose == 'd':
        print('End')    #不更改
        break