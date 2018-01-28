## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'


####################
###### FORMS #######
####################
class ArtistForm(FlaskForm):
	album= StringField('Enter the name of an album:', validators=[Required()])
	rating= RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1',1),('2',2),('3',3)], validators= [Required()])
	submit= SubmitField('Submit')


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artistform():
	return render_template('artistform.html')

@app.route('/artistinfo',methods=['GET'])
def artist():
	if request.method=='GET':
		term= request.args['artist']
		url= 'https://itunes.apple.com/search?entity=musicTrack&term={}'.format(term)
		req=requests.get(url)
		artist= req.json()['results']
		return render_template('artist_info.html',objects=artist)

@app.route('/artistlinks')
def artistlinks():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def artistname(artist_name):
	url='https://itunes.apple.com/search?entity=musicTrack&term={}'.format(artist_name)
	req= requests.get(url)
	artist= req.json()['results']
	return render_template('specific_artist.html',results=artist)

@app.route('/album_entry')
def albumentry():
	form=ArtistForm()
	return render_template('album_entry.html',form=form)

@app.route('/album_result', methods=['GET','POST'])
def albumresult():
	form1=ArtistForm(request.form)
	if request.method== 'POST' and form1.validate_on_submit():
		album=form1.album.data
		rating= form1.rating.data
		return render_template('album_data.html', album_name=album, album_rating=rating)
	flash('All fields are required')
	return redirect(url_for('album_entry'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
