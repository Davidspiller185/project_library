from db_connection import Connection_DB, connect_db

class MemberDB:
    def __init__(self,db_connect:Connection_DB):
        self.connect=db_connect
    
    def create_member(self,data:dict):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    INSERT INTO members(name,email,is_active,total_borrows) VALUES (%s,%s,%s,%s)
                    ''',
                    (data["name"],data["email"],True,0)

                )
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    
    def get_all_members(self):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    SELECT * FROM members
                    '''
                )
                return cursor.fetchall()
        finally:
            conn.close()
    
    def get_member_by_id(self,id):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    SELECT * FROM members WHERE id = %s
                    ''',
                    (id,)
                )
                return cursor.fetchone()
        finally:
            conn.close()

    def update_member(self,id, data:dict):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
               set_parts=[f'{key}=%s' for key in data.keys()] 
               set_clause=", ".join(set_parts)
               sql=f"UPDATE members SET {set_clause} WHERE id = %s"
               values=list[data.values()] + [id]
               cursor.execute(sql,values)
               conn.commit()
               return cursor.rowcount>0
        finally:
            conn.close()

    def deactivate_member(self,id):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    UPDATE members SET is_active = %s WHERE id= %s
                    ''',
                    (False,id)
                )
                conn.commit()
                return cursor.rowcount>0
        finally:
            conn.close()
    
    def activate_member(self,id):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    UPDATE members SET is_active = %s WHERE id= %s
                    ''',
                    (True,id)
                )
                conn.commit()
                return cursor.rowcount>0
        finally:
            conn.close()
    
    def increment_borrows(self,id):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    UPDATE members SET total_borrow = total_borrow+1 WHERE id = %s
                    ''',
                    (id,)
                )
                conn.commit()
                return cursor.rowcount>0
        finally:
            conn.close()
    
    def count_active_members(self):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    SELECT COUNT(*) AS total FROM members WHERE is_active = %s 
                    ''',
                    (True,)

                )
                return cursor.fetchone()
        finally:
            conn.close()
    
    def get_top_member(self):
        conn=self.connect.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    '''
                    SELECT MAX(total_borrows) AS max_borrows FROM members
                    '''
                )
                return cursor.fetchone()
        finally:
            conn.close()

    


member=MemberDB(connect_db)