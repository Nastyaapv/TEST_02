# Общие схемы



schema_empty_json = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "examples": [
        []
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items"
    }
}

schema_400_error = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "title": "The root schema",
    "type": "object",
    "description": "The root schema comprises the entire JSON document.",
    "required": [
        "message",
        "status",
        "timestamp"
    ],
    "properties": {
        "error": {
            "$id": "#/properties/error",
            "type": "string"
        },
        "message": {
            "$id": "#/properties/message",
            "type": "string"
        },
        "path": {
            "$id": "#/properties/path",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": ["string", "integer"]
        },
        "timestamp": {
            "$id": "#/properties/timestamp",
            "type": "string"
        }
    },
    "additionalProperties": True
}

schema_404_error = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "required": [
        "status",
        "message",
        "timestamp"
    ],
    "properties": {
        "error": {
            "$id": "#/properties/error",
            "type": "string"
        },
        "message": {
            "$id": "#/properties/message",
            "type": "string"
        },
        "path": {
            "$id": "#/properties/path",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": "string"
        },
        "timestamp": {
            "$id": "#/properties/timestamp",
            "type": "string"
        }
    },
    "additionalProperties": True
}

schema_405_error = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "error",
        "message",
        "path",
        "status",
        "timestamp"
    ],
    "properties": {
        "error": {
            "$id": "#/properties/error",
            "type": "string"
        },
        "message": {
            "$id": "#/properties/message",
            "type": "string"
        },
        "path": {
            "$id": "#/properties/path",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": "integer"
        },
        "timestamp": {
            "$id": "#/properties/timestamp",
            "type": "string"
        }
    },
    "additionalProperties": True
}

schema_409_error = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "status",
        "message",
        "timestamp"
    ],
    "properties": {
        "error": {
            "$id": "#/properties/error",
            "type": "string"
        },
        "message": {
            "$id": "#/properties/message",
            "type": "string"
        },
        "path": {
            "$id": "#/properties/path",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": "string"
        },
        "timestamp": {
            "$id": "#/properties/timestamp",
            "type": "string"
        }
    },
    "additionalProperties": True
}

schema_500_error = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "error": "Internal Server Error",
            "message": "The given id must not be null!; nested exception is java.lang.IllegalArgumentException: The given id must not be null!",
            "path": "//profile/attributes/additional/%20",
            "status": 500,
            "timestamp": "2021-11-11T13:43:54.262+00:00"
        }
    ],
    "required": [
        "error",
        "message",
        "path",
        "status",
        "timestamp"
    ],
    "properties": {
        "error": {
            "$id": "#/properties/error",
            "type": "string"
        },
        "message": {
            "$id": "#/properties/message",
            "type": "string"
        },
        "path": {
            "$id": "#/properties/path",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": "integer"
        },
        "timestamp": {
            "$id": "#/properties/timestamp",
            "type": "string"
        }
    },
    "additionalProperties": True
}

# Схемы для валидации ответов
GET_profile_attributes_base_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "GET_profile_attributes_base_200_main_schema",
    "description": "method: GET/profile/attributes/base; code: 200 OK; scenario: main",
    "default": [],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "id",
                    "identity",
                    "name",
                    "jsonName",
                    "type",
                    "metadata",
                    "deleted",
                    "creationDate"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "integer"
                    },
                    "identity": {
                        "$id": "#/items/anyOf/0/properties/identity",
                        "type": "string"
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/name",
                        "type": "string"
                    },
                    "jsonName": {
                        "$id": "#/items/anyOf/0/properties/jsonName",
                        "type": "string"
                    },
                    "type": {
                        "$id": "#/items/anyOf/0/properties/type",
                        "type": "string"
                    },
                    "metadata": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["object", "null"]
                    },
                    "deleted": {
                        "$id": "#/items/anyOf/0/properties/deleted",
                        "type": "boolean"
                    },
                    "creationDate": {
                        "$id": "#/items/anyOf/0/properties/creationDate",
                        "type": "string"
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_attributes_base_id_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "GET_profile_attributes_base_200_main_schema",
    "description": "method: GET/profile/attributes/base; code: 200 OK; scenario: main",
    "default": [],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "id",
                    "identity",
                    "name",
                    "jsonName",
                    "type",
                    "metadata",
                    "deleted",
                    "creationDate"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "integer"
                    },
                    "identity": {
                        "$id": "#/items/anyOf/0/properties/identity",
                        "type": "string"
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/name",
                        "type": "string"
                    },
                    "jsonName": {
                        "$id": "#/items/anyOf/0/properties/jsonName",
                        "type": "string"
                    },
                    "type": {
                        "$id": "#/items/anyOf/0/properties/type",
                        "type": "string"
                    },
                    "metadata": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["object", "null"]
                    },
                    "deleted": {
                        "$id": "#/items/anyOf/0/properties/deleted",
                        "type": "boolean"
                    },
                    "creationDate": {
                        "$id": "#/items/anyOf/0/properties/creationDate",
                        "type": "string"
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_attributes_base_search_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "totalElements",
        "totalPages",
        "sort",
        "numberOfElements",
        "pageable",
        "first",
        "last",
        "size",
        "content",
        "number",
        "empty"
    ],
    "properties": {
        "totalElements": {
            "$id": "#/properties/totalElements",
            "type": "integer",
        },
        "totalPages": {
            "$id": "#/properties/totalPages",
            "type": "integer",
        },
        "sort": {
            "$id": "#/properties/sort",
            "type": "object",
            "title": "The sort schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "sorted": True,
                    "unsorted": True,
                    "empty": True
                }
            ],
            "required": [
                "sorted",
                "unsorted",
                "empty"
            ],
            "properties": {
                "sorted": {
                    "$id": "#/properties/sort/properties/sorted",
                    "type": "boolean",
                },
                "unsorted": {
                    "$id": "#/properties/sort/properties/unsorted",
                    "type": "boolean",
                },
                "empty": {
                    "$id": "#/properties/sort/properties/empty",
                    "type": "boolean",
                }
            },
            "additionalProperties": True
        },
        "numberOfElements": {
            "$id": "#/properties/numberOfElements",
            "type": "integer",
        },
        "pageable": {
            "$id": "#/properties/pageable",
            "type": "object",
            "title": "The pageable schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "sort",
                "paged",
                "unpaged",
                "pageNumber",
                "pageSize",
                "offset"
            ],
            "properties": {
                "sort": {
                    "$id": "#/properties/pageable/properties/sort",
                    "type": "object",
                    "title": "The sort schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "required": [
                        "sorted",
                        "unsorted",
                        "empty"
                    ],
                    "properties": {
                        "sorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/sorted",
                            "type": "boolean",
                        },
                        "unsorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/unsorted",
                            "type": "boolean",
                        },
                        "empty": {
                            "$id": "#/properties/pageable/properties/sort/properties/empty",
                            "type": "boolean",
                        }
                    },
                    "additionalProperties": True
                },
                "paged": {
                    "$id": "#/properties/pageable/properties/paged",
                    "type": "boolean",
                },
                "unpaged": {
                    "$id": "#/properties/pageable/properties/unpaged",
                    "type": "boolean",
                },
                "pageNumber": {
                    "$id": "#/properties/pageable/properties/pageNumber",
                    "type": "integer",
                },
                "pageSize": {
                    "$id": "#/properties/pageable/properties/pageSize",
                    "type": "integer",
                },
                "offset": {
                    "$id": "#/properties/pageable/properties/offset",
                    "type": "integer",
                }
            },
            "additionalProperties": True
        },
        "first": {
            "$id": "#/properties/first",
            "type": "boolean",
        },
        "last": {
            "$id": "#/properties/last",
            "type": "boolean",
        },
        "size": {
            "$id": "#/properties/size",
            "type": "integer",
        },
        "content": {
            "$id": "#/properties/content",
            "type": "array",
            "title": "The content schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/content/items",
                "anyOf": [
                    {
                        "$id": "#/properties/content/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "required": [
                            "identity",
                            "name",
                            "jsonName",
                            "type",
                            "metadata"
                        ],
                        "properties": {
                            "identity": {
                                "$id": "#/properties/content/items/anyOf/0/properties/identity",
                                "type": "string",
                            },
                            "name": {
                                "$id": "#/properties/content/items/anyOf/0/properties/name",
                                "type": "string",
                            },
                            "jsonName": {
                                "$id": "#/properties/content/items/anyOf/0/properties/jsonName",
                                "type": "string",
                            },
                            "type": {
                                "$id": "#/properties/content/items/anyOf/0/properties/type",
                                "type": "string",
                            },
                            "metadata": {
                                "$id": "#/properties/content/items/anyOf/0/properties/metadata",
                                "type": ["object", "null"],
                                "title": "The metadata schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "required": [
                                ],
                                "properties": {
                                    "additionalProp1": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/metadata/properties/additionalProp1",
                                        "type": "object",
                                        "title": "The additionalProp1 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": {},
                                        "required": [],
                                        "additionalProperties": True
                                    },
                                    "additionalProp2": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/metadata/properties/additionalProp2",
                                        "type": "object",
                                        "title": "The additionalProp2 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": {},
                                        "examples": [
                                            {}
                                        ],
                                        "required": [],
                                        "additionalProperties": True
                                    }
                                },
                                "additionalProperties": True
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "number": {
            "$id": "#/properties/number",
            "type": "integer",
            "title": "The number schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "empty": {
            "$id": "#/properties/empty",
            "type": "boolean",
            "title": "The empty schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        }
    },
    "additionalProperties": True
}

