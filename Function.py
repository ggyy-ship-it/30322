#function 單純執行程式
def hello() :
    print('hello world')
hello()

#function 可帶入參數
def Name( name ) :
    print('hello',name)
Name('Jason')

#function 回傳結果
def add(a,b) :
    s = a + b
    return s
x = add(1,3)
print(x)