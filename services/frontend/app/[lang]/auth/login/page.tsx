"use client";

import React from 'react';
import styles from '../auth.module.css'
import { useState } from "react";
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {postData} from "@/lib/fetch-api";

export default function loginPage() {

  const router = useRouter();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const isValid: boolean = await postData("/users/login/", JSON.stringify(formData))
    if (isValid) {
      router.push('/');
    }
  };

  return (
    <form id={styles.mainForm} onSubmit={handleSubmit}>
      <h1 id={styles.mainTitle}>Login</h1>
      <input className="inputStyle1" name="username" type="text" placeholder="Username" onChange={handleChange}/>
      <input className="inputStyle1" name="password" type="password" placeholder="Password" onChange={handleChange}/>

      <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Login</button>
      <Link href="/auth/register">You don't have an account ?</Link>
    </form>
  );
}