GET_profile_attributes_additional_200_main_schema = {
    
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    # "type": "array",
    "title": "GET_profile_attributes_additional_200_main_schema",
    "description": "method: GET/profile/attributes/additional; code: 200 OK; scenario: main",
    "default": [],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "id",
                    "display",
                    "required",
                    "name",
                    "jsonName",
                    "fieldOrder",
                    "fieldType",
                    "userType",
                    "creationDate",
                    "region",
                    "metadata"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "integer"
                    },
                    "display": {
                        "$id": "#/items/anyOf/0/properties/display",
                        "type": ["boolean", "null"]
                    },
                    "required": {
                        "$id": "#/items/anyOf/0/properties/required",
                        "type": ["boolean", "null"]
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["string", "null"]
                    },
                    "jsonName": {
                        "$id": "#/items/anyOf/0/properties/jsonName",
                        "type": "string"
                    },
                    "fieldOrder": {
                        "$id": "#/items/anyOf/0/properties/fieldOrder",
                        "type": ["integer", "null"]
                    },
                    "fieldType": {
                        "$id": "#/items/anyOf/0/properties/fieldType",
                        "type": "string"
                    },
                    "userType": {
                        "$id": "#/items/anyOf/0/properties/userType",
                        "type": "string"
                    },
                    "creationDate": {
                        "$id": "#/items/anyOf/0/properties/creationDate",
                        "type": "string"
                    },
                    "region": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["string", "null"]
                    },
                    "metadata": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["object", "null"]
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_attributes_additional_search_200_main_schema = {
    
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "GET_profile_attributes_additional_200_main_schema",
    "description": "method: GET/profile/attributes/additional; code: 200 OK; scenario: main",
    "default": [],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "id",
                    "display",
                    "required",
                    "name",
                    "jsonName",
                    "fieldOrder",
                    "fieldType",
                    "userType",
                    "creationDate",
                    "region",
                    "metadata"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "integer"
                    },
                    "display": {
                        "$id": "#/items/anyOf/0/properties/display",
                        "type": ["boolean", "null"]
                    },
                    "required": {
                        "$id": "#/items/anyOf/0/properties/required",
                        "type": ["boolean", "null"]
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": "string"
                    },
                    "jsonName": {
                        "$id": "#/items/anyOf/0/properties/jsonName",
                        "type": "string"
                    },
                    "fieldOrder": {
                        "$id": "#/items/anyOf/0/properties/fieldOrder",
                        "type": ["integer", "null"]
                    },
                    "fieldType": {
                        "$id": "#/items/anyOf/0/properties/fieldType",
                        "type": "string"
                    },
                    "userType": {
                        "$id": "#/items/anyOf/0/properties/userType",
                        "type": "string"
                    },
                    "creationDate": {
                        "$id": "#/items/anyOf/0/properties/creationDate",
                        "type": "string"
                    },
                    "region": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["string", "null"]
                    },
                    "metadata": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["object", "null"]
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_system_attributes_200_main_schema = {
    
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    # "type": "array",
    "title": "GET_profile_system_attributes_200_main_schema",
    "description": "method: GET/profile/system-attributes/get; code: 200 OK; scenario: main",
    "default": [],
    "examples": [
        [
            {
                "id": 0,
                "required": True,
                "name": "string",
                "jsonName": "string",
                "fieldOrder": 0,
                "fieldType": "string",
                "userType": "string",
                "creationDate": "2021-11-10T13:45:45.293Z",
                "region": "string",
                "metadata": {
                    "additionalProp1": {},
                    "additionalProp2": {},
                    "additionalProp3": {}
                }
            }
        ]
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "examples": [
                    {
                        "id": 0,
                        "required": True,
                        "name": "string",
                        "jsonName": "string",
                        "fieldOrder": 0,
                        "fieldType": "string",
                        "userType": "string",
                        "creationDate": "2021-11-10T13:45:45.293Z",
                        "region": "string",
                        "metadata": {
                            "additionalProp1": {},
                            "additionalProp2": {},
                            "additionalProp3": {}
                        }
                    }
                ],
                "required": [
                    "id",
                    "required",
                    "name",
                    "jsonName",
                    "fieldOrder",
                    "fieldType",
                    "userType",
                    "creationDate",
                    "region",
                    "metadata"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "integer"
                    },
                    "required": {
                        "$id": "#/items/anyOf/0/properties/required",
                        "type": ["boolean", "null"]
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": "string"
                    },
                    "jsonName": {
                        "$id": "#/items/anyOf/0/properties/jsonName",
                        "type": "string"
                    },
                    "fieldOrder": {
                        "$id": "#/items/anyOf/0/properties/fieldOrder",
                        "type": ["integer", "null"]
                    },
                    "fieldType": {
                        "$id": "#/items/anyOf/0/properties/fieldType",
                        "type": "string"
                    },
                    "userType": {
                        "$id": "#/items/anyOf/0/properties/userType",
                        "type": "string"
                    },
                    "creationDate": {
                        "$id": "#/items/anyOf/0/properties/creationDate",
                        "type": "string"
                    },
                    "region": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": "string"
                    },
                    "metadata": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["object", "null"]
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_system_attributes_get_200_main_schema = {
    
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    # "type": "array",
    "title": "GET_profile_system_attributes_200_main_schema",
    "description": "method: GET/profile/system-attributes/get; code: 200 OK; scenario: main",
    "default": [],
    "examples": [
        [
            {
                "id": 0,
                "required": True,
                "name": "string",
                "jsonName": "string",
                "fieldOrder": 0,
                "fieldType": "string",
                "userType": "string",
                "creationDate": "2021-11-10T13:45:45.293Z",
                "region": "string",
                "metadata": {
                    "additionalProp1": {},
                    "additionalProp2": {},
                    "additionalProp3": {}
                }
            }
        ]
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "examples": [
                    {
                        "id": 0,
                        "required": True,
                        "name": "string",
                        "jsonName": "string",
                        "fieldOrder": 0,
                        "fieldType": "string",
                        "userType": "string",
                        "creationDate": "2021-11-10T13:45:45.293Z",
                        "region": "string",
                        "metadata": {
                            "additionalProp1": {},
                            "additionalProp2": {},
                            "additionalProp3": {}
                        }
                    }
                ],
                "required": [
                    "id",
                    "required",
                    "name",
                    "jsonName",
                    "fieldOrder",
                    "fieldType",
                    "userType",
                    "creationDate",
                    "region",
                    "metadata"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "integer"
                    },
                    "required": {
                        "$id": "#/items/anyOf/0/properties/required",
                        "type": ["boolean", "null"]
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": "string"
                    },
                    "jsonName": {
                        "$id": "#/items/anyOf/0/properties/jsonName",
                        "type": "string"
                    },
                    "fieldOrder": {
                        "$id": "#/items/anyOf/0/properties/fieldOrder",
                        "type": ["integer", "null"]
                    },
                    "fieldType": {
                        "$id": "#/items/anyOf/0/properties/fieldType",
                        "type": "string"
                    },
                    "userType": {
                        "$id": "#/items/anyOf/0/properties/userType",
                        "type": "string"
                    },
                    "creationDate": {
                        "$id": "#/items/anyOf/0/properties/creationDate",
                        "type": "string"
                    },
                    "region": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": "string"
                    },
                    "metadata": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["object", "null"]
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_system_attributes_list_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "examples": [
        [
            {
                "required": True,
                "name": "string",
                "jsonName": "string",
                "fieldType": "string",
                "userType": "string",
                "creationDate": "2021-11-15T11:18:54.992Z",
                "region": "string",
                "metadata": {}
            }
        ]
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "examples": [
                    {
                        "required": True,
                        "name": "string",
                        "jsonName": "string",
                        "fieldType": "string",
                        "userType": "string",
                        "creationDate": "2021-11-15T11:18:54.992Z",
                        "region": "string",
                        "metadata": {}
                    }
                ],
                "required": [
                    "required",
                    "name",
                    "jsonName",
                    "fieldType",
                    "userType",
                    "creationDate",
                    "region",
                    "metadata"
                ],
                "properties": {
                    "required": {
                        "$id": "#/items/anyOf/0/properties/required",
                        "type": "boolean",
                        "title": "The required schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": False,
                        "examples": [
                            True
                        ]
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/name",
                        "type": "string",
                        "title": "The name schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "jsonName": {
                        "$id": "#/items/anyOf/0/properties/jsonName",
                        "type": "string",
                        "title": "The jsonName schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "fieldType": {
                        "$id": "#/items/anyOf/0/properties/fieldType",
                        "type": "string",
                        "title": "The fieldType schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "userType": {
                        "$id": "#/items/anyOf/0/properties/userType",
                        "type": "string",
                        "title": "The userType schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "creationDate": {
                        "$id": "#/items/anyOf/0/properties/creationDate",
                        "type": "string",
                        "title": "The creationDate schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "2021-11-15T11:18:54.992Z"
                        ]
                    },
                    "region": {
                        "$id": "#/items/anyOf/0/properties/region",
                        "type": "string",
                        "title": "The region schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "metadata": {
                        "$id": "#/items/anyOf/0/properties/metadata",
                        "type": ["object", "null"],
                        "title": "The metadata schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {}
                        ],
                        "required": [],
                        "additionalProperties": True
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_system_attributes_user_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    ],
    "properties": {
        "additionalProp1": {
            "$id": "#/properties/additionalProp1",
            "type": "string"
        },
        "additionalProp2": {
            "$id": "#/properties/additionalProp2",
            "type": "string"
            
        },
        "additionalProp3": {
            "$id": "#/properties/additionalProp3",
            "type": "string"
            
        }
    },
    "additionalProperties": True
}

GET_profile_mgp_recipient_id_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "id": "005de354-c176-4359-9c5e-1d2c8552fa8e",
            "status": "POTENTIAL",
            "statusDate": "2021-07-11T21:00:00.000+00:00",
            "okopf": None,
            "userId": "testUser-QA50HT88"
        }
    ],
    "required": [
        "id",
        "status",
        "statusDate",
        "okopf",
        "userId"
    ],
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": "string"
        },
        "statusDate": {
            "$id": "#/properties/statusDate",
            "type": "string"
        },
        "okopf": {
            "$id": "#/properties/okopf",
            "type": "null"
        },
        "userId": {
            "$id": "#/properties/userId",
            "type": "string"
        }
    },
    "additionalProperties": True
}

