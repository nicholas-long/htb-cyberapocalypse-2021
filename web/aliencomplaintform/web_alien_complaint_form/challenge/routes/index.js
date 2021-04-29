const bot = require('../bot');

let db;

async function router (fastify, options) {
	fastify.get('/', async (request, reply) => {
		return reply.sendFile('index.html');
	});

	fastify.get('/list', async (request, reply) => {
		if (request.ip != '127.0.0.1') {
			return reply.code(401).header('Content-Type', 'application/json; charset=utf-8').send({ message: 'Only localhost is allowed'});
		}
		return reply.sendFile('list.html');
	});

	fastify.post('/api/submit', async (request, reply) => {
		let { complaint } = request.body;
		
		if (complaint) {
			return db.addFeedback(complaint)
				.then(() => {
					// bot.purgeHumanEntries(db);
					reply.send({ message: 'The Galactic Federation has processed your feedback.' });
				})
				.catch(() => reply.send({ message: 'The Galactic Federation spaceship controller has crashed.', error: 1}));
		}

		return reply.send({ message: 'Missing parameters.', error: 1 });
	});

	fastify.get('/api/jsonp', async (request, reply) => {
		let callback = request.query.callback || 'display';
		reply.header('Content-Type', 'application/javascript');
		let feedback = await db.getFeedback()
			.then(feedback => {
				if (feedback) {
					return feedback;
				}
				return 'The Galactic Federation archives appear to be empty.';
			})
			.catch(() => {
				return 'The Galactic Federation spaceship controller has crashed.';
			});
		reply.send(`${callback}(${JSON.stringify(feedback)})`);
	});
}

module.exports = database => {
	db = database;
	return router;
};