import sqlite3 as sql
con=sql.connect('database.db')
cur=con.cursor()

cur.execute('''create table if not exists patient
        (p_id number,name text,age number,sex text,b_gp text,contact number,e_contact number,image text,constraint pk1 primary key(p_id))''')

cur.execute('''create table if not exists disease
            (d_id integer primary key autoincrement,p_id number,name text,date text,duration number,constraint fk1 foreign key(p_id) references patient(p_id) on delete cascade)''')

cur.execute('''create table if not exists medication
            (m_id integer primary key autoincrement,d_id number,p_id number,name text,dose number,duration number,reaction text,constraint fk2 foreign key(d_id) references disease(d_id) on delete cascade,constraint fk3 foreign key(p_id) references patient(p_id) on delete cascade)''')

cur.execute('''create table if not exists surgeries
            (s_id integer primary key autoincrement,p_id number,part text,type text,purpose text,date text,recovery number,constraint fk4 foreign key(p_id) references patient(p_id) on delete cascade)''')

cur.execute('''create table if not exists drugs
            (sd_id integer primary key autoincrement,s_id number,p_id number,name text,dose number,duration number,reaction text,constraint fk5 foreign key(s_id) references surgeries(s_id) on delete cascade,constraint fk6 foreign key(p_id) references patient(p_id) on delete cascade)''')

cur.execute('''create table if not exists transfusions
            (t_id integer primary key autoincrement,p_id number,date text,units number,details text,constraint fk7 foreign key(p_id) references patient(p_id) on delete cascade)''')

cur.execute('''create table if not exists history
            (f_id integer primary key autoincrement,p_id number,disease text,relation text,constraint fk8 foreign key(p_id) references patient(p_id) on delete cascade)''')

cur.execute('''create trigger if not exists update_img after insert on patient for each row begin update patient set image="general.png" where p_id=new.p_id and image="";end;''' )