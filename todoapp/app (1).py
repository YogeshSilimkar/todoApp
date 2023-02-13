from flask import Flask,render_template,request,redirect,url_for
import pymysql

app = Flask(__name__)

db=None
cur=None

def connectDB():
    global db;
    global cur;
    db = pymysql.connect(host='localhost',
		user='root',
		password='',
		database='python')
    #create cursor
    cur = db.cursor()

def disconnectDB():
    db.close()

def insertRecords(taskname,status):
    connectDB()
    insertquery='insert into todo(task,status) values("{}","{}")'.format(taskname,status)
    cur.execute(insertquery)
    db.commit()
    disconnectDB()

def readAllRecords():
    connectDB()
    selectquery="select * from todo";
    cur.execute(selectquery)
    result=cur.fetchall()
    disconnectDB()
    return result

def deleteRecords(tid):
    connectDB()
    deletequery="delete from todo where id='{}'".format(tid)
    cur.execute(deletequery)
    db.commit()
    disconnectDB()

def readOneRecord(tid):
    connectDB()
    selectquery="select * from todo where id='{}'".format(tid)
    cur.execute(selectquery)
    result=cur.fetchone()
    disconnectDB()
    return result

def updateRecords(tid,taskname,status):
    connectDB()
    updatequery="update todo set task='{}',status='{}' where id='{}'".format(taskname,status,tid)
    cur.execute(updatequery)
    db.commit()
    disconnectDB()

@app.route('/')
def index():
    data=readAllRecords()
    print(data)
    return render_template('index.html',senddata=data)

@app.route('/update/<tid>',methods=['GET','POST'])
def update(tid):
    if request.method=='POST':
        taskname=request.form['task']
        status=request.form['status']
        updateRecords(tid,taskname,status)
        return redirect(url_for('index'))
    else:
        data=readOneRecord(tid)
        return render_template('update.html',senddata=data)

@app.route('/delete/<tid>')
def delete(tid):
    deleteRecords(tid)
    return redirect(url_for('index'))

@app.route('/insert',methods=['GET','POST'])
def insert():
    #Only for GET
    #taskname=request.args.get('task')
    #status=request.args.get('status')
    #insertRecords(taskname,status)
    #print(taskname,status)
    #Only for POST
    if request.method=='POST':
        taskname=request.form['task']
        status=request.form['status']
        insertRecords(taskname,status)
        return redirect(url_for('index'))
    else:
        return render_template('insert.html')


if __name__=='__main__':
    app.run(debug=True)
