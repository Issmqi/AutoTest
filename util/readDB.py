# -*- coding: utf-8 -*-
# !/bin/bash
import peewee
db=peewee.MySQLDatabase(
    host="192.168.41.17",
    user="occ01",
    password="occ01",
    database="occtest"
)
