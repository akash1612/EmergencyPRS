from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename
app=Flask(__name__)
UPLOAD_FOLDER = 'static/image'
#ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patient',methods=['GET'])
def patient():
    return render_template('patient.html')

@app.route('/patient/register',methods=['POST','GET'])
def getpatientBasic():
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method == 'POST':
        p_id=request.form['p_id']
        name=request.form['name']
        age=request.form['age']
        sex=request.form['sex']
        b_gp=request.form['b_gp']
        contact=request.form['contact']
        e_co=request.form['e_co']
        image = request.files['image']
        filename=""
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename=filename
        cur.execute("insert into patient values(?,?,?,?,?,?,?,?)",(p_id,name,age,sex,b_gp,contact,e_co,imagename))
        con.commit()
        return redirect(url_for('getdetails',pid=p_id))
    return render_template('register.html')


@app.route('/patient/getdetails/<pid>')
def getdetails(pid):
    return render_template('getdetails.html',p_id=pid)

@app.route('/patient/getdiseases/<pid>',methods=['GET','POST'])
def getdiseases(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        name=request.form['name']
        date=request.form['date']
        duration=request.form['duration']
        cur.execute("insert into disease(p_id,name,date,duration) values(?,?,?,?)",(p_id,name,date,duration))
        con.commit()
        d_id=cur.execute("select max(d_id) from disease").fetchall()[0][0]
        return redirect(url_for('getdiseasedetails',pid=p_id,did=d_id))
    return render_template('getdiseases.html')

@app.route('/patient/getdiseasedetails/<pid>/<did>')
def getdiseasedetails(pid,did):
    con=sql.connect
    return render_template('getdiseasedetails.html',p_id=pid,d_id=did)

@app.route('/patient/getmedications/<pid>/<did>',methods=['GET','POST'])
def getmedications(pid,did):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        d_id=did
        name=request.form['name']
        dose=request.form['dose']
        duration=request.form['duration']
        reaction=request.form['reaction']
        cur.execute("insert into medication(d_id,p_id,name,dose,duration,reaction) values(?,?,?,?,?,?)",(d_id,p_id,name,dose,duration,reaction))
        con.commit()
        return redirect(url_for('getdiseasedetails',pid=p_id,did=d_id))
    return render_template('getmedications.html')    

@app.route('/patient/getdiseasereports/<pid>/<did>')
def getdiseasereports(pid,did):
    return "upload disease reports"


@app.route('/patient/getsurgeries/<pid>',methods=['GET','POST'])
def getsurgeries(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        part=request.form['part']
        type=request.form['type']
        purpose=request.form['purpose']
        date=request.form['date']
        recovery=request.form['recovery']
        cur.execute("insert into surgeries(p_id,part,type,purpose,date,recovery) values(?,?,?,?,?,?)",(p_id,part,type,purpose,date,recovery))
        con.commit()
        s_id=cur.execute("select max(s_id) from surgeries").fetchall()[0][0]
        return redirect(url_for('getsurgerydetails',pid=p_id,sid=s_id))
    return render_template('getsurgeries.html')

@app.route('/patient/getsurgerydetails/<pid>/<sid>')
def getsurgerydetails(pid,sid):
    return render_template('getsurgerydetails.html',p_id=pid,s_id=sid)

@app.route('/patient/getsurgerydrugs/<pid>/<sid>',methods=['GET','POST'])
def getsurgerydrugs(pid,sid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        s_id=sid
        name=request.form['name']
        dose=request.form['dose']
        duration=request.form['duration']
        reaction=request.form['reaction']
        cur.execute("insert into drugs(s_id,p_id,name,dose,duration,reaction) values(?,?,?,?,?,?)",(s_id,p_id,name,dose,duration,reaction))
        con.commit()
        return redirect(url_for('getsurgerydetails',pid=p_id,sid=s_id))
    return render_template('getsurgerydrugs.html')


@app.route('/patient/gettransfusions/<pid>',methods=['GET','POST'])
def gettransfusions(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        date=request.form['date']
        units=request.form['units']
        details=request.form['details']
        cur.execute("insert into transfusions(p_id,date,units,details) values(?,?,?,?)",(p_id,date,units,details))
        con.commit()
        return redirect(url_for('getdetails',pid=p_id))
    return render_template('gettransfusions.html')

@app.route('/patient/getfamilyhistory/<pid>',methods=['GET','POST'])
def getfamilyhistory(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        disease=request.form['disease']
        relation=request.form['relation']
        cur.execute("insert into history(p_id,disease,relation) values(?,?,?)",(p_id,disease,relation))
        con.commit()
        return redirect(url_for('getdetails',pid=p_id))
    return render_template('getfamilyhistory.html')

@app.route('/patient/getreports/<pid>')
def getreports(pid):
    return "upload reports"

@app.route('/patient/login',methods=['GET','POST'])
def patientlogin():
    if request.method=='POST':
        p_id=request.form['p_id']
        return redirect(url_for('patientbasic',pid=p_id))
    return render_template('login.html')

@app.route('/patient/basic/<pid>')
def patientbasic(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from patient where p_id=(?)",(p_id,)).fetchone()
    if not res :
        return "<h1>Aadhar number not found</h1>"
    else :    
        return render_template('patientbasic.html',res=res,p_id=pid)

@app.route('/patient/updatebasic/<pid>',methods=['GET','POST'])
def updatebasic(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    res=cur.execute("select * from patient where p_id=(?)",(pid,)).fetchone()
    if request.method=='POST':
        p_id=pid
        name=request.form['name']
        age=request.form['age']
        sex=request.form['sex']
        b_gp=request.form['b_gp']
        contact=request.form['contact']
        e_co=request.form['e_co']
        cur.execute("update patient set name=(?),age=(?),sex=(?),b_gp=(?),contact=(?),e_contact=(?) where p_id=(?)",(name,age,sex,b_gp,contact,e_co,p_id))
        con.commit()
        return redirect(url_for('patientbasic',pid=p_id))
    return render_template('updatebasic.html',res=res)

@app.route('/patient/deletebasic/<pid>')
def deletebasic(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    cur.execute("pragma foreign_keys=ON")
    cur.execute("delete from patient where p_id=(?)",(pid,))
    con.commit()
    return redirect(url_for('index'))


@app.route('/patient/diseases/<pid>')
def patientdiseases(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from disease where p_id=(?)",(p_id,)).fetchall()
    return render_template('patientdiseases.html',res=res,p_id=p_id)

@app.route('/patient/adddiseases/<pid>',methods=['GET','POST'])
def adddiseases(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        name=request.form['name']
        date=request.form['date']
        duration=request.form['duration']
        cur.execute("insert into disease(p_id,name,date,duration) values(?,?,?,?)",(p_id,name,date,duration))
        con.commit()
        return redirect(url_for('patientdiseases',pid=p_id))   
    return render_template('getdiseases.html')

@app.route('/patient/updatediseases/<pid>/<did>',methods=['GET','POST'])
def updatediseases(pid,did):
    con=sql.connect('database.db')
    cur=con.cursor()
    res=cur.execute("select * from disease where d_id=(?)",(did,)).fetchone()
    if request.method=='POST':
        p_id=pid
        d_id=did
        name=request.form['name']
        date=request.form['date']
        duration=request.form['duration']
        cur.execute("update disease set name=(?),date=(?),duration=(?) where d_id=(?)",(name,date,duration,d_id))
        con.commit()
        return redirect(url_for('patientdiseases',pid=p_id)) 
    return render_template('updatediseases.html',res=res)

@app.route('/patient/deletediseases/<pid>/<did>')
def deletediseases(pid,did):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    cur.execute("pragma foreign_keys=ON")
    cur.execute("delete from disease where d_id=(?)",(did,))
    con.commit()
    return redirect(url_for('patientdiseases',pid=p_id))

@app.route('/patient/medication/<pid>/<did>')
def patientmedication(pid,did):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    d_id=did
    res=cur.execute("select * from medication where d_id=(?)",(d_id)).fetchall()
    return render_template('patientmedication.html',res=res,p_id=p_id,d_id=d_id)

@app.route('/patient/addmedication/<pid>/<did>',methods=['GET','POST'])
def addmedication(pid,did):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    d_id=did
    if request.method=='POST':
        name=request.form['name']
        dose=request.form['dose']
        duration=request.form['duration']
        reaction=request.form['reaction']
        cur.execute("insert into medication(d_id,p_id,name,dose,duration,reaction) values(?,?,?,?,?,?)",(d_id,p_id,name,dose,duration,reaction))
        con.commit()
        return redirect(url_for('patientmedication',pid=p_id,did=d_id))
    return render_template('getmedications.html')

@app.route('/patient/updatemedication/<pid>/<did>/<mid>',methods=['GET','POST'])
def updatemedication(pid,did,mid):
    con=sql.connect('database.db')
    cur=con.cursor()
    res=cur.execute("select * from medication where m_id=(?)",(mid,)).fetchone()
    if request.method=='POST':
        p_id=pid
        d_id=did
        m_id=mid
        name=request.form['name']
        dose=request.form['dose']
        duration=request.form['duration']
        reaction=request.form['reaction']
        cur.execute("update medication set name=(?),dose=(?),duration=(?),reaction=(?) where m_id=(?)",(name,dose,duration,reaction,m_id))
        con.commit()
        return redirect(url_for('patientmedication',pid=p_id,did=d_id))
    return render_template('updatemedication.html',res=res)

@app.route('/patient/deletemedication/<pid>/<did>/<mid>')
def deletemedication(pid,did,mid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    d_id=did
    cur.execute('delete from medication where m_id=(?)',(mid,))
    con.commit()
    return redirect(url_for('patientmedication',pid=p_id,did=d_id))


@app.route('/patient/surgeries/<pid>')
def patientsurgeries(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from surgeries where p_id=(?)",(p_id,)).fetchall()
    # print(res)
    time={}
    i=0
    for t in res:
        # print(t)
        time[i]=t[6]
        i+=1
    print(time)
    return render_template('patientsurgeries.html',res=res,p_id=p_id,time=time)

@app.route('/patient/addsurgeries/<pid>',methods=['GET','POST'])
def addsurgeries(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        part=request.form['part']
        type=request.form['type']
        purpose=request.form['purpose']
        date=request.form['date']
        recovery=request.form['recovery']
        cur.execute("insert into surgeries(p_id,part,type,purpose,date,recovery) values(?,?,?,?,?,?)",(p_id,part,type,purpose,date,recovery))
        con.commit()
        return redirect(url_for('patientsurgeries',pid=p_id))
    return render_template('getsurgeries.html')

@app.route('/patient/updatesurgeries/<pid>/<sid>',methods=['GET','POST'])
def updatesurgeries(pid,sid):
    con=sql.connect('database.db')
    cur=con.cursor()
    res=cur.execute("select * from surgeries where s_id=(?)",(sid,)).fetchone()
    if request.method=='POST':
        p_id=pid
        s_id=sid
        part=request.form['part']
        type=request.form['type']
        purpose=request.form['purpose']
        date=request.form['date']
        recovery=request.form['recovery']
        cur.execute("update surgeries set part=(?),type=(?),purpose=(?),date=(?),recovery=(?) where s_id=(?)",(part,type,purpose,date,recovery,s_id,))
        con.commit()
        return redirect(url_for('patientsurgeries',pid=p_id))
    return render_template('updatesurgeries.html',res=res)

@app.route('/patient/deletesurgeries/<pid>/<sid>')
def deletesurgeries(pid,sid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    s_id=sid
    cur.execute("pragma foreign_keys=ON")
    cur.execute("delete from surgeries where s_id=(?)",(s_id,))
    con.commit()
    return redirect(url_for('patientsurgeries',pid=p_id))

@app.route('/patient/surgerydrugs/<pid>/<sid>')
def patientdrugs(pid,sid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    s_id=sid
    res=cur.execute("select * from drugs where s_id=(?)",(s_id)).fetchall()
    return render_template('surgerydrugs.html',res=res,p_id=p_id,s_id=s_id)

@app.route('/patient/adddrugs/<pid>/<sid>',methods=['GET','POST'])
def adddrugs(pid,sid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    s_id=sid
    if request.method=='POST':
        name=request.form['name']
        dose=request.form['dose']
        duration=request.form['duration']
        reaction=request.form['reaction']
        cur.execute("insert into drugs(s_id,p_id,name,dose,duration,reaction) values(?,?,?,?,?,?)",(s_id,p_id,name,dose,duration,reaction))
        con.commit()
        return redirect(url_for('patientdrugs',pid=p_id,sid=s_id))
    return render_template('getsurgerydrugs.html')

@app.route('/patient/updatedrugs/<pid>/<sid>/<sdid>',methods=['GET','POST'])
def updatedrugs(pid,sid,sdid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    s_id=sid
    sd_id=sdid
    res=cur.execute("select * from drugs where sd_id=(?)",(sd_id,)).fetchone()
    if request.method=='POST':
        name=request.form['name']
        dose=request.form['dose']
        duration=request.form['duration']
        reaction=request.form['reaction']
        cur.execute("update drugs set name=(?),dose=(?),duration=(?),reaction=(?) where sd_id=(?)",(name,dose,duration,reaction,sd_id))
        con.commit()
        return redirect(url_for('patientdrugs',pid=p_id,sid=s_id))
    return render_template('updatedrugs.html',res=res)


@app.route('/patient/deletedrugs/<pid>/<sid>/<sdid>')
def deletedrugs(pid,sid,sdid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    s_id=sid
    sd_id=sdid
    cur.execute("delete from drugs where sd_id=(?)",(sd_id,))
    con.commit()
    return redirect(url_for('patientdrugs',pid=p_id,sid=s_id))

@app.route('/patient/transfusions/<pid>')
def patienttransfusions(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from transfusions where p_id=(?)",(p_id,)).fetchall()
    return render_template('patienttransfusions.html',res=res,p_id=p_id)

@app.route('/patient/addtransfusions/<pid>',methods=['GET','POST'])
def addtransfusions(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    if request.method=='POST':
        date=request.form['date']
        units=request.form['units']
        details=request.form['details']
        cur.execute("insert into transfusions(p_id,date,units,details) values(?,?,?,?)",(p_id,date,units,details))
        con.commit()
        return redirect(url_for('patienttransfusions',pid=p_id))
    return render_template('gettransfusions.html')

@app.route('/patient/updatetransfusions/<pid>/<tid>',methods=['GET','POST'])
def updatetransfusions(pid,tid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    t_id=tid
    res=cur.execute('select * from transfusions where t_id=(?)',(t_id,)).fetchone()
    if request.method=='POST':
        date=request.form['date']
        units=request.form['units']
        details=request.form['details']
        cur.execute("update transfusions set date=(?),units=(?),details=(?) where t_id=(?)",(date,units,details,t_id))
        con.commit()
        return redirect(url_for('patienttransfusions',pid=p_id))
    return render_template('updatetransfusions.html',res=res)

@app.route('/patient/deletetransfusions/<pid>/<tid>')
def deletetransfusions(pid,tid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    t_id=tid
    cur.execute("delete from transfusions where t_id=(?)",(t_id,))
    con.commit()
    return redirect(url_for('patienttransfusions',pid=p_id))


@app.route('/patient/familyhistory/<pid>')
def patientfamilyhistory(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from history where p_id=(?)",(p_id,))
    return render_template('patienthistory.html',res=res,p_id=p_id)

@app.route('/patient/addhistory/<pid>',methods=['GET','POST'])
def addhistory(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    if request.method=='POST':
        p_id=pid
        disease=request.form['disease']
        relation=request.form['relation']
        cur.execute("insert into history(p_id,disease,relation) values(?,?,?)",(p_id,disease,relation))
        con.commit()
        return redirect(url_for('patientfamilyhistory',pid=p_id))
    return render_template('getfamilyhistory.html')

@app.route('/patient/updatehistory/<pid>/<fid>',methods=['GET','POST'])
def updatehistory(pid,fid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    f_id=fid
    res=cur.execute("select * from history where f_id=(?)",(f_id,)).fetchone()
    if request.method=='POST':
        disease=request.form['disease']
        relation=request.form['relation']
        cur.execute("update history set disease=(?),relation=(?) where f_id=(?)",(disease,relation,f_id))
        con.commit()
        return redirect(url_for('patientfamilyhistory',pid=p_id))
    return render_template('updatehistory.html',res=res)

@app.route('/patient/deletehistory/<pid>/<fid>')
def deletehistory(pid,fid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    f_id=fid
    cur.execute("delete from history where f_id=(?)",(f_id,))
    con.commit()
    return redirect(url_for('patientfamilyhistory',pid=p_id))

@app.route('/doctor',methods = ['GET','POST'])
def doctor():
    if request.method == 'POST' :
        p_id = request.form['p_id']
        return redirect(url_for('viewbasic',pid=p_id))
    return render_template('login.html')

@app.route('/doctor/viewbasic/<pid>')
def viewbasic(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from patient where p_id=(?)",(p_id,)).fetchone()
    if not res :
        return "<h1>Aadhar number not found</h1>"
    else :    
        return render_template('viewbasic.html',res=res,p_id=pid)

@app.route('/doctor/viewdiseases/<pid>')
def viewdiseases(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from disease where p_id=(?)",(p_id,)).fetchall()
    return render_template('viewdiseases.html',res=res,p_id=p_id)

@app.route('/doctor/viewsurgeries/<pid>')
def viewsurgeries(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from surgeries where p_id=(?)",(p_id,)).fetchall()
    return render_template('viewsurgeries.html',res=res,p_id=p_id)

@app.route('/doctor/viewtransfusions/<pid>')
def viewtransfusions(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from transfusions where p_id=(?)",(p_id,)).fetchall()
    return render_template('viewtransfusions.html',res=res,p_id=p_id)

@app.route('/doctor/viewfamilyhistory/<pid>')
def viewfamilyhistory(pid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    res=cur.execute("select * from history where p_id=(?)",(p_id,))
    return render_template('viewhistory.html',res=res,p_id=p_id)

@app.route('/doctor/viewmedications/<pid>/<did>')
def viewmedications(pid,did):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    d_id=did
    res=cur.execute("select * from medication where d_id=(?)",(d_id)).fetchall()
    return render_template('viewmedication.html',res=res,p_id=p_id,d_id=d_id)

@app.route('/doctor/viewdrugs/<pid>/<sid>')
def viewdrugs(pid,sid):
    con=sql.connect('database.db')
    cur=con.cursor()
    p_id=pid
    s_id=sid
    res=cur.execute("select * from drugs where s_id=(?)",(s_id)).fetchall()
    return render_template('viewdrugs.html',res=res,p_id=p_id,s_id=s_id)

if __name__=="__main__":
    app.run(debug=True)