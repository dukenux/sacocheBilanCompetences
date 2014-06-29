#!/usr/bin/env python 
# -*- coding: utf8 -*-
import cgitb
import cgi
from SacocheDb import *

form = cgi.FieldStorage()
sdb=SacocheDb()
nomClasse=""
eleve=""
fromEleve=False
if form.getvalue('classe'):
   nomClasse = form.getvalue('classe')
if form.getvalue('eleve'):
   eleve = form.getvalue('eleve')
if form.getvalue('from'):
   fromEleve=True 
print "Content-type: text/html\n\n"
print '<html><body>'
print '<h1>Bilan de competences SEN</h1>'
if fromEleve==False:
    print '<form name="classeForm" target="_self" method="get">'
    l=sdb.getClassroomList()
    print 'Classe: <select name="classe">'
    for i in range(len(l)):
        if nomClasse==l[i]: print '<option value="'+l[i]+'" selected>'+l[i]+'</option>'
        else : print '<option value="'+l[i]+'">'+l[i]+'</option>'
    print '</select>'
    print '<input type="submit" value="Select"/>'
    print '</form>'

    if len(nomClasse)>0:
        l=sdb.getStudentList(nomClasse)
        print '<form name="eleveForm" target="_self" method="get">'
        print 'Eleve: <select name="eleve">'
        for i in range(len(l[0])):
            eleveConcat=l[0][i]+" "+l[1][i]
            if eleve==eleveConcat: print '<option value="'+eleveConcat+'" selected>'+eleveConcat+'</option>'
            else : print '<option value="'+eleveConcat+'">'+eleveConcat+'</option>'
        print '</select>'
        print '<input type="hidden" name="classe" value="'+nomClasse+'"/>'
        print '<input type="submit" value="Select"/>'
        print '</form>'
if len(eleve)>0:
    print '<table>'
    l=sdb.getSkillList()
# on fait une sorte de group by pour faire la moyenne de chaque compétence pour l'ensemble des professeurs
# chaque professeur doit avoir cependant le même regroupement d'item pour que ca marche
# on ne prend en compte que les compétences évaluées (>-1)
    while i<len(l[0]):
        debutCompet=l[1][i][0:5]
        m=sdb.getMarkAverage(sdb.getStudentMark(eleve,l[0][i]))
        i+=1
        j=1
        k=1
        while i<len(l[0]):
            if l[1][i][0:5]!=debutCompet: break
            competLevel=sdb.getMarkAverage(sdb.getStudentMark(eleve,l[0][i]))
            if competLevel>-1:
                m+=sdb.getMarkAverage(sdb.getStudentMark(eleve,l[0][i]))
                k=k+1
            i=i+1
            j=j+1
        m=m/k    
        if m==-1: img="ne.jpeg"
        elif m<2: img="0.jpeg"
        elif m<3: img="1.jpeg"
        elif m<4: img="2.jpeg"
        else: img="3.jpeg"
        print '<tr><td>'+l[1][i]+'</td><td><img src="'+img+'"/></td></tr>'
    print '</table>'
sdb.closeDb()
