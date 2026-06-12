import mysql.connector


class Connection_db:
    def __init__(self,host,password,root,database):
        self.host=host
        self.password=password
        self.root=root
        self.database=database
        self.connect()
    
    def connect(self):
        self.conn=mysql.connector.connect(
            host=self.host,
            passowrd=self.passowrd,
            root=self.root,
            database=self.database
        )

    def get_connection(self):
        if not self.conn.is_connected():
            self.connect()
        return self.conn
       
        
    
    def create_tables(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS books(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title  VARCHAR(50) NOT NULL,
            author  VARCHAR(50) NOT NULL,
            genre  ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
            is_available bool NOT NULL,
            borrowed_by_member_id int DEFAULT NULL)
            ''' 
            '''
            CREATE TABLE IF NOT EXISTS members(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name  VARCHAR(50) NOT NULL,
            email VARCHAR (50) UNIQUE NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT FALSE ,
            total_borrows INT NOT NULL DEFAULT 0)
            '''
            )
                
connect=Connection_db("localhost","root","root","library_db")
         
            
            

            

                    
    
    