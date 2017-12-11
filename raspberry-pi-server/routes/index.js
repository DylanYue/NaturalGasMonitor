var express = require('express');
var router = express.Router();
var fs = require('fs');
var csv = require("fast-csv");
var path = require('path');
var Promise = require('bluebird');
var moment = require('moment');

const filePath = __dirname + '/../../NaturalGasMonitor/data/';
/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {title: 'Express'});
});
router.get('/getData', async function (req, res, next) {
    var dataSample = [];
    var input = fs.createReadStream(filePath+'Data.csv');
    var csvStream = csv()
    .on("data", function (data) {
        dataSample.push(data);
    })
    .on("end", function () {
        console.log("done", dataSample);
        res.json(dataSample);
    });
    input.pipe(csvStream);

});

router.get('/getFile/:name', async function (req, res, next) {
    let file = req.params.name;
    let result = await fs.readFileSync(filePath + file, 'utf8');
    console.log(result);
    res.json({file, result});
});

router.get('/getAllFiles', async function(req, res, next) {
    let result = [];
    await fs.readdir(filePath, function(err, items) {
        for (let item of items) {
            let info = getFileInfo(filePath+item);
            result.push({
                fileName: item,
                size: (info.size / 1000000).toFixed(2),
                birthtime: info.birthtime,
                duration: info.duration,
            })
        }
        res.json(result.sort(function(a, b) {
            return b.birthtime - a.birthtime;
        }));
    });

});

router.delete('/deleteFile/:name', async function(req, res, next) {
    let fileName = req.params.name
    fs.unlinkSync(filePath+fileName);
    res.send("delete success");
});
function getFileInfo(filename) {
    var stats = fs.statSync(filename);    
    return {
        birthtime: moment(stats["birthtime"]).format("YY-MM-DD HH:mm"),
        size: stats["size"],
        duration: moment.duration(moment(stats['mtime']).diff(moment(stats['birthtime']))).asHours().toFixed(1),
    }
}


module.exports = router;
