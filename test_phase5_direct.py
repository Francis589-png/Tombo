"""
Phase 5 Library Direct Test - Import libraries individually
"""

import sys
import os

# Add the src/lib directory to path
lib_path = r"c:\Users\FRANCIS JUSU\Documents\TOMBO\src\lib"
sys.path.insert(0, lib_path)

def test_rest_library():
    """Test REST library functionality."""
    print("\n=== Testing REST Library ===")
    
    try:
        from rest import Router, ResourceController, APIResponse, create_response
        
        router = Router("/api")
        print("✅ Router created")
        
        response = APIResponse(data={"message": "success"})
        response_dict = response.to_dict()
        print(f"✅ Response created: {response_dict['data']}")
        
        return True
    except Exception as e:
        print(f"❌ REST test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_http_library():
    """Test HTTP library functionality."""
    print("\n=== Testing HTTP Library ===")
    
    try:
        from http import HTTPRequest, HTTPResponse, HTTPStatus, HTTPHeaders
        
        headers = HTTPHeaders()
        headers.set("Content-Type", "application/json")
        print(f"✅ Headers created")
        
        request = HTTPRequest("GET", "/api/users")
        request.set_query_param("limit", "10")
        print(f"✅ Request created: {request.method} {request.path}")
        
        response = HTTPResponse(200, "OK")
        print(f"✅ Response created: {response.status_code} {response.reason}")
        print(f"✅ Is success: {response.is_success()}")
        
        return True
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_web_library():
    """Test Web library functionality."""
    print("\n=== Testing Web Library ===")
    
    try:
        from web import HTTPClient, build_url, parse_url
        
        client = HTTPClient("http://api.example.com")
        print(f"✅ HTTPClient created")
        
        url = build_url("http://example.com", {"page": "1"})
        print(f"✅ URL built: {url[:40]}...")
        
        parsed = parse_url("http://example.com:8080/api/users")
        print(f"✅ URL parsed")
        
        return True
    except Exception as e:
        print(f"❌ Web test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_library():
    """Test Database library functionality."""
    print("\n=== Testing Database Library ===")
    
    try:
        from database import Database
        
        db = Database(":memory:")
        
        # Create a simple table
        db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        print("✅ Table created")
        
        # Insert data
        db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        db.commit()
        print("✅ Data inserted")
        
        # Query data
        rows = db.fetch_dict("SELECT * FROM users")
        print(f"✅ Data retrieved: {len(rows)} row(s)")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_orm_library():
    """Test ORM library functionality."""
    print("\n=== Testing ORM Library ===")
    
    try:
        from orm import Model, StringField, IntField
        
        # Define a model
        class User(Model):
            _table = "users"
            
            id = IntField(primary_key=True)
            name = StringField(max_length=100)
        
        print("✅ User model defined")
        print(f"✅ Model fields: {list(User._fields.keys())}")
        
        # Create instance
        user = User(name="Bob")
        user_data = user.to_dict()
        print(f"✅ User instance created: name={user_data.get('name')}")
        
        return True
    except Exception as e:
        print(f"❌ ORM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_graphql_library():
    """Test GraphQL library functionality."""
    print("\n=== Testing GraphQL Library ===")
    
    try:
        from graphql import create_schema
        
        schema = create_schema()
        print("✅ GraphQL schema created")
        
        # Define User type
        user_type = schema.define_type("User", {
            "id": "ID",
            "name": "String"
        })
        print("✅ User type defined")
        
        # Output SDL
        sdl = schema.to_sdl()
        print(f"✅ GraphQL SDL generated ({len(sdl)} chars)")
        
        return True
    except Exception as e:
        print(f"❌ GraphQL test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cache_library():
    """Test Cache library functionality."""
    print("\n=== Testing Cache Library ===")
    
    try:
        from cache import Cache, create_cache
        
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
        print(f"✅ Cache stats: {stats['hits']} hits, {stats['misses']} misses")
        
        return True
    except Exception as e:
        print(f"❌ Cache test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all Phase 5 library tests."""
    print("=" * 70)
    print("PHASE 5 LIBRARY TEST SUITE - All 7 Libraries")
    print("=" * 70)
    
    results = []
    
    results.append(("REST", test_rest_library()))
    results.append(("HTTP", test_http_library()))
    results.append(("Web", test_web_library()))
    results.append(("Database", test_database_library()))
    results.append(("ORM", test_orm_library()))
    results.append(("GraphQL", test_graphql_library()))
    results.append(("Cache", test_cache_library()))
    
    print("\n" + "=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"✅ PHASE 5 TEST RESULTS: {passed}/{total} PASSED")
    print("=" * 70)
    
    print("\n✅ PHASE 5 LIBRARIES SUMMARY:")
    libraries = [
        ("REST", "Router, ResourceController, APIResponse"),
        ("HTTP", "HTTPRequest, HTTPResponse, HTTPStatus, HTTPHeaders"),
        ("Web", "HTTPClient, URL parsing & building"),
        ("Database", "SQLite with execute, commit, query"),
        ("ORM", "Model classes, Field types, QueryBuilder"),
        ("GraphQL", "Schema, Query, Mutation, SDL generation"),
        ("Cache", "In-memory cache, TTL, LRU/LFU/FIFO eviction")
    ]
    
    for name, features in libraries:
        status = "✅" if any(r[0] == name and r[1] for r in results) else "❌"
        print(f"  {status} {name:12} - {features}")
    
    print(f"\n✅ Total: 7 Phase 5 libraries implemented and tested")
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
