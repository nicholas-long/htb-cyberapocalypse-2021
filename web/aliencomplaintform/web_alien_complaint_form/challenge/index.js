const fastify  = require('fastify')({
    logger:true
});
const routes   = require('./routes');
const path     = require('path');
const Database = require('./database');

const db = new Database('feedback.db');

fastify.register(require('fastify-formbody'));
fastify.register(routes(db));
fastify.register(require('fastify-static'), {
    root: path.join(__dirname, 'public'),
    prefix: '/'
});

(async () => {
    await db.connect();
    await db.migrate();
    fastify.listen(1337, '0.0.0.0', (err, address) => {
        if (err) {
            fastify.log.error(err);
            process.exit(1);
        }
        fastify.log.info(`Server listening on ${address}`);
    });
})();