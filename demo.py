from flask import Flask, render_template, request, abort
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    c = sqlite3.connect("project.db")
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    cur.execute("select * from student")
    r = cur.fetchall()
    c.close()
    return render_template('index.html', row = r)

@app.route("/insert")
def insert():
    return render_template('insert.html')

@app.route("/update")
def update():
    return render_template('edit.html')

@app.route("/delete")
def delete():
    return render_template('delete.html')

@app.route('/deleterecord', methods = ["POST"])
def deleterecord():
    try:
        regno = request.form['regno']
        email = request.form['email']
        db = sqlite3.connect('project.db')
        cursor = db.cursor()
        cursor.execute("delete from student where regno = ? and email = ?", (regno, email))
        rows_affected = cursor.rowcount

        if rows_affected == 0:
            db.rollback()
            message = "Invalid Credentials!"
        else:
            db.commit()
            message = "Deleted Successfully!"

    except Exception as e:
        print(f"Error: {e}")
        message = "Delete Failed!"
    finally:
        cursor.close()
        db.close()
        return render_template('message.html', message = message)

        
@app.route("/save", methods=["POST",'GET'])
def save():
    if request.method == "POST":
        message = "message"
        try:
            reg = request.form["regno"]
            n = request.form["name"]
            em = request.form["email"]
            mb = request.form["mobile"]
            c = sqlite3.connect('project.db')
            cur = c.cursor()
            cur.execute("insert into student (regno, name, email, mobile) values (?, ?, ?, ?)", (reg, n, em, mb))
            c.commit()
            message = "Inserted Successfully!"
        except Exception as e:
            c.rollback()
            message = e
        finally:
            return render_template("message.html", message = message)

@app.route('/up', methods = ['POST'])
def up():
    msg = "message"
    try:
        reg = request.form["regno"]
        n = request.form["name"]
        em = request.form["email"]
        mb = request.form["mobile"]
        c = sqlite3.connect("project.db")
        cur = c.cursor()
        cur.execute("update student set name = ?, email = ?, mobile = ? where regno = ?", (n, em, mb, reg))
        c.commit()
        msg = "Updated Successfully!"
    except Exception as e:
        msg = e
    finally:
        return render_template("message.html", message = msg)


if __name__ == '__main__':
    app.run(debug=True)