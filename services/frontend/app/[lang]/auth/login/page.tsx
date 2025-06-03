"use client";

import React from 'react';
import styles from '../auth.module.css'
import { useState } from "react";
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function loginPage() {

  const router = useRouter();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  }


  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const form = event.target as HTMLFormElement;
    const username = (form.elements.namedItem('username') as HTMLInputElement).value;
    const password = (form.elements.namedItem('password') as HTMLInputElement).value;
    const dataToSend = {
      username,
      password
    };

    console.log(dataToSend)

    try {
      const response = await fetch('/users/login/', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSend),
        credentials: "include"
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Login failed:', errorData);
        return;
      }

      const result = await response.json();
      console.log(result)
      router.push('/');
    } catch (err) {
      console.error('Login failed:', err);
    }
    console.log('Login:', dataToSend);
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <form id={styles.mainForm} onSubmit={handleSubmit}>
        <h1 style={{fontSize: '3em'}}>Login</h1>
        <input className="inputStyle1" name="username" type="text" placeholder="Username" onChange={handleChange}/>
        <input className="inputStyle1" name="password" type="password" placeholder="Password" onChange={handleChange}/>

        <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Login</button>
        <Link href="/auth/register">You don't have an account ?</Link>
      </form>
    </div>
  );
}