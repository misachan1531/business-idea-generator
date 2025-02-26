// script.js
async function generateIdeas() {
    const apiKey = document.getElementById('apiKey').value;
    const budget = document.getElementById('budget').value;
    const skills = document.getElementById('skills').value;
    const interests = document.getElementById('interests').value;
    const location = document.getElementById('location').value;

    // Validation
    if (!apiKey || !skills || !interests || !location) {
        alert('Please fill in all required fields');
        return;
    }

    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    try {
        const response = await fetch('/generate-ideas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                apiKey,
                budget,
                skills,
                interests,
                location
            })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Display results
        document.getElementById('ideasContent').innerHTML = data.ideas;
        document.getElementById('results').classList.remove('hidden');
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    const content = document.getElementById('ideasContent').innerText;
    const title = "Business Ideas Report";
    const date = new Date().toLocaleDateString();

    doc.setFontSize(16);
    doc.text(title, 20, 20);
    
    doc.setFontSize(12);
    doc.text(`Generated on: ${date}`, 20, 30);

    doc.setFontSize(10);
    const splitContent = doc.splitTextToSize(content, 170);
    doc.text(splitContent, 20, 40);

    doc.save('business-ideas.pdf');
}

function showEmailForm() {
    const email = prompt("Enter your email address:");
    if (email) {
        sendEmail(email);
    }
}

async function sendEmail(email) {
    try {
        const response = await fetch('/send-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                content: document.getElementById('ideasContent').innerText
            })
        });

        const data = await response.json();
        if (data.success) {
            alert('Email sent successfully!');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        alert('Error sending email: ' + error.message);
    }
}