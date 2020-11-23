from flask import Flask, render_template, request
import mysql.connector
import re

app = Flask(__name__, static_url_path='/static')

gamedb = mysql.connector.connect(user='callum', password='GT67phn@',
                              host='192.168.0.34', database='game',
                              auth_plugin='mysql_native_password')


#Code runs if index.html called (root)
@app.route('/', methods=['GET', 'POST'])
def index():
    if "viewcharacter" in request.form:
        return render_template('/view_char.html', data=viewchar())
    elif "viewitems" in request.form:
        return render_template('/view_item_charpick.html', data=view_char_items())
    elif "viewencounters" in request.form:
        return render_template('/.html')
    elif "characteroptions" in request.form:
        return render_template('/character_edit.html', data=character_edit_race(), data1=character_edit_class(), data2=character_edit_alignment(), data3=character_edit_armour(), data4=character_edit_protection())
    elif "additems" in request.form:
        return render_template('/add_item.html') 
    elif "addencounters" in request.form:
        return render_template('/.html') 
    else:
        return render_template('/index.html')


@app.route('/character_edit', methods=['GET', 'POST'])
def character():  
  if "submit" in request.form:
      details = request.form
      FirstName = details['FirstName']
      Surname = details['Surname']
      Age = details['Age']

      ### Get details from drop down boxes


      Level = details['Level']
      Strength = details['Strength']
      Brawn = details['Brawn']
      Agility = details['Agility']
      Mettle = details['Mettle']
      Craft = details['Craft']
      Insight = details['Insight']
      Wits = details['Wits']
      Resolve = details['Resolve']
      Life = details['Life']


          #cur = gamedb.cursor()
          # Need to finish line 
          # cur.execute("INSERT INTO player_characters(first_name, last_name, raceID_FK1, classID_FK1, alignmentID_FK1, level, strength, brawn, agility, mettle, craft, insight, wits, resolve, life, armourID_FK1, protectionID_FK1) VALUES (%s, %s, %s, %s, %s %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)", (Surname, FirstName, Address, Address2,Phone))
          #gamedb.commit()
          #cur.close()
          
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')

@app.route('/view_item_charpick.html', methods=['GET', 'POST'])
def item_charpick():
    if "Select" in request.form:
        details = request.form
        Character_Details = details['character']
        Character_Details = Character_Details.split(" ")
        CharacterFirstName = Character_Details[0]
        CharacterSecondName = Character_Details[1]
        character = get_char_name(CharacterFirstName, CharacterSecondName)
        #character2 = get_char_name(CharacterSecondName)
        print(CharacterFirstName)
        print(CharacterSecondName)
        int_nameID = character[0]
        int_nameID = str(int_nameID[0])
        return render_template('/view_item.html', data=get_char_name(CharacterFirstName, CharacterSecondName))
    elif "Back" in request.form:
        pass
    return render_template('/index.html')

def view_char_items():
    cur = gamedb.cursor()
    cur.execute('SELECT CONCAT(first_name," ",last_name) FROM player_characters')
    data = cur.fetchall()
    return data

def get_char_name(first_num, second_num):
    details = request.form
    cur = gamedb.cursor()
    check = ("SELECT playerID FROM player_characters where player_characters.first_name='" + first_num + "' and player_characters.last_name='" + second_num +"'")
    #playerid = check(details['playerID'])
    #print(playerid)
    #query = ("SELECT itemID_FK2 FROM inventory where inventory.playerID_FK1='" + name + "'")# nameinventory.playerID_FK1=player_characters.playerID'" + name + "'")
    cur.execute(check)
    code = cur.fetchall()
    print(code)

    temp = re.sub(r'[\[\]\(\), ]', '', str(code))
    print(temp)
    get_items = ("SELECT name, cost, item_load FROM inventory, items WHERE inventory.playerID_FK1='" + temp + "' and inventory.itemID_FK2=items.itemID") 
    cur.execute(get_items)
    data = cur.fetchall()
    return data

def view_items():
    cur = gamedb.cursor()
    cur.execute("SELECT itemID_FK2 FROM inventory")


def viewchar():
    cur = gamedb.cursor()
    cur.execute("SELECT first_name, last_name, race.name, classes.classes, alignment.type, level, strength, brawn, agility, mettle, craft, insight, wits, resolve, life, armour.name, protection.name FROM player_characters, race, classes, alignment, armour, protection where player_characters.raceID_FK1=race.raceID and player_characters.classID_FK1=classes.classID and player_characters.alignmentID_FK1=alignment.alignmentID and player_characters.armourID_FK1=armour.armourID and player_characters.protectionID_FK1=protection.protectionID;")
    data = cur.fetchall()
    return data

def character_edit_race():
    cur = gamedb.cursor()
    cur.execute('SELECT name FROM race')
    data = cur.fetchall()
    return data

def character_edit_class():
    cur = gamedb.cursor()
    cur.execute('SELECT classes FROM classes')
    data = cur.fetchall()
    return data

def character_edit_armour():
    cur = gamedb.cursor()
    cur.execute('SELECT name FROM armour')
    data = cur.fetchall()
    return data

def character_edit_protection():
    cur = gamedb.cursor()
    cur.execute('SELECT name FROM protection')
    data = cur.fetchall()
    return data

def character_edit_alignment():
    cur = gamedb.cursor()
    cur.execute('SELECT type FROM alignment')
    data = cur.fetchall()
    return data

if __name__ == '__main__':
    app.run(debug=True)
    #app.run()
