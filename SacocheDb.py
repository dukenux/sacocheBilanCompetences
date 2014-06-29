#!/usr/bin/python
# -*- coding: utf8 -*-
import MySQLdb


class SacocheDb():

    def __init__(self):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="hameg", db="sacoche")
        self.curs = self.db.cursor()

    def closeDb(self):
        self.curs.close()
        self.db.close()

    def getSkillList(self):
        skillList=[]
        skillList.append([])
        skillList.append([])
        result=self.curs.execute("select selection_item_id,selection_item_nom from sacoche_selection_item order by selection_item_nom")
        result=self.curs.fetchall()
        for i in range(len(result)):
            if len(result[i][1])>0:
                skillList[0].append(result[i][0])
                skillList[1].append(result[i][1])
        return skillList

    def getStudentList(self,classroom):
        studentList=[]
        studentList.append([])
        studentList.append([])
        result=self.curs.execute("select user_nom,user_prenom from sacoche_user,sacoche_groupe where eleve_classe_id=groupe_id and groupe_nom like '"+classroom+"' order by user_nom")
        result=self.curs.fetchall()
        for i in range(len(result)):
            if len(result[i][0])>0: 
                studentList[0].append(result[i][0])
                studentList[1].append(result[i][1])
        return studentList


    def getClassroomList(self):
        classroomList=[]
        result=self.curs.execute("select groupe_nom from sacoche_groupe")
        result=self.curs.fetchall()
        for i in range(len(result)):
            if len(result[i][0])>0: classroomList.append(result[i][0])
        return classroomList


    def getUserId(self,name,firstName):
        result=self.curs.execute("select user_id from sacoche_user where user_nom like '"+name+"' and user_prenom like '"+firstName+"'")
        result=self.curs.fetchall()
        if len(result)>0:
            try:
                return int(result[0][0])
            except ValueError:
                return -1
        else: return -1

    def getItemIdList(self,skillId):
        result=self.curs.execute("select selection_item_liste from sacoche_selection_item where selection_item_id="+str(skillId))
        result=self.curs.fetchall()
        index=[]
        for j in range(len(result)):
            s=result[j][0].split(',')
            for i in range(len(s)):
                try:
                    index.append(int(s[i]))
                except ValueError:
                    k=5
        return index


    def getItemList(self,skills):
        allSkills=""
        for i in range(len(skills)):
            if len(allSkills)>0:
                allSkills+=" or selection_item_nom like '"+skills[i]+"%'"
            else: allSkills+=" '"+skills[i]+"%'"
        result=self.curs.execute("select selection_item_liste from sacoche_selection_item where selection_item_nom like"+allSkills )
        result=self.curs.fetchall()
        index=[]
        for j in range(len(result)):
            s=result[j][0].split(',')
    	    for i in range(len(s)):
                try:
                    index.append(int(s[i]))
                except ValueError:
                    k=5
        return index

    def getMarkList(self,userId,itemList):
        allItems=""
        markList=[]
        for i in range(len(itemList)):
            if len(allItems)>0:
                allItems+=","+str(itemList[i])
            else: allItems+="("+str(itemList[i])
        if len(allItems)>0:
            result=self.curs.execute("select saisie_note from sacoche_saisie where eleve_id="+str(userId)+" and item_id in "+allItems+")")
            result=self.curs.fetchall()
            markList=[]
            for j in range(len(result)):
                s=result[j][0].split(',')
                for i in range(len(s)):
                    if s[i]=="RR": markList.append(1)
                    if s[i]=="R": markList.append(2)
                    if s[i]=="V": markList.append(3)
                    if s[i]=="VV": markList.append(4)
        return markList

    def getUserId(self,studentName):
        namePart=studentName.split(' ')
        if len(namePart)!=2: return -1
        result=self.curs.execute("select user_id from sacoche_user where user_nom like '"+namePart[0]+"' and user_prenom like '"+namePart[1]+"'")
        result=self.curs.fetchall()
        if len(result)>0: return result[0][0]
        return -1
    
    def getStudentMark(self,studentName,skillId):
        userId=self.getUserId(studentName)
        if userId==-1: return -1
        itemList=self.getItemIdList(skillId)
        allItems=""
        markList=[]
        for i in range(len(itemList)):
            if len(allItems)>0:
                allItems+=","+str(itemList[i])
            else: allItems+="("+str(itemList[i])
        if len(allItems)>0:
            result=self.curs.execute("select saisie_note from sacoche_saisie where eleve_id="+str(userId)+" and item_id in "+allItems+")")
            result=self.curs.fetchall()
            markList=[]
            for j in range(len(result)):
                s=result[j][0].split(',')
                for i in range(len(s)):
                    if s[i]=="RR": markList.append(1)
                    if s[i]=="R": markList.append(2)
                    if s[i]=="V": markList.append(3)
                    if s[i]=="VV": markList.append(4)
        return markList        

    def getMarkAverage(self,markList):
        average=0
        if len(markList)==0: return -1
        for i in range(len(markList)):
            average+=markList[i]
        return float(float(average)/float(len(markList)))

