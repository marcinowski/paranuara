use paranuara
db.dropDatabase()
db.createUser({user: "mongouser", pwd: "password", roles: []});
