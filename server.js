// server.js
const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.post('/submit', (req, res) => {
    const { name, studentId, githubLink } = req.body;
    
    // Format: Name, ID, Link, Date
    const csvLine = `${name},${studentId},${githubLink},${new Date().toISOString()}\n`;

    // Append data to submissions.csv
    fs.appendFile('submissions.csv', csvLine, (err) => {
        if (err) {
            console.error(err);
            return res.status(500).send('Error saving data');
        }
        res.status(200).send('Data saved!');
    });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
