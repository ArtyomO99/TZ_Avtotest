from flask import Flask, request
import linecache

def isnum(line):
    for i in range(1,len(line)): #чтобы пропустить все с альтернативами
        if line[i][0].isdigit()==False: #пропускаем все данные до цифр широты
            continue
        else:
            num = i
            return num   

def make_inf(cutline): #принимает часть списка (cutline), чтобы с помощью них сделать список с реальными данными о городе
    cut_inf = []
    cut_inf.append('Latitude  = '+ cutline[0])
    cut_inf.append('Longitude   = '+ cutline[1])
    cut_inf.append('Feature class = '+ cutline[2])
    cut_inf.append('Feature code = '+ cutline[3])
    cut_inf.append('Country code  = '+ cutline[4])
    cut_inf.append('Alternate country codes = '+ cutline[5])
    cut_inf.append('Population  =' + cutline[6]+'')
    cut_inf.append('Elevation  = '+ cutline[7]+'meters')
    cut_inf.append('The iana timezone id ='+ cutline[8])
    cut_inf.append('Date of last modification - '+ cutline[9])
    return cut_inf


app = Flask(__name__)


@app.route('/getfile/<geonameid>') # пример: http://127.0.0.1:8000/getfile/451828
def serch_geonameid(geonameid):
    with open('RU.txt', 'r', encoding='utf-8') as file: 
        while True:
            line = file.readline()
            if not line:
                break
            else:
                if geonameid in line:
                    s = []
                    line = line.split()
                    l1 ='Integer id of record in geonames database is ' + line[0]
                    l2 ='Name of geographical point is ' + line[1]
                    l = [l1,l2]
                    num = isnum(line)#остальные данные выводим пропуская всякие альтернативные имена начиная с элемента num
                    print(num)
                    cutline =line[num::] #разрезали список, это последние 10 элементов
                    cutline = make_inf(cutline) #список с инф. данными
                    line = l+cutline
                    s.append(line)
    return s


@app.route('/getpage') # пример: http://127.0.0.1:8000/getpage?page=2&perPage=10
def getpage():
    page=int(request.args.get('page')) #страница
    perPage=int(request.args.get('perPage')) #кол-во на странице
    firstline=(page*perPage)-(perPage-1) #первая строка страницы
    lastline=page*perPage #последняя строка
    s = []
    for i in range(firstline,lastline+1):
        line =  linecache.getline('RU.txt',i) #строка о городе
        # превращаем x в данные
        line = line.split()
        l1 ='Integer id of record in geonames database is ' + line[0]
        l2 ='Name of geographical point is ' + line[1]
        l = [l1,l2]
        num = isnum(line)#остальные данные выводим пропуская всякие альтернативные имена начиная с элемента num
        print(num)
        cutline =line[num::] #разрезали список, это последние 10 элементов
        cutline = make_inf(cutline) #список с инф. данными
        line = l+cutline
        s.append(line)
    return s
        

@app.route('/getcity') #пример: http://127.0.0.1:8000/getcity?city_1=Ступнево&city_2=Стукшино
def getcity():
    city_1=request.args.get('city_1')
    city_2=request.args.get('city_2')
    with open('RU.txt', 'r', encoding='utf-8') as file: 
        while True:
            line = file.readline()
            if not line:
                break
            else:
                if city_1 in line:
                    s1 = []
                    line1 = line.split()
                    point1 = line1[1]
                    l1 ='Integer id of record in geonames database is ' + line1[0]
                    l2 ='Name of geographical point is ' + line1[1]
                    l = [l1,l2] 
                    num = isnum(line1)#остальные данные выводим пропуская всякие альтернативные имена начиная с элемента num
                    cutline =line1[num::] #разрезали список, это последние 10 элементов
                    lat1 = float(cutline[0]) #получить широту 1-го города 
                    cutline = make_inf(cutline) #список с инф. данными
                    line1 = l+cutline
                    s1.append(line1)
                    time1 = cutline[9] # получить часовую зону 1-го города
                elif city_2 in line:
                    s2 = []
                    line2 = line.split()
                    point2 = line2[1]
                    l1 ='Integer id of record in geonames database is ' + line2[0]
                    l2 ='Name of geographical point is ' + line2[1]
                    l = [l1,l2]
                    num = isnum(line2)#остальные данные выводим пропуская всякие альтернативные имена начиная с элемента num
                    cutline =line2[num::] #разрезали список, это последние 10 элементов
                    lat2 = float(cutline[0]) #получить широту 2-го города 
                    cutline = make_inf(cutline) #список с инф. данными
                    line2 = l+cutline
                    s2.append(line2)
                    time2 = cutline[9] # получить часовую зону 2-го города
    if lat2>lat1:
        mes1 = 'The geographical point ' + point2 +'north of the point '+ point1
    else:
        mes1 = 'The geographical point ' + point1 +'north of the point '+ point2 #обращение к номеру списка, в котором полное название точки
    if time2==time1:
        mes2 = 'The time zones are the same'
    else:
        mes2 = 'Time zones are different'
    #Формируется список из списка 1-й, 2-й точки и двух результатов проверки
    result = []
    result.append(s1)
    result.append(s2)
    result.append(mes1)
    result.append(mes2)
    return result



if __name__ == "__main__":
    app.run(debug=True, port=8000)