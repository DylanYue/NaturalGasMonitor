var express = require('express');
var router = express.Router();
var fs = require('fs');
var csv = require("fast-csv");

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {title: 'Express'});
});
router.get('/getData', async function (req, res, next) {
    var dataSample = [];
    console.log(__dirname + '/../../DataSample/Data.csv');
    var input = fs.createReadStream(__dirname + '/../../DataSample/Data.csv');
    var csvStream = csv()
        .on("data", function (data) {
            dataSample.push(data);
        })
        .on("end", function () {
            console.log("done", dataSample);
            res.json(dataSample);
        });
    input.pipe(csvStream);

})

module.exports = router;
