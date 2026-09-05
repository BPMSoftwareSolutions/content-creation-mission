/* Vector/timing compiler only: no browser automation or provider execution. */
const fs = require('node:fs');
const flow = require('../templates/circuit-flow.js');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify({plan: flow.plan(input.projection, input.lengths), artwork: flow.sphereMarkup('episode-silver')}));
