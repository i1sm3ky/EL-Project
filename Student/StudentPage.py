from flask import Flask, request, render_template


app = Flask(__name__)

with open("./Teacher/Config/config.txt") as File:
    RoomNo = File.readline().lstrip("Class = ")

with open("./Teacher/Config/TempPass.txt") as File:
    CorrectPassword = File.readline().lstrip("Password = ")

def GetStudentDetails(MacAddr):
    global Name, RegNo
    with open("./Teacher/Config/StudentList.txt") as File:
        StudentDetails = File.readlines()
        for Details in StudentDetails:
            Details = Details.split()
            if Details[0] == MacAddr:
                Name = Details[1]
                RegNo = Details[2]

with open("./Teacher/Config/TempStudentList.txt", "w") as File:
    pass

@app.route('/', methods=["GET", "POST"])
def StudentIndex():
    if request.method == "POST":
        Password = request.form.get("otp_input")
        if Password == CorrectPassword:
            GetStudentDetails(request.remote_addr)
            with open("./Teacher/Config/TempStudentList.txt", "r") as File:
                if f"{ Name } { RegNo }" not in File.read():
                    with open("./Teacher/Config/TempStudentList.txt", "a") as File:
                        File.write(f"{ Name } { RegNo }\n")
                    return render_template("StudentIndex.html", AttendenceStatus="Attendence Marked!", RoomNo='')
        else:
            return render_template("StudentIndex.html", AttendenceStatus="Incorrect Password", RoomNo='')
    return render_template("StudentIndex.html", AttendenceStatus="Class Attendence", RoomNo=f"({RoomNo})")


def StudentMain(debug=False):
    app.run(debug=debug, port=5001)


if __name__ == "__main__":
    StudentMain(debug=True)
