# import mysql.connector

# config = {
#             'user':'root',
#             'password':'',
#             'host':'localhost',
#             'database':'tienda'
# }


# def connection(query):
#     try:
#         conn = mysql.connector.connect(**config)
#         cursor = conn.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except mysql.connector.Error as error:
#         print("Error al conectar a la base de datos:", error)
#         return None
#     finally:
#         if 'conn' in locals():
#             conn.close()

# def select(tabla):
#     try:
#         connection(f"select * from {tabla}")
#     except Exception as error:
#         print(error)