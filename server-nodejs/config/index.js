require('dotenv').config();

module.exports = {
  port: parseInt(process.env.PORT, 10) || 3000,
  openaiApiKey: process.env.OPENAI_API_KEY || '',
  isOpenAiConfigured: Boolean(process.env.OPENAI_API_KEY?.trim())
};
