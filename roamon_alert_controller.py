# encoding: UTF-8

# Copyright (c) 2019-2020 Japan Network Information Center ("JPNIC")
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute and/or sublicense of
# the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# 引数の処理はここを参考にした：https://qiita.com/oohira/items/308bbd33a77200a35a3d

import argparse
import roamon_alert_watcher
import roamon_alert_daemon
import roamon_alert_mail
import roamon_alert_db
import logging
from pyfiglet import Figlet
import configparser

# ログ関係の設定 (適当)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# コンフィグファイルのロード
config = configparser.ConfigParser()
config.read('config.ini')
config_roamon_verify = config["roamon-verify"]
config_roamon_alert = config["roamon-alert"]

# ファイルの保存先
dir_path_data = config_roamon_verify["dir_path_data"]
file_path_vrps = config_roamon_verify["file_path_vrps"]
file_path_rib = config_roamon_verify["file_path_rib"]

# デーモンの設定
log_path = config_roamon_alert["log_path"]  # "/tmp/alertd.log"
pid_file_path = config_roamon_alert["pid_file_path"]  # "/var/run/alertd.pid"

# メール関連の設定
smtp_server_address = config_roamon_alert["smtp_server_address"]
smtp_server_port = int(config_roamon_alert["smtp_server_port"])
sender_email_address = config_roamon_alert["sender_email_address"]

# 監視間隔
watch_interval = int(config_roamon_alert["watch_interval"])

# DBの設定
db_host = config_roamon_alert["db_host"]
db_port = int(config_roamon_alert["db_port"])
db_name = config_roamon_alert["db_name"]
db_user_name = config_roamon_alert["db_user_name"]
db_password = config_roamon_alert["db_password"]

# ロゴの描画
f = Figlet(font='slant')
print(f.renderText('roamon-alert'))

mailer = roamon_alert_mail.MailSender(smtp_server_address, smtp_server_port, sender_email_address)
db_controller = roamon_alert_db.RoamonAlertDb(db_host, db_port, db_name, db_user_name, db_password)
watcher = roamon_alert_watcher.RoamonAlertWatcher(dir_path_data, file_path_vrps, file_path_rib,
                                                  mailer, db_controller)


# 連絡先追加の処理を記述するコールバック関数 (以下同じ)
def command_add(args):
    watcher.add_contact_info_to_list(args.type, args.dest, args.prefixes, args.asns)


def command_delete(args):
    watcher.delete_contact_info_from_list(args.type, args.dest, args.prefixes, args.asns)


# 連絡先のリストアップ
def command_list(args):
    watcher.print_contact_lists()


# デーモンの開始と終了
def command_daemon(args):
    alertd = roamon_alert_daemon.RoamonAlertDaemon(pid_file_path, log_path, watcher, watch_interval)
    # 起動
    if args.start:
        alertd.start()

    # 終了
    if args.stop:
        alertd.stop()


def command_help(args):
    print(parser.parse_args([args.command, '--help']))
    # TODO: ヘルプをうまくやる


# コマンドラインパーサーを作成
parser = argparse.ArgumentParser(description='ROA - BGP Diff command !')
subparsers = parser.add_subparsers()

# add コマンドの parser を作成
parser_add = subparsers.add_parser('add', help="see `get -h`. It's command to add contact info.")
parser_add.add_argument('--asns', nargs="*", help='specify watch ASN')
parser_add.add_argument('--prefixes', nargs="*", help='specify watch ip prefix')
parser_add.add_argument('--type', default="email", help='specify contact type, such as email or slack.')
parser_add.add_argument('--dest', default="DUMMY_DEST@example.com",
                        help='specify contact dest, such as e-mail address or Slack info')
parser_add.set_defaults(handler=command_add)

# delete コマンドの parser を作成
parser_add = subparsers.add_parser('delete', help="see `get -h`. It's command to delete contact info.")
parser_add.add_argument('--asns', nargs="*", help='specify watch ASN')
parser_add.add_argument('--prefixes', nargs="*", help='specify watch ip prefix')
parser_add.add_argument('--type', default="email", help='specify contact type, such as email or slack.')
parser_add.add_argument('--dest', default="DUMMY_DEST@example.com",
                        help='specify contact dest, such as e-mail address or Slack info')
parser_add.set_defaults(handler=command_delete)

# list コマンドの parser を作成
parser_list = subparsers.add_parser('list', help="see `get -h`. It's command to list up contact info.")
parser_list.set_defaults(handler=command_list)

# daemonコマンドのパーサを作成
parser_daemon = subparsers.add_parser('daemon', help="see `get -h`. It's command to control daemon.")
parser_daemon.add_argument('--start', action='store_true', help='start daemon (DEFAULT)')
parser_daemon.add_argument('--stop', action='store_true', help='stop daemon')
parser_daemon.set_defaults(handler=command_daemon)

# help コマンドの parser を作成
parser_help = subparsers.add_parser('help', help='see `help -h`')
parser_help.add_argument('command', help='command name which help is shown')
parser_help.set_defaults(handler=command_help)

# コマンドライン引数をパースして対応するハンドラ関数を実行
args = parser.parse_args()
if hasattr(args, 'handler'):
    args.handler(args)
else:
    # 未知のサブコマンドの場合はヘルプを表示
    parser.print_help()
