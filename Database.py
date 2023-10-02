import sqlite3

class Database:
    db_name = 'sistema_academico.db'
    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    def get_values(self):
        query = 'SELECT * FROM aluno'
        db_rows = self.run_query(query)
        print(db_rows)
        
    def write_values(self,name_table, parameters):
        query = "INSERT INTO" + name_table + "VALUES(?, ?, ?)"
        #parameters = ('Monty Python Live at the Hollywood Bowl', 1982, 7.9)
        db_rows = self.run_query(query, parameters)
        print(db_rows)
    
    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()
  