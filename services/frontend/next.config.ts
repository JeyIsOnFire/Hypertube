import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    NEXT_PUBLIC_HOSTNAME: process.env.NEXT_PUBLIC_HOSTNAME,
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'image.tmdb.org',
        port: '',
        pathname: '/t/p/**',
      },
    ],
  },
};

module.exports = nextConfig;
