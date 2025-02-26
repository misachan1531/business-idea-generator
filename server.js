// server.js
const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(bodyParser.json());
app.use(express.static('public'));

// Serve static files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Generate ideas endpoint
app.post('/generate-ideas', async (req, res) => {
    try {
        const { apiKey, budget, skills, interests, location } = req.body;

        const response = await fetch('https://api.perplexity.ai/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'sonar-pro',
                messages: [
                    {
                        role: 'system',
                        content: 'You are a business consultant.'
                    },
                    {
                        role: 'user',
                        content: `Generate 5 business ideas based on:
                            Budget: ${budget}
                            Skills: ${skills}
                            Interests: ${interests}
                            Location: ${location}`
                    }
                ]
            })
        });

        const data = await response.json();
        res.json({ ideas: data.choices[0].message.content });
    } catch (error) {
        res.json({ error: error.message });
    }
});

// Send email endpoint
app.post('/send-email', async (req, res) => {
    try {
        const { email, content } = req.body;

        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS
            }
        });

        await transporter.sendMail({
            from: process.env.EMAIL_USER,
            to: email,
            subject: 'Your Business Ideas',
            text: content,
            html: `<div style="font-family: Arial, sans-serif;">${content}</div>`
        });

        res.json({ success: true });
    } catch (error) {
        res.json({ error: error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});