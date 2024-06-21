# This .py file stores Python functions used in the system
import pymysql
import datetime
import random
import json
import numpy as np

# Database parameters
host = '127.0.0.1'
port = 3306
user = 'root'
password = '1234567'
database = 'eyeweb'

# Login page
# Get password by user id
def get_password_by_id(id):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE Uid = '%s'" % (id)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def get_task_list(username, datatype):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    # Show all data by default
    if datatype == 'all':
        sql = '''
        SELECT a.Aid, a.Atitle, a.Alength, t.readtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid AND t.Uid = '%s'
        ORDER BY t.readtime ASC
        ''' % (username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # Show annotated data
    elif datatype == 'true':
        sql = '''
        SELECT a.Aid, a.Atitle, a.Alength, t.readtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid AND t.Uid = '%s' AND t.readtime IS NOT NULL
        ORDER BY t.readtime ASC
        ''' % (username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # Show unannotated data
    elif datatype == 'false':
        sql = '''
        SELECT a.Aid, a.Atitle, a.Alength, t.readtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid AND t.Uid = '%s' AND t.readtime IS NULL
        ORDER BY t.readtime ASC
        ''' % (username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def get_task_list_admin(datatype):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    # Show all data by default
    if datatype == 'all':
        sql = '''
        SELECT a.Aid, t.Uid, a.Atitle, t.readtime, t.duringtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid
        ORDER BY t.readtime ASC
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # Show annotated data
    elif datatype == 'true':
        sql = '''
        SELECT a.Aid, t.Uid, a.Atitle, t.readtime, t.duringtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid AND t.readtime IS NOT NULL
        ORDER BY t.readtime ASC
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # Show unannotated data
    elif datatype == 'false':
        sql = '''
        SELECT a.Aid, t.Uid, a.Atitle, t.readtime, t.duringtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid AND t.readtime IS NULL
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


# Check completion status of a task based on uid and aid (0 for incomplete, 1 for complete)
def check_state(uid, aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    sql = '''
    SELECT t.state
    FROM task AS t
    WHERE t.Uid = '%s' AND t.Aid = '%s'  
    ''' % (uid, aid)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


# Get information of sentences related to aid ('1', 'I am the first sentence of the first article.')
def get_sentence(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    sql = '''
    SELECT Sid, Sentence
    FROM sentence 
    WHERE Aid = '%s'  
    ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)
    # Sort sentences by sentence number
    result = bubble_sort(result)
    sentence = []
    for i in range(0, len(result)):
        sentence.append(result[i][1])
    return sentence


# Get the list of sentence IDs corresponding to article
def get_sentence_id(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    sql = '''
    SELECT Sid, Sentence
    FROM sentence 
    WHERE Aid = '%s'  
    ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)
    # Sort sentences by sentence number
    result = bubble_sort(result)
    sentence_id = []
    for i in range(0, len(result)):
        sentence_id.append(result[i][0])
    return sentence_id


# Bubble sort sentence IDs to determine sentence order
def bubble_sort(sentence):
    for j in range(0, len(sentence) - 1):  # Loop through the entire list for sorting
        for i in range(0, len(sentence) - 1 - j):
            # Traverse each element from start to end, one pass to sort one number
            temple = 0
            if sentence[i][0] > sentence[i + 1][0]:
                # Need to compare with the next element, so i only needs to go to len(alist) - 1 - j
                # sentence[i],sentence[i + 1] = sentence[i + 1],sentence[i]
                temple = sentence[i]
                sentence[i] = sentence[i + 1]
                sentence[i + 1] = temple
    return sentence


# Get article title from artical
def get_title(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    sql = '''
    SELECT Atitle
    FROM artical 
    WHERE Aid = '%s'  
    ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchone()
    result = result[0]
    return result


# Modify information in task table
def change_state(uid, aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    time = datetime.datetime.now()
    print(time)
    try:
        sql_up = '''
        UPDATE task
        SET state ='1', readtime = '%s'
        WHERE Uid = '%s' AND Aid = '%s'
        ''' % (time, uid, aid)
        cursor.execute(sql_up)
        db.commit()
    except:
        print("Failed to modify data, please return to the login page")


# Calculate duringtime and save it to database
# 1. Get current time
# 2. Get readtime from database
# 3. Calculate time difference between them
# 4. Insert result
def get_duringtime(uid, aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    # 1.
    time = datetime.datetime.now()
    # 2.
    sql = '''
    SELECT readtime
    FROM task 
    WHERE Uid = '%s' AND Aid = '%s'  
    ''' % (uid, aid)
    cursor.execute(sql)
    readtime = cursor.fetchone()
    readtime = readtime[0]
    # 3. Calculate time difference (in seconds）
    duringtime = time - readtime
    duringtime = duringtime.seconds
    # Modify data in the table
    try:
        sql_up = '''
        UPDATE task
        SET duringtime = '%s'
        WHERE Uid = '%s' AND Aid = '%s'
        ''' % (duringtime, uid, aid)
        cursor.execute(sql_up)
        db.commit()
    except:
        print("Failed to modify data, please return to the login page")


# Reset information related to task
def reset_task_info(a_id, u_id):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    state = 0
    # Print the task table before modification
    sql = '''
    SELECT *
    FROM task 
    WHERE Uid = '%s' AND Aid = '%s'  
    ''' % (u_id, a_id)
    cursor.execute(sql)
    result_be = cursor.fetchone()
    print(result_be)
    try:
        # Modify information in the task table (successful modification）
        sql_reset = '''
        UPDATE task
        SET state ='0', readtime = NULL, duringtime = NULL
        WHERE Uid = '%s' AND Aid = '%s'
        ''' % (u_id, a_id)
        cursor.execute(sql_reset)
        db.commit()
        # Delete relevant data in eyedata table
        sql_delete = '''
            DELETE a
            FROM eyedata AS a, sentence AS b
            WHERE  a.Sid = b.Sid And b.Aid = '%s' And a.Uid = '%s'
            '''% (a_id,u_id)
        cursor.execute(sql_delete)
        db.commit()
        state = 1
        sql = '''
                SELECT *
                FROM task 
                WHERE Uid = '%s' AND Aid = '%s'  
                ''' % (u_id, a_id)
        cursor.execute(sql)
        result_af = cursor.fetchone()
        print(result_af)
        return state
    except:
        print("数据修改失败,请返回登陆页面")


def save_eyedata_info(sid,uid,wordid,x,y,time):
    #连接数据库
    state = 0
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    # print(sid)
    sid = sid[1:-1]
    print(sid)
    #将数据存入数据库
    try:
        sql_in = '''
            INSERT  INTO  eyedata
            VALUES  ('%s','%s','%s','%s','%s','%s')
            '''% (sid,uid,wordid,time,x,y)
        cursor.execute(sql_in)
        db.commit()
        state = 1
        return state
    except:
        print("眼动数据保存失败！")
        return state


#获取artical表中的文章选项
def get_options(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    sql = '''
            SELECT options
            FROM artical 
            WHERE Aid = '%s'  
            ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchone()
    result = result[0]
    #结果为”信息熵；主题标引；服务；“，要对其进行分割成数组
    return result


def exchange_options(options):
    #在0-2中间获取一个随机数字
    a = random.randint(0, 2)
    b = random.randint(0, 2)
    temp = options[a]
    options[a] = options[b]
    options[b] = temp
    return options


#保存用户的验证问题答案
def save_u_answer(aid,uid,option):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    state = 0
    #打印修改前的task表
    sql = '''
            SELECT *
            FROM task 
            WHERE Uid = '%s' AND Aid = '%s'  
            ''' % (uid, aid)
    cursor.execute(sql)
    result_be= cursor.fetchone()
    print(result_be)
    if result_be[6] != None:
        return state
    else:
        try:
            time = datetime.datetime.now()
            # Update information in the task table (update successful)
            sql_answer = '''
                UPDATE task
                SET u_answer = '%s',a_time = '%s'
                WHERE  Uid = '%s' And Aid = '%s' 
                '''% (option,time,uid,aid)
            cursor.execute(sql_answer)
            db.commit()
            state = 1
            sql = '''
                SELECT *
                FROM task 
                WHERE Uid = '%s' AND Aid = '%s'  
                ''' % (uid, aid)
            cursor.execute(sql)
            result_af = cursor.fetchone()
            print(result_af)
            return state
        except:
            print("Data modification failed, please return to the login page")
            return state

# Test function functionality
if __name__ == '__main__':
    # 
    # a = '2'
    # b = '2'
    # get_duringtime(a,b)
    # test = (('4', 'I am the second sentence of the second article, I am the second sentence of the second article.'), ('3', 'I am the first sentence of the second article.'), ('5', 'I am the third sentence of the second article!'))
    # test = list(test)
    # bubble_sort(test)
    # time = datetime.datetime.now()
    # strftime("%Y-%m-%d %H:%M:%S.%L")
    # Testing if string can be accessed by index
    aid = "001"
    uid = "202201"
    option = "test"

    state = save_u_answer(aid, uid, option)
    print(state)
    # options = ["First", "Second", "Third"]
    # exchange_options(options)
