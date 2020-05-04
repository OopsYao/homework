const putFile = file => {
    console.time(`Job: file ${file}`)
    console.log(`Start uploading file ${file}`)
    return new Promise(resolve => setTimeout(resolve, 2000 * (1 + Math.random())))
        .then(() => {
            if (Math.random() < 0.1) { throw `Network error: upload file ${file} failed` }
            console.timeEnd(`Job: file ${file}`)
        })
}

(async () => {
    console.time('Total')
    const pl = []
    for (let i = 1; i < 10; i++) {
        pl.push(putFile(`File ${i}`).catch(err => {
            console.log(err)
            return `File ${i}`
        }))
    }
    const rl = (await Promise.all(pl)).filter(errFile => errFile !== undefined)
    console.log(`Failure list: ${rl}`)
    console.timeEnd('Total')
})()
