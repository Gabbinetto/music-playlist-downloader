// index.js

const ytdl = require('ytdl-core');
const ytpl = require('ytpl');
const fs = require('fs');
const express = require('express');
const archiver = require('archiver');

const indexHtml = fs.readFileSync('index.html')

const app = new express();
// https://www.youtube.com/playlist?list=PL7_XL8L2PxkolJPc__sZgkAl0_qLQBc-x

app.get('/', (req, res) => {
    res.end(indexHtml);  
})

app.get('/download', async (req, res) => {
    let id = req.query.url;
    let playlist;
    await ytpl(id).then((result) => playlist = result);
    
    // Downloading
    let streams = [];
    
    for (let item of playlist.items) {
        const video = ytdl(item.url, {
            filter: 'audioonly'
        });
        streams.push({
            name: item.title,
            stream: video
        })
        
    }

    res.send(streams);

    const archive = archiver('zip', {'zlib': {'level': 9}})
    archive.pipe(fs.createWriteStream(`${playlist.title}.zip`))

    for (let stream of streams) {
        archive.append(stream.stream, {name: stream.name})
    }

    archive.finalize();

    res.end();
})

app.listen(3000)
console.log('Server started at localhost:3000')