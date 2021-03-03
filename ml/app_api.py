# importing packages
from sklearn import preprocessing
import pickle
import nltk
import pandas as pd
from flask import Flask, render_template, request, escape, session, g, url_for, jsonify
import mysql.connector
import datetime
"""
string = "infection including flu pneumonia immunization diphtheria tetanus child teething \
    infant inflammatory disease including rheumatoid arthritis ra crohn disease blood \
        clot extreme sunburn food poisoning medication including antibiotic"
        """


stopword = nltk.corpus.stopwords.words('english') # we are storing the stop words in a variable


'''Starting Preprocessing '''


'''Function clean
29. create lemmatize object
30. tokenize words in a senteance  eg:'this is a boy' -->  [this],[is],[a],[boy]
31. convert tokenized words into lowercase
32. no_stopwords --> storing all stop words eg:- is, there, are etc...
33. no_alpha --> storing words which are not stop words
34.lemmatize --> removing 'ings','es','s' etc.. from words...
'''
def clean(text):
    wn = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    lower = [word.lower() for word in tokens]
    no_stopwords = [word for word in lower if word not in stopword]
    no_alpha = [word for word in no_stopwords if word.isalpha()]
    lemm_text = [wn.lemmatize(word) for word in no_alpha]
    return lemm_text


'''Funtion to convert clean group of words into sequence of numbers called vectors'''
def vectorize(data, tfidf_vect_fit):
    X_tfidf = tfidf_vect_fit.transform(data)
    words = tfidf_vect_fit.get_feature_names()
    X_tfidf_df = pd.DataFrame(X_tfidf.toarray())
    X_tfidf_df.columns = words
    return(X_tfidf_df)


# Prediction function
def predictions(string):

    strngs = clean(string)
    x_string = ""

    for stng in strngs:
        x_string = x_string+" "+stng

    with open('vector.pickle', 'rb') as vector:
        model_vector = pickle.load(vector)
        vector.close()

    with open('model.pickle', 'rb') as mlmodel:
        model1 = pickle.load(mlmodel)
        mlmodel.close()

    with open('labels.pickle', 'rb') as resltdict:
        labels = dict(pickle.load(resltdict))

    pred = model1.predict(model_vector.transform([x_string]))

    return labels[int(pred)]


# prediction function ended


# creating the flask server


app = Flask(__name__)

#it is used to generate session id
app.secret_key = 'aakljslhbfkaljbflaksjdfbla'

# MySQL Connection

mydb = mysql.connector.connect(
    host = "localhost",
    user = "<your user name>",
    password = "<your user password>",
    database = "medconnect"
)

mycursor = mydb.cursor(dictionary = True)
# the output of sql statements would be in form of a dictionary

@app.before_request 
def before_request():
    g.user = None
    if 'id' in session:
        g.user = session['id']

# Starting of routes

@app.route('/', methods = ['GET', 'POST']) 
def signin(): 
    if(request.method == 'POST'):
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        # return password
        mycursor.execute("select id, name, email, password from users where email = %s AND password = %s", (email, password))
        account = mycursor.fetchone()
        if account:
            session['id'] = account['id']
            message = 'Logged in successfully !'
            id = account['id']
            date = str(datetime.date.today())
            mycursor.execute("INSERT INTO logindetails (id, date) VALUES (%s, %s)", (id, date))
            mydb.commit()
            return render_template('home.html',account=account, message=message)
        else:
            message = 'invalid'
            return render_template('signin.html',message=message)
    else:
        return render_template('signin.html')

@app.route('/signup', methods = ['GET', 'POST']) 
def signup():
    if(request.method == 'POST'):
        email = escape(request.form['inputEmail'])
        password = escape(request.form['inputPassword'])
        name = escape(request.form['inputName'])
        place = escape(request.form['inputPlace'])
        mycursor.execute("INSERT INTO users (email,password,name,place) VALUES (%s, %s, %s, %s)", (email, password, name, place))
        mydb.commit()
        if mycursor.rowcount > 0:
            message = "Signup successfull. Please Login"
            return render_template('signin.html', message=message)
        else:
            message = "Signup not successfull."
            return render_template('signup.html', message=message)    
    else:
        return render_template('signup.html')

@app.route('/home') 
def home():
    if g.user:
        mycursor.execute("select name from users where id = %s", (g.user,))
        account = mycursor.fetchone()
        return render_template('home.html', account=account)
    else:
        render_template('signin.html', message = "Please login for accessing account")

@app.route('/account') 
def account():
    if g.user:
        mycursor.execute("SELECT users.email, users.name, users.place, logindetails.date FROM users INNER JOIN logindetails ON users.id = logindetails.id WHERE users.id = %s", (g.user,))
        account = mycursor.fetchall()
        return render_template('account.html', account=account)
    else:
        render_template('signin.html', message = "Please login for accessing account")

@app.route('/logout') 
def logout():
    message = "Successfully Logged Out"
    session.pop('id', None)
    return render_template('signin.html', message=message)

@app.route('/chatbot') 
def chatbot():
    if g.user:
        mycursor.execute("select name from users where id = %s", (g.user,))
        account = mycursor.fetchone()
        return render_template('chatbot.html', account=account)
    else:
        render_template('signin.html', message = "Please login for accessing account")

@app.route('/predict', methods=['GET','POST'])
def model_code(): 
    if request.method=="POST": 
        content = request.json
        strings = content["str"]
        print(strings)
        disease = predictions(strings)
        print(disease)
        return jsonify({"value":disease})

if __name__=='__main__':
    app.run()
