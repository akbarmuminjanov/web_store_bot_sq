# from typing import Union

# import asyncpg
# from asyncpg import Connection
# from asyncpg.pool import Pool
# import json
# from data import config

# class Database:

#     def init(self):
#         self.pool: Union[Pool, None] = None
        

#     async def create(self):
#         self.pool = await asyncpg.create_pool(
#             user=config.DB_USER,
#             password=config.DB_PASS,
#             host=config.DB_HOST,
#             database=config.DB_NAME
#         )
        
    

#     async def execute(self, command, *args,
#                       fetch: bool = False,
#                       fetchval: bool = False,
#                       fetchrow: bool = False,
#                       execute: bool = False
#                       ):
#         async with self.pool.acquire() as connection:
#             connection: Connection
#             async with connection.transaction():
#                 if fetch:
#                     result = await connection.fetch(command, *args)
#                 elif fetchval:
#                     result = await connection.fetchval(command, *args)
#                 elif fetchrow:
#                     result = await connection.fetchrow(command, *args)
#                 elif execute:
#                     result = await connection.execute(command, *args)
#             return result

#     # async def create_table_users(self):
#     #     sql = """
#     #     CREATE TABLE IF NOT EXISTS main_user (
#     #     id SERIAL PRIMARY KEY,
#     #     first_name VARCHAR(255) NOT NULL,
#     #     username varchar(255) NULL,
#     #     user_id BIGINT NOT NULL UNIQUE 
#     #     );
#     #     """
#     #     await self.execute(sql, execute=True)

#     @staticmethod
#     def format_args(sql, parameters: dict):
#         sql += " AND ".join([
#             f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
#                                                           start=1)
#         ])
#         return sql, tuple(parameters.values())
    
    
#     #-------------------------------FOR USERS-----------------------------------------
    
#     async def add_user(self, full_name,  user_id, phone_number=None, username=None):
#         sql = "INSERT INTO main_user (full_name, user_id, username, phone_number) VALUES($1, $2, $3, $4) returning *"
#         return await self.execute(sql, full_name, user_id, username, phone_number, fetchrow=True)

#     async def select_all_users(self):
#         sql = "SELECT * FROM main_user"
#         return await self.execute(sql, fetch=True)

#     async def select_user(self, **kwargs):
#         sql = "SELECT * FROM main_user WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetchrow=True)

#     async def count_users(self):
#         sql = "SELECT COUNT(*) FROM main_user"
#         return await self.execute(sql, fetchval=True)

#     async def update_user_username(self, username, user_id):
#         sql = "UPDATE main_user SET username=$1 WHERE user_id=$2"
#         return await self.execute(sql, username, user_id, execute=True)

#     async def delete_users(self):
#         await self.execute("DELETE FROM main_user WHERE TRUE", execute=True)

#     async def drop_users(self):
#         await self.execute("DROP TABLE main_user", execute=True)
        
        

#     #------------------------- Get Categories -------------------------------
        
#     async def select_all_categories(self):
#         sql = "SELECT * FROM main_category"
#         return await self.execute(sql, fetch=True)
    
#     async def count_categories(self):
#         sql = "SELECT COUNT(*) FROM main_category"
#         return await self.execute(sql, fetchval=True)
    
#     async def select_category(self, **kwargs):
#         sql = "SELECT * FROM main_category WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetchrow=True)
    
#     #------------------------ Get SubCategories ----------------------------
    
    
#     async def select_all_subcategories(self):
#         sql = "SELECT * FROM main_subcategory"
#         return await self.execute(sql, fetch=True)
    
    
#     async def count_subcategories(self):
#         sql = "SELECT COUNT(*) FROM main_subcategory"
#         return await self.execute(sql, fetchval=True)
    
#     async def select_subcategory(self, **kwargs):
#         sql = "SELECT * FROM main_subcategory WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetchrow=True)
    
    
#     async def select_subcategories(self, **kwargs):
#         sql = "SELECT * FROM main_subcategory WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetch=True)
    
    
    
# #------------------------- Get Products ---------------------------------------
    
#     async def select_all_products(self):
#         sql = "SELECT * FROM main_product"
#         return await self.execute(sql, fetch=True)
    
    
#     async def count_products(self):
#         sql = "SELECT COUNT(*) FROM main_product"
#         return await self.execute(sql, fetchval=True)
    
#     async def select_product(self, **kwargs):
#         sql = "SELECT * FROM main_product WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetchrow=True)
    
    
#     async def select_products(self, **kwargs):
#         sql = "SELECT * FROM main_product WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetch=True)
    
    
    
# #---------------------------- User Carts ------------------------------------------


# # Later