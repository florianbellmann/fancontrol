const readLastLine = require("read-last-line");
const path = require("path")

const fastify = require("fastify")({});

fastify.get("/logs", (request, reply) => {
        const filePath = path.join(__dirname, "log.txt")

        readLastLine
                .read(filePath, 200)
                .then(function (lines) {
                        reply.send(lines);
                })
                .catch(function (err) {
                        reply.send(filePath);
                });
});

fastify.listen(3003, "0.0.0.0", (err, address) => {
        if (err) throw err;
        console.log(`server listening on ${address}`);
});

