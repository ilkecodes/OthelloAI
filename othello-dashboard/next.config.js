/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const backend = process.env.BACKEND_URL || 'http://localhost:8000';
    return [{ source: '/api/:path*', destination: `${backend}/api/:path*` }];
  },
  // 🚀 Build sırasında ESLint HATALARINI yok say
  eslint: {
    ignoreDuringBuilds: true,
  },
  // (İsteğe bağlı) Type-check'i de Vercel build'inde pas geçmek istersen:
  typescript: {
    ignoreBuildErrors: true,
  },
};

module.exports = nextConfig;

