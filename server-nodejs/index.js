const express = require('express');
const cors = require('cors');
const config = require('./config');
const routes = require('./routes');
const { errorHandler, notFoundHandler } = require('./middleware/errorHandler');

const app = express();

app.use(cors());
app.use(express.json());

// Health check
app.get('/', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Welcome Message API is running',
    endpoint: '/welcome-message'
  });
});

// Mount API routes
app.use('/', routes);

// 404 and global error handling
app.use(notFoundHandler);
app.use(errorHandler);

app.listen(config.port, () => {
  console.log(`🚀 Server running on http://localhost:${config.port}`);
  console.log(`📝 Welcome message: http://localhost:${config.port}/welcome-message`);
  if (!config.isOpenAiConfigured) {
    console.warn('⚠️  OPENAI_API_KEY is not set. Set it in .env to use /welcome-message.');
  }
});

module.exports = app;
