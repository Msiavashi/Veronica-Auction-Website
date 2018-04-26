# auction

### How to contribute:

1. git clone <project>

2. git branch branch_name

3. // do your stuff

4. git add

5. git commit -m 'provide an expressive message'

6. git push

7. //send a new PR from branch_name to master

8. //don't merge your own PR!

### Tips:

we'll work on MVC based structure. api skeletons are provided within controller direcotry devided by api section names (e.g: Authentication-API.py, Shop-API.py, etc) then all you need to do is to implement route bodies within these files .

### Database:

in order to simplicity we have thread scope database module. 

to query on a model : Model_name.query.filter_by( field_name=some_value, field_name2=some_value2 , .... )

in order to save or update a model you need to create a database session:
  session = database.db_session()
  session.add(your_model)
  session.commit()  //to commit changes to datase
  
there is also a get_current_user() provided to simply get the currently loged in user .

NOTE: you don't have to close the session, the session will be terminated when thread is done.

### authentication

for those routes which needs authentication. just simply put a `@jwt_required` annotation on top of the function, i'll take care of the rest .
  
