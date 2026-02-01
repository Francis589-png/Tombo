"""
TOMBO GraphQL Library - GraphQL schema and query building
Define schemas, queries, mutations and execute GraphQL operations.
"""

from typing import Dict, List, Any, Optional, Callable


class GraphQLType:
    """GraphQL type definition."""
    
    def __init__(self, name: str, fields: Dict = None):
        """Initialize GraphQL type.
        
        Args:
            name: Type name
            fields: Type fields
        """
        self.name = name
        self.fields = fields or {}
    
    def field(self, field_name: str, field_type: str):
        """Add field to type."""
        self.fields[field_name] = field_type
        return self
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "fields": self.fields
        }


class GraphQLField:
    """GraphQL field definition."""
    
    def __init__(self, field_type: str, resolver: Callable = None, required: bool = False):
        """Initialize GraphQL field.
        
        Args:
            field_type: Field type (String, Int, Boolean, etc.)
            resolver: Function to resolve field value
            required: Is field required (non-null)
        """
        self.field_type = field_type
        self.resolver = resolver
        self.required = required
    
    def resolve(self, obj: Any, args: Dict):
        """Resolve field value."""
        if self.resolver:
            return self.resolver(obj, **args)
        return getattr(obj, self.field_type, None)


class GraphQLScalar:
    """GraphQL scalar type."""
    
    def __init__(self, name: str, serialize: Callable = None, parse: Callable = None):
        """Initialize scalar.
        
        Args:
            name: Scalar type name
            serialize: Serialize value to output
            parse: Parse input value
        """
        self.name = name
        self.serialize = serialize or (lambda x: x)
        self.parse = parse or (lambda x: x)


# Built-in scalars
String = GraphQLScalar("String", serialize=str)
Int = GraphQLScalar("Int", serialize=int)
Float = GraphQLScalar("Float", serialize=float)
Boolean = GraphQLScalar("Boolean", serialize=bool)
ID = GraphQLScalar("ID", serialize=str)


class GraphQLObject:
    """GraphQL object type."""
    
    def __init__(self, name: str):
        """Initialize object type.
        
        Args:
            name: Type name
        """
        self.name = name
        self.fields: Dict[str, GraphQLField] = {}
    
    def field(self, field_name: str, field_type: str = None, 
              resolver: Callable = None, required: bool = False):
        """Define field."""
        self.fields[field_name] = GraphQLField(field_type, resolver, required)
        return self
    
    def to_sdl(self) -> str:
        """Convert to SDL string."""
        fields_sdl = []
        for field_name, field in self.fields.items():
            type_str = field.field_type
            if field.required:
                type_str += "!"
            fields_sdl.append(f"  {field_name}: {type_str}")
        
        return f"type {self.name} {{\n" + "\n".join(fields_sdl) + "\n}"


class GraphQLQuery:
    """GraphQL query definition."""
    
    def __init__(self, name: str, return_type: str):
        """Initialize query.
        
        Args:
            name: Query name
            return_type: Return type
        """
        self.name = name
        self.return_type = return_type
        self.args: Dict[str, str] = {}
        self.resolver: Optional[Callable] = None
    
    def argument(self, arg_name: str, arg_type: str = "String"):
        """Add argument."""
        self.args[arg_name] = arg_type
        return self
    
    def resolve(self, resolver: Callable):
        """Set resolver function."""
        self.resolver = resolver
        return self


class GraphQLMutation:
    """GraphQL mutation definition."""
    
    def __init__(self, name: str, return_type: str):
        """Initialize mutation.
        
        Args:
            name: Mutation name
            return_type: Return type
        """
        self.name = name
        self.return_type = return_type
        self.args: Dict[str, str] = {}
        self.resolver: Optional[Callable] = None
    
    def argument(self, arg_name: str, arg_type: str = "String"):
        """Add argument."""
        self.args[arg_name] = arg_type
        return self
    
    def resolve(self, resolver: Callable):
        """Set resolver function."""
        self.resolver = resolver
        return self


class GraphQLSchema:
    """GraphQL schema."""
    
    def __init__(self, query: GraphQLObject):
        """Initialize schema.
        
        Args:
            query: Root query type
        """
        self.query = query
        self.mutation: Optional[GraphQLObject] = None
        self.types: Dict[str, Any] = {}
        self.queries: Dict[str, GraphQLQuery] = {}
        self.mutations: Dict[str, GraphQLMutation] = {}
    
    def define_type(self, type_name: str, fields: Dict = None) -> GraphQLObject:
        """Define custom type."""
        obj = GraphQLObject(type_name)
        if fields:
            for field_name, field_type in fields.items():
                obj.field(field_name, field_type)
        self.types[type_name] = obj
        return obj
    
    def query_field(self, field_name: str, return_type: str = "String") -> GraphQLQuery:
        """Define query field."""
        query = GraphQLQuery(field_name, return_type)
        self.queries[field_name] = query
        return query
    
    def mutation_field(self, field_name: str, return_type: str = "String") -> GraphQLMutation:
        """Define mutation field."""
        mutation = GraphQLMutation(field_name, return_type)
        self.mutations[field_name] = mutation
        return mutation
    
    def to_sdl(self) -> str:
        """Convert schema to GraphQL SDL."""
        sdl_parts = []
        
        # Query type
        sdl_parts.append(self.query.to_sdl())
        
        # Mutation type if exists
        if self.mutation:
            sdl_parts.append(self.mutation.to_sdl())
        
        # Custom types
        for type_obj in self.types.values():
            sdl_parts.append(type_obj.to_sdl())
        
        return "\n\n".join(sdl_parts)


class GraphQLExecutor:
    """Execute GraphQL queries and mutations."""
    
    def __init__(self, schema: GraphQLSchema):
        """Initialize executor.
        
        Args:
            schema: GraphQL schema
        """
        self.schema = schema
    
    def execute(self, query: str, variables: Dict = None) -> Dict:
        """Execute GraphQL query.
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            Query result
        """
        variables = variables or {}
        
        try:
            # Parse query (simplified)
            if query.strip().startswith("query"):
                return self._execute_query(query, variables)
            elif query.strip().startswith("mutation"):
                return self._execute_mutation(query, variables)
            else:
                return {"errors": ["Invalid query type"]}
        except Exception as e:
            return {"errors": [str(e)]}
    
    def _execute_query(self, query_str: str, variables: Dict) -> Dict:
        """Execute query."""
        result = {}
        
        for query_name, query_obj in self.schema.queries.items():
            if query_name in query_str:
                if query_obj.resolver:
                    try:
                        result[query_name] = query_obj.resolver(**variables)
                    except Exception as e:
                        result[query_name] = None
        
        return {"data": result} if result else {"data": {}}
    
    def _execute_mutation(self, mutation_str: str, variables: Dict) -> Dict:
        """Execute mutation."""
        result = {}
        
        for mutation_name, mutation_obj in self.schema.mutations.items():
            if mutation_name in mutation_str:
                if mutation_obj.resolver:
                    try:
                        result[mutation_name] = mutation_obj.resolver(**variables)
                    except Exception as e:
                        result[mutation_name] = None
        
        return {"data": result} if result else {"data": {}}


def create_schema(query_type: GraphQLObject = None) -> GraphQLSchema:
    """Create new GraphQL schema."""
    if not query_type:
        query_type = GraphQLObject("Query")
    
    return GraphQLSchema(query_type)
