const express = require('express');
const { exec } = require('child_process');
const app = express();
const path = require('path');
const mongoose = require('mongoose');
require('dotenv').config();

app.use(express.static(path.join(__dirname, 'public')));

// Access environment variables using process.env
const port = process.env.PORT || 3000;
const uri =process.env.mongoDBconnect;
mongoose.connect(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log("Connected to MongoDB"))
.catch((err) => console.error("Error connecting to MongoDB", err));

const trending_topicSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    unique_id: String,
    trend1: String,
    trend2: String,
    trend3: String,
    trend4: String,
    trend5: String,
    end_time: String,
    ip_address: String
});
const trending_topic = mongoose.model('trending_topic', trending_topicSchema);
app.get('/run-script', (req, res) => {
    exec('python test.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Error running script');
        }
        console.log("Python script output:", stdout);
        trending_topic.find({})
        .then( (docs) => {
            console.log('DOne finding ... ABHISHEK');
            var n = docs.length;
            console.log(docs);
            res.json(docs);
        });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
