/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // Enables deployment anywhere
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: '*' },
        ],
      },
    ];
  },
  // Add transpilePackages to ensure proper bundling
  transpilePackages: ['framer-motion'],
  // Enable experimental features if needed
  experimental: {
    serverActions: true,
  }
};

module.exports = nextConfig;
