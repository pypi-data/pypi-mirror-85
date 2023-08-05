onepath = r"E:\更新数据\db3\zt_wf_qk.20200331_000.db3"

import sqlite3


def dataMerge(inpath, attachpath):
    """
    合并两个db3
    :param inpath:
    :param attachpath:
    :return:
    """
    conn = sqlite3.connect(inpath)
    conn.text_factory = str
    cur = conn.cursor()
    attach = 'attach database "' + attachpath + '" as w;'
    sql1 = 'insert into modify_title_info_zt select * from w.modify_title_info_zt;'
    cur.execute(attach)
    cur.execute(sql1)
    conn.commit()
    cur.close()
    conn.close()


for i in range(1, 10):
    attachpath = r"E:\更新数据\db3\zt_wf_qk.20200331_00%s.db3" % (str(i))
    dataMerge(onepath, attachpath)
    print(attachpath)

# attachpath = r"\\192.168.31.177\down_data\cnkiwanfang\zt_wf_qk_20200323\db3\zt_wf_qk_20200323_0002.db3"
# dataMerge(onepath, attachpath)
# print(attachpath)


