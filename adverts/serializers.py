from jsonschema import validate

advertisement_model = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string", "maxLength": 200},
        "description": {"type": "string", "maxLength": 1000},
        "price": {"type": "number", "minimum": 0.0},
        "photo_links": {
            "type": "array",
            "maxItems": 3,
            "items": {"type": "string", "maxLength": 150}
        }
    },
    "required": ["title", "description", "price"]
}

def validate_advert(json):
    validate(json, advertisement_model)
