const mongoose = require('mongoose');

const EmailLogSchema = new mongoose.Schema({
  text: {
    type: String,
    required: true
  },
  prediction: {
    type: String,
    enum: ['spam', 'not spam'],
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('EmailLog', EmailLogSchema);
