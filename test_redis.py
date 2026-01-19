import redis
import os
from dotenv import load_dotenv

load_dotenv()

def test_redis_connection():
    try:
        # Conectar a Redis en tu VPS Contabo
        redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', '147.93.3.53'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True,
            socket_connect_timeout=5
        )
        
        # Test ping
        if redis_client.ping():
            print("✅ Conexión exitosa a Redis en VPS Contabo")
            print(f"📍 Host: {os.getenv('REDIS_HOST', '147.93.3.53')}")
            print(f"🔌 Puerto: {os.getenv('REDIS_PORT', 6379)}")
            
            # Test básico de escritura/lectura
            redis_client.set('test_key', 'test_value')
            value = redis_client.get('test_key')
            print(f"📝 Test write/read: {value}")
            redis_client.delete('test_key')
            
            # Info del servidor
            info = redis_client.info('server')
            print(f"🖥️  Redis version: {info.get('redis_version')}")
            
            return True
    except redis.ConnectionError as e:
        print(f"❌ Error de conexión a Redis: {e}")
        print("\n🔧 Verificaciones:")
        print("   1. ¿El puerto 6379 está abierto en tu VPS?")
        print("   2. ¿Redis está corriendo en Portainer?")
        print("   3. ¿Tu firewall permite conexiones al puerto 6379?")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    test_redis_connection()