GET_group_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "examples": [
        [
            {
                "name": "string",
                "description": "string",
                "role": "string"
            }
        ]
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "examples": [
                    {
                        "name": "string",
                        "description": "string",
                        "role": "string"
                    }
                ],
                "required": [
                    "name",
                    "description",
                    "role"
                ],
                "properties": {
                    "name": {
                        "$id": "#/items/anyOf/0/properties/name",
                        "type": "string"
                    },
                    "description": {
                        "$id": "#/items/anyOf/0/properties/description",
                        "type": "string"
                    },
                    "role": {
                        "$id": "#/items/anyOf/0/properties/role",
                        "type": "string"
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_group_link_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "examples": [
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "attrName",
                    "position",
                    "block"
                ],
                "properties": {
                    "attrName": {
                        "$id": "#/items/anyOf/0/properties/attrName",
                        "type": "string"
                    },
                    "position": {
                        "$id": "#/items/anyOf/0/properties/position",
                        "type": "integer"
                    },
                    "block": {
                        "$id": "#/items/anyOf/0/properties/block",
                        "type": "string"
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_document_list_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "data": [
                {
                    "fileName": "string",
                    "createdBy": "string",
                    "updatedBy": "string",
                    "deletedBy": "string",
                    "documentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "createOn": "2021-12-28T11:15:58.959Z",
                    "updatedOn": "2021-12-28T11:15:58.959Z",
                    "description": "string",
                    "expiresOn": "2021-12-28",
                    "deleted": True
                }
            ],
            "meta": {
                "elementsQuantity": 0,
                "currentPage": 0,
                "pageSize": 0,
                "pagesQuantity": 0
            }
        }
    ],
    "required": [
        "data"
    ],
    "properties": {
        "data": {
            "$id": "#/properties/data",
            "type": "array",
            "title": "The data schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "fileName": "string",
                        "createdBy": "string",
                        "updatedBy": "string",
                        "deletedBy": "string",
                        "documentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "createOn": "2021-12-28T11:15:58.959Z",
                        "updatedOn": "2021-12-28T11:15:58.959Z",
                        "description": "string",
                        "expiresOn": "2021-12-28",
                        "deleted": True
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/data/items",
                "anyOf": [
                    {
                        "$id": "#/properties/data/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "required": [
                            "fileName",
                            "createdBy",
                            "updatedBy",
                            "deletedBy",
                            "documentId",
                            "createOn",
                            "updatedOn",
                            "description",
                            "expiresOn",
                            "deleted"
                        ],
                        "properties": {
                            "fileName": {
                                "$id": "#/properties/data/items/anyOf/0/properties/fileName",
                                "type": "string"
                            },
                            "createdBy": {
                                "$id": "#/properties/data/items/anyOf/0/properties/createdBy",
                                "type": "string"
                            },
                            "updatedBy": {
                                "$id": "#/properties/data/items/anyOf/0/properties/updatedBy"
                            },
                            "deletedBy": {
                                "$id": "#/properties/data/items/anyOf/0/properties/deletedBy"
                            },
                            "documentId": {
                                "$id": "#/properties/data/items/anyOf/0/properties/documentId",
                                "type": "string"
                            },
                            "createOn": {
                                "$id": "#/properties/data/items/anyOf/0/properties/createOn",
                                "type": "string"
                            },
                            "updatedOn": {
                                "$id": "#/properties/data/items/anyOf/0/properties/updatedOn"
                            },
                            "description": {
                                "$id": "#/properties/data/items/anyOf/0/properties/description"
                            },
                            "expiresOn": {
                                "$id": "#/properties/data/items/anyOf/0/properties/expiresOn"
                            },
                            "deleted": {
                                "$id": "#/properties/data/items/anyOf/0/properties/deleted",
                                "type": "boolean"
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "meta": {
            "$id": "#/properties/meta",
            "type": "object",
            "title": "The meta schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "elementsQuantity",
                "currentPage",
                "pageSize",
                "pagesQuantity"
            ],
            "properties": {
                "elementsQuantity": {
                    "$id": "#/properties/meta/properties/elementsQuantity",
                    "type": "integer"
                },
                "currentPage": {
                    "$id": "#/properties/meta/properties/currentPage",
                    "type": "integer"
                },
                "pageSize": {
                    "$id": "#/properties/meta/properties/pageSize",
                    "type": "integer"
                },
                "pagesQuantity": {
                    "$id": "#/properties/meta/properties/pagesQuantity",
                    "type": "integer"
                }
            },
            "additionalProperties": True
        }
    },
    "additionalProperties": True
}

GET_reestr_indicators_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "examples": [
        [
            {
                "id": 0,
                "code": "string",
                "name": "string",
                "groupName": "string"
            }
        ]
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "id",
                    "code",
                    "name",
                    "groupName"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "integer"
                    },
                    "code": {
                        "$id": "#/items/anyOf/0/properties/code",
                        "type": "string"
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/name",
                        "type": "string"
                    },
                    "groupName": {
                        "$id": "#/items/anyOf/0/properties/groupName",
                        "type": "string"
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_employee_management_groups_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "id",
                    "name"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "string"
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/name",
                        "type": "string"
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_employee_management_employee_id_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "id",
        "orgId",
        "attributes"
    ],
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "string"
        },
        "orgId": {
            "$id": "#/properties/orgId",
            "type": "string"
        },
        "deleted": {
            "$id": "#/properties/deleted",
            "type": "boolean"
        },
        "attributes": {
            "$id": "#/properties/attributes",
            "type": "object",
            "title": "The attributes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
            ],
            "properties": {
                "additionalProp1": {
                    "$id": "#/properties/attributes/properties/additionalProp1",
                    "type": "string",
                    "title": "The additionalProp1 schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": ""
                },
            },
            "additionalProperties": True
        },
        "sources": {
            "$id": "#/properties/sources",
            "type": "object",
            "title": "The sources schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "esia",
                "user"
            ],
            "properties": {
                "esia": {
                    "$id": "#/properties/sources/properties/esia",
                    "type": "array",
                    "title": "The esia schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": [],
                    "additionalItems": True,
                    "items": {
                        "$id": "#/properties/sources/properties/esia/items",
                        "anyOf": [
                            {
                                "$id": "#/properties/sources/properties/esia/items/anyOf/0",
                                "type": "string",
                                "title": "The first anyOf schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": ""
                            }
                        ]
                    }
                },
                "user": {
                    "$id": "#/properties/sources/properties/user",
                    "type": "array",
                    "title": "The user schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": [],
                    "additionalItems": True,
                    "items": {
                        "$id": "#/properties/sources/properties/user/items",
                        "anyOf": [
                            {
                                "$id": "#/properties/sources/properties/user/items/anyOf/0",
                                "type": "string"
                            }
                        ]
                    }
                }
            },
            "additionalProperties": True
        }
    },
    "additionalProperties": True
}

