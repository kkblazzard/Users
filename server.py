from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/")
def index():
    print("index")
    return redirect("/users")

@app.route("/users/")
def users():
    print("users")
    mysql = connectToMySQL("users")
    all_users = mysql.query_db("SELECT * FROM users;") 
    return render_template("index.html", users = all_users)

@app.route("/users/new")
def new():
    print(new)
    mysql = connectToMySQL("users")
    all_users = mysql.query_db("SELECT * FROM users;") 
    print('new user')
    
    return render_template("add_user.html")

@app.route("/users/add", methods=["POST"])
def add_user_to_db():
    mysql = connectToMySQL('users')
    print('add user')
    query = "INSERT INTO users(full_name, email, created_at, updated_at) VALUES (%(n)s, %(e)s, NOW(), NOW());"
    data = {
        'n': request.form["full_name"],
        'e': request.form["email"]
    }
    new_user_id = mysql.query_db(query, data)
    return redirect("/users")

@app.route("/users/edit/<id>")
def edit_user_in_db(id):
    mysql = connectToMySQL("users")
    data={"id":id}
    all_users = mysql.query_db("SELECT * FROM users where users_id = %(id)s;",data) 
    print("edit")
    print(id)
    return render_template("edit_user.html", users=all_users)

@app.route("/users/update/<id>", methods=["POST"])
def update_user_in_db(id):
    mysql = connectToMySQL('users')
    print('update user')
    query = "UPDATE users SET full_name = %(n)s, email = %(e)s where users_id = %(id)s;" 
    data = {
            'n': request.form["full_name"],
            'id': id,
            'e': request.form["email"]
            }
    # if request.form["full_name"] != "":  
    #     query = "UPDATE users SET full_name = %(n)s where users_id = "+id+";"
    #     data = {
    #             'n': request.form["full_name"]
    #     }
    # if request.form["email"] != "":
    #     query += "UPDATE users SET email = %(e)s where users_id = "+id+";"
    #     data = {
    #             'e': request.form["email"]
    #     }
    # else:
    #     return redirect("/users")
    print(query)
    new_user_id = mysql.query_db(query, data)
    print(id)
    return redirect("/users/"+id)

@app.route("/users/<id>")
def user_profile_in_db(id):
    mysql = connectToMySQL("users")
    data={"id":id}
    all_users = mysql.query_db("SELECT * FROM users where users_id = %(id)s;",data)
    
    print("profile")
    print(id)
    return render_template("user_profile.html", users=all_users)

@app.route("/users/delete/<id>")
def delete_user_from_db(id):
    mysql = connectToMySQL('users')
    print('delete')
    query = ("delete from users where users_id =%(id)s;")
    data={"id":id}
    
    new_user_id = mysql.query_db(query,data)
    return redirect("/users")
    
if __name__ == "__main__":
    app.run(debug=True)