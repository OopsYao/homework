const fs = require('fs');
const path = require('path');

const getStructure = docAsset => {
    const structure = {};
    fs.readdirSync(docAsset).forEach(cat => {
        structure[cat] = []
        fs.readdirSync(path.join(docAsset, cat)).forEach(subcat => {
            structure[cat].push(subcat.substring(0, subcat.length - 4)) // Trim suffix
        })
    });
    return structure;
}

module.exports = getStructure