GET_employee_management_attributes_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "examples": [
        [
            {
                "id": "string",
                "groupId": "string",
                "name": "string",
                "fieldType": "string",
                "required": True,
                "defaultSource": "string",
                "main": True
            }
        ]
    ],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "examples": [
                    {
                        "id": "string",
                        "groupId": "string",
                        "name": "string",
                        "fieldType": "string",
                        "required": True,
                        "defaultSource": "string",
                        "main": True
                    }
                ],
                "required": [
                    "id",
                    "groupId",
                    "name",
                    "fieldType",
                    "required",
                    "defaultSource",
                    "main"
                ],
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "string",
                        "title": "The id schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "groupId": {
                        "$id": "#/items/anyOf/0/properties/groupId",
                        "type": "string",
                        "title": "The groupId schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "name": {
                        "$id": "#/items/anyOf/0/properties/name",
                        "type": "string",
                        "title": "The name schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "fieldType": {
                        "$id": "#/items/anyOf/0/properties/fieldType",
                        "type": "string",
                        "title": "The fieldType schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "required": {
                        "$id": "#/items/anyOf/0/properties/required",
                        "type": "boolean",
                        "title": "The required schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": False,
                        "examples": [
                            True
                        ]
                    },
                    "defaultSource": {
                        "$id": "#/items/anyOf/0/properties/defaultSource",
                        "type": "string",
                        "title": "The defaultSource schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "main": {
                        "$id": "#/items/anyOf/0/properties/main",
                        "type": "boolean",
                        "title": "The main schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": False,
                        "examples": [
                            True
                        ]
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

POST_employee_management_search_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "data",
        "meta"
    ],
    "properties": {
        "data": {
            "$id": "#/properties/data",
            "type": "array",
            "title": "The data schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/data/items",
                "anyOf": [
                    {
                        "$id": "#/properties/data/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "required": [
                            "id",
                            "orgId",
                            "attributes"
                        ],
                        "properties": {
                            "id": {
                                "$id": "#/properties/data/items/anyOf/0/properties/id",
                                "type": "string"
                            },
                            "orgId": {
                                "$id": "#/properties/data/items/anyOf/0/properties/orgId",
                                "type": "string"
                            },
                            "deleted": {
                                "$id": "#/properties/data/items/anyOf/0/properties/deleted",
                                "type": "boolean"
                            },
                            "attributes": {
                                "$id": "#/properties/data/items/anyOf/0/properties/attributes",
                                "type": "object",
                                "title": "The attributes schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "properties": {
                                    "additionalProp1": {
                                        "$id": "#/properties/data/items/anyOf/0/properties/attributes/properties/additionalProp1",
                                        "type": "string",
                                        "title": "The additionalProp1 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": ""
                                    }
                                },
                                "additionalProperties": True
                            },
                            "sources": {
                                "$id": "#/properties/data/items/anyOf/0/properties/sources",
                                "type": "object",
                                "title": "The sources schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "required": [
                                    "esia",
                                    "user"
                                ],
                                "properties": {
                                    "esia": {
                                        "$id": "#/properties/data/items/anyOf/0/properties/sources/properties/esia",
                                        "type": "array",
                                        "title": "The esia schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": [],
                                        "additionalItems": True,
                                        "items": {
                                            "$id": "#/properties/data/items/anyOf/0/properties/sources/properties/esia/items",
                                            "anyOf": [
                                                {
                                                    "$id": "#/properties/data/items/anyOf/0/properties/sources/properties/esia/items/anyOf/0",
                                                    "type": "string"
                                                }
                                            ]
                                        }
                                    },
                                    "user": {
                                        "$id": "#/properties/data/items/anyOf/0/properties/sources/properties/user",
                                        "type": "array",
                                        "title": "The user schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": [],
                                        "additionalItems": True,
                                        "items": {
                                            "$id": "#/properties/data/items/anyOf/0/properties/sources/properties/user/items",
                                            "anyOf": [
                                                {
                                                    "$id": "#/properties/data/items/anyOf/0/properties/sources/properties/user/items/anyOf/0",
                                                    "type": "string"
                                                }
                                            ]
                                        }
                                    }
                                },
                                "additionalProperties": True
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "meta": {
            "$id": "#/properties/meta",
            "type": "object",
            "title": "The meta schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "elementsQuantity",
                "currentPage",
                "pageSize",
                "pagesQuantity"
            ],
            "properties": {
                "elementsQuantity": {
                    "$id": "#/properties/meta/properties/elementsQuantity",
                    "type": "integer"
                },
                "currentPage": {
                    "$id": "#/properties/meta/properties/currentPage",
                    "type": "integer"
                },
                "pageSize": {
                    "$id": "#/properties/meta/properties/pageSize",
                    "type": "integer"
                },
                "pagesQuantity": {
                    "$id": "#/properties/meta/properties/pagesQuantity",
                    "type": "integer"
                }
            },
            "additionalProperties": True
        }
    },
    "additionalProperties": True
}

POST_employee_management_find_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "totalElements": 0,
            "totalPages": 0,
            "sort": {
                "sorted": True,
                "unsorted": True,
                "empty": True
            },
            "numberOfElements": 0,
            "pageable": {
                "sort": {
                    "sorted": True,
                    "unsorted": True,
                    "empty": True
                },
                "paged": True,
                "unpaged": True,
                "pageNumber": 0,
                "pageSize": 0,
                "offset": 0
            },
            "first": True,
            "last": True,
            "size": 0,
            "content": [
                {
                    "id": "string",
                    "orgId": "string",
                    "deleted": True,
                    "attributes": {
                        "additionalProp1": "string",
                        "additionalProp2": "string",
                        "additionalProp3": "string"
                    },
                    "sources": {
                        "esia": [
                            "string"
                        ],
                        "user": [
                            "string"
                        ]
                    }
                }
            ],
            "number": 0,
            "empty": True
        }
    ],
    "required": [
        "totalElements",
        "totalPages",
        "sort",
        "numberOfElements",
        "pageable",
        "first",
        "last",
        "size",
        "content",
        "number",
        "empty"
    ],
    "properties": {
        "totalElements": {
            "$id": "#/properties/totalElements",
            "type": "integer",
            "title": "The totalElements schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "totalPages": {
            "$id": "#/properties/totalPages",
            "type": "integer",
            "title": "The totalPages schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "sort": {
            "$id": "#/properties/sort",
            "type": "object",
            "title": "The sort schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "sorted": True,
                    "unsorted": True,
                    "empty": True
                }
            ],
            "required": [
                "sorted",
                "unsorted",
                "empty"
            ],
            "properties": {
                "sorted": {
                    "$id": "#/properties/sort/properties/sorted",
                    "type": "boolean",
                    "title": "The sorted schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "unsorted": {
                    "$id": "#/properties/sort/properties/unsorted",
                    "type": "boolean",
                    "title": "The unsorted schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "empty": {
                    "$id": "#/properties/sort/properties/empty",
                    "type": "boolean",
                    "title": "The empty schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                }
            },
            "additionalProperties": True
        },
        "numberOfElements": {
            "$id": "#/properties/numberOfElements",
            "type": "integer",
            "title": "The numberOfElements schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "pageable": {
            "$id": "#/properties/pageable",
            "type": "object",
            "title": "The pageable schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "sort": {
                        "sorted": True,
                        "unsorted": True,
                        "empty": True
                    },
                    "paged": True,
                    "unpaged": True,
                    "pageNumber": 0,
                    "pageSize": 0,
                    "offset": 0
                }
            ],
            "required": [
                "sort",
                "paged",
                "unpaged",
                "pageNumber",
                "pageSize",
                "offset"
            ],
            "properties": {
                "sort": {
                    "$id": "#/properties/pageable/properties/sort",
                    "type": "object",
                    "title": "The sort schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "examples": [
                        {
                            "sorted": True,
                            "unsorted": True,
                            "empty": True
                        }
                    ],
                    "required": [
                        "sorted",
                        "unsorted",
                        "empty"
                    ],
                    "properties": {
                        "sorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/sorted",
                            "type": "boolean",
                            "title": "The sorted schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": False,
                            "examples": [
                                True
                            ]
                        },
                        "unsorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/unsorted",
                            "type": "boolean",
                            "title": "The unsorted schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": False,
                            "examples": [
                                True
                            ]
                        },
                        "empty": {
                            "$id": "#/properties/pageable/properties/sort/properties/empty",
                            "type": "boolean",
                            "title": "The empty schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": False,
                            "examples": [
                                True
                            ]
                        }
                    },
                    "additionalProperties": True
                },
                "paged": {
                    "$id": "#/properties/pageable/properties/paged",
                    "type": "boolean",
                    "title": "The paged schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "unpaged": {
                    "$id": "#/properties/pageable/properties/unpaged",
                    "type": "boolean",
                    "title": "The unpaged schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "pageNumber": {
                    "$id": "#/properties/pageable/properties/pageNumber",
                    "type": "integer",
                    "title": "The pageNumber schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        0
                    ]
                },
                "pageSize": {
                    "$id": "#/properties/pageable/properties/pageSize",
                    "type": "integer",
                    "title": "The pageSize schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        0
                    ]
                },
                "offset": {
                    "$id": "#/properties/pageable/properties/offset",
                    "type": "integer",
                    "title": "The offset schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        0
                    ]
                }
            },
            "additionalProperties": True
        },
        "first": {
            "$id": "#/properties/first",
            "type": "boolean",
            "title": "The first schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        },
        "last": {
            "$id": "#/properties/last",
            "type": "boolean",
            "title": "The last schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        },
        "size": {
            "$id": "#/properties/size",
            "type": "integer",
            "title": "The size schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "content": {
            "$id": "#/properties/content",
            "type": "array",
            "title": "The content schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "id": "string",
                        "orgId": "string",
                        "deleted": True,
                        "attributes": {
                            "additionalProp1": "string",
                            "additionalProp2": "string",
                            "additionalProp3": "string"
                        },
                        "sources": {
                            "esia": [
                                "string"
                            ],
                            "user": [
                                "string"
                            ]
                        }
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/content/items",
                "anyOf": [
                    {
                        "$id": "#/properties/content/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "id": "string",
                                "orgId": "string",
                                "deleted": True,
                                "attributes": {
                                    "additionalProp1": "string",
                                    "additionalProp2": "string",
                                    "additionalProp3": "string"
                                },
                                "sources": {
                                    "esia": [
                                        "string"
                                    ],
                                    "user": [
                                        "string"
                                    ]
                                }
                            }
                        ],
                        "required": [
                            "id",
                            "orgId",
                            "deleted",
                            "attributes",
                        ],
                        "properties": {
                            "id": {
                                "$id": "#/properties/content/items/anyOf/0/properties/id",
                                "type": "string",
                                "title": "The id schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "string"
                                ]
                            },
                            "orgId": {
                                "$id": "#/properties/content/items/anyOf/0/properties/orgId",
                                "type": "string",
                                "title": "The orgId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "string"
                                ]
                            },
                            "deleted": {
                                "$id": "#/properties/content/items/anyOf/0/properties/deleted",
                                "type": "boolean",
                                "title": "The deleted schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": False,
                                "examples": [
                                    True
                                ]
                            },
                            "attributes": {
                                "$id": "#/properties/content/items/anyOf/0/properties/attributes",
                                "type": "object",
                                "title": "The attributes schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "additionalProp1": "string",
                                        "additionalProp2": "string",
                                        "additionalProp3": "string"
                                    }
                                ],
                                "required": [
                                ],
                                "properties": {
                                    "additionalProp1": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/attributes/properties/additionalProp1",
                                        "type": "string",
                                        "title": "The additionalProp1 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    },
                                    "additionalProp2": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/attributes/properties/additionalProp2",
                                        "type": "string",
                                        "title": "The additionalProp2 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    },
                                    "additionalProp3": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/attributes/properties/additionalProp3",
                                        "type": "string",
                                        "title": "The additionalProp3 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    }
                                },
                                "additionalProperties": True
                            },
                            "sources": {
                                "$id": "#/properties/content/items/anyOf/0/properties/sources",
                                "type": "object",
                                "title": "The sources schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "esia": [
                                            "string"
                                        ],
                                        "user": [
                                            "string"
                                        ]
                                    }
                                ],
                                "required": [
                                    "esia",
                                    "user"
                                ],
                                "properties": {
                                    "esia": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/sources/properties/esia",
                                        "type": "array",
                                        "title": "The esia schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": [],
                                        "examples": [
                                            [
                                                "string"
                                            ]
                                        ],
                                        "additionalItems": True,
                                        "items": {
                                            "$id": "#/properties/content/items/anyOf/0/properties/sources/properties/esia/items",
                                            "anyOf": [
                                                {
                                                    "$id": "#/properties/content/items/anyOf/0/properties/sources/properties/esia/items/anyOf/0",
                                                    "type": "string",
                                                    "title": "The first anyOf schema",
                                                    "description": "An explanation about the purpose of this instance.",
                                                    "default": "",
                                                    "examples": [
                                                        "string"
                                                    ]
                                                }
                                            ]
                                        }
                                    },
                                    "user": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/sources/properties/user",
                                        "type": "array",
                                        "title": "The user schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": [],
                                        "examples": [
                                            [
                                                "string"
                                            ]
                                        ],
                                        "additionalItems": True,
                                        "items": {
                                            "$id": "#/properties/content/items/anyOf/0/properties/sources/properties/user/items",
                                            "anyOf": [
                                                {
                                                    "$id": "#/properties/content/items/anyOf/0/properties/sources/properties/user/items/anyOf/0",
                                                    "type": "string",
                                                    "title": "The first anyOf schema",
                                                    "description": "An explanation about the purpose of this instance.",
                                                    "default": "",
                                                    "examples": [
                                                        "string"
                                                    ]
                                                }
                                            ]
                                        }
                                    }
                                },
                                "additionalProperties": True
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "number": {
            "$id": "#/properties/number",
            "type": "integer",
            "title": "The number schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "empty": {
            "$id": "#/properties/empty",
            "type": "boolean",
            "title": "The empty schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        }
    },
    "additionalProperties": True
}

