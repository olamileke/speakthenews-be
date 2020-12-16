### speakthenews-be
---
So I turned some of the scripts found [here](https://github.com/olamileke/web-scraping "here") into a REST API. It returns the title, summary, content and image of any [nytimes](https://nytimes.com "nytimes"), [washington post](https://washingtonpost.com "washington post"), [politico](https://politico.com "politico")
and [economist](https://economist.com "economist") article passed in as a query parameter.It is written in Flask-Restful and its functionality is exposed via a single /api/v1/text endpoint like

```
https://speakthenews.herokuapp.com/api/v1/text?url=xyz
```

I am currently working on a front end to consume this, which would allow users to create playlists of articles and have the articles read out to them.
The front end is written in React and is found [here](https://github.com/olamileke/speakthenews-fe "here").

To run this application locally, you need to have python3+ on your system. Get it 
[here](https://https://www.python.org/downloads/ "here"). Make sure to add python.exe to your operating system path variables to be able to run python scripts from the command line.

Navigate into a directory of choice on your system and run
``` 
git clone  https://github.com/olamileke/speakthenews-be.git
```
This will clone this repository onto your system. Next up, navigate into the application root by running
```
cd speakthenews-be
```

At this point, we need to create the virtual machine in which the application will run. Depending on if you are working in a windows or linux environment, follow the instructions found [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/ "here") to create the virtual environment.

Activate the virtual environment by running 
```
venv\scripts\activate
```
or 
```
source venv/scripts/activate
```
for windows and linux respectively.  Now, with the virtual environment active, run the following command
```
pip install -r requirements.txt
```
This will install all the application dependences as outlined in the requirements.txt file in the app root
Then, rename the *.env.example* file to *.env*. With the virtual environment still active, and still in the application root, run

```
python app.py
```
Here, the application will be available at http://localhost:5000

