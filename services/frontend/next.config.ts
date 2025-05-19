import type { NextConfig } from "next";

console.log("NEXT_PUBLIC_HOSTNAME", process.env.NEXT_PUBLIC_HOSTNAME);
const nextConfig: NextConfig = {
	middleware: true,
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
