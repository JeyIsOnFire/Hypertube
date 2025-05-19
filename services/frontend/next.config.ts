import type { NextConfig } from "next";
import { loadEnvConfig } from "@next/env";

const envFileDir = process.cwd() + "/../../";
loadEnvConfig(envFileDir);


const nextConfig: NextConfig = {
	middleware: true,
  env: {
    NEXT_PUBLIC_HOSTNAME: process.env.NEXT_PUBLIC_HOSTNAME,
  }
};

module.exports = nextConfig;
//export default nextConfig;
