from flask import Flask, render_template, redirect, request, session,request
from flask_session import Session
import time
import db
import datetime
from master import get_irancell_price


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def init_session():
    init_ses= ['is_login','name','level','start','message']
    if 'start' not in session:
        for index in init_ses:
            session[index] = None    

@app.route("/")
def index():
    init_session()
    if not session['is_login']:
        return redirect('login')
    showType = request.args.get('show','all')
    if showType == 'all':
        data = db.get_packages()
    elif showType == 'hamrahe_aval':
        data = db.get_packages('mci')
    elif showType == 'rightel':
        data = db.get_packages('rtl')
    else:
        data = db.get_packages('mtn')

    last_update_time = int(time.time()) - int(db.get_setting()['last_update'])
    
    if (last_update_time % 3600 // 60) == 0:
        last_update = '1 دقیقه پیش'
    elif last_update_time//3600 == 0:
        last_update = str(last_update_time % 3600 // 60) + ' دقیقه ' + ' پیش '
    else:
        last_update = str(last_update_time//3600) + ' ساعت ' + str(last_update_time % 3600 // 60) + ' دقیقه ' + ' پیش '

    requests_count = len(db.get_requests(session['user']['phone']))
    message = session['message']
    session['message'] = ''

    return render_template('main.html',packages=data,message=message,last_update=last_update,pricing_count=requests_count,show=showType,user=session['user'])


@app.route("/login" , methods=['POST','GET'])
def login():
    init_session()
    username = request.form.get('username')
    password = request.form.get('password')
    print(username)
    if request.method == 'POST' and not session['is_login']:
        user = db.get_user(username=username,password=password)
        if len(user) > 0:
            user = user[0]
            session['is_login'] = True
            session['user'] = user
            
            return redirect('/')
        else:
            return render_template('login.html',error='نام کاربری یا رمز عبور اشتباه است.')
    elif session['is_login']:
        return redirect('/')
    elif request.method == 'GET':
        return render_template('login.html')
    return render_template('login.html')

@app.route("/prediction")
def prediction():
    init_session()
    if not session['is_login']:
        return redirect('login')
    return render_template('basicPrediction.html',user=session['user'])

@app.route("/basicPrediction")
def basic():
    init_session()
    if not session['is_login']:
        return redirect('login')
    return render_template('basicPrediction.html',user=session['user'])

@app.route("/internetPrediction")
def internet():
    init_session()
    if not session['is_login']:
        return redirect('login')
    return render_template('internetPrediction.html',user=session['user'])

@app.route("/predictionHistory")
def history():
    init_session()
    if not session['is_login']:
        return redirect('login')
    history = db.get_requests(session['user']['phone'])
    return render_template('predictionHistory.html',history=history,user=session['user'])

@app.route("/result",methods=['POST','GET'])
def result():
    init_session()
    if not session['is_login']:
        return redirect('login')
    result = ''
    prices = {}
    action = request.form.get('action')
    if action == 'basicPrediction':
        internet = request.form.get('internet')
        call = request.form.get('call')
        sms = request.form.get('sms')
        period = request.form.get('period')
        try:
            result = get_irancell_price(internet=internet,call=call,sms=sms,period=period)
        except:
            return 'تلاش بیش از حد، دقایقی دیگر دوباره درخواست را ارسال کنید.'
        result = int(int(result) * 0.98 // 100 * 100 )
        nid = 'm' + str(int(time.time()))
        req ={
            'package': f" internet({internet}) call({call}) sms({sms})",
            'period': period,
            'price': result,
            'user': session['user']['phone'],
            'feedback': '',
            '_id': nid
        }
        db.insert_requests(req)
        is_internet = False
    elif action == 'internetPrediction':
        internet = request.form.get('internet')
        period = request.form.get('period')

        permanent = request.form.get('permanentOffer',0)
        prepaied = int(request.form.get('prepaiedOffer',0))
        data = int(request.form.get('datatOffer',0))
        if permanent == '':
            permanent = 0
        if prepaied == '':
            prepaied = 0
        if data == '':
            data = 0
        permanent = int(permanent) / 100
        prepaied = int(prepaied) / 100
        prepaied = int(prepaied) / 100
        try:
            a = int(get_irancell_price(internet,50,50,period))
            b  = int(get_irancell_price(50,50,50,period))
            c  = int(get_irancell_price(100,50,50,period))
            d  = int(get_irancell_price(50,50,50,period))
        except:
            return 'تلاش بیش از حد، دقایقی دیگر دوباره درخواست را ارسال کنید.'
        result = a - b + (c - d)
        result = int(int(result) * 0.98 // 100 * 100 )
        nid = 'm' + str(int(time.time()))
        req ={
            'package': f" internet({internet})",
            'period': period,
            'price': result,
            'user': session['user']['phone'],
            'feedback': '',
            '_id': nid
        }
        db.insert_requests(req)
        prices = {
            'permanent': int(result * (1 - permanent)),
            'prepaeid': int(result * (1 - prepaied)),
            'data': int(result * (1 - data))
        }
        is_internet = True


    return render_template('show.html',is_internet=is_internet,prices=prices,price=result,id=nid,user=session['user'])


@app.route("/feedback")
def feedback():
    init_session()
    if not session['is_login']:
        return redirect('login')
    ftype = request.args.get('type')
    fid = request.args.get('id')
    db.update_reqest_feedback(fid,ftype)

    session['message'] = 'فیدبک شما با موفقیت ثبت شد، درخواست شما از طریق تاریخچه قابل مرور است.'
    return redirect('/')

@app.route("/updatePackage")
def update_ackages():
    init_session()
    if not session['is_login']:
        return redirect('login')
    db.update_last_update()
    session['message'] = 'پایگاه داده و بسته‌ها با موفقیت بروزرسانی شدند، مدل آماده استفاده است.'
    return redirect('/')




@app.route("/logout" , methods=['POST','GET'])
def logout():
    init_session()
    session['is_login'] = False

    return redirect('/')


app.run(port=7980,host='0.0.0.0')