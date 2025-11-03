/** @type {import('next').NextConfig} */
const nextConfig = {
  // Prod'da backend'e proxy
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://othello-backend-production-2ff4.up.railway.app/api/:path*',
      },
    ];
  },

  // Hızlı deploy için lint’i build’te atla (sonra açarız)
  eslint: {
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig;
