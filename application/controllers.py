from flask import render_template, redirect, url_for
from flask import current_app as app
from flask_security import login_required, current_user
from flask import request
from .models import Complaint
from .database import db


@app.route("/", methods = ["GET", "POST"])
@login_required
def home():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# TODO Create controllers for /profile and /raisecomplaint
@app.route("/profile")
@login_required
def profile():
    complaints = Complaint.query.filter_by(userid = current_user.id).all()
    
    return render_template("profile.html", complaints = complaints)


@app.route("/raisecomplaint", methods = ["GET", "POST"])
@login_required
def raisecomplaint():
    if request.method == "GET":
        return render_template("raisecomplaint.html")
    elif request.method == "POST":
        print(current_user.id)
        formvals = request.form
        value = Complaint(current_user.id,
            formvals["hname"], 
            formvals["cat"],
            formvals["pname"],
            formvals["avail"],
            int(formvals["rno"]),
            int(formvals["mno"]), 
            formvals["desc"],
            )
        db.session.add(value)
        db.session.commit()
        '''
        self.userid = userid
        self.hostelName = hostelName
        self.category = category
        self.name = name
        self.availability = avail
        self.room_no = rno
        self.phone_no = pno
        self.description = desc


        hname
        cat
        pname
        avail
        rno
        mno
        desc
        '''
        return render_template("raisecomplaint.html")


@app.route("/verifyadmin", methods = ["GET", "POST"])
@login_required
def verifyadmin():
    if request.method == "GET":
        return render_template("verifyadmin.html")
    elif request.method == "POST":
        password = request.form["password"]
        pendingComplaints = Complaint.query.filter(Complaint.status == "Pending").all()
        escalatedComplaints = Complaint.query.filter(Complaint.status == "Escalated").all()
        allcomplaints = [_ for _ in pendingComplaints] + [_ for _ in escalatedComplaints]
        return render_template("verifyadmin.html", password = password, allcomplaints = allcomplaints)



@app.route("/verifyadmin/accept/<cid>", methods = ["GET", "POST"])
@login_required
def acceptcomplaint(cid):
    updatethis = Complaint.query.filter_by(id = cid).first()
    updatethis.status = "Resolved"
    updatethis.extra = "-"
    db.session.commit()
    return redirect(url_for("verifyadmin"))

@app.route("/verifyadmin/reject/<cid>", methods = ["GET", "POST"])
@login_required
def rejectcomplaint(cid):
    updatethis = Complaint.query.filter_by(id = cid).first()
    updatethis.status = "Rejected"
    updatethis.extra = "-"
    db.session.commit()
    return redirect(url_for("verifyadmin"))

@app.route("/verifyadmin/escalate/<cid>", methods = ["GET", "POST"])
@login_required
def escalatecomplaint(cid):
    updatethis = Complaint.query.filter_by(id = cid).first()
    level = updatethis.extra
    updatethis.status = "Escalated"
    if level == "-":
        updatethis.extra = "Level 2"
    elif level == "Level 2":
        updatethis.extra = "Level 3"
    db.session.commit()
    return redirect(url_for("verifyadmin"))