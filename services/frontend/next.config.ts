import type { NextConfig } from "next";

const nextConfig: NextConfig = {
	middleware: true,
  env: {
    NEXT_PUBLIC_HOSTNAME: process.env.NEXT_PUBLIC_HOSTNAME,
  }
};

module.exports = nextConfig;
//export default nextConfig;
