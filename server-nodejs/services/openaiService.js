const OpenAI = require('openai');

let openaiClient = null;

function getOpenAIClient() {
  if (!openaiClient) {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      throw new Error('OPENAI_API_KEY is not configured');
    }
    openaiClient = new OpenAI({ apiKey });
  }
  return openaiClient;
}

/**
 * Generates a short, friendly welcome message in Hebrew for a new user using OpenAI.
 * @returns {Promise<{ success: true, message: string } | { success: false, error: string }>}
 */
async function generateHebrewWelcomeMessage() {
  const client = getOpenAIClient();
  const completion = await client.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      {
        role: 'system',
        content: 'You are a friendly assistant that creates warm, creative welcome messages in Hebrew for new users. Keep messages short (2-3 sentences), personal, and welcoming. Respond only with the Hebrew message, no explanations.'
      },
      {
        role: 'user',
        content: 'Create a short, creative welcome message in Hebrew for a new user joining our platform.'
      }
    ],
    max_tokens: 150,
    temperature: 0.8
  });

  const message = completion.choices[0]?.message?.content?.trim();
  if (!message) {
    throw new Error('OpenAI returned an empty welcome message');
  }
  return { success: true, message };
}

module.exports = {
  getOpenAIClient,
  generateHebrewWelcomeMessage
};
