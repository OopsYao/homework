const qiniu = require('qiniu')
const mime = require('mime-types')
const getfilelist = require('./traverse')
const {
    accessKey,
    secretKey,
    bucket
} = require('./keypair.config')


const mac = new qiniu.auth.digest.Mac(accessKey, secretKey);

// Overseas host
qiniu.conf.UP_HOST = 'up.qiniug.com'
const config = new qiniu.conf.Config();
// 空间对应的机房
config.zone = qiniu.zone.Zone_z0;
// 是否使用https域名
config.useHttpsDomain = true;
// 上传是否使用cdn加速
config.useCdnDomain = true;

const formUploader = new qiniu.form_up.FormUploader(config);
// Wrap formUploader.putFile with Promise
const putFile = (uploadToken, key, localFile, putExtra) =>
    new Promise((resolve, reject) => {
        formUploader.putFile(uploadToken, key, localFile, putExtra,
            (respErr, respBody, respInfo) => {
                if (respErr) {
                    reject(respErr);
                }
                if (respInfo.statusCode == 200) {
                    resolve(respBody)
                } else {
                    reject(respBody)
                }
            });
    })

const DIST_DIR = 'dist'
const filelist = getfilelist(DIST_DIR)
// Set default 404 page
filelist.push(['errno-404', `${DIST_DIR}/index.html`])

// Upload files in filelist
async function upload(filelist) {
    const pl = []
    filelist.forEach(file => {
        const localFile = file[1];
        const remoteFile = file[0];
        // To cover an existed file
        const options = { scope: `${bucket}:${remoteFile}` };
        const putPolicy = new qiniu.rs.PutPolicy(options);
        const uploadToken = putPolicy.uploadToken(mac);

        // Set MIME, A remote name is sufficient
        const putExtra = new qiniu.form_up.PutExtra(mimeType = mime.lookup(remoteFile));
        pl.push(
            putFile(uploadToken, remoteFile, localFile, putExtra).catch(error => {
                console.log(error);
                throw file;
            })
        )
    });
    // Collect failed filelist after all promises resolved
    // Since there is no resolve handler for `push`, the resolved value would be `undefined`
    return (await Promise.all(pl)).filter(errFile => errFile !== undefined);
}

(async () => {
    const maxFailure = 2;
    let failurelist = filelist;
    for (_ of [...Array(maxFailure)]) {
        if (failurelist.length == 0) {
            console.log('No failure, no retry needed')
        } else {
            failurelist = await upload(failurelist);
            console.log(`Failures: ${failurelist.length}`)
        }
    }
})()