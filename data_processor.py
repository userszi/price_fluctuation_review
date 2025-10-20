import pandas as pd
import json
import re

def process_excel_data():
    """处理Excel数据并转换为JSON格式"""
    
    # 读取Excel文件
    df = pd.read_excel('d:/工作细化/量化代码/涨跌停复盘/涨停25.10.20.xlsx')
    
    # 数据清洗和处理
    stock_data = []
    
    for index, row in df.iterrows():
        # 检查股票代码和名称是否有效（不为空或NaN）
        if pd.isna(row['代码']) or pd.isna(row['名称']):
            continue
            
        # 处理总金额，支持亿、万单位换算
        amount_value = row['总金额'] if pd.notna(row['总金额']) else 0
        if amount_value >= 100000000:  # 大于等于1亿
            amount_str = f"{amount_value/100000000:.2f}亿"
        elif amount_value >= 10000:  # 大于等于1万
            amount_str = f"{amount_value/10000:.2f}万"
        else:
            amount_str = f"{amount_value:.2f}"
            
        # 处理流通市值，支持亿、万单位换算
        market_value = row['流通市值'] if pd.notna(row['流通市值']) else 0
        if market_value >= 100000000:  # 大于等于1亿
            market_value_str = f"{market_value/100000000:.2f}亿"
        elif market_value >= 10000:  # 大于等于1万
            market_value_str = f"{market_value/10000:.2f}万"
        else:
            market_value_str = f"{market_value:.2f}"
        
        # 基础信息
        stock = {
            'code': str(row['代码']) if pd.notna(row['代码']) else '--',
            'name': str(row['名称']) if pd.notna(row['名称']) else '--',
            'price': str(row['现价']) if pd.notna(row['现价']) else 'null',
            'change': f"{float(row['涨幅'])*100:+.2f}%" if pd.notna(row['涨幅']) else 'null',
            'turnover': str(row['换手']) if pd.notna(row['换手']) else 'null',
            'amount': amount_str,
            'amount_value': amount_value,  # 保存原始数值用于排序
            'marketValue': market_value_str,
            'marketValue_value': market_value,  # 保存原始数值用于排序
            'reason': row['涨停原因类别[20251014]'] if pd.notna(row['涨停原因类别[20251014]']) else '--',
            'industry': row['所属行业'] if pd.notna(row['所属行业']) else '--',
            'subIndustry': row['细分行业'] if pd.notna(row['细分行业']) else '--',
            'daysLimit': int(row['连续涨停天数[20251014]']) if pd.notna(row['连续涨停天数[20251014]']) and row['连续涨停天数[20251014]'] != '--' else 0,
            'province': row['省份'] if pd.notna(row['省份']) else '--',
            'concepts': row['所属概念'] if pd.notna(row['所属概念']) else '--'
        }
        
        # 处理涨停原因分析
        reasons = []
        if pd.notna(row['input']):
            input_text = str(row['input'])
            # 解析JSON格式的原因分析
            try:
                # 直接尝试解析整个input文本为JSON
                reasons_data = json.loads(input_text)
                for reason_item in reasons_data:
                    if isinstance(reason_item, dict):
                        reasons.append({
                            'topic': reason_item.get('话题', ''),
                            'importance': reason_item.get('重要度', 3),
                            'summary': reason_item.get('摘要', ''),
                            'count': reason_item.get('次数', '1'),
                            'time': reason_item.get('时间', ''),
                            'core_entity': reason_item.get('核心主体', ''),
                            'key_info_chain': reason_item.get('关键信息链', '')
                        })
            except json.JSONDecodeError:
                # 如果直接解析失败，尝试清理数据格式后再解析
                try:
                    # 清理数据格式
                    input_text = input_text.replace('\\n', ' ').replace('\\"', '"')
                    # 尝试提取JSON数组
                    json_matches = re.findall(r'\[.*?\]', input_text, re.DOTALL)
                    if json_matches:
                        reasons_data = json.loads(json_matches[0])
                        for reason_item in reasons_data:
                            if isinstance(reason_item, dict):
                                reasons.append({
                                'topic': reason_item.get('话题', ''),
                                'importance': reason_item.get('重要度', 3),
                                'summary': reason_item.get('摘要', ''),
                                'count': reason_item.get('次数', '1'),
                                'time': reason_item.get('时间', ''),
                                'core_entity': reason_item.get('核心主体', ''),
                                'key_info_chain': reason_item.get('关键信息链', '')
                            })
                except:
                    # 如果JSON解析仍然失败，尝试提取关键信息
                    topics = re.findall(r'"话题"\s*:\s*"([^"]+)"', input_text)
                    summaries = re.findall(r'"摘要"\s*:\s*"([^"]+)"', input_text)
                    
                    for i, topic in enumerate(topics):
                        summary = summaries[i] if i < len(summaries) else ''
                        reasons.append({
                            'topic': topic,
                            'importance': 3,
                            'summary': summary
                        })
        
        # 如果没有解析到原因，使用涨停原因类别
        if not reasons and stock['reason'] != '--':
            reasons = [{
                'topic': f"{stock['name']}涨跌停原因分析",
                'importance': 4,
                'summary': f"该股票因{stock['reason']}相关因素涨停"
            }]
        
        stock['reasons'] = reasons
        
        # 处理reason字段，提取stockLogic内容
        stock_logic = ''
        if pd.notna(row['reason']):
            reason_text = str(row['reason'])
            try:
                reason_data = json.loads(reason_text)
                # 检查reason_data可能是列表或字典
                if isinstance(reason_data, dict):
                    # 尝试获取stockLogic或analysisContent字段
                    stock_logic = reason_data.get('stockLogic', '') or reason_data.get('analysisContent', '')
                elif isinstance(reason_data, list) and len(reason_data) > 0:
                    # 如果是列表，尝试获取第一个元素的stockLogic或analysisContent字段
                    first_item = reason_data[0]
                    if isinstance(first_item, dict):
                        stock_logic = first_item.get('stockLogic', '') or first_item.get('analysisContent', '')
            except json.JSONDecodeError:
                stock_logic = reason_text
        
        stock['stockLogic'] = stock_logic
        stock_data.append(stock)
    
    return stock_data

