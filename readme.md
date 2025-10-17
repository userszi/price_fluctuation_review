## 手动刷新缓存
1. cd d:/cursor/workshop/Price_fluctuation_review; python data_processor.py 
2. python -m http.server 8000 
3. http://localhost:8000/new_stock_analysis.html

## 使用路径
1. 从THS获取涨停excel+跌停excel，整理成一个excel
2. 提取其中的股票名字丢给豆包整理成同创批量需要的格式
3. 同创批量跑
4. 批量文件丢给豆包整理成合适的格式
5. 提取input字段填充到完整excel上
6. 跑脚本
7. 启动服务+进网址