const readLastLine = require("read-last-line");

const fastify = require("fastify")({});

fastify.get("/logs", (request, reply) => {
  readLastLine
    .read("./logs.txt", 100)
    .then(function (lines) {
      reply.send(lines);
    })
    .catch(function (err) {
      reply.send("error");
    });
});

fastify.listen(3003, "0.0.0.0", (err, address) => {
  if (err) throw err;
  console.log(`server listening on ${address}`);
});

