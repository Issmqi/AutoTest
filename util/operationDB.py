# -*- coding:utf-8 -*-
from sshtunnel import SSHTunnelForwarder
import pymysql.cursors

with SSHTunnelForwarder(
        ('52.80.128.243', 22),  # B机器的配置
        ssh_username="centos",
        ssh_pkey='D:/macys/Operation/macys-uat.pem',
        remote_bind_address=(
        'macys-uat-mysql-new.ck31axgwtpkd.rds.cn-north-1.amazonaws.com.cn', 13306)) as server:  # A机器的配置

    connection = pymysql.connect(
        host='127.0.0.1',  # 此处必须是是127.0.0.1
        port=server.local_bind_port,
        user='macys',
        passwd='4g8*V#my',
        db='wmb2c'
    )
    with connection.cursor() as cursor:
        cursor.execute("select * from tbl_um_buyer")
        print(cursor.fetchone())
    connection.commit()


