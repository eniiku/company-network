from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom

class Company(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    industry = StringProperty()
    founded_year = StringProperty()
    
    # Relationships
    suppliers = RelationshipTo('Company', 'SUPPLIES')
    customers = RelationshipFrom('Company', 'SUPPLIES')
    partners = RelationshipTo('Company', 'PARTNERS_WITH')
    competitors = RelationshipTo('Company', 'COMPETES_WITH')
