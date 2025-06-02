"use client";

import React from 'react';
import styles from '../auth.module.css'
import { useState } from "react";
import { useRouter } from 'next/navigation';
import Link from 'next/link';

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

  //We need a FormData because we have special input (File..) which mean a basic JSON stringify can't work.
  function convertToFormData(): FormData {
    const formDataConvert = new FormData();

    for (const key in formData) {
      const value = formData[key];

      if (value === null || value === undefined) continue;

      if (value instanceof File)
        formDataConvert.append(key, value);
      else
        formDataConvert.append(key, String(value));
    }
    return formDataConvert;
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const dataToSend = convertToFormData();
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
    console.log('Registration successful:', dataToSend);
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <form id={styles.mainForm} onSubmit={handleSubmit}>
        <h1 style={{fontSize: '3em'}}>Register</h1>
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
              <input type="radio" name="preferredLanguage" value="eng" defaultChecked onChange={handleChange}/>
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
    </div>
  );
}
