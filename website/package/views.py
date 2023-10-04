from flask import Blueprint , render_template , request , flash , jsonify ,redirect ,url_for
from flask_login import login_required, current_user
from .models import Note , Submission
from . import db 
import requests 
import json 
views=Blueprint('views',__name__)


@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')

        if len(note)<1:
            flash('Note is too short!',category='error')
        else :
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!",category='success')


    return render_template('home.html',user=current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/Data-Stewards', methods=['GET','POST'])
@login_required
def Data_stewards():
    if request.method=="POST":
        Data_ID=request.form.get('Data_ID')
        Title=request.form.get('Title')
        Desc=request.form.get('Desc')
        Pub=request.form.get('Pub')
        List_Sub=[Data_ID,Title,Desc,Pub]

        DI=Submission.query.filter_by(Data_ID=Data_ID).first()
        if DI:
            flash("Data ID already exists.",category='error')
            return (render_template("DS_form.html", user=current_user))

        #if isinstance(Data_ID,str):
            #flash("Must be an Integer.",category='error')

        elif len(Title)<2:
            flash('Title needs to be more than 2 character', category= 'error')
        elif len(Desc)<2:
            flash('Description needs to be more than 2 characters', category= 'error')
        elif len(Pub)<4:
            flash('Password needs to be more than 4 characters', category= 'error')
        
        else :
            new_sub=Submission(Data_ID=Data_ID,Title=Title,Desc=Desc,Pub=Pub,user_id=current_user.id)
            db.session.add(new_sub)
            db.session.commit()
            
            flash('Submission Logged', category= 'success')
        if List_Sub:
            return render_template("DS_form.html",List_Sub=List_Sub,user=current_user)
    return render_template("DS_form.html",user=current_user)

@views.route('/submission', methods=['GET','POST'])
def submission():
    if request.method=="POST":
        import requests

# defining the api-endpoint
        API_ENDPOINT = "https://pastebin.com/api/api_post.php"

# your API key here
        API_KEY = "TELwZAA2OKhAKPMff2qAOPY7gebhlz9p"


# your source code here
        source_code = '''
        print("API CALL recieved next is SSC data catalog")
        '''

    # data to be sent to api
        data = {'api_dev_key': API_KEY,
		'api_option': 'paste',
		'api_paste_code': source_code,
		'api_paste_format': 'python'}

# sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is:%s" % pastebin_url)
        return render_template("Succes_form.html",pastebin_url=pastebin_url,user=current_user)

