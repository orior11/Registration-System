import React, { useState } from 'react';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: { email?: string; password?: string } = {};

    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      console.log('Form submitted:', { email, password });
      // Handle login logic here
    }
  };

  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    console.log(`Login with ${provider}`);
    // Handle social login logic here
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-[1000px] bg-white rounded-3xl shadow-lg overflow-hidden">
        <div className="flex flex-col md:flex-row min-h-[600px]">
          {/* Left Panel - Decorative */}
          <div className="hidden md:flex md:w-1/2 bg-brand-blue items-center justify-center p-12">
            <div className="text-center space-y-6">
              {/* Illustration Container */}
              <div className="flex justify-center mb-8">
                <div className="w-72 h-72 relative">
                  {/* Modern abstract illustration */}
                  <svg
                    viewBox="0 0 300 300"
                    className="w-full h-full"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    {/* Background decorative circles */}
                    <circle cx="150" cy="150" r="100" fill="rgba(255,255,255,0.1)" />
                    <circle cx="150" cy="150" r="70" fill="rgba(255,255,255,0.15)" />
                    
                    {/* Main central icon - Security/Lock theme */}
                    <g transform="translate(150, 150)">
                      {/* Shield shape */}
                      <path
                        d="M 0 -60 L 40 -45 L 40 0 C 40 30 20 50 0 60 C -20 50 -40 30 -40 0 L -40 -45 Z"
                        fill="rgba(255,255,255,0.9)"
                        stroke="rgba(255,255,255,1)"
                        strokeWidth="2"
                      />
                      
                      {/* Lock icon inside shield */}
                      <rect x="-15" y="-5" width="30" height="25" rx="3" fill="#3B4CB8" />
                      <path
                        d="M -10 -5 L -10 -15 C -10 -21 -5.5 -25 0 -25 C 5.5 -25 10 -21 10 -15 L 10 -5"
                        fill="none"
                        stroke="#3B4CB8"
                        strokeWidth="3"
                        strokeLinecap="round"
                      />
                      <circle cx="0" cy="5" r="3" fill="rgba(255,255,255,0.9)" />
                      <rect x="-1" y="7" width="2" height="8" fill="rgba(255,255,255,0.9)" />
                    </g>
                    
                    {/* Floating decorative elements */}
                    <circle cx="80" cy="80" r="4" fill="rgba(255,255,255,0.6)">
                      <animate attributeName="cy" values="80;75;80" dur="3s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="220" cy="100" r="3" fill="rgba(255,255,255,0.5)">
                      <animate attributeName="cy" values="100;95;100" dur="4s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="90" cy="220" r="3" fill="rgba(255,255,255,0.5)">
                      <animate attributeName="cy" values="220;215;220" dur="3.5s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="210" cy="210" r="4" fill="rgba(255,255,255,0.6)">
                      <animate attributeName="cy" values="210;205;210" dur="4.5s" repeatCount="indefinite" />
                    </circle>
                    
                    {/* Decorative rings around */}
                    <circle cx="70" cy="150" r="8" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="2" />
                    <circle cx="230" cy="150" r="8" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="2" />
                    <circle cx="150" cy="70" r="8" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="2" />
                    <circle cx="150" cy="230" r="8" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="2" />
                    
                    {/* Corner accents */}
                    <path d="M 40 40 L 40 50 M 40 40 L 50 40" stroke="rgba(255,255,255,0.4)" strokeWidth="2" strokeLinecap="round" />
                    <path d="M 260 40 L 260 50 M 260 40 L 250 40" stroke="rgba(255,255,255,0.4)" strokeWidth="2" strokeLinecap="round" />
                    <path d="M 40 260 L 40 250 M 40 260 L 50 260" stroke="rgba(255,255,255,0.4)" strokeWidth="2" strokeLinecap="round" />
                    <path d="M 260 260 L 260 250 M 260 260 L 250 260" stroke="rgba(255,255,255,0.4)" strokeWidth="2" strokeLinecap="round" />
                  </svg>
                </div>
              </div>

              {/* Text Content */}
              <div className="space-y-3">
                <h1 className="text-white font-bold text-[28px] leading-tight">
                  Welcome aboard my friend
                </h1>
                <p className="text-white text-[15px] opacity-70">
                  just a couple of clicks and we start
                </p>
              </div>
            </div>
          </div>

          {/* Right Panel - Form */}
          <div className="w-full md:w-1/2 p-8 md:p-16 flex items-center justify-center">
            <div className="w-full max-w-[360px] space-y-5">
              {/* Header */}
              <div className="text-center mb-6">
                <h2 className="text-blue-600 text-xl font-semibold">Log in</h2>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Email Input */}
                <div>
                  <label htmlFor="email" className="sr-only">
                    Email
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <svg
                        className="h-5 w-5 text-gray-400"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                        />
                      </svg>
                    </div>
                    <input
                      id="email"
                      name="email"
                      type="email"
                      autoComplete="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className={`w-full pl-10 pr-4 py-2.5 bg-gray-50 border ${
                        errors.email ? 'border-red-400' : 'border-gray-200'
                      } rounded-xl text-sm focus:outline-none focus:bg-white focus:border-blue-400 transition-colors placeholder:text-gray-400`}
                      placeholder="Email"
                      aria-label="Email address"
                      aria-invalid={!!errors.email}
                      aria-describedby={errors.email ? 'email-error' : undefined}
                    />
                  </div>
                  {errors.email && (
                    <p id="email-error" className="mt-1 text-sm text-red-600">
                      {errors.email}
                    </p>
                  )}
                </div>

                {/* Password Input */}
                <div>
                  <label htmlFor="password" className="sr-only">
                    Password
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <svg
                        className="h-5 w-5 text-gray-400"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                        />
                      </svg>
                    </div>
                    <input
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      autoComplete="current-password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={`w-full pl-10 pr-10 py-2.5 bg-gray-50 border ${
                        errors.password ? 'border-red-400' : 'border-gray-200'
                      } rounded-xl text-sm focus:outline-none focus:bg-white focus:border-blue-400 transition-colors placeholder:text-gray-400`}
                      placeholder="Password"
                      aria-label="Password"
                      aria-invalid={!!errors.password}
                      aria-describedby={errors.password ? 'password-error' : undefined}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? (
                        <svg
                          className="h-5 w-5 text-gray-400 hover:text-gray-600 transition-colors"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                          />
                        </svg>
                      ) : (
                        <svg
                          className="h-5 w-5 text-gray-400 hover:text-gray-600 transition-colors"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                          />
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                          />
                        </svg>
                      )}
                    </button>
                  </div>
                  {errors.password && (
                    <p id="password-error" className="mt-1 text-sm text-red-600">
                      {errors.password}
                    </p>
                  )}
                </div>

                {/* Forgot Password Link */}
                <div className="flex justify-end -mt-1">
                  <a
                    href="#"
                    className="text-xs text-blue-600 hover:text-blue-700 transition-colors"
                  >
                    Forgot password?
                  </a>
                </div>

                {/* Login Button */}
                <button
                  type="submit"
                  className="w-full bg-button-primary hover:bg-button-primary-hover text-white py-2.5 rounded-full font-medium text-sm transition-all duration-200 hover:shadow-md active:scale-[0.98] mt-4"
                  aria-label="Log in"
                >
                  Log in
                </button>

                {/* Divider */}
                <div className="text-center py-3">
                  <span className="text-xs text-gray-400">Or</span>
                </div>

                {/* Social Login Buttons */}
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => handleSocialLogin('google')}
                    className="flex items-center justify-center gap-1.5 py-2.5 px-3 bg-white border border-gray-200 rounded-full hover:bg-gray-50 transition-all duration-200 active:scale-[0.98]"
                    aria-label="Log in with Google"
                  >
                    <svg className="w-4 h-4" viewBox="0 0 24 24">
                      <path
                        fill="#4285F4"
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      />
                      <path
                        fill="#34A853"
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      />
                      <path
                        fill="#FBBC05"
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      />
                      <path
                        fill="#EA4335"
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      />
                    </svg>
                    <span className="text-xs font-medium text-gray-600">Google</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleSocialLogin('facebook')}
                    className="flex items-center justify-center gap-1.5 py-2.5 px-3 bg-white border border-gray-200 rounded-full hover:bg-gray-50 transition-all duration-200 active:scale-[0.98]"
                    aria-label="Log in with Facebook"
                  >
                    <svg className="w-4 h-4" viewBox="0 0 24 24">
                      <path
                        fill="#1877F2"
                        d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"
                      />
                    </svg>
                    <span className="text-xs font-medium text-gray-600">Facebook</span>
                  </button>
                </div>

                {/* Register Link */}
                <div className="pt-3">
                  <p className="text-center text-xs text-gray-500 mb-3">
                    Have no account yet?
                  </p>
                  <button
                    type="button"
                    onClick={() => console.log('Navigate to register')}
                    className="w-full py-2.5 border border-blue-600 text-blue-600 rounded-full font-medium text-sm hover:bg-blue-50 transition-all duration-200 active:scale-[0.98]"
                    aria-label="Register for a new account"
                  >
                    Register
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
