# friends.py
# 負責讀取文字檔並建立 graph 資料結構

def load_network(filename: str) -> dict:
    """
    從文字檔讀取友誼小船，並建立 'graph' 字典。
    """
    graph = {}
    print(f"正在從 {filename} 讀取友誼小船...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]: # 跳過標題行
                
                # .strip() 去除換行
                # .split(',') 用逗號分割
                parts = line.strip().split(',')
                
                if len(parts) != 3:
                    print(f"格式錯誤，跳過此行: {line.strip()}")
                    continue
                    
                p1, p2, closeness_str = parts
                
                # 確保 closeness 是數字
                closeness = int(closeness_str)
                
                # 因為是無向圖，兩邊都要加
                graph.setdefault(p1, {})[p2] = closeness
                graph.setdefault(p2, {})[p1] = closeness
                
        print("友誼小船讀取完畢。")
        return graph # 將建立好的 graph 回傳
    
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {filename}")
        return {} # 回傳空字典
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return {}