const express = require('express');
const { getWelcomeMessage } = require('../controllers/welcomeMessageController');

const router = express.Router();

router.get('/welcome-message', getWelcomeMessage);

module.exports = router;
