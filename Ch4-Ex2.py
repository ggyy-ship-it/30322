def quicksort(array):
    #Base Case:        剩下 0 或 1 個元素的陣列，就不用再比較了
    if len(array) <=1 :       ####修改 是否剩下0或1個值####
       return array                   #回傳1個值或空值
    #Recursive Case:   還有沒比較的(>=2個值以上)
            
    pivot = array[0]                #預設0為基準點
    less=[]                         #左邊空間
    greater=[]                      #右邊空間
    for i in range( 1, len(array) ):#從1開始(0的下一個)
            if pivot >= array[i] :                ####修改 跟基準比較####
                less.append(array[i])                               ####修改 放到左邊####
            elif pivot <= array[i]:              ####修改 跟基準比較####
                greater.append(array[i])                       ####修改 放到右邊####
    print(less,[pivot],greater)     #輸出不更動#
         
    return quicksort(less) + [pivot] + quicksort(greater)    ####修改 左邊+中間+右邊 陣列相加，參考最上面補充####
 

data = list(map(int,input().split()))#讀資料
print( quicksort(data) )    #輸出不更動#