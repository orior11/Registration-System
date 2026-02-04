const OpenAI = require('openai');

/**
 * Centralized error handler middleware.
 * Sends appropriate status codes and JSON error responses.
 */
function errorHandler(err, req, res, next) {
  console.error('Error:', err);

  // OpenAI API errors
  if (err instanceof OpenAI.APIError) {
    return res.status(err.status || 500).json({
      success: false,
      error: 'OpenAI API error',
      message: err.message,
      type: err.type || 'unknown'
    });
  }

  // Network / connection errors
  if (err.code === 'ECONNREFUSED' || err.code === 'ETIMEDOUT' || err.code === 'ENOTFOUND') {
    return res.status(503).json({
      success: false,
      error: 'Service unavailable',
      message: 'Unable to reach OpenAI. Please check your network and API key.'
    });
  }

  // Validation / config errors
  if (err.message && err.message.includes('OPENAI_API_KEY')) {
    return res.status(503).json({
      success: false,
      error: 'Configuration error',
      message: err.message
    });
  }

  // Default: 500
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: err.message || 'An unexpected error occurred'
  });
}

/**
 * 404 handler for unknown routes.
 */
function notFoundHandler(req, res) {
  res.status(404).json({
    success: false,
    error: 'Not found',
    message: `Route ${req.method} ${req.path} not found`
  });
}

module.exports = {
  errorHandler,
  notFoundHandler
};
