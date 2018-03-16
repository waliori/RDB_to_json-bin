from sqlalchemy import *
from sqlalchemy.sql import *
from classGen import *
import tkinter as Tk
import tkinter.constants as cnsts
import tkinter.ttk as ttk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as MB
import json
import pickle
import sys
import time


champs = {}
bd_con_inf=''

def jsonC(engine):
	conn = engine.connect()
	inspecteur = inspect(engine)
	noms = inspecteur.get_table_names()

	for nom in noms:
		fichier = open(nom+".json",'w')
		cols=inspecteur.get_columns(nom)
		attrs = []
		for col in cols:
			attrs.append(col['name'])
		c = classGen(nom,[attr for attr in attrs])
		stm = "select * from " + nom
		s = conn.execute(stm)	
		l=c()

		for row in s:
			j=0
			for attri in attrs:
				if(type(row[j]).__name__ == "datetime"):
					f=str(row[j])
				elif(type(row[j]).__name__ == "Decimal"):
					f=int(row[j])
				else:
					f=row[j]
				setattr(l, attri, f)
				j=j+1
			json.dump(l, fichier,default=lambda o: o.__dict__, indent=4)
	fichier.close()
	MB.showinfo('Etat conversion','Conversion en JSON completé avec succes ')

def binC(engine):
	conn = engine.connect()
	inspecteur = inspect(engine)
	noms = inspecteur.get_table_names()
	for nom in noms:
		fichier2 = open(nom+".p", 'wb')
		cols=inspecteur.get_columns(nom)
		attrs = []
		for col in cols:
			attrs.append(col['name'])
		c = classGen(nom,[attr for attr in attrs])
		stm = "select * from " + nom
		s = conn.execute(stm)	
		l=c()

		for row in s:
			j=0

			for attri in attrs:
				setattr(l, attri, row[j])
				j=j+1
			pickle.dump(l.__dict__, fichier2)
	fichier2.close()
	MB.showinfo('Etat conversion','Conversion en Binaire completé avec succes ')

def test_bdr(event):
	global selected
	selected = event.widget.get()
	
	if selected == "Oracle":
		champs['Mot de passe'].configure(state="enabled")
		champs['Base de données'].configure(state="disabled")
		champs['Nom d\'utilisateur'].configure(state="enabled")

	elif selected == "SQLite":
		champs['Base de données'].configure(state="disabled")
		champs['Mot de passe'].configure(state="disabled")
		champs['Nom d\'utilisateur'].configure(state="disabled")
		MB.showinfo('emplacement fichier de la base de données','C:\\Users\\waliori\\testDB.db')


	else:
		champs['Mot de passe'].configure(state="enabled")
		champs['Base de données'].configure(state="enabled")
		champs['Nom d\'utilisateur'].configure(state="enabled")


def deb(root):
	root.title("BD2C MiniProjet : Python  ->  Connection")
	frame = ttk.Frame(root)
	frame.pack()
	bdr=("Mysql", "Oracle", "SQLite")
	row = Tk.Frame(root)
	row.pack(side=cnsts.TOP, fill=cnsts.X, padx=5, pady=5)
	champ = Tk.Label(row, width=25, text="choix SGBD : ", anchor='w')
	box=ttk.Combobox(row,values=bdr,state="readonly")
	champ.pack(side=cnsts.LEFT)
	box.current(0)
	box.pack()
	box.bind("<<ComboboxSelected>>", test_bdr)
	noms_champs = ('Nom d\'utilisateur', 'Mot de passe','Base de données')
	for nom_champ in noms_champs:
		row = Tk.Frame(root)
		row.pack(side=cnsts.TOP, fill=cnsts.X, padx=5, pady=5)
		champ = Tk.Label(row, width=25, text=nom_champ + " : ", anchor='w')
		champ.pack(side=cnsts.LEFT)
		if nom_champ == 'Mot de passe':
			ent = ttk.Entry(row, show="*")
		else:
			ent = ttk.Entry(row)
		ent.pack(side=cnsts.RIGHT, expand=cnsts.YES, fill=cnsts.X)
		champs[nom_champ] = ent
	ttk.Button(root, text='Quiter', command=root.quit).pack(side=cnsts.RIGHT, padx=5, pady=5)
	ttk.Button(root, text="Connexion", command=connexion).pack(side=cnsts.RIGHT, padx=5, pady=5)

def connexion():
	
	if selected == "Mysql":
		bd_con_inf="mysql+pymysql://"+champs['Nom d\'utilisateur'].get()+":"+champs['Mot de passe'].get()+"@localhost/"+champs['Base de données'].get()
	elif selected == "Oracle":
		bd_con_inf="oracle://"+champs['Nom d\'utilisateur'].get()+":"+champs['Mot de passe'].get()+"@127.0.0.1:8080"
	else:
		bd_con_inf="sqlite:///C:\\Users\\waliori\\testDB.db"
	
	engine=create_engine(bd_con_inf,encoding='utf8', convert_unicode=True)
	try:
		conn = engine.connect()
		inspecteur = inspect(engine)
		noms = inspecteur.get_table_names()
		names=''
		for nom in noms:
			names=names+(nom+"\n")
		root.withdraw()
		fentre = Tk.Tk()
		fentre.title("BD2C MiniProjet : Python  ->  tables")
		frame = ttk.Frame(fentre)
		frame.pack()
		Label1 = Tk.Label(fentre, text = selected+"\nTables trouvées:\n\n"+names )
		Label1.pack()
		ttk.Button(fentre, text='Quiter', command=fentre.quit).pack(side=cnsts.RIGHT, padx=5, pady=5)
		json = ttk.Button(fentre, text="Json", command=lambda: jsonC(engine))
		json.pack(side=cnsts.RIGHT, padx=5, pady=5)
		bin=ttk.Button(fentre, text="Binaire", command=lambda: binC(engine))
		bin.pack(side=cnsts.RIGHT, padx=5, pady=5)
	except:
		MB.showinfo('Erreure soulevée',sys.exc_info()[1])
		root.quit



def test(root,names,engine):
	root = Tk.Tk()
	root.title("BD2C MiniProjet : Python  ->  tables")
	frame = ttk.Frame(root)
	frame.pack()
	Label1 = Tk.Label(root, text = "Tables trouvées:\n\n"+names )
	Label1.pack()
	ttk.Button(root, text='Quiter', command=root.quit).pack(side=cnsts.RIGHT, padx=5, pady=5)
	json = ttk.Button(root, text="Json", command=jsonC(engine))
	json.pack(side=cnsts.RIGHT, padx=5, pady=5)
	bin=ttk.Button(root, text="Binaire", command=binC(engine))
	bin.pack(side=cnsts.RIGHT, padx=5, pady=5)



if __name__ == "__main__":
    root = Tk.Tk()
    deb(root)
    root.mainloop()




	

