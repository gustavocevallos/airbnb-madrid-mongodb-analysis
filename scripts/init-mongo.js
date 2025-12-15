// Script de inicialización de MongoDB
// Se ejecuta automáticamente cuando el contenedor de Docker se inicia

db = db.getSiblingDB('airbnb_madrid');

// Crear usuario para la base de datos
db.createUser({
    user: 'airbnb_user',
    pwd: 'airbnb_pass',
    roles: [
        {
            role: 'readWrite',
            db: 'airbnb_madrid'
        }
    ]
});

// Crear colección con validación de esquema
db.createCollection('listings', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['name', 'price'],
            properties: {
                name: {
                    bsonType: 'string',
                    description: 'Nombre del listing - requerido'
                },
                price: {
                    bsonType: ['double', 'int'],
                    minimum: 0,
                    description: 'Precio por noche - requerido y >= 0'
                },
                neighbourhood: {
                    bsonType: 'string',
                    description: 'Barrio de Madrid'
                },
                room_type: {
                    bsonType: 'string',
                    enum: ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room'],
                    description: 'Tipo de alojamiento'
                },
                latitude: {
                    bsonType: ['double'],
                    minimum: -90,
                    maximum: 90
                },
                longitude: {
                    bsonType: ['double'],
                    minimum: -180,
                    maximum: 180
                },
                availability_365: {
                    bsonType: ['int', 'double'],
                    minimum: 0,
                    maximum: 365
                },
                location: {
                    bsonType: 'object',
                    required: ['type', 'coordinates'],
                    properties: {
                        type: {
                            enum: ['Point']
                        },
                        coordinates: {
                            bsonType: 'array',
                            minItems: 2,
                            maxItems: 2
                        }
                    }
                }
            }
        }
    }
});

// Crear índices básicos
db.listings.createIndex({ price: 1 });
db.listings.createIndex({ neighbourhood: 1 });
db.listings.createIndex({ room_type: 1 });
db.listings.createIndex({ neighbourhood: 1, price: 1 });

// Índice geoespacial
db.listings.createIndex({ location: '2dsphere' });

// Índice de texto para búsqueda
db.listings.createIndex({ 
    name: 'text', 
    description: 'text' 
});

print('✅ Base de datos airbnb_madrid inicializada');
print('✅ Colección listings creada con validación de esquema');
print('✅ Índices creados exitosamente');
