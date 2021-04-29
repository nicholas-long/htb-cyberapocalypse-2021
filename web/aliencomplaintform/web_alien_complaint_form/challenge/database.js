const sqlite = require('sqlite-async');

class Database {
    constructor(db_file) {
        this.db_file = db_file;
        this.db = undefined;
    }
    
    async connect() {
        this.db = await sqlite.open(this.db_file);
    }

    async migrate() {
        return this.db.exec(`
            DROP TABLE IF EXISTS feedback;

            CREATE TABLE IF NOT EXISTS feedback (
                id         INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
                complaint  VARCHAR(255) NOT NULL,
                species    VARCHAR(255) NOT NULL,
                created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
            );

            INSERT INTO feedback (complaint, species) VALUES ('Employee #1655 resolved to slurs once a mistake was pointed out.', 'Alien');
            INSERT INTO feedback (complaint, species) VALUES ('Employee #7843 ate my intergalactic donut.', 'Alien');
            INSERT INTO feedback (complaint, species) VALUES ('Employee #4933 made coffee for everyone except me.', 'Alien');
        `);
    }

    async addFeedback(complaint, species = 'Human') {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('INSERT INTO feedback (complaint, species) VALUES (? , ?)');
                resolve(await stmt.run(complaint, species));
            } catch(e) {
                reject(e);
            }
        });
    }

    async getFeedback() {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM feedback');
                resolve(await stmt.all());
            } catch(e) {
                reject(e);
            }
        });
    }
}

module.exports = Database;