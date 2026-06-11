# project_library
 המערכת בונה שרת שמתחבר לממסד נתונים SQL ואחראית לנהל את מערכת הספרים דרך טבלת הספרים ואת מערכת המנויים לספרייה ובודקת האם הספר פנוי להשאלה או לא ובודקת האם החבר פעיל בספרייה או לא ונותנת אפשרות לפעולות CRUD על הספרים ועל מנויי הספרייה

# קוד ליצירת docker עם mysql
pip install mysql-connector-python

docker run --name mysql-w7 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:8

# מבנה התיקיות

project_library/
│
│
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   └── app.log
│   └── logger_config.py   
│
├── README.md
├── requirements.txt
└── .gitignore

# מבנה הטבלאות
**טבלת books — שדות**
id - int
title - str
author -str
genre -str
is_available -bool
borrowed_by_member_id - int|Null

**טבלת members - שדות**
id - int
name - str
email- str
is_active - bool
total_borrows - int

# חוקי מערכת
**1 - יצירת ספר**
המשתמש שולח title/author/genre — המערכת מוסיפה is_available=True, borrowed_by=NULL

**2 - genre**
חייב להיות Fiction / Non-Fiction / Science / History / Other — כל ערך אחר מחזיר שגיאה
יש לוודא הן בהוספה (POST) והן בעדכון (PATCH)

**3 - יצירת חבר**
המשתמש שולח name/email — המערכת מוסיפה is_active=True, total_borrows=0

**4 - email**
חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה
**5 - חבר לא פעיל**
אם is_active=False — אי אפשר להשאיל ספר

**6 - ספר לא זמין**
אי אפשר להשאיל ספר שכבר מושאל (is_available=False)

**7 - מקסימום ספרים**
חבר לא יכול להחזיק יותר מ-3 ספרים 
בו-זמנית
**8 -  החזרת ספר**
ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו

# רשימת endpoint
**books** 
@app.post("/books")
@app.get("/books")
@app.Patch("/books/{id}")
@app.patch("/books/{id}/borrow/{member_id}")
@app.patch("/books/{id}/return/{member_id}")

**members**
@app.post("/members")
@app.get("/members")
@app.get("/members/{id}")
@app.patch("/members/{id}")
@app.patch("/members/{id}/deactivate")
@app.patch("/members/{id}/activate")

**reports**
@app.get("/reports/summary")
@app.get("/reports/books-by-genre")
@app.get("/reports/top-member")

# זרימת המערכת
**book request**
client ask to borrowed a book > the request came to books oop and check if the book is available, if available > return a sussces message and > update the collumn is_available in the SQL db to false, if not return a messages that the borrow is not suscssec 

**members request**
client ask to be a member > the request came to members oop and check if he already a member > if yes> return to the client message that he is already excsiste, if not >
update the SQL db with his details member and return message succsses to the client.

**report request**
client ask a genre > the request came to report oop and check if the genere exsicte > the oop bring from the SQL db the genre and the count of this genre in the library,
if genere not exciste > return to the client a message that this genre not in the library.

# הוראות הרצה

** python -m  venv.venv
 
** source .venv/Scripts/activate

** pip frezz > requierment.txt

** pip install 'fastapi[standard]'

** uvicorn main:app --reloade 

 



