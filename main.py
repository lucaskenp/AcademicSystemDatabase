import sqlite3

class Database:
    db_name = 'sistema_academico.db'

       
    def run_query(self, query, parameters = ()):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(query, parameters)
        except sqlite3.Error as e:
            print(f"Erro : {e}")
        return cursor,conn
    def select_values(self,name_table):
        query = f"""
            SELECT * FROM {name_table}
        """
        cursor, conn = self.run_query(query)
        data = cursor.fetchall()
        conn.close()
        print(data)
    
    def get_info_table(self,name_table):
        query = f"""
            PRAGMA table_info({name_table})
        """
        cursor, conn = self.run_query(query)
        colunas = cursor.fetchall()
        tipos_colunas = {}
        nomes_colunas = [info[1] for info in colunas]
        tipos_colunas = [info[2] for info in colunas]
        chave_primaria = [info[5] for info in colunas]
        conn.close()
        return nomes_colunas, tipos_colunas, chave_primaria

    def insert_values(self,name_table, parameters = ()):
        valores = ', '.join(['?'] * len(parameters))
        
        query = f"""
            INSERT INTO {name_table} VALUES ({valores});
        """
        cursor, conn = self.run_query(query,parameters)
        conn.commit()
        conn.close()
        self.select_values(name_table)
    #"UPDATE {name_table} SET {name_coluna} = ?, {name_coluna} = ?, .... WHERE {name_pk} = ?"
    def update_values(self,name_table, parameters = ()):
        nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(name_table)
        index_pk = chaves_primarias.index(1)
        query = f" UPDATE {name_table} SET "
    
        for i in range(len(nomes_colunas)):
            if i != index_pk:
                query += f'{nomes_colunas[i]} = ?'
                if(i != (len(nomes_colunas)-1)):
                    query += ', '
        query += f' WHERE {nomes_colunas[index_pk]} = ?'
        
        cursor, conn = self.run_query(query,parameters)
        conn.commit()
        conn.close()
        self.select_values(name_table)
    #DELETE FROM {name_table} WHERE {name_pk} = ?;
    def delete_values(self, name_table, parameters = ()):
        nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(name_table)
        pk_colunas = []
        for i in chaves_primarias:
            if i != 0:
                pk_colunas.append(nomes_colunas[i-1])
                
        len_pks = len(pk_colunas)        
        query = f" DELETE FROM {name_table} WHERE "
        
        for i in range(len_pks):
           query += f'{pk_colunas[i]} = ? '
           if(i != (len_pks - 1)):
               query += 'AND '
            
        cursor, conn = self.run_query(query,parameters)
        conn.commit()
        conn.close()
        print("----------------------Valores restantes-----------------------\n")
        print("\n")
        self.select_values(name_table)  
        print("\n")
        print("--------------------------------------------------------------\n")

    # Função para mapear o tipo de dado Python para o tipo de dado SQL
    def converter_valor_para_tipo(self,valor, tipo_esperado):
        try:
            if tipo_esperado == 'INTEGER' or tipo_esperado =='NUMERIC':
                return int(valor)
            elif tipo_esperado == 'REAL':
                return float(valor)
            elif tipo_esperado == 'TEXT':
                return str(valor)
            elif tipo_esperado == 'BOOLEAN':
                return bool(int(valor))
            else:
                return valor
        except ValueError:
            print("Erro ao converter valor")
            return None  # Retorna None se a conversão falhar
    def verificar_chave_primaria_existe(self, name_table, parameters = ()):
        nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(name_table)
        index_pk = chaves_primarias.index(1)
        query = f"SELECT 1 FROM {name_table} WHERE {nomes_colunas[index_pk]} = ?"
        cursor, conn = self.run_query(query,parameters)  
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return True  # A chave primária existe na tabela
        else:
            return False  # A chave primária não existe na tabela

def get_data(db):
    names_table = ['aluno','curso','disciplina','professor','turma']
    print("----------------------Ler valores de--------------------\n")
    print("                       1. Aluno\n")
    print("                       2. Curso\n")
    print("                       3. Disciplina\n")
    print("                       4. Professor\n")
    print("                       5. Turma\n")
    print("--------------------------------------------------------\n")
    try:
        index = int(input('Escolha uma opção\n'))
        index -= 1
    except ValueError:
        print("Opção digitada inválida")
        return
    
    if(index > (len(names_table) - 1) or index < 0):
        print(" Opção Inválida \n")
        return
    db.select_values(names_table[index])
    
