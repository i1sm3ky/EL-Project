from flask import Flask, request, render_template, redirect
# from Student.StudentPage import StudentMain
from threading import Thread
import csv


app = Flask(__name__)
TimeInterval = 100000

with open("./Teacher/Config/config.txt") as File:
    RoomNo = File.readline().lstrip("Class = ")


@app.route('/', methods=["GET", "POST"])
def TeacherIndex():
    global TimeInterval, PresentStudents
    if request.method == "POST":
        Password = request.form.get("otp_input")
        with open("./Teacher/Config/TempPass.txt", "w") as File:
            File.write(f"Password = { Password }")
        TimeInterval = 1
        # StudentProcess = Thread(target=StudentMain)
        # StudentProcess.setDaemon(True)
        # StudentProcess.start()
        # StudentProcess.join()

    with open("./Teacher/Config/TempStudentList.txt") as File:
        PresentStudents = File.readlines()
    return render_template("TeacherIndex.html", TimeInterval=TimeInterval, RoomNo=RoomNo, PresentStudents=PresentStudents)

@app.route('/Stop')
def StopAttendence():
    global TimeInterval
    TimeInterval = 100000
    return redirect('/')

@app.route('/Export')
def ExportAttendence():
    with open("./Teacher/Attendence.csv", "w") as File:
        Writer = csv.writer(File)
        [Writer.writerow(Student.split()) for Student in ''.join(PresentStudents).split("\n")]
    return redirect('/')

def TeacherMain(debug=False):
    app.run(debug=debug, port=5000)


if __name__ == "__main__":
    TeacherMain(debug=True)
