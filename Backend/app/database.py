from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from app.models import User, Room, Message, RoomUser


def init_db():
    """
    Inicializa o banco de dados Cassandra:
    - Conecta ao cluster
    - Configura o keyspace
    - Cria tabelas somente se elas não existirem
    """
    cluster = Cluster(["127.0.0.1"])
    session = cluster.connect()

    # Define o keyspace (ajuste conforme necessário)
    keyspace = "realtime_db"
    session.execute(
        f"""
    CREATE KEYSPACE IF NOT EXISTS {keyspace}
    WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
    """
    )

    # Usa o keyspace
    session.set_keyspace(keyspace)

    # Configura o cassandra-cqlengine para usar essa sessão
    connection.set_session(session)

    # Sincroniza os modelos com o Cassandra (cria tabelas apenas se necessário)
    sync_table(User)
    sync_table(Room)
    sync_table(Message)
    sync_table(RoomUser)

    print("Banco de dados inicializado com sucesso!")
