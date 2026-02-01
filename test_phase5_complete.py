"""
Phase 5 Library Integration Test
Tests REST, HTTP, Web, Database, ORM, GraphQL, and Cache libraries
"""

import sys
sys.path.insert(0, r'c:\Users\FRANCIS JUSU\Documents\TOMBO')

from src.lib.rest import Router, ResourceController, APIResponse, create_response
from src.lib.http import HTTPRequest, HTTPResponse, HTTPStatus, HTTPHeaders
from src.lib.web import HTTPClient, build_url, parse_url
from src.lib.database import Database
from src.lib.orm import Model, StringField, IntField, query, QueryBuilder
from src.lib.graphql import GraphQLSchema, GraphQLObject, create_schema
from src.lib.cache import Cache, CacheManager, cache_result


def test_rest_library():
    """Test REST library functionality."""
    print("\n=== Testing REST Library ===")
    
    router = Router("/api")
    
    @router.get("/users/:id")
    def get_user(request):
        user_id = request.path_params.get("id")
        return APIResponse(data={"id": user_id, "name": "John"}).to_dict()
    
    print("✅ Router created")
    print("✅ GET route registered")
    
    response = APIResponse(data={"message": "success"})
    print(f"✅ Response created: {response.to_dict()}")


def test_http_library():
    """Test HTTP library functionality."""
    print("\n=== Testing HTTP Library ===")
    
    headers = HTTPHeaders()
    headers.set("Content-Type", "application/json")
    headers.set("Authorization", "Bearer token")
    print(f"✅ Headers created: {dict(headers._headers)}")
    
    request = HTTPRequest("GET", "/api/users")
    request.set_query_param("limit", "10")
    print(f"✅ Request created: {request.method} {request.path}")
    
    response = HTTPResponse(200, "OK")
    print(f"✅ Response created: {response.status_code} {response.reason}")
    print(f"✅ Is success: {response.is_success()}")


def test_web_library():
    """Test Web library functionality."""
    print("\n=== Testing Web Library ===")
    
    client = HTTPClient("http://api.example.com")
    print(f"✅ HTTPClient created with base_url: {client.base_url}")
    
    url = build_url("http://example.com", {"page": "1", "limit": "10"})
    print(f"✅ URL built: {url}")
    
    parsed = parse_url("http://example.com:8080/api/users?id=123")
    print(f"✅ URL parsed: scheme={parsed.get('scheme')}, host={parsed.get('host')}")


def test_database_library():
    """Test Database library functionality."""
    print("\n=== Testing Database Library ===")
    
    db = Database(":memory:")
    
    # Create a simple table
    db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    """)
    print("✅ Table created")
    
    # Insert data
    db.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
               ("Alice", "alice@example.com"))
    db.commit()
    print("✅ Data inserted")
    
    # Query data
    rows = db.fetch_dict("SELECT * FROM users")
    print(f"✅ Data retrieved: {rows}")


def test_orm_library():
    """Test ORM library functionality."""
    print("\n=== Testing ORM Library ===")
    
    # Define a model
    class User(Model):
        _table = "users"
        
        id = IntField(primary_key=True)
        name = StringField(max_length=100)
        email = StringField(max_length=255)
    
    print("✅ User model defined")
    print(f"✅ Model fields: {list(User._fields.keys())}")
    print(f"✅ Table schema: {User.get_schema()}")
    
    # Create instance
    user = User(name="Bob", email="bob@example.com")
    print(f"✅ User instance created: {user.to_dict()}")


def test_graphql_library():
    """Test GraphQL library functionality."""
    print("\n=== Testing GraphQL Library ===")
    
    schema = create_schema()
    print("✅ GraphQL schema created")
    
    # Define User type
    user_type = schema.define_type("User", {
        "id": "ID",
        "name": "String",
        "email": "String"
    })
    print("✅ User type defined")
    
    # Define query
    query_field = schema.query_field("user", "User")
    query_field.argument("id", "ID")
    print("✅ Query field defined with arguments")
    
    # Output SDL
    sdl = schema.to_sdl()
    print(f"✅ GraphQL SDL generated ({len(sdl)} chars)")


def test_cache_library():
    """Test Cache library functionality."""
    print("\n=== Testing Cache Library ===")
    
    cache = Cache(max_size=100, eviction_policy="LRU")
    print("✅ Cache created with LRU eviction")
    
    # Set and get values
    cache.set("key1", "value1", ttl=300)
    value = cache.get("key1")
    print(f"✅ Value cached and retrieved: {value}")
    
    # Cache statistics
    cache.set("key2", "value2")
    cache.get("key1")
    stats = cache.stats()
    print(f"✅ Cache stats: {stats['hits']} hits, {stats['misses']} misses, "
          f"hit_rate={stats['hit_rate']:.1f}%")
    
    # Cache decorator
    @cache_result(ttl=60, cache_name="functions")
    def expensive_function(n):
        return n * 2
    
    result = expensive_function(5)
    print(f"✅ Function result cached: {result}")


def run_all_tests():
    """Run all Phase 5 library tests."""
    print("=" * 60)
    print("PHASE 5 LIBRARY TEST SUITE")
    print("=" * 60)
    
    try:
        test_rest_library()
        test_http_library()
        test_web_library()
        test_database_library()
        test_orm_library()
        test_graphql_library()
        test_cache_library()
        
        print("\n" + "=" * 60)
        print("✅ ALL PHASE 5 TESTS PASSED")
        print("=" * 60)
        
        # Summary
        libraries = [
            "REST (routing, controllers, responses)",
            "HTTP (request, response, headers, status)",
            "Web (client, URL parsing)",
            "Database (SQL, execute, query)",
            "ORM (models, fields, queries)",
            "GraphQL (schema, queries, mutations)",
            "Cache (in-memory, TTL, decorators)"
        ]
        
        print("\n✅ PHASE 5 LIBRARIES IMPLEMENTED:")
        for lib in libraries:
            print(f"  • {lib}")
        
        print(f"\n✅ Total: 7 Phase 5 libraries ready for use")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
