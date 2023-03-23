const { request } = require("undici");
const fs = require("fs")
const path = require("path")

async function userNameToUUID(userName) {
    return await request(`https://api.mojang.com/users/profiles/minecraft/${userName}`)
        .then(result => result.body.json())
        .then(json => json.id)
        .catch(error => console.warn('Error occured during fetching UUID: ' + error.message));
}

function findJSFiles(dirPath, arrayOfFiles) {
    files = fs.readdirSync(dirPath)

    arrayOfFiles = arrayOfFiles || []
  
    files.forEach(function(file) {
      if (fs.statSync(dirPath + "/" + file).isDirectory()) {
        arrayOfFiles = findJSFiles(dirPath + "/" + file, arrayOfFiles)
      } else {
        if (file.endsWith('.js')) {
            arrayOfFiles.push(path.join(dirPath, "/", file))
        }
      }
    })
  
    return arrayOfFiles
}

module.exports = {userNameToUUID, findJSFiles};
