# zeno

```
# 挂载谷歌云盘到本地
# 1. 获取google drive client id 和secret
# 2. 左侧面板选择‘凭据’，右侧选择‘OAuth 2.0 客户端ID’
# 3. 选择对应的项目，如果没有，就新建，选择‘编辑’，就可以看到client id 和secret了，保存这两项

apt install rclone
rclone config
# 1.  n) New remote
# 2.  ‘name’输入gdrive
# 3.  选择‘Google Drive’对应的序号，当前是‘13’
# 4.  ‘client id’，输入刚才得到的client id
# 5.  ‘client secret’，输入刚才得到的client secret
# 6.  ‘scope’选择1，Full access.
# 7.  ‘roo_folder_id’选择谷歌云盘文件夹的id，可以在浏览器的URL里最后一段找到
# 8.  ‘service account’回车跳过
# 9.  ‘Advanced config’选择‘n’
# 10. ‘Auto config’选择‘n’
# 11. 浏览器访问软件提示的网址，完成授权，将授权后的代码，粘贴到当前命令行输入
# 12. ‘team drive’选择‘n’
# 13. 连续输入‘y’和‘q’退出

# 同步命令在instal.sh中，其他问题参考：https://tcude.net/setting-up-rclone-with-google-drive/

# Install dependencies
apt install python3-pip
python3 -m pip install -r requirements.txt

# Install and configure automation
bash install.sh
crontab -l  # To check daily job trigger.
```
