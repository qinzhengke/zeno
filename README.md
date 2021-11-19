# zeno

# 1.获取谷歌网盘相关秘钥信息

```
# 1. 获取Google drive相关秘钥
# 1) 找到‘google api console’页面，获取google drive client id 和secret
# 2) 左侧面板选择‘凭据’，右侧选择‘OAuth 2.0 客户端ID’
# 3) 选择对应的项目，如果没有，就新建，选择‘编辑’，就可以看到client id 和secret了，保存这两项
```

# 2. 配置rclone，关联到谷歌网盘

```
apt install rclone
rclone config
# 1)  n) New remote
# 2)  ‘name’输入gdrive
# 3)  选择‘Google Drive’对应的序号，当前是‘13’
# 4)  ‘client id’，输入刚才得到的client id
# 5)  ‘client secret’，输入刚才得到的client secret
# 6)  ‘scope’选择1，Full access.
# 7)  ‘roo_folder_id’选择谷歌云盘文件夹的id，可以在浏览器的URL里最后一段找到
# 8)  ‘service account’回车跳过
# 9)  ‘Advanced config’选择‘n’
# 10) ‘Auto config’选择‘n’
# 11) 浏览器访问软件提示的网址，完成授权，将授权后的代码，粘贴到当前命令行输入
# 12) ‘team drive’选择‘n’
# 13) 连续输入‘y’和‘q’退出
```

注：同步命令在install.sh中，其他问题参考：https://tcude.net/setting-up-rclone-with-google-drive/

# 3. 配置API秘钥

- 将Twitter的api秘钥存放在~/.zeno/twitter_api_key.txt
- 将Cryptorank的api秘钥存放在~/.zeno/cryptorank_api_key.txt

# 4. 安装并启用本仓库相关应用

```
apt install python3-pip
python3 -m pip install -r requirements.txt

# Install and configure automation
bash install.sh
crontab -l  # To check daily job trigger.
```

# 5. 新建“~/.ssh/config”文件，填入以下内容
```
Host github.com
    User git
    Hostname github.com
    PreferredAuthentications publickey
    IdentityFile /home/user/.ssh/my_key
```

# 6. 克隆ledger仓库

# 7. 在bash中运行的相关配置

```
echo "export ZENO_OUTPUT_DIR=~/root/ledger" >> ~/.bashrc
echo "export LEDGER_DIR=~/root/ledger" >> ~/.bashrc
echo "eval $(ssh-agent)" >> ~/.bashrc
source ~/.bashrc

```

# 8. 在crontab中定时作业的相关配置

使用命令“crontab -e”，并在提示的编辑器中输入如下配置，按“Esc”+“:”+“q”退出编辑。
```
ZENO_OUTPUT_DIR=/root/zeno_output
LEDGER_DIR=/root/zeno_output

# 每天UTC时间18点（北京时间凌晨2点）0分、10分、20分依次执行任务。
0 18 * * * bash ~/zeno/collector/run.sh
10 18 * * * bash ~/zeno/analyzer/run.sh
20 18 * * * rclone sync ${ZENO_OUTPUT_DIR} gdrive: --bwlimit=8.5M --progress
```

提示：使用“date”命令查看当前时间，注意区分时间格式为“UTC”还是“CST”，后者是北京时间。
