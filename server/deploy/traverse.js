const fs = require('fs')
const path = require('path')

let DIR = '' 
const filelist = []
function traverseDir(dir) {
    fs.readdirSync(dir).forEach(file => {
        let fullPath = path.join(dir, file);
        if (fs.lstatSync(fullPath).isDirectory()) {
            traverseDir(fullPath);
        } else {
            filelist.push([fullPath.substr(1 + DIR.length), fullPath])
        }
    });
}

module.exports = dir => {
    DIR = dir
    traverseDir(dir)
    return filelist
}