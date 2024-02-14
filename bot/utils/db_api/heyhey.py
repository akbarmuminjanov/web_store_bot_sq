import datetime
import sqlite3


class Database:
    
    def __init__(self, path_to_db="data/bot.sqlite3"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False, lastrowid=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        elif fetchone:
            data = cursor.fetchone()
        elif lastrowid:
            data = cursor.lastrowid

        connection.close()
        return data



    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        
        
        return sql+";", tuple(parameters.values())
        
    # @staticmethod
    # def format_args(sql, parameters: dict):
    #     conditions =[]
    #     for item in parameters.keys():
    #         conditions.append(f"{item} = ?")
            
    #     sql += " AND " .join(conditions)
    #     return sql, tuple(parameters.values())
    
    
    # ======================================= Userlar uchun ===========================================
    

    def add_user(self, id: int, full_name: str,  phone_number: str = None, username:str=None, language: str = 'uz'):
        sql = """INSERT INTO main_user(id, full_name, phone_number, username, language) VALUES(?, ?, ?, ?, ?)"""
        self.execute(sql, parameters=(id, full_name, phone_number, username,  language), commit=True)


    def select_all_users(self):
        sql = """SELECT * FROM main_user"""
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM main_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM main_user;", fetchone=True)


    def update_user_phone_number(self, phone_number, id):
        # SQL_EXAMPLE = "UPDATE main_user SET email=mail@gmail.com WHERE id=12345"

        sql = f"""UPDATE main_user SET phone_number=? WHERE id=?"""
        return self.execute(sql, parameters=(phone_number, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM main_user WHERE TRUE", commit=True)



    #=====================================Kategoriyalar uchun ==========================================
    
    def select_all_categories(self):
        sql = "SELECT * FROM main_category;"
        return  self.execute(sql, fetchall=True)
    
    def count_categories(self):
        sql = "SELECT COUNT(*) FROM main_category;"
        return  self.execute(sql, fetchone=True)
    
    def select_category(self, **kwargs):
        sql = "SELECT * FROM main_category WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        
        return  self.execute(sql, parameters=parameters, fetchone=True)
    
    #===================================Sub kategoriyalar uchun ======================================

    def select_all_subcategories(self):
        sql = "SELECT * FROM main_subcategory;"
        return  self.execute(sql, fetchall=True)
    
    
    def count_subcategories(self):
        sql = "SELECT COUNT(*) FROM main_subcategory;"
        return  self.execute(sql, fetchval=True)
    
    def select_subcategory(self, **kwargs):
        sql = "SELECT * FROM main_subcategory WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return  self.execute(sql, parameters=parameters, fetchone=True)
    
    
    def select_subcategories(self, **kwargs):
        sql = "SELECT * FROM main_subcategory WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        
        print(sql)
        return  self.execute(sql, *parameters, fetchall=True)


#------------------------- Mahsulotlar uchun ---------------------------------------
    
    def select_all_products(self):
        sql = "SELECT * FROM main_product;"
        return  self.execute(sql, fetchall=True)
    
    
    def count_products(self):
        sql = "SELECT COUNT(*) FROM main_product;"
        return  self.execute(sql, fetchone=True)
    
    def select_product(self, **kwargs):
        sql = "SELECT * FROM main_product WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return  self.execute(sql, *parameters, fetchone=True)
    
    def select_products(self, **kwargs):
        sql = "SELECT * FROM main_product WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return  self.execute(sql, *parameters, fetchall=True)

#=============================== Cart Uchun ===========================================

    # def select_cart(self, **kwargs):
    #     sql = "SELECT * FROM main_cart WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return self.execute(sql, *parameters, fetchone=True)
    
    
    
    def select_user_products(self, **kwargs):
        sql = "SELECT * FROM main_user_products WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return self.execute(sql, (*parameters,), fetchall=True)
    
    
    def add_product_to_cart(self, user_id, product_id):
        try:
            data = (user_id, product_id)
            sql = "INSERT INTO main_user_products(user_id, product_id) VALUES(?, ?)"
            return self.execute(sql, commit=True, parameters=data)
        
        except sqlite3.IntegrityError:
            return "added-before"
        
        except Exception as err:
            print("Error!")
            return "error"
        
    
    def clear_user_cart(self, user_id):
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # History yaratish
        sql = "INSERT INTO main_history (created, status, user_id) VALUES (?, ?, ?)"
        history_id = self.execute(sql, (current_datetime, 'preparing', user_id), commit=True, lastrowid=True)
        
        
        products = self.select_user_products(user_id=str(user_id))
        
        for product in products:
            sql = "INSERT INTO main_history_products (history_id, product_id) VALUES (?, ?)"
            self.execute(sql, (history_id, product[2]), commit=True)

        sql = "DELETE FROM main_user_products WHERE user_id = ?"
        return self.execute(sql, (str(user_id),), commit=True)


    def select_user_histories(self, **kwargs):
        sql = "SELECT * FROM main_history WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return  self.execute(sql, (*parameters,), fetchall=True)
    

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")