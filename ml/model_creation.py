# importing packages
import pandas as pd
from sklearn import preprocessing # all the algorithms and preprocessing functions are in sklearn
import nltk  # natural language tool kit
from sklearn.feature_extraction.text import TfidfVectorizer # to change sentence to vectors
from sklearn.model_selection import train_test_split
import pickle # to save data and models
from sklearn.ensemble import RandomForestClassifier # algorithm
label_encoder = preprocessing.LabelEncoder() # to change words into numbers
from sklearn.metrics import accuracy_score # to calculate the accuracy


stopword = nltk.corpus.stopwords.words('english') # we are storing the stop words in a variable


#importing dataset
medical_dataset=pd.read_csv(r"dataSet.csv")


# Function to convert to words into lower cases. eg:- apple
def lower_con(strings):
    return strings.lower()


'''Starting Preprocessing '''


'''Function clean
43. create lemmatize object
44. tokenize words in a senteance  eg:'this is a boy' -->  [this],[is],[a],[boy]
45. convert tokenized words into lowercase
46. no_stopwords --> storing all stop words eg:- is, there, are etc...
47. no_alpha --> storing words which are not stop words
48.lemmatize --> removing 'ings','es','s' etc.. from words...
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
def vectorize(data,tfidf_vect_fit):
    X_tfidf = tfidf_vect_fit.transform(data)
    words = tfidf_vect_fit.get_feature_names()
    X_tfidf_df = pd.DataFrame(X_tfidf.toarray())        
    X_tfidf_df.columns = words
    return(X_tfidf_df)


'''apply function --> (function in pandas ) syntax :apply(functin_name)
It will pass each data in the dataset as an argument to function clean'''
medical_dataset['symptoms']=medical_dataset['symptoms'].apply(clean)

'''convert lists into strings [i ] [am] [good]-->'i am good' ''' 
medical_dataset['clean_text']=medical_dataset['symptoms'].apply(lambda x: " ".join([str(word) for word in x]))


'''creating tfidf object'''
tfidf_vect = TfidfVectorizer(analyzer=clean)
tfidf_vect_fit=tfidf_vect.fit(medical_dataset['clean_text'])
X_train=vectorize(medical_dataset['clean_text'],tfidf_vect_fit)


'''saving tfidf object for testing
It is saved in binary format'''
with open('vector.pickle', 'wb') as vcmodel:
    pickle.dump(tfidf_vect_fit, vcmodel, protocol=pickle.HIGHEST_PROTOCOL)


'''converting words into numbers'''
label_encoder = preprocessing.LabelEncoder() 
target_label_model=label_encoder.fit(medical_dataset['Disease'])


'''transforming numbers to labels'''
y_train=target_label_model.transform(medical_dataset['Disease'])
result_dict={}
for uni in pd.Series(y_train).unique():
    result_dict[uni]=target_label_model.inverse_transform([uni])[0]


'''Saving labels for testing 
It is saved in binary format
{
    1:'feaver',
    2:'headache',
    .....
}
'''
with open('labels.pickle', 'wb') as lbltxt:
    pickle.dump(result_dict, lbltxt, protocol=pickle.HIGHEST_PROTOCOL)


'''Spliting the data into test data and training data.
Here test-size is 0.4 which means that we are taking 40% as test data'''
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.4, random_state=0)


'''PreProcessing Finished'''


'''Training Starting
The random forest algorithm is a supervised classification algorithm. As the name suggests,
this algorithm creates the forest with a number of trees.
'''
text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
model=text_classifier.fit(X_train, y_train)


'''saving model
It is saved in binary format'''
with open('model.pickle', 'wb') as mlmodel:
    pickle.dump(model, mlmodel, protocol=pickle.HIGHEST_PROTOCOL)


'''Calculating the accurracy of model'''
y_pred=model.predict(X_test)
print("model_accuracy {}% ".format(accuracy_score(y_pred,y_test)*100))

# print(model.get_params())