POST_employee_management_add_201_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "id",
        "orgId",
        "attributes",
        # "sources"
    ],
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "string",
            "title": "The id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": ""
        },
        "orgId": {
            "$id": "#/properties/orgId",
            "type": "string",
            "title": "The orgId schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
        },
        "deleted": {
            "$id": "#/properties/deleted",
            "type": "boolean",
            "title": "The deleted schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
        },
        "attributes": {
            "$id": "#/properties/attributes",
            "type": "object",
            "title": "The attributes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
            ],
            "properties": {
                "additionalProp1": {
                    "$id": "#/properties/attributes/properties/additionalProp1",
                    "type": "string"
                },
            },
            "additionalProperties": True
        },
        "sources": {
            "$id": "#/properties/sources",
            "type": "object",
            "title": "The sources schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "esia",
                "user"
            ],
            "properties": {
                "esia": {
                    "$id": "#/properties/sources/properties/esia",
                    "type": "array",
                    "title": "The esia schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": [],
                    "additionalItems": True,
                    "items": {
                        "$id": "#/properties/sources/properties/esia/items",
                        "anyOf": [
                            {
                                "$id": "#/properties/sources/properties/esia/items/anyOf/0",
                                "type": "string"
                            }
                        ]
                    }
                },
                "user": {
                    "$id": "#/properties/sources/properties/user",
                    "type": "array",
                    "additionalItems": True,
                    "items": {
                        "$id": "#/properties/sources/properties/user/items",
                        "anyOf": [
                            {
                                "$id": "#/properties/sources/properties/user/items/anyOf/0",
                                "type": "string"
                            }
                        ]
                    }
                }
            },
            "additionalProperties": True
        }
    },
    "additionalProperties": True
}

GET_profile_user_id_data_all_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    ],
    "properties": {
        "additionalProp1": {
            "$id": "#/properties/additionalProp1",
            "type": "string",
        },
    },
    "additionalProperties": True
}

GET_profile_user_user_id_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "userId",
        "region",
        "role",
        "status"
    ],
    "properties": {
        "userId": {
            "$id": "#/properties/userId",
            "type": "string"
        },
        "region": {
            "$id": "#/properties/region",
            "type": "string"
        },
        "role": {
            "$id": "#/properties/role",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": "object",
            "required": [
                "status",
                "documentLink"
            ],
            "properties": {
                "status": {
                    "$id": "#/properties/status/properties/status",
                    "type": "string",
                },
                "documentLink": {
                    "$id": "#/properties/status/properties/documentLink",
                    "type": "string",
                }
            },
            "additionalProperties": True
        }
    },
    "additionalProperties": True
}

POST_profile_users_find_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "totalElements",
        "totalPages",
        "sort",
        "last",
        "numberOfElements",
        "pageable",
        "first",
        "size",
        "content",
        "number",
        "empty"
    ],
    "properties": {
        "totalElements": {
            "$id": "#/properties/totalElements",
            "type": "integer",
            "totalPages": {
                "$id": "#/properties/totalPages",
                "type": "integer",
            },
            "sort": {
                "$id": "#/properties/sort",
                "type": "object",
                "title": "The sort schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "unsorted",
                    "sorted",
                    "empty"
                ],
                "properties": {
                    "unsorted": {
                        "$id": "#/properties/sort/properties/unsorted",
                        "type": "boolean",
                    },
                    "sorted": {
                        "$id": "#/properties/sort/properties/sorted",
                        "type": "boolean",
                    },
                    "empty": {
                        "$id": "#/properties/sort/properties/empty",
                        "type": "boolean",
                    }
                },
                "additionalProperties": True
            },
            "last": {
                "$id": "#/properties/last",
                "type": "boolean",
            },
            "numberOfElements": {
                "$id": "#/properties/numberOfElements",
                "type": "integer",
                "title": "The numberOfElements schema",
                "description": "An explanation about the purpose of this instance.",
                "default": 0,
                "examples": [
                    0
                ]
            },
            "pageable": {
                "$id": "#/properties/pageable",
                "type": "object",
                "title": "The pageable schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "page",
                    "size",
                    "sort"
                ],
                "properties": {
                    "page": {
                        "$id": "#/properties/pageable/properties/page",
                        "type": "integer",
                    },
                    "size": {
                        "$id": "#/properties/pageable/properties/size",
                        "type": "integer",
                    },
                    "sort": {
                        "$id": "#/properties/pageable/properties/sort",
                        "type": "array",
                        "additionalItems": True,
                        "items": {
                            "$id": "#/properties/pageable/properties/sort/items",
                            "anyOf": [
                                {
                                    "$id": "#/properties/pageable/properties/sort/items/anyOf/0",
                                    "type": "string",
                                }
                            ]
                        }
                    }
                },
                "additionalProperties": True
            },
            "first": {
                "$id": "#/properties/first",
                "type": "boolean",
            },
            "size": {
                "$id": "#/properties/size",
                "type": "integer",
                "title": "The size schema",
                "description": "An explanation about the purpose of this instance.",
                "default": 0,
            },
            "content": {
                "$id": "#/properties/content",
                "type": "array",
                "title": "The content schema",
                "description": "An explanation about the purpose of this instance.",
                "default": [],
                "additionalItems": True,
                "items": {
                    "$id": "#/properties/content/items",
                    "anyOf": [
                        {
                            "$id": "#/properties/content/items/anyOf/0",
                            "type": "object",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": {},
                            "properties": {
                                "additionalProp1": {
                                    "$id": "#/properties/content/items/anyOf/0/properties/additionalProp1",
                                    "type": "string"
                                }
                            },
                            "additionalProperties": True
                        }
                    ]
                }
            },
            "number": {
                "$id": "#/properties/number",
                "type": "integer",
            },
            "empty": {
                "$id": "#/properties/empty",
                "type": "boolean"
            }
        },
        "additionalProperties": True
    }
}

