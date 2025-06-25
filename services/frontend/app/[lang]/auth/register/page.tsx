"use client";

import React from 'react';
import styles from '../auth.module.css'
import { useState } from "react";
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {convertToFormData, isDataFilled} from '@/lib/utils'
import {postData} from "@/lib/fetch-api";
import toast from "react-hot-toast";
import OAuth from "@/app/[lang]/auth/oauth/page";

export default function registerPage() {

  const router = useRouter();
  const initialFormData = {
    username: "",
    password: "",
    confirm_password: "",
    email: "",
    first_name: "",
    last_name: "",
    preferred_language: "en",
    profile_picture: null as File | null,
  };

  const [formData, setFormData] = useState(initialFormData);

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
    const isValid: boolean = await postData("/users/register/", dataToSend);
    if (isValid) {
      toast.success("Registration completed")
      router.push('/');
    } else toast.error("Error registration");
    setFormData(initialFormData);
  };

  function getValuesExceptFile(): string[] {
      return Object.entries(formData)
          .filter(([key]) => key !== "profile_picture")
          .map(([_, value]) => (typeof value === 'string' ? value : ''));
  }

  return (
    <form id={styles.mainForm} onSubmit={handleSubmit}>
      <h1 id={styles.mainTitle}>Register</h1>
      <input className="inputStyle1" name="username" type="text" placeholder="Username" value={formData.username} onChange={handleChange}/>
      <input className="inputStyle1" name="password" type="password" placeholder="Password" value={formData.password} onChange={handleChange}/>
      <input className="inputStyle1" name="confirm_password" type="password" placeholder="Password confirmation" value={formData.confirm_password} onChange={handleChange}/>
      <input className="inputStyle1" name="email" type="email" placeholder="Email" value={formData.email} onChange={handleChange}/>
      <input className="inputStyle1" name="first_name" type="text" placeholder="First Name" value={formData.first_name} onChange={handleChange}/>
      <input className="inputStyle1" name="last_name" type="text" placeholder="Last Name" value={formData.last_name} onChange={handleChange}/>
      <fieldset>
        <legend>Preferred language</legend>

        <div style={{display: 'flex', gap: '15px'}}>
          <label className="custom-radio">
            <input type="radio" name="preferred_language" value="en"  checked={formData.preferred_language === 'en'} onChange={handleChange}/>
            <span className="radio-mark"></span>
            English
          </label>

          <label className="custom-radio">
            <input type="radio" name="preferred_language" value="fr" checked={formData.preferred_language === 'fr'} onChange={handleChange}/>
            <span className="radio-mark"></span>
            French
          </label>
        </div>
      </fieldset>
      <span>
          <div>Profile picture (optional)</div>
          <input className="uploadInputFile" type="file" name="profilePicture" accept="image/*" onChange={handleChange}/>
      </span>
      <button className={styles.button} type="submit" disabled={!isDataFilled(getValuesExceptFile())}>Register</button>

      <OAuth></OAuth>

      <Link href="/auth/login">Already register ?</Link>
    </form>
  );
}
