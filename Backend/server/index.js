require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://127.0.0.1:5000';

// Middleware
app.use(cors({
  origin: '*', // Allows all domains. For better security, you can change this to your exact Vercel URL later.
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type']
}));
app.use(express.json());

// Routes
app.post('/api/classify', async (req, res) => {
  try {
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Email text is required' });
    }

    // Call the Python ML microservice
    let mlResponse;
    try {
      mlResponse = await axios.post(`${ML_SERVICE_URL}/predict`, { text });
    } catch (mlError) {
      console.error('Error calling ML service:', mlError.message);
      return res.status(503).json({ error: 'Machine Learning service is unavailable. Did you start the Python backend?' });
    }

    const prediction = mlResponse.data.prediction;

    // Send prediction back directly without saving to a database
    res.json({
      success: true,
      prediction
    });

  } catch (error) {
    console.error('Classification error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
