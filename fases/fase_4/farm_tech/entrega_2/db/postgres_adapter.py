import psycopg2
from psycopg2 import sql

class PostgresAdapter:
    """Adaptador para PostgreSQL."""

    def __init__(self, host, port, database, user, password):
        """Inicializa o adaptador."""
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def conectar(self):
        """Estabelece a conexão com o banco de dados."""
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """Executa uma consulta SQL."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Erro ao executar consulta: {str(e)}")
            return False

    def fetch_one(self, query, params=None):
        """Executa uma consulta e retorna um único resultado."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar um registro: {str(e)}")
            return None

    def fetch_all(self, query, params=None):
        """Executa uma consulta e retorna todos os resultados."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar registros: {str(e)}")
            return []

    def insert(self, table, data):
        """Insere um registro na tabela."""
        try:
            columns = data.keys()
            values = [data[column] for column in columns]

            if table == 'plantacoes':
                pk_column = 'id_plantacao'
            elif table == 'sensores':
                pk_column = 'id_sensor'
            elif table == 'dados_sensores':
                pk_column = 'id_dado_sensor'
            else:
                pk_column = f"id_{table[:-1]}"

            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING {};").format(
                sql.Identifier(table),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns)),
                sql.Identifier(pk_column)
            )

            self.cursor.execute(insert_query, values)
            id_inserted = self.cursor.fetchone()[0]
            self.connection.commit()
            return id_inserted
        except Exception as e:
            self.connection.rollback()
            print(f"Erro ao inserir registro: {str(e)}")
            return None

    def update(self, table, data, condition):
        """Atualiza registros na tabela."""
        try:
            set_items = []
            values = []

            for key, value in data.items():
                set_items.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
                values.append(value)

            update_query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
                sql.Identifier(table),
                sql.SQL(', ').join(set_items),
                sql.SQL(condition)
            )

            self.cursor.execute(update_query, values)
            rows_affected = self.cursor.rowcount
            self.connection.commit()
            return rows_affected > 0
        except Exception as e:
            self.connection.rollback()
            print(f"Erro ao atualizar registro: {str(e)}")
            return False

    def delete(self, table, condition):
        """Exclui registros da tabela."""
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE {}").format(
                sql.Identifier(table),
                sql.SQL(condition)
            )

            self.cursor.execute(delete_query)
            rows_affected = self.cursor.rowcount
            self.connection.commit()
            return rows_affected > 0
        except Exception as e:
            self.connection.rollback()
            print(f"Erro ao excluir registro: {str(e)}")
            return False