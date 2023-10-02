import sqlite3

def create_table():
    con = sqlite3.connect("sistema_academico.db")
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    
    cur.execute ("""
    CREATE TABLE IF NOT EXISTS curso (
        codigo INTEGER PRIMARY KEY,
        nome   TEXT,
        turno  TEXT
    );
    """)

    cur.execute ("""
    CREATE TABLE IF NOT EXISTS aluno (
        matricula INTEGER PRIMARY KEY,
        nome      TEXT,
        telefone  NUMERIC,
        email     TEXT
    );
    """)

    cur.execute ("""
    CREATE TABLE IF NOT EXISTS professor (
        siape       INTEGER PRIMARY KEY,
        nome        TEXT,
        salario     INTEGER,
        telefone    NUMERIC,
        email       TEXT
    );
    """)
    
    cur.execute ("""
    CREATE TABLE IF NOT EXISTS disciplina (
        codigo          INTEGER PRIMARY KEY,
        descricao       TEXT,
        carga_horaria   INTEGER
    );
    """)

    cur.execute ("""
    CREATE TABLE IF NOT EXISTS turma (
        codigo            INTEGER PRIMARY KEY,
        disciplina_codigo INTEGER REFERENCES disciplina (codigo) ON DELETE CASCADE
                                                                ON UPDATE CASCADE
                                NOT NULL,
        semestre          INTEGER,
        horario           INTEGER
    );

    """)

    cur.execute ("""
    CREATE TABLE IF NOT EXISTS turma_possui_prof (
        professor_siape INTEGER REFERENCES professor (siape) ON DELETE CASCADE
                                                            ON UPDATE CASCADE,
        turma_codigo    INTEGER REFERENCES turma (codigo) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
        PRIMARY KEY (
            professor_siape,
            turma_codigo
        )
    );

    """)

    cur.execute ("""
    CREATE TABLE IF NOT EXISTS curso_possui_discip (
        curso_codigo        INTEGER REFERENCES curso (codigo) ON DELETE CASCADE
                                                            ON UPDATE CASCADE,
        disciplina_codigo   INTEGER REFERENCES disciplina (codigo) ON DELETE CASCADE
                                                                ON UPDATE CASCADE,
        PRIMARY KEY (
            curso_codigo,
            disciplina_codigo
        )
    );

    """)

    cur.execute ("""
    CREATE TABLE IF NOT EXISTS curso_possui_aluno (
        curso_codigo        INTEGER REFERENCES curso (codigo) ON DELETE CASCADE
                                                            ON UPDATE CASCADE,
        aluno_matricula     INTEGER REFERENCES aluno (matricula) ON DELETE CASCADE
                                                            ON UPDATE CASCADE,
        PRIMARY KEY (
            curso_codigo,
            aluno_matricula
        )
    );

    """)

    cur.execute ("""
    CREATE TABLE IF NOT EXISTS turma_possui_aluno (
        turma_codigo        INTEGER REFERENCES turma (codigo) ON DELETE CASCADE
                                                            ON UPDATE CASCADE,
        aluno_matricula     INTEGER REFERENCES aluno (matricula) ON DELETE CASCADE
                                                            ON UPDATE CASCADE,
        freq                INTEGER,
        media               INTEGER,
        
        PRIMARY KEY (
            turma_codigo,
            aluno_matricula
        )
    );

    """)

    con.commit()
    

create_table()
#cur.execute("CREATE TABLE sqlitestudio_temp_table AS SELECT *FROM movie")

#cur.execute("DROP TABLE movie")

#cur.execute("""
#    CREATE TABLE movie (
#        title TEXT    PRIMARY KEY
#                    NOT NULL,
#        year  NUMERIC NOT NULL,
#        score NUMERIC NOT NULL
#    )          
#""")
#
#cur.execute("""
#    INSERT INTO movie (
#                      title,
#                      year,
#                      score
#                  )
#                  SELECT title,
#                         year,
#                         score
#                    FROM sqlitestudio_temp_table
#""")
#
#cur.execute("""
#   DROP TABLE sqlitestudio_temp_table
#""")