def generate_statistics(stock_data):
    """生成统计数据"""
    total_stocks = len(stock_data)
    
    # 计算涨停股票数量（涨幅接近10%的）
    limit_up_count = 0
    total_turnover = 0
    
    for stock in stock_data:
        if stock['change'] != '--':
            change_value = float(stock['change'].replace('+', '').replace('%', ''))
            if change_value >= 0:  # 接近涨停
                limit_up_count += 1
        
        if stock['turnover'] != '--':
            turnover_value = float(stock['turnover'].replace('%', ''))
            total_turnover += turnover_value
    
    avg_turnover = total_turnover / total_stocks if total_stocks > 0 else 0
    # 计算跌停股票数量（涨幅接近-10%的）
    limit_down_count = 0
    for stock in stock_data:
        if stock['change'] != '--':
            change_value = float(stock['change'].replace('%', ''))
            if change_value <= 0:  # 接近跌停
                limit_down_count += 1
    
    return {
        'total_stocks': total_stocks,
        'limit_up': limit_up_count,
        'limit_down': limit_down_count,
        'avg_turnover': f"{avg_turnover:.1f}%"
    }

def save_data_to_json(stock_data, stats):
    """保存数据到JSON文件"""
    output = {
        'statistics': stats,
        'stocks': stock_data
    }
    
    with open('d:/cursor/workshop/Price_fluctuation_review/stock_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存，共处理 {len(stock_data)} 只股票")
    print(f"统计数据: 总股票数={stats['total_stocks']}, 涨停={stats['limit_up']}, 跌停={stats['limit_down']}, 平均换手率={stats['avg_turnover']}")

if __name__ == "__main__":
    print("开始处理Excel数据...")
    
    # 处理数据
    stock_data = process_excel_data()
    
    # 生成统计数据
    stats = generate_statistics(stock_data)
    
    # 保存数据
    save_data_to_json(stock_data, stats)
    
    # 显示前3只股票的信息作为示例
    print("\n前3只股票信息:")
    for i, stock in enumerate(stock_data[:3]):
        print(f"{i+1}. {stock['code']} {stock['name']} - {stock['change']} - {stock['reason']}")
        if stock['reasons']:
            print(f"   涨停原因: {stock['reasons'][0]['topic']}")