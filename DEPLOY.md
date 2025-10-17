# Vercel部署指南

## 部署步骤

1. 将代码推送到GitHub仓库
   ```bash
   git push origin main
   ```

2. 访问 [Vercel官网](https://vercel.com) 并登录

3. 点击 "New Project"

4. 导入您的GitHub仓库 `price_fluctuation_review`

5. 配置项目设置：
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: 留空（不需要）
   - Output Directory: 留空（不需要）
   - Install Command: 留空（不需要）

6. 点击 "Deploy"

## 常见问题解决

### 1. 404错误
- 确保 `vercel.json` 文件已正确配置
- 检查 `stock_data.json` 文件是否在仓库根目录

### 2. JSON文件加载失败
- 检查HTML中的路径是否为 `./stock_data.json`
- 确保JSON文件没有语法错误

### 3. 页面样式丢失
- 确保所有CSS样式都在HTML文件内
- 检查是否有外部CSS链接无法访问

## 部署后访问

部署成功后，Vercel会提供一个URL，您可以：
- 直接访问该URL查看应用
- 分享该URL给其他人查看

## 本地预览

在部署前，您可以使用以下命令在本地预览：
```bash
# 启动本地服务器
python -m http.server 8000

# 访问 http://localhost:8000/new_stock_analysis.html
```

## 更新部署

每次更新代码后：
1. 提交更改到Git
2. 推送到GitHub
3. Vercel会自动重新部署