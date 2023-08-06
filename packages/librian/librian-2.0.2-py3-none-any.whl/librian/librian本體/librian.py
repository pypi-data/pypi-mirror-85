import os
import logging

from . import 環境
from . import librian虛擬機
from . import 窗口

from .librian虛擬機 import 虛擬機環境


def ember(project, 編寫模式=False):
    logging.info('librian_main啓動。')
    librian虛擬機.虛擬機環境.加載配置(project)
    環境.導入全局配置({
        '編寫模式': 編寫模式
    })

    os.makedirs(f'{虛擬機環境.工程路徑}/存檔資料/手動存檔', exist_ok=True)
        
    app = 窗口.啓動app()
    app.MainLoop()
