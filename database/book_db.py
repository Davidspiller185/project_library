from db_connection import Connection_DB,connect_db

class BookDB():
    def __init__(self,db_connect:Connection_DB):
        self.connect=db_connect
    
    def create_book(self,data:dict):
      conn=self.connect.get_connection()
      try:
        with conn.cursor(dictionary=True)as cursor:
            cursor.execute(
                '''
                INSERT INTO  books(title,author,genre,is_available,borrowed_by_member_id)
                VALUES (%s,%s,%s,%s,%s) 
                ''',
                (data["title"],data["author"],data["genre"],True,None)

            )
            conn.commit()
            return cursor.lastrowid
      finally:
        conn.close()


    def get_all_books(self):
         conn=self.connect.get_connection()
         try:
            with conn.cursor(dictionary=True)as cursor:
                cursor.execute(
                    '''
                    SELECT * FROM books 
                    
                    '''
                ) 
                return cursor.fetchall()
         finally:
            conn.close()
    
    def get_book_by_id(self,id):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True)as cursor:
               cursor.execute(
                    '''
                    SELECT * FROM books WHERE id = %s
                    ''',
                    (id,)
                )
               return cursor.fetchone()
        finally:
           conn.close()

    def update_book(self,id, data:dict):
       conn=self.connect.get_connection()
       try:
            with conn.cursor(dictionary=True)as cursor:
               set_parts=[f"{key}=%s" for key in data.keys()]
               set_clause=", ".join(set_parts)
               sql=f"UPDATE books SET {set_clause} WHERE id = %s"
               values=list(data.values()) + [id]
               cursor.execute(sql,values)
               conn.commit()
               return cursor.rowcount > 0
       finally:
          conn.close()
    
    def set_available(self,id, val:bool, member_id:int):
       conn=self.connect.get_connection()
       try:
          with conn.cursor(dictionary=True)as cursor:
             cursor.execute(
                '''
                UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE id =%s
                ''',
                (val,member_id,id)
                

             )
             conn.commit()
             return cursor.rowcount >0
       finally:
          conn.close()

    def count_total_books(self):
       conn=self.connect.get_connection()
       try:
          with conn.cursor(dictionary=True)as cursor:
             cursor.execute(
                '''
                SELECT COUNT(*) AS total_books FROM books
                '''
             )
             return cursor.fetchone()
          
       finally:
          conn.close()

    def count_available_books(self):
        conn=self.connect.get_connection()
        try:
          with conn.cursor(dictionary=True)as cursor:
             cursor.execute(
                '''
                SELECT COUNT(*) AS total_books_available FROM books WHERE is_availabale = %s
                '''
                (True,)
             )
             return cursor.fetchone()
        finally:
           conn.close()
    
    def count_borrowed_books(self):
        conn=self.connect.get_connection()
        try:
          with conn.cursor(dictionary=True)as cursor:
             cursor.execute(
                '''
                SELECT COUNT(*) AS total_books_available FROM books WHERE is_availabale = %s
                '''
                (False,)
             )
             return cursor.fetchone()
        finally:
           conn.close()

    def count_by_genre(self,genre):
        conn=self.connect.get_connection()
        try:
          with conn.cursor(dictionary=True)as cursor:
             cursor.execute(
                '''
                SELECT COUNT(*) AS total_books_by_genre FROM books WHERE genre = %s
                '''
                (genre,)
             )
             return cursor.fetchone()
        finally:
           conn.close()
    
    def count_active_borrows_by_member(self,member_id):
        conn=self.connect.get_connection()
        try:
          with conn.cursor(dictionary=True)as cursor:
             cursor.execute(
                '''
                SELECT borrowed_by_member_id, COUNT(*) FROM books WHERE borrowed_by_member_id = %s GROUP BY borrowed_by_member_id 
                '''
                (member_id,)
             )
             return cursor.fetchone()
        finally:
           conn.close()

book=BookDB(connect_db)   


             
          

               
          




