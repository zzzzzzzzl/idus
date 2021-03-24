# -*- coding: utf-8 -*-

import subprocess as sp


# 模拟Linux命令行
def cmd(command):
    subp = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, encoding="utf-8", close_fds=True)
    subp.wait(100)
    if subp.poll() == 0:
        cmd_res = subp.communicate()[0]
        # 清空std流程
        if subp.stdin:
            subp.stdin.close()
        if subp.stdout:
            subp.stdout.close()
        if subp.stderr:
            subp.stderr.close()
        try:
            subp.kill()
        except OSError:
            pass
        return cmd_res
    else:
        print(command + " 执行失败")