GET_profile_users_data_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "totalElements",
        "totalPages",
        "sort",
        "numberOfElements",
        "last",
        "pageable",
        "first",
        "size",
        "content",
        "number",
        "empty"
    ],
    "properties": {
        "totalElements": {
            "$id": "#/properties/totalElements",
            "type": "integer",
        },
        "totalPages": {
            "$id": "#/properties/totalPages",
            "type": "integer",
        },
        "sort": {
            "$id": "#/properties/sort",
            "type": "object",
            "title": "The sort schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "unsorted",
                "sorted",
                "empty"
            ],
            "properties": {
                "unsorted": {
                    "$id": "#/properties/sort/properties/unsorted",
                    "type": "boolean",
                },
                "sorted": {
                    "$id": "#/properties/sort/properties/sorted",
                    "type": "boolean",
                },
                "empty": {
                    "$id": "#/properties/sort/properties/empty",
                    "type": "boolean",
                }
            },
            "additionalProperties": True
        },
        "numberOfElements": {
            "$id": "#/properties/numberOfElements",
            "type": "integer",
        },
        "last": {
            "$id": "#/properties/last",
            "type": "boolean",
        },
        "pageable": {
            "$id": "#/properties/pageable",
            "type": "object",
            "title": "The pageable schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "sort",
                "paged",
                "unpaged",
                "pageNumber",
                "pageSize",
                "offset"
            ],
            "properties": {
                "sort": {
                    "$id": "#/properties/pageable/properties/sort",
                    "type": "object",
                    "title": "The sort schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "required": [
                        "unsorted",
                        "sorted",
                        "empty"
                    ],
                    "properties": {
                        "unsorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/unsorted",
                            "type": "boolean",
                        },
                        "sorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/sorted",
                            "type": "boolean",
                        },
                        "empty": {
                            "$id": "#/properties/pageable/properties/sort/properties/empty",
                            "type": "boolean",
                        }
                    },
                    "additionalProperties": True
                },
                "paged": {
                    "$id": "#/properties/pageable/properties/paged",
                    "type": "boolean",
                },
                "unpaged": {
                    "$id": "#/properties/pageable/properties/unpaged",
                    "type": "boolean",
                },
                "pageNumber": {
                    "$id": "#/properties/pageable/properties/pageNumber",
                    "type": "integer",
                },
                "pageSize": {
                    "$id": "#/properties/pageable/properties/pageSize",
                    "type": "integer",
                },
                "offset": {
                    "$id": "#/properties/pageable/properties/offset",
                    "type": "integer",
                }
            },
            "additionalProperties": True
        },
        "first": {
            "$id": "#/properties/first",
            "type": "boolean",
        },
        "size": {
            "$id": "#/properties/size",
            "type": "integer",
        },
        "content": {
            "$id": "#/properties/content",
            "type": "array",
            "title": "The content schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/content/items",
                "anyOf": [
                    {
                        "$id": "#/properties/content/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "required": [
                            "userData",
                            "attributes"
                        ],
                        "properties": {
                            "userData": {
                                "$id": "#/properties/content/items/anyOf/0/properties/userData",
                                "type": "object",
                                "title": "The userData schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "required": [
                                    "userId",
                                    "region",
                                    "role",
                                    "status"
                                ],
                                "properties": {
                                    "userId": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/userData/properties/userId",
                                        "type": "string",
                                    },
                                    "region": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/userData/properties/region",
                                        "type": "string",
                                    },
                                    "role": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/userData/properties/role",
                                        "type": "string",
                                    },
                                    "status": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/userData/properties/status",
                                        "type": "object",
                                        "title": "The status schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": {},
                                        "examples": [
                                            {
                                                "status": "string",
                                                "documentLink": "string"
                                            }
                                        ],
                                        "required": [
                                            "status",
                                            "documentLink"
                                        ],
                                        "properties": {
                                            "status": {
                                                "$id": "#/properties/content/items/anyOf/0/properties/userData/properties/status/properties/status",
                                                "type": "string",
                                            },
                                            "documentLink": {
                                                "$id": "#/properties/content/items/anyOf/0/properties/userData/properties/status/properties/documentLink",
                                                "type": "string",
                                            }
                                        },
                                        "additionalProperties": True
                                    }
                                },
                                "additionalProperties": True
                            },
                            "attributes": {
                                "$id": "#/properties/content/items/anyOf/0/properties/attributes",
                                "type": "array",
                                "title": "The attributes schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": [],
                                "additionalItems": True,
                                "items": {
                                    "$id": "#/properties/content/items/anyOf/0/properties/attributes/items",
                                    "anyOf": [
                                        {
                                            "$id": "#/properties/content/items/anyOf/0/properties/attributes/items/anyOf/0",
                                            "type": "object",
                                            "required": [
                                                "name",
                                                "value"
                                            ],
                                            "properties": {
                                                "name": {
                                                    "$id": "#/properties/content/items/anyOf/0/properties/attributes/items/anyOf/0/properties/name",
                                                    "type": "string",
                                                },
                                                "value": {
                                                    "$id": "#/properties/content/items/anyOf/0/properties/attributes/items/anyOf/0/properties/value",
                                                    "type": "string",
                                                },
                                                "multiple": {
                                                    "$id": "#/properties/content/items/anyOf/0/properties/attributes/items/anyOf/0/properties/multiple",
                                                    "type": "boolean",
                                                }
                                            },
                                            "additionalProperties": True
                                        }
                                    ]
                                }
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "number": {
            "$id": "#/properties/number",
            "type": "integer",
        },
        "empty": {
            "$id": "#/properties/empty",
            "type": "boolean"
        }
    },
    "additionalProperties": True
}

GET_profile_data_region_all_constructor_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "totalElements",
        "totalPages",
        "sort",
        "numberOfElements",
        "last",
        "pageable",
        "first",
        "size",
        "content",
        "number",
        "empty"
    ],
    "properties": {
        "totalElements": {
            "$id": "#/properties/totalElements",
            "type": "integer",
        },
        "totalPages": {
            "$id": "#/properties/totalPages",
            "type": "integer",
        },
        "sort": {
            "$id": "#/properties/sort",
            "type": "object",
            "title": "The sort schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "unsorted",
                "sorted",
                "empty"
            ],
            "properties": {
                "unsorted": {
                    "$id": "#/properties/sort/properties/unsorted",
                    "type": "boolean",
                },
                "sorted": {
                    "$id": "#/properties/sort/properties/sorted",
                    "type": "boolean",
                },
                "empty": {
                    "$id": "#/properties/sort/properties/empty",
                    "type": "boolean",
                }
            },
            "additionalProperties": True
        },
        "numberOfElements": {
            "$id": "#/properties/numberOfElements",
            "type": "integer",
        },
        "last": {
            "$id": "#/properties/last",
            "type": "boolean",
        },
        "pageable": {
            "$id": "#/properties/pageable",
            "type": "object",
            "title": "The pageable schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "sort",
                "paged",
                "unpaged",
                "pageNumber",
                "pageSize",
                "offset"
            ],
            "properties": {
                "sort": {
                    "$id": "#/properties/pageable/properties/sort",
                    "type": "object",
                    "title": "The sort schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "required": [
                        "unsorted",
                        "sorted",
                        "empty"
                    ],
                    "properties": {
                        "unsorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/unsorted",
                            "type": "boolean",
                        },
                        "sorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/sorted",
                            "type": "boolean",
                        },
                        "empty": {
                            "$id": "#/properties/pageable/properties/sort/properties/empty",
                            "type": "boolean",
                        }
                    },
                    "additionalProperties": True
                },
                "paged": {
                    "$id": "#/properties/pageable/properties/paged",
                    "type": "boolean",
                },
                "unpaged": {
                    "$id": "#/properties/pageable/properties/unpaged",
                    "type": "boolean",
                },
                "pageNumber": {
                    "$id": "#/properties/pageable/properties/pageNumber",
                    "type": "integer",
                },
                "pageSize": {
                    "$id": "#/properties/pageable/properties/pageSize",
                    "type": "integer",
                },
                "offset": {
                    "$id": "#/properties/pageable/properties/offset",
                    "type": "integer",
                }
            },
            "additionalProperties": True
        },
        "first": {
            "$id": "#/properties/first",
            "type": "boolean",
        },
        "size": {
            "$id": "#/properties/size",
            "type": "integer",
        },
        "content": {
            "$id": "#/properties/content",
            "type": "array",
            "title": "The content schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/content/items",
                "anyOf": [
                    {
                        "$id": "#/properties/content/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "properties": {
                            "userData": {
                                "$id": "#/properties/content/items/anyOf/0/properties/userData",
                                "type": "object",
                            },
                            "additionalProperties": True
                        }
                    }
                ]
            }
        },
        "number": {
            "$id": "#/properties/number",
            "type": "integer",
        },
        "empty": {
            "$id": "#/properties/empty",
            "type": "boolean"
        }
    },
    "additionalProperties": True
}

