'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  let token = null;

  useEffect(() => {
    token = localStorage.getItem('token');

    if (token) {
      router.push('/');
    }
  }, []);

  if (!token) {
    return <div>Loading...</div>;
  }

  return <>{children}</>;
}