db = db.getSiblingDB("blog_db");

db.createCollection("posts", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["titre", "auteur", "vues"],
            properties: {
                titre: {
                    bsonType: "string",
                    description: "doit être une chaîne"
                },
                auteur: {
                    bsonType: "string",
                    description: "doit être une chaîne"
                },
                vues: {
                    bsonType: "int",
                    description: "doit être un entier"
                },
                date: {
                    bsonType: "date",
                    description: "doit être une date"
                },
                origin: {
                    bsonType: "object",
                    title: "Country Validator",
                    properties: {
                        country: {
                            enum: ["FR", "CA"],
                            description: "doit être un pays francophone"
                        }
                    }
                },
                note: {
                    bsonType: "double",
                    description: "doit être un double"
                }
            }
        }
    }
});


db.posts.insertMany([
    {
        titre: "Premier article",
        auteur: "Jean",
        vues: 10,
        date: new Date(),
        note: 4.5
    },
    {
        titre: "Deuxième article",
        auteur: "Pierre",
        vues: 20,
        date: new Date(),
        note: 3.5
    },
    {
        titre: "Troisième article",
        auteur: "Jacques",
        vues: 30,
        date: new Date(),
        note: 2.5
    },
    {
        titre: "Quatrième article",
        auteur: "Marie",
        vues: 40,
        date: new Date(),
        note: 1.5,
        origin: {
            country: "CA"
        }
    },
    {
        titre: "Cinquième article",
        auteur: "Sophie",
        vues: 50,
        date: new Date(),
        origin: {
            country: "FR"
        },
        note: 0.5
    }
]);