def add_data(db):
    names_table = ['aluno','curso','disciplina','professor','turma']
    print("-------------------Adicionar valores de-----------------\n")
    print("                      1. Aluno\n")
    print("                      2. Curso\n")
    print("                      3. Disciplina\n")
    print("                      4. Professor\n")
    print("                      5. Turma\n")
    print("--------------------------------------------------------\n")
    try:
        index = int(input('Escolha uma opção\n'))
        index -= 1
    except ValueError:
        print("Opção digitada inválida")
        return
    
    if(index > (len(names_table) - 1) or index < 0):
        print(" Opção Inválida \n")
        return
    print(f"-----------Atributos de {names_table[index]}-----------\n")
    nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(names_table[index])
    print(f"Colunas da tabela {names_table[index]} e seus tipos respectivamente: \n{nomes_colunas} \n{tipo_colunas}")
    print("\n")
    print("--------------------------------------------------------\n")
    parametros = []
    for i in range(len(nomes_colunas)):
        valor = input(f'Escreva o valor da coluna {nomes_colunas[i]}\n')
        parametros.insert(i,db.converter_valor_para_tipo(valor,tipo_colunas[i]))
        
    db.insert_values(names_table[index],parametros)
    print("--------------------------------------------------------\n")
    
def update_data(db):
    names_table = ['aluno','curso','disciplina','professor','turma']
    print("--------------------Atualizar valores de----------------\n")
    print("                     1. Aluno\n")
    print("                     2. Curso\n")
    print("                     3. Disciplina\n")
    print("                     4. Professor\n")
    print("                     5. Turma\n")
    print("--------------------------------------------------------\n")
    try:
        index = int(input('Escolha uma opção\n'))
        index -= 1
    except ValueError:
        print("Opção digitada inválida")
        return
    
    if(index > (len(names_table) - 1) or index < 0):
        print(" Opção Inválida \n")
        return
    
    print(f"-----------Atributos de {names_table[index]}-----------\n")
    print("\n")
    nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(names_table[index])
    print(f"Colunas da tabela {names_table[index]} e seus tipos respectivamente: \n{nomes_colunas} \n{tipo_colunas}")
    print("\n")
    print("---------------Lista dos valores da tabela--------------\n")
    print("\n")
    db.select_values(names_table[index])
    print("\n")
    print("--------------------------------------------------------\n")

    index_pk = chaves_primarias.index(1)
    pk_coluna = nomes_colunas[index_pk]
    pk_value = input(f'Qual valor da coluna {pk_coluna}(PK) você deseja selecionar para atualizar?\n')
    pk_value = db.converter_valor_para_tipo(pk_value,tipo_colunas[index_pk])
            
    parametros = []
    for i in range(len(nomes_colunas)):
        if nomes_colunas[i] != pk_coluna:
            valor = input(f'Escreva o novo valor da coluna {nomes_colunas[i]}\n')
            parametros.append(db.converter_valor_para_tipo(valor,tipo_colunas[i]))
    
    parametros.append(pk_value)    
    db.update_values(names_table[index], parametros)
    print("--------------------------------------------------------\n")
    
def delete_data(db):
    names_table = ['aluno','curso','disciplina','professor','turma']
    print("-------------------Deletar valores de-------------------\n")
    print("                     1. Aluno\n")
    print("                     2. Curso\n")
    print("                     3. Disciplina\n")
    print("                     4. Professor\n")
    print("                     5. Turma\n")
    print("--------------------------------------------------------\n")
    try:
        index = int(input('Escolha uma opção\n'))
        index -= 1
    except ValueError:
        print("Opção digitada inválida")
        return
    
    if(index > (len(names_table) - 1) or index < 0):
        print(" Opção Inválida \n")
        return
    
    print(f"------------Atributos de {names_table[index]}------------\n")
    print("\n")
    nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(names_table[index])
    print(f"Colunas da tabela {names_table[index]} e seus tipos respectivamente: \n{nomes_colunas} \n{tipo_colunas}")
    print("\n")
    print("---------------Lista dos valores da tabela----------------\n")
    print("\n")
    db.select_values(names_table[index])
    print("\n")
    print("----------------------------------------------------------\n")

    index_pk = chaves_primarias.index(1)
    pk_coluna = nomes_colunas[index_pk]
    pk_value = input(f'Qual valor da coluna {pk_coluna}(PK) você deseja selecionar para deletar?\n')
    pk_value = db.converter_valor_para_tipo(pk_value,tipo_colunas[index_pk])
    parametros = []
    parametros.append(pk_value)    
    db.delete_values(names_table[index], parametros)

