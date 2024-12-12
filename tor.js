const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname)));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'ui.html'));
});

app.get('/run-script', (req, res) => {
    const url = req.query.url;
    const urlRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;
    if (!url || !urlRegex.test(url)) {
        return res.status(400).send("Invalid input. Provide a valid YouTube 'url'.");
    }

    console.log('Received URL:', url);

    const scriptPath = path.join(__dirname, 'soul.py');
    console.log('Executing Python script...');

    const pythonProcess = spawn('python', [scriptPath, url]);

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    pythonProcess.stdout.on('data', (data) => {
        const message = data.toString();
        console.log(message);
        res.write(`data: ${message}\n\n`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error('Error:', data.toString());
        res.write(`event: error\ndata: ${data.toString()}\n\n`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Script exited with code ${code}`);
        res.write(`event: complete\ndata: Script finished with code ${code}\n\n`);
        res.end();
    });

    pythonProcess.on('error', (err) => {
        console.error('Failed to start Python process:', err.message);
        res.write(`event: error\ndata: ${err.message}\n\n`);
        res.end();
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
