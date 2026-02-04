const OpenAI = require('openai');
const { generateHebrewWelcomeMessage } = require('../services/openaiService');
const config = require('../config');

/**
 * GET /welcome-message
 * Generates a friendly Hebrew welcome message using OpenAI and returns it.
 */
async function getWelcomeMessage(req, res, next) {
  try {
    if (!config.isOpenAiConfigured) {
      return res.status(503).json({
        success: false,
        error: 'Service unavailable',
        message: 'OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file.'
      });
    }

    const result = await generateHebrewWelcomeMessage();
    return res.json({
      success: true,
      message: result.message,
      language: 'hebrew',
      model: 'gpt-4o-mini'
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  getWelcomeMessage
};