def register_data(db):
    names_table = ['curso_possui_aluno','curso_possui_discip','turma_possui_aluno','turma_possui_prof']
    print("-------------------------Cadastrar----------------------\n")
    print("                  1. Aluno em um curso\n")
    print("                  2. Disciplina em algum curso\n")
    print("                  3. Aluno em alguma turma\n")
    print("                  4. Professor em alguma turma\n")
    print("--------------------------------------------------------\n")
    try:
        index = int(input('Escolha uma opção\n'))
        index -= 1
    except ValueError:
        print("Opção digitada inválida")
        return
    
    if(index > (len(names_table) - 1) or index < 0):
        print(" Opção digitada inválida \n")
        return
    
    print(f"-----------Atributos de {names_table[index]}-----------\n")
    nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(names_table[index])
    print(f"Colunas da tabela {names_table[index]} e seus tipos respectivamente: \n{nomes_colunas} \n{tipo_colunas}")
    print("\n")
    print("--------------------------------------------------------\n")
    parametros = []
    for i in range(len(nomes_colunas)):
        valor = input(f'Escreva o valor da coluna {nomes_colunas[i]}\n')
        parametros.insert(i,db.converter_valor_para_tipo(valor,tipo_colunas[i]))
        
    db.insert_values(names_table[index],parametros)
    print("--------------------------------------------------------\n")

def delete_registers_data(db):
    names_table = ['curso_possui_aluno','curso_possui_discip','turma_possui_aluno','turma_possui_prof']
    print("-------------------Deletar valores de-------------------\n")
    print("                  1. Aluno em um curso\n")
    print("                  2. Disciplina em algum curso\n")
    print("                  3. Aluno em alguma turma\n")
    print("                  4. Professor em alguma turma\n")
    print("--------------------------------------------------------\n")
    try:
        index = int(input('Escolha uma opção\n'))
        index -= 1
    except ValueError:
        print("Opção digitada inválida")
        return
    
    if(index > (len(names_table) - 1) or index < 0):
        print(" Opção Inválida \n")
        return
    
    print(f"------------Atributos de {names_table[index]}------------\n")
    print("\n")
    nomes_colunas, tipo_colunas, chaves_primarias = db.get_info_table(names_table[index])
    print(f"Colunas da tabela {names_table[index]} e seus tipos respectivamente: \n{nomes_colunas} \n{tipo_colunas}")
    print("\n")
    print("---------------Lista dos valores da tabela----------------\n")
    print("\n")
    db.select_values(names_table[index])
    print("\n")
    print("----------------------------------------------------------\n")
    
    pk_colunas = []
    for i in chaves_primarias:
        pk_colunas.append(nomes_colunas[i-1])
            
    pk_value = []
    for pk_coluna in pk_colunas:
        pk_value_input = input(f'Qual valor da coluna {pk_coluna}(PK) você deseja selecionar para deletar?\n') 
        pk_value.append(db.converter_valor_para_tipo(pk_value_input,tipo_colunas[nomes_colunas.index(pk_coluna)])) 
      
    db.delete_values(names_table[index], pk_value)
                 
def loop(db):
    choice = 0
    while choice != 7:
        print("------------------------------------------------------------------------\n")
        print("                  1. Ler valores\n")
        print("                  2. Adicionar valores\n")
        print("                  3. Atualizar valores\n")
        print("                  4. Deletar valores\n")
        print("                  5. Cadastros de alunos, disciplinas e professores\n")
        print("                  6. Deletar cadastros de alunos, disciplinas e professores\n")
        print("                  7. Quit\n")
        print("------------------------------------------------------------------------\n")
        try:
            choice = int(input('Escolha uma opção\n'))
            if(choice == 1):
                get_data(db)
            elif(choice == 2):
                add_data(db)
            elif(choice == 3):
                update_data(db)
            elif(choice == 4):
                delete_data(db)
            elif(choice == 5):
                register_data(db)
            elif(choice == 6):
                delete_registers_data(db)
                
        except ValueError:
           print("\n Valor digitado inválido!\n")
        

if __name__ == '__main__':
    db = Database()
    loop(db)