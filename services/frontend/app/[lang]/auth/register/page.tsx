"use client";

import React from 'react';
import styles from '../auth.module.css'
import { useState } from "react";
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { convertToFormData } from '@/lib/utils'

export default function registerPage() {

  const router = useRouter();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirmPassword: "",
    email: "",
    first_name: "",
    last_name: "",
    preferredLanguage: "eng",
    profilePicture: null as File | null,
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const dataToSend = convertToFormData(formData);
    try {
      const response = await fetch('/users/register/', {
        method: 'POST',
        body: dataToSend,
        credentials: "include"
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Registration failed:', errorData);
        return;
      }

      const result = await response.json();
      console.log(result)
      router.push('/');
    } catch (err) {
      console.error('Request failed:', err);
    }
  };

  return (
    <form id={styles.mainForm} onSubmit={handleSubmit}>
      <h1 id={styles.mainTitle}>Register</h1>
      <input className="inputStyle1" name="username" type="text" placeholder="Username" onChange={handleChange}/>
      <input className="inputStyle1" name="password" type="password" placeholder="Password" onChange={handleChange}/>
      <input className="inputStyle1" name="confirmPassword" type="password" placeholder="Password confirmation" onChange={handleChange}/>
      <input className="inputStyle1" name="email" type="email" placeholder="Email" onChange={handleChange}/>
      <input className="inputStyle1" name="first_name" type="text" placeholder="First Name" onChange={handleChange}/>
      <input className="inputStyle1" name="last_name" type="text" placeholder="Last Name" onChange={handleChange}/>
      <fieldset>
        <legend>Preferred language</legend>

        <div style={{display: 'flex', gap: '15px'}}>
          <label className="custom-radio">
            <input type="radio" name="preferredLanguage" value="en" defaultChecked onChange={handleChange}/>
            <span className="radio-mark"></span>
            English
          </label>

          <label className="custom-radio">
            <input type="radio" name="preferredLanguage" value="fr" onChange={handleChange}/>
            <span className="radio-mark"></span>
            French
          </label>
        </div>
      </fieldset>
      <span>
          <div>Profile picture (optional)</div>
          <input className="uploadInputFile" type="file" name="profilePicture" accept="image/*" onChange={handleChange}/>
      </span>
      <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Register</button>
      <Link href="/auth/login">Already register ?</Link>
    </form>
  );
}