GET_profile_users_shtp_200_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "totalElements",
        "totalPages",
        "sort",
        "numberOfElements",
        "last",
        "pageable",
        "first",
        "size",
        "content",
        "number",
        "empty"
    ],
    "properties": {
        "totalElements": {
            "$id": "#/properties/totalElements",
            "type": "integer",
        },
        "totalPages": {
            "$id": "#/properties/totalPages",
            "type": "integer",
        },
        "sort": {
            "$id": "#/properties/sort",
            "type": "object",
            "title": "The sort schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "unsorted",
                "sorted",
                "empty"
            ],
            "properties": {
                "unsorted": {
                    "$id": "#/properties/sort/properties/unsorted",
                    "type": "boolean",
                },
                "sorted": {
                    "$id": "#/properties/sort/properties/sorted",
                    "type": "boolean",
                },
                "empty": {
                    "$id": "#/properties/sort/properties/empty",
                    "type": "boolean",
                }
            },
            "additionalProperties": True
        },
        "numberOfElements": {
            "$id": "#/properties/numberOfElements",
            "type": "integer",
        },
        "last": {
            "$id": "#/properties/last",
            "type": "boolean",
        },
        "pageable": {
            "$id": "#/properties/pageable",
            "type": "object",
            "title": "The pageable schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "required": [
                "sort",
                "paged",
                "unpaged",
                "pageNumber",
                "pageSize",
                "offset"
            ],
            "properties": {
                "sort": {
                    "$id": "#/properties/pageable/properties/sort",
                    "type": "object",
                    "title": "The sort schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "required": [
                        "unsorted",
                        "sorted",
                        "empty"
                    ],
                    "properties": {
                        "unsorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/unsorted",
                            "type": "boolean",
                        },
                        "sorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/sorted",
                            "type": "boolean",
                        },
                        "empty": {
                            "$id": "#/properties/pageable/properties/sort/properties/empty",
                            "type": "boolean",
                        }
                    },
                    "additionalProperties": True
                },
                "paged": {
                    "$id": "#/properties/pageable/properties/paged",
                    "type": "boolean",
                },
                "unpaged": {
                    "$id": "#/properties/pageable/properties/unpaged",
                    "type": "boolean",
                },
                "pageNumber": {
                    "$id": "#/properties/pageable/properties/pageNumber",
                    "type": "integer",
                },
                "pageSize": {
                    "$id": "#/properties/pageable/properties/pageSize",
                    "type": "integer",
                },
                "offset": {
                    "$id": "#/properties/pageable/properties/offset",
                    "type": "integer",
                }
            },
            "additionalProperties": True
        },
        "first": {
            "$id": "#/properties/first",
            "type": "boolean",
        },
        "size": {
            "$id": "#/properties/size",
            "type": "integer",
        },
        "content": {
            "$id": "#/properties/content",
            "type": "array",
            "title": "The content schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/content/items",
                "anyOf": [
                    {
                        "$id": "#/properties/content/items/anyOf/0",
                        "type": "string",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "properties": {
                            "userData": {
                                "$id": "#/properties/content/items/anyOf/0/properties/userData",
                                "type": "object",
                            },
                            "additionalProperties": True
                        }
                    }
                ]
            }
        },
        "number": {
            "$id": "#/properties/number",
            "type": "integer",
        },
        "empty": {
            "$id": "#/properties/empty",
            "type": "boolean"
        }
    },
    "additionalProperties": True
}

GET_profile_user_id_revision_all_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "revision",
                    "version",
                    "date",
                    "value",
                    "source"
                ],
                "properties": {
                    "revision": {
                        "$id": "#/items/anyOf/0/properties/revision",
                        "type": "integer",
                    },
                    "version": {
                        "$id": "#/items/anyOf/0/properties/version",
                        "type": "integer",
                    },
                    "date": {
                        "$id": "#/items/anyOf/0/properties/date",
                        "type": "string",
                    },
                    "value": {
                        "$id": "#/items/anyOf/0/properties/value",
                        "type": "string",
                    },
                    "source": {
                        "$id": "#/items/anyOf/0/properties/source",
                        "type": "string",
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_user_id_attributes_history_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "userId",
        "actualAttributes",
        "deletedAttributes"
    ],
    "properties": {
        "userId": {
            "$id": "#/properties/userId",
            "type": "string",
        },
        "actualAttributes": {
            "$id": "#/properties/actualAttributes",
            "type": "array",
            "title": "The actualAttributes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/actualAttributes/items",
                "anyOf": [
                    {
                        "$id": "#/properties/actualAttributes/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "required": [
                            "attributeName",
                            "revisions"
                        ],
                        "properties": {
                            "attributeName": {
                                "$id": "#/properties/actualAttributes/items/anyOf/0/properties/attributeName",
                                "type": "string",
                            },
                            "revisions": {
                                "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions",
                                "type": "array",
                                "title": "The revisions schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": [],
                                "additionalItems": True,
                                "items": {
                                    "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions/items",
                                    "anyOf": [
                                        {
                                            "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions/items/anyOf/0",
                                            "type": "object",
                                            "title": "The first anyOf schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": {},
                                            "required": [
                                                "revision",
                                                "version",
                                                "date",
                                                "value",
                                                "source"
                                            ],
                                            "properties": {
                                                "revision": {
                                                    "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/revision",
                                                    "type": "integer",
                                                },
                                                "version": {
                                                    "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/version",
                                                    "type": "integer",
                                                },
                                                "date": {
                                                    "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/date",
                                                    "type": "string",
                                                },
                                                "value": {
                                                    "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/value",
                                                    "type": "string",
                                                },
                                                "source": {
                                                    "$id": "#/properties/actualAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/source",
                                                    "type": "string",
                                                }
                                            },
                                            "additionalProperties": True
                                        }
                                    ]
                                }
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "deletedAttributes": {
            "$id": "#/properties/deletedAttributes",
            "type": "array",
            "title": "The deletedAttributes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/deletedAttributes/items",
                "anyOf": [
                    {
                        "$id": "#/properties/deletedAttributes/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "required": [
                            "attributeName",
                            "revisions"
                        ],
                        "properties": {
                            "attributeName": {
                                "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/attributeName",
                                "type": "string",
                            },
                            "revisions": {
                                "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions",
                                "type": "array",
                                "title": "The revisions schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": [],
                                "additionalItems": True,
                                "items": {
                                    "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions/items",
                                    "anyOf": [
                                        {
                                            "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions/items/anyOf/0",
                                            "type": "object",
                                            "title": "The first anyOf schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": {},
                                            "required": [
                                                "revision",
                                                "version",
                                                "date",
                                                "value",
                                                "source"
                                            ],
                                            "properties": {
                                                "revision": {
                                                    "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/revision",
                                                    "type": "integer",
                                                },
                                                "version": {
                                                    "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/version",
                                                    "type": "integer",
                                                },
                                                "date": {
                                                    "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/date",
                                                    "type": "string",
                                                },
                                                "value": {
                                                    "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/value",
                                                    "type": "string",
                                                },
                                                "source": {
                                                    "$id": "#/properties/deletedAttributes/items/anyOf/0/properties/revisions/items/anyOf/0/properties/source",
                                                    "type": "string",
                                                },
                                                "additionalProperties": True
                                            }
                                            
                                        }
                                    ]
                                }
                            },
                            "additionalProperties": True
                        }
                    }
                ]
            }
        }
        
    },
    "additionalProperties": True
}

PUT_profile_mgp_recipient_id_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "id": "005de354-c176-4359-9c5e-1d2c8552fa8e",
            "status": "POTENTIAL",
            "statusDate": "2021-07-11T21:00:00.000+00:00",
            "okopf": None,
            "userId": "testUser-QA50HT88"
        }
    ],
    "required": [
        "id",
        "status",
        "statusDate",
        "okopf",
        "userId"
    ],
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "string"
        },
        "status": {
            "$id": "#/properties/status",
            "type": "string"
        },
        "statusDate": {
            "$id": "#/properties/statusDate",
            "type": "string"
        },
        "okopf": {
            "$id": "#/properties/okopf",
            "type": "string"
        },
        "userId": {
            "$id": "#/properties/userId",
            "type": "string"
        }
    },
    "additionalProperties": True
}

GET_profile_revision_uuid_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "additionalItems": True,
    "items": {
        "$id": "#/items",
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "required": [
                    "version",
                    "date",
                ],
                "properties": {
                    "revision": {
                        "$id": "#/items/anyOf/0/properties/revision",
                        "type": "integer",
                        "title": "The revision schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": 0,
                        "examples": [
                            0
                        ]
                    },
                    "version": {
                        "$id": "#/items/anyOf/0/properties/version",
                        "type": "integer",
                        "title": "The version schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": 0,
                        "examples": [
                            0
                        ]
                    },
                    "date": {
                        "$id": "#/items/anyOf/0/properties/date",
                        "type": "string",
                        "title": "The date schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "2022-02-17T15:46:43.389Z"
                        ]
                    },
                    "value": {
                        "$id": "#/items/anyOf/0/properties/value",
                        "type": "string",
                        "title": "The value schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    },
                    "source": {
                        "$id": "#/items/anyOf/0/properties/source",
                        "type": "string",
                        "title": "The source schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "string"
                        ]
                    }
                },
                "additionalProperties": True
            }
        ]
    }
}

GET_profile_revision_uuid_main_schema_wrong = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "description": "The root schema is the schema that comprises the entire JSON document.",
    "default": {},
    "required": [
        "checked",
        "dimensions",
        "id",
        "name",
        "price",
        "tags"
    ],
    "properties": {
        "checked": {
            "$id": "#/properties/checked",
            "type": "boolean",
            "title": "The Checked Schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                False
            ]
        },
        "dimensions": {
            "$id": "#/properties/dimensions",
            "type": "object",
            "title": "The Dimensions Schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "height": 10.0,
                    "width": 5.0
                }
            ],
            "required": [
                "width",
                "height"
            ],
            "properties": {
                "width": {
                    "$id": "#/properties/dimensions/properties/width",
                    "type": "integer",
                    "title": "The Width Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        5
                    ]
                },
                "height": {
                    "$id": "#/properties/dimensions/properties/height",
                    "type": "integer",
                    "title": "The Height Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        10
                    ]
                }
            }
        },
        "id": {
            "$id": "#/properties/id",
            "type": "integer",
            "title": "The Id Schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                1
            ]
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The Name Schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "A green door"
            ]
        },
        "price": {
            "$id": "#/properties/price",
            "type": "number",
            "title": "The Price Schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                12.5
            ]
        },
        "tags": {
            "$id": "#/properties/tags",
            "type": "array",
            "title": "The Tags Schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    "home",
                    "green"
                ]
            ],
            "items": {
                "$id": "#/properties/tags/items",
                "type": "string",
                "title": "The Items Schema",
                "description": "An explanation about the purpose of this instance.",
                "default": "",
                "examples": [
                    "home",
                    "green"
                ]
            }
        }
    }
}

