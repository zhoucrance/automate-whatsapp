from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime


cluster = MongoClient("mongodb+srv://crance:crance@cluster0.mgpfz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["medicalAid"]
users = db["users"]


app = Flask(__name__)

#name=""
@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("message")
    number = request.form.get("sender")
    res = {"reply": ""}
    user = users.find_one({"number": number})

    if bool(user) == False:
        res["reply"] += '\n' + (
            "Hi, thanks for contacting *Clientsure*.\nYou can choose from one of the options below: "
            "\n\n 1. *Register*  \n 2. *Customer* *Support*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res["reply"] += '\n' + ("Please enter a valid response")
        if option == 1:
            res["reply"] += '\n' + ("What is your *name* ?")
            users.update_one(
                {"number": number}, {"$set": {"status": "name"}})

        elif option == 2:
            res["reply"] += '\n' + ("You have entered customer support mode")
            users.update_one(
                {"number": number}, {"$set": {"status": "customer_support"}})

    elif user["status"] == "name":
        global name
        name= text
        res["reply"] += '\n' + ("I have noted *"+name +"* What is your *surname* ?")
        users.update_one(
            {"number": number}, {"$set": {"status": "surname"}})

    elif user["status"] == "surname":
        surname = text
        res["reply"] += '\n' + ("I have noted *"+surname +"* What is your *ID* ? *eg* this format : 03-188788F03")
        users.update_one(
            {"number": number}, {"$set": {"status": "id"}})

    elif user["status"] == "id":
        id = text
        res["reply"] += '\n' + ("I have noted *"+id+"* What is your *Date Of Birth* ? *e.g* this format: dd/mm/yy")
        users.update_one(
            {"number": number}, {"$set": {"status": "dob"}})
    elif user["status"] == "dob":
        dob = text
        res["reply"] += '\n' + ("I have noted *"+dob+"* What is your *Phone Number* ? *e.g* this format: 078 492 7848")
        users.update_one(
            {"number": number}, {"$set": {"status": "phone"}})

    elif user["status"] == "phone":
        phone = text
        res["reply"] += '\n' + ("I have noted *"+phone+"* What is your *Address* ?")
        users.update_one(
            {"number": number}, {"$set": {"status": "address"}})

    elif user["status"] == "address":
        address = text
        res["reply"] += '\n' + ("I have noted *"+address+"*. Thanks to you *""* for showing your interest and giving valuable time to *Clientsure Medical Aid Fund*. We are going to cal you within 24 hours👏" )
        users.update_one(
            {"number": number}, {"$set": {"status": "else"}})
    elif user["status"] == "else":
        res["reply"] += '\n' + (
            "Hi, thanks for contacting *Clientsure*.\nYou can choose from one of the options below: "
            "\n\n 1. *Register*  \n 2. *Customer* *Support*")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
    else:
        res["reply"] += '\n' + ("Please enter a valid response")




    return str(res)


if __name__ == "__main__":
    app.run()
