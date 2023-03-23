const { findJSFiles } = require("./src/utils");
const path = require('node:path');

const jobsPath = path.join(__dirname, 'src/jobs');
for (const filePath of findJSFiles(jobsPath)) {
    console.log(filePath);
}