GET_profile_document_document_id_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "fileName",
        "createdBy",
        "updatedBy",
        "deletedBy",
        "documentId",
        "createOn",
        "updatedOn",
        "description",
        "expiresOn",
        "metadata",
        "deleted"
    ],
    "properties": {
        "fileName": {
            "$id": "#/properties/fileName",
            "type": "string",
            "title": "The fileName schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "string"
            ]
        },
        "createdBy": {
            "$id": "#/properties/createdBy",
            "type": "string",
            "title": "The createdBy schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "string"
            ]
        },
        "updatedBy": {
            "$id": "#/properties/updatedBy",
            "type": ["null", "string"],
        },
        "deletedBy": {
            "$id": "#/properties/deletedBy",
            "type": ["null", "string"],
        },
        "documentId": {
            "$id": "#/properties/documentId",
            "type": "string",
            "title": "The documentId schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            ]
        },
        "createOn": {
            "$id": "#/properties/createOn",
            "type": "string",
            "title": "The createOn schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "2022-02-17T16:24:33.340Z"
            ]
        },
        "updatedOn": {
            "$id": "#/properties/updatedOn",
            "type": ["null", "string"],
            "title": "The updatedOn schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "2022-02-17T16:24:33.340Z"
            ]
        },
        "description": {
            "$id": "#/properties/description",
            "type": ["null", "string"],
        },
        "expiresOn": {
            "$id": "#/properties/expiresOn",
            "type": ["null", "string"],
        },
        "metadata": {
            "$id": "#/properties/metadata",
            "type": ["null", "string"],
        },
        "deleted": {
            "$id": "#/properties/deleted",
            "type": "boolean",
            "title": "The deleted schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        }
    },
    "additionalProperties": True
}

POST_profile_user_search_main_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "totalElements",
        "totalPages",
        "sort",
        "numberOfElements",
        "last",
        "pageable",
        "first",
        "size",
        "content",
        "number",
        "empty"
    ],
    "properties": {
        "totalElements": {
            "$id": "#/properties/totalElements",
            "type": "integer",
            "title": "The totalElements schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "totalPages": {
            "$id": "#/properties/totalPages",
            "type": "integer",
            "title": "The totalPages schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "sort": {
            "$id": "#/properties/sort",
            "type": "object",
            "title": "The sort schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "unsorted": True,
                    "sorted": True,
                    "empty": True
                }
            ],
            "required": [
                "unsorted",
                "sorted",
                "empty"
            ],
            "properties": {
                "unsorted": {
                    "$id": "#/properties/sort/properties/unsorted",
                    "type": "boolean",
                    "title": "The unsorted schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "sorted": {
                    "$id": "#/properties/sort/properties/sorted",
                    "type": "boolean",
                    "title": "The sorted schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "empty": {
                    "$id": "#/properties/sort/properties/empty",
                    "type": "boolean",
                    "title": "The empty schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                }
            },
            "additionalProperties": True
        },
        "numberOfElements": {
            "$id": "#/properties/numberOfElements",
            "type": "integer",
            "title": "The numberOfElements schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "last": {
            "$id": "#/properties/last",
            "type": "boolean",
            "title": "The last schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        },
        "pageable": {
            "$id": "#/properties/pageable",
            "type": "object",
            "title": "The pageable schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "sort": {
                        "unsorted": True,
                        "sorted": True,
                        "empty": True
                    },
                    "paged": True,
                    "unpaged": True,
                    "pageNumber": 0,
                    "pageSize": 0,
                    "offset": 0
                }
            ],
            "required": [
                "sort",
                "paged",
                "unpaged",
                "pageNumber",
                "pageSize",
                "offset"
            ],
            "properties": {
                "sort": {
                    "$id": "#/properties/pageable/properties/sort",
                    "type": "object",
                    "title": "The sort schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "examples": [
                        {
                            "unsorted": True,
                            "sorted": True,
                            "empty": True
                        }
                    ],
                    "required": [
                        "unsorted",
                        "sorted",
                        "empty"
                    ],
                    "properties": {
                        "unsorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/unsorted",
                            "type": "boolean",
                            "title": "The unsorted schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": False,
                            "examples": [
                                True
                            ]
                        },
                        "sorted": {
                            "$id": "#/properties/pageable/properties/sort/properties/sorted",
                            "type": "boolean",
                            "title": "The sorted schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": False,
                            "examples": [
                                True
                            ]
                        },
                        "empty": {
                            "$id": "#/properties/pageable/properties/sort/properties/empty",
                            "type": "boolean",
                            "title": "The empty schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": False,
                            "examples": [
                                True
                            ]
                        }
                    },
                    "additionalProperties": True
                },
                "paged": {
                    "$id": "#/properties/pageable/properties/paged",
                    "type": "boolean",
                    "title": "The paged schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "unpaged": {
                    "$id": "#/properties/pageable/properties/unpaged",
                    "type": "boolean",
                    "title": "The unpaged schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [
                        True
                    ]
                },
                "pageNumber": {
                    "$id": "#/properties/pageable/properties/pageNumber",
                    "type": "integer",
                    "title": "The pageNumber schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        0
                    ]
                },
                "pageSize": {
                    "$id": "#/properties/pageable/properties/pageSize",
                    "type": "integer",
                    "title": "The pageSize schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        0
                    ]
                },
                "offset": {
                    "$id": "#/properties/pageable/properties/offset",
                    "type": "integer",
                    "title": "The offset schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [
                        0
                    ]
                }
            },
            "additionalProperties": True
        },
        "first": {
            "$id": "#/properties/first",
            "type": "boolean",
            "title": "The first schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        },
        "size": {
            "$id": "#/properties/size",
            "type": "integer",
            "title": "The size schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "content": {
            "$id": "#/properties/content",
            "type": "array",
            "title": "The content schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "userId": "string",
                        "region": "string",
                        "role": "string",
                        "status": {
                            "status": "string",
                            "documentLink": "string"
                        },
                        "data": {
                            "additionalProp1": "string",
                            "additionalProp2": "string",
                            "additionalProp3": "string"
                        }
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/content/items",
                "anyOf": [
                    {
                        "$id": "#/properties/content/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "userId": "string",
                                "region": "string",
                                "role": "string",
                                "status": {
                                    "status": "string",
                                    "documentLink": "string"
                                },
                                "data": {
                                    "additionalProp1": "string",
                                    "additionalProp2": "string",
                                    "additionalProp3": "string"
                                }
                            }
                        ],
                        "required": [
                            "userId",
                            "region",
                            "role",
                            "status",
                            "data"
                        ],
                        "properties": {
                            "userId": {
                                "$id": "#/properties/content/items/anyOf/0/properties/userId",
                                "type": "string",
                                "title": "The userId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "string"
                                ]
                            },
                            "region": {
                                "$id": "#/properties/content/items/anyOf/0/properties/region",
                                "type": "string",
                                "title": "The region schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "string"
                                ]
                            },
                            "role": {
                                "$id": "#/properties/content/items/anyOf/0/properties/role",
                                "type": "string",
                                "title": "The role schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "string"
                                ]
                            },
                            "status": {
                                "$id": "#/properties/content/items/anyOf/0/properties/status",
                                "type": "object",
                                "title": "The status schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "status": "string",
                                        "documentLink": "string"
                                    }
                                ],
                                "required": [
                                    "status",
                                    "documentLink"
                                ],
                                "properties": {
                                    "status": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/status/properties/status",
                                        "type": "string",
                                        "title": "The status schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    },
                                    "documentLink": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/status/properties/documentLink",
                                        "type": "string",
                                        "title": "The documentLink schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    }
                                },
                                "additionalProperties": True
                            },
                            "data": {
                                "$id": "#/properties/content/items/anyOf/0/properties/data",
                                "type": "object",
                                "title": "The data schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "required": [
                                ],
                                "properties": {
                                    "additionalProp1": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/data/properties/additionalProp1",
                                        "type": "string",
                                        "title": "The additionalProp1 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    },
                                    "additionalProp2": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/data/properties/additionalProp2",
                                        "type": "string",
                                        "title": "The additionalProp2 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    },
                                    "additionalProp3": {
                                        "$id": "#/properties/content/items/anyOf/0/properties/data/properties/additionalProp3",
                                        "type": "string",
                                        "title": "The additionalProp3 schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "string"
                                        ]
                                    }
                                },
                                "additionalProperties": True
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "number": {
            "$id": "#/properties/number",
            "type": "integer",
            "title": "The number schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "empty": {
            "$id": "#/properties/empty",
            "type": "boolean",
            "title": "The empty schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                True
            ]
        }
    },
    "additionalProperties": True
}
